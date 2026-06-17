# PhoBERT-base Teacher Fine-tuning Report

## Configuration

- Model: `vinai/phobert-base`
- Train CSV: `/kaggle/input/datasets/duynguynhoang/distillation-dataset/train.csv`
- Val CSV: `/kaggle/input/datasets/duynguynhoang/distillation-dataset/val.csv`
- Seed: `42`
- Max length: `128`
- Epochs: `3`
- Train batch size: `16`
- Eval batch size: `32`
- Gradient accumulation steps: `1`
- Learning rate: `2e-05`
- Weight decay: `0.01`
- Warmup ratio: `0.1`
- FP16: `True`
- Elapsed seconds: `377.13`

## Validation Metrics

| metric            |    value |
|:------------------|---------:|
| accuracy          | 0.984823 |
| macro_f1          | 0.984681 |
| weighted_f1       | 0.98482  |
| precision_label_1 | 0.985047 |
| recall_label_1    | 0.981378 |
| f1_label_1        | 0.983209 |
| precision_label_0 | 0.984639 |
| recall_label_0    | 0.987673 |
| f1_label_0        | 0.986154 |
| roc_auc           | 0.999296 |
| pr_auc            | 0.999132 |

## Confusion Matrix

`labels=[0, 1]`, rows are true labels and columns are predicted labels.

|        |   pred_0 |   pred_1 |
|:-------|---------:|---------:|
| true_0 |      641 |        8 |
| true_1 |       10 |      527 |

## Train Distribution

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       1 |    4104 |     51.13 |
|       0 |    3922 |     48.87 |

### Data Origin

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |    3465 |     43.17 |
| real                    |    1797 |     22.39 |
| synthetic               |    1606 |     20.01 |
| synthetic_hard_positive |     457 |      5.69 |
| external_curated        |     351 |      4.37 |
| external_real           |     350 |      4.36 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     898 |     11.19 |
| Khác                       |     585 |      7.29 |
| Tuyển dụng giả             |     555 |      6.92 |
| Cờ bạc / Betting           |     531 |      6.62 |
| BHXH / Trợ cấp giả         |     524 |      6.53 |
| Crypto / Đầu tư giả        |     511 |      6.37 |
| Nội dung nhạy cảm          |     506 |      6.3  |
| Tin nhắn cá nhân và OTP    |     494 |      6.15 |
| Dịch vụ công giả           |     449 |      5.59 |
| Giả mạo ngân hàng          |     407 |      5.07 |
| Đòi nợ / Đe dọa            |     391 |      4.87 |
| P2P hard negative          |     351 |      4.37 |
| P2P hội thoại thông thường |     350 |      4.36 |
| Ngân hàng thật             |     332 |      4.14 |
| Quảng cáo hợp lệ           |     276 |      3.44 |
| Dịch vụ công thật          |     273 |      3.4  |
| Vận chuyển                 |     224 |      2.79 |
| Thương mại điện tử         |     203 |      2.53 |
| Dịch vụ y tế               |     166 |      2.07 |

### Label x Data Origin

| data_origin             |    0 |    1 |
|:------------------------|-----:|-----:|
| external_curated        |  351 |    0 |
| external_real           |  350 |    0 |
| paraphrased             |    0 | 3465 |
| real                    | 1625 |  172 |
| synthetic               | 1596 |   10 |
| synthetic_hard_positive |    0 |  457 |

## Validation Distribution

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     649 |     54.72 |
|       1 |     537 |     45.28 |

### Data Origin

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |     434 |     36.59 |
| real                    |     385 |     32.46 |
| synthetic               |     201 |     16.95 |
| synthetic_hard_positive |      66 |      5.56 |
| external_real           |      50 |      4.22 |
| external_curated        |      50 |      4.22 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     179 |     15.09 |
| Khác                       |     111 |      9.36 |
| Tin nhắn cá nhân và OTP    |      80 |      6.75 |
| Tuyển dụng giả             |      73 |      6.16 |
| Cờ bạc / Betting           |      70 |      5.9  |
| BHXH / Trợ cấp giả         |      67 |      5.65 |
| Nội dung nhạy cảm          |      64 |      5.4  |
| Crypto / Đầu tư giả        |      63 |      5.31 |
| Dịch vụ công giả           |      57 |      4.81 |
| Giả mạo ngân hàng          |      57 |      4.81 |
| Đòi nợ / Đe dọa            |      51 |      4.3  |
| Ngân hàng thật             |      50 |      4.22 |
| P2P hội thoại thông thường |      50 |      4.22 |
| P2P hard negative          |      50 |      4.22 |
| Dịch vụ công thật          |      46 |      3.88 |
| Quảng cáo hợp lệ           |      43 |      3.63 |
| Vận chuyển                 |      29 |      2.45 |
| Thương mại điện tử         |      25 |      2.11 |
| Dịch vụ y tế               |      21 |      1.77 |

### Label x Data Origin

| data_origin             |   0 |   1 |
|:------------------------|----:|----:|
| external_curated        |  50 |   0 |
| external_real           |  50 |   0 |
| paraphrased             |   0 | 434 |
| real                    | 348 |  37 |
| synthetic               | 201 |   0 |
| synthetic_hard_positive |   0 |  66 |
