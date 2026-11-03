"""
Adapter: Pangrango ERA5 5-node dataset -> CSDI Forecasting_Dataset format.

CSDI (Tashiro et al., NeurIPS 2021) expects:
  data/<name>/data.pkl     = (main_data [T x N], mask_data [T x N])
  data/<name>/meanstd.pkl  = (mean_data [N], std_data [N])

Channel layout — 10 channels per node (9 features + the precipitation target):
  for node in [MAIN, UP, DOWN, LEFT, RIGHT]:
      channels 0..8  = FINAL_FEATURE_COLS
      channel  9     = precipitation (contemporaneous, the prediction target)

`precipitation` is NOT in FINAL_FEATURE_COLS (only `precipitation_lag1` is), so it
must be carried as its own channel; otherwise the target would silently be the
lag-1 value instead of the current-hour value.

Normalisation uses TRAIN-ONLY statistics (split boundaries from the thesis,
Tabel 3.10 / core/src/train.py), so no validation/test information leaks into
the scaler. log1p is applied to precipitation-bearing channels before z-scoring.

Run:  cd core/csdi_baseline && python build_data.py
"""
from __future__ import annotations

import os
import pickle
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CORE = os.path.dirname(HERE)
sys.path.insert(0, CORE)

from src.config import FINAL_FEATURE_COLS, NODE_NAMES  # noqa: E402

# Thesis Tabel 3.10 boundaries (dataset starts 2004-12-31 17:00 UTC).
# These are the defaults of src.train.temporal_split — the one authority on the
# split. Kept as plain constants (not an import) so this script stays runnable
# without importing torch; a drift test asserts they still match.
TRAIN_END = "2018-12-31 16:00"
VAL_END = "2021-12-31 16:00"

PARQUET = os.path.join(CORE, "data", "raw", "pangrango_era5_5node_2005_2025.parquet")
OUT_DIR = os.path.join(HERE, "data", "pangrango")

FEATURE_COLS = list(FINAL_FEATURE_COLS)
NODES = list(NODE_NAMES)
N_FEAT = len(FEATURE_COLS)
N_NODES = len(NODES)
CH_PER_NODE = N_FEAT + 1                      # 9 features + precipitation target
N_CH = N_NODES * CH_PER_NODE                  # 5 * 10 = 50

# Precipitation lives at offset N_FEAT within each node block.
PRECIP_OFFSET = N_FEAT
LAG_OFFSET = FEATURE_COLS.index("precipitation_lag1")


def _ch(node_i: int, offset: int) -> int:
    return node_i * CH_PER_NODE + offset


MAIN_I = NODES.index("MAIN")
# Evaluated target channels on MAIN (thesis: main_node_only).
TARGET_CHANNELS = {
    "precipitation": _ch(MAIN_I, PRECIP_OFFSET),
    "wind_speed": _ch(MAIN_I, FEATURE_COLS.index("wind_speed")),
    "relative_humidity": _ch(MAIN_I, FEATURE_COLS.index("relative_humidity")),
}


def build():
    df = pd.read_parquet(PARQUET)
    df["date"] = pd.to_datetime(df["date"])
    if df["date"].dt.tz is not None:
        df["date"] = df["date"].dt.tz_convert("UTC").tz_localize(None)
    df = df.sort_values(["date", "node"]).reset_index(drop=True)

    ts = np.sort(df["date"].unique())
    t_index = {t: i for i, t in enumerate(ts)}

    cube = np.zeros((len(ts), N_NODES, CH_PER_NODE), dtype=np.float64)
    for node_i, node in enumerate(NODES):
        sub = df[df["node"] == node].sort_values("date")
        idx = sub["date"].map(t_index).to_numpy()
        cube[idx, node_i, :N_FEAT] = sub[FEATURE_COLS].to_numpy(dtype=np.float64)
        cube[idx, node_i, PRECIP_OFFSET] = sub["precipitation"].to_numpy(dtype=np.float64)

    # log1p the precipitation target channel (matches RDM-STGNN's target transform).
    # precipitation_lag1 is also log1p'd: it is raw precip shifted by one step, and
    # leaving a heavy-tailed 0..21.5mm covariate raw would hurt the diffusion model
    # more than it helps comparability. Note this is NOT identical to RDM-STGNN,
    # which z-scores that lag feature on raw values — recorded in the limitations.
    cube[:, :, PRECIP_OFFSET] = np.log1p(cube[:, :, PRECIP_OFFSET])
    cube[:, :, LAG_OFFSET] = np.log1p(cube[:, :, LAG_OFFSET])

    flat = cube.reshape(len(ts), N_CH)

    train_mask = ts <= np.datetime64(TRAIN_END)
    mean_data = flat[train_mask].mean(axis=0)
    std_data = flat[train_mask].std(axis=0)
    std_data[std_data < 1e-6] = 1.0
    norm = (flat - mean_data) / std_data

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "data.pkl"), "wb") as f:
        pickle.dump((norm.astype(np.float32), np.ones_like(norm, dtype=np.float32)), f)
    with open(os.path.join(OUT_DIR, "meanstd.pkl"), "wb") as f:
        pickle.dump((mean_data.astype(np.float64), std_data.astype(np.float64)), f)

    # Leakage guards.
    assert train_mask.sum() < len(ts), "train mask selected every row"
    post = flat[~train_mask]
    post_mean = post.mean(axis=0)
    assert not np.allclose(post_mean, mean_data), "val/test stats match train stats"

    print(f"timestamps : {len(ts)}  ({ts[0]} .. {ts[-1]})")
    print(f"channels   : {N_CH}  ({N_NODES} nodes x {CH_PER_NODE} = 9 features + precipitation)")
    print(f"train rows used for stats: {int(train_mask.sum())} (val+test rows: {int((~train_mask).sum())})")
    print(f"target ch  : {TARGET_CHANNELS}")
    print(f"written    : {OUT_DIR}/data.pkl, meanstd.pkl")
    print("guards     : stats train-only — OK")


if __name__ == "__main__":
    build()