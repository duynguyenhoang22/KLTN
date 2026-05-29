# Codex Guidelines: Offline Soft-label Distillation cho ViSmishDS

> Muc dich: Day la guideline bat buoc cho Codex khi trien khai pipeline offline soft-label distillation trong repo nay.
>
> Nguon can bam sat: `docs/offline_soft_label_distillation_plan.md` va context da thong nhat voi nguoi dung.
>
> Nguyen tac lon: Uu tien proof-of-concept tiet kiem tai nguyen truoc. Khong mac dinh dung teacher lon nhu PhoBERT-large/XLM-R-large neu nguoi dung chua yeu cau.

---

## 1. Huong di da chot

Pipeline proof-of-concept mac dinh:

```text
Teacher:
  vinai/phobert-base fine-tuned
  max_length = 256
  epochs = 3
  batch_size = 32 (dieu chinh theo GPU)

Student 1:
  TF-IDF + Logistic Regression hoac LinearSVC calibrated

Student 2:
  BiLSTM/TextCNN

Student 3 optional:
  MiniLM multilingual
```

Y nghia thuc nghiem:

```text
PhoBERT-base teacher -> student nho hon/nhanh hon/re hon
```

Khong goi day la "large-to-small distillation" theo nghia manh neu teacher chi la PhoBERT-base. Goi dung la:

```text
resource-constrained offline soft-label distillation
```

Hoac:

```text
proof-of-concept teacher-student distillation trong dieu kien tai nguyen han che
```

---

## 2. Cac viec khong duoc lam

- Khong dua `data_origin` vao input cua model.
- Khong dung test set de chon checkpoint, chon alpha, chon temperature, hay dieu chinh hyperparameter.
- Khong tron cac split neu chua ghi ro muc dich.
- Khong de `content` overlap giua train/val/test chinh.
- Khong coi `test_mixed` la bang chung chinh neu ket qua tren `test_real` yeu.
- Khong mac dinh fine-tune `phobert-large` hoac `xlm-roberta-large`.
- Khong sua/xoa cac thay doi git khong phai do minh tao.
- Khong viet file bang shell redirection/cat. Khi tao/sua file thu cong, dung `apply_patch`.
- Khong chi bao cao accuracy. Accuracy khong du cho bai toan smishing.

---

## 3. Thu tu trien khai bat buoc

### Phase 1: Split dataset

Input mac dinh:

```text
data/final/vismishds_content_label_origin.csv
```

Output de xuat:

```text
data/distillation/splits/train.csv
data/distillation/splits/val.csv
data/distillation/splits/test_real.csv
data/distillation/splits/test_mixed.csv
data/distillation/splits/test_challenge.csv
setup_results/distillation/split_report.md
```

Can lam truoc moi fine-tuning teacher.

### Phase 2: Fine-tune teacher

Teacher mac dinh:

```text
vinai/phobert-base
```

Thong so mac dinh:

```text
max_length = 128
epochs = 3
batch_size = 16 neu GPU chiu duoc
```

Neu batch size 16 OOM, giam:

```text
batch_size = 8 hoac 4
gradient_accumulation_steps de giu effective batch size
```

### Phase 3: Sinh teacher outputs

Chay inference teacher tren moi split can thiet:

```text
train
val
test_real
test_mixed
test_challenge
```

Luu logits va probabilities, khong chi luu predicted label.

### Phase 4: Audit teacher outputs

Bat buoc tao audit truoc khi train student distilled:

```text
teacher performance theo split
teacher performance theo data_origin
teacher_agree_label
teacher disagreement confidence cao
phan bo teacher_p1 theo label va data_origin
```

### Phase 5: Train student hard-label baseline

Moi student phai co baseline hoc nhan cung:

```text
content -> label
```

### Phase 6: Train student distilled

Moi student distilled phai so sanh voi chinh baseline cua no:

```text
Student TF-IDF hard-label vs Student TF-IDF distilled
Student BiLSTM hard-label vs Student BiLSTM distilled
Student MiniLM hard-label vs Student MiniLM distilled
```

### Phase 7: Bao cao so sanh

Bao cao phai co:

```text
teacher
student hard-label
student distilled
```

Tren it nhat:

```text
test_real
test_mixed
test_challenge
```

---

## 4. Nguyen tac split du lieu

Split phai nham muc tieu:

```text
Kiem tra model co hoc ranh gioi smishing that hay chi hoc shortcut synthetic/paraphrased.
```

Luat:

1. Tach test truoc, train sau.
2. Luon co `test_real.csv`.
3. `test_real.csv` chi gom `data_origin = real`.
4. `test_real.csv` phai co ca `label=0` va `label=1`.
5. Validation phai co `real label 1`.
6. Stratify theo `label x data_origin`, khong chi theo `label`.
7. Dung seed co dinh, mac dinh `42` neu nguoi dung khong yeu cau khac.
8. Kiem tra exact duplicate/overlap theo `content` giua split.
9. `test_mixed` la phu.
10. `test_challenge` la stress test, khong thay the `test_real`.

Goi y ty le:

```text
Real label 1:
  train 70%
  val   15%
  test_real 15%

Real label 0:
  train 70%
  val   15%
  test_real 15%

Synthetic/paraphrased/external:
  train 80%
  val   10%
  test_mixed 10%

synthetic_hard_negative:
  train 70%
  val   10%
  test_challenge 20%
```

Voi strata qua nho, vi du `synthetic label 1` chi co it mau, uu tien dua vao train/val thay vi ep chia vao moi test.

---

## 5. Schema teacher outputs

Moi file teacher output nen giu cac cot goc:

```text
content
label
data_origin
```

Va them cac cot:

```text
teacher_model
teacher_version
teacher_logit_0
teacher_logit_1
teacher_p0_t1
teacher_p1_t1
teacher_pred
teacher_confidence
teacher_agree_label
distill_weight
```

Neu co temperature distillation tu logits, them:

```text
teacher_p0_t2
teacher_p1_t2
teacher_temperature
```

Mac dinh:

```text
teacher_pred = argmax(teacher_p0_t1, teacher_p1_t1)
teacher_confidence = max(teacher_p0_t1, teacher_p1_t1)
teacher_agree_label = teacher_pred == label
```

---

## 6. Loss distillation can dung

### Student neural model

Voi student neural co logits:

```text
L_total = alpha * CE(y, student_logits)
        + (1 - alpha) * soft_loss
```

Neu dung binary probability:

```text
soft_loss = BCE(teacher_p1, student_p1)
```

Neu dung logits voi temperature:

```text
soft_loss = T^2 * KL(
  softmax(teacher_logits / T),
  softmax(student_logits / T)
)
```

Gia tri ablation mac dinh:

```text
alpha = 0.3, 0.5, 0.7
T = 1, 2, 4
```

Voi proof-of-concept, co the bat dau:

```text
alpha = 0.5
T = 1
```

### Student TF-IDF Logistic Regression

Can co hai baseline:

```text
Hard-label:
  y = label

Soft-label/distilled:
  target = teacher_p1
```

Neu thu vien/classifier khong ho tro soft target truc tiep, can dung cach phu hop:

- train logistic regression hard-label roi calibration bang teacher probabilities;
- hoac dung regression/probability model hoc `teacher_p1`;
- hoac tao sample weighting/label smoothing theo teacher confidence;
- neu dung LinearSVC, can calibrated probability bang `CalibratedClassifierCV`.

Khi bao cao, phai noi ro TF-IDF distilled duoc hien thuc theo cach nao.

---

## 7. Distill weight

Mac dinh co the dat:

```text
if teacher_agree_label and teacher_confidence >= 0.8:
  distill_weight = 1.0
elif teacher_agree_label:
  distill_weight = 0.7
else:
  distill_weight = 0.3
```

Neu chua dung weighted loss trong lan dau, van phai luu `distill_weight` de audit va mo rong sau.

---

## 8. Metrics bat buoc

Khong duoc chi bao cao accuracy.

Metrics toi thieu:

```text
accuracy
precision_label_1
recall_label_1
f1_label_1
macro_f1
weighted_f1
confusion_matrix
```

Nen them neu kha thi:

```text
roc_auc
pr_auc
ece/calibration
model_size
latency
```

Bao cao phai tach:

```text
overall
theo data_origin
test_real
test_mixed
test_challenge
```

Tieu chi thanh cong cua POC:

```text
Student distilled tot hon student hard-label baseline
```

It nhat tren mot so mat quan trong:

- macro-F1;
- F1 label 1;
- recall label 1 tren `test_real`;
- calibration;
- hoac latency/model size voi chat luong chap nhan duoc.

---

## 9. Bao cao va artifacts can tao

Moi phase nen co output ro rang.

Split:

```text
setup_results/distillation/split_report.md
```

Teacher:

```text
setup_results/distillation/teacher_metrics.json
setup_results/distillation/teacher_audit.md
```

Student:

```text
setup_results/distillation/student_tfidf_hard_metrics.json
setup_results/distillation/student_tfidf_distilled_metrics.json
setup_results/distillation/student_bilstm_hard_metrics.json
setup_results/distillation/student_bilstm_distilled_metrics.json
```

Tong hop:

```text
setup_results/distillation/comparison_report.md
```

---

## 10. Thu tu uu tien khi nguoi dung bao "trien khai"

Neu nguoi dung yeu cau bat dau trien khai ma khong noi cu the phase nao, Codex phai lam theo thu tu:

1. Tao script split dataset va split report.
2. Tao skeleton script/notebook fine-tune PhoBERT-base teacher.
3. Tao script inference teacher outputs.
4. Tao script audit teacher outputs.
5. Tao TF-IDF hard-label baseline.
6. Tao TF-IDF distilled baseline.
7. Sau khi POC TF-IDF on, moi them BiLSTM/TextCNN.
8. MiniLM la optional, chi lam khi nguoi dung xac nhan hoac cac buoc truoc da on.

Khong nhay thang vao BiLSTM/MiniLM khi chua co split va teacher output.

---

## 11. Cach dien giai trong khoa luan

Dung cach goi:

```text
Offline soft-label knowledge distillation
Resource-constrained teacher-student setup
PhoBERT-base fine-tuned teacher
Lightweight student classifiers
```

Khong phong dai thanh:

```text
distillation tu mo hinh cuc lon
LLM-level knowledge transfer
large-to-small compression neu teacher khong phai large model
```

Luan diem dung:

```text
Trong dieu kien tai nguyen han che, nghien cuu dung PhoBERT-base fine-tuned lam teacher de tao soft labels cho du lieu SMS tieng Viet. Cac student nho hon duoc huan luyen bang nhan cung ket hop soft labels, nham kiem tra lieu teacher probabilities co cai thien hieu nang, calibration, hoac trade-off toc do/chat luong so voi student hoc nhan cung hay khong.
```

---

## 12. Checklist truoc khi ket luan mot phase

Truoc khi bao hoan thanh, Codex phai kiem tra:

- File/artifact da duoc tao dung duong dan.
- Khong co overlap `content` giua split chinh.
- Report co bang phan bo `label`, `data_origin`, `label x data_origin`.
- Script co seed co dinh.
- Metrics co label-1 recall/F1 va macro-F1.
- Cac thay doi khong ghi de file nguoi dung dang sua neu khong can thiet.
- Neu chua chay duoc do thieu GPU/dependency, phai noi ro va de lai script chay duoc tren Kaggle/Colab.
