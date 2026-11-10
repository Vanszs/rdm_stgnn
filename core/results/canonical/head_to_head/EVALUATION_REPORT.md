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
- **rain_probability_threshold**: `0.6000000238418579`
- **sample_batch_size**: `256`

## PRECIPITATION

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 0.6478 | 0.2741 | 0.6815 | 0.2036 |
| diff_retrieval | 0.6534 | 0.2782 | 0.6770 | 0.2007 |
| diff_gnn | 0.6469 | 0.2809 | 0.7073 | 0.2059 |
| full_model | 0.6445 | 0.2809 | 0.7077 | 0.2009 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 1.1163 | 0.8590 | 0.8422 | 0.6121 |
| diff_retrieval | 1.1260 | 0.8664 | 0.8438 | 0.6078 |
| diff_gnn | 0.9742 | 0.7498 | 0.8772 | 0.5286 |
| full_model | 1.0019 | 0.7668 | 0.8760 | 0.5342 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 4.3127 | 2.7729 | 0.9430 | 2.1459 |
| diff_retrieval | 4.3551 | 2.7881 | 0.9417 | 2.0680 |
| diff_gnn | 3.0287 | 2.1139 | 0.9729 | 1.5566 |
| full_model | 2.9714 | 2.0581 | 0.9727 | 1.4571 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.6479 | 0.5653 | 0.3516 | 0.0351 |
| diff_retrieval | 0.6245 | 0.5720 | 0.3404 | 0.0359 |
| diff_gnn | 0.7182 | 0.5740 | 0.3650 | 0.0359 |
| full_model | 0.7182 | 0.5629 | 0.3731 | 0.0359 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.0949 | 0.2258 | 0.0923 | 0.0061 |
| diff_retrieval | 0.0791 | 0.3750 | 0.0755 | 0.0061 |
| diff_gnn | 0.1107 | 0.3333 | 0.1049 | 0.0060 |
| full_model | 0.1225 | 0.3673 | 0.1144 | 0.0061 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.1429 | 0.0000 | 0.1429 | 0.0002 |
| diff_retrieval | 0.1429 | 0.0000 | 0.1429 | 0.0002 |
| diff_gnn | 0.0000 | 1.0000 | 0.0000 | 0.0002 |
| full_model | 0.1429 | 0.0000 | 0.1429 | 0.0002 |

