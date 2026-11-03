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


class NodeTelemetry(BaseModel):
    """Telemetri observasi satu node pada jam terkini."""

    nodeId: str
    tempCelsius: float
    dewPointCelsius: float
    rainIntensityMmH: float
    humidityPercent: float
    windSpeedKmh: float
    windDirectionDeg: float
    pressureHpa: float


class TimelineFrame(BaseModel):
    """Frame observasi lima node saat ini."""

    offset: str = "Now"
    timeWib: str
    windowRangeWib: str | None = None
    description: str
    telemetries: dict[str, NodeTelemetry]


class NowcastDistribution(BaseModel):
    """Distribusi probabilitas prediksi nowcasting T+1 jam."""

    horizon: str = "T+1h"
    validAtWib: str
    samples: list[float]
    mean: float
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float
    observedNow: float | None = None
    unit: str
    variable: str


class NowcastVariableSet(BaseModel):
    """Set tiga variabel prediksi nowcasting T+1 jam."""

    precipitation: NowcastDistribution
    wind_speed: NowcastDistribution
    relative_humidity: NowcastDistribution


class HistoricalAnalog(BaseModel):
    """Item analog historis hasil query FAISS IndexFlatL2."""

    id: str
    rank: int | None = None
    datetime: str
    patternAtWib: str | None = None
    patternType: str
    distanceL2: float | None = None
    rainRateMmH: float | None = None
    peakWindKmh: float
    tempCelsius: float | None = None
    humidityPercent: float | None = None
    pressureHpa: float | None = None
    outcomeSummary: str


class DashboardLiveSnapshot(BaseModel):
    """Payload kontrak GET /api/v1/dashboard/live untuk dashboard publik."""

    source: str
    generatedAt: str
    frame: TimelineFrame
    nowcast: NowcastVariableSet
    analogs: list[HistoricalAnalog] | None = None
