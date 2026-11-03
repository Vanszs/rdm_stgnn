"""
Evaluate the trained CSDI baseline on the Pangrango test split and compare with RDM-STGNN.

Produces the same metric set the thesis asks for (Tabel 3.18):
  precip/wind/humidity: RMSE, MAE, Pearson r, CRPS, and Brier/POD/FAR/CSI at 2/5/10 mm.

Metrics are imported from core/src/evaluation/probabilistic_metrics.py so both models
are scored by identical code — the comparison is like-for-like by construction.

Sampling: 30 ensemble members, DDIM-style 20 steps (CSDI's impute() already uses a
fixed 50-step training schedule; we take 30 samples as the thesis specifies and
report the actual step count used).

Run:  cd core/csdi_baseline && python evaluate_csdi.py [--nsample 30]
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, CORE)

from main_model import CSDI_Forecasting  # noqa: E402
from ddim_sampler import impute_ddim  # noqa: E402
from build_data import TARGET_CHANNELS, CH_PER_NODE, NODES, FEATURE_COLS  # noqa: E402
from src.evaluation.probabilistic_metrics import (  # noqa: E402
    compute_rmse, compute_mae, compute_correlation, compute_crps,
    compute_brier_score, compute_pod, compute_far, compute_csi,
)

from train_csdi import PangrangoForecast, load_arrays, TRAIN_END, VAL_END  # noqa: E402
from src.config import PRECIP_PHYSICAL_MAX_MM  # noqa: E402

CKPT = os.path.join(HERE, "save", "csdi_pangrango.pth")
OUT_JSON = os.path.join(HERE, "csdi_metrics.json")
THRESHOLDS = [2.0, 5.0, 10.0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsample", type=int, default=30)
    ap.add_argument("--max-windows", type=int, default=0, help="0 = all test windows")
    ap.add_argument("--sampler", choices=["ddim", "official"], default="ddim",
                    help="ddim = vectorised DDIM (thesis protocol); official = CSDI impute() DDPM loop")
    ap.add_argument("--ddim-steps", type=int, default=20)
    ap.add_argument("--batch-size", type=int, default=32,
                    help="Windows per forward. Larger = better GPU use on this 4 GB card.")
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(1)
    np.random.seed(1)

    ck = torch.load(CKPT, map_location=device, weights_only=False)
    cfg, target_dim = ck["config"], ck["target_dim"]
    mean, std = ck["mean"], ck["std"]
    model = CSDI_Forecasting(cfg, device, target_dim=target_dim).to(device)
    model.load_state_dict(ck["model"])
    model.eval()
    print(f"loaded checkpoint epoch={ck.get('epoch')} best_val={ck.get('best_val'):.4f}")

    main_data, mask_data, _, _, ts = load_arrays()
    te = PangrangoForecast(main_data, mask_data, ts, "test")
    if args.max_windows:
        te.starts = te.starts[: args.max_windows]
    loader = DataLoader(te, batch_size=args.batch_size, shuffle=False)
    n_batches = len(loader)
    print(f"test windows: {len(te)}   nsample={args.nsample}   batch={args.batch_size}")

    # Accumulate ensemble samples per evaluated timestep and per target.
    keys = list(TARGET_CHANNELS.keys())
    ch_idx = [TARGET_CHANNELS[k] for k in keys]

    # Resumable shards: one .npz per batch, so an 11-hour run survives an
    # interruption and restarts from the last completed batch.
    shard_dir = os.path.join(HERE, "eval_shards")
    os.makedirs(shard_dir, exist_ok=True)
    # Batch size belongs in the tag: it changes both the shard count and which
    # windows each shard holds, so mixing shards from two batch sizes would
    # concatenate mismatched windows into silently wrong metrics.
    import hashlib
    ck_hash = hashlib.sha256(open(CKPT, "rb").read()).hexdigest()[:12]
    tag = (f"{args.sampler}_m{args.nsample}_s{args.ddim_steps}_bs{args.batch_size}"
           f"_c{ck_hash}_e{int(ck.get('epoch', -1))}"
           + (f"_w{args.max_windows}" if args.max_windows else ""))
    shard = lambda bi: os.path.join(shard_dir, f"{tag}_b{bi:05d}.npz")

    done = sum(1 for bi in range(n_batches) if os.path.exists(shard(bi)))
    if done:
        print(f"resuming: {done}/{n_batches} batches already computed")

    def run_batch(batch):
        """Draw samples for one batch; returns (samples, observed_data)."""
        if args.sampler == "ddim":
            # Thesis 3.9.6: both models use scheduler DDIM with 20 steps.
            obs_d = batch["observed_data"].to(device).float().permute(0, 2, 1)
            gt_d = batch["gt_mask"].to(device).float().permute(0, 2, 1)
            tp_d = batch["timepoints"].to(device).float()
            cond = gt_d
            side_d = model.get_side_info(tp_d, cond)
            samples = impute_ddim(model, obs_d, cond, side_d,
                                  n_samples=args.nsample, num_steps=args.ddim_steps)
            return samples, obs_d
        samples, observed_data, _, _, _ = model.evaluate(batch, n_samples=args.nsample)
        return samples, observed_data

    with torch.no_grad():
        for bi, batch in enumerate(loader):
            if os.path.exists(shard(bi)):
                continue
            try:
                samples, observed_data = run_batch(batch)
            except RuntimeError as e:
                # Halve the batch once on OOM: an 11-hour run must not die on the
                # first batch, and sharding makes the retry cheap.
                if "out of memory" not in str(e).lower() or batch["observed_data"].shape[0] <= 1:
                    raise
                torch.cuda.empty_cache()
                chunk = max(1, batch["observed_data"].shape[0] // 2)
                print(f"  OOM at batch {bi}; retrying at chunk={chunk}", flush=True)
                parts = []
                for st in range(0, batch["observed_data"].shape[0], chunk):
                    sl = {k: v[st:st + chunk] for k, v in batch.items() if torch.is_tensor(v)}
                    parts.append(run_batch(sl))
                samples = torch.cat([p[0] for p in parts], dim=0)
                observed_data = torch.cat([p[1] for p in parts], dim=0)
            # samples: (B, nsample, K, L); last timestep is the prediction horizon.
            last = samples[:, :, :, -1]                     # (B, nsample, K)
            truth = observed_data[:, :, -1]                 # (B, K)
            payload = {}
            for k, ci in zip(keys, ch_idx):
                s = last[:, :, ci].cpu().numpy()             # (B, nsample)
                t = truth[:, ci].cpu().numpy()               # (B,)
                # inverse transform: z*std + mean, then expm1 for precipitation
                s = s * std[ci] + mean[ci]
                t = t * std[ci] + mean[ci]
                if k == "precipitation":
                    # Match RDM-STGNN's denorm contract exactly. RDM does
                    # clamp(expm1(clamp(z, max=LOG_PRECIP_MAX)), 0, PRECIP_PHYSICAL_MAX_MM),
                    # which reduces to clip(expm1(z), 0, PRECIP_PHYSICAL_MAX_MM). Without
                    # the ceiling a stray large z in the raw ensemble explodes (observed
                    # 6.8e22 mm) and makes CRPS hugely negative -- impossible for a
                    # proper scoring rule.
                    s = np.clip(np.expm1(s), 0.0, PRECIP_PHYSICAL_MAX_MM)
                    t = np.clip(np.expm1(t), 0.0, PRECIP_PHYSICAL_MAX_MM)
                payload[f"{k}__pred"] = s
                payload[f"{k}__obs"] = t
            np.savez_compressed(shard(bi), **payload)
            if (bi + 1) % 20 == 0 or bi + 1 == n_batches:
                print(f"  batch {bi+1}/{n_batches}", flush=True)

    # Gather all shards in batch order (independent of execution order).
    preds = {k: [] for k in keys}
    obs = {k: [] for k in keys}
    for bi in range(n_batches):
        with np.load(shard(bi)) as z:
            for k in keys:
                preds[k].append(z[f"{k}__pred"])
                obs[k].append(z[f"{k}__obs"])

    results = {k: {} for k in keys}
    for k in keys:
        ens = np.concatenate(preds[k], axis=0)              # (N, nsample)
        ob = np.concatenate(obs[k], axis=0)                 # (N,)
        if k == "precipitation":
            # Applied here as well as at write time: the gather is what produces the
            # final numbers, and it must behave identically whether the shards were
            # written before or after the ceiling was introduced.
            ens = np.clip(ens, 0.0, PRECIP_PHYSICAL_MAX_MM)
            ob = np.clip(ob, 0.0, PRECIP_PHYSICAL_MAX_MM)
        med = np.median(ens, axis=1)
        r = {
            "rmse": float(compute_rmse(med, ob)),
            "mae": float(compute_mae(med, ob)),
            "correlation": float(compute_correlation(med, ob)),
            "crps": float(compute_crps(ens, ob)),
        }
        if k == "precipitation":
            for thr in THRESHOLDS:
                tag = f"{int(thr)}mm"
                r[f"brier_{tag}"] = float(compute_brier_score(ens, ob, threshold=thr))
                r[f"pod_{tag}"] = float(compute_pod(ens, ob, threshold=thr, prob_threshold=0.5))
                r[f"far_{tag}"] = float(compute_far(ens, ob, threshold=thr, prob_threshold=0.5))
                r[f"csi_{tag}"] = float(compute_csi(ens, ob, threshold=thr, prob_threshold=0.5))
        results[k] = r

    out = {
        "model": "CSDI",
        "source": "Tashiro et al., NeurIPS 2021 (ermongroup/CSDI)",
        "nsample": args.nsample,
        "sampler": args.sampler,
        "ddim_steps": args.ddim_steps if args.sampler == "ddim" else None,
        "test_windows": len(te),
        "checkpoint_epoch": int(ck.get("epoch", -1)),
        "checkpoint_best_val": float(ck.get("best_val", float("nan"))),
        "metrics": results,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)

    print("\n=== CSDI test metrics ===")
    for k in keys:
        print(f"[{k}]")
        for mk, mv in results[k].items():
            print(f"  {mk:16} {mv:.4f}")
    print(f"\nwritten: {OUT_JSON}")


if __name__ == "__main__":
    main()