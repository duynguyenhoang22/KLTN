# CafeBERT Teacher Report

## Configuration

- Hugging Face model: `uitnlp/CafeBERT`
- Seed: `42`
- Epochs: `3.0`
- Max length: `128`
- Train batch size: `16`
- Eval batch size: `32`
- Gradient accumulation: `1`
- Effective train batch size: `16`
- Temperature: `2.0`
- FP16: `True`
- BF16: `False`
- Elapsed seconds: `1566.81`

## Inputs

| split   | path                                                             |
|:--------|:-----------------------------------------------------------------|
| train   | /kaggle/input/datasets/duynguynhoang/vismish-benchmark/train.csv |
| dev     | /kaggle/input/datasets/duynguynhoang/vismish-benchmark/dev.csv   |
| test    | /kaggle/input/datasets/duynguynhoang/vismish-benchmark/test.csv  |

## Metrics

| split   |   rows |   macro_f1 |   f1_label_1 |   recall_label_1 |   precision_label_1 |   pr_auc |   tn |   fp |   fn |   tp |
|:--------|-------:|-----------:|-------------:|-----------------:|--------------------:|---------:|-----:|-----:|-----:|-----:|
| train   |   9492 |   0.994054 |     0.994578 |         0.993808 |            0.995349 | 0.99966  | 4300 |   24 |   32 | 5136 |
| dev     |    535 |   0.947201 |     0.901408 |         0.864865 |            0.941176 | 0.947743 |  496 |    2 |    5 |   32 |
| test    |    535 |   0.935477 |     0.88     |         0.891892 |            0.868421 | 0.926091 |  493 |    5 |    4 |   33 |

## Artifact

- Model: `/kaggle/working/cafebert_teacher/model`
- Teacher outputs: `/kaggle/working/cafebert_teacher/teacher_outputs`
- ZIP: `/kaggle/working/cafebert_teacher_artifacts.zip`
