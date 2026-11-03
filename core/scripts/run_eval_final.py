"""
Comprehensive RDM-STGNN ablation evaluation on canonical main-node-only target.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import (  # noqa: E402
    CONTEXT_POLICY,
    DDIM_INFERENCE_STEPS,
    FINAL_FEATURE_COLS,
    FINAL_TARGET_COLS,
    LOG_PRECIP_MAX,
    MAIN_NODE_NAME,
    NODE_COORDINATES,
    NODE_NAMES,
    OPEN_METEO_MODEL,
    PRECIP_PHYSICAL_MAX_MM,
    TARGET_NODE_POLICY,
    ZSCORE_EPSILON,
    harmonize_weather_columns,
    validate_feature_schema,
    validate_feature_values,
)
from src.data.ingest import CANONICAL_DATA_PATH, fetch_era5_data  # noqa: E402
from src.evaluation.probabilistic_metrics import (  # noqa: E402
    compute_brier_score,
    compute_correlation,
    compute_crps,
    compute_csi,
    compute_far,
    compute_mae,
    compute_pod,
    compute_rmse,
)
from src.inference import BatchGraphBuilder, load_model_and_stats  # noqa: E402
from src.train import compute_stats_from_training, temporal_split  # noqa: E402

matplotlib.use("Agg")

TARGET_COLS = FINAL_TARGET_COLS
VAR_NAMES = FINAL_TARGET_COLS
THRESHOLDS_PRECIP = [2.0, 5.0, 10.0]
PALETTE = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_test_data(data_path: str, checkpoint: str = "models/diffusion_chkpt.pth"):
    if not os.path.exists(data_path):
        fetch_era5_data(start_year=2005, end_year=2025)
    df = pd.read_parquet(data_path)
    df = harmonize_weather_columns(df)
    validate_feature_schema(df, FINAL_FEATURE_COLS, FINAL_TARGET_COLS)
    validate_feature_values(df, FINAL_FEATURE_COLS)

    ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    feature_cols = ckpt["config"].get("feature_cols", FINAL_FEATURE_COLS)
    train_end = ckpt["config"].get("train_end", "2018-12-31 16:00")
    val_end = ckpt["config"].get("val_end", "2021-12-31 16:00")

    train_df, _, test_df = temporal_split(df, train_end, val_end)
    stats = ckpt["stats"]

    test_df = test_df.copy()
    test_df["date"] = pd.to_datetime(test_df["date"])
    if test_df["date"].dt.tz is not None:
        test_df["date"] = test_df["date"].dt.tz_localize(None)

    main_df = (
        test_df[test_df["node"] == MAIN_NODE_NAME]
        .copy()
        .sort_values("date")
        .reset_index(drop=True)
    )
    per_node_data = {}
    for node in NODE_NAMES:
        ndf = (
            test_df[test_df["node"] == node]
            .copy()
            .sort_values("date")
            .reset_index(drop=True)
        )
        if ndf.empty:
            raise ValueError(f"Test split missing node '{node}'")
        if not ndf["date"].reset_index(drop=True).equals(main_df["date"]):
            raise ValueError(f"Date mismatch between MAIN and node '{node}' in test split")
        per_node_data[node] = ndf

    return main_df, per_node_data, feature_cols, stats


def _eval_indices(main_df, seq_len, eval_step, max_eval_samples=0):
    """
    Single source of evaluation indices so every scenario uses identical samples.
    idx-seq_len (windows) is always valid since idx>=seq_len>=1.
    """
    idxs = list(range(seq_len, len(main_df), eval_step))
    if max_eval_samples and max_eval_samples > 0:
        idxs = idxs[:max_eval_samples]
    return idxs


def _fetch_retrieval_batched(retrieval_db, contexts_np, k):
    """
    Fetch FAISS neighbors for every window once, up front. The retrieval DB is
    static, so querying per window inside the sampling loop buys nothing but a
    python round-trip per window.
    """
    retrieval_db.ensure_index_built()
    out = retrieval_db.query(contexts_np, k=k)
    return out if torch.is_tensor(out) else torch.as_tensor(out, dtype=torch.float32)


def run_diffusion_scenario(
    main_df,
    per_node_data,
    feature_cols,
    stats,
    eval_step,
    seq_len,
    num_ensemble,
    use_retrieval=True,
    use_gnn=True,
    max_eval_samples=0,
    checkpoint="models/diffusion_chkpt.pth",
    num_inference_steps=DDIM_INFERENCE_STEPS,
    sample_batch_size=256,
):
    model_wrapper, _, retrieval_db, _catalog = load_model_and_stats(checkpoint)
    model_wrapper.to(DEVICE)
    model_wrapper.eval()

    config = model_wrapper.config
    # Each scenario gets its own RNG stream so metrics do not depend on which
    # scenarios ran before it (stable offset from the scenario flags).
    import zlib

    base_seed = int(config.get("seed", 1))
    offset = zlib.crc32(f"{use_retrieval}-{use_gnn}".encode()) % 10000
    torch.manual_seed(base_seed + offset)
    np.random.seed((base_seed + offset) % (2**32))
    st_gnn = model_wrapper.st_gnn
    forecaster = model_wrapper.forecaster

    c_mean = stats["c_mean"].numpy()
    c_std = stats["c_std"].numpy()
    t_mean_t = stats["t_mean"].to(DEVICE)
    t_std_t = stats["t_std"].to(DEVICE)

    features_raw = main_df[feature_cols].values.astype(np.float32)
    features_norm = (features_raw - c_mean) / (c_std + ZSCORE_EPSILON)
    targets_raw = main_df[TARGET_COLS].values.astype(np.float32)

    rain_cfg = config.get("rain_specialization", {})
    rain_enabled = bool(rain_cfg.get("enabled", False))
    wet_threshold = float(rain_cfg.get("wet_probability_threshold", 0.6))
    eval_idxs = _eval_indices(main_df, seq_len, eval_step, max_eval_samples)

    # Pre-fetch everything the sampling loop needs, once, in bulk. None of it
    # depends on a previous window, so per-window assembly was pure python cost.
    window_idx = np.stack([np.arange(i - seq_len, i) for i in eval_idxs])          # [N, seq_len]
    contexts_np = features_norm[window_idx.reshape(-1)].reshape(-1, seq_len, features_norm.shape[-1])
    # The conditioning context is the LAST observed row of each window (row i-1),
    # matching main_ctx_seq[-1] in the original loop.
    context_last_np = features_norm[np.asarray(eval_idxs) - 1]                     # [N, C]
    targets = targets_raw[eval_idxs]                                               # [N, 3]

    retrieved_all = None
    if use_retrieval:
        retrieved_all = _fetch_retrieval_batched(retrieval_db, context_last_np, config["k_neighbors"])
    # use_retrieval=False keeps retrieved_all=None: downstream code passes
    # retrieved=None so the retrieval_mlp branch is a true structural bypass
    # (zero contribution). A zero tensor instead keeps the branch in the graph
    # and injects its bias-only activation into cond_emb, silently biasing the
    # ablation table (clean-branch contract, tests/test_ablation_clean_branch.py).

    node_windows_all = None
    if use_gnn:
        per_node_arrays = [per_node_data[n][feature_cols].values.astype(np.float32) for n in NODE_NAMES]
        padded = [np.concatenate([np.zeros((seq_len, arr.shape[1]), np.float32), arr], axis=0) for arr in per_node_arrays]
        stacked = np.stack(padded, axis=1)                                         # [T + seq_len, num_nodes, C]
        node_windows_all = stacked[window_idx + seq_len]                           # [N, seq_len, num_nodes, C]
        node_windows_all = (node_windows_all - c_mean) / (c_std + ZSCORE_EPSILON)
        edge_dim = getattr(st_gnn.spatial_gnn.conv1, "edge_dim", 2)
        graph_builder = BatchGraphBuilder(config, device=DEVICE, edge_dim=edge_dim)

    n_total = len(eval_idxs)
    preds_all, ensemble_all, wet_probs_all = [], [], []

    for start in tqdm(range(0, n_total, sample_batch_size), desc=f"Diff(R={use_retrieval},G={use_gnn})"):
        stop = min(start + sample_batch_size, n_total)
        b = stop - start
        with torch.no_grad():
            if use_gnn:
                node_windows = torch.as_tensor(node_windows_all[start:stop], dtype=torch.float32).to(DEVICE)
                graphs = graph_builder.build(node_windows)
                graph_emb = st_gnn(graphs)
            else:
                graph_emb = None

            dim = forecaster.model.input_dim
            cond = torch.as_tensor(context_last_np[start:stop], dtype=torch.float32).to(DEVICE)
            # retrieved is None when retrieval is ablated (structural bypass),
            # else the FAISS-fetched tensor slice for this batch.
            retrieved = None
            if retrieved_all is not None:
                retrieved = retrieved_all[start:stop].to(DEVICE)

            wet_prob = None
            if rain_enabled:
                wet_prob = forecaster.model.compute_wet_probability(
                    context=cond, retrieved=retrieved, graph_emb=graph_emb
                )

            # One noise draw per window, sliced across the M ensemble members.
            # Draw order and shape are identical to the original per-window loop
            # (torch.randn((M, dim)) per window), so results are reproducible.
            init_noise = torch.cat(
                [torch.randn(num_ensemble, dim) for _ in range(b)], dim=0
            ).to(DEVICE)

            samples = forecaster.sample_fast(
                condition=cond.repeat_interleave(num_ensemble, dim=0),
                retrieved=(None if retrieved is None else retrieved.repeat_interleave(num_ensemble, dim=0)),
                graph_emb=(None if graph_emb is None else graph_emb.repeat_interleave(num_ensemble, dim=0)),
                num_samples=b * num_ensemble,
                num_inference_steps=num_inference_steps,
                init_noise=init_noise,
            )
            samples_denorm = samples * t_std_t + t_mean_t
            samples_denorm[:, 0] = torch.clamp(torch.expm1(torch.clamp(samples_denorm[:, 0], max=LOG_PRECIP_MAX)), min=0.0, max=PRECIP_PHYSICAL_MAX_MM)
            samples_denorm[:, 1] = torch.clamp(samples_denorm[:, 1], min=0.0)  # wind speed >= 0
            samples_denorm[:, 2] = torch.clamp(samples_denorm[:, 2], min=0.0, max=100.0)
            samples_np = samples_denorm.cpu().numpy().reshape(b, num_ensemble, -1)

            if wet_prob is not None:
                wet_probs_all.append(wet_prob.detach().cpu().numpy().reshape(-1))

        preds_all.append(np.median(samples_np, axis=1))
        ensemble_all.append(samples_np)

    targets = np.asarray(targets)
    preds = np.concatenate(preds_all, axis=0)
    ensemble = np.concatenate(ensemble_all, axis=0)
    wet_probs = np.concatenate(wet_probs_all, axis=0) if wet_probs_all else None

    # FIX #5: apply rain gate AFTER the loop with an anti-degenerate guard.
    # If every window is below threshold, skip gating entirely (transparent) instead of
    # silently zeroing all precipitation.
    if rain_enabled and wet_probs is not None:
        wet_arr = np.asarray(wet_probs, dtype=np.float32)
        if float(wet_arr.max()) < wet_threshold:
            print(
                f"  [rain-gate guard] All {len(wet_arr)} windows have wet_prob < {wet_threshold:.3f} "
                f"(max={wet_arr.max():.3f}); skipping gate to avoid degenerate all-dry output."
            )
        else:
            gate_mask = wet_arr < wet_threshold
            # Only the point forecast is gated here; CRPS/Brier must be scored on the
            # raw ensemble so the gate cannot inflate calibration metrics.
            preds[gate_mask, 0] = 0.0

    return targets, preds, ensemble


def compute_scenario_metrics(targets, preds, ensemble):
    results = {}
    for i, var in enumerate(VAR_NAMES):
        act = targets[:, i]
        pred = preds[:, i]
        ens = ensemble[:, :, i]
        m = {
            "rmse": compute_rmse(pred, act),
            "mae": compute_mae(pred, act),
            "correlation": compute_correlation(pred, act),
            "crps": compute_crps(ens, act),
        }
        if var == "precipitation":
            for thr in THRESHOLDS_PRECIP:
                m[f"brier_{int(thr)}mm"] = compute_brier_score(ens, act, threshold=thr)
                m[f"pod_{int(thr)}mm"] = compute_pod(ens, act, threshold=thr)
                m[f"far_{int(thr)}mm"] = compute_far(ens, act, threshold=thr)
                m[f"csi_{int(thr)}mm"] = compute_csi(ens, act, threshold=thr)
        results[var] = m
    return results


def plot_bar_chart(all_results, save_dir):
    scenarios = list(all_results.keys())
    metrics_to_plot = ["rmse", "mae", "correlation"]
    fig, axes = plt.subplots(3, 3, figsize=(18, 14))
    for vi, var in enumerate(VAR_NAMES):
        for mi, metric in enumerate(metrics_to_plot):
            ax = axes[vi][mi]
            vals = [all_results[s].get(var, {}).get(metric, 0) for s in scenarios]
            bars = ax.bar(range(len(scenarios)), vals, color=PALETTE[: len(scenarios)])
            ax.set_xticks(range(len(scenarios)))
            ax.set_xticklabels([s.replace("_", "\n") for s in scenarios], fontsize=8, rotation=45, ha="right")
            ax.set_title(f"{var} - {metric.upper()}")
            for bar, v in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{v:.3f}", ha="center", va="bottom", fontsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "bar_chart_metrics.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_scatter(all_data, save_dir):
    if "full_model" not in all_data:
        return
    targets, preds, ensemble = all_data["full_model"]
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, var in enumerate(VAR_NAMES):
        ax = axes[i]
        act = targets[:, i]
        pred = preds[:, i]
        spread = ensemble[:, :, i].std(axis=1)
        sc = ax.scatter(act, pred, c=spread, cmap="YlOrRd", alpha=0.6, s=15, edgecolors="none")
        mn, mx = min(act.min(), pred.min()), max(act.max(), pred.max())
        ax.plot([mn, mx], [mn, mx], "k--", alpha=0.5, lw=1)
        ax.set_title(f"{var} (Main node)")
        plt.colorbar(sc, ax=ax, label="Spread")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "scatter_actual_vs_pred.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_time_series(all_data, save_dir, n_points=720):
    if "full_model" not in all_data:
        return
    targets, preds, ensemble = all_data["full_model"]
    n = min(n_points, len(targets))
    fig, axes = plt.subplots(3, 1, figsize=(16, 12), sharex=True)
    for i, var in enumerate(VAR_NAMES):
        ax = axes[i]
        act = targets[:n, i]
        med = preds[:n, i]
        p10 = np.percentile(ensemble[:n, :, i], 10, axis=1)
        p90 = np.percentile(ensemble[:n, :, i], 90, axis=1)
        x = np.arange(n)
        ax.fill_between(x, p10, p90, alpha=0.3, color=PALETTE[0], label="P10-P90")
        ax.plot(x, med, color=PALETTE[0], lw=1, label="Median pred")
        ax.plot(x, act, color=PALETTE[3], lw=1, alpha=0.8, label="Actual")
        ax.legend(loc="upper right", fontsize=9)
        ax.set_ylabel(var)
    axes[-1].set_xlabel("Time step")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "time_series_sample.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_reliability(all_data, save_dir):
    if "full_model" not in all_data:
        return
    targets, _, ensemble = all_data["full_model"]
    threshold = 2.0
    obs_binary = (targets[:, 0] > threshold).astype(float)
    forecast_prob = np.mean(ensemble[:, :, 0] > threshold, axis=1)
    n_bins = 10
    bin_edges = np.linspace(0, 1, n_bins + 1)
    obs_freq, pred_freq = [], []
    for b in range(n_bins):
        mask = (forecast_prob >= bin_edges[b]) & (forecast_prob < bin_edges[b + 1])
        if mask.sum() > 0:
            obs_freq.append(obs_binary[mask].mean())
            pred_freq.append(forecast_prob[mask].mean())
        else:
            obs_freq.append(np.nan)
            pred_freq.append((bin_edges[b] + bin_edges[b + 1]) / 2)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Perfect")
    ax.plot(pred_freq, obs_freq, "o-", color=PALETTE[0], markersize=8, label=f"Precip > {threshold}mm")
    ax.legend()
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "reliability_diagram.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_crps_comparison(all_results, save_dir):
    scenarios = list(all_results.keys())
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for i, var in enumerate(VAR_NAMES):
        ax = axes[i]
        vals = [all_results[s].get(var, {}).get("crps", 0) for s in scenarios]
        bars = ax.barh(range(len(scenarios)), vals, color=PALETTE[: len(scenarios)])
        ax.set_yticks(range(len(scenarios)))
        ax.set_yticklabels(scenarios, fontsize=9)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f" {v:.4f}", va="center", fontsize=8)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "crps_comparison.png"), dpi=150, bbox_inches="tight")
    plt.close()


def plot_ablation(all_results, save_dir):
    order = ["diff_only", "diff_retrieval", "diff_gnn", "full_model"]
    labels = ["Diff Only", "+Retrieval", "+GNN", "Full"]
    available = [s for s in order if s in all_results]
    if len(available) < 2:
        return
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    for i, var in enumerate(VAR_NAMES):
        ax = axes[i]
        corrs = [all_results[s].get(var, {}).get("correlation", 0) for s in available]
        lbls = [labels[order.index(s)] for s in available]
        ax.plot(range(len(corrs)), corrs, "o-", color=PALETTE[0], markersize=10, lw=2)
        ax.set_xticks(range(len(corrs)))
        ax.set_xticklabels(lbls)
        ax.set_ylim(-0.1, 1.05)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "ablation_contribution.png"), dpi=150, bbox_inches="tight")
    plt.close()


def main(eval_step=1, num_ensemble=30, seq_len=6, data_path=CANONICAL_DATA_PATH, max_eval_samples=0, seed=1,
         checkpoint="models/diffusion_chkpt.pth", num_inference_steps=DDIM_INFERENCE_STEPS, out_dir="result_test",
         scenarios="all", sample_batch_size=256):
    print("=" * 70)
    print("COMPREHENSIVE 6-SCENARIO EVALUATION (MAIN NODE ONLY)")
    print("=" * 70)

    # Reproducible diffusion sampling.
    import random as _random
    _random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    os.makedirs(f"{out_dir}/plots", exist_ok=True)
    os.makedirs(f"{out_dir}/comparison", exist_ok=True)

    print("\n[1/8] Loading test data...")
    main_df, per_node_data, feature_cols, stats = load_test_data(data_path, checkpoint)
    ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    rain_cfg = ckpt.get("config", {}).get("rain_specialization", {})
    if not isinstance(rain_cfg, dict):
        rain_cfg = {}
    expected_n = len(_eval_indices(main_df, seq_len, eval_step, max_eval_samples))
    print(f"Main-node test rows: {len(main_df)} | eval_step={eval_step} | expected samples/scenario: {expected_n}")

    all_results: Dict[str, Dict[str, Dict[str, float]]] = {}
    all_data: Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]] = {}

    if scenarios in ("all", "diff_only"):
        print("\n[2/8] Scenario 1: Diffusion only...")
        t, p, e = run_diffusion_scenario(
            main_df, per_node_data, feature_cols, stats, eval_step, seq_len, num_ensemble, False, False, max_eval_samples, checkpoint=checkpoint,
            num_inference_steps=num_inference_steps, sample_batch_size=sample_batch_size,
        )
        all_results["diff_only"] = compute_scenario_metrics(t, p, e)
        all_data["diff_only"] = (t, p, e)

    if scenarios in ("all", "diff_retrieval"):
        print("\n[3/8] Scenario 2: Diffusion + Retrieval...")
        t, p, e = run_diffusion_scenario(
            main_df, per_node_data, feature_cols, stats, eval_step, seq_len, num_ensemble, True, False, max_eval_samples, checkpoint=checkpoint,
            num_inference_steps=num_inference_steps, sample_batch_size=sample_batch_size,
        )
        all_results["diff_retrieval"] = compute_scenario_metrics(t, p, e)
        all_data["diff_retrieval"] = (t, p, e)

    if scenarios in ("all", "diff_gnn"):
        print("\n[4/8] Scenario 3: Diffusion + GNN...")
        t, p, e = run_diffusion_scenario(
            main_df, per_node_data, feature_cols, stats, eval_step, seq_len, num_ensemble, False, True, max_eval_samples, checkpoint=checkpoint,
            num_inference_steps=num_inference_steps, sample_batch_size=sample_batch_size,
        )
        all_results["diff_gnn"] = compute_scenario_metrics(t, p, e)
        all_data["diff_gnn"] = (t, p, e)

    if scenarios in ("all", "full_model"):
        print("\n[5/8] Scenario 4: Full model...")
        t, p, e = run_diffusion_scenario(
            main_df, per_node_data, feature_cols, stats, eval_step, seq_len, num_ensemble, True, True, max_eval_samples, checkpoint=checkpoint,
            num_inference_steps=num_inference_steps, sample_batch_size=sample_batch_size,
        )
        all_results["full_model"] = compute_scenario_metrics(t, p, e)
        all_data["full_model"] = (t, p, e)

    # FIX #3: fail-fast if any scenario produced a different number of samples.
    sample_counts = {name: int(data[0].shape[0]) for name, data in all_data.items()}
    unique_counts = set(sample_counts.values())
    if len(unique_counts) != 1:
        raise AssertionError(
            f"Scenario sample-count mismatch (alignment broken): {sample_counts}"
        )
    print(f"  Sample-count alignment OK: all scenarios = {unique_counts.pop()} samples")

    metadata = {
        "main_node_name": MAIN_NODE_NAME,
        "main_node_identifier": NODE_COORDINATES[MAIN_NODE_NAME],
        "node_order": NODE_NAMES,
        "graph_topology": "star",
        "target_node_policy": TARGET_NODE_POLICY,
        "context_policy": CONTEXT_POLICY,
        "model_mode": OPEN_METEO_MODEL,
        "data_path": data_path,
        "eval_step": eval_step,
        "max_eval_samples": int(max_eval_samples),
        "samples_per_scenario": int(next(iter(sample_counts.values()))),
        "num_ensemble": num_ensemble,
        "seq_len": seq_len,
        "seed": int(seed),
        "crps_estimator": "fair_unbiased",
        "rain_specialization_enabled": bool(rain_cfg.get("enabled", False)),
        "rain_occurrence_threshold_mm": rain_cfg.get("rain_occurrence_threshold_mm"),
        "rain_probability_threshold": rain_cfg.get("wet_probability_threshold"),
        "sample_batch_size": int(sample_batch_size),
    }

    for scenario_name, metrics in all_results.items():
        scenario_dir = f"{out_dir}/{scenario_name}"
        os.makedirs(scenario_dir, exist_ok=True)
        with open(os.path.join(scenario_dir, "metrics.json"), "w", encoding="utf-8") as f:
            json.dump({"metadata": metadata, "metrics": metrics}, f, indent=2)

    print("\n[8/8] Writing summary and plots...")
    rows = []
    for scenario, scenario_metrics in all_results.items():
        for var in VAR_NAMES:
            m = scenario_metrics.get(var, {})
            rows.append(
                {
                    "scenario": scenario,
                    "variable": var,
                    "rmse": m.get("rmse", np.nan),
                    "mae": m.get("mae", np.nan),
                    "correlation": m.get("correlation", np.nan),
                    "crps": m.get("crps", np.nan),
                    "main_node_name": MAIN_NODE_NAME,
                    "graph_topology": "star",
                    "target_node_policy": TARGET_NODE_POLICY,
                    "context_policy": CONTEXT_POLICY,
                    "model_mode": OPEN_METEO_MODEL,
                }
            )
    summary_df = pd.DataFrame(rows)
    summary_df.to_csv(f"{out_dir}/comparison/comparison_summary.csv", index=False)
    with open(f"{out_dir}/comparison/comparison_summary.json", "w", encoding="utf-8") as f:
        json.dump({"metadata": metadata, "results": all_results}, f, indent=2)

    plot_dir = f"{out_dir}/plots"
    plot_bar_chart(all_results, plot_dir)
    plot_scatter(all_data, plot_dir)
    plot_time_series(all_data, plot_dir)
    plot_reliability(all_data, plot_dir)
    plot_crps_comparison(all_results, plot_dir)
    plot_ablation(all_results, plot_dir)

    with open(f"{out_dir}/EVALUATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# Evaluation Report - Main Node Only\n\n")
        for k, v in metadata.items():
            f.write(f"- **{k}**: `{v}`\n")
        f.write("\n")
        for var in VAR_NAMES:
            f.write(f"## {var.upper()}\n\n")
            f.write("| Scenario | RMSE | MAE | Corr | CRPS |\n")
            f.write("|---|---:|---:|---:|---:|\n")
            for scenario in all_results:
                m = all_results[scenario].get(var, {})
                f.write(
                    f"| {scenario} | {m.get('rmse',0):.4f} | {m.get('mae',0):.4f} | "
                    f"{m.get('correlation',0):.4f} | {m.get('crps',0):.4f} |\n"
                )
            f.write("\n")
        f.write("## Precipitation Threshold Metrics\n\n")
        for thr in THRESHOLDS_PRECIP:
            f.write(f"### Threshold {thr} mm\n\n")
            f.write("| Scenario | POD | FAR | CSI | Brier |\n")
            f.write("|---|---:|---:|---:|---:|\n")
            for scenario in all_results:
                m = all_results[scenario].get("precipitation", {})
                f.write(
                    f"| {scenario} | {m.get(f'pod_{int(thr)}mm', float('nan')):.4f} | "
                    f"{m.get(f'far_{int(thr)}mm', float('nan')):.4f} | "
                    f"{m.get(f'csi_{int(thr)}mm', float('nan')):.4f} | "
                    f"{m.get(f'brier_{int(thr)}mm', float('nan')):.4f} |\n"
                )
            f.write("\n")

    print(f"Evaluation complete. Outputs refreshed in {out_dir}/.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-step", type=int, default=1,
                        help="Hourly nowcasting uses 1 (every hour). Higher values subsample.")
    parser.add_argument("--num-ensemble", type=int, default=30)
    parser.add_argument("--seq-len", type=int, default=6)
    parser.add_argument("--max-eval-samples", type=int, default=0,
                        help="Optional cap on number of eval samples per scenario (0 = no cap).")
    parser.add_argument("--seed", type=int, default=1, help="Seed for reproducible diffusion sampling.")
    parser.add_argument("--data-path", type=str, default=CANONICAL_DATA_PATH)
    parser.add_argument("--checkpoint", type=str, default="models/diffusion_chkpt.pth",
                        help="Checkpoint to evaluate. Default keeps the canonical path.")
    parser.add_argument("--num-inference-steps", type=int, default=DDIM_INFERENCE_STEPS,
                        help="DDIM inference steps (Tabel 3.17 sweeps 10/15/20/30/50).")
    parser.add_argument("--scenarios", type=str, default="all",
                        help="Which ablation to run: all | diff_only | diff_retrieval | diff_gnn | full_model")
    parser.add_argument("--out-dir", type=str, default="result_test",
                        help="Output directory. Use a per-scenario dir to avoid overwriting.")
    parser.add_argument("--sample-batch-size", type=int, default=256,
                        help="Mini-batch size for window evaluation (default: 256 for fast batched inference).")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(
        eval_step=args.eval_step,
        num_ensemble=args.num_ensemble,
        seq_len=args.seq_len,
        data_path=args.data_path,
        max_eval_samples=args.max_eval_samples,
        seed=args.seed,
        checkpoint=args.checkpoint,
        num_inference_steps=args.num_inference_steps,
        out_dir=args.out_dir,
        scenarios=args.scenarios,
        sample_batch_size=args.sample_batch_size,
    )
