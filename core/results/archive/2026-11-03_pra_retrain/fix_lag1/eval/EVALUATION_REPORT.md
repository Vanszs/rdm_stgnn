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
| full_model | 0.6252 | 0.2568 | 0.7015 | 0.1843 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 0.9857 | 0.7527 | 0.8806 | 0.5302 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| full_model | 2.8831 | 2.0080 | 0.9743 | 1.4130 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.6674 | 0.5718 | 0.3529 | 0.0336 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.0830 | 0.2593 | 0.0806 | 0.0060 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| full_model | 0.0000 | nan | 0.0000 | 0.0002 |

