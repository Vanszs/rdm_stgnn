"""Unit tests for src.inference.create_inference_graphs shape contract."""
import unittest

import torch

from src.config import NODE_NAMES, build_star_edge_attr
from src.inference import BatchGraphBuilder, create_inference_graphs
from src.models.gnn import SpatioTemporalGNN


class InferenceGraphsTest(unittest.TestCase):
    def _config(self):
        return {
            "seq_len": 6,
            "node_names": NODE_NAMES,
            "num_nodes": 5,
            "main_node_name": "MAIN",
            "graph_dim": 8,
            "feature_cols": ["f"],
        }

    def test_create_inference_graphs_correct_shape(self):
        cfg = self._config()
        cond = torch.randn(6, 5, 9)  # [seq_len, nodes, features]
        graphs = create_inference_graphs(cond, cfg, device="cpu")
        self.assertEqual(len(graphs), 6)
        self.assertEqual(graphs[0].x.shape, (5, 9))
        self.assertTrue(hasattr(graphs[0], "edge_attr"))
        self.assertEqual(graphs[0].edge_attr.shape, (8, 2))

    def test_create_inference_graphs_rejects_wrong_shape(self):
        cfg = self._config()
        cond = torch.randn(6, 9)  # missing node dimension
        with self.assertRaisesRegex(ValueError, "condition_sequence must be 3-dimensional"):
            create_inference_graphs(cond, cfg, device="cpu")

    def test_create_inference_graphs_rejects_wrong_node_count(self):
        cfg = self._config()
        cond = torch.randn(6, 3, 9)  # 3 nodes instead of 5
        with self.assertRaisesRegex(ValueError, "Condition node dimension mismatch"):
            create_inference_graphs(cond, cfg, device="cpu")


class BatchGraphBuilderEquivalenceTest(unittest.TestCase):
    """The batched builder must reproduce per-window graphs node-for-node."""

    def _config(self):
        return {
            "seq_len": 6,
            "node_names": NODE_NAMES,
            "num_nodes": 5,
            "main_node_name": "MAIN",
            "graph_dim": 8,
            "feature_cols": ["f"],
            "star_edges": None,
        }

    def test_batch_matches_per_window(self):
        cfg = self._config()
        torch.manual_seed(0)
        windows = torch.randn(3, 6, 5, 9)  # [B, seq_len, nodes, features]

        builder = BatchGraphBuilder(cfg, device="cpu")
        batched = builder.build(windows)
        self.assertEqual(len(batched), 6)
        self.assertEqual(batched[0].x.shape, (15, 9))
        # every node must know which graph it belongs to, and each graph must own
        # exactly one copy of the star topology (8 directed edges).
        self.assertEqual(batched[0].batch.tolist(), [0] * 5 + [1] * 5 + [2] * 5)
        self.assertEqual(batched[0].edge_index.shape, (2, 24))

        gnn = SpatioTemporalGNN(node_features=9, hidden_dim=8, output_dim=8, seq_len=6)
        gnn.eval()
        with torch.no_grad():
            emb_batch = gnn(batched)
            emb_loop = torch.cat(
                [gnn(create_inference_graphs(windows[i], cfg, device="cpu")) for i in range(3)],
                dim=0,
            )
        self.assertTrue(torch.allclose(emb_batch, emb_loop, atol=1e-5))

    def test_batch_rejects_bad_shapes(self):
        cfg = self._config()
        builder = BatchGraphBuilder(cfg, device="cpu")
        with self.assertRaisesRegex(ValueError, "4-dimensional"):
            builder.build(torch.randn(6, 5, 9))
        with self.assertRaisesRegex(ValueError, "seq dim"):
            builder.build(torch.randn(3, 4, 5, 9))
        with self.assertRaisesRegex(ValueError, "node dim"):
            builder.build(torch.randn(3, 6, 4, 9))
