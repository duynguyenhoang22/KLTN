# Teacher Output Generation Report

## Output Files

| split          | path                                                                    |
|:---------------|:------------------------------------------------------------------------|
| train          | /kaggle/working/distillation_teacher_outputs/train_teacher.csv          |
| val            | /kaggle/working/distillation_teacher_outputs/val_teacher.csv            |
| test_real      | /kaggle/working/distillation_teacher_outputs/test_real_teacher.csv      |
| test_mixed     | /kaggle/working/distillation_teacher_outputs/test_mixed_teacher.csv     |
| test_challenge | /kaggle/working/distillation_teacher_outputs/test_challenge_teacher.csv |

## Metrics Summary

| split          |   rows |   accuracy |   macro_f1 |   f1_label_1 |   recall_label_1 |   precision_label_1 |   teacher_agree_rate |   mean_confidence |
|:---------------|-------:|-----------:|-----------:|-------------:|-----------------:|--------------------:|---------------------:|------------------:|
| train          |   8026 |     0.9986 |     0.9986 |       0.9987 |           0.9978 |              0.9995 |               0.9986 |            0.9992 |
| val            |   1186 |     0.9848 |     0.9847 |       0.9832 |           0.9814 |              0.985  |               0.9848 |            0.9983 |
| test_real      |    385 |     0.9662 |     0.9083 |       0.8354 |           0.8919 |              0.7857 |               0.9662 |            0.9944 |
| test_mixed     |    635 |     0.9937 |     0.9927 |       0.9954 |           0.9977 |              0.9931 |               0.9937 |            0.9981 |
| test_challenge |    330 |     1      |     1      |       1      |           1      |              1      |               1      |            0.9971 |

## Confusion Matrices

### train

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |     3920 |        2 |
| true_1 |        9 |     4095 |

### val

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      641 |        8 |
| true_1 |       10 |      527 |

### test_real

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      339 |        9 |
| true_1 |        4 |       33 |

### test_mixed

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      198 |        3 |
| true_1 |        1 |      433 |

### test_challenge

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      200 |        0 |
| true_1 |        0 |      130 |
