import { ModelMetrics } from '../types';
import { CURRENT_MODEL_METRICS } from '../data/nodesData';

const endpoint = import.meta.env.VITE_METRICS_URL ?? '/api/v1/metrics';

export async function fetchModelMetrics(signal?: AbortSignal): Promise<ModelMetrics> {
  try {
    const response = await fetch(endpoint, { headers: { Accept: 'application/json' }, signal });
    if (!response.ok) return CURRENT_MODEL_METRICS;
    const data = await response.json();
    const p = data?.results?.full_model?.precipitation;
    if (!p) return CURRENT_MODEL_METRICS;

    return {
      rmse: Number(p.rmse ?? CURRENT_MODEL_METRICS.rmse),
      mae: Number(p.mae ?? CURRENT_MODEL_METRICS.mae),
      corr: Number(p.correlation ?? CURRENT_MODEL_METRICS.corr),
      crps: Number(p.crps ?? CURRENT_MODEL_METRICS.crps),
      brierScore: Number(p.brier_2mm ?? CURRENT_MODEL_METRICS.brierScore),
      pod: Number(p.pod_2mm ?? CURRENT_MODEL_METRICS.pod),
      far: Number(p.far_2mm ?? CURRENT_MODEL_METRICS.far),
      csi: Number(p.csi_2mm ?? CURRENT_MODEL_METRICS.csi),
    };
  } catch {
    return CURRENT_MODEL_METRICS;
  }
}
