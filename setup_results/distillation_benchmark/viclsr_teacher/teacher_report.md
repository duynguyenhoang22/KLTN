# ViCLSR Teacher Report

## Configuration

- Hugging Face model: `huynhtin/ViCLSR`
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
- Elapsed seconds: `1617.03`

## Inputs

| split   | path                                                             |
|:--------|:-----------------------------------------------------------------|
| train   | /kaggle/input/datasets/duynguynhoang/vismish-benchmark/train.csv |
| dev     | /kaggle/input/datasets/duynguynhoang/vismish-benchmark/dev.csv   |
| test    | /kaggle/input/datasets/duynguynhoang/vismish-benchmark/test.csv  |

## Metrics

| split   |   rows |   macro_f1 |   f1_label_1 |   recall_label_1 |   precision_label_1 |   pr_auc |   tn |   fp |   fn |   tp |
|:--------|-------:|-----------:|-------------:|-----------------:|--------------------:|---------:|-----:|-----:|-----:|-----:|
| train   |   9492 |   0.998195 |     0.998354 |         0.997291 |            0.999418 | 0.99996  | 4321 |    3 |   14 | 5154 |
| dev     |    535 |   0.921139 |     0.853333 |         0.864865 |            0.842105 | 0.902818 |  492 |    6 |    5 |   32 |
| test    |    535 |   0.921139 |     0.853333 |         0.864865 |            0.842105 | 0.901995 |  492 |    6 |    5 |   32 |

## Artifact

- Model: `/kaggle/working/viclsr_teacher/model`
- Teacher outputs: `/kaggle/working/viclsr_teacher/teacher_outputs`
- ZIP: `/kaggle/working/viclsr_teacher_artifacts.zip`
