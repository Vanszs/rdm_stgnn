import { ModelMetrics } from '../types';

const endpoint = import.meta.env.VITE_METRICS_URL ?? '/api/v1/metrics';

const num = (value: unknown): number | null =>
  typeof value === 'number' && Number.isFinite(value) ? value : null;

export async function fetchModelMetrics(signal?: AbortSignal): Promise<ModelMetrics | null> {
  try {
    const response = await fetch(endpoint, { headers: { Accept: 'application/json' }, signal });
    if (!response.ok) return null;
    const data = await response.json();
    const p = data?.results?.full_model?.precipitation;
    if (!p) return null;
    const metrics: ModelMetrics = {
      rmse: num(p.rmse) ?? NaN,
      mae: num(p.mae) ?? NaN,
      corr: num(p.correlation) ?? NaN,
      crps: num(p.crps) ?? NaN,
      brierScore: num(p.brier_2mm) ?? NaN,
      pod: num(p.pod_2mm) ?? NaN,
      far: num(p.far_2mm) ?? NaN,
      csi: num(p.csi_2mm) ?? NaN,
    };
    return Object.values(metrics).every(Number.isFinite) ? metrics : null;
  } catch {
    return null;
  }
}
