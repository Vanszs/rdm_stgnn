"""
End-to-end integration tests for FastAPI backend routes:
- GET /api/v1/metrics
- GET /api/v1/dashboard/live
"""
from __future__ import annotations

from unittest.mock import patch
import pytest
import httpx

from main import app


@pytest.mark.asyncio
async def test_metrics_endpoint_returns_skenario_3_metrics():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/metrics")
        assert resp.status_code == 200
        data = resp.json()

        assert "metadata" in data
        assert "results" in data
        assert data["metadata"]["samples_per_scenario"] == 35058

        full_model = data["results"]["full_model"]
        precip = full_model["precipitation"]
        assert precip["rmse"] > 0
        assert precip["crps"] > 0
        assert 0.65 < precip["rmse"] < 0.68  # Skenario 3: 0.6620


@pytest.mark.asyncio
async def test_dashboard_live_endpoint_returns_real_rdm_inference():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/dashboard/live")
        assert resp.status_code == 200
        data = resp.json()

        assert data["source"] in ("era5_h7", "sample")
        assert "generatedAt" in data
        assert "frame" in data
        assert "nowcast" in data

        # 1. Telemetries for 5 canonical nodes
        telemetries = data["frame"]["telemetries"]
        for node in ("MAIN", "UP", "DOWN", "LEFT", "RIGHT"):
            assert node in telemetries
            tel = telemetries[node]
            assert -10.0 <= tel["tempCelsius"] <= 50.0
            assert 0.0 <= tel["humidityPercent"] <= 100.0
            assert 600.0 <= tel["pressureHpa"] <= 1050.0
            assert tel["rainIntensityMmH"] >= 0.0

        # 2. Nowcasting distributions for 3 variables
        nowcast = data["nowcast"]
        for var in ("precipitation", "wind_speed", "relative_humidity"):
            dist = nowcast[var]
            assert dist["horizon"] == "T+1h"
            assert len(dist["samples"]) == 30
            assert dist["p10"] <= dist["p50"] <= dist["p90"]
            assert dist["mean"] >= 0.0

        # 3. Real FAISS historical analogs
        assert "analogs" in data
        analogs = data["analogs"]
        assert len(analogs) == 3
        for idx, analog in enumerate(analogs, start=1):
            assert analog["id"] == f"FAISS-{idx:02d}"
            assert analog["rank"] == idx
            assert analog["distanceL2"] >= 0.0
            assert "similarityPercent" not in analog
            assert "WIB" in analog["datetime"]


@pytest.mark.asyncio
async def test_dashboard_live_fallback_on_network_failure():
    """Verify that when Open-Meteo network request fails, parquet fallback activates cleanly."""
    transport = httpx.ASGITransport(app=app)
    with patch("api.services.inference_service._fetch_era5_h7", return_value=None):
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/api/v1/dashboard/live")
            assert resp.status_code == 200
            data = resp.json()
            assert data["source"] == "sample"
            assert len(data["frame"]["telemetries"]) == 5
            assert len(data["nowcast"]["precipitation"]["samples"]) == 30


@pytest.mark.asyncio
async def test_root_and_web_app_mount():
    """Verify root endpoint and static web app delivery."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r_root = await client.get("/")
        assert r_root.status_code == 200
        assert r_root.json()["status"] == "online"

        r_app = await client.get("/app/")
        assert r_app.status_code == 200
        assert "html" in r_app.text.lower()


@pytest.mark.asyncio
async def test_dashboard_live_latency_under_two_seconds():
    """Verify live inference latency satisfies operational <= 2.0s constraint."""
    import time

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Warmup
        await client.get("/api/v1/dashboard/live")

        # Benchmark
        t0 = time.time()
        resp = await client.get("/api/v1/dashboard/live")
        latency = time.time() - t0
        assert resp.status_code == 200
        assert latency < 2.0, f"Latency {latency:.3f}s exceeded 2.0s limit"



# --- FAISS analog selection: distance flag, distinct events, k cap ---

class _FakeIndex:
    def __init__(self, idxs, dists):
        import numpy as np

        self._idxs = np.asarray(idxs, dtype=np.int64)
        self._dists = np.asarray(dists, dtype=np.float32)

    def search(self, _query, k):
        n = min(k, len(self._idxs))
        return self._dists[:n].reshape(1, -1), self._idxs[:n].reshape(1, -1)


def _catalog(hours: int):
    import pandas as pd

    return pd.DataFrame({"date": pd.date_range("2015-01-01", periods=hours, freq="h")})


def test_analogs_collapse_consecutive_hours_to_one_event():
    import numpy as np

    from api.services.inference_service import _select_analogs

    index = _FakeIndex(idxs=[0, 1, 2, 30], dists=[0.1, 0.1, 0.1, 0.2])
    picked = _select_analogs(index, _catalog(48), np.zeros((1, 10)), k=3, max_distance=1e9)
    assert [i for i, _, _ in picked] == [0, 30], picked


def test_analogs_flag_far_matches_instead_of_dropping():
    import numpy as np

    from api.services.inference_service import _select_analogs

    index = _FakeIndex(idxs=[0, 30], dists=[0.5, 9.0])
    picked = _select_analogs(index, _catalog(48), np.zeros((1, 10)), k=3, max_distance=1.0)
    assert [i for i, _, _ in picked] == [0, 30], picked
    assert [c for _, _, c in picked] == [True, False], picked


def test_analogs_cap_at_k_and_skip_invalid_indices():
    import numpy as np

    from api.services.inference_service import _select_analogs

    index = _FakeIndex(idxs=[-1, 0, 30, 60, 90], dists=[0.1, 0.1, 0.1, 0.1, 0.1])
    picked = _select_analogs(index, _catalog(200), np.zeros((1, 10)), k=2, max_distance=1e9)
    assert [i for i, _, _ in picked] == [0, 30], picked
