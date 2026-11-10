#!/usr/bin/env python3
"""
Generate publication-quality comparison plots: RDM-STGNN vs CSDI vs Actual.

Features visualized:
1. Multi-variable time-series (Precipitation, Wind Speed, Relative Humidity)
   with stochastic ensemble uncertainty envelopes (P10 - P90).
2. Extreme Orographic Rain Event Zoom-in (Peak > 6.0 mm/h), illustrating
   why RDM-STGNN achieves superior POD and CSI for heavy precipitation.
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set clean scientific plotting style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.titlesize": 14,
    "lines.linewidth": 1.5,
})

from scripts.run_eval_final import load_test_data, run_diffusion_scenario

def main():
    print("[1/4] Loading CSDI baseline shards...")
    shards = sorted(glob.glob("csdi_baseline/eval_shards/*.npz"))[:10]  # First 320 hours
    assert len(shards) == 10, f"Expected 10 shards, found {len(shards)}"

    csdi_precip_ens = np.concatenate([np.load(s)["precipitation__pred"] for s in shards], axis=0) # [320, 30]
    csdi_precip_obs = np.concatenate([np.load(s)["precipitation__obs"] for s in shards], axis=0)  # [320]

    csdi_wind_ens = np.concatenate([np.load(s)["wind_speed__pred"] for s in shards], axis=0)     # [320, 30]
    csdi_wind_obs = np.concatenate([np.load(s)["wind_speed__obs"] for s in shards], axis=0)      # [320]

    csdi_rh_ens = np.concatenate([np.load(s)["relative_humidity__pred"] for s in shards], axis=0) # [320, 30]
    csdi_rh_obs = np.concatenate([np.load(s)["relative_humidity__obs"] for s in shards], axis=0)  # [320]

    N = len(csdi_precip_obs)
    print(f"Loaded {N} windows from CSDI.")

    print("[2/4] Generating RDM-STGNN (Skenario 3) predictions...")
    data_path = "data/raw/pangrango_era5_5node_2005_2025.parquet"
    ckpt_path = "results/canonical/tabel_3_17/sken_3_default_kontrol/model.pth"
    main_df, per_node_data, feature_cols, stats = load_test_data(data_path, ckpt_path)

    # Run inference for the exact matching 320 windows
    targets, preds, rdm_ens = run_diffusion_scenario(
        main_df, per_node_data, feature_cols, stats,
        eval_step=1, seq_len=6, num_ensemble=30, num_inference_steps=20,
        max_eval_samples=N, checkpoint=ckpt_path
    )

    # Verification: targets match
    assert np.allclose(csdi_precip_obs, targets[:, 0], atol=1e-4), "Obs mismatch!"

    # Compute percentiles
    rdm_p_med = np.median(rdm_ens[:, :, 0], axis=1)
    rdm_p_p10 = np.percentile(rdm_ens[:, :, 0], 10, axis=1)
    rdm_p_p90 = np.percentile(rdm_ens[:, :, 0], 90, axis=1)

    csdi_p_med = np.median(csdi_precip_ens, axis=1)
    csdi_p_p10 = np.percentile(csdi_precip_ens, 10, axis=1)
    csdi_p_p90 = np.percentile(csdi_precip_ens, 90, axis=1)

    rdm_w_med = np.median(rdm_ens[:, :, 1], axis=1)
    rdm_w_p10 = np.percentile(rdm_ens[:, :, 1], 10, axis=1)
    rdm_w_p90 = np.percentile(rdm_ens[:, :, 1], 90, axis=1)

    csdi_w_med = np.median(csdi_wind_ens, axis=1)
    csdi_w_p10 = np.percentile(csdi_wind_ens, 10, axis=1)
    csdi_w_p90 = np.percentile(csdi_wind_ens, 90, axis=1)

    rdm_rh_med = np.median(rdm_ens[:, :, 2], axis=1)
    rdm_rh_p10 = np.percentile(rdm_ens[:, :, 2], 10, axis=1)
    rdm_rh_p90 = np.percentile(rdm_ens[:, :, 2], 90, axis=1)

    csdi_rh_med = np.median(csdi_rh_ens, axis=1)
    csdi_rh_p10 = np.percentile(csdi_rh_ens, 10, axis=1)
    csdi_rh_p90 = np.percentile(csdi_rh_ens, 90, axis=1)

    # Dates
    dates = pd.to_datetime(main_df.loc[6: 6 + N - 1, "date"].values)

    print("[3/4] Creating comprehensive comparison figure...")
    fig = plt.figure(figsize=(15, 12), dpi=200)
    gs = fig.add_gridspec(4, 1, height_ratios=[1.2, 1.0, 1.0, 1.2], hspace=0.35)

    c_actual = "#111827"    # Dark charcoal
    c_rdm = "#f97316"       # Bright orange
    c_csdi = "#2563eb"      # Vibrant blue

    # --- Panel 1: Precipitation (Full 320h) ---
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(dates, csdi_precip_obs, color=c_actual, lw=1.8, label="Aktual (Ground Truth)", zorder=4)
    ax1.plot(dates, rdm_p_med, color=c_rdm, lw=1.5, label="RDM-STGNN (Median)", zorder=3)
    ax1.fill_between(dates, rdm_p_p10, rdm_p_p90, color=c_rdm, alpha=0.25, label="RDM-STGNN (P10-P90)")
    ax1.plot(dates, csdi_p_med, color=c_csdi, lw=1.5, linestyle="--", label="CSDI Baseline (Median)", zorder=2)
    ax1.fill_between(dates, csdi_p_p10, csdi_p_p90, color=c_csdi, alpha=0.20, label="CSDI (P10-P90)")
    ax1.set_ylabel("Presipitasi (mm/jam)")
    ax1.set_title("(a) Dinamika Curah Hujan Jam-jaman di Node MAIN (Puncak Pass, 1529 mdpl)", fontweight="bold")
    ax1.legend(loc="upper right", frameon=True, framealpha=0.9, ncol=3)
    ax1.set_ylim(-0.2, max(csdi_precip_obs.max() * 1.15, 7.0))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

    # --- Panel 2: Wind Speed ---
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax2.plot(dates, csdi_wind_obs, color=c_actual, lw=1.6, label="Aktual", zorder=4)
    ax2.plot(dates, rdm_w_med, color=c_rdm, lw=1.4, label="RDM-STGNN", zorder=3)
    ax2.fill_between(dates, rdm_w_p10, rdm_w_p90, color=c_rdm, alpha=0.22)
    ax2.plot(dates, csdi_w_med, color=c_csdi, lw=1.4, linestyle="--", label="CSDI", zorder=2)
    ax2.fill_between(dates, csdi_w_p10, csdi_w_p90, color=c_csdi, alpha=0.18)
    ax2.set_ylabel("Kecepatan Angin (m/s)")
    ax2.set_title("(b) Kecepatan Angin Permukaan (Wind Speed 10m)", fontweight="bold")
    ax2.legend(loc="upper right", frameon=True, framealpha=0.9, ncol=3)
    ax2.set_ylim(0, max(csdi_wind_obs.max() * 1.2, 5.0))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

    # --- Panel 3: Relative Humidity ---
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    ax3.plot(dates, csdi_rh_obs, color=c_actual, lw=1.6, label="Aktual", zorder=4)
    ax3.plot(dates, rdm_rh_med, color=c_rdm, lw=1.4, label="RDM-STGNN", zorder=3)
    ax3.fill_between(dates, rdm_rh_p10, rdm_rh_p90, color=c_rdm, alpha=0.22)
    ax3.plot(dates, csdi_rh_med, color=c_csdi, lw=1.4, linestyle="--", label="CSDI", zorder=2)
    ax3.fill_between(dates, csdi_rh_p10, csdi_rh_p90, color=c_csdi, alpha=0.18)
    ax3.set_ylabel("Kelembapan (%)")
    ax3.set_title("(c) Kelembapan Relatif (Relative Humidity 2m)", fontweight="bold")
    ax3.legend(loc="lower right", frameon=True, framealpha=0.9, ncol=3)
    ax3.set_ylim(60, 102)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))

    # --- Panel 4: Zoom-in Extreme Rain Event (Hours 210 to 260) ---
    z_start, z_end = 210, 260
    z_dates = dates[z_start:z_end]
    ax4 = fig.add_subplot(gs[3])
    ax4.plot(z_dates, csdi_precip_obs[z_start:z_end], color=c_actual, lw=2.2, marker="o", markersize=4, label="Aktual (Ground Truth)", zorder=4)
    ax4.plot(z_dates, rdm_p_med[z_start:z_end], color=c_rdm, lw=1.8, marker="s", markersize=4, label="RDM-STGNN (median)", zorder=3)
    ax4.fill_between(z_dates, rdm_p_p10[z_start:z_end], rdm_p_p90[z_start:z_end], color=c_rdm, alpha=0.25, label="RDM-STGNN P10-P90 Band")
    ax4.plot(z_dates, csdi_p_med[z_start:z_end], color=c_csdi, lw=1.8, linestyle="--", marker="^", markersize=4, label="CSDI (median)", zorder=2)
    ax4.fill_between(z_dates, csdi_p_p10[z_start:z_end], csdi_p_p90[z_start:z_end], color=c_csdi, alpha=0.20, label="CSDI P10-P90 Band")
    ax4.set_ylabel("Presipitasi (mm/jam)")
    ax4.set_xlabel("Waktu (UTC)", labelpad=8)
    ax4.set_title(f"(d) Zoom-In Episode Hujan Ekstrem Orografis ({z_dates[0]:%d %b %Y} – {z_dates[-1]:%d %b %Y})", fontweight="bold")
    ax4.legend(loc="upper left", frameon=True, framealpha=0.9, ncol=2)
    ax4.set_ylim(-0.2, max(csdi_precip_obs[z_start:z_end].max() * 1.35, 3.0))
    ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))

    # Annotate peak
    peak_idx = z_start + np.argmax(csdi_precip_obs[z_start:z_end])
    peak_val = csdi_precip_obs[peak_idx]
    peak_date = dates[peak_idx]
    ax4.annotate(
        f"Puncak hujan: {peak_val:.1f} mm/jam\nRDM: {rdm_p_med[peak_idx]:.1f} · CSDI: {csdi_p_med[peak_idx]:.1f}",
        xy=(peak_date, peak_val),
        xytext=(mdates.date2num(peak_date) + 0.35, 5.0),
        arrowprops=dict(facecolor="black", shrink=0.08, width=1, headwidth=5),
        fontsize=8.5,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#fef08a", edgecolor="#ca8a04", alpha=0.95),
    )

    out_paths = [
        "../docs/bukti_highlight/komparasi_prediksi_stgnn_csdi_aktual.png",
        "results/canonical/tabel_3_17/sken_3_default_kontrol/eval/plots/komparasi_csdi_vs_rdm_aktual.png"
    ]

    for p in out_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, bbox_inches="tight")
        print(f"Plot saved to: {p}")

    plt.close()
    print("[4/4] Done successfully!")

if __name__ == "__main__":
    main()
