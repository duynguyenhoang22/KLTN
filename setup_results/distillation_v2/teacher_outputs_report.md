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
| train          |   7212 |     0.9978 |     0.9978 |       0.9979 |           0.9974 |              0.9984 |               0.9978 |            0.9989 |
| val            |   1186 |     0.9882 |     0.9881 |       0.987  |           0.987  |              0.987  |               0.9882 |            0.9972 |
| test_real      |    385 |     0.9636 |     0.8807 |       0.7812 |           0.6757 |              0.9259 |               0.9636 |            0.9954 |
| test_mixed     |   1059 |     0.9906 |     0.9906 |       0.9905 |           0.9886 |              0.9924 |               0.9906 |            0.997  |
| test_challenge |    720 |     0.9903 |     0.9899 |       0.9878 |           0.9861 |              0.9895 |               0.9903 |            0.9972 |

## Confusion Matrices

### train

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |     3350 |        6 |
| true_1 |       10 |     3846 |

### val

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      642 |        7 |
| true_1 |        7 |      530 |

### test_real

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      346 |        2 |
| true_1 |       12 |       25 |

### test_mixed

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      530 |        4 |
| true_1 |        6 |      519 |

### test_challenge

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      430 |        3 |
| true_1 |        4 |      283 |
