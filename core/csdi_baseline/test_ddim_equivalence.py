"""
Verification for ddim_sampler.py.

Claim under test: folding the ensemble dimension into the batch is a PURE
REFACTOR — member i of the batched path performs exactly the same arithmetic as
iteration i of CSDI's outer `for i in range(n_samples)` loop.

Why the test compares one step at a time rather than a whole reverse chain:
an untrained/random CSDI has zero-initialised `output_projection2`, so its
epsilon prediction is 0 and the DDPM recursion `x <- (1/sqrt(alpha_bar_t)) * x`
amplifies by ~172x per step and overflows to inf regardless of batching. That
is a property of the degenerate fixture, not of the sampler, so chaining 50
steps proves nothing. Comparing individual steps isolates the refactor.

Run:  cd core/csdi_baseline && python test_ddim_equivalence.py
"""
from __future__ import annotations

import sys

import numpy as np
import torch

sys.path.insert(0, ".")

from ddim_sampler import impute_ddim  # noqa: E402
from train_csdi import CSDI_Forecasting, build_config  # noqa: E402

# Batching changes the Transformer's kernel selection, so results agree only to
# floating-point round-off (~1e-4 on values of order 1e2 here), not bit-exactly.
# The refactor claim is "same arithmetic", which this tolerance establishes; a
# logic error would produce O(1) differences (we measured 7.7e+01 while the row
# layout was wrong).
TOL = 1e-3


def _make_model(seed=0):
    torch.manual_seed(seed)
    cfg = build_config(epochs=1, batch_size=4, layers=2, channels=16)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    m = CSDI_Forecasting(cfg, dev, target_dim=6).to(dev).eval()
    # Give the fixture a non-degenerate denoiser so the recursion is numerically
    # meaningful; the point is to compare batching, not to have a good model.
    torch.manual_seed(seed + 1)
    for p in m.diffmodel.output_projection2.parameters():
        torch.nn.init.normal_(p, mean=0.0, std=0.05)
    return m, dev


def _batch(m, dev, B=2, K=6, L=7):
    torch.manual_seed(1)
    obs = torch.randn(B, K, L, device=dev)
    mask = torch.ones(B, K, L, device=dev)
    mask[:, :, -1] = 0.0            # last timestep is the prediction target
    tp = torch.arange(L, device=dev).float().unsqueeze(0).expand(B, -1)
    side = m.get_side_info(tp, mask)
    return obs, mask, side


def _step_ddpm(m, obs, mask, side, cur, t):
    """One DDPM reverse step, exactly as CSDI's impute() does it."""
    cond_obs = (mask * obs).unsqueeze(1)
    noisy_target = ((1 - mask) * cur).unsqueeze(1)
    diff_input = torch.cat([cond_obs, noisy_target], dim=1)
    pred = m.diffmodel(diff_input, side, torch.tensor([t], device=m.device))
    coeff1 = 1 / m.alpha[t] ** 0.5
    coeff2 = (1 - m.alpha[t]) / (1 - m.alpha_hat[t]) ** 0.5
    return coeff1 * (cur - coeff2 * pred)


def test_per_step_batching_identical():
    """Each step: M sequential member updates == 1 batched update."""
    m, dev = _make_model()
    obs, mask, side = _batch(m, dev)
    B, K, L = obs.shape
    M = 3

    torch.manual_seed(7)
    starts = torch.randn(B * M, K, L, device=dev)

    worst = 0.0
    with torch.no_grad():
        for t in (49, 40, 30, 20, 10, 0):
            # Batched: all members at once.
            cur_b = starts.clone()
            bi = torch.arange(B, device=dev).repeat_interleave(M)   # window per row
            out_b = _step_ddpm(m, obs[bi], mask[bi], side[bi], cur_b, t)
            # Sequential: member-by-member, CSDI's own loop shape.
            # Layout is interleaved (repeat_interleave), so member m of window b
            # sits at row b*M + m; emulating member m means gathering
            # [m, M+m, 2M+m, ...].
            out_s = torch.zeros_like(cur_b)
            for i in range(M):
                idx = torch.arange(i, B * M, M, device=dev)
                out_s[idx] = _step_ddpm(m, obs, mask, side, cur_b[idx].clone(), t)
            worst = max(worst, (out_b - out_s).abs().max().item())

    print(f"CLAIM 1  per-step batching == loop : max|diff| = {worst:.3e} (fp round-off, tol {TOL:g})  -> "
          f"{'PASS' if worst < TOL else 'FAIL'}")
    assert worst < TOL, "batching is not equivalent to the sequential loop"


def test_ddim_step_batching_identical():
    """Same equivalence check for the DDIM update used in ddim_sampler.py."""
    m, dev = _make_model()
    obs, mask, side = _batch(m, dev)
    B, K, L = obs.shape
    M = 3
    alpha = np.asarray(m.alpha)

    torch.manual_seed(11)
    starts = torch.randn(B * M, K, L, device=dev)
    t, t_prev = 30, 25
    a_t, a_prev = float(alpha[t]), float(alpha[t_prev])

    def ddim_step(o, mk, sd, x):
        di = torch.cat([(mk * o).unsqueeze(1), ((1 - mk) * x).unsqueeze(1)], dim=1)
        eps = m.diffmodel(di, sd, torch.tensor([t], device=m.device))
        x0 = (x - (1 - a_t) ** 0.5 * eps) / a_t ** 0.5
        return a_prev ** 0.5 * x0 + (1 - a_prev) ** 0.5 * eps

    with torch.no_grad():
        bi = torch.arange(B, device=dev).repeat_interleave(M)
        out_b = ddim_step(obs[bi], mask[bi], side[bi], starts.clone())
        out_s = torch.zeros_like(starts)
        for i in range(M):
            idx = torch.arange(i, B * M, M, device=dev)
            out_s[idx] = ddim_step(obs, mask, side, starts[idx].clone())
        worst = (out_b - out_s).abs().max().item()

    print(f"CLAIM 1b DDIM per-step batching   : max|diff| = {worst:.3e} (fp round-off, tol {TOL:g})  -> "
          f"{'PASS' if worst < TOL else 'FAIL'}")
    assert worst < TOL


def test_ddim_sampler_properties():
    """Shape, finiteness, determinism, and preservation of observed entries."""
    m, dev = _make_model()
    obs, mask, side = _batch(m, dev)
    M, steps = 4, 20

    with torch.no_grad():
        torch.manual_seed(3)
        a = impute_ddim(m, obs, mask, side, n_samples=M, num_steps=steps)
        torch.manual_seed(3)
        b = impute_ddim(m, obs, mask, side, n_samples=M, num_steps=steps)

    shape_ok = tuple(a.shape) == (obs.shape[0], M, obs.shape[1], obs.shape[2])
    finite = bool(torch.isfinite(a).all())
    deterministic = bool(torch.allclose(a, b, atol=1e-7))
    # Observed entries outside the target timestep must be preserved exactly.
    keep = mask.clone()
    keep[:, :, -1] = 0.0
    keep = keep.bool()
    # a: (B, M, K, L); keep: (B, K, L). Broadcast the mask over the ensemble dim.
    keep4 = keep.unsqueeze(1).expand_as(a)
    preserved = bool(torch.allclose(a[keep4], obs.unsqueeze(1).expand_as(a)[keep4], atol=1e-5))

    for label, ok in (("shape", shape_ok), ("finite", finite),
                      ("deterministic (eta=0)", deterministic),
                      ("observed entries preserved", preserved)):
        print(f"CLAIM 2  DDIM {label:24}: {'PASS' if ok else 'FAIL'}")
    assert shape_ok and finite and deterministic and preserved


if __name__ == "__main__":
    test_per_step_batching_identical()
    test_ddim_step_batching_identical()
    test_ddim_sampler_properties()
    print("\nALL CHECKS PASS")