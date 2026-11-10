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
- **num_ensemble**: `30`
- **seq_len**: `6`
- **seed**: `1`
- **crps_estimator**: `fair_unbiased`
- **rain_specialization_enabled**: `True`
- **rain_occurrence_threshold_mm**: `0.1`
- **rain_probability_threshold**: `0.6000000238418579`

## PRECIPITATION

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 0.6433 | 0.2641 | 0.7067 | 0.1921 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 1.0157 | 0.7817 | 0.8804 | 0.5524 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 3.0812 | 2.2199 | 0.9723 | 1.6215 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.7030 | 0.5894 | 0.3499 | 0.0369 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.1411 | 0.4925 | 0.1241 | 0.0065 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.1667 | 0.8571 | 0.0833 | 0.0003 |

