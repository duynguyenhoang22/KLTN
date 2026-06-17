# student_bilstm_hard Report

## 1. Scope

- Student: `character-level BiLSTM`
- Mode: `hard`
- Input features: `content` only
- Threshold: `0.5`

## 2. Configuration

```text
max_len = 256
embed_dim = 64
hidden_dim = 64
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
| train | 7212 | 0.9720 | 0.9719 | 0.9737 | 0.9684 | 0.9790 | 0.9961 | 0.9967 |
| val | 1186 | 0.9604 | 0.9600 | 0.9561 | 0.9534 | 0.9588 | 0.9909 | 0.9887 |
| test_real | 385 | 0.9221 | 0.7580 | 0.5588 | 0.5135 | 0.6129 | 0.9119 | 0.6239 |
| test_mixed | 1059 | 0.9509 | 0.9509 | 0.9499 | 0.9390 | 0.9610 | 0.9895 | 0.9907 |
| test_challenge | 720 | 0.9264 | 0.9231 | 0.9072 | 0.9024 | 0.9120 | 0.9788 | 0.9644 |

## 5. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 3276 | 80 |
| true_1 | 122 | 3734 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 627 | 22 |
| true_1 | 25 | 512 |

### test_real

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 336 | 12 |
| true_1 | 18 | 19 |

### test_mixed

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 514 | 20 |
| true_1 | 32 | 493 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 408 | 25 |
| true_1 | 28 | 259 |

## 6. Test Metrics by Data Origin

| split | group_value | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 50 | 0.4845 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 50 | 0.4845 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | paraphrased | 132 | 0.4962 | 0.9924 | 0.9848 | 1.0000 |
| test_challenge | real | 258 | 0.8126 | 0.6667 | 0.7600 | 0.5938 |
| test_challenge | synthetic | 100 | 0.4845 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | synthetic_hard_positive | 130 | 0.4583 | 0.9167 | 0.8462 | 1.0000 |
| test_mixed | external_curated | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | paraphrased | 434 | 0.4953 | 0.9907 | 0.9816 | 1.0000 |
| test_mixed | real | 258 | 0.7396 | 0.5357 | 0.6000 | 0.4839 |
| test_mixed | synthetic | 201 | 0.4950 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | synthetic_hard_positive | 66 | 0.4407 | 0.8814 | 0.7879 | 1.0000 |
| test_real | real | 385 | 0.7580 | 0.5588 | 0.5135 | 0.6129 |

## 7. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.446981  |       0.849948 |         0.830591 |             0.798883 |
|       2 |    0.229308  |       0.917073 |         0.907354 |             0.884544 |
|       3 |    0.158995  |       0.916035 |         0.902513 |             0.836127 |
|       4 |    0.11941   |       0.959995 |         0.956116 |             0.953445 |
|       5 |    0.0941917 |       0.951994 |         0.945841 |             0.910615 |
|       6 |    0.0762795 |       0.946689 |         0.943498 |             0.979516 |
|       7 |    0.0587608 |       0.950925 |         0.948029 |             0.985102 |
