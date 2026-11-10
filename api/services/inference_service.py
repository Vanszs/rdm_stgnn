"""
Inference service for ERA5 H-7 archive nowcasting with dataset fallback.

Integrates RDM-STGNN (Skenario 3, 10-fitur) and FAISS retrieval with the
public dashboard snapshot contract.
"""
from __future__ import annotations

import datetime
import logging
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
    FINAL_FEATURE_COLS,
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
CANDIDATE_FEATURE_COLS = list(FINAL_FEATURE_COLS) + ["precipitation"]


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
            model_wrapper, stats, retrieval_db, main_train = load_model_and_stats(checkpoint_path)
            checkpoint_features = list(model_wrapper.config.get("feature_cols", []))
            if checkpoint_features != CANDIDATE_FEATURE_COLS:
                raise RuntimeError(
                    "Checkpoint feature_cols tidak cocok dengan urutan fitur API: "
                    f"{checkpoint_features}"
                )
            _ENGINE_INSTANCE = (model_wrapper, stats, retrieval_db, main_train)
    return _ENGINE_INSTANCE


ANALOG_MIN_GAP_HOURS = 24
_ANALOG_THRESHOLD: float | None = None


def _analog_distance_threshold(retrieval_db: Any, sample_size: int = 512, quantile: float = 95.0) -> float:
    """p95 nearest-other-key L2 distance. Analogs beyond it are not 'similar' at all."""
    global _ANALOG_THRESHOLD
    if _ANALOG_THRESHOLD is None:
        index = retrieval_db.index
        if index is None or index.ntotal < 3:
            _ANALOG_THRESHOLD = float("inf")
        else:
            rng = np.random.default_rng(0)
            ids = rng.choice(index.ntotal, size=min(sample_size, index.ntotal), replace=False)
            probe = np.ascontiguousarray(index.reconstruct_batch(ids), dtype=np.float32)
            dists, _ = index.search(probe, 2)
            _ANALOG_THRESHOLD = float(np.percentile(dists[:, 1], quantile))
    return _ANALOG_THRESHOLD


def _select_analogs(index: Any, main_train: pd.DataFrame, context: np.ndarray, *, k: int,
                    max_distance: float, min_gap_hours: int = ANALOG_MIN_GAP_HOURS,
                    extra: int = 8) -> List[Tuple[int, float, bool]]:
    """Pick up to k distinct past events, each >= min_gap_hours apart.

    `is_close` is False when the match is farther than the training-cloud p95:
    the analog is still shown, but callers must label it as distant rather than
    claiming a similar pattern.
    """
    n_refs = len(main_train) - 1  # FAISS keys are rows[:-1]
    k_search = min(n_refs, max(k, k * extra))
    if k_search <= 0:
        return []
    dists, idxs = index.search(np.ascontiguousarray(context, dtype=np.float32), k_search)
    picked: List[Tuple[int, float, bool]] = []
    for idx, dist in zip(idxs[0].tolist(), dists[0].tolist()):
        if idx < 0 or idx >= n_refs:
            continue
        when = main_train.iloc[idx]["date"]
        if any(abs((when - main_train.iloc[j]["date"]).total_seconds()) < min_gap_hours * 3600
               for j, _, _ in picked):
            continue
        picked.append((int(idx), float(dist), bool(dist <= max_distance)))
        if len(picked) >= k:
            break
    return picked


_CACHE_LOCK = threading.Lock()
_ERA5_CACHE: Tuple[np.ndarray, Dict[str, NodeTelemetry], datetime.datetime] | None = None
_ERA5_TIMESTAMP: float = 0.0

ERA5_H7_DAYS = 7
ERA5_LOOKBACK_DAYS = 1
ERA5_CACHE_TTL_SECONDS = 3600.0

_COMPLETE_FIELDS = (
    "temperature_2m", "relative_humidity_2m", "dew_point_2m", "surface_pressure",
    "wind_speed_10m", "wind_direction_10m", "cloud_cover", "precipitation",
)


def _select_h7_end_index(times: List[str], cutoff: datetime.datetime) -> int:
    """Newest hourly index whose timestamp is at or before cutoff; -1 when none."""
    cutoff_iso = cutoff.strftime("%Y-%m-%dT%H:%M")
    return max((i for i, t in enumerate(times) if t <= cutoff_iso), default=-1)


def _has_complete_window(data: List[dict], end_i: int, seq_len: int = 6) -> bool:
    """True when all nodes have non-null values for every hour in the window."""
    for i in range(end_i - seq_len + 1, end_i + 1):
        for node in data:
            hourly = node["hourly"]
            if any(hourly[field][i] is None for field in _COMPLETE_FIELDS):
                return False
    return True


def _telemetry(node_name: str, temp: float, dew: float, rain: float, humidity: float, wind: float, wind_dir: float, pressure: float) -> NodeTelemetry:
    return NodeTelemetry(
        nodeId=node_name,
        tempCelsius=round(temp, 1),
        dewPointCelsius=round(dew, 1),
        rainIntensityMmH=round(rain, 2),
        humidityPercent=round(humidity, 1),
        windSpeedKmh=round(wind, 1),
        windDirectionDeg=round(wind_dir, 0),
        pressureHpa=round(pressure, 1),
    )


def _fetch_era5_h7() -> Tuple[np.ndarray, Dict[str, NodeTelemetry], datetime.datetime] | None:
    """
    Fetch the newest ERA5 archive window that is at least H-7 old.

    cutoff = utcnow - 7 days; the last input hour must be <= cutoff, so every
    response is guaranteed to lag at least 7 days. If the boundary hour is not
    fully populated yet, the window shifts back one hour at a time instead of
    falling back to the stale parquet. Cached for an hour.
    Returns (features_array [6, 5, 10], telemetries_dict, latest_timestamp) or None.
    """
    global _ERA5_CACHE, _ERA5_TIMESTAMP
    import time

    with _CACHE_LOCK:
        if _ERA5_CACHE is not None and (time.time() - _ERA5_TIMESTAMP) < ERA5_CACHE_TTL_SECONDS:
            return _ERA5_CACHE

    try:
        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=ERA5_H7_DAYS)
        start = (cutoff - datetime.timedelta(days=ERA5_LOOKBACK_DAYS)).date().isoformat()
        lats = [str(NODE_COORDINATES[n][0]) for n in NODE_NAMES]
        lons = [str(NODE_COORDINATES[n][1]) for n in NODE_NAMES]
        params = {
            "latitude": ",".join(lats),
            "longitude": ",".join(lons),
            "start_date": start,
            "end_date": cutoff.date().isoformat(),
            "hourly": list(_COMPLETE_FIELDS),
            "timezone": "UTC",
            "models": "era5",
        }
        resp = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params, timeout=20)
        if resp.status_code != 200:
            return _ERA5_CACHE
        data = resp.json()
        if not isinstance(data, list) or len(data) != len(NODE_NAMES):
            return _ERA5_CACHE

        elev_map = {d["name"]: d["elevation_m"] for d in NODE_DEFINITIONS}
        h_sample = data[0]["hourly"]
        end_i = _select_h7_end_index(h_sample["time"], cutoff)
        while end_i >= 5 and not _has_complete_window(data, end_i):
            end_i -= 1
        if end_i < 5:
            return _ERA5_CACHE
        indices = list(range(end_i - 5, end_i + 1))

        latest_dt_utc = datetime.datetime.fromisoformat(h_sample["time"][end_i])
        if latest_dt_utc > cutoff:
            raise RuntimeError(f"ERA5 H-7 guard violated: {latest_dt_utc} > {cutoff}")

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
            telemetries[node_name] = _telemetry(
                node_name,
                float(h["temperature_2m"][last_i]),
                float(h["dew_point_2m"][last_i]),
                float(h["precipitation"][last_i]),
                float(h["relative_humidity_2m"][last_i]),
                float(h["wind_speed_10m"][last_i]),
                float(h["wind_direction_10m"][last_i]),
                float(h["surface_pressure"][last_i]),
            )

        feats = np.array(node_matrices, dtype=np.float32).transpose(1, 0, 2)
        with _CACHE_LOCK:
            _ERA5_CACHE = (feats, telemetries, latest_dt_utc)
            _ERA5_TIMESTAMP = time.time()
        return _ERA5_CACHE

    except Exception:
        logging.getLogger(__name__).exception("ERA5 H-7 fetch failed; serving fallback")
        return _ERA5_CACHE


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
        telemetries[n] = _telemetry(
            n,
            float(last_row["temperature"]),
            float(last_row["dewpoint"]),
            float(last_row["precipitation"]),
            float(last_row["relative_humidity"]),
            float(last_row["wind_speed"]),
            float(last_row["wind_direction"]),
            float(last_row["surface_pressure"]),
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
    1. Fetch an ERA5 archive window at least 7 days old (or dataset fallback)
    2. Normalize and run Spatio-Temporal GNN + FAISS Retrieval + Diffusion sampling
    3. Query top-3 real analogs from training database
    4. Format valid JSON response
    """
    model_wrapper, stats, retrieval_db, main_train = get_inference_engine(checkpoint_path)
    feature_cols = model_wrapper.config["feature_cols"]

    # 1. Fetch input sequence — ERA5 archive, guaranteed H-7 or older
    era5_result = _fetch_era5_h7()
    if era5_result is not None:
        feats_raw, telemetries, obs_dt = era5_result
        source_label = "era5_h7"
    else:
        feats_raw, telemetries, obs_dt = _fetch_parquet_fallback(feature_cols)
        source_label = "sample"

    # Single WIB formatter: every "WIB" string comes from a UTC value shifted once.
    bulan_id = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
        7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des",
    }

    def _wib(dt: datetime.datetime) -> str:
        dt = dt + datetime.timedelta(hours=7)
        return f"{dt.day} {bulan_id[dt.month]} {dt.year}, {dt.strftime('%H:%M WIB')}"

    obs_wib = obs_dt + datetime.timedelta(hours=7)
    window_start_wib = obs_wib - datetime.timedelta(hours=5)
    obs_wib_str = _wib(obs_dt)
    valid_wib_str = _wib(obs_dt + datetime.timedelta(hours=1))
    if window_start_wib.date() == obs_wib.date():
        window_range_str = f"{window_start_wib.strftime('%H:%M')} – {obs_wib.strftime('%H:%M WIB')}"
    else:
        window_range_str = f"{window_start_wib.day} {bulan_id[window_start_wib.month]} {window_start_wib.strftime('%H:%M')} – {obs_wib.day} {bulan_id[obs_wib.month]} {obs_wib.strftime('%H:%M WIB')}"

    # 2. Normalize and run inference
    c_mean = stats["c_mean"].numpy()
    c_std = stats["c_std"].numpy()
    feats_norm = (feats_raw - c_mean) / (c_std + ZSCORE_EPSILON)
    feats_norm_t = torch.tensor(feats_norm, dtype=torch.float32)

    # ponytail: one seed per observed hour, so refresh gives identical samples.
    # Per-request seeds would need a cached sampler; add if multi-user determinism matters.
    torch.manual_seed(int(obs_dt.timestamp()) // 3600)

    inference_res = run_inference_real(
        feats_norm_t,
        model_wrapper,
        stats,
        retrieval_db,
        num_samples=30,
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
            unit="km/jam",
            raw_samples=inference_res["wind_speed"],
            observed_now=round(main_telemetry.windSpeedKmh, 2) if main_telemetry else None,
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

    # 4. Extract Real FAISS Historical Analogs (distance-bounded, distinct events)
    context_last = feats_norm[-1, 0, :].reshape(1, -1)  # MAIN node at time t
    k_analogs = int(model_wrapper.config.get("k_neighbors", 3))
    threshold = _analog_distance_threshold(retrieval_db)
    picked = _select_analogs(
        retrieval_db.index, main_train, context_last,
        k=k_analogs, max_distance=threshold,
    )

    analogs: List[HistoricalAnalog] = []
    for rank, (idx, dist, is_close) in enumerate(picked, start=1):
        row = main_train.iloc[idx + 1]
        pattern_wib = _wib(main_train.iloc[idx]["date"])
        analog_wib = _wib(row["date"])
        pattern = (
            "Hujan lebat"
            if row["precipitation"] >= 5.0
            else ("Hujan sedang" if row["precipitation"] >= 2.0 else ("Gerimis" if row["precipitation"] > 0 else "Tidak hujan"))
        )
        analog = HistoricalAnalog(
            id=f"FAISS-{rank:02d}",
            rank=rank,
            datetime=analog_wib,
            patternAtWib=pattern_wib,
            patternType=pattern,
            distanceL2=round(float(dist), 2),
            rainRateMmH=round(float(row["precipitation"]), 2),
            peakWindKmh=round(float(row["wind_speed"]), 1),
            tempCelsius=round(float(row["temperature"]), 1),
            humidityPercent=round(float(row["relative_humidity"]), 1),
            pressureHpa=round(float(row["surface_pressure"]), 1),
            isWithinThreshold=is_close,
            outcomeSummary=(
                ("" if is_close else "Analog jauh (di luar p95 data latih). ")
                + f"Pola cuaca {pattern_wib} mirip. Satu jam kemudian: {pattern.lower()}, "
                f"angin {row['wind_speed']:.1f} km/jam, kelembapan {row['relative_humidity']:.1f}%."
            ),
        )
        analogs.append(analog)

    # 5. Build TimelineFrame
    frame = TimelineFrame(
        offset="Now",
        timeWib=obs_wib_str,
        windowRangeWib=window_range_str,
        description=f"Observasi 5 sel ERA5 jendela 6 titik jam ({window_range_str}) menuju jam berikutnya {valid_wib_str}.",
        telemetries=telemetries,
    )

    return DashboardLiveSnapshot(
        source=source_label,
        generatedAt=datetime.datetime.utcnow().isoformat() + "Z",
        frame=frame,
        nowcast=nowcast,
        analogs=analogs,
    )
