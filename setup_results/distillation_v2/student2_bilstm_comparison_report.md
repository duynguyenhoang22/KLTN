# Student 2 BiLSTM Distillation Comparison Report

> Pham vi: Bao cao so sanh Student 2 trong distillation POC.
>
> Student 2: `character-level BiLSTM`
>
> Muc tieu: Kiem tra lieu soft-label distillation co huu ich hon khi student la neural model co logits/representation, thay vi TF-IDF Logistic Regression.

---

## 1. Ket luan chinh

Khac voi Student 1 TF-IDF, **Student 2 BiLSTM distilled cai thien ro so voi BiLSTM hard-label baseline tren tat ca test split**, bao gom benchmark chinh `test_real`.

Tren `test_real`:

| metric | BiLSTM hard-label | BiLSTM distilled | Delta |
|---|---:|---:|---:|
| Macro-F1 | 0.7580 | 0.8052 | +0.0472 |
| F1 Label 1 | 0.5588 | 0.6494 | +0.0905 |
| Recall Label 1 | 0.5135 | 0.6757 | +0.1622 |
| Precision Label 1 | 0.6129 | 0.6250 | +0.0121 |
| PR-AUC | 0.6239 | 0.7332 | +0.1093 |

Ket qua nay cho thay distillation co tac dung tich cuc hon voi neural student so voi classical TF-IDF student. Dac biet, Recall Label 1 tren `test_real` tang tu `0.5135` len `0.6757`, tuong duong giam false negative tu 18 xuong 12 mau.

Tuy nhien, BiLSTM distilled van chua vuot TF-IDF hard-label baseline tren `test_real` ve Macro-F1/F1 Label 1:

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 |
|---|---:|---:|---:|---:|
| TF-IDF hard-label | 0.8703 | 0.7619 | 0.6486 | 0.9231 |
| BiLSTM distilled | 0.8052 | 0.6494 | 0.6757 | 0.6250 |

Nghia la BiLSTM distilled bat duoc them Label 1 so voi TF-IDF hard-label, nhung doi lai precision Label 1 thap hon nhieu. Day la trade-off can duoc bao cao ro.

---

## 2. Thiet lap

### Student hard-label

Input:

```text
data/distillation/splits_v2/
```

Training objective:

```text
BCEWithLogitsLoss(hard_label)
```

Output:

```text
setup_results/distillation_v2/student_bilstm_hard_label/
```

### Student distilled

Input:

```text
data/distillation/teacher_outputs_v2/
```

Training objective:

```text
loss = alpha * BCEWithLogitsLoss(hard_label)
     + (1 - alpha) * distill_weight * BCEWithLogitsLoss(teacher_p1_t2)
```

Cau hinh:

```text
alpha = 0.8
teacher probability = teacher_p1_t2
fn_distill_weight = 0.0
threshold = 0.5
max_len = 256
embed_dim = 64
hidden_dim = 64
dropout = 0.3
```

Quy tac an toan:

```text
Neu label=1 va teacher_pred=0:
  effective_distill_weight = 0.0
```

Output:

```text
setup_results/distillation_v2/student_bilstm_distilled/
```

---

## 3. So sanh BiLSTM Hard va BiLSTM Distilled

### 3.1 Validation

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| BiLSTM hard-label | 0.9600 | 0.9561 | 0.9534 | 0.9588 | 0.9887 |
| BiLSTM distilled | 0.9770 | 0.9748 | 0.9739 | 0.9757 | 0.9961 |

Distillation cai thien validation tren tat ca metric chinh.

### 3.2 Test Real

`test_real` la benchmark chinh.

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| BiLSTM hard-label | 0.7580 | 0.5588 | 0.5135 | 0.6129 | 0.6239 |
| BiLSTM distilled | 0.8052 | 0.6494 | 0.6757 | 0.6250 | 0.7332 |

Confusion matrix tren `test_real`:

| model | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| BiLSTM hard-label | 336 | 12 | 18 | 19 |
| BiLSTM distilled | 333 | 15 | 12 | 25 |

Dien giai:

- Distillation tang true positives tu 19 len 25.
- False negatives giam tu 18 xuong 12.
- False positives tang tu 12 len 15.
- Trong bai toan smishing, viec giam false negative la diem tich cuc, nhung FP tang can duoc ghi nhan.

### 3.3 Test Mixed

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| BiLSTM hard-label | 0.9509 | 0.9499 | 0.9390 | 0.9610 | 0.9907 |
| BiLSTM distilled | 0.9773 | 0.9771 | 0.9752 | 0.9790 | 0.9963 |

Distillation cai thien ca recall va precision Label 1 tren `test_mixed`.

### 3.4 Test Challenge

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| BiLSTM hard-label | 0.9231 | 0.9072 | 0.9024 | 0.9120 | 0.9644 |
| BiLSTM distilled | 0.9711 | 0.9655 | 0.9756 | 0.9556 | 0.9936 |

Distillation cai thien rat ro tren `test_challenge`, dac biet Recall Label 1 tang tu `0.9024` len `0.9756`.

---

## 4. So sanh voi Teacher va Student 1

### 4.1 Test Real

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.8807 | 0.7812 | 0.6757 | 0.9259 | 0.8427 |
| TF-IDF hard-label | 0.8703 | 0.7619 | 0.6486 | 0.9231 | 0.8570 |
| TF-IDF distilled | 0.8597 | 0.7419 | 0.6216 | 0.9200 | 0.8567 |
| BiLSTM hard-label | 0.7580 | 0.5588 | 0.5135 | 0.6129 | 0.6239 |
| BiLSTM distilled | 0.8052 | 0.6494 | 0.6757 | 0.6250 | 0.7332 |

Nhan xet:

- BiLSTM distilled dat Recall Label 1 bang teacher tren `test_real` (`0.6757`).
- BiLSTM distilled co recall cao hon TF-IDF hard-label (`0.6757` vs `0.6486`).
- Tuy nhien, BiLSTM distilled co precision Label 1 thap hon nhieu (`0.6250` vs `0.9231`).
- Vi vay, BiLSTM distilled la bien the tang do nhay, khong phai bien the tong the tot nhat.

### 4.2 Dien giai vai tro cua Student 2

Student 2 tra loi mot cau hoi khac Student 1:

```text
Distillation co the giup neural lightweight student hoc tot hon chinh hard-label baseline cua no khong?
```

Voi BiLSTM, cau tra loi la:

```text
Co, trong thiet lap nay distillation cai thien ro so voi BiLSTM hard-label baseline.
```

Nhung neu hoi:

```text
BiLSTM distilled co phai student tot nhat hien tai khong?
```

Thi cau tra loi la:

```text
Chua. TF-IDF hard-label van tot hon ve Macro-F1, F1 Label 1 va Precision Label 1 tren test_real.
```

---

## 5. Ket luan co the dua vao luan van

Doan ket luan de xuat:

```text
Khac voi Student 1 TF-IDF Logistic Regression, Student 2 character-level BiLSTM cho thay loi ich ro hon tu soft-label distillation. Khi so sanh voi BiLSTM hard-label baseline, bien the distilled cai thien Macro-F1 tren test_real tu 0.7580 len 0.8052, F1 Label 1 tu 0.5588 len 0.6494, va Recall Label 1 tu 0.5135 len 0.6757. Ket qua nay cho thay teacher probabilities co the huu ich hon khi student la neural model co representation va logits de hap thu tin hieu mem. Tuy nhien, BiLSTM distilled van co Precision Label 1 thap hon dang ke so voi TF-IDF hard-label baseline, nen no nen duoc dien giai la bien the tang do nhay phat hien smishing, khong phai mo hinh lightweight tot nhat ve tong the.
```

Doan dien giai ngan:

```text
Ket qua Student 2 ung ho nhan dinh rang distillation khong mac nhien co loi cho moi loai student. Voi TF-IDF, soft labels khong cai thien test_real. Voi BiLSTM, soft labels cai thien ro so voi hard-label baseline cung kien truc, dac biet ve Recall Label 1. Tuy nhien, trade-off precision/recall van can duoc bao cao minh bach.
```

---

## 6. Quyet dinh sau Student 2

Quyet dinh:

```text
Ghi nhan BiLSTM distilled la ket qua distillation tich cuc dau tien trong POC.
Khong ket luan no la mo hinh lightweight tot nhat, vi precision tren test_real con thap.
Dung no de chung minh distillation phu thuoc vao loai student va co loi hon voi neural student.
```

Nen lam tiep:

```text
1. Viet bao cao tong hop Student 1 vs Student 2.
2. Neu con thoi gian, thu TextCNN hoac threshold tuning tren validation cho BiLSTM distilled.
3. Khong tune threshold bang test_real.
```

