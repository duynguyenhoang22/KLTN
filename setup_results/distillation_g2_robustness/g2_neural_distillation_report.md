# G2-style Neural Distillation Robustness Report

> Pham vi: Thu nghiem rieng sau distillation POC chinh, dung split/data setup gan voi `G2_external_curated`.
>
> Models: Character-level BiLSTM va Character-level TextCNN.
>
> Muc tieu: Kiem tra xem distilled neural students co con giu loi ich khi chuyen sang setup train/val/test theo Setup G2 hay khong.

---

## 1. Luu y ve thiet lap

Day la **robustness check rieng**, khong thay the POC split v2.

Train/val/test:

```text
Train: setup_results/setup_g_results/setup_g_train_G2_external_curated.csv
Val:   setup_results/setup_g_results/setup_g_challenge_val.csv
Test:  setup_results/setup_g_results/setup_g_challenge_test.csv
```

Soft labels:

```text
data/distillation/teacher_outputs_v2/
```

Soft labels duoc join vao G2 files bang exact `content`. Coverage la 100% cho ca train, val va test.

Dieu can dien giai ro:

```text
Day la G2-style split robustness check dung teacher outputs v2 da co.
Chua phai la thiet lap retrain teacher rieng theo G2.
```

---

## 2. Ket luan chinh

Ket qua G2-style robustness check cho thay:

```text
BiLSTM:
  Distillation khong cai thien hard-label baseline tren test_challenge.

TextCNN:
  Distillation cai thien ro TextCNN hard-label baseline tren val va test_challenge.
```

Ket qua quan trong nhat tren `test_challenge`:

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| BiLSTM hard-label | 0.8398 | 0.6984 | 0.5946 | 0.8462 | 0.7301 |
| BiLSTM distilled | 0.8172 | 0.6562 | 0.5676 | 0.7778 | 0.7454 |
| TextCNN hard-label | 0.9068 | 0.8267 | 0.8378 | 0.8158 | 0.8798 |
| TextCNN distilled | 0.9355 | 0.8800 | 0.8919 | 0.8684 | 0.8954 |

TextCNN distilled la model tot nhat trong nhom nay tren `test_challenge`.

---

## 3. Data split

Setup G2-style trong thu nghiem nay:

| split | rows | ghi chu |
|---|---:|---|
| train | 7,142 | `G2_external_curated` train |
| val | 535 | challenge validation |
| test_challenge | 537 | challenge test |

G2 train co them `external_curated` Label 0 nhung khong dung `external_real` trong train, dung dung tinh than G2.

---

## 4. BiLSTM result

### 4.1 Metrics by split

| split | model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---|---:|---:|---:|---:|---:|
| val | BiLSTM hard-label | 0.8341 | 0.6923 | 0.7297 | 0.6585 | 0.7427 |
| val | BiLSTM distilled | 0.8416 | 0.7042 | 0.6757 | 0.7353 | 0.7626 |
| test_challenge | BiLSTM hard-label | 0.8398 | 0.6984 | 0.5946 | 0.8462 | 0.7301 |
| test_challenge | BiLSTM distilled | 0.8172 | 0.6562 | 0.5676 | 0.7778 | 0.7454 |

### 4.2 Test challenge confusion matrix

| model | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| BiLSTM hard-label | 496 | 4 | 15 | 22 |
| BiLSTM distilled | 494 | 6 | 16 | 21 |

Dien giai:

- Distilled BiLSTM tang nhe val Macro-F1 va PR-AUC.
- Tren `test_challenge`, distilled BiLSTM giam Macro-F1, F1 Label 1, Recall Label 1 va Precision Label 1.
- Do do, voi G2-style split, distillation khong huu ich cho BiLSTM.

---

## 5. TextCNN result

### 5.1 Metrics by split

| split | model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---|---:|---:|---:|---:|---:|
| val | TextCNN hard-label | 0.8702 | 0.7595 | 0.8108 | 0.7143 | 0.8310 |
| val | TextCNN distilled | 0.9112 | 0.8354 | 0.8919 | 0.7857 | 0.8781 |
| test_challenge | TextCNN hard-label | 0.9068 | 0.8267 | 0.8378 | 0.8158 | 0.8798 |
| test_challenge | TextCNN distilled | 0.9355 | 0.8800 | 0.8919 | 0.8684 | 0.8954 |

### 5.2 Test challenge confusion matrix

| model | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| TextCNN hard-label | 493 | 7 | 6 | 31 |
| TextCNN distilled | 495 | 5 | 4 | 33 |

Dien giai:

- Distillation cai thien TextCNN tren ca val va test_challenge.
- Tren `test_challenge`, TextCNN distilled giam FP tu 7 xuong 5.
- Dong thoi giam FN tu 6 xuong 4.
- F1 Label 1 tang tu `0.8267` len `0.8800`.
- Recall Label 1 tang tu `0.8378` len `0.8919`.
- Precision Label 1 tang tu `0.8158` len `0.8684`.

Day la ket qua rat tot vi distilled TextCNN cai thien ca recall lan precision, khong chi di chuyen threshold theo huong bat nhieu Label 1 hon.

---

## 6. So sanh voi POC split v2

Ket qua POC split v2 da cho thay TextCNN distilled la student tot nhat tren `test_real`.

Ket qua G2-style robustness check tiep tuc ung ho:

```text
TextCNN la student neural phu hop nhat voi distillation trong nhom da thu.
```

Ket qua BiLSTM khong on dinh bang:

```text
BiLSTM distilled tot hon BiLSTM hard-label tren split_v2,
nhung khong tot hon BiLSTM hard-label trong G2-style challenge test.
```

Ket qua TextCNN on dinh hon:

```text
TextCNN distilled tot hon TextCNN hard-label tren split_v2 test_real,
va tiep tuc tot hon TextCNN hard-label tren G2-style test_challenge.
```

---

## 7. Ket luan co the bao cao

Doan ngan:

```text
Sau POC split_v2, em thu them robustness check theo setup gan voi G2_external_curated cho hai neural student BiLSTM va TextCNN. Soft labels duoc join tu teacher_outputs_v2 theo content voi coverage 100%. Ket qua cho thay BiLSTM distilled khong cai thien tren G2-style test_challenge, nhung TextCNN distilled tiep tuc cai thien ro so voi TextCNN hard-label: Macro-F1 tang tu 0.9068 len 0.9355, F1 Label 1 tang tu 0.8267 len 0.8800, Recall Label 1 tang tu 0.8378 len 0.8919 va Precision Label 1 tang tu 0.8158 len 0.8684. Dieu nay cung co ket luan tu POC: distillation co loi nhat voi TextCNN, trong khi hieu qua khong dong deu voi moi neural student.
```

Doan can than:

```text
Thiet lap nay la G2-style robustness check, chua phai retrain teacher rieng theo G2. Tuy nhien, vi teacher outputs co coverage day du tren cac mau G2, ket qua van huu ich de kiem tra tinh on dinh cua distilled student khi chuyen sang mot split gan voi setup best-performing truoc do.
```

---

## 8. Quyet dinh

```text
TextCNN distilled nen duoc chon lam distilled student chinh hien tai.
BiLSTM distilled nen duoc bao cao nhu ket qua phu: co loi tren split_v2 nhung khong on dinh trong G2-style robustness check.
Khong can mo rong them student moi truoc khi viet ket qua.
```

