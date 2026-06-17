# student_textcnn_distilled Report

## 1. Scope

- Student: `character-level textcnn`
- Mode: `distilled`
- Input features: `content` only
- Threshold: `0.5`

## 2. Configuration

```text
max_len = 256
embed_dim = 64
hidden_dim = 64
num_filters = 96
kernel_sizes = 3,4,5
dropout = 0.3
batch_size = 128
epochs = 12
patience = 3
lr = 0.002
alpha = 0.8
fn_distill_weight = 0.0
```

## 3. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7212 | 0.9999 | 0.9999 | 0.9999 | 1.0000 | 0.9997 | 1.0000 | 1.0000 |
| val | 1186 | 0.9899 | 0.9898 | 0.9888 | 0.9870 | 0.9907 | 0.9995 | 0.9994 |
| test_real | 385 | 0.9636 | 0.8840 | 0.7879 | 0.7027 | 0.8966 | 0.9794 | 0.8770 |
| test_mixed | 1059 | 0.9943 | 0.9943 | 0.9943 | 0.9905 | 0.9981 | 0.9996 | 0.9996 |
| test_challenge | 720 | 0.9861 | 0.9855 | 0.9826 | 0.9826 | 0.9826 | 0.9993 | 0.9989 |

## 4. Comparison with Hard Baseline

| split | macro_f1_hard | macro_f1_distilled | delta_macro_f1 | f1_label_1_hard | f1_label_1_distilled | delta_f1_label_1 | recall_label_1_hard | recall_label_1_distilled | delta_recall_label_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 0.9969 | 0.9999 | 0.0029 | 0.9971 | 0.9999 | 0.0027 | 0.9961 | 1.0000 | 0.0039 |
| val | 0.9872 | 0.9898 | 0.0026 | 0.9860 | 0.9888 | 0.0028 | 0.9851 | 0.9870 | 0.0019 |
| test_real | 0.8610 | 0.8840 | 0.0230 | 0.7463 | 0.7879 | 0.0416 | 0.6757 | 0.7027 | 0.0270 |
| test_mixed | 0.9868 | 0.9943 | 0.0076 | 0.9866 | 0.9943 | 0.0077 | 0.9790 | 0.9905 | 0.0114 |
| test_challenge | 0.9884 | 0.9855 | -0.0029 | 0.9861 | 0.9826 | -0.0035 | 0.9861 | 0.9826 | -0.0035 |

## 5. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 3355 | 1 |
| true_1 | 0 | 3856 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 644 | 5 |
| true_1 | 7 | 530 |

### test_real

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 345 | 3 |
| true_1 | 11 | 26 |

### test_mixed

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 533 | 1 |
| true_1 | 5 | 520 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 428 | 5 |
| true_1 | 5 | 282 |

## 6. Test Metrics by Data Origin

| split | group_value | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | paraphrased | 132 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_challenge | real | 258 | 0.9114 | 0.8400 | 0.8400 | 0.8400 |
| test_challenge | synthetic | 100 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | synthetic_hard_positive | 130 | 0.4981 | 0.9961 | 0.9923 | 1.0000 |
| test_mixed | external_curated | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | paraphrased | 434 | 0.4994 | 0.9988 | 0.9977 | 1.0000 |
| test_mixed | real | 258 | 0.9662 | 0.9388 | 0.9200 | 0.9583 |
| test_mixed | synthetic | 201 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | synthetic_hard_positive | 66 | 0.4923 | 0.9846 | 0.9697 | 1.0000 |
| test_real | real | 385 | 0.8840 | 0.7879 | 0.7027 | 0.8966 |

## 7. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.273251  |       0.974477 |         0.972067 |             0.972067 |
|       2 |    0.117616  |       0.977835 |         0.975518 |             0.964618 |
|       3 |    0.0823156 |       0.978676 |         0.976393 |             0.962756 |
|       4 |    0.0771208 |       0.984676 |         0.983178 |             0.979516 |
|       5 |    0.066945  |       0.98553  |         0.984127 |             0.981378 |
|       6 |    0.0602042 |       0.988082 |         0.986916 |             0.98324  |
|       7 |    0.0597584 |       0.98552  |         0.984067 |             0.977654 |
|       8 |    0.0546622 |       0.988089 |         0.986965 |             0.986965 |
|       9 |    0.0523959 |       0.985515 |         0.984038 |             0.975791 |
|      10 |    0.0507563 |       0.988069 |         0.986842 |             0.977654 |
|      11 |    0.0467968 |       0.989788 |         0.988806 |             0.986965 |
|      12 |    0.0453719 |       0.988078 |         0.986891 |             0.981378 |
