# Focused TextCNN Distillation Study

- Seeds: `42, 123, 2025`
- Architecture and preprocessing are fixed across all modes.
- `hard`: hard-label training only.
- `vanilla_kd`: uniform teacher soft-target weight.
- `risk_aware_kd`: confidence-aware weight with teacher false-negative suppression.

## Mean ± SD across seeds

| split   | study_mode    | metric         | mean_sd         |      min |      max |
|:--------|:--------------|:---------------|:----------------|---------:|---------:|
| dev     | hard          | f1_label_1     | 0.8532 ± 0.0207 | 0.837838 | 0.876712 |
| dev     | hard          | macro_f1       | 0.9213 ± 0.0111 | 0.912895 | 0.933843 |
| dev     | hard          | pr_auc         | 0.8772 ± 0.0356 | 0.852876 | 0.918118 |
| dev     | hard          | recall_label_1 | 0.8378 ± 0.0270 | 0.810811 | 0.864865 |
| dev     | risk_aware_kd | f1_label_1     | 0.8514 ± 0.0275 | 0.833333 | 0.883117 |
| dev     | risk_aware_kd | macro_f1       | 0.9202 ± 0.0146 | 0.910655 | 0.937027 |
| dev     | risk_aware_kd | pr_auc         | 0.8896 ± 0.0135 | 0.881807 | 0.90514  |
| dev     | risk_aware_kd | recall_label_1 | 0.8559 ± 0.0563 | 0.810811 | 0.918919 |
| dev     | vanilla_kd    | f1_label_1     | 0.8411 ± 0.0213 | 0.816901 | 0.857143 |
| dev     | vanilla_kd    | macro_f1       | 0.9147 ± 0.0112 | 0.901944 | 0.923033 |
| dev     | vanilla_kd    | pr_auc         | 0.8710 ± 0.0324 | 0.850792 | 0.908435 |
| dev     | vanilla_kd    | recall_label_1 | 0.8378 ± 0.0541 | 0.783784 | 0.891892 |
| test    | hard          | f1_label_1     | 0.7949 ± 0.0374 | 0.769231 | 0.837838 |
| test    | hard          | macro_f1       | 0.8898 ± 0.0202 | 0.875543 | 0.912895 |
| test    | hard          | pr_auc         | 0.8706 ± 0.0145 | 0.856207 | 0.885241 |
| test    | hard          | recall_label_1 | 0.8018 ± 0.0413 | 0.756757 | 0.837838 |
| test    | risk_aware_kd | f1_label_1     | 0.8276 ± 0.0332 | 0.789474 | 0.85     |
| test    | risk_aware_kd | macro_f1       | 0.9069 ± 0.0176 | 0.886689 | 0.918939 |
| test    | risk_aware_kd | pr_auc         | 0.8791 ± 0.0287 | 0.851201 | 0.908633 |
| test    | risk_aware_kd | recall_label_1 | 0.8919 ± 0.0715 | 0.810811 | 0.945946 |
| test    | vanilla_kd    | f1_label_1     | 0.7726 ± 0.0058 | 0.769231 | 0.779221 |
| test    | vanilla_kd    | macro_f1       | 0.8774 ± 0.0032 | 0.875543 | 0.88105  |
| test    | vanilla_kd    | pr_auc         | 0.8789 ± 0.0195 | 0.858005 | 0.896646 |
| test    | vanilla_kd    | recall_label_1 | 0.8108 ± 0.0000 | 0.810811 | 0.810811 |
| train   | hard          | f1_label_1     | 0.9994 ± 0.0004 | 0.998935 | 0.99971  |
| train   | hard          | macro_f1       | 0.9993 ± 0.0004 | 0.998832 | 0.999681 |
| train   | hard          | pr_auc         | 1.0000 ± 0.0000 | 0.999997 | 1        |
| train   | hard          | recall_label_1 | 0.9990 ± 0.0005 | 0.998646 | 0.999613 |
| train   | risk_aware_kd | f1_label_1     | 0.9993 ± 0.0006 | 0.998548 | 0.999613 |
| train   | risk_aware_kd | macro_f1       | 0.9992 ± 0.0007 | 0.998407 | 0.999575 |
| train   | risk_aware_kd | pr_auc         | 1.0000 ± 0.0000 | 0.999985 | 1        |
| train   | risk_aware_kd | recall_label_1 | 0.9989 ± 0.0009 | 0.997872 | 0.99942  |
| train   | vanilla_kd    | f1_label_1     | 0.9989 ± 0.0005 | 0.998548 | 0.999516 |
| train   | vanilla_kd    | macro_f1       | 0.9988 ± 0.0006 | 0.998407 | 0.999469 |
| train   | vanilla_kd    | pr_auc         | 1.0000 ± 0.0000 | 0.999979 | 0.999999 |
| train   | vanilla_kd    | recall_label_1 | 0.9983 ± 0.0008 | 0.997678 | 0.999226 |

## Paired bootstrap difference versus hard-label

| split   | comparison           | metric         |   mean_delta |   ci95_low |   ci95_high | positive_seeds   |
|:--------|:---------------------|:---------------|-------------:|-----------:|------------:|:-----------------|
| dev     | vanilla_kd - hard    | macro_f1       |      -0.0064 |    -0.0216 |      0.0067 | 1/3              |
| dev     | vanilla_kd - hard    | f1_label_1     |      -0.0119 |    -0.0402 |      0.0127 | 1/3              |
| dev     | vanilla_kd - hard    | recall_label_1 |       0.0004 |    -0.0241 |      0.0278 | 1/3              |
| dev     | vanilla_kd - hard    | pr_auc         |      -0.0062 |    -0.0254 |      0.0141 | 0/3              |
| dev     | risk_aware_kd - hard | macro_f1       |      -0.0014 |    -0.0174 |      0.0146 | 1/3              |
| dev     | risk_aware_kd - hard | f1_label_1     |      -0.0024 |    -0.0318 |      0.0274 | 1/3              |
| dev     | risk_aware_kd - hard | recall_label_1 |       0.0171 |    -0.0155 |      0.0541 | 2/3              |
| dev     | risk_aware_kd - hard | pr_auc         |       0.0125 |    -0.0056 |      0.0334 | 2/3              |
| test    | vanilla_kd - hard    | macro_f1       |      -0.0124 |    -0.0343 |      0.0096 | 1/3              |
| test    | vanilla_kd - hard    | f1_label_1     |      -0.0225 |    -0.0639 |      0.0183 | 1/3              |
| test    | vanilla_kd - hard    | recall_label_1 |       0.0093 |    -0.0465 |      0.0604 | 1/3              |
| test    | vanilla_kd - hard    | pr_auc         |       0.0081 |    -0.011  |      0.0283 | 2/3              |
| test    | risk_aware_kd - hard | macro_f1       |       0.0172 |    -0.0062 |      0.041  | 3/3              |
| test    | risk_aware_kd - hard | f1_label_1     |       0.0328 |    -0.0106 |      0.0776 | 3/3              |
| test    | risk_aware_kd - hard | recall_label_1 |       0.09   |     0.0357 |      0.1476 | 2/3              |
| test    | risk_aware_kd - hard | pr_auc         |       0.0083 |    -0.0126 |      0.029  | 1/3              |

A confidence interval containing zero is treated as insufficient evidence of a stable difference.
