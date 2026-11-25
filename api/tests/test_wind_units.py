"""Wind crosses the API boundary in km/h; ERA5/parquet store m/s."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))

from api.services.inference_service import _MS_TO_KMH, _telemetry  # noqa: E402


def test_ms_to_kmh_factor():
    assert _MS_TO_KMH == 3.6


def test_telemetry_reports_wind_in_kmh():
    tel = _telemetry("MAIN", 10.0, 9.0, 0.0, 90.0, 4.0, 180.0, 700.0)
    assert tel.windSpeedKmh == 14.4
