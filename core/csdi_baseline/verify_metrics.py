"""
Independently recompute CSDI metrics from the raw shards and check them against
csdi_metrics.json.

Completion criterion (d) for Tabel 3.18 is that every number is traceable to a raw
output file. csdi_metrics.json is a derived file; the shards in eval_shards/ are the
raw record. This script closes that gap: it recomputes every metric straight from
the shards, using the same metric module, and fails loudly if the derived file
disagrees. It also reports coverage, so a table built from a partial run is caught.

Read-only with respect to the repo. Exit 0 = traceable, 1 = mismatch/missing.

Run:  cd core/csdi_baseline && python verify_metrics.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, CORE)

from src.evaluation.probabilistic_metrics import (  # noqa: E402
    compute_rmse, compute_mae, compute_correlation, compute_crps,
    compute_brier_score, compute_pod, compute_far, compute_csi,
)
from src.config import PRECIP_PHYSICAL_MAX_MM  # noqa: E402

TAG = "ddim_m30_s20_bs32"
TOTAL_SHARDS = 1096
TOTAL_WINDOWS = 35058
THRESHOLDS = [2.0, 5.0, 10.0]
KEYS = ["precipitation", "wind_speed", "relative_humidity"]
TOL = 1e-9


def recompute():
    shards = sorted(glob.glob(os.path.join(HERE, "eval_shards", f"{TAG}_*.npz")))
    if not shards:
        return None, 0, 0
    preds = {k: [] for k in KEYS}
    obs = {k: [] for k in KEYS}
    for f in shards:
        with np.load(f) as z:
            for k in KEYS:
                preds[k].append(z[f"{k}__pred"])
                obs[k].append(z[f"{k}__obs"])

    out = {}
    for k in KEYS:
        ens = np.concatenate(preds[k], axis=0)
        ob = np.concatenate(obs[k], axis=0)
        if k == "precipitation":
            # Same ceiling evaluate_csdi.py applies on write, so a pre-fix shard
            # set verifies identically to a post-fix one.
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
                t = f"{int(thr)}mm"
                r[f"brier_{t}"] = float(compute_brier_score(ens, ob, threshold=thr))
                r[f"pod_{t}"] = float(compute_pod(ens, ob, threshold=thr, prob_threshold=0.5))
                r[f"far_{t}"] = float(compute_far(ens, ob, threshold=thr, prob_threshold=0.5))
                r[f"csi_{t}"] = float(compute_csi(ens, ob, threshold=thr, prob_threshold=0.5))
        out[k] = r
    return out, len(shards), len(ob)


def same(a, b):
    """NaN == NaN counts as agreement; otherwise exact within TOL."""
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    if isinstance(a, float) and isinstance(b, float) and np.isnan(a) and np.isnan(b):
        return True
    return abs(float(a) - float(b)) <= TOL


def main():
    raw, n_shards, n_win = recompute()
    if raw is None:
        print("MISSING: no shards found -- nothing to verify")
        return 1

    print(f"shards present : {n_shards}/{TOTAL_SHARDS}")
    print(f"windows found  : {n_win} (expected {TOTAL_WINDOWS})")

    derived_path = os.path.join(HERE, "csdi_metrics.json")
    if not os.path.exists(derived_path):
        print("MISSING: csdi_metrics.json -- run evaluate_csdi.py first")
        return 1
    derived = json.load(open(derived_path))
    got_win = derived.get("test_windows")

    ok = True
    if n_win != TOTAL_WINDOWS:
        print(f"FAIL: partial run ({n_win}/{TOTAL_WINDOWS} windows) -- table would be incomplete")
        ok = False
    if got_win != n_win:
        print(f"FAIL: csdi_metrics.json says test_windows={got_win}, shards hold {n_win}")
        ok = False
    if derived.get("nsample") != 30 or derived.get("sampler") != "ddim":
        print(f"FAIL: derived run is M={derived.get('nsample')} sampler={derived.get('sampler')}")
        ok = False

    print(f"\n{'target':<20}{'metric':<14}{'from shards':>14}{'csdi_metrics':>15}  match")
    for k in KEYS:
        for m, v in raw[k].items():
            d = derived.get("metrics", {}).get(k, {}).get(m)
            good = same(v, d)
            ok = ok and good
            va = "nan" if (isinstance(v, float) and np.isnan(v)) else f"{v:.6f}"
            vd = "nan" if (d is None or (isinstance(d, float) and np.isnan(d))) else f"{float(d):.6f}"
            print(f"{k:<20}{m:<14}{va:>14}{vd:>15}  {'ok' if good else 'MISMATCH'}")

    print(f"\nVERDICT: {'TRACEABLE -- every table number is reproducible from the raw shards' if ok else 'NOT TRACEABLE -- see failures above'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
