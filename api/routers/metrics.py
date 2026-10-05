import json
import math
import os

from fastapi import APIRouter, HTTPException

from api.schemas import MetricsSummary

router = APIRouter(prefix="/api/v1/metrics", tags=["Evaluation Metrics"])

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_SUMMARY_PATH = "core/results/tabel_3_17/sken_3_default_kontrol/eval/comparison/comparison_summary.json"


def _resolve_summary_path() -> str:
    """Artefak evaluasi kanonik, dapat ditimpa lewat env untuk rerun skenario lain."""
    configured = os.environ.get("METRICS_SUMMARY_PATH", DEFAULT_SUMMARY_PATH)
    if os.path.isabs(configured):
        return configured
    return os.path.join(PROJECT_ROOT, configured)


def _sanitize_json(value):
    """NaN/Infinity bukan JSON valid; FastAPI menolaknya dengan 500."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _sanitize_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_json(item) for item in value]
    return value


@router.get("", response_model=MetricsSummary)
def get_metrics_summary() -> MetricsSummary:
    """Metrik evaluasi model kanonik (main-node-only, 35.058 jendela uji)."""
    summary_path = _resolve_summary_path()

    if not os.path.exists(summary_path):
        raise HTTPException(
            status_code=404,
            detail=f"Metrics summary not found at {summary_path}",
        )

    try:
        with open(summary_path, "r", encoding="utf-8") as file:
            payload = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise HTTPException(
            status_code=500,
            detail=f"Metrics summary unreadable: {error}",
        ) from error

    return MetricsSummary.model_validate(_sanitize_json(payload))
