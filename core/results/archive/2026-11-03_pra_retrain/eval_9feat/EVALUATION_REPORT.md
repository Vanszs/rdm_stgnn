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
- **rain_probability_threshold**: `0.550000011920929`
- **sample_batch_size**: `256`

## PRECIPITATION

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 0.6938 | 0.3011 | 0.6797 | 0.2256 |
| diff_retrieval | 0.7378 | 0.3230 | 0.6758 | 0.2316 |
| diff_gnn | 0.7157 | 0.3165 | 0.6699 | 0.2273 |
| full_model | 0.7531 | 0.3346 | 0.6721 | 0.2331 |

## WIND_SPEED

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 1.1319 | 0.8722 | 0.8430 | 0.6239 |
| diff_retrieval | 1.1477 | 0.8835 | 0.8434 | 0.6223 |
| diff_gnn | 0.9985 | 0.7631 | 0.8782 | 0.5431 |
| full_model | 1.0137 | 0.7757 | 0.8772 | 0.5435 |

## RELATIVE_HUMIDITY

| Scenario | RMSE | MAE | Corr | CRPS |
|---|---:|---:|---:|---:|
| diff_only | 4.6022 | 3.1341 | 0.9365 | 2.3131 |
| diff_retrieval | 4.6520 | 3.0885 | 0.9361 | 2.2402 |
| diff_gnn | 3.1423 | 2.1484 | 0.9703 | 1.5279 |
| full_model | 3.2818 | 2.2099 | 0.9687 | 1.5450 |

## Precipitation Threshold Metrics

### Threshold 2.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.7155 | 0.6173 | 0.3322 | 0.0425 |
| diff_retrieval | 0.7369 | 0.6445 | 0.3155 | 0.0467 |
| diff_gnn | 0.7423 | 0.6360 | 0.3231 | 0.0438 |
| full_model | 0.7731 | 0.6543 | 0.3139 | 0.0471 |

### Threshold 5.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.1502 | 0.3770 | 0.1377 | 0.0061 |
| diff_retrieval | 0.2055 | 0.5593 | 0.1630 | 0.0069 |
| diff_gnn | 0.1067 | 0.4808 | 0.0971 | 0.0064 |
| full_model | 0.1542 | 0.5714 | 0.1279 | 0.0071 |

### Threshold 10.0 mm

| Scenario | POD | FAR | CSI | Brier |
|---|---:|---:|---:|---:|
| diff_only | 0.2857 | 0.5000 | 0.2222 | 0.0002 |
| diff_retrieval | 0.2857 | 0.6000 | 0.2000 | 0.0002 |
| diff_gnn | 0.2857 | 0.6000 | 0.2000 | 0.0002 |
| full_model | 0.4286 | 0.6250 | 0.2500 | 0.0002 |

