# Ke hoach Offline Soft-label Knowledge Distillation cho ViSmishDS

> Pham vi: Tai lieu nay mo ta co so ly thuyet va ke hoach ap dung offline soft-label distillation cho tap `data/final/vismishds_content_label_origin.csv`.
>
> Muc tieu: Tao mot pipeline trong do mo hinh lon dong vai tro `teacher`, sinh soft labels cho tung tin nhan SMS; sau do huan luyen mo hinh nho hon `student` bang ket hop giua nhan cung `0/1` va xac suat mem tu teacher.

---

## 1. Boi canh du lieu hien tai

Tap du lieu hien tai:

```text
data/final/vismishds_content_label_origin.csv
```

Co ba cot:

```text
content,label,data_origin
```

Thong ke tai thoi diem kiem tra:

| Thuoc tinh | Gia tri |
|---|---:|
| Tong so mau | 10,562 |
| So cot | 3 |
| Label 0 | 5,320 |
| Label 1 | 5,242 |
| Noi dung rong | 0 |
| Noi dung trung lap | 0 |
| Do dai trung binh | 156.8 ky tu |
| So tu trung binh | 30.4 tu |

Phan bo theo `data_origin`:

| data_origin | label 0 | label 1 | tong |
|---|---:|---:|---:|
| real | 2,321 | 246 | 2,567 |
| synthetic | 1,998 | 10 | 2,008 |
| paraphrased | 0 | 4,333 | 4,333 |
| synthetic_hard_negative | 0 | 653 | 653 |
| external_curated | 501 | 0 | 501 |
| external_real | 500 | 0 | 500 |

Nhan xet quan trong:

- Tap du lieu da can bang gan 1:1 theo nhan `0/1`.
- `content` ngan, phu hop voi cac encoder nho nhu PhoBERT-base, DistilBERT, MiniLM, BiLSTM/CNN.
- `data_origin` tuong quan rat manh voi `label`, nen khong nen dua cot nay vao input cua mo hinh.
- `data_origin` nen duoc dung de chia tap, gan trong so mau, va phan tich loi.
- Tap hien tai moi co nhan cung, chua co teacher outputs. Vi vay no la base dataset cho distillation, chua phai distilled dataset.

---

## 2. Van de cua huan luyen bang nhan cung

Voi huan luyen thong thuong, moi mau chi co mot nhan:

```text
content -> label
```

Vi du:

```text
"Tai khoan cua ban bi khoa. Xac minh tai..." -> 1
"Ma OTP cua ban la 123456" -> 0
```

Nhan cung `0/1` co uu diem la ro rang, de huan luyen, de danh gia. Tuy nhien no mat di nhieu thong tin:

- Mau nao rat de?
- Mau nao sat bien quyet dinh?
- Mau nao co kha nang bi gan nhan sai?
- Mau nao la tin hop le nhung co dau hieu giong lua dao?
- Mau nao la tin lua dao nhung nguon/van phong viet rat giong tin that?

Trong bai toan SMS smishing, hai tin nhan co the cung la `label=1`, nhung khac nhau ve muc do chac chan:

```text
Tin A: ro rang lua dao, co link la, mao danh ngan hang, tao ap luc thoi gian.
Tin B: co dau hieu bat thuong nhung noi dung gan voi thong bao that.
```

Huan luyen bang nhan cung doi xu ca hai tin nay nhu nhau:

```text
label = 1
```

Distillation them mot lop thong tin:

```text
Tin A: teacher_p1 = 0.98
Tin B: teacher_p1 = 0.61
```

Day la gia tri chinh cua soft-label distillation.

---

## 3. Co so ly thuyet cua knowledge distillation

### 3.1 Teacher va student

Knowledge distillation gom hai thanh phan:

```text
Teacher model: mo hinh lon, chat luong cao, chi phi suy luan lon.
Student model: mo hinh nho, nhe, nhanh, de trien khai hon.
```

Teacher khong truyen truc tiep trong so cho student. Student hoc bat chuoc hanh vi cua teacher tren tap du lieu:

```text
x_i -> teacher_output_i
x_i -> student_output_i
```

Muc tieu:

```text
student_output_i gan teacher_output_i
```

Trong phan loai nhi phan:

```text
teacher_output_i = P_teacher(label=1 | content_i)
student_output_i = P_student(label=1 | content_i)
```

### 3.2 Soft labels

Nhan cung:

```text
y = 0 hoac 1
```

Nhan mem:

```text
q = P_teacher(label=1 | x)
```

Vi du:

| content | label | teacher_p1 |
|---|---:|---:|
| Tin lua dao ro rang | 1 | 0.98 |
| Tin lua dao nhap nhang | 1 | 0.66 |
| Tin OTP hop le | 0 | 0.04 |
| Tin ngan hang hop le nhung co link | 0 | 0.32 |

Soft label giup student hoc duoc do chac chan va khoang cach tu mau toi ranh gioi quyet dinh.

### 3.3 Dark knowledge

`Dark knowledge` la tri thuc nam trong phan bo xac suat cua teacher, khong nam trong nhan dung/sai.

Voi bai toan nhieu lop, dark knowledge the hien moi quan he giua cac lop. Vi du anh meo co the gan voi cho hon la xe tai.

Voi bai toan nhi phan nhu smishing SMS, dark knowledge chu yeu nam o:

- do chac chan cua teacher;
- muc do nhap nhang cua mau;
- kha nang nhan goc bi nhieu;
- mau nam gan hay xa decision boundary;
- tin hieu nao lam teacher nghi ngo day la lua dao.

### 3.4 Temperature

Trong phan loai, mo hinh tao logits:

```text
z = [z_0, z_1]
```

Softmax chuyen logits thanh xac suat:

```text
p_i = exp(z_i) / sum_j exp(z_j)
```

Distillation thuong dung temperature `T`:

```text
p_i(T) = exp(z_i / T) / sum_j exp(z_j / T)
```

Khi `T = 1`, day la softmax thong thuong.

Khi `T > 1`, phan bo tro nen mem hon:

```text
T = 1: P(0)=0.01, P(1)=0.99
T = 4: P(0)=0.24, P(1)=0.76
```

Voi bai toan nhi phan, temperature van huu ich neu co logits that tu teacher. Neu teacher la LLM API chi tra ve `confidence`, co the dung confidence truc tiep nhung nen xem do la do tin cay tu bao cao, khong phai xac suat da calibration.

### 3.5 Ham mat mat

Huan luyen student ket hop hai nguon tin hieu:

```text
L_total = alpha * L_hard + (1 - alpha) * L_soft
```

Trong do:

```text
L_hard: so sanh student voi nhan goc 0/1
L_soft: so sanh student voi soft label cua teacher
alpha: muc do uu tien nhan goc
```

Voi binary classification:

```text
L_hard = BCE(y, p_student)
L_soft = BCE(q_teacher, p_student)
```

Cong thuc don gian:

```text
L_total = alpha * BCE(y, p_student)
        + (1 - alpha) * BCE(q_teacher, p_student)
```

Neu co logits va dung KL divergence:

```text
L_total = alpha * CE(y, p_student)
        + (1 - alpha) * T^2 * KL(q_teacher^T || p_student^T)
```

`T^2` thuong duoc dung de giu do lon gradient on dinh khi tang temperature.

---

## 4. Vi sao offline soft-label distillation phu hop voi dataset nay

Offline distillation nghia la:

```text
1. Teacher duoc huan luyen/chon truoc.
2. Teacher chay mot lan tren dataset.
3. Teacher outputs duoc luu lai.
4. Student duoc huan luyen tu dataset da co soft labels.
```

Huong nay phu hop vi:

- Dataset chi co 10,562 mau, teacher co the annotate toan bo voi chi phi chap nhan duoc.
- Noi dung ngan, teacher inference nhanh hon so voi van ban dai.
- Hien co nhan cung can bang, nen co baseline ro rang.
- Co cot `data_origin`, giup danh gia rieng real/synthetic/paraphrased/hard negative.
- Khong can thay doi toan bo pipeline ngay tu dau.
- De trinh bay trong khoa luan: baseline hard-label vs student distilled vs teacher.

---

## 5. Teacher models kha di

Teacher can tot hon student ve nang luc bieu dien hoac ve nang luc hieu ngu canh. Co ba nhom kha di.

### 5.1 Teacher encoder tieng Viet

Ung vien:

```text
vinai/phobert-large
```

Ly do:

- PhoBERT la model tieng Viet quen thuoc, phu hop voi du lieu tieng Viet.
- Repo hien tai da co code huan luyen PhoBERT, nen de mo rong.
- Neu student la PhoBERT-base hoac DistilBERT/MiniLM, PhoBERT-large la teacher hop ly.

Han che:

- Can word segmentation bang `pyvi` hoac cong cu tuong duong.
- Kha nang xu ly SMS khong dau, viet tat, URL la, so dien thoai phu thuoc fine-tuning.
- Can GPU de fine-tune thuan tien.

Khuyen nghi:

```text
Teacher: vinai/phobert-large fine-tuned
Student: vinai/phobert-base hoac model nho hon
```

### 5.2 Teacher da ngon ngu

Ung vien:

```text
FacebookAI/xlm-roberta-large
microsoft/mdeberta-v3-base
```

Ly do:

- Xu ly duoc tieng Viet co dau, khong dau, va mot so pattern lai ngon ngu.
- Khong can word segmentation bat buoc nhu PhoBERT.
- Manh voi text classification neu fine-tune dung.

Han che:

- Co the nang hon PhoBERT-base.
- Khong chuyen biet tieng Viet bang PhoBERT trong mot so ngu canh.
- Can thuc nghiem de biet model nao hop domain SMS hon.

Khuyen nghi:

```text
Teacher 1: xlm-roberta-large fine-tuned
Teacher 2: phobert-large fine-tuned
Chon teacher dua tren real-only validation/test.
```

### 5.3 Teacher LLM

Ung vien:

```text
GPT-4.1 / GPT-4o / GPT-5 class qua API
Qwen / Llama / Gemma instruction-tuned local neu co ha tang
```

Ly do:

- Co the sinh `label`, `confidence`, `risk_factors`, `explanation`.
- Phu hop neu muon gan voi Explainable AI va rationale distillation.
- Huu ich de phat hien nhan nhieu hoac mau nhap nhang.

Han che:

- `confidence` cua LLM khong phai logits that.
- Output can duoc rang buoc JSON chat che.
- Chi phi va tinh tai lap phu thuoc model/API.
- Can kiem soat prompt version, temperature, va parsing loi.

Khuyen nghi:

```text
Giai doan 1: dung encoder fine-tuned lam teacher chinh de co logits/probabilities sach.
Giai doan 2: dung LLM bo sung rationale/risk_factors cho explainability.
```

### 5.4 Teacher ensemble

Co the dung nhieu teacher:

```text
Teacher A: phobert-large
Teacher B: xlm-roberta-large
Teacher C: LLM judge
```

Sau do lay trung binh:

```text
teacher_p1 = mean(p1_A, p1_B, p1_C)
```

Hoac dung quy tac:

```text
neu 2/3 teacher dong y va confidence cao -> soft label tin cay
neu bat dong manh -> dua vao tap review
```

Huong nay tot cho chat luong, nhung phuc tap. Khong nen dung ngay trong lan dau.

---

## 6. De xuat thiet ke cho lan trien khai dau tien

### 6.1 Lua chon mac dinh cap nhat: proof-of-concept tiet kiem tai nguyen

Do gioi han GPU tren Kaggle/Colab, khong bat buoc fine-tune teacher lon nhu `vinai/phobert-large` hoac `xlm-roberta-large` trong giai doan dau. Huong uu tien cho proof-of-concept la:

```text
Teacher:
  vinai/phobert-base fine-tuned
  max_length = 128
  epochs = 3
  batch_size = 16 neu GPU chiu duoc

Student 1:
  TF-IDF + Logistic Regression hoac LinearSVC calibrated

Student 2:
  BiLSTM/TextCNN

Student 3 optional:
  MiniLM multilingual
```

Trong thiet ke nay, `vinai/phobert-base` dong vai tro teacher vi no la encoder Transformer tieng Viet manh hon va nang hon cac student du kien. Cac student phai nho hon, nhanh hon, hoac re hon de lap luan distillation co y nghia:

```text
PhoBERT-base teacher -> TF-IDF/Linear model student
PhoBERT-base teacher -> BiLSTM/TextCNN student
PhoBERT-base teacher -> MiniLM multilingual student
```

Day la huong `resource-constrained offline soft-label distillation`: uu tien chung minh pipeline va loi ich cua soft labels trong dieu kien tai nguyen han che. Neu sau nay co GPU tot hon, co the mo rong teacher sang `vinai/phobert-large` hoac `xlm-roberta-large`.

Muc tieu cua proof-of-concept:

```text
Student distilled > Student hard-label baseline
```

Tren cac chi so:

- macro-F1;
- F1 label 1;
- recall label 1 tren `test_real`;
- calibration;
- latency va kich thuoc model.

### 6.2 Lua chon mo rong neu co tai nguyen

De xuat pipeline dau tien:

```text
Teacher: vinai/phobert-large fine-tuned
Student baseline: vinai/phobert-base hard-label
Student distilled: vinai/phobert-base + soft-label loss
```

Neu tai nguyen GPU han che:

```text
Teacher: vinai/phobert-base fine-tuned tot nhat tu cac setup hien co
Student: smaller encoder / BiLSTM / TF-IDF Logistic Regression with teacher probability
```

Ve mat khoa luan, phien ban ro rang nhat la:

```text
Teacher lon hon student:
  PhoBERT-large -> PhoBERT-base
```

Hoac:

```text
Teacher manh hon student:
  XLM-R-large -> PhoBERT-base/MiniLM
```

### 6.3 Cot output can tao

File distilled nen co schema:

```text
content
label
data_origin
teacher_model
teacher_version
teacher_logit_0
teacher_logit_1
teacher_p0_t1
teacher_p1_t1
teacher_p0_t2
teacher_p1_t2
teacher_pred
teacher_confidence
teacher_agree_label
distill_weight
```

Trong do:

- `teacher_p*_t1`: xac suat voi temperature 1.
- `teacher_p*_t2`: xac suat voi temperature duoc chon cho distillation, vi du `T=2`.
- `teacher_confidence`: `max(teacher_p0_t1, teacher_p1_t1)`.
- `teacher_agree_label`: teacher prediction co trung nhan goc khong.
- `distill_weight`: trong so tin vao teacher cho tung mau.

Neu teacher la LLM, co the them:

```text
teacher_rationale
teacher_risk_factors
teacher_output_raw
teacher_parse_ok
prompt_version
```

### 6.4 Khong dua `data_origin` vao model input

Khong nen huan luyen model voi input:

```text
[origin=paraphrased] content...
```

Ly do: `data_origin` co tuong quan qua manh voi label. Model se hoc shortcut:

```text
paraphrased -> label 1
external_real -> label 0
```

Dung `data_origin` cho:

- stratified split;
- sample weighting;
- error analysis;
- bao cao ket qua theo mien du lieu;
- phat hien teacher bias.

---

## 7. Chia train/validation/test

Voi dataset hien tai, can tranh danh gia ao do synthetic/paraphrased chiem nhieu.

De xuat tao cac tap:

### 7.1 Real-only test set

Tap quan trong nhat:

```text
Test_real:
  chi lay data_origin = real
  giu ty le label 0/1 hop ly
```

Vi `real label 1` chi co 246 mau, can chia can than.

Vi du:

```text
real label 1:
  train/val/test = 60/20/20 hoac 70/15/15
```

Khong nen de tat ca real label 1 vao train, vi luc do khong con kiem tra duoc kha nang tong quat tren scam that.

### 7.2 Mixed validation set

Dung de chon checkpoint:

```text
Validation_mixed:
  real + synthetic + paraphrased + hard_negative
```

Nhung phai bao cao rieng theo `data_origin`.

### 7.3 Challenge test set

Tap kho:

```text
synthetic_hard_negative
real label 1
real label 0 co URL/OTP/ngan hang
external_real
```

Muc tieu: kiem tra false positive va false negative o cac mau gan bien.

### 7.4 Nguyen tac bat bien

Teacher co the duoc fine-tune tren train/validation, nhung khi sinh teacher outputs cho test, can ghi ro:

```text
Teacher da tung thay mau test trong qua trinh fine-tune hay chua?
```

De thuc nghiem sach:

```text
1. Chia train/val/test truoc.
2. Fine-tune teacher chi tren train.
3. Chon checkpoint tren val.
4. Sinh teacher outputs cho train/val/test.
5. Huan luyen student chi tren train.
6. Bao cao ket qua tren val/test.
```

---

## 8. Pipeline trien khai

### 8.1 Buoc 1: Tao split co kiem soat

Input:

```text
data/final/vismishds_content_label_origin.csv
```

Output:

```text
data/distillation/splits/train.csv
data/distillation/splits/val.csv
data/distillation/splits/test_real.csv
data/distillation/splits/test_mixed.csv
data/distillation/splits/test_challenge.csv
```

Yeu cau:

- split theo `label` va `data_origin`;
- giu rieng test real;
- dam bao khong trung `content` giua cac split;
- luu random seed.

### 8.2 Buoc 2: Fine-tune teacher

Input:

```text
train.csv
val.csv
```

Teacher objective:

```text
content -> label
```

Metric chon checkpoint:

```text
macro_f1
f1_label_1
recall_label_1_real_val
```

Khong nen chi dung accuracy.

Output:

```text
models/teacher/phobert_large/
setup_results/distillation/teacher_metrics.json
```

### 8.3 Buoc 3: Sinh teacher outputs

Teacher chay inference tren tat ca split:

```text
train
val
test_real
test_mixed
test_challenge
```

Output:

```text
data/distillation/teacher_outputs/train_teacher.csv
data/distillation/teacher_outputs/val_teacher.csv
data/distillation/teacher_outputs/test_real_teacher.csv
...
```

Moi file can co:

```text
content,label,data_origin,teacher_logit_0,teacher_logit_1,teacher_p0,teacher_p1,teacher_pred,teacher_confidence,teacher_agree_label
```

### 8.4 Buoc 4: Audit teacher outputs

Can thong ke:

```text
teacher accuracy/f1 theo split
teacher accuracy/f1 theo data_origin
teacher disagreement voi label
top mau teacher_confidence cao nhung khac label
top mau teacher_confidence thap
phan bo teacher_p1 theo label va data_origin
```

Muc dich:

- phat hien label noise;
- phat hien teacher qua nhay voi synthetic pattern;
- phat hien shortcut theo nguon du lieu;
- quyet dinh co can review/sua nhan hay khong.

### 8.5 Buoc 5: Huan luyen student baseline

Baseline:

```text
Student hard-label:
  input: content
  target: label
  loss: CE/BCE voi nhan cung
```

Can co baseline truoc khi distillation de chung minh gia tri cua teacher outputs.

### 8.6 Buoc 6: Huan luyen student distilled

Student distilled:

```text
input: content
target 1: label
target 2: teacher_p1 hoac teacher logits
loss: alpha * hard_loss + (1 - alpha) * soft_loss
```

Gia tri thu nghiem:

```text
alpha = 0.3, 0.5, 0.7
T = 1, 2, 4
```

Neu teacher la LLM confidence:

```text
T = 1
soft_loss = BCE(teacher_p1, student_p1)
```

Neu teacher co logits:

```text
T = 2 hoac 4
soft_loss = KL(softmax(teacher_logits/T), softmax(student_logits/T))
```

### 8.7 Buoc 7: Danh gia

So sanh it nhat ba mo hinh:

| Model | Mo ta |
|---|---|
| Teacher | Mo hinh lon fine-tuned |
| Student baseline | Student hoc nhan cung |
| Student distilled | Student hoc nhan cung + soft label |

Chi so:

```text
accuracy
precision label 1
recall label 1
f1 label 1
macro_f1
weighted_f1
roc_auc
pr_auc
confusion matrix
ece/calibration
model size
latency
```

Bao cao rieng:

```text
test_real
test_mixed
test_challenge
theo data_origin
theo label
```

Thanh cong duoc xem la:

```text
Student distilled > Student baseline
```

Ve:

- macro-F1;
- F1 label 1;
- recall label 1 tren real;
- calibration;
- hoac latency/model size trong khi chat luong gan teacher.

---

## 9. Sample weighting theo do tin cay

Khong phai moi teacher output deu dang tin nhu nhau.

Co the dat:

```text
teacher_agree_label = teacher_pred == label
```

Va gan trong so:

```text
neu teacher dong y label va confidence cao:
  distill_weight = 1.0

neu teacher dong y label nhung confidence thap:
  distill_weight = 0.7

neu teacher khac label:
  distill_weight = 0.3
```

Loss:

```text
L_total = alpha * L_hard
        + (1 - alpha) * distill_weight * L_soft
```

Ly do:

- Neu teacher va label dong y, soft label co the giup student hoc do chac chan.
- Neu teacher va label bat dong, mau nay co the la label noise hoac teacher error.
- Khong nen de teacher keo student qua manh o cac mau bat dong.

Co the dung quy tac rieng cho `data_origin`:

```text
real:
  tin nhan that, nen uu tien nhan goc hon neu da duoc xac minh

synthetic/paraphrased:
  co nguy co pattern lap, nen can audit teacher ky hon

synthetic_hard_negative:
  huu ich cho decision boundary, nhung de gay lech neu tao sinh qua cong thuc
```

---

## 10. Cac thuc nghiem de dua vao khoa luan

### Experiment A: Hard-label baseline

```text
Train: train.csv
Target: label
Model: student
```

Muc tieu:

```text
Tao moc so sanh.
```

### Experiment B: Soft-label distillation

```text
Train: train_teacher.csv
Target: label + teacher_p
Model: student
```

Muc tieu:

```text
Kiem tra teacher soft labels co cai thien student khong.
```

### Experiment C: Temperature ablation

```text
T = 1, 2, 4
```

Muc tieu:

```text
Kiem tra muc lam mem xac suat nao phu hop.
```

### Experiment D: Alpha ablation

```text
alpha = 0.3, 0.5, 0.7
```

Muc tieu:

```text
Kiem tra nen tin nhan goc hay teacher output nhieu hon.
```

### Experiment E: Data-origin evaluation

Bao cao:

```text
real
synthetic
paraphrased
synthetic_hard_negative
external_real
external_curated
```

Muc tieu:

```text
Phat hien student distilled co hoc shortcut theo nguon du lieu hay khong.
```

### Experiment F: Teacher disagreement audit

Tach cac mau:

```text
teacher_pred == label
teacher_pred != label
```

Muc tieu:

```text
Kiem tra cac mau bat dong co phai label noise hoac mau kho that su khong.
```

---

## 11. Rationale distillation trong giai doan sau

Offline soft-label distillation nen la giai doan 1.

Sau khi co pipeline on dinh, co the mo rong sang Explainable AI:

```text
content -> label
content -> teacher_p1
content -> risk_factors
content -> explanation
```

Vi du risk factors:

```text
link_la
mao_danh_ngan_hang
mao_danh_co_quan_nha_nuoc
yeu_cau_xac_minh
tao_ap_luc_thoi_gian
yeu_cau_cung_cap_otp
hua_hen_trung_thuong
noi_dung_nhay_cam
```

Co the dung LLM de sinh:

```json
{
  "label": 1,
  "confidence": 0.94,
  "risk_factors": ["link_la", "yeu_cau_xac_minh", "tao_ap_luc_thoi_gian"],
  "explanation": "Tin nhan yeu cau xac minh tai khoan qua duong link khong chinh thuc va tao ap luc trong thoi gian ngan."
}
```

Nhung can tach ro:

```text
soft-label distillation: dung cho cai thien classifier
rationale distillation: dung cho giai thich va phan tich loi
```

Khong nen tron ca hai ngay tu dau neu chua co baseline vung.

---

## 12. Rui ro va cach giam thieu

### 12.1 Teacher hoc shortcut theo synthetic pattern

Rui ro:

```text
Teacher thay paraphrased gan nhu toan label 1, synthetic gan nhieu label 0.
```

Giam thieu:

- split va bao cao theo `data_origin`;
- khong dua `data_origin` vao input;
- dung real-only test;
- audit prediction distribution theo origin.

### 12.2 Teacher sai nhung confidence cao

Rui ro:

```text
Student hoc lai loi cua teacher.
```

Giam thieu:

- dung `teacher_agree_label`;
- review mau bat dong confidence cao;
- giam `distill_weight` khi teacher khac label;
- neu co dieu kien, dung ensemble teacher.

### 12.3 LLM confidence khong calibrated

Rui ro:

```text
LLM noi confidence=0.95 nhung khong tuong ung xac suat that.
```

Giam thieu:

- uu tien encoder teacher co logits cho giai doan 1;
- neu dung LLM, goi la `teacher_confidence`, khong goi la calibrated probability;
- dung LLM chu yeu cho rationale/risk factors.

### 12.4 Student khong du dung luong hoc teacher

Rui ro:

```text
Student qua nho, khong bat chuoc duoc teacher.
```

Giam thieu:

- bat dau voi student vua phai nhu PhoBERT-base;
- sau do moi thu MiniLM/BiLSTM/TF-IDF;
- bao cao trade-off chat luong kich thuoc toc do.

---

## 13. Cau truc thu muc de xuat

```text
data/
  distillation/
    splits/
      train.csv
      val.csv
      test_real.csv
      test_mixed.csv
      test_challenge.csv
    teacher_outputs/
      train_teacher.csv
      val_teacher.csv
      test_real_teacher.csv
      test_mixed_teacher.csv
      test_challenge_teacher.csv
    audits/
      teacher_disagreement.csv
      teacher_probability_summary.csv

models/
  teacher/
    phobert_large/
  student/
    phobert_base_hard/
    phobert_base_distilled/

setup_results/
  distillation/
    teacher_metrics.json
    student_baseline_metrics.json
    student_distilled_metrics.json
    comparison_report.md
```

---

## 14. Ke hoach trien khai theo thu tu uu tien

### Phase 1: Chuan bi va split

1. Tao script split dataset.
2. Kiem tra phan bo `label x data_origin`.
3. Luu split co seed co dinh.
4. Tao test_real va test_challenge.

### Phase 2: Teacher

1. Fine-tune `vinai/phobert-large` hoac teacher kha dung nhat.
2. Chon checkpoint theo macro-F1 va recall label 1.
3. Sinh logits/probabilities cho cac split.
4. Audit teacher disagreement.

### Phase 3: Student baseline

1. Huan luyen student chi voi nhan cung.
2. Luu metric va confusion matrix.
3. Bao cao rieng tren real-only test.

### Phase 4: Student distilled

1. Huan luyen student voi `hard_loss + soft_loss`.
2. Thu cac gia tri `alpha`, `T`.
3. So sanh voi baseline.
4. Phan tich error cases.

### Phase 5: Mo rong XAI

1. Dung LLM/teacher sinh risk factors.
2. Tao tap rationale/risk-factor labels.
3. Huan luyen model phu hoac multi-task student.
4. Danh gia tinh dung va tinh huu ich cua giai thich.

---

## 15. Ket luan dinh huong

Dataset hien tai rat phu hop de bat dau voi offline soft-label distillation vi:

- da co nhan nhi phan can bang;
- noi dung ngan, de chay inference teacher;
- co nhieu nguon du lieu khac nhau de danh gia robustness;
- co hard negatives va paraphrases, huu ich cho hoc decision boundary;
- co the tao baseline ro rang bang PhoBERT hien co.

Huong trien khai duoc khuyen nghi:

```text
1. Chia split sach, uu tien real-only test.
2. Fine-tune teacher lon, uu tien PhoBERT-large hoac XLM-R-large.
3. Sinh teacher logits/probabilities.
4. Audit teacher outputs.
5. Huan luyen student baseline va student distilled.
6. So sanh theo F1 label 1, recall label 1 tren real, calibration, latency va model size.
```

Thanh cong mong doi:

```text
Student distilled nho va nhanh hon teacher,
nhung tot hon student hard-label baseline,
dac biet tren cac mau real va hard negative.
```

---

## 16. Tai lieu tham khao nen trich dan

- Hinton, Vinyals, Dean. "Distilling the Knowledge in a Neural Network", 2015.
- Sanh et al. "DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter", 2019.
- Jiao et al. "TinyBERT: Distilling BERT for Natural Language Understanding", 2019.
- Model card `vinai/phobert-large`.
- Model card `FacebookAI/xlm-roberta-large`.
- Model card `microsoft/mdeberta-v3-base`.
