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
- **rain_probability_threshold**: `0.6499999761581421`
- **sample_batch_size**: `256`

## PRECIPITATION

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 0.6578 | 0.2662 | 0.6714 | 0.1953 |
| diff_retrieval | 0.6656 | 0.2702 | 0.6642 | 0.1965 |
| diff_gnn | 0.6514 | 0.2676 | 0.7114 | 0.1930 |
| full_model | 0.6620 | 0.2727 | 0.7008 | 0.1950 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 1.1782 | 0.8916 | 0.8412 | 0.6291 |
| diff_retrieval | 1.1964 | 0.9058 | 0.8363 | 0.6333 |
| diff_gnn | 0.9728 | 0.7403 | 0.8819 | 0.5186 |
| full_model | 0.9952 | 0.7581 | 0.8783 | 0.5288 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 4.3115 | 2.7805 | 0.9425 | 2.0915 |
| diff_retrieval | 4.3748 | 2.8235 | 0.9406 | 2.0657 |
| diff_gnn | 3.1276 | 2.2356 | 0.9721 | 1.6122 |
| full_model | 3.0958 | 2.1906 | 0.9702 | 1.5260 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.6531 | 0.5966 | 0.3322 | 0.0355 |
| diff_retrieval | 0.6453 | 0.6049 | 0.3246 | 0.0368 |
| diff_gnn | 0.7400 | 0.5822 | 0.3643 | 0.0356 |
| full_model | 0.7350 | 0.5935 | 0.3545 | 0.0368 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.0664 | 0.4839 | 0.0625 | 0.0063 |
| diff_retrieval | 0.0415 | 0.3750 | 0.0405 | 0.0066 |
| diff_gnn | 0.1369 | 0.6118 | 0.1126 | 0.0069 |
| full_model | 0.1120 | 0.6582 | 0.0922 | 0.0070 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.0000 | 1.0000 | 0.0000 | 0.0002 |
| diff_retrieval | 0.0000 | 1.0000 | 0.0000 | 0.0002 |
| diff_gnn | 0.0000 | 1.0000 | 0.0000 | 0.0002 |
| full_model | 0.0000 | 1.0000 | 0.0000 | 0.0003 |

