# Student 3 TextCNN Distillation Comparison Report

> Pham vi: Bao cao so sanh Student 3 trong distillation POC.
>
> Student 3: `character-level TextCNN`
>
> Muc tieu: Kiem tra neural student nhe cuoi cung trong POC, sau TF-IDF va BiLSTM.

---

## 1. Ket luan chinh

Student 3 TextCNN la ket qua tot nhat hien tai trong nhom student. Khac voi TF-IDF, distillation cai thien TextCNN hard-label baseline tren `test_real`, `val` va `test_mixed`; tren `test_challenge`, TextCNN hard-label nhinh hon mot chut tai threshold 0.5.

Tren `test_real`:

| metric | TextCNN hard-label | TextCNN distilled | Delta |
|---|---:|---:|---:|
| Macro-F1 | 0.8610 | 0.8840 | +0.0230 |
| F1 Label 1 | 0.7463 | 0.7879 | +0.0416 |
| Recall Label 1 | 0.6757 | 0.7027 | +0.0270 |
| Precision Label 1 | 0.8333 | 0.8966 | +0.0632 |
| PR-AUC | 0.8123 | 0.8770 | +0.0647 |

TextCNN distilled cung vuot TF-IDF hard-label tren `test_real` ve Macro-F1, F1 Label 1 va Recall Label 1:

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 |
|---|---:|---:|---:|---:|
| TF-IDF hard-label | 0.8703 | 0.7619 | 0.6486 | 0.9231 |
| TextCNN distilled | 0.8840 | 0.7879 | 0.7027 | 0.8966 |

Nghia la sau Student 3, POC khong con chi la "distillation co loi cho BiLSTM nhung chua thanh best model". Ket qua moi cho thay **distilled neural student co the tro thanh student tot nhat tren benchmark chinh `test_real`**, du precision Label 1 van thap hon TF-IDF hard-label.

---

## 2. Thiet lap

### Student hard-label

Architecture:

```text
Character-level TextCNN
```

Training objective:

```text
BCEWithLogitsLoss(hard_label)
```

Output:

```text
setup_results/distillation_v2/student_textcnn_hard_label/
```

### Student distilled

Training objective:

```text
loss = alpha * BCE(student_logits, hard_label)
     + (1 - alpha) * effective_distill_weight * BCE(student_logits, teacher_p1_t2)
```

Cau hinh:

```text
alpha = 0.8
teacher probability = teacher_p1_t2
fn_distill_weight = 0.0
max_len = 256
embed_dim = 64
num_filters = 96
kernel_sizes = 3,4,5
dropout = 0.3
```

Output:

```text
setup_results/distillation_v2/student_textcnn_distilled/
```

---

## 3. So sanh TextCNN Hard va TextCNN Distilled

### 3.1 Validation

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| TextCNN hard-label | 0.9872 | 0.9860 | 0.9851 | 0.9869 | 0.9989 |
| TextCNN distilled | 0.9898 | 0.9888 | 0.9870 | 0.9907 | 0.9994 |

Distillation cai thien nhe tren validation.

### 3.2 Test Real

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| TextCNN hard-label | 0.8610 | 0.7463 | 0.6757 | 0.8333 | 0.8123 |
| TextCNN distilled | 0.8840 | 0.7879 | 0.7027 | 0.8966 | 0.8770 |

Confusion matrix tren `test_real`:

| model | TN | FP | FN | TP |
|---|---:|---:|---:|---:|
| TextCNN hard-label | 343 | 5 | 12 | 25 |
| TextCNN distilled | 345 | 3 | 11 | 26 |

Dien giai:

- Distillation giam FP tu 5 xuong 3.
- Distillation giam FN tu 12 xuong 11.
- TP tang tu 25 len 26.
- Day la trade-off tot hon BiLSTM distilled: vua tang recall, vua tang precision.

### 3.3 Test Mixed

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| TextCNN hard-label | 0.9868 | 0.9866 | 0.9790 | 0.9942 | 0.9993 |
| TextCNN distilled | 0.9943 | 0.9943 | 0.9905 | 0.9981 | 0.9996 |

Distillation cai thien ro tren `test_mixed`.

### 3.4 Test Challenge

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| TextCNN hard-label | 0.9884 | 0.9861 | 0.9861 | 0.9861 | 0.9986 |
| TextCNN distilled | 0.9855 | 0.9826 | 0.9826 | 0.9826 | 0.9989 |

Tren `test_challenge`, TextCNN distilled giam nhe metric threshold-based so voi hard-label, nhung PR-AUC tang nhe. Vi `test_real` la benchmark chinh, ket qua `test_challenge` duoc xem la canh bao phu: distilled TextCNN tot tren real/mixed nhung khong thang tuyet doi tren moi split.

---

## 4. So sanh voi cac model truoc

### 4.1 Test Real

| model | Macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Teacher PhoBERT-base | 0.8807 | 0.7812 | 0.6757 | 0.9259 | 0.8427 |
| TF-IDF hard-label | 0.8703 | 0.7619 | 0.6486 | 0.9231 | 0.8570 |
| TF-IDF distilled | 0.8597 | 0.7419 | 0.6216 | 0.9200 | 0.8567 |
| BiLSTM hard-label | 0.7580 | 0.5588 | 0.5135 | 0.6129 | 0.6239 |
| BiLSTM distilled | 0.8052 | 0.6494 | 0.6757 | 0.6250 | 0.7332 |
| TextCNN hard-label | 0.8610 | 0.7463 | 0.6757 | 0.8333 | 0.8123 |
| TextCNN distilled | 0.8840 | 0.7879 | 0.7027 | 0.8966 | 0.8770 |

Nhan xet:

- TextCNN distilled la student tot nhat tren `test_real` theo Macro-F1, F1 Label 1, Recall Label 1 va PR-AUC.
- Teacher van co Precision Label 1 cao nhat trong nhom neural/teacher.
- TF-IDF hard-label van co Precision Label 1 cao nhat trong cac student.
- TextCNN distilled la bang chung manh nhat rang distillation co the tao ra cai thien thuc chat khi student architecture phu hop.

---

## 5. Ket luan co the dua vao luan van

Doan ket luan de xuat:

```text
Student 3 TextCNN la bien the neural lightweight tot nhat trong distillation POC. So voi TextCNN hard-label baseline, TextCNN distilled cai thien tren benchmark chinh test_real: Macro-F1 tang tu 0.8610 len 0.8840, F1 Label 1 tang tu 0.7463 len 0.7879, Recall Label 1 tang tu 0.6757 len 0.7027, va Precision Label 1 tang tu 0.8333 len 0.8966. Ket qua nay cho thay, khac voi TF-IDF Logistic Regression, neural student co kha nang hap thu teacher probabilities mot cach hieu qua hon. TextCNN distilled cung vuot TF-IDF hard-label tren test_real ve Macro-F1 va F1 Label 1, du precision Label 1 van thap hon mot chut. Vi vay, TextCNN distilled duoc xem la ket qua tich cuc nhat cua distillation POC hien tai.
```

---

## 6. Quyet dinh sau Student 3

Quyet dinh:

```text
TextCNN distilled la distilled student tot nhat hien tai.
TextCNN distilled la bang chung chinh cho loi ich cua distillation trong POC.
Khong can them student moi truoc khi chuyen sang test theo setup G2.
```

Nen lam tiep:

```text
1. Cap nhat final POC report voi Student 3.
2. Sau do thiet ke buoc test theo setup G2 nhu da du dinh.
```

