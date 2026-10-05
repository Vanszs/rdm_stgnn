from typing import Any

from pydantic import BaseModel, ConfigDict


class VariableMetrics(BaseModel):
    """Metrik satu variabel target.

    `extra="allow"` meneruskan field artefak yang tidak dinamai eksplisit
    (`brier_5mm`, `pod_10mm`, `far_2mm`, ...) tanpa memotong payload.
    """

    model_config = ConfigDict(extra="allow")

    rmse: float | None = None
    mae: float | None = None
    correlation: float | None = None
    crps: float | None = None


class ScenarioMetrics(BaseModel):
    """Satu skenario evaluasi dengan tiga target kanonik pipeline."""

    model_config = ConfigDict(extra="allow")

    precipitation: VariableMetrics | None = None
    wind_speed: VariableMetrics | None = None
    relative_humidity: VariableMetrics | None = None


class MetricsSummary(BaseModel):
    """Kontrak `GET /api/v1/metrics` dari artefak evaluasi kanonik."""

    model_config = ConfigDict(extra="allow")

    metadata: dict[str, Any]
    results: dict[str, ScenarioMetrics]
