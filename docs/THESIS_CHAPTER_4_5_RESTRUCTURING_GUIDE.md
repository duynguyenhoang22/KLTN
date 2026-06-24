# SƯỜN CHỈ DẪN TÁI CẤU TRÚC CHƯƠNG 4–5

## 1. Mục đích của tài liệu

Tài liệu này là khung tham chiếu bắt buộc khi chỉnh sửa phần thực nghiệm và phân tích kết quả của khóa luận ViSmish. Mọi nội dung viết mới từ Chương 4 trở đi cần tuân theo cấu trúc và mạch lập luận được quy định tại đây.

Mục tiêu của việc tái cấu trúc:

1. Đưa benchmark nhiều mô hình trở thành thực nghiệm trung tâm.
2. Loại bỏ cách tổ chức báo cáo thành hai nhánh thực nghiệm độc lập.
3. Xem các mô hình distilled là cấu hình thuộc benchmark, không phải một nhánh nghiên cứu riêng.
4. Xem TSTR và các setup augmentation là bằng chứng để phân tích giá trị của dữ liệu tạo sinh.
5. Tổ chức chương kết quả theo các câu hỏi nghiên cứu lớn.
6. Đào sâu phân tích dữ liệu và kết quả theo độ dài, mức độ che giấu và các metadata liên quan.

---

## 2. Các nguyên tắc bắt buộc

### 2.1. Không sử dụng lại cấu trúc “hai nhánh thực nghiệm”

Không tiếp tục trình bày:

- Nhánh 1: Đánh giá dữ liệu tạo sinh.
- Nhánh 2: Knowledge Distillation.

Benchmark mô hình là thực nghiệm chính. TSTR, augmentation, external challenge và distillation là các lát cắt hoặc cấu hình bổ sung phục vụ những câu hỏi nghiên cứu cụ thể.

### 2.2. Không trình bày kết quả theo thứ tự Setup A–G

Các setup vẫn có thể được giữ làm mã tham chiếu kỹ thuật, nhưng không được dùng làm xương sống của chương kết quả.

Thay vì lần lượt kể “Setup A cho kết quả…, Setup B cho kết quả…”, cần bắt đầu từ câu hỏi cần trả lời, sau đó chọn các setup liên quan làm bằng chứng.

Ví dụ:

> Dữ liệu tạo sinh có thể thay thế dữ liệu thật không?

Sau đó dùng kết quả Real-only và TSTR để trả lời.

### 2.3. Phân biệt rõ dev và test

- Dev được dùng để lựa chọn mô hình, checkpoint, threshold và thực hiện phân tích kết quả chi tiết.
- Test chỉ dùng để báo cáo khả năng tổng quát hóa cuối cùng.
- Không lựa chọn mô hình tốt nhất dựa trên kết quả test.
- Các phân tích lát cắt và phân tích lỗi chính nên được thực hiện trên dev theo yêu cầu của giảng viên.

### 2.4. Phải thống nhất giao thức dữ liệu trước khi chốt số liệu

Hiện tồn tại hai giao thức:

- Real-only protocol: test khoảng 386 mẫu, chỉ gồm dữ liệu thật.
- Benchmark protocol: dev và test mỗi tập 535 mẫu, gồm dữ liệu real và external Label 0.

Khi viết cần:

1. Chọn một giao thức chính cho benchmark.
2. Mô tả rõ thành phần từng split.
3. Nếu giữ cả hai, phải đặt tên rõ là `real test` và `extended/challenge test`.
4. Không đặt các bảng sử dụng hai giao thức cạnh nhau mà không giải thích sự khác biệt.

### 2.5. Mỗi mục kết quả phải trả lời một ý lớn

Cấu trúc lập luận chuẩn:

1. Nêu câu hỏi.
2. Nêu bằng chứng định lượng.
3. Giải thích xu hướng.
4. Kiểm tra bằng phân tích lát cắt hoặc ví dụ lỗi.
5. Đưa ra kết luận ngắn và giới hạn của kết luận.

---

## 3. Các câu hỏi nghiên cứu

Các chương thực nghiệm cần xoay quanh ba câu hỏi:

### RQ1 — So sánh mô hình

Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu ViSmish?

### RQ2 — Ảnh hưởng của đặc điểm dữ liệu

Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế nào đến khả năng phát hiện smishing?

### RQ3 — Phân tích lỗi

Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân có thể là gì?

---

# 4. SƯỜN CHƯƠNG 4 — PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM

## 4.1. Tổng quan thiết kế thực nghiệm

Nội dung cần có:

- Mục tiêu tổng quát của thực nghiệm.
- Ba câu hỏi nghiên cứu RQ1–RQ3.
- Sơ đồ quy trình từ dữ liệu, huấn luyện benchmark, đánh giá đến phân tích kết quả.
- Giải thích benchmark là trục thực nghiệm chính.

Không sử dụng cụm từ “hai nhánh thực nghiệm”.

## 4.2. Dữ liệu và chiến lược phân chia

### 4.2.1. Thành phần dữ liệu

Trình bày các nguồn:

- `real`
- `external_real`
- `external_curated`
- `synthetic`
- `paraphrased`
- `synthetic_hard_positive`

Làm rõ nguồn nào xuất hiện trong train, dev và test.

### 4.2.2. Chiến lược chia tập

Trình bày:

- Tỷ lệ train/dev/test.
- Seed chia dữ liệu.
- Stratification theo `label × data_origin × category`.
- Synthetic chỉ được đưa vào train.
- Dev và test không chứa dữ liệu tạo sinh.
- Quy tắc xử lý các strata quá nhỏ.

### 4.2.3. Kiểm tra rò rỉ dữ liệu

Tối thiểu gồm:

- Trùng `sample_id`.
- Trùng nội dung chính xác.
- Trùng nội dung sau chuẩn hóa.
- Nếu có điều kiện, kiểm tra near-duplicate.

### 4.2.4. Vai trò của dev và test

Nêu rõ:

- Dev: chọn checkpoint, lựa chọn mô hình, điều chỉnh threshold và result analysis.
- Test: đánh giá cuối cùng.

## 4.3. Các mô hình benchmark

### 4.3.1. Mô hình character-level

- BiLSTM.
- TextCNN.

Giải thích lý do chọn mô hình ký tự: phù hợp với SMS ngắn, viết tắt, lỗi chính tả, leet và obfuscation.

### 4.3.2. Mô hình character-level có distillation

- BiLSTM distilled từ PhoBERT-base.
- TextCNN distilled từ PhoBERT-base.

Chỉ mô tả distillation như một biến thể huấn luyện trong benchmark. Không xây dựng thành nhánh thực nghiệm riêng.

### 4.3.3. Các pretrained language model

- PhoBERT-base.
- PhoBERT-large.
- mBERT.
- VisoBERT.
- CafeBERT.
- DistilBERT multilingual.
- XLM-RoBERTa-base.
- XLM-RoBERTa-large.
- ViCLSR.

Nên nhóm và so sánh theo:

- Đơn ngữ và đa ngữ.
- Base và large.
- Mô hình tổng quát và mô hình hướng tới văn bản mạng xã hội/noisy text.

## 4.4. Thiết lập huấn luyện

Trình bày:

- Tokenization hoặc biểu diễn ký tự.
- Max length.
- Batch size.
- Learning rate.
- Số epoch.
- Early stopping.
- Optimizer và weight decay.
- Random seed.
- Tiêu chí chọn checkpoint.
- Phần cứng hoặc môi trường huấn luyện nếu cần.

Nếu các nhóm mô hình dùng cấu hình khác nhau, tách thành bảng riêng.

## 4.5. Các độ đo đánh giá

Các metric chính:

- Macro-F1.
- F1 Label 1.
- Recall Label 1.
- Precision Label 1.
- PR-AUC/AUPRC.
- FP và FN.

Macro-F1 là thước đo tổng quát. F1 và Recall Label 1 phản ánh khả năng phát hiện smishing. Precision và FP phản ánh nguy cơ cảnh báo sai.

Không dùng Accuracy làm căn cứ kết luận chính do dữ liệu đánh giá mất cân bằng.

## 4.6. Phương pháp phân tích kết quả

### 4.6.1. Phân tích theo độ dài

Định nghĩa trước các khoảng, ví dụ:

- Ngắn: ≤ 80 ký tự.
- Trung bình: 81–160 ký tự.
- Dài: 161–240 ký tự.
- Rất dài: > 240 ký tự.

Có thể thay bằng quantile nếu phân phối dev quá lệch, nhưng phải giữ cùng một cách chia cho mọi mô hình.

### 4.6.2. Phân tích theo mức độ che giấu

Do Label 0 sử dụng `NONE`, phân tích độ khó theo `obfuscation_level` chủ yếu thực hiện trên Label 1:

- Level 0.
- Level 1–2.
- Level 3 trở lên.

Nếu số mẫu từng level đủ lớn, báo cáo riêng từng level.

### 4.6.3. Phân tích theo metadata

Các lát cắt ưu tiên:

- `data_origin`.
- `category`.
- `has_URL`.
- `has_phone_number`.
- `sender_type`.

### 4.6.4. Phân tích lỗi

Phân tích:

- False positive.
- False negative.
- Lỗi lặp lại giữa nhiều mô hình.
- Lỗi chỉ một nhóm mô hình mắc phải.
- Lỗi có confidence cao.

### 4.6.5. So sánh giữa các mô hình

Đặc biệt kiểm tra:

- PLM và character-level.
- Base và large.
- Hard-label và distilled.
- Mô hình tốt nhất theo metric tổng và mô hình tốt nhất theo Recall Label 1.

---

# 5. SƯỜN CHƯƠNG 5 — KẾT QUẢ VÀ PHÂN TÍCH

## 5.1. RQ1: Mô hình nào đạt hiệu quả tốt nhất?

### 5.1.1. Kết quả benchmark tổng thể trên dev và test

Đưa bảng benchmark chính lên đầu chương. Báo cáo kết quả của 17 cấu hình trên cả dev và test; việc lựa chọn, xếp hạng và phân tích mô hình dựa trên dev, còn test chỉ dùng để đánh giá khả năng tổng quát hóa cuối cùng.

Bảng tối thiểu gồm:

| Nhóm | Mô hình | Split | Macro-F1 | F1 L1 | Recall L1 | PR-AUC |
|---|---|---|---:|---:|---:|---:|

Mọi kết luận lựa chọn mô hình phải dựa trên dev.

### 5.1.2. So sánh theo nhóm kiến trúc

Trả lời:

- PLM có vượt character-level không?
- Mô hình lớn có luôn tốt hơn bản base không?
- Mô hình noisy/social text có lợi thế không?
- Mô hình nhẹ đánh đổi bao nhiêu hiệu năng?

### 5.1.3. Vai trò của distillation trong benchmark

So sánh trực tiếp:

- BiLSTM hard-label và BiLSTM distilled.
- TextCNN hard-label và TextCNN distilled.

Không khái quát rằng distillation luôn hiệu quả nếu kết quả không nhất quán.

### 5.1.4. Kết quả cuối cùng trên test

Chỉ báo cáo sau khi đã chọn mô hình bằng dev.

Nên phân biệt:

- Mô hình được chọn theo tiêu chí chính.
- Các baseline quan trọng.
- Kết quả test cuối cùng.

## 5.2. RQ2: Đặc điểm nào làm thay đổi hiệu năng?

### 5.2.1. Theo độ dài tin nhắn

Báo cáo mỗi lát cắt:

- Số mẫu.
- Phân phối nhãn.
- Macro-F1.
- F1/Recall Label 1.
- FP và FN.

Phải trả lời:

- Tin nhắn quá ngắn có thiếu ngữ cảnh không?
- Tin nhắn dài có bị cắt bởi max length không?
- Character-level và PLM phản ứng khác nhau như thế nào?

### 5.2.2. Theo `obfuscation_level`

Phải trả lời:

- Recall có giảm khi mức che giấu tăng không?
- Character-level có bền vững hơn PLM không?
- Những kiểu obfuscation nào vẫn gây lỗi?

Luôn kèm số lượng mẫu để tránh kết luận mạnh từ nhóm quá nhỏ.

### 5.2.3. Theo nguồn dữ liệu

So sánh:

- `real`.
- `external_real`.
- `external_curated`.

Mục tiêu là phát hiện domain shift và sự khác biệt giữa miền SMS thật với dữ liệu chéo miền.

### 5.2.4. Theo category và metadata

Ưu tiên:

- Nhóm OTP/ngân hàng.
- Tuyển dụng.
- Viễn thông.
- Dịch vụ công.
- URL.
- Số điện thoại.
- Sender type.

Chỉ trình bày các lát cắt có đủ số mẫu và có ý nghĩa giải thích.

## 5.3. RQ3: Mô hình sai ở đâu và vì sao?

### 5.3.1. Tổng quan FP/FN

So sánh số FP/FN giữa các mô hình đại diện:

- Mô hình benchmark tốt nhất.
- Một PLM baseline.
- TextCNN hoặc BiLSTM.
- Một biến thể distilled nếu có ý nghĩa.

### 5.3.2. Taxonomy lỗi

Các nhóm lỗi dự kiến:

- Smishing có bề mặt giống OTP hoặc brandname hợp lệ.
- Smishing không chứa URL hoặc lời kêu gọi hành động rõ ràng.
- Smishing có obfuscation/leet.
- Tin hợp lệ chứa URL, hotline hoặc ngôn ngữ cảnh báo.
- Tin hợp lệ liên quan bảo mật/tài khoản.
- Văn bản ngoài miền SMS.
- Lỗi do thiếu ngữ cảnh hoặc nhãn mơ hồ.

### 5.3.3. Ví dụ lỗi tiêu biểu

Mỗi ví dụ cần có:

- Nội dung rút gọn.
- Nhãn thật.
- Dự đoán.
- Confidence nếu có.
- Nhóm lỗi.
- Giải thích.

Chỉ chọn 5–8 ví dụ tiêu biểu. Không dùng ví dụ thay thế cho thống kê.

### 5.3.4. So sánh tập lỗi giữa mô hình

Phân tích:

- Mẫu mọi mô hình đều sai.
- Mẫu PLM đúng nhưng character-level sai.
- Mẫu character-level đúng nhưng PLM sai.
- Tác động của obfuscation đối với từng nhóm.

## 5.5. Tổng hợp câu trả lời nghiên cứu

Kết thúc chương bằng bảng:

| Câu hỏi | Kết luận chính | Bằng chứng |
|---|---|---|
| RQ1 | Nhóm/mô hình nào hiệu quả nhất | Benchmark dev và test |
| RQ2 | Những đặc điểm dữ liệu ảnh hưởng mạnh | Slice analysis |
| RQ3 | Các vùng lỗi và nguyên nhân chính | FP/FN và ví dụ định tính |

---

## 6. Bổ sung cho phần phân tích dữ liệu ở Chương 3

Phần EDA hiện có cần được đào sâu để hỗ trợ trực tiếp cho Chương 5.

### 6.1. Phân tích độ dài

Không chỉ báo cáo trung bình và trung vị. Cần thêm:

- Histogram hoặc density plot.
- Boxplot theo `label`.
- Độ dài theo `label × data_origin`.
- Tỷ lệ mẫu theo các khoảng độ dài.
- Outlier và khả năng bị truncate bởi max length.

### 6.2. Phân tích `obfuscation_level`

Cần thêm:

- Phân phối level trong Label 1.
- Level theo `data_origin`.
- Level theo `category`.
- Quan hệ giữa obfuscation và độ dài.
- Số mẫu thực và synthetic ở từng level.

Phải lưu ý rằng `NONE` của Label 0 và Level 0 của Label 1 có ý nghĩa khác nhau.

### 6.3. Phân tích metadata kết hợp

Các bảng/biểu đồ nên cân nhắc:

- `has_URL × label × data_origin`.
- `has_phone_number × label`.
- `sender_type × label`.
- `category × label × data_origin`.
- Độ dài theo category.

### 6.4. Tránh kết luận vượt quá bằng chứng

- WordCloud chỉ có tính minh họa, không chứng minh dữ liệu tạo sinh đã bảo toàn ngữ nghĩa.
- Bộ dữ liệu tổng thể cân bằng không có nghĩa mọi tập con đều cân bằng.
- Real data vẫn mất cân bằng, vì vậy class weighting vẫn là baseline hợp lý.
- Category và obfuscation không được dùng trực tiếp làm đặc trưng đầu vào nếu gây data leakage.

---

## 7. Ánh xạ nội dung cũ sang cấu trúc mới

| Nội dung hiện tại | Vị trí mới | Cách xử lý |
|---|---|---|
| Tổng quan hai nhánh thực nghiệm | 4.1 | Viết lại hoàn toàn theo RQ1–RQ3 |
| Nhánh 1: Đánh giá dữ liệu tạo sinh | - | Loại bỏ hoàn toàn (không còn TSTR & Augmentation) |
| Nhánh 2: Knowledge Distillation | 4.3.2 và 5.1.3 | Bỏ tư cách nhánh độc lập |
| Kết quả distillation cũ | 5.1.3 | Chỉ giữ nếu cùng giao thức benchmark |
| Benchmark mới | 5.1 | Đưa thành kết quả chính đầu chương |

---

## 8. Artefact nguồn cần tham chiếu

### Benchmark

- `setup_results/distillation_benchmark/summary/benchmark_report.md`
- `setup_results/distillation_benchmark/summary/benchmark_metrics_dev_test_wide.csv`
- `setup_results/distillation_benchmark/summary/benchmark_metrics_long.csv`
- `setup_results/distillation_benchmark/split_report.md`

### Prediction phục vụ result analysis

- Các file `*_predictions_dev.csv` trong từng thư mục mô hình benchmark.
- Các file `*_errors_dev.csv` trong từng thư mục mô hình benchmark.

### Phân tích lỗi hiện có

- Đã loại bỏ các file phân tích cũ của Setup A/B/E/G. Phân tích lỗi mới sẽ được thực hiện trên benchmark chính.

---

## 9. Checklist trước khi hoàn tất mỗi mục

- [ ] Mục này đang trả lời RQ nào?
- [ ] Kết luận có dựa trên dev hay vô tình lựa chọn theo test?
- [ ] Bảng có ghi rõ split và số lượng mẫu không?
- [ ] Các kết quả được so sánh có cùng giao thức dữ liệu không?
- [ ] Có báo cáo số mẫu của từng lát cắt không?
- [ ] Có phân biệt ý nghĩa thống kê với chênh lệch vài mẫu không?
- [ ] Có phân tích cả Recall/FN và Precision/FP không?
- [ ] Có tránh kể tuần tự theo Setup A–G không?
- [ ] Distillation có đang được trình bày đúng như một cấu hình benchmark không?
- [ ] Kết luận có chỉ ra giới hạn của bằng chứng không?
- [ ] Các hình/bảng có thực sự hỗ trợ câu hỏi đang trả lời không?

---

## 10. Thứ tự triển khai

1. Thống nhất giao thức benchmark, dev và test.
2. Viết lại Chương 4 theo sườn ở tài liệu này.
3. Đưa benchmark chính vào Chương 5.
4. Triển khai result analysis trên dev theo độ dài và `obfuscation_level`.
5. Mở rộng sang `data_origin`, category, URL, số điện thoại và sender type.
6. Thực hiện phân tích lỗi giữa các mô hình đại diện.
7. Viết bảng tổng hợp RQ1–RQ3.
8. Chỉnh lại phần EDA ở Chương 3 để tạo tiền đề cho phân tích kết quả.
