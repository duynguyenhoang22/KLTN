# Distillation POC Phase 5 Readiness Note

> Muc dich: Tai lieu nay ghi lai cac quyet dinh va khuc mac quan trong truoc khi trien khai Phase 5 cua proof-of-concept offline soft-label distillation cho ViSmishDS.
>
> Trang thai: Phase 1-4 da hoan thanh voi split v2. Phase 5 tiep theo la train student hard-label baseline.

---

## 1. Ket luan ngan gon

Co the tiep tuc Phase 5, nhung khong nen dien giai teacher hien tai la mot oracle manh tren moi mien du lieu.

Teacher PhoBERT-base hien tai co ket qua rat cao tren `test_mixed` va `test_challenge`, nhung tren benchmark quan trong nhat la `test_real`, recall Label 1 chi dat `0.6757`. Day la mot tin hieu can than trong vi bai toan smishing uu tien khong bo sot tin lua dao. Neu student hoc qua manh theo soft labels cua teacher, student co nguy co hoc lai chinh cac false negative cua teacher.

Vi vay, POC nen duoc trien khai theo huong:

```text
Hard label la nguon giam sat chinh.
Soft label cua teacher la tin hieu phu co trong so.
Teacher disagreements, dac biet label=1 nhung teacher_pred=0, phai bi giam anh huong.
```

Noi cach khac, POC khong hoi:

```text
Teacher co du tot de thay the nhan that khong?
```

Ma hoi:

```text
Teacher probabilities co giup student nho hon cai thien so voi chinh hard-label baseline cua no khong?
```

Day la khung dien giai an toan va hop ly hon cho luan van.

---

## 2. Trang thai artifact hien tai

Split chinh tu Phase 5 tro di:

```text
data/distillation/splits_v2/
```

Teacher outputs chinh:

```text
data/distillation/teacher_outputs_v2/
```

Bao cao split va audit:

```text
setup_results/distillation/split_report_v2.md
setup_results/distillation_v2/teacher_phobert_base_report.md
setup_results/distillation_v2/teacher_audit/teacher_audit_report.md
setup_results/distillation_v2/teacher_audit/teacher_metrics_by_split.csv
setup_results/distillation_v2/teacher_audit/teacher_metrics_by_data_origin.csv
```

Trang thai phase:

```text
Phase 1: Split dataset v2                 DONE
Phase 2: Fine-tune PhoBERT-base teacher   DONE
Phase 3: Generate teacher outputs v2      DONE
Phase 4: Audit teacher outputs v2         DONE
Phase 5: Student hard-label baseline      NEXT
Phase 6: Student distilled                AFTER PHASE 5
```

---

## 3. Ket qua teacher can ghi nho

Ket qua teacher v2 theo split:

| split | rows | accuracy | macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| train | 7,212 | 0.9978 | 0.9978 | 0.9979 | 0.9974 | 0.9984 | 0.9999 |
| val | 1,186 | 0.9882 | 0.9881 | 0.9870 | 0.9870 | 0.9870 | 0.9988 |
| test_real | 385 | 0.9636 | 0.8807 | 0.7812 | 0.6757 | 0.9259 | 0.8427 |
| test_mixed | 1,059 | 0.9906 | 0.9906 | 0.9905 | 0.9886 | 0.9924 | 0.9992 |
| test_challenge | 720 | 0.9903 | 0.9899 | 0.9878 | 0.9861 | 0.9895 | 0.9987 |

Dien giai:

- `test_real` la benchmark chinh va kho nhat.
- Teacher co precision Label 1 cao tren `test_real` (`0.9259`), nghia la khi teacher goi mot mau la smishing thi kha dang tin.
- Teacher co recall Label 1 thap tren `test_real` (`0.6757`), nghia la teacher bo sot kha nhieu smishing that.
- Ket qua rat cao tren `test_mixed` va `test_challenge` khong du de xoa bo lo ngai tren `test_real`.

Ket qua teacher tren phan `real` cua cac split:

| split | rows real | macro-F1 | F1 Label 1 | Recall Label 1 | Precision Label 1 |
|---|---:|---:|---:|---:|---:|
| val/real | 385 | 0.9168 | 0.8493 | 0.8378 | 0.8611 |
| test_real | 385 | 0.8807 | 0.7812 | 0.6757 | 0.9259 |
| test_mixed/real | 258 | 0.9045 | 0.8261 | 0.7600 | 0.9048 |
| test_challenge/real | 258 | 0.9557 | 0.9200 | 0.9200 | 0.9200 |

Diem can de phong:

```text
Teacher khong yeu tren moi split.
Nhung teacher co mot diem yeu quan trong: recall smishing that tren test_real.
```

---

## 4. Lo ngai chinh: teacher recall Label 1 thap co nguy hiem khong?

Co. Day la lo ngai dung.

Trong bai toan smishing, Label 1 la lop rui ro cao. False negative co nghia la tin lua dao bi xem la hop le. Neu teacher da bo sot cac mau Label 1 tren `test_real`, viec bat student hoc manh theo soft label cua teacher co the lam student:

- giam do nhay voi cac mau smishing kho;
- hoc shortcut rang nhung tin co van phong gan voi thong bao hop le nen la Label 0;
- cai thien accuracy hoac precision nhung lam xau recall Label 1;
- dat ket qua dep tren mixed/challenge nhung yeu tren real smishing.

Vi vay, teacher recall thap khong phai la mot tin hieu "tot". No la mot rui ro can duoc kiem soat.

Tuy nhien, teacher khong vo dung. Teacher co precision Label 1 cao tren `test_real`, nen co the duoc xem la teacher bao thu:

```text
Teacher khong bat het smishing.
Nhung khi teacher chac mot mau la smishing, du doan nay thuong dang tin.
```

Gia tri cua teacher trong POC vi the nam o soft signal co dieu kien, khong nam o viec thay the nhan that.

---

## 5. Teacher thap co khi nao lai tot?

Can tach ro hai y:

```text
Teacher thap ve recall Label 1: khong tot neu dung teacher nhu oracle.
Teacher khong hoan hao: co the chap nhan duoc neu dung teacher nhu regularizer/tin hieu phu.
```

Mot teacher qua manh va qua tu tin co the lam POC tro thanh bai toan "student bat chuoc oracle". Dieu nay dep ve mat ket qua nhung doi khi kho phan tich trong dieu kien tai nguyen han che.

Nguoc lai, mot teacher vua phai co the van huu ich neu no cung cap:

- thong tin ve muc do chac chan cua mau;
- do mem cho cac mau sat bien;
- tin hieu calibration cho student;
- cach phan bo xac suat tot hon hard label 0/1.

Nhung "teacher vua phai" khong dong nghia voi "teacher false negative cao la tot". Voi bai toan smishing, false negative cua teacher la loai loi can chan truyen sang student.

Ket luan:

```text
Teacher hien tai co the dung cho POC, nhung chi nen dung voi distillation co trong so va hard-label anchor manh.
```

---

## 6. Student co nen hoc tu teacher recall Label 1 = 0.6757 khong?

Co, neu "hoc tu teacher" duoc hieu la hoc them tin hieu phu.

Khong, neu "hoc tu teacher" duoc hieu la thay nhan that bang soft label cua teacher.

Thiet ke nen dung:

```text
Student hard-label baseline:
  student hoc truc tiep content -> label

Student distilled:
  student hoc label that + teacher probability
```

Khong nen dung:

```text
Student distilled:
  student chi hoc teacher probability
```

Cong thuc cho neural student:

```text
loss = alpha * CE(student_logits, hard_label)
     + (1 - alpha) * distill_weight * KL(student_T, teacher_T)
```

Trong do:

- `CE` giu nhan that lam diem neo.
- `KL` giup student hoc phan bo xac suat cua teacher.
- `alpha` nen cao, vi teacher co recall Label 1 thap tren `test_real`.
- `distill_weight` giam anh huong cua teacher tren cac mau bat dong voi nhan that.

Gia tri khoi dau nen dung:

```text
alpha = 0.7 hoac 0.8
temperature = 2.0
distill_weight = 1.0 cho teacher_agree_label=True
distill_weight = 0.3 hoac 0.0 cho teacher_agree_label=False
```

Rieng truong hop nhay cam nhat:

```text
label = 1 va teacher_pred = 0
```

Day la false negative cua teacher. Nen giam manh distillation loss:

```text
distill_weight = 0.0 hoac rat thap
```

Ly do:

```text
Khong nen de teacher day student xem smishing that la hop le.
```

---

## 7. Tai sao Phase 5 phai la hard-label baseline truoc?

Phase 5 khong phai buoc phu. No la moc doi chieu bat buoc.

Neu khong co hard-label baseline, ta se khong tra loi duoc cau hoi:

```text
Distillation co giup gi khong?
```

Vi student distilled chi co y nghia khi so sanh voi chinh student cung kien truc nhung chi hoc hard label:

```text
TF-IDF + Logistic Regression hard-label
vs
TF-IDF + Logistic Regression distilled/calibrated
```

Hoac:

```text
BiLSTM hard-label
vs
BiLSTM distilled
```

Neu student distilled tot hon teacher nhung khong tot hon hard-label baseline, thi distillation khong co loi ich ro rang cho student do.

Neu student distilled tot hon hard-label baseline tren `test_mixed`/`test_challenge` nhung kem hon tren `test_real`, ket luan phai than trong:

```text
Distillation co the giup tren mixed/challenge distribution,
nhung chua cai thien kha nang tong quat tren real SMS.
```

Neu student distilled cai thien calibration hoac precision nhung lam giam recall Label 1, can bao cao ro trade-off. Khong nen chi bao cao accuracy.

---

## 8. Tai sao khong nhay thang vao E4 hoac G2 ngay tu dau?

E4/G2 tra loi cau hoi:

```text
Setup du lieu nao giup PhoBERT classifier tot hon?
```

Distillation POC tra loi cau hoi khac:

```text
Soft labels tu teacher co giup student nho hon tot hon hard-label baseline khong?
```

Neu nhay thang vao champion setup ma khong co baseline student va teacher audit, ket qua se bi tron hai hieu ung:

```text
Hieu ung setup du lieu: G2 tot vi them external curated Label 0.
Hieu ung distillation: student tot vi hoc teacher probabilities.
```

Khi hai hieu ung bi tron, se kho noi trong luan van rang distillation thuc su co dong gop gi.

Tuy vay, bai hoc tu G2 van nen duoc ke thua. Teacher distillation v2 hien tai da co tinh than do: train split co `external_curated` va `external_real` Label 0, giup mo rong mien negative va giam nguy co false positive tren external Label 0.

Ket luan dung:

```text
Khong bo qua bai hoc E4/G2.
Nhung trong POC, can tach baseline student va distilled student de chung minh rieng tac dong cua distillation.
```

---

## 9. Phase 5 nen trien khai nhu the nao?

Phase 5 chi train hard-label student baseline. Chua dung teacher outputs de toi uu student.

Student dau tien:

```text
TF-IDF + Logistic Regression
```

Input:

```text
data/distillation/splits_v2/train.csv
data/distillation/splits_v2/val.csv
```

Evaluation:

```text
data/distillation/splits_v2/test_real.csv
data/distillation/splits_v2/test_mixed.csv
data/distillation/splits_v2/test_challenge.csv
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

Ly do:

```text
Phase 5 can do nang luc text-only baseline.
Metadata chi dung de audit loi va bao cao subgroup.
```

Metric bat buoc:

```text
accuracy
macro_f1
f1_label_1
recall_label_1
precision_label_1
roc_auc neu co probability
pr_auc neu co probability
confusion matrix
```

Bao cao phai tach:

```text
test_real
test_mixed
test_challenge
```

Va neu co the, phan tich them theo:

```text
data_origin
category
has_url
has_phone_number
sender_type
obfuscation_level
```

Tieu chi thanh cong cua Phase 5:

```text
Co mot hard-label baseline tai lap duoc.
Co metrics day du tren 3 test split.
Co error files de so voi teacher va Phase 6.
```

Phase 5 khong can thang teacher. Phase 5 can lam moc doi chieu ro rang cho Phase 6.

---

## 10. Phase 6 nen chong rui ro teacher nhu the nao?

Phase 6 moi dung teacher outputs.

Du lieu:

```text
data/distillation/teacher_outputs_v2/train_teacher.csv
data/distillation/teacher_outputs_v2/val_teacher.csv
data/distillation/teacher_outputs_v2/test_real_teacher.csv
data/distillation/teacher_outputs_v2/test_mixed_teacher.csv
data/distillation/teacher_outputs_v2/test_challenge_teacher.csv
```

Nhung Phase 6 khong nen hoc soft label mot cach dong nhat. Can co safety rules:

| Truong hop | Cach dung teacher |
|---|---|
| `teacher_agree_label=True` | Dung soft label voi weight cao hon |
| `teacher_agree_label=False` | Giam weight hoac bo KL |
| `label=1`, `teacher_pred=0` | Giam manh weight, uu tien hard label |
| `label=0`, `teacher_pred=1` | Co the giu weight thap de hoc uncertainty, nhung can theo doi FP |
| Teacher confidence thap | Co the dung nhu mau sat bien |
| Teacher confidence cao nhung sai | Khong duoc hoc manh theo teacher |

Neu dung neural student:

```text
alpha = 0.7 or 0.8
temperature = 2.0
distill_weight from teacher output
```

Neu dung TF-IDF + Logistic Regression:

Khong co KL loss truc tiep theo kieu neural logits, nen co the chon mot trong cac bien the nhe:

```text
1. Hard-label baseline only trong Phase 5.
2. Soft-target logistic regression bang pseudo-probability objective neu implementation ho tro.
3. Sample weighting/label smoothing dua tren teacher_p1 va distill_weight.
4. Calibration sau hard-label training bang teacher probabilities tren train/val, nhung phai bao cao ro day la calibration-style distillation.
```

Dieu quan trong:

```text
Moi bien the distilled phai so voi chinh baseline cung kien truc.
```

---

## 11. Cac cau hoi khuc mac va tra loi ngan

### Q1. Ket qua teacher thap lieu co la tot?

Khong, neu "thap" la recall Label 1 thap tren real smishing.

Teacher recall Label 1 = `0.6757` tren `test_real` la mot diem yeu can bao cao. No khong nen duoc xem la uu diem.

Tuy nhien, teacher khong can hoan hao de dung trong POC. Teacher co the cung cap soft probabilities nhu tin hieu phu, mien la hard labels van la giam sat chinh va cac loi teacher duoc giam trong so.

### Q2. Student co nen hoc tu teacher recall Label 1 thap khong?

Co, nhung khong hoc mu quang.

Student nen hoc:

```text
hard label + teacher signal co trong so
```

Student khong nen hoc:

```text
teacher signal thay the hard label
```

### Q3. Neu teacher bo sot smishing, student co bi bo sot theo khong?

Co the, neu KL/soft-label loss qua manh.

Giam rui ro bang cach:

```text
alpha cao cho hard-label CE
distill_weight thap cho teacher disagreement
distill_weight gan 0 cho label=1 nhung teacher_pred=0
theo doi recall Label 1 tren test_real
```

### Q4. Teacher precision cao nhung recall thap co nghia la gi?

Teacher dang bao thu voi Label 1.

Nghia la:

```text
Khi teacher du doan smishing, thuong dung.
Nhung teacher khong bat het smishing.
```

Day co the huu ich cho cac tin hieu smishing chac chan, nhung khong du de lam nguon nhan thay the.

### Q5. Neu student distilled tang precision nhung giam recall Label 1 thi co xem la tot khong?

Khong nen mac dinh la tot.

Voi smishing, recall Label 1 la metric rat quan trong. Neu precision tang nhe nhung recall giam manh, day co the la trade-off khong chap nhan duoc. Bao cao nen neu ro:

```text
distilled student improves precision/calibration but hurts detection sensitivity
```

### Q6. Co nen dung `test_mixed` va `test_challenge` lam bang chung chinh khong?

Khong.

`test_real` la benchmark chinh. `test_mixed` va `test_challenge` la bo danh gia phu de xem model co on dinh tren mixed/source-augmented distribution khong.

### Q7. Co nen doi teacher truoc Phase 5 khong?

Chua nen, neu muc tieu truoc mat la POC tiet kiem thoi gian.

Nen lam Phase 5 truoc de co student hard-label baseline. Sau do moi quyet dinh co can retrain teacher, doi teacher theo G2 chat hon, hay them threshold tuning khong.

### Q8. Co nen tune threshold cho teacher de tang recall Label 1 khong?

Co the can, nhung khong nen dung test set de tune.

Neu lam, chi tune threshold tren validation set, roi bao cao ket qua tren test. Tuy nhien, threshold tuning cua teacher khong thay the duoc Phase 5. No la mot bien the bo sung neu can cai thien teacher outputs truoc Phase 6.

### Q9. Neu teacher khong tot hon student hard-label thi distillation co con y nghia khong?

Van co the co y nghia, nhung ket luan phai khiem ton.

Mot teacher co the khong thang student tren tat ca metric, nhung soft labels van co the giup:

- calibration;
- precision/recall trade-off;
- on dinh hon tren mixed/challenge;
- giam model size trong khi giu chat luong gan teacher.

Neu khong co cai thien nao, do cung la ket qua hop le cua POC:

```text
Trong dieu kien teacher hien tai, soft-label distillation chua mang lai loi ich ro rang so voi hard-label baseline.
```

### Q10. Ket luan an toan cho luan van nen viet the nao?

Nen viet:

```text
Teacher PhoBERT-base duoc dung nhu nguon soft supervision co kiem soat, khong phai nguon nhan thay the. Do teacher co recall Label 1 han che tren real test, qua trinh distillation giu hard-label supervision lam thanh phan chinh va giam anh huong cua teacher tren cac mau bat dong voi nhan that. Thiet lap nay nham danh gia lieu teacher probabilities co cai thien student nho hon ve hieu nang, calibration, hoac trade-off precision/recall trong dieu kien tai nguyen han che hay khong.
```

---

## 12. Go/No-Go truoc Phase 5

Quyet dinh:

```text
GO cho Phase 5.
```

Ly do:

- Phase 5 chi train hard-label baseline, chua phu thuoc vao viec teacher co hoan hao hay khong.
- Phase 5 la moc bat buoc de danh gia Phase 6.
- Lo ngai teacher recall thap khong chan Phase 5; no anh huong den cach thiet ke Phase 6.

Dieu kien khi sang Phase 6:

```text
Khong dung teacher soft labels nhu nhan thay the.
Khong toi uu alpha/temperature/threshold tren test set.
Khong bo qua recall Label 1 tren test_real.
Khong chi bao cao accuracy.
Phai so sanh distilled student voi hard-label baseline cung kien truc.
```

---

## 13. Checklist hanh dong tiep theo

Phase 5:

- Train TF-IDF + Logistic Regression hard-label baseline.
- Luu model/config/vectorizer neu can tai lap.
- Evaluate tren `test_real`, `test_mixed`, `test_challenge`.
- Luu metrics JSON/CSV.
- Luu predictions va errors cho tung split.
- Bao cao confusion matrix va cac metric Label 1.

Sau Phase 5:

- So sanh hard-label student voi teacher tren cung cac split.
- Kiem tra student co recall Label 1 tren `test_real` cao hon teacher khong.
- Neu student hard-label da thang teacher ve recall Label 1, Phase 6 phai rat can than de khong lam mat loi the nay.
- Chon bien the Phase 6 co hard-label anchor manh va disagreement down-weighting.

