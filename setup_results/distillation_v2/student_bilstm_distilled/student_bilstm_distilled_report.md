# student_bilstm_distilled Report

## 1. Scope

- Student: `character-level BiLSTM`
- Mode: `distilled`
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
alpha = 0.8
fn_distill_weight = 0.0
```

## 3. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7212 | 0.9904 | 0.9904 | 0.9910 | 0.9904 | 0.9917 | 0.9994 | 0.9995 |
| val | 1186 | 0.9772 | 0.9770 | 0.9748 | 0.9739 | 0.9757 | 0.9964 | 0.9961 |
| test_real | 385 | 0.9299 | 0.8052 | 0.6494 | 0.6757 | 0.6250 | 0.9440 | 0.7332 |
| test_mixed | 1059 | 0.9773 | 0.9773 | 0.9771 | 0.9752 | 0.9790 | 0.9959 | 0.9963 |
| test_challenge | 720 | 0.9722 | 0.9711 | 0.9655 | 0.9756 | 0.9556 | 0.9961 | 0.9936 |

## 5. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 3324 | 32 |
| true_1 | 37 | 3819 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 636 | 13 |
| true_1 | 14 | 523 |

### test_real

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 333 | 15 |
| true_1 | 12 | 25 |

### test_mixed

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 523 | 11 |
| true_1 | 13 | 512 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 420 | 13 |
| true_1 | 7 | 280 |

## 6. Test Metrics by Data Origin

| split | group_value | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 50 | 0.4898 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | paraphrased | 132 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| test_challenge | real | 258 | 0.8843 | 0.7925 | 0.8400 | 0.7500 |
| test_challenge | synthetic | 100 | 0.4924 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | synthetic_hard_positive | 130 | 0.4942 | 0.9883 | 0.9769 | 1.0000 |
| test_mixed | external_curated | 50 | 0.4949 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | external_real | 50 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | paraphrased | 434 | 0.4977 | 0.9954 | 0.9908 | 1.0000 |
| test_mixed | real | 258 | 0.8503 | 0.7308 | 0.7600 | 0.7037 |
| test_mixed | synthetic | 201 | 0.4975 | 0.0000 | 0.0000 | 0.0000 |
| test_mixed | synthetic_hard_positive | 66 | 0.4884 | 0.9767 | 0.9545 | 1.0000 |
| test_real | real | 385 | 0.8052 | 0.6494 | 0.6757 | 0.6250 |

## 7. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.459504  |       0.845058 |         0.817623 |             0.743017 |
|       2 |    0.243714  |       0.914516 |         0.909254 |             0.942272 |
|       3 |    0.150572  |       0.953788 |         0.948177 |             0.919926 |
|       4 |    0.117994  |       0.956382 |         0.951196 |             0.925512 |
|       5 |    0.0955659 |       0.956797 |         0.953846 |             0.981378 |
|       6 |    0.0928846 |       0.956835 |         0.954178 |             0.988827 |
|       7 |    0.0721753 |       0.977026 |         0.974837 |             0.973929 |
|       8 |    0.0609562 |       0.97009  |         0.966635 |             0.944134 |
|       9 |    0.0652266 |       0.973614 |         0.971055 |             0.968343 |
|      10 |    0.0602948 |       0.976163 |         0.973832 |             0.970205 |
