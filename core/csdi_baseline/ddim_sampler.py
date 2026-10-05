"""
DDIM sampler for CSDI, batched over ensemble members.

Why this file exists
--------------------
The official CSDI `impute()` samples ensembles with an *outer* Python loop:

    for i in range(n_samples):              # 30
        for t in reversed(range(num_steps)):  # 50
            predicted = self.diffmodel(...)

That is 1,500 sequential forward passes per window and takes 3.9 s/window on an
RTX 3050 Laptop -> ~38 h for the 35,058-window test split (measured, not guessed).

Two changes, both required by the thesis protocol (Section 3.9.6: "the same
diffusion inference configuration, scheduler DDIM with 20 steps"):

  1. Ensemble dimension is folded into the batch: each of the `n_samples`
     members is an independent row, so all members advance through the
     reverse process together. This is mathematically identical to the loop —
     members never interact — and is verified against the original `impute()`
     in `test_ddim_equivalence.py`.
  2. The reverse process is DDIM (deterministic, `eta=0`) with a configurable
     step count, instead of DDPM's fixed 50 stochastic steps, so both models in
     the comparison use scheduler DDIM with 20 steps.

Nothing here changes the trained network; it only changes how samples are drawn.
"""
from __future__ import annotations

import numpy as np
import torch


@torch.no_grad()
def impute_ddim(
    model,
    observed_data: torch.Tensor,
    cond_mask: torch.Tensor,
    side_info: torch.Tensor,
    n_samples: int = 30,
    num_steps: int = 20,
) -> torch.Tensor:
    """Draw `n_samples` DDIM samples for a batch of windows.

    Args:
        model: a CSDI model instance (uses .diffmodel, .alpha, .alpha_hat, .device)
        observed_data: (B, K, L)
        cond_mask:     (B, K, L) — 1 where observed (condition), 0 where to predict
        side_info:     (B, *, K, L) from model.get_side_info()
        n_samples:     ensemble size M
        num_steps:     DDIM steps (thesis uses 20)

    Returns:
        (B, n_samples, K, L)
    """
    B, K, L = observed_data.shape
    device = model.device

    alpha = np.asarray(model.alpha)         # cumulative prod of (1-beta), length T
    alpha_hat = np.asarray(model.alpha_hat)  # 1 - beta
    T = len(alpha)

    # DDIM step schedule: evenly spaced indices incl. the final step, descending.
    step_idx = np.linspace(0, T - 1, num_steps).round().astype(int)[::-1]

    # Fold the ensemble into the batch: (B*M, K, L)
    rep = lambda t: t.repeat_interleave(n_samples, dim=0)
    obs_rep = rep(observed_data)
    mask_rep = rep(cond_mask)
    side_rep = rep(side_info)

    x = torch.randn(B * n_samples, K, L, device=device)

    for i, t in enumerate(step_idx):
        t_prev = step_idx[i + 1] if i + 1 < len(step_idx) else -1
        a_t = float(alpha[t])
        a_prev = float(alpha[t_prev]) if t_prev >= 0 else 1.0

        diff_input = torch.cat(
            [(mask_rep * obs_rep).unsqueeze(1), ((1 - mask_rep) * x).unsqueeze(1)], dim=1
        )
        eps = model.diffmodel(diff_input, side_rep, torch.tensor([t], device=device))

        # DDIM (eta=0): deterministic update using the implied x0.
        x0 = (x - (1 - a_t) ** 0.5 * eps) / a_t ** 0.5
        x = a_prev ** 0.5 * x0 + (1 - a_prev) ** 0.5 * eps

    # Keep the known (conditioned) entries exactly as observed for stability.
    x = mask_rep * obs_rep + (1 - mask_rep) * x
    return x.reshape(B, n_samples, K, L)