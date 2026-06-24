# Focused TextCNN Distillation Study

- Seeds: `42, 123, 2025`
- Architecture and preprocessing are fixed across all modes.
- `hard`: hard-label training only.
- `vanilla_kd`: uniform teacher soft-target weight.
- `risk_aware_kd`: confidence-aware weight with teacher false-negative suppression.

## Mean ± SD across seeds

| split   | study_mode    | metric         | mean_sd         |      min |      max |
|:--------|:--------------|:---------------|:----------------|---------:|---------:|
| dev     | hard          | f1_label_1     | 0.8282 ± 0.0268 | 0.8      | 0.853333 |
| dev     | hard          | macro_f1       | 0.9074 ± 0.0147 | 0.891919 | 0.921139 |
| dev     | hard          | pr_auc         | 0.8707 ± 0.0289 | 0.848588 | 0.903327 |
| dev     | hard          | recall_label_1 | 0.8649 ± 0.0000 | 0.864865 | 0.864865 |
| dev     | risk_aware_kd | f1_label_1     | 0.8337 ± 0.0340 | 0.794521 | 0.853333 |
| dev     | risk_aware_kd | macro_f1       | 0.9107 ± 0.0181 | 0.889738 | 0.921139 |
| dev     | risk_aware_kd | pr_auc         | 0.8829 ± 0.0237 | 0.864165 | 0.909485 |
| dev     | risk_aware_kd | recall_label_1 | 0.8378 ± 0.0468 | 0.783784 | 0.864865 |
| dev     | vanilla_kd    | f1_label_1     | 0.8301 ± 0.0213 | 0.810811 | 0.852941 |
| dev     | vanilla_kd    | macro_f1       | 0.9089 ± 0.0117 | 0.898377 | 0.921481 |
| dev     | vanilla_kd    | pr_auc         | 0.8773 ± 0.0103 | 0.867204 | 0.887786 |
| dev     | vanilla_kd    | recall_label_1 | 0.8108 ± 0.0270 | 0.783784 | 0.837838 |
| test    | hard          | f1_label_1     | 0.7852 ± 0.0397 | 0.741573 | 0.819277 |
| test    | hard          | macro_f1       | 0.8835 ± 0.0221 | 0.859064 | 0.90204  |
| test    | hard          | pr_auc         | 0.8574 ± 0.0227 | 0.831813 | 0.875174 |
| test    | hard          | recall_label_1 | 0.8829 ± 0.0413 | 0.837838 | 0.918919 |
| test    | risk_aware_kd | f1_label_1     | 0.7542 ± 0.0545 | 0.692308 | 0.795181 |
| test    | risk_aware_kd | macro_f1       | 0.8671 ± 0.0291 | 0.834057 | 0.888978 |
| test    | risk_aware_kd | pr_auc         | 0.8483 ± 0.0410 | 0.801078 | 0.874356 |
| test    | risk_aware_kd | recall_label_1 | 0.8198 ± 0.0826 | 0.72973  | 0.891892 |
| test    | vanilla_kd    | f1_label_1     | 0.7583 ± 0.0144 | 0.75     | 0.775    |
| test    | vanilla_kd    | macro_f1       | 0.8698 ± 0.0075 | 0.864899 | 0.878409 |
| test    | vanilla_kd    | pr_auc         | 0.8443 ± 0.0197 | 0.825149 | 0.864422 |
| test    | vanilla_kd    | recall_label_1 | 0.7928 ± 0.0563 | 0.72973  | 0.837838 |
| train   | hard          | f1_label_1     | 0.9978 ± 0.0028 | 0.994502 | 0.999419 |
| train   | hard          | macro_f1       | 0.9976 ± 0.0031 | 0.993943 | 0.999363 |
| train   | hard          | pr_auc         | 1.0000 ± 0.0001 | 0.999877 | 0.999999 |
| train   | hard          | recall_label_1 | 0.9986 ± 0.0010 | 0.997485 | 0.999226 |
| train   | risk_aware_kd | f1_label_1     | 0.9978 ± 0.0027 | 0.994671 | 0.999419 |
| train   | risk_aware_kd | macro_f1       | 0.9976 ± 0.0030 | 0.994161 | 0.999363 |
| train   | risk_aware_kd | pr_auc         | 0.9999 ± 0.0001 | 0.999757 | 0.999997 |
| train   | risk_aware_kd | recall_label_1 | 0.9972 ± 0.0034 | 0.993228 | 0.999226 |
| train   | vanilla_kd    | f1_label_1     | 0.9976 ± 0.0006 | 0.996895 | 0.998161 |
| train   | vanilla_kd    | macro_f1       | 0.9974 ± 0.0007 | 0.996604 | 0.997982 |
| train   | vanilla_kd    | pr_auc         | 0.9999 ± 0.0000 | 0.999926 | 0.999948 |
| train   | vanilla_kd    | recall_label_1 | 0.9961 ± 0.0020 | 0.994002 | 0.997872 |

## Paired bootstrap difference versus hard-label

| split   | comparison           | metric         |   mean_delta |   ci95_low |   ci95_high | positive_seeds   |
|:--------|:---------------------|:---------------|-------------:|-----------:|------------:|:-----------------|
| dev     | vanilla_kd - hard    | macro_f1       |       0.0011 |    -0.0195 |      0.0193 | 2/3              |
| dev     | vanilla_kd - hard    | f1_label_1     |       0.0013 |    -0.0377 |      0.0355 | 2/3              |
| dev     | vanilla_kd - hard    | recall_label_1 |      -0.0538 |    -0.1002 |     -0.0167 | 0/3              |
| dev     | vanilla_kd - hard    | pr_auc         |       0.007  |    -0.0107 |      0.0264 | 2/3              |
| dev     | risk_aware_kd - hard | macro_f1       |       0.0035 |    -0.0131 |      0.0203 | 1/3              |
| dev     | risk_aware_kd - hard | f1_label_1     |       0.0059 |    -0.0251 |      0.0374 | 1/3              |
| dev     | risk_aware_kd - hard | recall_label_1 |      -0.0268 |    -0.0686 |      0.0098 | 0/3              |
| dev     | risk_aware_kd - hard | pr_auc         |       0.0123 |    -0.0012 |      0.028  | 3/3              |
| test    | vanilla_kd - hard    | macro_f1       |      -0.0138 |    -0.0357 |      0.0086 | 1/3              |
| test    | vanilla_kd - hard    | f1_label_1     |      -0.027  |    -0.0674 |      0.0145 | 1/3              |
| test    | vanilla_kd - hard    | recall_label_1 |      -0.0898 |    -0.1493 |     -0.0354 | 0/3              |
| test    | vanilla_kd - hard    | pr_auc         |      -0.0133 |    -0.0393 |      0.0123 | 0/3              |
| test    | risk_aware_kd - hard | macro_f1       |      -0.0165 |    -0.035  |     -0.0007 | 0/3              |
| test    | risk_aware_kd - hard | f1_label_1     |      -0.0314 |    -0.0658 |     -0.0017 | 0/3              |
| test    | risk_aware_kd - hard | recall_label_1 |      -0.0633 |    -0.1105 |     -0.0222 | 0/3              |
| test    | risk_aware_kd - hard | pr_auc         |      -0.0093 |    -0.0305 |      0.0112 | 1/3              |

A confidence interval containing zero is treated as insufficient evidence of a stable difference.
