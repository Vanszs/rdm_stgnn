#!/usr/bin/env python3
"""Time-series evaluation over the FULL test split (35.058 jam): CSDI vs RDM-STGNN.

Rows: (a) presipitasi jam-jaman + rata-rata bergerak 7 hari,
      (b) bias rata-rata bergerak 7 hari (median model - aktual).
Run from core/: PYTHONPATH=. python scripts/plot_timeseries_full.py
"""
import glob
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scripts.run_eval_final import load_test_data, run_diffusion_scenario

DATA = "data/raw/pangrango_era5_5node_2005_2025.parquet"
CKPT = "results/tabel_3_17/sken_3_default_kontrol/model.pth"
ROLL = 24 * 7


def rolling_mean(a):
    return pd.Series(a).rolling(ROLL, min_periods=ROLL // 7, center=True).mean().to_numpy()


def main():
    shards = sorted(glob.glob("csdi_baseline/eval_shards/*.npz"))
    csdi_obs = np.concatenate([np.load(s)["precipitation__obs"] for s in shards])
    csdi_med = np.median(
        np.concatenate([np.load(s)["precipitation__pred"] for s in shards]), axis=1
    )

    main_df, per_node, feats, stats = load_test_data(DATA, CKPT)
    targets, _, ens = run_diffusion_scenario(
        main_df, per_node, feats, stats,
        eval_step=1, seq_len=6, num_ensemble=30, num_inference_steps=20,
    )

    obs = targets[:, 0]
    rdm_med = np.median(ens[:, :, 0], axis=1)
    N = len(obs)
    assert len(csdi_obs) == N, (len(csdi_obs), N)
    assert np.allclose(csdi_obs, obs, atol=1e-4), "obs CSDI != obs RDM"

    dates = pd.to_datetime(main_df.loc[6:6 + N - 1, "date"]).to_numpy()

    rmse = lambda p: float(np.sqrt(np.mean((p - obs) ** 2)))
    print(f"N={N}  CSDI RMSE={rmse(csdi_med):.4f}  RDM RMSE={rmse(rdm_med):.4f}")

    fig, axes = plt.subplots(
        2, 1, figsize=(16, 9), dpi=170, sharex=True,
        gridspec_kw={"height_ratios": [2, 1]},
    )

    ax = axes[0]
    ax.plot(dates, obs, color="#9ca3af", lw=0.4, alpha=0.55, label="Aktual (jam-jaman)")
    ax.plot(dates, csdi_med, color="#2563eb", lw=0.4, alpha=0.40, label="CSDI (median)")
    ax.plot(dates, rdm_med, color="#f97316", lw=0.4, alpha=0.40, label="RDM-STGNN (median)")
    ax.plot(dates, rolling_mean(obs), color="#111827", lw=1.8, label="Aktual (rata-rata 7 hari)")
    ax.plot(dates, rolling_mean(csdi_med), color="#2563eb", lw=2.0, label="CSDI (rata-rata 7 hari)")
    ax.plot(dates, rolling_mean(rdm_med), color="#f97316", lw=2.0, label="RDM-STGNN (rata-rata 7 hari)")
    ax.set_ylabel("Presipitasi (mm/jam)")
    ax.set_title(
        f"Evaluasi time-series seluruh split uji ({N:,} jam): CSDI vs RDM-STGNN".replace(",", "."),
        fontweight="bold",
    )
    ax.grid(alpha=0.25)
    ax.legend(ncol=3, fontsize=8, framealpha=0.9)

    ax2 = axes[1]
    ax2.axhline(0, color="#111827", lw=0.9)
    ax2.plot(dates, rolling_mean(csdi_med - obs), color="#2563eb", lw=1.6,
             label="Bias CSDI (median − aktual)")
    ax2.plot(dates, rolling_mean(rdm_med - obs), color="#f97316", lw=1.6,
             label="Bias RDM-STGNN (median − aktual)")
    ax2.set_ylabel(f"Bias {ROLL // 24} hari (mm/jam)")
    ax2.set_xlabel("Waktu (UTC)")
    ax2.grid(alpha=0.25)
    ax2.legend(fontsize=8, framealpha=0.9)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    for path in [
        "../docs/bukti_highlight/timeseries_penuh_csdi_vs_rdm.png",
        "results/tabel_3_17/sken_3_default_kontrol/eval/plots/timeseries_penuh_csdi_vs_rdm.png",
    ]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fig.savefig(path, bbox_inches="tight")
        print("saved", path)


if __name__ == "__main__":
    main()
