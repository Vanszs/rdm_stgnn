"""
Regenerate core/csdi_baseline/rdm_stgnn_metrics.json from a RDM-STGNN eval run.

The comparison in Tabel 3.18 must compare models scored on the SAME test set, so
this reads whatever run produced that set and records the provenance alongside
the numbers. Point it at the current-code run:

    cd core/csdi_baseline
    python make_rdm_metrics.py --summary ../results/archive/2026-11-03_pra_retrain/current_code_eval/comparison/comparison_summary.json

Legacy key names from older runs (wind_speed/humidity) are mapped to the thesis
contract (wind_speed_10m / relative_humidity_2m) on the way in.
"""
from __future__ import annotations

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "rdm_stgnn_metrics.json")

# Older RDM-STGNN runs used short target names.
KEYMAP = {"wind_speed": "wind_speed", "humidity": "relative_humidity"}
SCENARIO = "full_model"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True, help="path to comparison_summary.json")
    ap.add_argument("--scenario", default=SCENARIO)
    args = ap.parse_args()

    src = os.path.abspath(args.summary)
    data = json.load(open(src))
    meta = data.get("metadata", {})
    runs = data.get("results", {})

    if args.scenario not in runs:
        raise SystemExit(
            f"scenario '{args.scenario}' not in {src}; available: {sorted(runs)}"
        )

    metrics = {KEYMAP.get(k, k): v for k, v in runs[args.scenario].items()}

    out = {
        "model": "RDM-STGNN",
        "source": os.path.relpath(src, os.path.dirname(HERE)),
        "scenario": args.scenario,
        "metadata": {
            "samples_per_scenario": meta.get("samples_per_scenario"),
            "num_ensemble": meta.get("num_ensemble"),
            "eval_step": meta.get("eval_step"),
            "seed": meta.get("seed"),
            "crps": meta.get("crps_estimator"),
            "rain_probability_threshold": meta.get("rain_probability_threshold"),
        },
        "metrics": metrics,
    }

    # Flag any mismatch against the thesis evaluation protocol (Sec 3.9.1: eval_step=1).
    if meta.get("eval_step") != 1:
        out["caveat"] = (
            f"eval_step={meta.get('eval_step')} — the thesis requires eval_step=1 "
            "(no test timestamp skipped); this run subsamples."
        )
    json.dump(out, open(OUT, "w"), indent=2)

    print(f"written: {OUT}")
    print(f"  source    : {out['source']}")
    print(f"  samples   : {out['metadata']['samples_per_scenario']}")
    print(f"  eval_step : {out['metadata']['eval_step']}")
    for t, v in metrics.items():
        print(f"  {t:18} rmse={v.get('rmse'):.4f} crps={v.get('crps'):.4f}")
    if out.get("caveat"):
        print(f"  CAVEAT: {out['caveat']}")


if __name__ == "__main__":
    main()