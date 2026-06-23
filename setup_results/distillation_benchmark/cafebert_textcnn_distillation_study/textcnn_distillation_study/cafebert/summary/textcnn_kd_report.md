# Focused TextCNN Distillation Study

- Seeds: `42, 123, 2025`
- Architecture and preprocessing are fixed across all modes.
- `hard`: hard-label training only.
- `vanilla_kd`: uniform teacher soft-target weight.
- `risk_aware_kd`: confidence-aware weight with teacher false-negative suppression.

## Mean ± SD across seeds

| split   | study_mode    | metric         | mean_sd         |      min |      max |
|:--------|:--------------|:---------------|:----------------|---------:|---------:|
| dev     | hard          | f1_label_1     | 0.8342 ± 0.0297 | 0.8      | 0.853333 |
| dev     | hard          | macro_f1       | 0.9107 ± 0.0163 | 0.891919 | 0.921139 |
| dev     | hard          | pr_auc         | 0.8783 ± 0.0287 | 0.848588 | 0.905781 |
| dev     | hard          | recall_label_1 | 0.8559 ± 0.0156 | 0.837838 | 0.864865 |
| dev     | risk_aware_kd | f1_label_1     | 0.8292 ± 0.0218 | 0.810811 | 0.853333 |
| dev     | risk_aware_kd | macro_f1       | 0.9084 ± 0.0116 | 0.898377 | 0.921139 |
| dev     | risk_aware_kd | pr_auc         | 0.8747 ± 0.0157 | 0.861564 | 0.892107 |
| dev     | risk_aware_kd | recall_label_1 | 0.8108 ± 0.0541 | 0.756757 | 0.864865 |
| dev     | vanilla_kd    | f1_label_1     | 0.8468 ± 0.0058 | 0.842105 | 0.853333 |
| dev     | vanilla_kd    | macro_f1       | 0.9177 ± 0.0031 | 0.915016 | 0.921139 |
| dev     | vanilla_kd    | pr_auc         | 0.8918 ± 0.0136 | 0.878254 | 0.90536  |
| dev     | vanilla_kd    | recall_label_1 | 0.8468 ± 0.0312 | 0.810811 | 0.864865 |
| test    | hard          | f1_label_1     | 0.7872 ± 0.0398 | 0.741573 | 0.814815 |
| test    | hard          | macro_f1       | 0.8846 ± 0.0223 | 0.859064 | 0.899824 |
| test    | hard          | pr_auc         | 0.8629 ± 0.0308 | 0.831813 | 0.893389 |
| test    | hard          | recall_label_1 | 0.8739 ± 0.0312 | 0.837838 | 0.891892 |
| test    | risk_aware_kd | f1_label_1     | 0.7670 ± 0.0534 | 0.705882 | 0.804878 |
| test    | risk_aware_kd | macro_f1       | 0.8746 ± 0.0277 | 0.842961 | 0.894342 |
| test    | risk_aware_kd | pr_auc         | 0.8335 ± 0.0354 | 0.796541 | 0.867222 |
| test    | risk_aware_kd | recall_label_1 | 0.8018 ± 0.1333 | 0.648649 | 0.891892 |
| test    | vanilla_kd    | f1_label_1     | 0.8218 ± 0.0147 | 0.804878 | 0.831169 |
| test    | vanilla_kd    | macro_f1       | 0.9036 ± 0.0081 | 0.894342 | 0.909039 |
| test    | vanilla_kd    | pr_auc         | 0.8701 ± 0.0131 | 0.855561 | 0.881121 |
| test    | vanilla_kd    | recall_label_1 | 0.8919 ± 0.0270 | 0.864865 | 0.918919 |
| train   | hard          | f1_label_1     | 0.9978 ± 0.0029 | 0.994502 | 0.999613 |
| train   | hard          | macro_f1       | 0.9976 ± 0.0032 | 0.993943 | 0.999575 |
| train   | hard          | pr_auc         | 1.0000 ± 0.0001 | 0.999877 | 0.999999 |
| train   | hard          | recall_label_1 | 0.9988 ± 0.0011 | 0.997485 | 0.999613 |
| train   | risk_aware_kd | f1_label_1     | 0.9964 ± 0.0039 | 0.991917 | 0.998645 |
| train   | risk_aware_kd | macro_f1       | 0.9960 ± 0.0042 | 0.991197 | 0.998513 |
| train   | risk_aware_kd | pr_auc         | 0.9998 ± 0.0002 | 0.999584 | 0.999986 |
| train   | risk_aware_kd | recall_label_1 | 0.9941 ± 0.0074 | 0.985488 | 0.998452 |
| train   | vanilla_kd    | f1_label_1     | 0.9989 ± 0.0008 | 0.997968 | 0.999419 |
| train   | vanilla_kd    | macro_f1       | 0.9988 ± 0.0009 | 0.99777  | 0.999363 |
| train   | vanilla_kd    | pr_auc         | 1.0000 ± 0.0000 | 0.999981 | 0.999998 |
| train   | vanilla_kd    | recall_label_1 | 0.9985 ± 0.0007 | 0.997678 | 0.998839 |

## Paired bootstrap difference versus hard-label

| split   | comparison           | metric         |   mean_delta |   ci95_low |   ci95_high | positive_seeds   |
|:--------|:---------------------|:---------------|-------------:|-----------:|------------:|:-----------------|
| dev     | vanilla_kd - hard    | macro_f1       |       0.0068 |    -0.0086 |      0.0221 | 1/3              |
| dev     | vanilla_kd - hard    | f1_label_1     |       0.0123 |    -0.0163 |      0.0408 | 1/3              |
| dev     | vanilla_kd - hard    | recall_label_1 |      -0.0089 |    -0.0417 |      0.0201 | 1/3              |
| dev     | vanilla_kd - hard    | pr_auc         |       0.0133 |    -0.0057 |      0.0351 | 2/3              |
| dev     | risk_aware_kd - hard | macro_f1       |      -0.0023 |    -0.0226 |      0.0165 | 2/3              |
| dev     | risk_aware_kd - hard | f1_label_1     |      -0.005  |    -0.0428 |      0.0302 | 2/3              |
| dev     | risk_aware_kd - hard | recall_label_1 |      -0.0451 |    -0.0934 |     -0.0023 | 1/3              |
| dev     | risk_aware_kd - hard | pr_auc         |      -0.0035 |    -0.0266 |      0.0201 | 2/3              |
| test    | vanilla_kd - hard    | macro_f1       |       0.0192 |    -0.0028 |      0.042  | 2/3              |
| test    | vanilla_kd - hard    | f1_label_1     |       0.0349 |    -0.0052 |      0.0774 | 2/3              |
| test    | vanilla_kd - hard    | recall_label_1 |       0.0185 |    -0.0378 |      0.0761 | 2/3              |
| test    | vanilla_kd - hard    | pr_auc         |       0.0071 |    -0.021  |      0.0351 | 2/3              |
| test    | risk_aware_kd - hard | macro_f1       |      -0.0103 |    -0.0357 |      0.0137 | 1/3              |
| test    | risk_aware_kd - hard | f1_label_1     |      -0.0208 |    -0.0687 |      0.0237 | 1/3              |
| test    | risk_aware_kd - hard | recall_label_1 |      -0.0723 |    -0.1339 |     -0.0125 | 1/3              |
| test    | risk_aware_kd - hard | pr_auc         |      -0.0283 |    -0.0611 |      0.0006 | 1/3              |

A confidence interval containing zero is treated as insufficient evidence of a stable difference.
