import os
from typing import Dict

import numpy as np
import pandas as pd
import torch
from torch_geometric.data import Batch, Data

from src.config import (
    DDIM_INFERENCE_STEPS,
    FINAL_FEATURE_COLS,
    LOG_PRECIP_MAX,
    FINAL_TARGET_COLS,
    MAIN_NODE_NAME,
    NODE_NAMES,
    PRECIP_PHYSICAL_MAX_MM,
    STAR_EDGE_COUNT,
    TARGET_NODE_POLICY,
    ZSCORE_EPSILON,
    build_star_edge_attr,
    build_star_edge_index,
    harmonize_weather_columns,
    validate_feature_schema,
    validate_feature_values,
)
from src.models.diffusion import ConditionalDiffusionModel, RainForecaster
from src.models.gnn import SpatioTemporalGNN
from src.retrieval.base import RetrievalDatabase


def _build_edge_index_from_config(config: Dict[str, object], device: torch.device) -> torch.Tensor:
    node_names = config.get("node_names", NODE_NAMES)
    star_edges = config.get("star_edges")
    if star_edges:
        idx = {name: i for i, name in enumerate(node_names)}
        sources = [idx[src] for src, _ in star_edges]
        targets = [idx[dst] for _, dst in star_edges]
        edge_index = torch.tensor([sources, targets], dtype=torch.long, device=device)
    else:
        edge_index = build_star_edge_index(node_names).to(device)
    if edge_index.shape[1] != STAR_EDGE_COUNT:
        raise ValueError(
            f"Invalid star edge count in checkpoint graph metadata. "
            f"Expected {STAR_EDGE_COUNT}, got {edge_index.shape[1]}"
        )
    return edge_index


def create_inference_graphs(condition_sequence, config, device="cpu"):
    """
    Create graph sequence using checkpoint metadata (no hardcoded node count).
    """
    if isinstance(device, str):
        device = torch.device(device)
    seq_len = int(config["seq_len"])
    node_names = list(config.get("node_names", NODE_NAMES))
    num_nodes = int(config.get("num_nodes", len(node_names)))
    edge_index = _build_edge_index_from_config(config, device)
    edge_attr = build_star_edge_attr(node_names).to(device)

    graphs_sequence = []
    for t in range(seq_len):
        if condition_sequence.dim() != 3:
            raise ValueError(
                f"condition_sequence must be 3-dimensional [seq_len, num_nodes, features], "
                f"got shape {tuple(condition_sequence.shape)}"
            )
        node_features = condition_sequence[t]
        if node_features.shape[0] != num_nodes:
            raise ValueError(
                f"Condition node dimension mismatch. Expected {num_nodes}, got {node_features.shape[0]}"
            )
        graph = Data(x=node_features.to(device), edge_index=edge_index, edge_attr=edge_attr)
        batch = Batch.from_data_list([graph])
        graphs_sequence.append(batch.to(device))
    return graphs_sequence


class BatchGraphBuilder:
    """
    Builds one PyG batch per timestep from stacked node windows, reusing the edge
    tensors. Equivalent to calling create_inference_graphs per window and
    Batch.from_data_list, but one allocation per timestep instead of per window.
    """

    def __init__(self, config, device="cpu", edge_dim=None):
        if isinstance(device, str):
            device = torch.device(device)
        self.device = device
        self.seq_len = int(config["seq_len"])
        self.num_nodes = int(config.get("num_nodes", len(config.get("node_names", NODE_NAMES))))
        self.edge_index = _build_edge_index_from_config(config, device)
        raw_attr = build_star_edge_attr(list(config.get("node_names", NODE_NAMES))).to(device)
        if edge_dim == 1 or (edge_dim is None and config.get("edge_dim") == 1):
            self.edge_attr = raw_attr[:, :1]
        else:
            self.edge_attr = raw_attr

    def build(self, node_windows):
        """
        node_windows: [B, seq_len, num_nodes, features]
        Returns: list of length seq_len, each a PyG Batch of B graphs.
        """
        if node_windows.dim() != 4:
            raise ValueError(
                f"node_windows must be 4-dimensional [B, seq_len, num_nodes, features], "
                f"got shape {tuple(node_windows.shape)}"
            )
        if node_windows.shape[1] != self.seq_len:
            raise ValueError(
                f"node_windows seq dim {node_windows.shape[1]} != config seq_len {self.seq_len}"
            )
        if node_windows.shape[2] != self.num_nodes:
            raise ValueError(
                f"node_windows node dim {node_windows.shape[2]} != config num_nodes {self.num_nodes}"
            )

        batch = int(node_windows.shape[0])
        # Node order is [g0 nodes, g1 nodes, ...], so the graph index per node is
        # arange(batch) interleaved over nodes (each graph owns num_nodes consecutive nodes).
        graph_batch = torch.arange(batch, device=self.device).repeat_interleave(self.num_nodes)

        # Offset each copy of the single-graph topology into its own node block.
        # Batch.from_data_list does this internally; without it every graph but the
        # first passes messages only among nodes 0..num_nodes-1 and gets none of its own.
        n_edges = self.edge_index.shape[1]
        offsets = (torch.arange(batch, device=self.device) * self.num_nodes).repeat_interleave(n_edges)
        edge_index_batched = self.edge_index.repeat(1, batch) + offsets.unsqueeze(0)
        edge_attr_batched = self.edge_attr.repeat(batch, 1)

        graphs_sequence = []
        for t in range(self.seq_len):
            x = node_windows[:, t].reshape(-1, node_windows.shape[-1]).to(self.device)
            graph = Data(x=x, edge_index=edge_index_batched, edge_attr=edge_attr_batched)
            graph.batch = graph_batch
            graphs_sequence.append(graph)
        return graphs_sequence


class InferenceModelWrapper:
    def __init__(self, st_gnn, forecaster, config):
        self.st_gnn = st_gnn
        self.forecaster = forecaster
        self.config = config
        self.device = "cpu"

    def eval(self):
        self.st_gnn.eval()
        self.forecaster.model.eval()

    def to(self, device):
        self.device = device
        self.st_gnn.to(device)
        self.forecaster.model.to(device)
        self.forecaster.device = device
        return self


def migrate_legacy_st_gnn_state(state: Dict[str, torch.Tensor], config: Dict[str, object]) -> Dict[str, torch.Tensor]:
    """
    Reshape a pre-migration ST-GNN state dict (edge_dim=1) for the edge_dim=2 convs.

    The learned second column starts at zero, so the migrated model boots and runs. This is
    NOT an exact behavioural port: legacy training saw a constant 0.25 edge attribute and the
    new convs see normalised haversine distance, so attention logits shift. Retraining is what
    actually picks up the new edge signal; this only keeps old checkpoints loadable instead of
    crashing the checkpoint contract.
    """
    migrated = dict(state)
    edge_keys = [k for k in migrated if k.endswith("lin_edge.weight")]
    if not edge_keys:
        return migrated
    legacy_dim = int(migrated[edge_keys[0]].shape[-1])
    if legacy_dim == 2:
        return migrated
    if legacy_dim != 1:
        raise ValueError(
            f"Unsupported legacy ST-GNN edge_dim={legacy_dim}; expected 1 (constant attr) or 2."
        )
    for key in edge_keys:
        weight = migrated[key]
        migrated[key] = torch.cat([weight, torch.zeros_like(weight)], dim=-1)
    return migrated


def load_model_and_stats(checkpoint_path="models/diffusion_chkpt.pth"):
    if not os.path.exists(checkpoint_path):
        if os.path.exists(os.path.join("..", checkpoint_path)):
            checkpoint_path = os.path.join("..", checkpoint_path)
        else:
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    stats = checkpoint["stats"]
    config = checkpoint["config"]
    rain_cfg = config.get("rain_specialization", {})
    if not isinstance(rain_cfg, dict):
        rain_cfg = {}
    config["rain_specialization"] = {
        "enabled": bool(rain_cfg.get("enabled", False)),
        "rain_occurrence_threshold_mm": float(rain_cfg.get("rain_occurrence_threshold_mm", 0.1)),
        "wet_loss_weight": float(rain_cfg.get("wet_loss_weight", 0.7)),
        "wet_pos_weight": float(rain_cfg.get("wet_pos_weight", 1.0)),
        "wet_probability_threshold": float(rain_cfg.get("wet_probability_threshold", 0.6)),
        "calibration_metric": str(rain_cfg.get("calibration_metric", "csi")),
        "calibration_split": str(rain_cfg.get("calibration_split", "validation")),
    }

    required = [
        "node_names",
        "node_roles",
        "node_coordinates",
        "main_node_identifier",
        "main_node_name",
        "graph_topology",
        "num_nodes",
        "target_node_policy",
        "context_policy",
    ]
    missing = [k for k in required if k not in config]
    if missing:
        raise ValueError(f"Checkpoint missing required migration metadata keys: {missing}")
    if config["graph_topology"] != "star":
        raise ValueError(f"Unsupported graph topology '{config['graph_topology']}'. Expected 'star'.")
    if config["target_node_policy"] != "main_node_only":
        raise ValueError(
            f"Unsupported target policy '{config['target_node_policy']}'. Expected 'main_node_only'."
        )

    st_gnn = SpatioTemporalGNN(
        node_features=config["context_dim"],
        hidden_dim=config["hidden_dim"] // 2,
        output_dim=config["graph_dim"],
        num_gat_heads=4,
        num_attn_heads=4,
        seq_len=config["seq_len"],
        edge_dim=2,
    )
    st_gnn_state = migrate_legacy_st_gnn_state(checkpoint["st_gnn_state"], config)
    missing, unexpected = st_gnn.load_state_dict(st_gnn_state, strict=False)
    allowed_missing = {"temporal_attn.pos_embedding", "temporal_attn.pool_query"}
    invalid_missing = sorted([k for k in missing if k not in allowed_missing])
    if invalid_missing:
        raise RuntimeError(f"Checkpoint missing unexpected ST-GNN keys: {invalid_missing}")
    if unexpected:
        raise RuntimeError(f"Checkpoint has unexpected ST-GNN keys: {unexpected}")

    num_targets = config.get("num_targets", len(FINAL_TARGET_COLS))
    diff_model = ConditionalDiffusionModel(
        input_dim=num_targets,
        context_dim=config["context_dim"],
        retrieval_dim=config["retrieval_dim"],
        graph_dim=config["graph_dim"],
        hidden_dim=config["hidden_dim"],
    )
    diffusion_state = dict(checkpoint["diffusion_state"])
    # Keep existing checkpoints loadable after merging up1 and out into up_mlp.
    if "up1.0.weight" in diffusion_state:
        diffusion_state["up_mlp.0.weight"] = diffusion_state.pop("up1.0.weight")
        diffusion_state["up_mlp.0.bias"] = diffusion_state.pop("up1.0.bias")
    if "out.weight" in diffusion_state:
        diffusion_state["up_mlp.2.weight"] = diffusion_state.pop("out.weight")
        diffusion_state["up_mlp.2.bias"] = diffusion_state.pop("out.bias")
    missing, unexpected = diff_model.load_state_dict(diffusion_state, strict=False)
    invalid_missing = sorted([k for k in missing if not k.startswith("wet_head.")])
    if invalid_missing:
        raise RuntimeError(f"Checkpoint missing unexpected diffusion keys: {invalid_missing}")
    if unexpected:
        raise RuntimeError(f"Checkpoint has unexpected diffusion keys: {unexpected}")
    if missing and config["rain_specialization"]["enabled"]:
        # Safety fallback: if wet head weights are absent, disable rain specialization.
        config["rain_specialization"]["enabled"] = False
    forecaster = RainForecaster(diff_model)
    model_wrapper = InferenceModelWrapper(st_gnn, forecaster, config)

    # Rebuild retrieval DB from training main-node rows only.
    data_path = config.get("data_path", "data/raw/pangrango_era5_5node_2005_2025.parquet")
    retrieval_db = RetrievalDatabase(embedding_dim=config["context_dim"])
    if os.path.exists(data_path):
        df = pd.read_parquet(data_path)
        df = harmonize_weather_columns(df)
        validate_feature_schema(df, FINAL_FEATURE_COLS, FINAL_TARGET_COLS)
        validate_feature_values(df, FINAL_FEATURE_COLS)
        df["date"] = pd.to_datetime(df["date"])
        if df["date"].dt.tz is not None:
            df["date"] = df["date"].dt.tz_localize(None)
        train_end = config.get("train_end", "2018-12-31 16:00")
        main_name = config.get("main_node_name", MAIN_NODE_NAME)
        main_train = df[(df["date"] <= pd.to_datetime(train_end)) & (df["node"] == main_name)].copy()
        main_train = main_train.sort_values("date")
        feature_cols = config.get("feature_cols", FINAL_FEATURE_COLS)
        target_cols = config.get("target_cols", FINAL_TARGET_COLS)
        train_features = main_train[feature_cols].values
        c_mean = stats["c_mean"].numpy()
        c_std = stats["c_std"].numpy()
        train_features_norm = (train_features - c_mean) / (c_std + ZSCORE_EPSILON)

        # Retrieval value = next-step outcome (target at tau+1), normalized like training targets.
        precip_idx = list(target_cols).index("precipitation")
        train_targets_g = main_train[target_cols].values.astype(np.float32)
        train_targets_g[:, precip_idx] = np.log1p(train_targets_g[:, precip_idx])
        t_mean = stats["t_mean"].numpy()
        t_std = stats["t_std"].numpy()
        train_targets_norm = ((train_targets_g - t_mean) / (t_std + ZSCORE_EPSILON)).astype(np.float32)

        retrieval_db.add_items(
            train_features_norm[:-1].astype(np.float32),
            train_targets_norm[1:],
        )
    return model_wrapper, stats, retrieval_db


def run_inference_real(
    features_norm,
    model_wrapper,
    stats,
    retrieval_db,
    num_samples=50,
    device="cpu",
):
    if isinstance(device, str):
        device = torch.device(device)

    model_wrapper.to(device)
    model_wrapper.eval()
    if not torch.is_tensor(features_norm):
        features_norm = torch.tensor(features_norm, dtype=torch.float32)
    features_norm = features_norm.to(device)

    num_nodes = len(model_wrapper.config.get("node_names", NODE_NAMES))
    if features_norm.dim() == 2:
        # (seq_len, features) -> add batch dim
        features_norm = features_norm.unsqueeze(0)
    elif features_norm.dim() == 3 and features_norm.shape[1] == num_nodes:
        # (seq_len, nodes, features) -> add batch dim
        features_norm = features_norm.unsqueeze(0)

    seq_len = features_norm.shape[1]
    cfg_seq_len = model_wrapper.config["seq_len"]
    if seq_len < cfg_seq_len:
        last = features_norm[:, -1:, ...]
        repeats = cfg_seq_len - seq_len
        features_norm = torch.cat([features_norm, last.repeat(1, repeats, *([1] * (last.dim() - 2)))], dim=1)
    elif seq_len > cfg_seq_len:
        features_norm = features_norm[:, -cfg_seq_len:, ...]

    st_gnn = model_wrapper.st_gnn
    forecaster = model_wrapper.forecaster
    config = model_wrapper.config
    main_name = config["main_node_name"]

    with torch.no_grad():
        condition_seq = features_norm[0]
        graphs_sequence = create_inference_graphs(condition_seq, config, device=device)
        graph_emb = st_gnn(graphs_sequence)

        if condition_seq.dim() == 3:
            main_idx = config["node_names"].index(main_name)
            context_last = condition_seq[-1, main_idx, :].unsqueeze(0)
        else:
            context_last = condition_seq[-1].unsqueeze(0)

        retrieved = retrieval_db.query(context_last.cpu().numpy(), k=config["k_neighbors"]).to(device)
        samples = forecaster.sample_fast(
            condition=context_last,
            retrieved=retrieved,
            graph_emb=graph_emb,
            num_samples=num_samples,
            num_inference_steps=DDIM_INFERENCE_STEPS,
        )

        t_mean = stats["t_mean"].to(device)
        t_std = stats["t_std"].to(device)
        target_cols = list(config.get("target_cols", FINAL_TARGET_COLS))
        precip_idx = target_cols.index("precipitation")
        wind_idx = target_cols.index("wind_speed")
        humidity_idx = target_cols.index("relative_humidity")
        samples_denorm = samples * t_std + t_mean
        samples_denorm[:, precip_idx] = torch.expm1(torch.clamp(samples_denorm[:, precip_idx], max=LOG_PRECIP_MAX))
        samples_denorm[:, precip_idx] = torch.clamp(
            samples_denorm[:, precip_idx], min=0.0, max=PRECIP_PHYSICAL_MAX_MM
        )
        samples_denorm[:, wind_idx] = torch.clamp(samples_denorm[:, wind_idx], min=0.0)  # wind speed >= 0
        samples_denorm[:, humidity_idx] = torch.clamp(samples_denorm[:, humidity_idx], min=0.0, max=100.0)
        rain_cfg = config.get("rain_specialization", {})
        wet_prob_value = None
        wet_prob_threshold = float(rain_cfg.get("wet_probability_threshold", 0.6))
        if rain_cfg.get("enabled", False):
            wet_prob = forecaster.model.compute_wet_probability(
                context=context_last,
                retrieved=retrieved,
                graph_emb=graph_emb,
            )
            wet_prob_value = float(wet_prob.squeeze().item())
            if wet_prob_value < wet_prob_threshold:
                samples_denorm[:, precip_idx] = 0.0
        result = samples_denorm.cpu().numpy()
        return {
            "main_node_name": main_name,
            "target_node_policy": config.get("target_node_policy", TARGET_NODE_POLICY),
            **{col: result[:, i] for i, col in enumerate(target_cols)},
            "rain_specialization_enabled": bool(rain_cfg.get("enabled", False)),
            "rain_occurrence_probability": wet_prob_value,
            "rain_occurrence_probability_threshold": wet_prob_threshold,
            "raw": result,
        }
