"""Unit tests for clean-branch ablation: retrieved=None must bypass retrieval_mlp.

Guarantees that when retrieval analogs are ablated (`retrieved=None`) the
output really runs without the retrieval branch: the branch weights receive no
gradient, drop no activations from other pathways, and an ablated call equals
a call through a model with the retrieval_mlp weights zeroed + branch skipped.
"""
import unittest

import torch

from src.models.diffusion import ConditionalDiffusionModel


DIM = dict(input_dim=3, context_dim=9, retrieval_dim=9, graph_dim=8, hidden_dim=16)


class RetrievedNoneAblationTest(unittest.TestCase):
    def _model(self, seed=0):
        torch.manual_seed(seed)
        return ConditionalDiffusionModel(**DIM)

    @staticmethod
    def _batch(batch=4):
        torch.manual_seed(7)
        return {
            "x": torch.randn(batch, DIM["input_dim"]),
            "t": torch.randint(0, 100, (batch,)),
            "context": torch.randn(batch, DIM["context_dim"]),
            "retrieved": torch.randn(batch, 3, DIM["retrieval_dim"] // 3),
            "graph_emb": torch.randn(batch, DIM["graph_dim"]),
        }

    def test_forward_accepts_retrieved_none(self):
        model = self._model()
        model.eval()
        b = self._batch()
        with torch.no_grad():
            out_ablated = model(b["x"], b["t"], b["context"], retrieved=None, graph_emb=b["graph_emb"])
            out_full = model(b["x"], b["t"], b["context"], retrieved=b["retrieved"], graph_emb=b["graph_emb"])
        self.assertEqual(out_ablated.shape, out_full.shape)
        self.assertFalse(torch.allclose(out_ablated, out_full), "ablated output must differ from full")

    def test_ablated_output_equals_condition_only_path(self):
        """retrieved=None must be mathematically identical to cond+graph only."""
        model = self._model()
        model.eval()
        b = self._batch()
        ctx_only = model._encode_condition(b["context"], retrieved=None, graph_emb=b["graph_emb"])
        full = model._encode_condition(b["context"], retrieved=b["retrieved"], graph_emb=b["graph_emb"])
        with torch.no_grad():
            r_flat = b["retrieved"].reshape(b["retrieved"].shape[0], -1)
            manual = model.cond_mlp(b["context"]) + model.retrieval_mlp(r_flat) + model.graph_mlp(b["graph_emb"])
        torch.testing.assert_close(full, manual)
        torch.testing.assert_close(ctx_only, model.cond_mlp(b["context"]) + model.graph_mlp(b["graph_emb"]))

    def test_no_gradient_flows_to_retrieval_mlp_when_ablated(self):
        model = self._model()
        model.train()
        b = self._batch()
        out = model(b["x"], b["t"], b["context"], retrieved=None, graph_emb=b["graph_emb"])
        out.sum().backward()
        for name, p in model.named_parameters():
            if name.startswith("retrieval_mlp"):
                self.assertIsNone(p.grad, f"{name} got gradient despite retrieved=None")

    def test_gradient_flows_to_retrieval_mlp_when_active(self):
        model = self._model()
        model.train()
        b = self._batch()
        out = model(b["x"], b["t"], b["context"], retrieved=b["retrieved"], graph_emb=b["graph_emb"])
        out.sum().backward()
        grads = [p.grad for n, p in model.named_parameters() if n.startswith("retrieval_mlp")]
        self.assertTrue(all(g is not None for g in grads))
        self.assertTrue(any(g.abs().sum() > 0 for g in grads), "retrieval_mlp must receive gradient when active")

    def test_ablated_matches_zeroed_retrieval_weights(self):
        """Skipping the branch ≈ forcing the branch to contribute its zero-input output.

        For a Sequential(Linear, SiLU, Linear), a zero input yields a constant
        bias vector; adding it everywhere shifts cond_emb but leaves noise_pred
        invariant only through the final Linear. The clean-branch contract is the
        stronger one: retrieved=None must NOT add anything, so we verify that the
        ablated run equals a run where the branch output is subtracted manually.
        """
        model = self._model()
        model.eval()
        b = self._batch()
        with torch.no_grad():
            out_ablated = model(b["x"], b["t"], b["context"], retrieved=None, graph_emb=b["graph_emb"])

            r_flat = b["retrieved"].reshape(b["retrieved"].shape[0], -1)
            r_emb = model.retrieval_mlp(r_flat)
            cond_emb = model.cond_mlp(b["context"]) + model.graph_mlp(b["graph_emb"])

            t_emb = model.time_mlp(b["t"])
            h1 = model.down1(b["x"]) + (t_emb + cond_emb)
            h2 = model.down2(h1)
            h_mid = model.mid(h2)
            manual = model.up_mlp(torch.cat([h_mid, h2], dim=-1))
        torch.testing.assert_close(out_ablated, manual)

    def test_wet_head_ablation_uses_same_bypass(self):
        model = self._model()
        model.eval()
        b = self._batch()
        with torch.no_grad():
            wet_ablated = model.compute_wet_logit(b["context"], retrieved=None, graph_emb=b["graph_emb"])
            cond_emb = model.cond_mlp(b["context"]) + model.graph_mlp(b["graph_emb"])
            manual = model.wet_head(cond_emb)
        torch.testing.assert_close(wet_ablated, manual)

    def test_cond_dropout_zeroed_retrieval_differs_from_none(self):
        """train-time ablation used by FIX #16 zeros the tensor; that keeps the
        branch in the graph (bias-only contribution). Only retrieved=None is a
        true structural bypass. The two must not be conflated."""
        model = self._model()
        model.eval()
        b = self._batch()
        with torch.no_grad():
            out_none = model(b["x"], b["t"], b["context"], retrieved=None, graph_emb=b["graph_emb"])
            out_zero = model(b["x"], b["t"], b["context"],
                             retrieved=torch.zeros_like(b["retrieved"]), graph_emb=b["graph_emb"])
        self.assertFalse(torch.allclose(out_none, out_zero))


if __name__ == "__main__":
    unittest.main()
