"""Guards the ERA5 H-7 contract: the input window never ends after the cutoff."""
from __future__ import annotations

import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "core"))

from api.services.inference_service import (  # noqa: E402
    _COMPLETE_FIELDS,
    _has_complete_window,
    _select_h7_end_index,
)

CUTOFF = datetime.datetime(2026, 10, 22, 12, 0)


def test_picks_last_hour_at_or_before_cutoff():
    times = ["2026-10-22T10:00", "2026-10-22T11:00", "2026-10-22T12:00", "2026-10-22T13:00"]
    assert _select_h7_end_index(times, CUTOFF) == 2


def test_rejects_window_entirely_after_cutoff():
    times = ["2026-10-22T13:00", "2026-10-22T14:00"]
    assert _select_h7_end_index(times, CUTOFF) == -1


def test_window_end_is_never_newer_than_cutoff():
    times = [f"2026-10-2{d}T{h:02d}:00" for d in (0, 1, 2) for h in range(24)]
    end = _select_h7_end_index(times, CUTOFF)
    assert end >= 5
    assert datetime.datetime.fromisoformat(times[end]) <= CUTOFF
    assert datetime.datetime.fromisoformat(times[end + 1]) > CUTOFF


def _node(n_hours=8, null_precip_at=None):
    hourly = {field: [1.0] * n_hours for field in _COMPLETE_FIELDS}
    if null_precip_at is not None:
        hourly["precipitation"][null_precip_at] = None
    return {"hourly": hourly}


def test_window_needs_the_lag_hour_too():
    # 6-hour window ending at index 6 reads precipitation[0] as lag1.
    assert _has_complete_window([_node()], 6) is True
    assert _has_complete_window([_node(null_precip_at=0)], 6) is False
