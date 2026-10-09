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

        assert data["source"] in ("live", "sample")
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
            assert len(dist["samples"]) == 50
            assert dist["p10"] <= dist["p50"] <= dist["p90"]
            assert dist["mean"] >= 0.0

        # 3. Real FAISS historical analogs
        assert "analogs" in data
        analogs = data["analogs"]
        assert len(analogs) == 3
        for idx, analog in enumerate(analogs, start=1):
            assert analog["id"] == f"FAISS-{idx:02d}"
            assert analog["rank"] == idx
            assert 0.0 <= analog["similarityPercent"] <= 100.0
            assert analog["distanceL2"] >= 0.0
            assert "WIB" in analog["datetime"]


@pytest.mark.asyncio
async def test_dashboard_live_fallback_on_network_failure():
    """Verify that when Open-Meteo network request fails, parquet fallback activates cleanly."""
    transport = httpx.ASGITransport(app=app)
    with patch("api.services.inference_service._fetch_open_meteo_live", return_value=None):
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/api/v1/dashboard/live")
            assert resp.status_code == 200
            data = resp.json()
            assert data["source"] == "live"
            assert len(data["frame"]["telemetries"]) == 5
            assert len(data["nowcast"]["precipitation"]["samples"]) == 50


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

