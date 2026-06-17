# student_textcnn_hard Report

## 1. Scope

- Student: `character-level textcnn`
- Mode: `hard`
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
alpha = N/A
fn_distill_weight = N/A
```

## 3. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7212 | 0.9969 | 0.9969 | 0.9971 | 0.9961 | 0.9982 | 0.9999 | 0.9999 |
| val | 1186 | 0.9874 | 0.9872 | 0.9860 | 0.9851 | 0.9869 | 0.9990 | 0.9989 |
| test_real | 385 | 0.9558 | 0.8610 | 0.7463 | 0.6757 | 0.8333 | 0.9649 | 0.8123 |
| test_mixed | 1059 | 0.9868 | 0.9868 | 0.9866 | 0.9790 | 0.9942 | 0.9993 | 0.9993 |
| test_challenge | 720 | 0.9889 | 0.9884 | 0.9861 | 0.9861 | 0.9861 | 0.9991 | 0.9986 |

## 5. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 3349 | 7 |
| true_1 | 15 | 3841 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 642 | 7 |
| true_1 | 8 | 529 |

### test_real

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 343 | 5 |
| true_1 | 12 | 25 |

### test_mixed

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 531 | 3 |
| true_1 | 11 | 514 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 429 | 4 |
| true_1 | 4 | 283 |

## 6. Test Metrics by Data Origin

| split | group_value | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | paraphrased | 132 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_challenge | real | 258 | 0.9238 | 0.8627 | 0.8800 | 0.8462 |
| test_challenge | synthetic | 100 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | synthetic_hard_positive | 130 | 0.4981 | 0.9961 | 0.9923 | 1.0000 |
| test_mixed | external_curated | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | paraphrased | 434 | 0.4994 | 0.9988 | 0.9977 | 1.0000 |
| test_mixed | real | 258 | 0.8758 | 0.7727 | 0.6800 | 0.8947 |
| test_mixed | synthetic | 201 | 0.4988 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | synthetic_hard_positive | 66 | 0.4923 | 0.9846 | 0.9697 | 1.0000 |
| test_real | real | 385 | 0.8610 | 0.7463 | 0.6757 | 0.8333 |

## 7. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.259172  |       0.972758 |         0.970093 |             0.96648  |
|       2 |    0.0934651 |       0.970973 |         0.967742 |             0.949721 |
|       3 |    0.0551183 |       0.979547 |         0.977444 |             0.968343 |
|       4 |    0.0509293 |       0.987237 |         0.986021 |             0.985102 |
|       5 |    0.0378008 |       0.9838   |         0.982092 |             0.970205 |
|       6 |    0.0320215 |       0.982944 |         0.981132 |             0.968343 |
|       7 |    0.0292133 |       0.98637  |         0.984991 |             0.977654 |
