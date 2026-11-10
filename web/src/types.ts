export type NodeId = 'MAIN' | 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';

export interface ObservationNode {
  id: NodeId;
  name: string;
  locationName: string;
  role: string;
  lat: number;
  lng: number;
  elevation: number;
  isTarget: boolean;
  color: string;
}

export interface NodeTelemetry {
  nodeId: NodeId;
  tempCelsius: number;
  dewPointCelsius: number;
  rainIntensityMmH: number;
  humidityPercent: number;
  windSpeedKmh: number;
  windDirectionDeg: number;
  pressureHpa: number;
}

export interface NowcastDistribution {
  horizon: 'T+1h';
  validAtWib: string;
  samples: number[];
  mean: number;
  p10: number;
  p25: number;
  p50: number;
  p75: number;
  p90: number;
  observedNow?: number;
  unit: string;
  variable: 'precipitation' | 'wind_speed' | 'relative_humidity';
}

export interface TimelineFrame {
  offset: 'Now';
  timeWib: string;
  windowRangeWib?: string;
  description: string;
  telemetries: Partial<Record<NodeId, NodeTelemetry>>;
}

export type DashboardDataSource = 'era5_h7' | 'sample';
export type NowcastVariableSet = {
  precipitation: NowcastDistribution;
  wind_speed: NowcastDistribution;
  relative_humidity: NowcastDistribution;
};
export interface DashboardLiveSnapshot {
  source: DashboardDataSource;
  frame: TimelineFrame;
  nowcast: NowcastVariableSet;
  analogs?: HistoricalAnalog[];
}

export interface ModelMetrics {
  csi: number;
  pod: number;
  far: number;
  rmse: number;
  mae: number;
  crps: number;
  brierScore: number;
  corr: number;
}

export interface HistoricalAnalog {
  id: string;
  rank?: number | null;
  datetime: string;
  patternAtWib?: string | null;
  patternType: string;
  distanceL2?: number | null;
  rainRateMmH?: number | null;
  peakWindKmh: number;
  tempCelsius?: number | null;
  humidityPercent?: number | null;
  pressureHpa?: number | null;
  isWithinThreshold?: boolean;
  outcomeSummary: string;
}

export type ActiveTab = 'map' | 'forecast' | 'eval';
