# Phase 6 Student Distilled Report

## 1. Scope

- Student: `TF-IDF char_wb 3-5 + Logistic Regression`
- Training signal: hard labels plus teacher probabilities
- Input features: `content` only
- Teacher dir: `data\distillation\teacher_outputs_v2`
- Baseline dir: `setup_results\distillation_v2\student_tfidf_hard_label`

## 2. Distillation Method

Scikit-learn Logistic Regression does not accept soft targets directly. This implementation converts each training sample into two weighted rows: one with label 0 and weight `soft_target_p0`, one with label 1 and weight `soft_target_p1`.

```text
beta = (1 - alpha) * effective_distill_weight
soft_target_p1 = (1 - beta) * hard_label + beta * teacher_p1
soft_target_p0 = 1 - soft_target_p1
```

For teacher false negatives (`label=1`, `teacher_pred=0`), `effective_distill_weight` is capped to avoid teaching the student to miss smishing.

## 3. Configuration

```text
alpha = 0.9
teacher_probability = t2
fn_distill_weight = 0.0
threshold = 0.5
tfidf_min_df = 2
tfidf_max_features = 200000
logreg_C = 2.0
class_weight = balanced
seed = 42
```

## 4. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7212 | 0.9956 | 0.9955 | 0.9958 | 0.9933 | 0.9984 | 0.9999 | 0.9999 |
| val | 1186 | 0.9865 | 0.9864 | 0.9850 | 0.9777 | 0.9924 | 0.9984 | 0.9982 |
| test_real | 385 | 0.9584 | 0.8597 | 0.7419 | 0.6216 | 0.9200 | 0.9783 | 0.8569 |
| test_mixed | 1059 | 0.9877 | 0.9877 | 0.9875 | 0.9790 | 0.9961 | 0.9974 | 0.9982 |
| test_challenge | 720 | 0.9833 | 0.9827 | 0.9792 | 0.9861 | 0.9725 | 0.9991 | 0.9986 |

## 5. Comparison with Phase 5 Hard-label Baseline

| split | macro_f1_hard | macro_f1_distilled | delta_macro_f1 | f1_label_1_hard | f1_label_1_distilled | delta_f1_label_1 | recall_label_1_hard | recall_label_1_distilled | delta_recall_label_1 | precision_label_1_hard | precision_label_1_distilled | delta_precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 0.9955 | 0.9955 | 0.0000 | 0.9958 | 0.9958 | 0.0000 | 0.9933 | 0.9933 | 0.0000 | 0.9984 | 0.9984 | 0.0000 |
| val | 0.9855 | 0.9864 | 0.0009 | 0.9840 | 0.9850 | 0.0010 | 0.9758 | 0.9777 | 0.0019 | 0.9924 | 0.9924 | 0.0000 |
| test_real | 0.8703 | 0.8597 | -0.0107 | 0.7619 | 0.7419 | -0.0200 | 0.6486 | 0.6216 | -0.0270 | 0.9231 | 0.9200 | -0.0031 |
| test_mixed | 0.9877 | 0.9877 | 0.0000 | 0.9875 | 0.9875 | -0.0000 | 0.9790 | 0.9790 | 0.0000 | 0.9961 | 0.9961 | -0.0000 |
| test_challenge | 0.9827 | 0.9827 | 0.0000 | 0.9792 | 0.9792 | -0.0000 | 0.9861 | 0.9861 | 0.0000 | 0.9725 | 0.9725 | 0.0000 |

## 6. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 3350 | 6 |
| true_1 | 26 | 3830 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 645 | 4 |
| true_1 | 12 | 525 |

### test_real

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 346 | 2 |
| true_1 | 14 | 23 |

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

## 7. Soft Target Audit

| statistic | value |
|---|---:|
| mean_effective_distill_weight | 0.9978 |
| mean_beta | 0.0998 |
| mean_soft_target_p1 | 0.5347 |
| teacher_disagreement_rows | 16 |

## 8. Group Audit Files

Full subgroup metrics are saved to `student_tfidf_distilled_metrics_by_group.csv`.

### Test Metrics by Data Origin

| split | group_value | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 50 | 0.4792 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | paraphrased | 132 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_challenge | real | 258 | 0.9311 | 0.8750 | 0.8400 | 0.9130 |
| test_challenge | synthetic | 100 | 0.4975 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | synthetic_hard_positive | 130 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_mixed | external_curated | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | paraphrased | 434 | 0.4988 | 0.9977 | 0.9954 | 1.0000 |
| test_mixed | real | 258 | 0.8858 | 0.7907 | 0.6800 | 0.9444 |
| test_mixed | synthetic | 201 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | synthetic_hard_positive | 66 | 0.4962 | 0.9924 | 0.9848 | 1.0000 |
| test_real | real | 385 | 0.8597 | 0.7419 | 0.6216 | 0.9200 |

## 9. Outputs

```text
student_tfidf_distilled_metrics.json
student_tfidf_distilled_metrics_by_split.csv
student_tfidf_distilled_metrics_by_group.csv
student_tfidf_distilled_comparison_with_hard.csv
student_tfidf_distilled_predictions_<split>.csv
student_tfidf_distilled_errors_<split>.csv
student_tfidf_distilled_soft_target_audit_train.csv
student_tfidf_distilled_model.joblib
student_tfidf_distilled_report.md
```
