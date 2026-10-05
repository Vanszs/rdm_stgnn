"""Unit tests for the 10-feature schema & dimension contract.

Guarantees that `input_dim` (num_targets = 3), `context_dim`
(len(feature_cols) = 10 in "both" precip_mode), and the `feature_cols`
list stay synchronized across config, loader, stats, and the diffusion/STGNN
models, so a checkpoint trained on one feature count cannot be loaded against
another silently.
"""
import os
import unittest

import pandas as pd
import torch

from src.config import (
    FINAL_FEATURE_COLS,
    FINAL_TARGET_COLS,
    NODE_NAMES,
    NUM_NODES,
    OPTIONAL_LEGACY_RENAMES,
    STAR_EDGE_COUNT,
    build_star_edge_attr,
    build_star_edge_index,
    harmonize_weather_columns,
    validate_feature_schema,
    validate_feature_values,
)
from src.data.temporal_loader import TemporalGraphDataset
from src.models.diffusion import ConditionalDiffusionModel
from src.models.gnn import SpatioTemporalGNN


FEATURE_COLS_10 = FINAL_FEATURE_COLS + ["precipitation"]  # precip_mode="both"


def _make_df(num_timestamps=10, feature_cols=None):
    """Synthetic canonical-order dataframe carrying 9 base + raw precipitation.

    wind_speed / relative_humidity are both features and targets, so the final
    column list must be deduplicated before selecting.
    """
    feature_cols = feature_cols if feature_cols is not None else FEATURE_COLS_10
    target_cols = [c for c in FINAL_TARGET_COLS if c not in feature_cols]
    times = pd.date_range("2024-01-01", periods=num_timestamps, freq="h")
    rows = []
    for t_i, ts in enumerate(times):
        for n_i, node in enumerate(NODE_NAMES):
            rows.append(
                {
                    "date": ts,
                    "node": node,
                    "temperature": 20.0 + n_i,
                    "relative_humidity": 80.0 + n_i,
                    "dewpoint": 18.0 + n_i,
                    "surface_pressure": 900.0 + n_i,
                    "wind_speed": 2.0 + n_i,
                    "wind_direction": 180.0,
                    "cloud_cover": 50.0,
                    "precipitation_lag1": 0.1 * t_i,
                    "elevation": 100.0 * (n_i + 1),
                    "precipitation": 0.2 * t_i,
                }
            )
    return pd.DataFrame(rows)[["date", "node", *feature_cols, *target_cols]]


def _make_stats(feature_cols):
    return {
        "t_mean": torch.zeros(len(FINAL_TARGET_COLS)),
        "t_std": torch.ones(len(FINAL_TARGET_COLS)),
        "c_mean": torch.zeros(len(feature_cols)),
        "c_std": torch.ones(len(feature_cols)),
    }


class TenFeatureSchemaTest(unittest.TestCase):
    """Column schema of the 10-feature ("both" precip_mode) dataframe."""

    def test_final_feature_cols_is_9_base_features(self):
        self.assertEqual(len(FINAL_FEATURE_COLS), 9)
        self.assertNotIn("precipitation", FINAL_FEATURE_COLS)
        self.assertIn("precipitation_lag1", FINAL_FEATURE_COLS)

    def test_10_feature_schema_has_both_lag1_and_raw_precipitation(self):
        self.assertIn("precipitation_lag1", FEATURE_COLS_10)
        self.assertIn("precipitation", FEATURE_COLS_10)
        self.assertEqual(len(FEATURE_COLS_10), 10)
        self.assertEqual(len(set(FEATURE_COLS_10)), 10)

    def test_validate_schema_accepts_10_features(self):
        df = _make_df()
        validate_feature_schema(df, feature_cols=FEATURE_COLS_10, target_cols=FINAL_TARGET_COLS)
        validate_feature_values(df, feature_cols=FEATURE_COLS_10)

    def test_validate_schema_rejects_missing_10th_feature(self):
        # The 9-feature df still passes: FINAL_TARGET_COLS carries precipitation.
        df = _make_df(feature_cols=FINAL_FEATURE_COLS)
        validate_feature_schema(df, FINAL_FEATURE_COLS, FINAL_TARGET_COLS)
        # Drop raw precipitation entirely: the 10-feature ask must then fail.
        df_no_precip = df.drop(columns=["precipitation"])
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            validate_feature_schema(df_no_precip, FEATURE_COLS_10, FINAL_TARGET_COLS)

    def test_validate_schema_rejects_missing_target(self):
        df = _make_df()
        df = df.drop(columns=["relative_humidity"])
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            validate_feature_schema(df, FEATURE_COLS_10, FINAL_TARGET_COLS)

    def test_validate_values_rejects_all_nan_feature(self):
        df = _make_df()
        df["cloud_cover"] = float("nan")
        with self.assertRaisesRegex(ValueError, "all-NaN"):
            validate_feature_values(df, FEATURE_COLS_10)

    def test_harmonize_weather_columns_renames_legacy_names(self):
        df = _make_df()
        legacy = {new: old for old, new in OPTIONAL_LEGACY_RENAMES.items()}
        renamed = df.rename(columns=legacy)
        restored = harmonize_weather_columns(renamed)
        validate_feature_schema(restored, FINAL_FEATURE_COLS, FINAL_TARGET_COLS)
        for col in FINAL_FEATURE_COLS:
            self.assertIn(col, restored.columns)


class TenFeatureDimensionContractTest(unittest.TestCase):
    """input_dim / context_dim / feature_cols must agree across all components."""

    def test_loader_exposes_10_feature_tensor(self):
        df = _make_df()
        stats = {
            "t_mean": torch.zeros(len(FINAL_TARGET_COLS)),
            "t_std": torch.ones(len(FINAL_TARGET_COLS)),
            "c_mean": torch.zeros(len(FEATURE_COLS_10)),
            "c_std": torch.ones(len(FEATURE_COLS_10)),
        }
        ds = TemporalGraphDataset(df=df, feature_cols=FEATURE_COLS_10, seq_len=2, stats=stats)
        self.assertEqual(ds.num_nodes, NUM_NODES)
        self.assertEqual(ds.num_targets, len(FINAL_TARGET_COLS))
        self.assertEqual(ds.features.shape, (10, NUM_NODES, 10))
        self.assertEqual(ds.targets.shape, (10, NUM_NODES, len(FINAL_TARGET_COLS)))
        graphs, target, context = ds[0]
        self.assertEqual(len(graphs), 2)
        self.assertEqual(graphs[0].x.shape, (NUM_NODES, 10))
        self.assertEqual(target.shape, (len(FINAL_TARGET_COLS),))
        self.assertEqual(context.shape, (10,))

    def test_edge_topology_independent_of_feature_count(self):
        df = _make_df()
        ds = TemporalGraphDataset(df=df, feature_cols=FEATURE_COLS_10, seq_len=2)
        self.assertEqual(ds.edge_index.shape, (2, STAR_EDGE_COUNT))
        # Edge attr carries the canonical [num_edges, 2] haversine pair
        # (normalised distance, heavy-tail inverse), independent of feature count.
        self.assertEqual(tuple(ds.edge_attr.shape), (STAR_EDGE_COUNT, 2))
        torch.testing.assert_close(ds.edge_attr, build_star_edge_attr(NODE_NAMES))

    def test_models_match_10_feature_context_dim(self):
        context_dim = len(FEATURE_COLS_10)
        num_targets = len(FINAL_TARGET_COLS)
        gnn = SpatioTemporalGNN(
            node_features=context_dim, hidden_dim=8, output_dim=8, seq_len=2
        )
        h = gnn.spatial_gnn(
            torch.randn(NUM_NODES, context_dim),
            build_star_edge_index(NODE_NAMES),
            edge_attr=build_star_edge_attr(NODE_NAMES),
            batch=torch.zeros(NUM_NODES, dtype=torch.long),
        )
        self.assertEqual(h.shape, (1, 8))

        diff = ConditionalDiffusionModel(
            input_dim=num_targets,
            context_dim=context_dim,
            retrieval_dim=num_targets * 3,
            graph_dim=8,
            hidden_dim=8,
        )
        self.assertEqual(diff.input_dim, num_targets)
        out = diff(
            torch.randn(4, num_targets),
            torch.randint(0, 100, (4,)),
            torch.randn(4, context_dim),
            torch.randn(4, num_targets, 3),
            torch.randn(4, 8),
        )
        self.assertEqual(out.shape, (4, num_targets))

    def test_stats_shapes_follow_feature_and_target_dim(self):
        feature_cols = FEATURE_COLS_10
        stats = _make_stats(feature_cols)
        ds = TemporalGraphDataset(
            df=_make_df(), feature_cols=feature_cols, seq_len=2, stats=stats
        )
        self.assertEqual(ds.features_norm.shape, ds.features.shape)
        self.assertEqual(ds.targets_norm.shape, ds.targets.shape)


@unittest.skipUnless(
    os.path.exists("models/diffusion_chkpt.pth"), "real checkpoint not available"
)
class RealCheckpointDimContractTest(unittest.TestCase):
    """The shipped real artifact must satisfy the full dimension-sync contract."""

    @classmethod
    def setUpClass(cls):
        cls.ckpt = torch.load(
            "models/diffusion_chkpt.pth", map_location="cpu", weights_only=False
        )
        cls.cfg = cls.ckpt["config"]
        cls.stats = cls.ckpt["stats"]

    def test_context_dim_matches_feature_cols(self):
        self.assertEqual(len(self.cfg["feature_cols"]), self.cfg["context_dim"])

    def test_stats_dims_match_config_dims(self):
        self.assertEqual(len(self.stats["c_mean"]), self.cfg["context_dim"])
        self.assertEqual(len(self.stats["c_std"]), self.cfg["context_dim"])
        self.assertEqual(len(self.stats["t_mean"]), self.cfg["num_targets"])
        self.assertEqual(len(self.stats["t_std"]), self.cfg["num_targets"])

    def test_retrieval_dim_matches_num_targets_times_k(self):
        self.assertEqual(
            self.cfg["retrieval_dim"], self.cfg["num_targets"] * self.cfg["k_neighbors"]
        )

    def test_input_dim_matches_num_targets(self):
        # Older checkpoints may miss input_dim; num_targets then defines it.
        self.assertEqual(
            self.cfg.get("input_dim", self.cfg["num_targets"]), self.cfg["num_targets"]
        )

    def test_topology_metadata_matches_canonical_contract(self):
        self.assertEqual(self.cfg["num_nodes"], NUM_NODES)
        self.assertEqual(self.cfg["node_names"], NODE_NAMES)
        self.assertEqual(self.cfg["graph_topology"], "star")
        self.assertEqual(self.cfg["target_node_policy"], "main_node_only")


if __name__ == "__main__":
    unittest.main()
