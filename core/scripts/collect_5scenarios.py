"""
Susun Tabel 3.17 dari hasil 5 skenario (core/results/tabel_3_17/sken_*).

Aturan pemilihan model optimal mengikuti naskah hal. 69 (§3.8.2):
  "Model yang menghasilkan CRPS terendah, CSI >= 5 mm/jam tertinggi, dan
   latensi <= 2 detik dinobatkan sebagai RDM-STGNN Optimal."

Jalankan:  cd core && python scripts/collect_5scenarios.py
Output:    core/results/tabel_3_17/summary.json  + tabel markdown ke stdout
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.dirname(HERE)
ROOT = os.path.join(CORE, "results", "tabel_3_17")

# Skenario sesuai Tabel 3.17 naskah.
SCHEMES = [
    (1, "ultra_lightweight", 1e-3, 10, 5, 1, 10, 10, 0.3),
    (2, "moderate_fast", 1e-3, 20, 8, 2, 15, 20, 0.5),
    (3, "default_kontrol", 1e-3, 20, 12, 3, 20, 30, 0.7),
    (4, "fine_tuned", 5e-4, 35, 12, 4, 30, 40, 0.7),
    (5, "high_capacity", 1e-4, 50, 15, 5, 50, 50, 1.0),
]

LATENCY_LIMIT_S = 2.0
PRECIP = "precipitation"
TOLERANCE = 1e-6


def is_finite_num(val: any) -> bool:
    """True jika val adalah angka riil berhingga dan bukan NaN."""
    if val is None:
        return False
    try:
        f = float(val)
        return not math.isnan(f) and math.isfinite(f)
    except (TypeError, ValueError):
        return False


def parse_metric_value(val: any) -> float | None:
    """Parse nilai metrik; kembalikan float atau None jika tidak valid."""
    if val is None:
        return None
    try:
        f = float(val)
        return f
    except (TypeError, ValueError):
        return None


def sanitize_for_json(obj: any) -> any:
    """
    Konversi NaN / Inf menjadi None agar output json.dump sesuai standar RFC 8259
    dan tidak merusak parser JSON eksternal (JavaScript, dashboard web).
    """
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(v) for v in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or not math.isfinite(obj):
            return None
        return obj
    return obj


def load_run(run_dir: str):
    """
    Kembalikan (metrics_dict, latency_dict) atau (None, None).
    Mendukung skema baru, alias model, dan fallback jika format file berbeda.
    """
    m = None
    summ_path = os.path.join(run_dir, "eval", "comparison", "comparison_summary.json")
    full_metrics_path = os.path.join(run_dir, "eval", "full_model", "metrics.json")

    if os.path.exists(summ_path):
        try:
            with open(summ_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            res = data.get("results", {})
            if isinstance(res, dict):
                # Cari kunci model penuh
                for k in ("full_model", "RDM-STGNN", "rdm-stgnn", "rdm_stgnn", "optimal"):
                    if k in res:
                        m = res[k]
                        break
                if m is None and len(res) == 1:
                    m = next(iter(res.values()))
        except Exception:
            m = None

    # Fallback ke metrics.json di folder full_model jika belum ditemukan
    if m is None and os.path.exists(full_metrics_path):
        try:
            with open(full_metrics_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            m = data.get("metrics") or data.get("results")
        except Exception:
            m = None

    # Load latency
    lat = None
    latp = os.path.join(run_dir, "latency.json")
    if os.path.exists(latp):
        try:
            with open(latp, "r", encoding="utf-8") as f:
                lat = json.load(f)
        except Exception:
            lat = None

    # Fallback hitung latency_per_sample_s jika belum ada
    if lat and lat.get("latency_per_sample_s") is None:
        tot = lat.get("eval_total_seconds")
        n = lat.get("n_samples")
        if is_finite_num(tot) and is_finite_num(n) and float(n) > 0:
            lat["latency_per_sample_s"] = float(tot) / float(n)

    return m, lat


def extract_precip_metrics(m: dict) -> dict:
    """Ekstrak metrik presipitasi secara defensif terhadap variasi key."""
    if not isinstance(m, dict):
        return {"crps": None, "rmse": None, "csi_5mm": None}

    p = None
    for k in ("precipitation", "precip", "rain"):
        if k in m and isinstance(m[k], dict):
            p = m[k]
            break
    if p is None:
        p = m

    crps = None
    for k in ("crps", "CRPS"):
        if k in p:
            crps = parse_metric_value(p[k])
            break

    rmse = None
    for k in ("rmse", "RMSE"):
        if k in p:
            rmse = parse_metric_value(p[k])
            break

    csi_5mm = None
    for k in ("csi_5mm", "csi_5", "csi_5.0mm", "CSI_5mm"):
        if k in p:
            csi_5mm = parse_metric_value(p[k])
            break

    return {"crps": crps, "rmse": rmse, "csi_5mm": csi_5mm}


def csi_sort_key(r: dict) -> float:
    """CSI score key; NaN / None diberi penalti -1.0 agar tidak memenangkan tie-break."""
    c = r.get("csi_5mm")
    return float(c) if is_finite_num(c) else -1.0


def main():
    rows = []
    for (sid, label, lr, ep, pat, k, ddim, ens, aux) in SCHEMES:
        run_dir = os.path.join(ROOT, f"sken_{sid}_{label}")
        m, lat = load_run(run_dir)
        p_metrics = extract_precip_metrics(m)

        lat_val = (lat or {}).get("latency_per_sample_s")
        lat_clean = float(lat_val) if is_finite_num(lat_val) else None

        row = {
            "skenario": sid,
            "label": label,
            "lr": lr,
            "epochs": ep,
            "patience": pat,
            "k": k,
            "ddim": ddim,
            "ensemble": ens,
            "aux": aux,
            "status": "belum dijalankan" if m is None else "selesai",
            "crps_precip": p_metrics["crps"],
            "rmse_precip": p_metrics["rmse"],
            "csi_5mm": p_metrics["csi_5mm"],
            "latency_per_sample_s": lat_clean,
        }
        rows.append(row)

    done = [r for r in rows if r["status"] == "selesai"]

    # Filter kandidat yang memenuhi syarat:
    # 1. Latensi valid & <= 2.0 detik
    # 2. CRPS presipitasi valid & berhingga (bukan NaN / None / negatif)
    eligible = [
        r for r in done
        if is_finite_num(r["latency_per_sample_s"])
        and float(r["latency_per_sample_s"]) <= LATENCY_LIMIT_S
        and is_finite_num(r["crps_precip"])
        and float(r["crps_precip"]) >= 0.0
    ]

    all_done = len(done) == len(SCHEMES)
    optimal = None
    provisional_optimal = None

    if eligible:
        # 1. CRPS terendah
        best_crps = min(float(r["crps_precip"]) for r in eligible)
        near_crps = [r for r in eligible if abs(float(r["crps_precip"]) - best_crps) <= TOLERANCE]

        # 2. Tie-break: CSI >= 5 mm/jam tertinggi (NaN dipenalti ke -1.0)
        best_csi = max(csi_sort_key(r) for r in near_crps)
        tied_csi = [r for r in near_crps if abs(csi_sort_key(r) - best_csi) <= TOLERANCE]

        # 3. Tie-break lanjutan: latensi terendah, lalu ID skenario terkecil
        winner = min(tied_csi, key=lambda r: (float(r["latency_per_sample_s"]), r["skenario"]))
        provisional_optimal = winner["skenario"]

        if all_done:
            optimal = provisional_optimal

    out = {
        "schemes": sanitize_for_json(rows),
        "optimal_skenario": optimal,
        "provisional_optimal_skenario": provisional_optimal,
        "scenarios_complete": f"{len(done)}/{len(SCHEMES)}",
        "latency_limit_s": LATENCY_LIMIT_S,
        "selection_rule": "CRPS terendah, tie-break CSI>=5mm tertinggi, latensi <= 2s (tahan NaN)",
    }
    os.makedirs(ROOT, exist_ok=True)
    with open(os.path.join(ROOT, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)

    print("\n=== Tabel 3.17 — Skenario Penalaan Hiperparameter RDM-STGNN ===\n")
    hdr = ("SKEN", "lr", "ep(pat)", "k", "DDIM", "M", "aux",
           "CRPS precip", "CSI>=5mm", "latency/s", "status")
    print("| " + " | ".join(hdr) + " |")
    print("|" + "---|" * len(hdr))

    def fmt_num(v: any, p: int = 4) -> str:
        if v is None:
            return "—"
        if isinstance(v, (int, float)):
            if math.isnan(v):
                return "NaN"
            if math.isinf(v):
                return "Inf"
            return f"{v:.{p}f}"
        return str(v)

    for r in rows:
        print("| " + " | ".join([
            str(r["skenario"]),
            f"{r['lr']:.0e}", f"{r['epochs']}({r['patience']})",
            str(r["k"]), str(r["ddim"]), str(r["ensemble"]), f"{r['aux']}",
            fmt_num(r["crps_precip"]), fmt_num(r["csi_5mm"]),
            fmt_num(r["latency_per_sample_s"], 3), r["status"],
        ]) + " |")

    print()
    if optimal:
        print(f"RDM-STGNN Optimal (aturan naskah): SKENARIO {optimal}")
    elif not all_done:
        prov_msg = f" (kandidat sementara: SKENARIO {provisional_optimal})" if provisional_optimal else ""
        print(f"RDM-STGNN Optimal: BELUM FINAL — {len(done)}/{len(SCHEMES)} skenario selesai{prov_msg}. "
              "Penobatan resmi memerlukan seluruh skenario grid selesai.")
    else:
        print("RDM-STGNN Optimal: tidak ada skenario yang memenuhi syarat (latensi <= 2s dan metrik valid).")
    print(f"\nsummary.json: {os.path.join(ROOT, 'summary.json')}")


if __name__ == "__main__":
    main()