# Evaluation Report - Main Node Only

- **main_node_name**: `MAIN`
- **main_node_identifier**: `(-6.75, 107.0)`
- **node_order**: `['MAIN', 'UP', 'DOWN', 'LEFT', 'RIGHT']`
- **graph_topology**: `star`
- **target_node_policy**: `main_node_only`
- **context_policy**: `main_node_context`
- **model_mode**: `era5`
- **data_path**: `/home/vanszs/Documents/Skripsi_Bevan/core/data/raw/pangrango_era5_5node_2005_2025.parquet`
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
| diff_only | 0.6538 | 0.2651 | 0.6758 | 0.1981 |
| diff_retrieval | 0.6705 | 0.2729 | 0.6595 | 0.1988 |
| diff_gnn | 0.6554 | 0.2689 | 0.7092 | 0.1974 |
| full_model | 0.6641 | 0.2730 | 0.6997 | 0.1953 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 1.1813 | 0.8943 | 0.8405 | 0.6313 |
| diff_retrieval | 1.1943 | 0.9041 | 0.8369 | 0.6335 |
| diff_gnn | 0.9718 | 0.7399 | 0.8820 | 0.5181 |
| full_model | 0.9946 | 0.7575 | 0.8784 | 0.5284 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 4.3205 | 2.7818 | 0.9422 | 2.0944 |
| diff_retrieval | 4.3823 | 2.8294 | 0.9404 | 2.0719 |
| diff_gnn | 3.1248 | 2.2337 | 0.9722 | 1.6110 |
| full_model | 3.1002 | 2.1882 | 0.9701 | 1.5244 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.6459 | 0.5736 | 0.3456 | 0.0361 |
| diff_retrieval | 0.6265 | 0.5962 | 0.3255 | 0.0378 |
| diff_gnn | 0.7356 | 0.5630 | 0.3777 | 0.0359 |
| full_model | 0.7282 | 0.5723 | 0.3688 | 0.0367 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.0672 | 0.4138 | 0.0642 | 0.0066 |
| diff_retrieval | 0.0356 | 0.4706 | 0.0345 | 0.0069 |
| diff_gnn | 0.1423 | 0.5663 | 0.1200 | 0.0070 |
| full_model | 0.0870 | 0.7215 | 0.0710 | 0.0074 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.0000 | nan | 0.0000 | 0.0002 |
| diff_retrieval | 0.0000 | nan | 0.0000 | 0.0002 |
| diff_gnn | 0.0000 | 1.0000 | 0.0000 | 0.0003 |
| full_model | 0.0000 | 1.0000 | 0.0000 | 0.0003 |

