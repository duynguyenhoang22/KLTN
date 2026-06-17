# g2_textcnn_hard Report

## 1. Scope

- Architecture: `textcnn`
- Mode: `hard`
- Setup: `G2_external_curated` robustness check
- Input features: `content` only

## 2. Metrics by Split

| split | rows | accuracy | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| train | 7142 | 0.9961 | 0.9951 | 0.9973 | 0.9952 | 0.9994 | 0.9999 | 1.0000 |
| val | 535 | 0.9645 | 0.8702 | 0.7595 | 0.8108 | 0.7143 | 0.9725 | 0.8310 |
| test_challenge | 537 | 0.9758 | 0.9068 | 0.8267 | 0.8378 | 0.8158 | 0.9814 | 0.8798 |

## 4. Confusion Matrices

### train

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 1971 | 3 |
| true_1 | 25 | 5143 |

### val

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 486 | 12 |
| true_1 | 7 | 30 |

### test_challenge

| | pred_0 | pred_1 |
|---|---:|---:|
| true_0 | 493 | 7 |
| true_1 | 6 | 31 |

## 5. Metrics by Data Origin

| split | data_origin | rows | macro_f1 | f1_label_1 | recall_label_1 | precision_label_1 |
| --- | --- | --- | --- | --- | --- | --- |
| test_challenge | external_curated | 76 | 0.4933 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | external_real | 75 | 1.0000 | 0.0000 | 0.0000 | 0.0000 |
| test_challenge | real | 386 | 0.9168 | 0.8493 | 0.8378 | 0.8611 |
| train | external_curated | 350 | 0.4993 | 0.0000 | 0.0000 | 0.0000 |
| train | paraphrased | 4333 | 0.4997 | 0.9994 | 0.9988 | 1.0000 |
| train | real | 1796 | 0.9629 | 0.9325 | 0.8837 | 0.9870 |
| train | synthetic | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| train | synthetic_hard_positive | 653 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| val | external_curated | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| val | external_real | 75 | 0.4966 | 0.0000 | 0.0000 | 0.0000 |
| val | real | 385 | 0.8773 | 0.7792 | 0.8108 | 0.7500 |

## 6. Training History

|   epoch |   train_loss |   val_macro_f1 |   val_f1_label_1 |   val_recall_label_1 |
|--------:|-------------:|---------------:|-----------------:|---------------------:|
|       1 |    0.155211  |       0.817191 |         0.65625  |             0.567568 |
|       2 |    0.0412223 |       0.845403 |         0.717391 |             0.891892 |
|       3 |    0.0269932 |       0.870161 |         0.759494 |             0.810811 |
|       4 |    0.0220096 |       0.869342 |         0.756757 |             0.756757 |
|       5 |    0.0151954 |       0.863798 |         0.75     |             0.891892 |
|       6 |    0.0124517 |       0.83672  |         0.702128 |             0.891892 |
