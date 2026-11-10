# Evaluation Report - Main Node Only

- **main_node_name**: `MAIN`
- **main_node_identifier**: `(-6.75, 107.0)`
- **node_order**: `['MAIN', 'UP', 'DOWN', 'LEFT', 'RIGHT']`
- **graph_topology**: `star`
- **target_node_policy**: `main_node_only`
- **context_policy**: `main_node_context`
- **model_mode**: `era5`
- **data_path**: `data/raw/pangrango_era5_5node_2005_2025.parquet`
- **eval_step**: `1`
- **max_eval_samples**: `0`
- **samples_per_scenario**: `35058`
- **num_ensemble**: `40`
- **seq_len**: `6`
- **seed**: `1`
- **crps_estimator**: `fair_unbiased`
- **rain_specialization_enabled**: `True`
- **rain_occurrence_threshold_mm**: `0.1`
- **rain_probability_threshold**: `0.6000000238418579`
- **sample_batch_size**: `256`

## PRECIPITATION

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 0.7279 | 0.3165 | 0.6693 | 0.2234 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 0.9996 | 0.7636 | 0.8833 | 0.5333 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 2.8582 | 1.9915 | 0.9749 | 1.4082 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.7600 | 0.6670 | 0.3013 | 0.0448 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.1079 | 0.5357 | 0.0959 | 0.0070 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.0000 | 1.0000 | 0.0000 | 0.0002 |

