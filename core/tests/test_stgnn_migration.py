"""Contract tests for the ST-GNN edge-attribute and temporal-pooling migration."""
import unittest

import torch
from torch_geometric.data import Data

import sys
sys.path.insert(0, ".")

from src.config import NODE_NAMES, build_star_edge_attr, build_star_edge_index
from src.inference import migrate_legacy_st_gnn_state
from src.models.gnn import SpatioTemporalGNN, TemporalAttention


class TemporalPoolingTest(unittest.TestCase):
    def _graphs(self, batch=4, nodes=5, features=9, seq_len=6, edge_dim=2):
        edge_index = build_star_edge_index(NODE_NAMES)
        edge_attr = build_star_edge_attr(NODE_NAMES)
        x = torch.randn(batch * nodes, features)
        node_batch = torch.arange(batch).repeat_interleave(nodes)
        return [
            Data(x=x, edge_index=edge_index, edge_attr=edge_attr, batch=node_batch)
            for _ in range(seq_len)
        ]

    def test_pooling_uses_all_timesteps(self):
        """
        Changing any single timestep must change the pooled embedding, proving the
        sequence is no longer reduced to `x[:, -1, :]`.
        """
        torch.manual_seed(0)
        gnn = SpatioTemporalGNN(node_features=9, hidden_dim=8, output_dim=8, seq_len=6).eval()
        graphs = self._graphs()
        with torch.no_grad():
            base = gnn(graphs)
            for t in range(6):
                mutated = [g.clone() for g in graphs]
                mutated[t].x = mutated[t].x + 1.0
                self.assertFalse(
                    torch.allclose(base, gnn(mutated), atol=1e-6),
                    f"timestep {t} is ignored by temporal pooling",
                )

    def test_pooling_is_permutation_equivariant_shape(self):
        """Pooling must not depend on seq_len beyond max_len; shape stays [B, out]."""
        attn = TemporalAttention(hidden_dim=8, num_heads=2, max_len=64).eval()
        for seq_len in (1, 2, 6, 17):
            with torch.no_grad():
                out = attn(torch.randn(3, seq_len, 8))
            self.assertEqual(tuple(out.shape), (3, 8))

    def test_pooling_rejects_overlong_sequence(self):
        attn = TemporalAttention(hidden_dim=8, num_heads=2, max_len=4)
        with self.assertRaisesRegex(ValueError, "exceeds max_len"):
            attn(torch.randn(2, 5, 8))

    def test_backward_through_pooling(self):
        gnn = SpatioTemporalGNN(node_features=9, hidden_dim=8, output_dim=8, seq_len=6)
        gnn(self._graphs()).sum().backward()
        self.assertIsNotNone(gnn.temporal_attn.pool_query.grad)
        self.assertGreater(float(gnn.temporal_attn.pool_query.grad.norm()), 0.0)


class EdgeBranchTest(unittest.TestCase):
    def test_edge_dim_none_allocates_no_edge_params(self):
        from src.models.gnn import SpatialGNN

        gnn = SpatialGNN(input_dim=9, hidden_dim=8, output_dim=8, edge_dim=None)
        names = set(dict(gnn.named_parameters()))
        self.assertFalse(any("lin_edge" in n or "att_edge" in n for n in names))

    def test_legacy_state_migration_widens_edge_projection(self):
        legacy = SpatioTemporalGNN(node_features=9, hidden_dim=8, output_dim=8, seq_len=6, edge_dim=1)
        state = legacy.state_dict()
        self.assertEqual(state["spatial_gnn.conv1.lin_edge.weight"].shape[-1], 1)

        migrated = migrate_legacy_st_gnn_state(state, {})
        self.assertEqual(migrated["spatial_gnn.conv1.lin_edge.weight"].shape[-1], 2)
        self.assertTrue(
            torch.equal(
                migrated["spatial_gnn.conv1.lin_edge.weight"][:, 1],
                torch.zeros_like(migrated["spatial_gnn.conv1.lin_edge.weight"][:, 1]),
            )
        )

        new = SpatioTemporalGNN(node_features=9, hidden_dim=8, output_dim=8, seq_len=6, edge_dim=2)
        missing, unexpected = new.load_state_dict(migrated, strict=False)
        self.assertEqual(missing, [])
        self.assertEqual(unexpected, [])

    def test_current_state_passes_through_migration(self):
        current = SpatioTemporalGNN(node_features=9, hidden_dim=8, output_dim=8, seq_len=6, edge_dim=2)
        migrated = migrate_legacy_st_gnn_state(current.state_dict(), {})
        self.assertEqual(migrated["spatial_gnn.conv1.lin_edge.weight"].shape[-1], 2)


if __name__ == "__main__":
    unittest.main()
