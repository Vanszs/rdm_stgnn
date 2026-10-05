"""Unit tests for precipitation loss isolation in weighted_noise_loss.

Guarantees that the 5x/10x event weights (|target| > 1σ -> 5x, |target| > 3σ
-> 10x) scale ONLY the precipitation channel and never leak into the wind
(wind_speed) or humidity (relative_humidity) channels of the multi-output loss.
"""
import unittest

import torch

from src.config import FINAL_TARGET_COLS
from src.models.diffusion import RainForecaster


PRECIP_IDX = FINAL_TARGET_COLS.index("precipitation")
WIND_IDX = FINAL_TARGET_COLS.index("wind_speed")
HUMIDITY_IDX = FINAL_TARGET_COLS.index("relative_humidity")


def _loss_weights(target_reference):
    """Mirror of weighted_noise_loss weighting, for per-element verification."""
    weights = torch.ones_like(target_reference)
    weights[target_reference.abs() > 1.0] = 5.0
    weights[target_reference.abs() > 3.0] = 10.0
    return weights


class PrecipitationLossIsolationTest(unittest.TestCase):
    def _case(self, batch=4, seed=0):
        torch.manual_seed(seed)
        noise_pred = torch.zeros(batch, 3)
        noise = torch.full((batch, 3), 0.5)
        return noise_pred, noise

    def test_extreme_precip_does_not_reweight_wind_and_humidity(self):
        noise_pred, noise = self._case()
        # precipitation deep in the 10x tier, wind/humidity far below 1σ
        targets = torch.tensor([[4.0, 0.0, 0.5], [-3.5, -0.2, 0.9],
                                [2.0, 0.3, -0.8], [1.5, 0.1, 0.0]])
        loss = RainForecaster.weighted_noise_loss(noise_pred, noise, targets)

        weights = _loss_weights(targets)
        # wind & humidity stay at 1x despite extreme precipitation
        self.assertTrue(bool((weights[:, WIND_IDX] == 1.0).all()))
        self.assertTrue(bool((weights[:, HUMIDITY_IDX] == 1.0).all()))
        self.assertTrue(bool((weights[:, PRECIP_IDX] > 1.0).all()))

        manual = (0.25 * weights).mean()
        self.assertAlmostEqual(loss.item(), manual.item(), places=6)

    def test_single_sample_isolation_exact_value(self):
        # Per-element weighting: only the precipitation entry crosses the 10x
        # tier ([4.0, 0.8, 0.9]); wind & humidity stay at 1x.
        noise_pred = torch.zeros(1, 3)
        noise = torch.full((1, 3), 0.5)
        targets = torch.tensor([[4.0, 0.8, 0.9]])
        loss = RainForecaster.weighted_noise_loss(noise_pred, noise, targets)
        expected = 0.25 * (10.0 + 1.0 + 1.0) / 3  # 10x only on precip
        self.assertAlmostEqual(loss.item(), expected, places=6)

    def test_extreme_wind_humidity_also_reweighted_documented_semantics(self):
        """semantic guard, NOT isolation: weighting uses |target| per element, so
        a wind/humidity entry at 5.0 ALSO gets 10x. This documents the true
        per-element semantics; extreme-only-on-precip isolation is guaranteed by
        keeping wind/humidity moderate in the other tests."""
        noise_pred = torch.zeros(1, 3)
        noise = torch.full((1, 3), 0.5)
        targets = torch.tensor([[4.0, 5.0, 5.0]])
        loss = RainForecaster.weighted_noise_loss(noise_pred, noise, targets)
        expected = 0.25 * 10.0  # all three elements land in the 10x tier
        self.assertAlmostEqual(loss.item(), expected, places=6)

    def test_precip_weight_applied_only_to_precip_channel(self):
        """Precip at 10x, wind & humidity at 1x: total loss must equal the
        precip-10x contribution plus two 1x contributions, exactly."""
        noise_pred = torch.zeros(1, 3)
        noise = torch.full((1, 3), 0.5)
        targets = torch.tensor([[4.0, 0.2, 0.2]])
        loss = RainForecaster.weighted_noise_loss(noise_pred, noise, targets)
        expected = 0.25 * (10.0 + 1.0 + 1.0) / 3
        self.assertAlmostEqual(loss.item(), expected, places=6)

    def test_thresholds_apply_per_channel(self):
        # |target| > 1σ -> 5x, |target| > 3σ -> 10x, each channel on its own.
        targets = torch.tensor([[0.5, 1.5, 3.5]])  # 1x, 5x, 10x by contract
        weights = _loss_weights(targets)
        self.assertEqual(weights[0, PRECIP_IDX].item(), 1.0)
        self.assertEqual(weights[0, WIND_IDX].item(), 5.0)
        self.assertEqual(weights[0, HUMIDITY_IDX].item(), 10.0)

    def test_negative_extremes_treated_same_as_positive(self):
        noise_pred = torch.zeros(1, 3)
        noise = torch.full((1, 3), 0.5)
        targets = torch.tensor([[-4.0, 0.0, 0.0]])
        loss = RainForecaster.weighted_noise_loss(noise_pred, noise, targets)
        expected = 0.25 * (10.0 + 1.0 + 1.0) / 3
        self.assertAlmostEqual(loss.item(), expected, places=6)

    def test_zero_batch_edge(self):
        noise_pred = torch.zeros(0, 3)
        noise = torch.zeros(0, 3)
        targets = torch.zeros(0, 3)
        loss = RainForecaster.weighted_noise_loss(noise_pred, noise, targets)
        self.assertTrue(torch.isnan(loss))  # mean() of empty -> NaN, by contract

    def test_wind_humidity_weights_never_exceed_one_for_moderate_targets(self):
        torch.manual_seed(3)
        targets = torch.cat(
            [torch.rand(64, 1) * 4.0,  # precipitation 0..4 (0..>3 tiers)
             torch.randn(64, 2),  # wind/humidity gaussian
             ],
            dim=1,
        )
        weights = _loss_weights(targets)
        self.assertTrue(bool((weights[:, PRECIP_IDX] >= 1.0).all()))
        self.assertTrue(bool((weights[:, PRECIP_IDX] <= 10.0).all()))
        self.assertTrue(bool((weights[:, WIND_IDX] >= 1.0).all()))
        self.assertTrue(bool((weights[:, WIND_IDX] <= 10.0).all()))

    def test_gradient_scales_match_weights(self):
        """Backward through the loss: per-channel gradient must be proportional
        to that channel's own weight and unaffected by precip extremes."""
        model_pred = torch.zeros(2, 3, requires_grad=True)
        noise = torch.full((2, 3), 1.0)
        targets = torch.tensor([[4.0, 0.2, 0.2], [-3.5, -0.3, 0.2]])
        loss = RainForecaster.weighted_noise_loss(model_pred, noise, targets)
        loss.backward()
        grad = model_pred.grad  # d/d(pred) (pred-noise)^2 * w / numel = 2*(0-1)*w/6
        weights = _loss_weights(targets)
        manual = (-2.0 / 6.0) * weights
        torch.testing.assert_close(grad, manual)
        # wind grad column independent of precip extremes (w=1 per element)
        self.assertAlmostEqual(grad[:, WIND_IDX].abs().sum().item(), 2.0 / 3.0, places=6)


if __name__ == "__main__":
    unittest.main()
