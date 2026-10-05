"""Unit tests for edge_attr behavior in SpatioTemporalGNN."""
import unittest

import torch
from torch_geometric.data import Data

from src.config import NODE_NAMES, build_star_edge_attr, build_star_edge_index
from src.models.gnn import SpatioTemporalGNN


class GNNEdgeAttrTest(unittest.TestCase):
    def _make_graphs(self, edge_attr_value, node_features=9, hidden_dim=8):
        edge_index = build_star_edge_index(NODE_NAMES)
        edge_attr = torch.full((edge_index.shape[1], 2), edge_attr_value, dtype=torch.float32)
        x = torch.randn(5, node_features)
        # batch assignment: all 5 nodes belong to the same graph sample.
        batch = torch.zeros(5, dtype=torch.long)
        graphs = [Data(x=x, edge_index=edge_index, edge_attr=edge_attr, batch=batch) for _ in range(6)]
        return graphs

    def test_gnn_output_shape(self):
        gnn = SpatioTemporalGNN(
            node_features=9, hidden_dim=8, output_dim=8, seq_len=6
        )
        graphs = self._make_graphs(0.25)
        out = gnn(graphs)
        self.assertEqual(out.shape, (1, 8))

    def test_edge_attr_encodes_haversine_distance(self):
        """
        Edge attributes must carry real geography, not a constant grid step:
        the E/W neighbours sit ~0.19 km closer to MAIN than the N/S neighbours on
        this (non-conformal) lat/lon grid, and the two features are monotone inverses.
        """
        edge_attr = build_star_edge_attr(NODE_NAMES)
        self.assertEqual(tuple(edge_attr.shape), (8, 2))
        self.assertFalse(bool((edge_attr == edge_attr[0]).all()))

        main_to_up = edge_attr[0]      # MAIN -> UP (north-south leg)
        main_to_left = edge_attr[4]    # MAIN -> LEFT (east-west leg)
        self.assertLess(float(main_to_left[0]), float(main_to_up[0]))
        self.assertGreaterEqual(float(edge_attr.min()), 0.0)
        # feature 1 = 1 / (1 + feature 0)
        expected = 1.0 / (1.0 + edge_attr[:, 0])
        self.assertTrue(torch.allclose(edge_attr[:, 1], expected, atol=1e-6))
