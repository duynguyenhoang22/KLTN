# Distillation Benchmark Split Report

## Policy

- Input file: `model/base/temp.csv`
- Seed: `42`
- Real-like origins `real`, `external_real`, `external_curated`: stratified 70/15/15.
- Train-only origins `synthetic`, `paraphrased`, `synthetic_hard_positive`: 100% train.
- Stratum key: `label x data_origin x category`.

## Split Sizes

| split   |   rows |   percent |
|:--------|-------:|----------:|
| train   |   9492 |     89.87 |
| dev     |    535 |      5.07 |
| test    |    535 |      5.07 |

## Content Overlap

| left_split   | right_split   |   content_overlap |
|:-------------|:--------------|------------------:|
| train        | dev           |                 0 |
| train        | test          |                 0 |
| dev          | test          |                 0 |

## Sample ID Overlap

| left_split   | right_split   |   sample_id_overlap |
|:-------------|:--------------|--------------------:|
| train        | dev           |                   0 |
| train        | test          |                   0 |
| dev          | test          |                   0 |

## Strata Summary

|   label | data_origin             | category                   |    n |   train |   dev |   test | rule              |
|--------:|:------------------------|:---------------------------|-----:|--------:|------:|-------:|:------------------|
|       0 | external_curated        | P2P hard negative          |  501 |     351 |    75 |     75 | real_70_15_15     |
|       0 | external_real           | P2P hội thoại thông thường |  500 |     350 |    75 |     75 | real_70_15_15     |
|       1 | paraphrased             | BHXH / Trợ cấp giả         |  587 |     587 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Crypto / Đầu tư giả        |  625 |     625 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Cờ bạc / Betting           |  618 |     618 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Dịch vụ công giả           |  474 |     474 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Giả mạo ngân hàng          |  386 |     386 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Nội dung nhạy cảm          |  621 |     621 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Tuyển dụng giả             |  595 |     595 |     0 |      0 | train_only_origin |
|       1 | paraphrased             | Đòi nợ / Đe dọa            |  427 |     427 |     0 |      0 | train_only_origin |
|       0 | real                    | Dịch vụ công thật          |  170 |     118 |    26 |     26 | real_70_15_15     |
|       0 | real                    | Dịch vụ y tế               |    2 |       2 |     0 |      0 | small_all_train   |
|       0 | real                    | Khác                       |  507 |     355 |    76 |     76 | real_70_15_15     |
|       0 | real                    | Ngân hàng thật             |  126 |      88 |    19 |     19 | real_70_15_15     |
|       0 | real                    | Quảng cáo hợp lệ           |  136 |      96 |    20 |     20 | real_70_15_15     |
|       0 | real                    | Thương mại điện tử         |    1 |       1 |     0 |      0 | small_all_train   |
|       0 | real                    | Tin nhắn cá nhân và OTP    |  301 |     211 |    45 |     45 | real_70_15_15     |
|       0 | real                    | Viễn thông                 | 1060 |     742 |   159 |    159 | real_70_15_15     |
|       0 | real                    | Vận chuyển                 |   18 |      12 |     3 |      3 | real_70_15_15     |
|       1 | real                    | BHXH / Trợ cấp giả         |   15 |      11 |     2 |      2 | real_70_15_15     |
|       1 | real                    | Crypto / Đầu tư giả        |    2 |       2 |     0 |      0 | small_all_train   |
|       1 | real                    | Cờ bạc / Betting           |   53 |      37 |     8 |      8 | real_70_15_15     |
|       1 | real                    | Dịch vụ công giả           |   16 |      12 |     2 |      2 | real_70_15_15     |
|       1 | real                    | Giả mạo ngân hàng          |   65 |      45 |    10 |     10 | real_70_15_15     |
|       1 | real                    | Khác                       |   46 |      32 |     7 |      7 | real_70_15_15     |
|       1 | real                    | Nội dung nhạy cảm          |   10 |       6 |     2 |      2 | real_70_15_15     |
|       1 | real                    | Tuyển dụng giả             |   27 |      19 |     4 |      4 | real_70_15_15     |
|       1 | real                    | Đòi nợ / Đe dọa            |   12 |       8 |     2 |      2 | real_70_15_15     |
|       0 | synthetic               | Dịch vụ công thật          |  195 |     195 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Dịch vụ y tế               |  206 |     206 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Ngân hàng thật             |  306 |     306 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Quảng cáo hợp lệ           |  226 |     226 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Thương mại điện tử         |  252 |     252 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Tin nhắn cá nhân và OTP    |  353 |     353 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Viễn thông                 |  196 |     196 |     0 |      0 | train_only_origin |
|       0 | synthetic               | Vận chuyển                 |  264 |     264 |     0 |      0 | train_only_origin |
|       1 | synthetic               | BHXH / Trợ cấp giả         |    2 |       2 |     0 |      0 | train_only_origin |
|       1 | synthetic               | Dịch vụ công giả           |    2 |       2 |     0 |      0 | train_only_origin |
|       1 | synthetic               | Giả mạo ngân hàng          |    1 |       1 |     0 |      0 | train_only_origin |
|       1 | synthetic               | Nội dung nhạy cảm          |    3 |       3 |     0 |      0 | train_only_origin |
|       1 | synthetic               | Tuyển dụng giả             |    1 |       1 |     0 |      0 | train_only_origin |
|       1 | synthetic               | Đòi nợ / Đe dọa            |    1 |       1 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | BHXH / Trợ cấp giả         |   60 |      60 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | Crypto / Đầu tư giả        |   11 |      11 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | Dịch vụ công giả           |   79 |      79 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | Giả mạo ngân hàng          |   76 |      76 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | Khác                       |  282 |     282 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | Tuyển dụng giả             |   86 |      86 |     0 |      0 | train_only_origin |
|       1 | synthetic_hard_positive | Đòi nợ / Đe dọa            |   59 |      59 |     0 |      0 | train_only_origin |

## Split Detail: `train`

Rows: `9492`

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       1 |    5168 |     54.45 |
|       0 |    4324 |     45.55 |

### Data Origin

| data_origin             |   count |   percent |
|:------------------------|--------:|----------:|
| paraphrased             |    4333 |     45.65 |
| synthetic               |    2008 |     21.15 |
| real                    |    1797 |     18.93 |
| synthetic_hard_positive |     653 |      6.88 |
| external_curated        |     351 |      3.7  |
| external_real           |     350 |      3.69 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     938 |      9.88 |
| Tuyển dụng giả             |     701 |      7.39 |
| Khác                       |     669 |      7.05 |
| BHXH / Trợ cấp giả         |     660 |      6.95 |
| Cờ bạc / Betting           |     655 |      6.9  |
| Crypto / Đầu tư giả        |     638 |      6.72 |
| Nội dung nhạy cảm          |     630 |      6.64 |
| Dịch vụ công giả           |     567 |      5.97 |
| Tin nhắn cá nhân và OTP    |     564 |      5.94 |
| Giả mạo ngân hàng          |     508 |      5.35 |
| Đòi nợ / Đe dọa            |     495 |      5.21 |
| Ngân hàng thật             |     394 |      4.15 |
| P2P hard negative          |     351 |      3.7  |
| P2P hội thoại thông thường |     350 |      3.69 |
| Quảng cáo hợp lệ           |     322 |      3.39 |
| Dịch vụ công thật          |     313 |      3.3  |
| Vận chuyển                 |     276 |      2.91 |
| Thương mại điện tử         |     253 |      2.67 |
| Dịch vụ y tế               |     208 |      2.19 |

### Label x Data Origin

| data_origin             |    0 |    1 |
|:------------------------|-----:|-----:|
| external_curated        |  351 |    0 |
| external_real           |  350 |    0 |
| paraphrased             |    0 | 4333 |
| real                    | 1625 |  172 |
| synthetic               | 1998 |   10 |
| synthetic_hard_positive |    0 |  653 |

## Split Detail: `dev`

Rows: `535`

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     498 |     93.08 |
|       1 |      37 |      6.92 |

### Data Origin

| data_origin      |   count |   percent |
|:-----------------|--------:|----------:|
| real             |     385 |     71.96 |
| external_real    |      75 |     14.02 |
| external_curated |      75 |     14.02 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     159 |     29.72 |
| Khác                       |      83 |     15.51 |
| P2P hội thoại thông thường |      75 |     14.02 |
| P2P hard negative          |      75 |     14.02 |
| Tin nhắn cá nhân và OTP    |      45 |      8.41 |
| Dịch vụ công thật          |      26 |      4.86 |
| Quảng cáo hợp lệ           |      20 |      3.74 |
| Ngân hàng thật             |      19 |      3.55 |
| Giả mạo ngân hàng          |      10 |      1.87 |
| Cờ bạc / Betting           |       8 |      1.5  |
| Tuyển dụng giả             |       4 |      0.75 |
| Vận chuyển                 |       3 |      0.56 |
| BHXH / Trợ cấp giả         |       2 |      0.37 |
| Đòi nợ / Đe dọa            |       2 |      0.37 |
| Dịch vụ công giả           |       2 |      0.37 |
| Nội dung nhạy cảm          |       2 |      0.37 |

### Label x Data Origin

| data_origin      |   0 |   1 |
|:-----------------|----:|----:|
| external_curated |  75 |   0 |
| external_real    |  75 |   0 |
| real             | 348 |  37 |

## Split Detail: `test`

Rows: `535`

### Label

|   label |   count |   percent |
|--------:|--------:|----------:|
|       0 |     498 |     93.08 |
|       1 |      37 |      6.92 |

### Data Origin

| data_origin      |   count |   percent |
|:-----------------|--------:|----------:|
| real             |     385 |     71.96 |
| external_curated |      75 |     14.02 |
| external_real    |      75 |     14.02 |

### Category

| category                   |   count |   percent |
|:---------------------------|--------:|----------:|
| Viễn thông                 |     159 |     29.72 |
| Khác                       |      83 |     15.51 |
| P2P hard negative          |      75 |     14.02 |
| P2P hội thoại thông thường |      75 |     14.02 |
| Tin nhắn cá nhân và OTP    |      45 |      8.41 |
| Dịch vụ công thật          |      26 |      4.86 |
| Quảng cáo hợp lệ           |      20 |      3.74 |
| Ngân hàng thật             |      19 |      3.55 |
| Giả mạo ngân hàng          |      10 |      1.87 |
| Cờ bạc / Betting           |       8 |      1.5  |
| Tuyển dụng giả             |       4 |      0.75 |
| Vận chuyển                 |       3 |      0.56 |
| Nội dung nhạy cảm          |       2 |      0.37 |
| Đòi nợ / Đe dọa            |       2 |      0.37 |
| BHXH / Trợ cấp giả         |       2 |      0.37 |
| Dịch vụ công giả           |       2 |      0.37 |

### Label x Data Origin

| data_origin      |   0 |   1 |
|:-----------------|----:|----:|
| external_curated |  75 |   0 |
| external_real    |  75 |   0 |
| real             | 348 |  37 |
