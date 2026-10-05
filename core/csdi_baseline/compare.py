"""
Merge CSDI and RDM-STGNN metrics into the thesis Tabel 3.18 layout.

Inputs:
  core/csdi_baseline/csdi_metrics.json      (produced by evaluate_csdi.py)
  core/csdi_baseline/rdm_stgnn_metrics.json (extracted from the RDM-STGNN run)

Output:
  core/csdi_baseline/tabel_3_18.json  (+ a markdown table printed to stdout)

Run:  cd core/csdi_baseline && python compare.py
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CSDI = os.path.join(HERE, "csdi_metrics.json")
RDM = os.path.join(HERE, "rdm_stgnn_metrics.json")
OUT = os.path.join(HERE, "tabel_3_18.json")

TARGETS = ["precipitation", "wind_speed", "relative_humidity"]
BASE = ["rmse", "mae", "correlation", "crps"]
THRESH = ["2mm", "5mm", "10mm"]



def _check_alignment(csdi, rdm):
    """Refuse an apples-to-oranges comparison.

    Both models must be scored on the same test windows, otherwise the pairwise
    differences in Tabel 3.18 are not attributable to the models.
    """
    n_csdi = csdi.get("test_windows")
    n_rdm = (rdm.get("metadata") or {}).get("samples_per_scenario")
    ok = n_csdi == n_rdm
    print(f"ALIGNMENT  CSDI windows={n_csdi}  RDM-STGNN samples={n_rdm}  -> "
          f"{'OK' if ok else 'MISMATCH'}")
    if not ok:
        print("           WARNING: the two models were scored on different test sets.")
        print("           Re-run RDM-STGNN with --eval-step 1 before quoting this table.")
        if rdm.get("caveat"):
            print(f"           RDM caveat: {rdm['caveat']}")
    return ok

def rows_for(m: dict, target: str):
    """Build the thesis metric rows for one target from one model's metrics."""
    v = m["metrics"].get(target, {})
    out = {}
    for k in BASE:
        out[k] = v.get(k)
    if target == "precipitation":
        for t in THRESH:
            for mk in ("brier", "pod", "far", "csi"):
                out[f"{mk}_{t}"] = v.get(f"{mk}_{t}")
    return out


def fmt(x):
    if x is None:
        return "—"
    if isinstance(x, float):
        return "nan" if x != x else f"{x:.4f}"
    return str(x)


def main():
    csdi = json.load(open(CSDI))
    rdm = json.load(open(RDM))
    aligned = _check_alignment(csdi, rdm)
    n_rdm = (rdm.get("metadata") or {}).get("samples_per_scenario")
    final = aligned and csdi.get("nsample") == 30 and csdi.get("sampler") == "ddim"

    table = {}
    for target in TARGETS:
        a = rows_for(csdi, target)
        b = rows_for(rdm, target)
        keys = list(dict.fromkeys(list(a.keys()) + list(b.keys())))
        table[target] = {k: {"CSDI": a.get(k), "RDM-STGNN": b.get(k)} for k in keys}

    json.dump(
        {"aligned_test_set": aligned,
         "csdi_meta": {k: csdi.get(k) for k in ("nsample", "test_windows",
                                                "checkpoint_epoch", "checkpoint_best_val")},
         "rdm_meta": rdm.get("metadata"),
         "rdm_caveat": rdm.get("caveat"),
         "table": table},
        open(OUT, "w"), indent=2,
    )

    labels = {
        "rmse": "RMSE", "mae": "MAE", "correlation": "Korelasi Pearson (r)",
        "crps": "CRPS",
    }
    for t in THRESH:
        labels[f"brier_{t}"] = f"Brier Score (ambang {t})"
        labels[f"pod_{t}"] = f"POD (ambang {t})"
        labels[f"far_{t}"] = f"FAR (ambang {t})"
        labels[f"csi_{t}"] = f"CSI (ambang {t})"

    for target in TARGETS:
        print(f"\n### {target.upper()}")
        print(f"| Metrik | CSDI | RDM-STGNN |")
        print("|---|---:|---:|")
        for k, pair in table[target].items():
            print(f"| {labels.get(k, k)} | {fmt(pair['CSDI'])} | {fmt(pair['RDM-STGNN'])} |")

    # Inject the rendered tables into the report so no manual copy-paste is needed.
    doc = os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "CSDI_COMPARISON.md")
    START, END = "<!-- TABEL_3_18_START -->", "<!-- TABEL_3_18_END -->"
    if os.path.exists(doc):
        md_lines = []
        for target in TARGETS:
            md_lines.append(f"\n### {target.replace('_', ' ').title()}\n")
            md_lines.append("| Metrik | CSDI | RDM-STGNN |")
            md_lines.append("|---|---:|---:|")
            for k, pair in table[target].items():
                md_lines.append(f"| {labels.get(k, k)} | {fmt(pair['CSDI'])} | {fmt(pair['RDM-STGNN'])} |")
        block = (
            f"\n> **Status tabel: {'FINAL' if final else 'PROVISIONAL — jangan dikutip'}.** "
            f"CSDI {csdi.get('test_windows')} window (M={csdi.get('nsample')}, "
            f"{csdi.get('sampler')}); RDM-STGNN {n_rdm} window (eval_step "
            f"{(rdm.get('metadata') or {}).get('eval_step')}).\n\n"
            + "\n".join(md_lines)
            + f"\n\n_aligned_test_set: {aligned}_\n"
            + f"_source CSDI: checkpoint epoch {csdi.get('checkpoint_epoch')}, "
              f"sampler {csdi.get('sampler')}, M={csdi.get('nsample')}, "
              f"windows={csdi.get('test_windows')}_\n"
            + (f"_source RDM-STGNN: {rdm['caveat']}_\n" if rdm.get("caveat")
               else f"_source RDM-STGNN: {rdm.get('source')} (eval_step "
                    f"{rdm.get('metadata', {}).get('eval_step')})_\n")
        )
        src = open(doc).read()
        if START in src and END in src:
            pre = src.split(START)[0]
            post = src.split(END)[1]
            open(doc, "w").write(pre + START + block + END + post)
            print(f"injected into {doc}")

    print(f"\nwritten: {OUT}")
    if rdm.get("caveat"):
        print(f"\nWARNING (RDM-STGNN side): {rdm['caveat']}")


if __name__ == "__main__":
    main()