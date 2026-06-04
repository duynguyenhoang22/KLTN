# Phase 5 Student Hard-label Baseline Report

## 1. Scope

- Student: `TF-IDF char_wb 3-5 + Logistic Regression`
- Training signal: hard labels only
- Teacher outputs: not used
- Split dir: `data\distillation\splits_v2`
- Decision threshold: `0.5`

## 2. Configuration

```text
tfidf_analyzer = char_wb
tfidf_ngram_range = (3, 5)
tfidf_min_df = 2
tfidf_max_features = 200000
logreg_C = 2.0
logreg_class_weight = balanced
seed = 42
```

The model uses only `content` as input. Metadata columns are kept only for audit.

## 3. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7212 | 0.9956 | 0.9955 | 0.9958 | 0.9933 | 0.9984 | 0.9999 | 0.9999 |
| val | 1186 | 0.9857 | 0.9855 | 0.9840 | 0.9758 | 0.9924 | 0.9984 | 0.9982 |
| test_real | 385 | 0.9610 | 0.8703 | 0.7619 | 0.6486 | 0.9231 | 0.9782 | 0.8570 |
| test_mixed | 1059 | 0.9877 | 0.9877 | 0.9875 | 0.9790 | 0.9961 | 0.9974 | 0.9982 |
| test_challenge | 720 | 0.9833 | 0.9827 | 0.9792 | 0.9861 | 0.9725 | 0.9990 | 0.9985 |

## 4. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 3350 | 6 |
| true_1 | 26 | 3830 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 645 | 4 |
| true_1 | 13 | 524 |

### test_real

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 346 | 2 |
| true_1 | 13 | 24 |

### test_mixed

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 532 | 2 |
| true_1 | 11 | 514 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 425 | 8 |
| true_1 | 4 | 283 |

## 5. Train Distribution

### Label

|   label |   count |
|--------:|--------:|
|       1 |    3856 |
|       0 |    3356 |

### Data Origin

| data_origin             |   count |
|:------------------------|--------:|
| paraphrased             |    3333 |
| synthetic               |    1506 |
| real                    |    1281 |
| synthetic_hard_negative |     391 |
| external_curated        |     351 |
| external_real           |     350 |

## 6. Group Audit Files

Full subgroup metrics are saved to `student_tfidf_hard_metrics_by_group.csv`.

### Test Metrics by Data Origin

| split | group_value | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 50 | 0.4792 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | paraphrased | 132 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_challenge | real | 258 | 0.9311 | 0.8750 | 0.8400 | 0.9130 |
| test_challenge | synthetic | 100 | 0.4975 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | synthetic_hard_negative | 130 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_mixed | external_curated | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | paraphrased | 434 | 0.4988 | 0.9977 | 0.9954 | 1.0000 |
| test_mixed | real | 258 | 0.8858 | 0.7907 | 0.6800 | 0.9444 |
| test_mixed | synthetic | 201 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | synthetic_hard_negative | 66 | 0.4962 | 0.9924 | 0.9848 | 1.0000 |
| test_real | real | 385 | 0.8703 | 0.7619 | 0.6486 | 0.9231 |

## 7. Outputs

```text
student_tfidf_hard_metrics.json
student_tfidf_hard_metrics_by_split.csv
student_tfidf_hard_metrics_by_group.csv
student_tfidf_hard_predictions_<split>.csv
student_tfidf_hard_errors_<split>.csv
student_tfidf_hard_model.joblib
student_tfidf_hard_report.md
```

## 8. Phase 6 Reminder

This baseline must be compared against a distilled student with the same architecture. If Phase 6 reduces `recall_label_1` on `test_real`, report the trade-off explicitly.
