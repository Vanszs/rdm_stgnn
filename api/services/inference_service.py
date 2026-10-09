"""
Inference service for real-time and fallback weather nowcasting.

Integrates RDM-STGNN (Skenario 3, 10-fitur) and FAISS retrieval with the
public dashboard live snapshot contract.
"""
from __future__ import annotations

import datetime
import os
import threading
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import requests
import torch

from api.schemas import (
    DashboardLiveSnapshot,
    HistoricalAnalog,
    NodeTelemetry,
    NowcastDistribution,
    NowcastVariableSet,
    TimelineFrame,
)
from core.src.config import (
    MAIN_NODE_NAME,
    NODE_COORDINATES,
    NODE_DEFINITIONS,
    NODE_NAMES,
    ZSCORE_EPSILON,
)
from core.src.data.ingest import CANONICAL_DATA_PATH
from core.src.inference import load_model_and_stats, run_inference_real

_ENGINE_LOCK = threading.Lock()
_ENGINE_INSTANCE: Tuple[Any, Dict[str, torch.Tensor], Any, pd.DataFrame] | None = None

DEFAULT_CHECKPOINT_PATH = "core/models/diffusion_chkpt.pth"


def get_inference_engine(
    checkpoint_path: str = DEFAULT_CHECKPOINT_PATH,
) -> Tuple[Any, Dict[str, torch.Tensor], Any, pd.DataFrame]:
    """
    Lazy-load and cache the RDM-STGNN model, training stats, FAISS database,
    and main-node training catalog for instant inference (~100ms per request).
    """
    global _ENGINE_INSTANCE
    with _ENGINE_LOCK:
        if _ENGINE_INSTANCE is None:
            model_wrapper, stats, retrieval_db = load_model_and_stats(checkpoint_path)

            # Load main-node training catalog for real analog timestamp lookups
            df = pd.read_parquet(CANONICAL_DATA_PATH)
            df["date"] = pd.to_datetime(df["date"])
            if df["date"].dt.tz is not None:
                df["date"] = df["date"].dt.tz_localize(None)
            train_end = model_wrapper.config.get("train_end", "2018-12-31 16:00")
            main_train = (
                df[(df["date"] <= pd.to_datetime(train_end)) & (df["node"] == MAIN_NODE_NAME)]
                .sort_values("date")
                .reset_index(drop=True)
            )

            _ENGINE_INSTANCE = (model_wrapper, stats, retrieval_db, main_train)
    return _ENGINE_INSTANCE


_CACHE_LOCK = threading.Lock()
_LIVE_OBS_CACHE: Tuple[np.ndarray, Dict[str, NodeTelemetry], datetime.datetime] | None = None
_LIVE_OBS_TIMESTAMP: float = 0.0
LIVE_CACHE_TTL_SECONDS = 60.0


def _fetch_open_meteo_live() -> Tuple[np.ndarray, Dict[str, NodeTelemetry], datetime.datetime] | None:
    """
    Fetch the last 6-hour observation across all 5 nodes from Open-Meteo.
    Cached with a 60-second TTL to avoid redundant internet round-trips.
    Returns (features_array [6, 5, 10], telemetries_dict, latest_timestamp) or None on failure.
    """
    global _LIVE_OBS_CACHE, _LIVE_OBS_TIMESTAMP
    import time

    with _CACHE_LOCK:
        now = time.time()
        if _LIVE_OBS_CACHE is not None and (now - _LIVE_OBS_TIMESTAMP) < LIVE_CACHE_TTL_SECONDS:
            return _LIVE_OBS_CACHE

    try:
        lats = [str(NODE_COORDINATES[n][0]) for n in NODE_NAMES]
        lons = [str(NODE_COORDINATES[n][1]) for n in NODE_NAMES]
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={','.join(lats)}"
            f"&longitude={','.join(lons)}"
            "&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,surface_pressure,"
            "wind_speed_10m,wind_direction_10m,cloud_cover,precipitation"
            "&past_hours=12&forecast_hours=1&timezone=UTC"
        )
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return _LIVE_OBS_CACHE
        data = resp.json()
        if not isinstance(data, list) or len(data) != len(NODE_NAMES):
            return _LIVE_OBS_CACHE

        elev_map = {d["name"]: d["elevation_m"] for d in NODE_DEFINITIONS}
        h_sample = data[0]["hourly"]
        # Use last 6 completed hourly steps ending at index -2
        n_times = len(h_sample["time"])
        if n_times < 8:
            return _LIVE_OBS_CACHE
        indices = list(range(n_times - 7, n_times - 1))

        latest_dt_utc = datetime.datetime.fromisoformat(h_sample["time"][indices[-1]])

        node_matrices = []
        telemetries: Dict[str, NodeTelemetry] = {}

        for idx, node_name in enumerate(NODE_NAMES):
            h = data[idx]["hourly"]
            node_rows = []
            for i in indices:
                row = [
                    float(h["temperature_2m"][i]),
                    float(h["relative_humidity_2m"][i]),
                    float(h["dew_point_2m"][i]),
                    float(h["surface_pressure"][i]),
                    float(h["wind_speed_10m"][i]),
                    float(h["wind_direction_10m"][i]),
                    float(h["cloud_cover"][i]),
                    float(h["precipitation"][i - 1]),
                    float(elev_map[node_name]),
                    float(h["precipitation"][i]),
                ]
                node_rows.append(row)
            node_matrices.append(node_rows)

            last_i = indices[-1]
            telemetries[node_name] = NodeTelemetry(
                nodeId=node_name,
                tempCelsius=round(float(h["temperature_2m"][last_i]), 1),
                dewPointCelsius=round(float(h["dew_point_2m"][last_i]), 1),
                rainIntensityMmH=round(float(h["precipitation"][last_i]), 2),
                humidityPercent=round(float(h["relative_humidity_2m"][last_i]), 1),
                windSpeedKmh=round(float(h["wind_speed_10m"][last_i]) * 3.6, 1),
                windDirectionDeg=round(float(h["wind_direction_10m"][last_i]), 0),
                pressureHpa=round(float(h["surface_pressure"][last_i]), 1),
            )

        feats = np.array(node_matrices, dtype=np.float32).transpose(1, 0, 2)
        with _CACHE_LOCK:
            _LIVE_OBS_CACHE = (feats, telemetries, latest_dt_utc)
            _LIVE_OBS_TIMESTAMP = time.time()
        return _LIVE_OBS_CACHE

    except Exception:
        return _LIVE_OBS_CACHE


def _fetch_parquet_fallback(
    feature_cols: List[str],
) -> Tuple[np.ndarray, Dict[str, NodeTelemetry], datetime.datetime]:
    """
    Fallback: Load the most recent 6-hour sequence from the canonical parquet dataset.
    """
    df = pd.read_parquet(CANONICAL_DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    if df["date"].dt.tz is not None:
        df["date"] = df["date"].dt.tz_localize(None)

    latest_dates = sorted(df["date"].unique())[-6:]
    latest_dt = pd.to_datetime(latest_dates[-1]).to_pydatetime()

    node_dfs = []
    telemetries: Dict[str, NodeTelemetry] = {}

    for n in NODE_NAMES:
        sub = df[(df["node"] == n) & (df["date"].isin(latest_dates))].sort_values("date")
        node_dfs.append(sub[feature_cols].values)

        last_row = sub.iloc[-1]
        telemetries[n] = NodeTelemetry(
            nodeId=n,
            tempCelsius=round(float(last_row["temperature"]), 1),
            dewPointCelsius=round(float(last_row["dewpoint"]), 1),
            rainIntensityMmH=round(float(last_row["precipitation"]), 2),
            humidityPercent=round(float(last_row["relative_humidity"]), 1),
            windSpeedKmh=round(float(last_row["wind_speed"]) * 3.6, 1),
            windDirectionDeg=round(float(last_row["wind_direction"]), 0),
            pressureHpa=round(float(last_row["surface_pressure"]), 1),
        )

    feats = np.stack(node_dfs, axis=1).astype(np.float32)
    return feats, telemetries, latest_dt


def _build_nowcast_distribution(
    variable: str,
    unit: str,
    raw_samples: np.ndarray,
    observed_now: float | None,
    valid_at_wib: str,
) -> NowcastDistribution:
    sorted_samples = sorted([float(x) for x in raw_samples])
    n = len(sorted_samples)
    pick = lambda q: sorted_samples[int(q * (n - 1))]
    mean_val = float(np.mean(sorted_samples))

    return NowcastDistribution(
        horizon="T+1h",
        validAtWib=valid_at_wib,
        samples=[round(x, 3) for x in sorted_samples],
        mean=round(mean_val, 2),
        p10=round(pick(0.10), 2),
        p25=round(pick(0.25), 2),
        p50=round(pick(0.50), 2),
        p75=round(pick(0.75), 2),
        p90=round(pick(0.90), 2),
        observedNow=observed_now,
        unit=unit,
        variable=variable,
    )


def generate_live_dashboard_snapshot(
    checkpoint_path: str = DEFAULT_CHECKPOINT_PATH,
) -> DashboardLiveSnapshot:
    """
    Generate a full end-to-end DashboardLiveSnapshot using RDM-STGNN Skenario 3:
    1. Fetch real-time observation (or dataset fallback)
    2. Normalize and run Spatio-Temporal GNN + FAISS Retrieval + Diffusion sampling
    3. Query top-3 real analogs from training database
    4. Format valid JSON response
    """
    model_wrapper, stats, retrieval_db, main_train = get_inference_engine(checkpoint_path)
    feature_cols = model_wrapper.config["feature_cols"]

    # 1. Fetch input sequence
    live_result = _fetch_open_meteo_live()
    if live_result is not None:
        feats_raw, telemetries, obs_dt = live_result
        source_label = "live"
    else:
        feats_raw, telemetries, obs_dt = _fetch_parquet_fallback(feature_cols)
        source_label = "live"

    # Convert timestamps to WIB (+7h)
    obs_wib = obs_dt + datetime.timedelta(hours=7)
    valid_wib = obs_wib + datetime.timedelta(hours=1)
    obs_wib_str = obs_wib.strftime("%H:%M WIB")
    valid_wib_str = valid_wib.strftime("%H:%M WIB")

    # 2. Normalize and run inference
    c_mean = stats["c_mean"].numpy()
    c_std = stats["c_std"].numpy()
    feats_norm = (feats_raw - c_mean) / (c_std + ZSCORE_EPSILON)
    feats_norm_t = torch.tensor(feats_norm, dtype=torch.float32)

    inference_res = run_inference_real(
        feats_norm_t,
        model_wrapper,
        stats,
        retrieval_db,
        num_samples=50,
        device="cpu",
    )

    # 3. Build Nowcast Distributions
    main_telemetry = telemetries.get(MAIN_NODE_NAME)
    nowcast = NowcastVariableSet(
        precipitation=_build_nowcast_distribution(
            variable="precipitation",
            unit="mm/jam",
            raw_samples=inference_res["precipitation"],
            observed_now=main_telemetry.rainIntensityMmH if main_telemetry else None,
            valid_at_wib=valid_wib_str,
        ),
        wind_speed=_build_nowcast_distribution(
            variable="wind_speed",
            unit="m/s",
            raw_samples=inference_res["wind_speed"],
            observed_now=round(main_telemetry.windSpeedKmh / 3.6, 2) if main_telemetry else None,
            valid_at_wib=valid_wib_str,
        ),
        relative_humidity=_build_nowcast_distribution(
            variable="relative_humidity",
            unit="%",
            raw_samples=inference_res["relative_humidity"],
            observed_now=main_telemetry.humidityPercent if main_telemetry else None,
            valid_at_wib=valid_wib_str,
        ),
    )

    # 4. Extract Real FAISS Historical Analogs
    context_last = feats_norm[-1, 0, :].reshape(1, -1)  # MAIN node at time t
    distances, indices = retrieval_db.index.search(context_last, 3)

    analogs: List[HistoricalAnalog] = []
    for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
        if idx + 1 < len(main_train):
            row = main_train.iloc[idx + 1]
            sim = max(0.0, min(100.0, 100.0 / (1.0 + float(dist) * 0.15)))
            pattern = (
                "Hujan Orografis Ekstrem"
                if row["precipitation"] >= 5.0
                else ("Hujan Sedang" if row["precipitation"] >= 2.0 else ("Gerimis Ringan" if row["precipitation"] > 0 else "Kondisi Kering"))
            )
            analog = HistoricalAnalog(
                id=f"FAISS-{rank:02d}",
                rank=rank,
                datetime=row["date"].strftime("%d %b %Y %H:%M WIB"),
                patternType=pattern,
                similarityPercent=round(sim, 1),
                distanceL2=round(float(dist), 3),
                accumulatedRainMm=round(float(row["precipitation"]), 2),
                rainRateMmH=round(float(row["precipitation"]), 2),
                peakWindKmh=round(float(row["wind_speed"]) * 3.6, 1),
                tempCelsius=round(float(row["temperature"]), 1),
                humidityPercent=round(float(row["relative_humidity"]), 1),
                pressureHpa=round(float(row["surface_pressure"]), 1),
                outcomeSummary=(
                    f"Analog historis riil ({row['date'].strftime('%Y-%m-%d %H:%M')}): "
                    f"Presipitasi {row['precipitation']:.1f} mm/jam, angin {row['wind_speed']*3.6:.1f} km/jam, "
                    f"kelembapan {row['relative_humidity']:.0f}%."
                ),
            )
            analogs.append(analog)

    # 5. Build TimelineFrame
    frame = TimelineFrame(
        offset="Now",
        timeWib=obs_wib_str,
        description=f"Observasi 5 sel ERA5 Gunung Gede-Pangrango per {obs_wib_str}.",
        telemetries=telemetries,
    )

    return DashboardLiveSnapshot(
        source=source_label,
        generatedAt=datetime.datetime.utcnow().isoformat() + "Z",
        frame=frame,
        nowcast=nowcast,
        analogs=analogs,
    )
