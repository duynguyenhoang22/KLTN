# Distillation POC Final Report

> Pham vi: Bao cao tong hop proof-of-concept offline soft-label distillation voi ba student hien tai.
>
> Teacher: PhoBERT-base fine-tuned
>
> Student 1: TF-IDF char_wb 3-5 + Logistic Regression
>
> Student 2: Character-level BiLSTM
>
> Student 3: Character-level TextCNN

---

## 1. Ket luan tong quat

POC hien tai cho thay **distillation khong mac nhien co loi cho moi loai student**, nhung co the tao ra cai thien ro khi student architecture phu hop. Hieu qua distillation phu thuoc ro vao kien truc student.

Ket qua chinh:

```text
Student 1 TF-IDF:
  Distillation khong cai thien hard-label baseline.
  Tren test_real, distilled TF-IDF giam Macro-F1, F1 Label 1 va Recall Label 1.

Student 2 BiLSTM:
  Distillation cai thien ro so voi BiLSTM hard-label baseline.
  Tren test_real, Recall Label 1 tang tu 0.5135 len 0.6757.

Student 3 TextCNN:
  Distillation cai thien TextCNN hard-label baseline tren test_real.
  TextCNN distilled la student tot nhat hien tai tren test_real.

Best lightweight performance hien tai:
  TextCNN distilled, vi co Macro-F1/F1 Label 1/Recall Label 1/PR-AUC tot nhat tren test_real trong cac student.

Best evidence for distillation:
  TextCNN distilled, vi cai thien TextCNN hard-label va vuot TF-IDF hard-label tren benchmark chinh test_real.
```

Voi bai toan smishing, `test_real` la benchmark chinh. Vi vay, ket luan ve hieu qua thuc chat phai uu tien `test_real`, khong chi dua vao `val`, `test_mixed` hay `test_challenge`.

---

## 2. Thiet lap POC

### 2.1 Split va artifact

Split chinh:

```text
data/distillation/splits_v2/
```

Teacher outputs:

```text
data/distillation/teacher_outputs_v2/
```

Evaluation splits:

```text
val
test_real
test_mixed
test_challenge
```

Vai tro cua cac split:

```text
test_real:
  benchmark chinh, real SMS only.

test_mixed:
  mixed-domain holdout, dung de kiem tra on dinh tren nhieu data_origin.

test_challenge:
  challenge holdout co external va hard examples, dung lam danh gia phu.
```

### 2.2 Teacher

Teacher:

```text
PhoBERT-base fine-tuned
```

Teacher khong duoc dung nhu nhan thay the. Teacher duoc dung nhu nguon soft supervision co kiem soat.

Ly do:

```text
Teacher co precision Label 1 cao tren test_real,
nhung recall Label 1 tren test_real chi dat 0.6757.
```

### 2.3 Student 1

Student 1:

```text
TF-IDF char_wb 3-5 + Logistic Regression
```

Hai bien the:

```text
TF-IDF hard-label
TF-IDF distilled
```

Distillation implementation:

```text
soft_target_p1 = (1 - beta) * hard_label + beta * teacher_p1_t2
beta = (1 - alpha) * effective_distill_weight
alpha = 0.8
fn_distill_weight = 0.0
```

### 2.4 Student 2

Student 2:

```text
Character-level BiLSTM
```

### 2.5 Student 3

Student 3:

```text
Character-level TextCNN
```

Hai bien the:

```text
TextCNN hard-label
TextCNN distilled
```

Distillation loss giong Student 2:

```text
loss = alpha * BCE(student_logits, hard_label)
     + (1 - alpha) * effective_distill_weight * BCE(student_logits, teacher_p1_t2)
```

Cau hinh chinh:

```text
alpha = 0.8
fn_distill_weight = 0.0
max_len = 256
embed_dim = 64
num_filters = 96
kernel_sizes = 3,4,5
dropout = 0.3
```

Hai bien the:

```text
BiLSTM hard-label
BiLSTM distilled
```

Distillation loss:

```text
loss = alpha * BCE(student_logits, hard_label)
     + (1 - alpha) * effective_distill_weight * BCE(student_logits, teacher_p1_t2)
```

Cau hinh chinh:

```text
alpha = 0.8
fn_distill_weight = 0.0
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

Muc dich:

```text
Khong de teacher false negative day student bo sot smishing that.
```

---

## 3. Ket qua tong hop tren test_real

`test_real` la benchmark chinh.

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.8807 | 0.7812 | 0.6757 | 0.9259 | 0.8427 |
| TF-IDF hard-label | 0.8703 | 0.7619 | 0.6486 | 0.9231 | 0.8570 |
| TF-IDF distilled | 0.8597 | 0.7419 | 0.6216 | 0.9200 | 0.8567 |
| BiLSTM hard-label | 0.7580 | 0.5588 | 0.5135 | 0.6129 | 0.6239 |
| BiLSTM distilled | 0.8052 | 0.6494 | 0.6757 | 0.6250 | 0.7332 |
| TextCNN hard-label | 0.8610 | 0.7463 | 0.6757 | 0.8333 | 0.8123 |
| TextCNN distilled | 0.8840 | 0.7879 | 0.7027 | 0.8966 | 0.8770 |

Confusion matrix tren `test_real`:

| model | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| Teacher PhoBERT-base | 346 | 2 | 12 | 25 |
| TF-IDF hard-label | 346 | 2 | 13 | 24 |
| TF-IDF distilled | 346 | 2 | 14 | 23 |
| BiLSTM hard-label | 336 | 12 | 18 | 19 |
| BiLSTM distilled | 333 | 15 | 12 | 25 |
| TextCNN hard-label | 343 | 5 | 12 | 25 |
| TextCNN distilled | 345 | 3 | 11 | 26 |

Dien giai:

- TextCNN distilled co Macro-F1, F1 Label 1, Recall Label 1 va PR-AUC cao nhat trong cac student tren `test_real`.
- TextCNN distilled vuot teacher nhe ve Macro-F1/F1 Label 1/Recall Label 1, nhung teacher van co Precision Label 1 cao hon.
- TF-IDF hard-label van co Precision Label 1 cao nhat trong cac student.
- BiLSTM distilled co Recall Label 1 bang teacher (`0.6757`), nhung precision thap.
- BiLSTM distilled giam FN tu 18 xuong 12 so voi BiLSTM hard-label, nhung tang FP tu 12 len 15.
- TF-IDF distilled lam xau hon TF-IDF hard-label, dac biet FN tang tu 13 len 14.

---

## 4. Ket qua tren val

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.9881 | 0.9870 | 0.9870 | 0.9870 | 0.9988 |
| TF-IDF hard-label | 0.9855 | 0.9840 | 0.9758 | 0.9924 | 0.9982 |
| TF-IDF distilled | 0.9872 | 0.9859 | 0.9795 | 0.9925 | 0.9983 |
| BiLSTM hard-label | 0.9600 | 0.9561 | 0.9534 | 0.9588 | 0.9887 |
| BiLSTM distilled | 0.9770 | 0.9748 | 0.9739 | 0.9757 | 0.9961 |
| TextCNN hard-label | 0.9872 | 0.9860 | 0.9851 | 0.9869 | 0.9989 |
| TextCNN distilled | 0.9898 | 0.9888 | 0.9870 | 0.9907 | 0.9994 |

Dien giai:

- Distillation cai thien ca TF-IDF, BiLSTM va TextCNN tren validation.
- Tuy nhien, TF-IDF distilled tang tren validation nhung giam tren `test_real`.
- TextCNN distilled la bien the validation tot nhat trong cac student.
- Dieu nay cho thay validation improvement huu ich de theo doi, nhung ket luan chinh van phai dua tren `test_real`.

---

## 5. Ket qua tren test_mixed

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.9906 | 0.9905 | 0.9886 | 0.9924 | 0.9992 |
| TF-IDF hard-label | 0.9877 | 0.9875 | 0.9790 | 0.9961 | 0.9982 |
| TF-IDF distilled | 0.9877 | 0.9875 | 0.9790 | 0.9961 | 0.9982 |
| BiLSTM hard-label | 0.9509 | 0.9499 | 0.9390 | 0.9610 | 0.9907 |
| BiLSTM distilled | 0.9773 | 0.9771 | 0.9752 | 0.9790 | 0.9963 |
| TextCNN hard-label | 0.9868 | 0.9866 | 0.9790 | 0.9942 | 0.9993 |
| TextCNN distilled | 0.9943 | 0.9943 | 0.9905 | 0.9981 | 0.9996 |

Dien giai:

- TF-IDF distilled gan nhu khong thay doi so voi TF-IDF hard-label.
- BiLSTM distilled cai thien ro so voi BiLSTM hard-label.
- TextCNN distilled la model manh nhat tren `test_mixed` trong bang hien tai.

---

## 6. Ket qua tren test_challenge

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.9899 | 0.9878 | 0.9861 | 0.9895 | 0.9987 |
| TF-IDF hard-label | 0.9827 | 0.9792 | 0.9861 | 0.9725 | 0.9985 |
| TF-IDF distilled | 0.9827 | 0.9792 | 0.9861 | 0.9725 | 0.9986 |
| BiLSTM hard-label | 0.9231 | 0.9072 | 0.9024 | 0.9120 | 0.9644 |
| BiLSTM distilled | 0.9711 | 0.9655 | 0.9756 | 0.9556 | 0.9936 |
| TextCNN hard-label | 0.9884 | 0.9861 | 0.9861 | 0.9861 | 0.9986 |
| TextCNN distilled | 0.9855 | 0.9826 | 0.9826 | 0.9826 | 0.9989 |

Dien giai:

- TF-IDF distilled khong cai thien metric phan loai tai threshold 0.5.
- BiLSTM distilled tang manh so voi BiLSTM hard-label.
- TextCNN hard-label la student manh nhat tren `test_challenge` tai threshold 0.5.
- TextCNN distilled giam nhe metric threshold-based tren `test_challenge`, nhung PR-AUC tang nhe.

---

## 7. Phan tich theo student

### 7.1 Student 1: TF-IDF Logistic Regression

Ket qua Student 1:

```text
Hard-label baseline tot hon distilled tren test_real.
Distilled chi tang nhe tren validation, khong tong quat sang test_real.
```

Tren `test_real`:

| metric | TF-IDF hard-label | TF-IDF distilled | Delta |
|---|---:|---:|---:|
| Macro-F1 | 0.8703 | 0.8597 | -0.0107 |
| F1 Label 1 | 0.7619 | 0.7419 | -0.0200 |
| Recall Label 1 | 0.6486 | 0.6216 | -0.0270 |
| Precision Label 1 | 0.9231 | 0.9200 | -0.0031 |

Ket luan:

```text
Soft-label distillation khong huu ich cho TF-IDF Logistic Regression trong thiet lap hien tai.
```

Dien giai:

- TF-IDF la mo hinh tuyen tinh dua tren n-gram.
- Soft labels khong tao representation moi cho student.
- Teacher probabilities co the lam bien quyet dinh dich nhe nhung khong giup bat real smishing tot hon.
- Ket qua nay la bang chung rang distillation khong mac nhien co loi.

### 7.2 Student 2: Character-level BiLSTM

Ket qua Student 2:

```text
Distilled BiLSTM cai thien ro so voi BiLSTM hard-label baseline.
```

Tren `test_real`:

| metric | BiLSTM hard-label | BiLSTM distilled | Delta |
|---|---:|---:|---:|
| Macro-F1 | 0.7580 | 0.8052 | +0.0472 |
| F1 Label 1 | 0.5588 | 0.6494 | +0.0905 |
| Recall Label 1 | 0.5135 | 0.6757 | +0.1622 |
| Precision Label 1 | 0.6129 | 0.6250 | +0.0121 |

Ket luan:

```text
Soft-label distillation co loi cho BiLSTM student trong thiet lap hien tai.
```

Dien giai:

- BiLSTM co embedding, hidden states va logits nen co kha nang hap thu tin hieu mem tu teacher tot hon TF-IDF.
- Distillation giup BiLSTM bat them Label 1 tren `test_real`.
- Tuy nhien, precision Label 1 cua BiLSTM distilled con thap, nen day la bien the tang do nhay hon la bien the tot nhat tong the.

### 7.3 Student 3: Character-level TextCNN

Ket qua Student 3:

```text
TextCNN distilled cai thien TextCNN hard-label baseline tren test_real.
TextCNN distilled la student tot nhat hien tai tren benchmark chinh.
```

Tren `test_real`:

| metric | TextCNN hard-label | TextCNN distilled | Delta |
|---|---:|---:|---:|
| Macro-F1 | 0.8610 | 0.8840 | +0.0230 |
| F1 Label 1 | 0.7463 | 0.7879 | +0.0416 |
| Recall Label 1 | 0.6757 | 0.7027 | +0.0270 |
| Precision Label 1 | 0.8333 | 0.8966 | +0.0632 |

Ket luan:

```text
TextCNN distilled la ket qua tich cuc nhat cua distillation POC hien tai.
```

Dien giai:

- TextCNN hard-label da manh hon BiLSTM hard-label.
- Distillation van tiep tuc cai thien TextCNN tren `test_real`.
- Khac voi BiLSTM distilled, TextCNN distilled tang ca recall va precision Label 1 tren `test_real`.
- TextCNN distilled vuot TF-IDF hard-label ve Macro-F1 va F1 Label 1, du precision van thap hon nhe.

---

## 8. Best model va best distillation evidence

Can tach hai ket luan:

### 8.1 Best lightweight performance hien tai

```text
TextCNN distilled
```

Ly do:

- Trong cac student, TextCNN distilled co Macro-F1, F1 Label 1, Recall Label 1 va PR-AUC cao nhat tren `test_real`.
- TextCNN distilled giam ca FP va FN so voi TextCNN hard-label tren `test_real`.
- TextCNN distilled vuot TF-IDF hard-label ve Macro-F1 va F1 Label 1.

Han che:

- Precision Label 1 cua TextCNN distilled (`0.8966`) van thap hon TF-IDF hard-label (`0.9231`) va teacher (`0.9259`).

### 8.2 Best evidence for distillation

```text
TextCNN distilled
```

Ly do:

- Cai thien TextCNN hard-label tren `test_real`: Macro-F1 +0.0230, F1 Label 1 +0.0416, Recall Label 1 +0.0270, Precision Label 1 +0.0632.
- Cai thien `test_mixed` ro rang.
- La distilled student tot nhat tren benchmark chinh.

Han che:

- Tren `test_challenge`, TextCNN distilled giam nhe so voi TextCNN hard-label tai threshold 0.5.

---

## 9. Tra loi cac cau hoi nghien cuu tu POC

### Q1. Soft-label distillation co mac nhien cai thien student khong?

Khong.

Student 1 TF-IDF la bang chung ro: distilled variant giam ket qua tren `test_real` so voi hard-label baseline.

### Q2. Teacher probabilities co the huu ich khong?

Co, nhung phu thuoc vao student.

Voi BiLSTM, teacher probabilities giup cai thien ro so voi BiLSTM hard-label.

### Q3. Teacher recall Label 1 thap co gay rui ro khong?

Co.

Teacher tren `test_real` co Recall Label 1 `0.6757`. Vi vay POC da giu hard-label anchor manh va cap teacher false-negative distill weight ve 0.0. Day la quyet dinh dung vi khong nen de teacher day student bo sot smishing.

### Q4. Distillation co giai quyet duoc diem yeu real smishing khong?

Mot phan.

Voi BiLSTM, distillation tang Recall Label 1 tren `test_real`. Nhung precision con thap va TF-IDF hard-label van tot hon ve F1 Label 1.

### Q5. Co nen claim distilled student la model tot nhat khong?

Khong.

Nen claim:

```text
Distillation co loi cho BiLSTM so voi chinh baseline BiLSTM.
```

Khong nen claim:

```text
Distilled student la mo hinh lightweight tot nhat.
```

---

## 10. Ket luan co the dua vao luan van

Doan ket luan de xuat:

```text
Trong proof-of-concept offline soft-label distillation, nghien cuu su dung PhoBERT-base fine-tuned lam teacher va danh gia ba student nhe: TF-IDF Logistic Regression, character-level BiLSTM va character-level TextCNN. Ket qua cho thay distillation khong mac nhien cai thien moi student. Voi TF-IDF Logistic Regression, distilled variant lam giam ket qua tren benchmark chinh test_real, trong do F1 Label 1 giam tu 0.7619 xuong 0.7419 va Recall Label 1 giam tu 0.6486 xuong 0.6216. Nguoc lai, voi cac neural student, distillation tao cai thien ro hon. BiLSTM distilled tang F1 Label 1 tren test_real tu 0.5588 len 0.6494 va Recall Label 1 tu 0.5135 len 0.6757. Dac biet, TextCNN distilled dat ket qua tot nhat trong cac student tren test_real, voi Macro-F1 = 0.8840, F1 Label 1 = 0.7879, Recall Label 1 = 0.7027 va Precision Label 1 = 0.8966. Ket qua nay cho thay teacher probabilities huu ich hon khi student co representation neural va logits de hap thu tin hieu mem, dong thoi khang dinh distillation can duoc danh gia theo tung kien truc student thay vi xem nhu mot cai tien mac dinh.
```

Doan ngan de chen vao phan thao luan:

```text
Ket qua POC cung co y nghia canh bao: neu teacher co recall Label 1 han che tren real SMS, soft labels khong nen duoc dung nhu nhan thay the. Distillation can duoc thiet ke voi hard-label anchor va disagreement down-weighting. Dieu nay dac biet quan trong trong bai toan smishing, noi false negative co chi phi cao hon false positive.
```

---

## 11. Quyet dinh sau POC hien tai

Quyet dinh:

```text
1. Ghi nhan TextCNN distilled la lightweight student co hieu nang tong the tot nhat hien tai tren test_real.
2. Ghi nhan TextCNN distilled la bang chung tich cuc nhat cho hieu qua distillation.
3. Ghi nhan TF-IDF distilled la ket qua am quan trong: distillation khong mac nhien co loi.
4. Khong tiep tuc tune threshold tren test_real.
```

Neu tiep tuc:

```text
Option A:
  Tune threshold cho BiLSTM distilled tren validation only,
  sau do apply threshold co dinh len test splits.

Option B:
  Thu TextCNN hard-label va TextCNN distilled de xem neural architecture khac co trade-off tot hon BiLSTM khong.

Option C:
  Viet phan luan van tu cac ket qua hien co, vi POC da du de chung minh distillation co dieu kien.
```

Khuyen nghi:

```text
Viet phan ket qua POC hien tai truoc.
Neu con thoi gian, chi lam threshold tuning tren validation cho BiLSTM distilled nhu mot phan phan tich bo sung.
```
