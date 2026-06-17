# Distillation Benchmark Summary

## Primary Metrics

- `macro_f1`: main balanced quality measure across both labels.
- `f1_label_1`: smishing-class F1.
- `recall_label_1`: missed-smishing control metric.
- `pr_auc`: threshold-independent ranking metric for imbalanced binary detection.

## Dev/Test Results

| model_group    | model_name    | split   |   rows |   macro_f1 |   f1_label_1 |   recall_label_1 |   pr_auc |
|:---------------|:--------------|:--------|-------:|-----------:|-------------:|-----------------:|---------:|
| fine_tuned_plm | PhoBERT-base  | dev     |    535 |     0.875  |       0.7671 |           0.7568 |   0.8439 |
| fine_tuned_plm | PhoBERT-base  | test    |    535 |     0.9068 |       0.8267 |           0.8378 |   0.9191 |
| fine_tuned_plm | PhoBERT-large | dev     |    535 |     0.8975 |       0.8101 |           0.8649 |   0.8648 |
| fine_tuned_plm | PhoBERT-large | test    |    535 |     0.937  |       0.8831 |           0.9189 |   0.9248 |

## Output Files

- Long table: `setup_results/distillation_benchmark/summary/benchmark_metrics_long.csv`
- Dev/test wide table: `setup_results/distillation_benchmark/summary/benchmark_metrics_dev_test_wide.csv`
