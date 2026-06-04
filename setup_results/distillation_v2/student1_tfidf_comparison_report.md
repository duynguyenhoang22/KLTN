# Student 1 TF-IDF Distillation Comparison Report

> Pham vi: Bao cao so sanh Student 1 trong distillation POC.
>
> Student 1: `TF-IDF char_wb 3-5 + Logistic Regression`
>
> Muc tieu: Kiem tra lieu soft-label distillation tu PhoBERT-base teacher co cai thien student TF-IDF so voi hard-label baseline hay khong.

---

## 1. Ket luan chinh

Ket qua Phase 5 va Phase 6 cho thay **soft-label distillation chua cai thien Student 1 TF-IDF Logistic Regression tren benchmark quan trong nhat la `test_real`**.

Tren `test_real`, distilled student giam so voi hard-label baseline:

| metric | Hard-label student | Distilled student | Delta |
|---|---:|---:|---:|
| Macro-F1 | 0.8703 | 0.8597 | -0.0107 |
| F1 Label 1 | 0.7619 | 0.7419 | -0.0200 |
| Recall Label 1 | 0.6486 | 0.6216 | -0.0270 |
| Precision Label 1 | 0.9231 | 0.9200 | -0.0031 |
| PR-AUC | 0.8570 | 0.8567 | -0.0003 |

Day la ket qua quan trong vi `test_real` la benchmark chinh de danh gia kha nang tong quat tren SMS that. Dac biet, Recall Label 1 giam tu `0.6486` xuong `0.6216`, tuc distilled student bo sot them 1 mau smishing tren `test_real` so voi hard-label baseline.

Ket luan thuc nghiem:

```text
Voi Student 1 TF-IDF Logistic Regression, soft-label distillation tu teacher PhoBERT-base hien tai khong mang lai loi ich ro rang so voi hard-label baseline. Ket qua validation tang nhe, nhung tren test_real, distilled student lam giam Macro-F1, F1 Label 1 va Recall Label 1. Vi bai toan smishing uu tien khong bo sot Label 1, bien the distilled nay khong nen duoc xem la cai thien.
```

---

## 2. Thiet lap so sanh

### Teacher

Teacher la PhoBERT-base fine-tuned, da sinh offline soft labels trong:

```text
data/distillation/teacher_outputs_v2/
```

Teacher duoc audit truoc khi train student. Ket qua teacher can ghi nho:

| split | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| val | 0.9881 | 0.9870 | 0.9870 | 0.9870 | 0.9988 |
| test_real | 0.8807 | 0.7812 | 0.6757 | 0.9259 | 0.8427 |
| test_mixed | 0.9906 | 0.9905 | 0.9886 | 0.9924 | 0.9992 |
| test_challenge | 0.9899 | 0.9878 | 0.9861 | 0.9895 | 0.9987 |

### Student hard-label baseline

Phase 5 train Student 1 chi bang hard labels:

```text
content -> label
```

Model:

```text
TF-IDF char_wb 3-5 + Logistic Regression
```

Input feature:

```text
content
```

Khong dua vao input:

```text
data_origin
category
sender_type
has_url
has_phone_number
obfuscation_level
```

Output:

```text
setup_results/distillation_v2/student_tfidf_hard_label/
```

### Student distilled

Phase 6 train cung kien truc Student 1, nhung dung soft target co hard-label anchor:

```text
beta = (1 - alpha) * effective_distill_weight
soft_target_p1 = (1 - beta) * hard_label + beta * teacher_p1
soft_target_p0 = 1 - soft_target_p1
```

Cau hinh chinh:

```text
alpha = 0.8
teacher_probability = teacher_p1_t2
fn_distill_weight = 0.0
threshold = 0.5
```

Quy tac an toan:

```text
Neu label=1 nhung teacher_pred=0, effective_distill_weight bi cap ve 0.0.
```

Ly do:

```text
Khong de teacher false negative day student xem smishing that la hop le.
```

Output:

```text
setup_results/distillation_v2/student_tfidf_distilled/
```

Mot bien the `alpha=0.9` cung da duoc chay de kiem tra khi hard-label anchor manh hon:

```text
setup_results/distillation_v2/student_tfidf_distilled_alpha09/
```

Bien the nay van khong cai thien `test_real`.

---

## 3. So sanh Teacher, Hard Student va Distilled Student

### 3.1 Validation

Tren validation set, distilled student tang nhe so voi hard-label baseline:

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.9881 | 0.9870 | 0.9870 | 0.9870 | 0.9988 |
| Student hard-label | 0.9855 | 0.9840 | 0.9758 | 0.9924 | 0.9982 |
| Student distilled | 0.9872 | 0.9859 | 0.9795 | 0.9925 | 0.9983 |

Dien giai:

- Distilled student co cai thien nhe tren validation.
- Tuy nhien, validation khong phai bang chung cuoi cung.
- Can doi chieu voi `test_real`, vi day la benchmark chinh.

### 3.2 Test Real

`test_real` la benchmark quan trong nhat.

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.8807 | 0.7812 | 0.6757 | 0.9259 | 0.8427 |
| Student hard-label | 0.8703 | 0.7619 | 0.6486 | 0.9231 | 0.8570 |
| Student distilled | 0.8597 | 0.7419 | 0.6216 | 0.9200 | 0.8567 |

Confusion matrix tren `test_real`:

| model | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| Teacher PhoBERT-base | 346 | 2 | 12 | 25 |
| Student hard-label | 346 | 2 | 13 | 24 |
| Student distilled | 346 | 2 | 14 | 23 |

Dien giai:

- Ca ba model deu co precision Label 1 cao, nhung recall Label 1 thap.
- Teacher bo sot 12/37 mau Label 1 tren `test_real`.
- Hard-label student bo sot 13/37 mau Label 1.
- Distilled student bo sot 14/37 mau Label 1.
- Distillation khong giam false positive; FP van giu o muc 2.
- Distillation lam tang false negative tu 13 len 14.

Voi bai toan smishing, day la trade-off khong tot vi loi false negative nghia la bo sot tin lua dao.

### 3.3 Test Mixed

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.9906 | 0.9905 | 0.9886 | 0.9924 | 0.9992 |
| Student hard-label | 0.9877 | 0.9875 | 0.9790 | 0.9961 | 0.9982 |
| Student distilled | 0.9877 | 0.9875 | 0.9790 | 0.9961 | 0.9982 |

Dien giai:

- Distilled student gan nhu trung voi hard-label baseline.
- Khong co cai thien dang ke tren `test_mixed`.
- Teacher van cao hon student tren split nay.

### 3.4 Test Challenge

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.9899 | 0.9878 | 0.9861 | 0.9895 | 0.9987 |
| Student hard-label | 0.9827 | 0.9792 | 0.9861 | 0.9725 | 0.9985 |
| Student distilled | 0.9827 | 0.9792 | 0.9861 | 0.9725 | 0.9986 |

Dien giai:

- Distilled student khong thay doi F1/recall/precision so voi hard-label baseline.
- PR-AUC tang rat nho, nhung khong lam thay doi ket qua phan loai tai threshold 0.5.
- Teacher van co precision va F1 Label 1 cao hon student.

---

## 4. So sanh Hard Student va Distilled Student

Bang delta distilled - hard:

| split | Delta Macro-F1 | Delta F1 Label 1 | Delta Recall Label 1 | Delta Precision Label 1 | Delta PR-AUC |
|---|---:|---:|---:|---:|---:|
| val | +0.0017 | +0.0019 | +0.0037 | +0.0000 | +0.0000 |
| test_real | -0.0107 | -0.0200 | -0.0270 | -0.0031 | -0.0003 |
| test_mixed | +0.0000 | -0.0000 | +0.0000 | -0.0000 | +0.0000 |
| test_challenge | +0.0000 | -0.0000 | +0.0000 | +0.0000 | +0.0001 |

Nhan xet:

- Distillation co cai thien nhe tren validation.
- Distillation khong cai thien `test_mixed` va `test_challenge` tai threshold 0.5.
- Distillation lam giam ket qua tren `test_real`.
- Do `test_real` la benchmark chinh, Student 1 distilled khong duoc xem la variant tot hon hard-label baseline.

---

## 5. Tai sao ket qua nay hop ly?

Co ba ly do chinh.

### 5.1 Teacher cung co recall Label 1 thap tren test_real

Teacher tren `test_real`:

```text
Recall Label 1 = 0.6757
Precision Label 1 = 0.9259
```

Teacher co xu huong bao thu voi Label 1: khi du doan smishing thi kha chinh xac, nhung khong bat het smishing. Student hoc them soft probabilities tu teacher vi the co nguy co bi day ve ranh gioi bao thu hon.

Ngay ca khi da cap teacher false negative weight ve 0, cac mau teacher agree co probability rat cuc doan van co the lam model thay doi bien quyet dinh theo huong khong co loi cho `test_real`.

### 5.2 TF-IDF Logistic Regression khong phai kien truc ly tuong cho distillation

TF-IDF Logistic Regression la baseline nhanh, nhe va de giai thich. Tuy nhien, no khong co representation neural de hap thu day du thong tin mem tu teacher.

Trong thiet lap nay, soft-target training chu yeu thay doi trong so cua cac n-gram. Neu teacher probabilities khong mang tin hieu bo sung phu hop voi `test_real`, student distilled co the chi thay doi threshold/bien tuyen tinh nhe ma khong hoc duoc bieu dien tot hon.

### 5.3 Validation cai thien nhe khong bao dam tong quat tren test_real

Distilled student tang nhe tren validation:

```text
Delta Macro-F1 val = +0.0017
Delta Recall Label 1 val = +0.0037
```

Nhung tren `test_real`, cac delta deu am. Dieu nay cho thay tin hieu teacher co the phu hop hon voi validation/mixed distribution, nhung chua giup tong quat tren real SMS.

---

## 6. Ket luan co the dua vao luan van

Doan ket luan de xuat:

```text
Voi Student 1 la TF-IDF + Logistic Regression, nghien cuu so sanh hard-label baseline voi bien the distilled su dung soft probabilities tu PhoBERT-base teacher. Ket qua cho thay distilled student tang nhe tren validation set, nhung khong cai thien tren benchmark chinh test_real. Cu the, tren test_real, Macro-F1 giam tu 0.8703 xuong 0.8597, F1 Label 1 giam tu 0.7619 xuong 0.7419, va Recall Label 1 giam tu 0.6486 xuong 0.6216. Do bai toan smishing dac biet quan tam den viec khong bo sot Label 1, bien the distilled cua Student 1 khong duoc xem la cai thien so voi hard-label baseline. Ket qua nay cho thay soft-label distillation khong mac nhien co loi, dac biet khi teacher co recall Label 1 han che tren real SMS va student la mo hinh tuyen tinh dua tren TF-IDF.
```

Doan dien giai ngan:

```text
Student 1 duoc giu lai nhu mot baseline quan trong: no cho thay mot mo hinh nhe, text-only co the dat ket qua cao tren mixed/challenge split, nhung van gap kho voi real smishing. Distillation tu teacher hien tai khong giai quyet duoc diem yeu nay. Vi vay, buoc tiep theo hop ly la thu Student 2 co kien truc neural nhe nhu BiLSTM/TextCNN, trong do distillation loss co the duoc tich hop truc tiep voi hard-label CE va teacher probability.
```

---

## 7. Quyet dinh sau Student 1

Quyet dinh:

```text
Khong chon Student 1 distilled lam ket qua cai thien.
Giu Student 1 hard-label baseline lam moc so sanh chinh cho nhom lightweight classical model.
Ghi nhan Student 1 distilled la ket qua am/co dieu kien cua POC.
```

Khong nen lam tiep:

```text
Khong tiep tuc tune alpha/threshold theo test_real de ep distilled student thang baseline.
```

Nen lam tiep:

```text
1. Bao cao Student 1 hard-label vs distilled nhu mot ket qua trung thuc.
2. Trien khai Student 2 neural lightweight hard-label baseline.
3. Sau do trien khai Student 2 distilled voi hard-label anchor manh.
```

Ly do:

```text
Distillation co kha nang phu hop hon voi neural student, vi neural student co logits/representation de hoc soft target truc tiep hon TF-IDF Logistic Regression.
```

