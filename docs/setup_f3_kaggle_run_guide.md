# Huong dan chay Setup F3 tren Kaggle

## Muc tieu

Chay rieng bien the `F3_external_plus_synthetic_label0`:

```text
Real Train
+ Synthetic Label 1
+ Synthetic Label 0
+ external_real Label 0
+ external_curated Label 0
```

Ket qua F1-F2c da co trong `setup_results/setup_f_results/`, vi vay lan chay Kaggle nay chi can bo sung F3.

## File can upload len Kaggle Dataset

Tao mot Kaggle Dataset, vi du `kltn-tstr-data`, gom 2 file:

```text
data/final/vismishds_content_label_origin.csv
setup_results/setup_a_results/setup_a_real_test.csv
```

Ten file trong dataset phai giu dung:

```text
vismishds_content_label_origin.csv
setup_a_real_test.csv
```

Notebook se tu tim 2 file nay duoi `/kaggle/input`.

## Notebook can upload

Dung file:

```text
notebooks/setup_f3_kaggle_label0_source_augmentation_phobert.ipynb
```

Hoac copy noi dung tu script:

```text
notebooks/script_py/setup_f3_kaggle_label0_source_augmentation_phobert.py
```

## Cau hinh Kaggle

Trong Kaggle Notebook:

1. Add dataset vua tao vao notebook.
2. Bat accelerator GPU, uu tien T4/P100.
3. Bat Internet neu moi truong chua co package `transformers`, `datasets`, `pyvi`.
4. Run all.

## Co che chong mat ket qua

Notebook luu ket qua sau tung seed vao:

```text
/kaggle/working/setup_f3_results/setup_f3_per_seed_results.csv
```

Neu session bi ngat giua chung, chay lai notebook se skip seed da co trong file nay.

Sau khi tong hop, notebook tao:

```text
/kaggle/working/setup_f3_results/setup_f3_results.csv
/kaggle/working/setup_f3_results/setup_f3_confusion_matrix_F3_external_plus_synthetic_label0.png
/kaggle/working/setup_f3_results.zip
```

Tai file zip ve, roi giai nen/copy vao repo:

```text
setup_results/setup_f3_results/
```

Hoac gop hang F3 trong `setup_f3_results.csv` vao bang tong hop Setup F.

## Ket qua mong doi ve kich thuoc train

Neu dung dung dataset hien tai, F3 Train se xap xi:

```text
Real Train Label 0: 1624
Real Train Label 1: 172
Synthetic Label 0: 1998
external_real Label 0: 500
external_curated Label 0: 501
Synthetic Label 1: 4996

Tong Label 0: 4623
Tong Label 1: 5168
Tong train: 9791
```

## Luu y khi dien giai

F3 khong nen duoc doc rieng nhu mot setup toi uu diem Real Test. No la bien the kiem tra tac dong khi ket hop tat ca nguon mo rong Label 0. Khi so sanh, dat F3 canh:

```text
F1: synthetic Label 0 doi chung
F2b: external_curated Label 0
F2c: external_real + external_curated Label 0
```

Neu F3 kem F2b/F2c, co the ket luan viec tron them synthetic Label 0 vao external Label 0 khong tao loi ich tren Real Test hien tai.
