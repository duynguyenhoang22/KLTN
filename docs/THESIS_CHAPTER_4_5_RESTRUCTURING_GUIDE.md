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

### 2.6. Hạn chế phân cấp tiểu mục

Từ Mục 4.2 đến hết Chương 5, ưu tiên chỉ sử dụng các mục cấp 2 tương ứng với một chủ đề hoặc câu hỏi nghiên cứu lớn. Không tách nội dung thành các mục cấp 3–4 chỉ vì nội dung có nhiều thành phần.

Thay cho việc chia nhỏ tiêu đề, sử dụng:

- Câu chuyển đoạn để nối các bước lập luận.
- Đoạn mở đầu nêu vai trò của phần sắp trình bày.
- Bảng để gom các ánh xạ hoặc thông số lặp lại.
- Cụm dẫn nhập ngắn trong câu văn khi cần đổi góc nhìn.

Chỉ tạo mục cấp 3 khi đồng thời thỏa mãn hai điều kiện:

1. Nội dung đủ dài và độc lập để người đọc cần tra cứu riêng.
2. Việc bỏ tiêu đề làm mạch lập luận trở nên khó theo dõi hơn rõ rệt.

Không sử dụng mục cấp 4 trong Chương 4 và Chương 5, trừ trường hợp bắt buộc theo mẫu trình bày của khoa.

---

## 3. Các câu hỏi nghiên cứu

Các chương thực nghiệm cần xoay quanh bốn câu hỏi:

### RQ1 — So sánh mô hình

Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu ViSmish?

### RQ2 — Ảnh hưởng của đặc điểm dữ liệu

Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế nào đến khả năng phát hiện smishing?

### RQ3 — Phân tích lỗi

Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân có thể là gì?

### RQ4 — Giá trị của dữ liệu tạo sinh

Dữ liệu tạo sinh mang lại giá trị gì, có thể thay thế dữ liệu thật hay chỉ phù hợp để tăng cường dữ liệu?

---

# 4. SƯỜN CHƯƠNG 4 — PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM

## 4.1. Tổng quan thiết kế thực nghiệm

Nội dung cần có:

- Mục tiêu tổng quát của thực nghiệm.
- Bốn câu hỏi nghiên cứu RQ1–RQ4.
- Sơ đồ quy trình từ dữ liệu, huấn luyện benchmark, đánh giá đến phân tích kết quả.
- Giải thích benchmark là trục thực nghiệm chính.
- Giới thiệu ngắn các thí nghiệm bổ sung về synthetic data.

Không sử dụng cụm từ “hai nhánh thực nghiệm”.

## 4.2. Dữ liệu và chiến lược phân chia

Mục này được kể thành một tuyến liên tục, không chia thành 4.2.1–4.2.4. Thứ tự lập luận:

1. Giới thiệu thành phần dữ liệu và vai trò từng nguồn.
2. Chuyển sang chính sách phân chia.
3. Trình bày kiểm tra rò rỉ.
4. Kết lại bằng vai trò khác nhau của train, dev và test.

Các nguồn cần trình bày:

- `real`
- `external_real`
- `external_curated`
- `synthetic`
- `paraphrased`
- `synthetic_hard_positive`

Làm rõ nguồn nào xuất hiện trong train, dev và test. Sau đó chuyển tự nhiên sang:

- Tỷ lệ train/dev/test.
- Seed chia dữ liệu.
- Stratification theo `label × data_origin × category`.
- Synthetic chỉ được đưa vào train.
- Dev và test không chứa dữ liệu tạo sinh.
- Quy tắc xử lý các strata quá nhỏ.

Phần kiểm tra rò rỉ nối tiếp ngay sau chiến lược chia, tối thiểu gồm:

- Trùng `sample_id`.
- Trùng nội dung chính xác.
- Trùng nội dung sau chuẩn hóa.
- Nếu có điều kiện, kiểm tra near-duplicate.

Kết thúc mục bằng vai trò của từng split:

- Dev: chọn checkpoint, lựa chọn mô hình, điều chỉnh threshold và result analysis.
- Test: đánh giá cuối cùng.

## 4.3. Các mô hình benchmark

Không chia thành 4.3.1–4.3.3. Mở đầu bằng lý do benchmark cần nhiều họ kiến trúc, sau đó lần lượt giới thiệu trong cùng một mạch:

- BiLSTM và TextCNN.
- Hai biến thể distilled từ PhoBERT-base.
- Các pretrained language model.
- Các mô hình ngôn ngữ lớn được fine-tune.

Giải thích lý do chọn mô hình ký tự: phù hợp với SMS ngắn, viết tắt, lỗi chính tả, leet và obfuscation. Distillation chỉ là một biến thể huấn luyện trong benchmark, không phải nhánh thực nghiệm riêng.

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

Không chia thành các mục 4.6.1–4.6.5. Trình bày theo một chuỗi từ phân tích định lượng theo lát cắt đến phân tích lỗi và so sánh mô hình.

Bắt đầu với độ dài và định nghĩa trước các khoảng, ví dụ:

- Ngắn: ≤ 80 ký tự.
- Trung bình: 81–160 ký tự.
- Dài: 161–240 ký tự.
- Rất dài: > 240 ký tự.

Có thể thay bằng quantile nếu phân phối dev quá lệch, nhưng phải giữ cùng một cách chia cho mọi mô hình.

Tiếp theo là mức độ phi chuẩn của văn bản. Phần này tạm để placeholder cho tới khi triển khai một thuộc tính như `text_noise_level`, được định nghĩa theo hiện tượng bề mặt và áp dụng độc lập cho cả hai nhãn. Không sử dụng `obfuscation_level` hiện tại như thước đo chung vì thuộc tính này gắn với ý định che giấu trong Label 1.

Nếu vẫn phân tích `obfuscation_level`, chỉ xem đây là phân tích phụ trong nội bộ Label 1 và phải nêu rõ giới hạn. Sau đó mở rộng sang các metadata:

- `data_origin`.
- `category`.
- `has_URL`.
- `has_phone_number`.
- `sender_type`.

Phần sau của mục chuyển sang phân tích lỗi:

- False positive.
- False negative.
- Lỗi lặp lại giữa nhiều mô hình.
- Lỗi chỉ một nhóm mô hình mắc phải.
- Lỗi có confidence cao.

Kết thúc bằng các đối chiếu giữa mô hình:

- PLM và character-level.
- Base và large.
- Hard-label và distilled.
- Mô hình tốt nhất theo metric tổng và mô hình tốt nhất theo Recall Label 1.

## 4.7. Thí nghiệm bổ sung về dữ liệu tạo sinh

Không chia thành 4.7.1–4.7.4. Kể theo chuỗi giả thuyết tăng dần:

1. Thiết lập mốc real-only.
2. Dùng TSTR để kiểm tra synthetic có thể thay thế real hay không.
3. Dùng positive augmentation để kiểm tra synthetic Label 1 như nguồn bổ sung.
4. Dùng negative augmentation và external challenge để kiểm tra ranh giới Label 0.

Trong đoạn cuối, kiểm tra vai trò của synthetic/external Label 0 trong:

- Mở rộng miền âm tính.
- Giảm false positive.
- Tăng độ bền vững khi gặp dữ liệu ngoài miền.

Các tên Setup A–G chỉ dùng như mã tham chiếu trong bảng hoặc phụ lục.

Để tránh quá tải, không trình bày mọi biến thể A–G với trọng lượng ngang nhau. Phần nội dung chính chỉ giữ các phép so sánh đại diện trực tiếp trả lời RQ4:

1. A/B1 so với C/D: real-only và synthetic-only.
2. E1–E4: ảnh hưởng của lượng synthetic Label 1.
3. F1 so với F2b: synthetic Label 0 và external curated Label 0.
4. G0 so với G2: domain shift trước và sau khi bổ sung external curated Label 0.

Các biến thể B2, F2a, F2c, F3, G1 và G3 đóng vai trò kiểm tra bổ sung hoặc độ bền. Chỉ tóm tắt khi chúng làm thay đổi kết luận chính; bảng chi tiết, kết quả từng seed và phần lớn confusion matrix được chuyển xuống phụ lục.

---

# 5. SƯỜN CHƯƠNG 5 — KẾT QUẢ VÀ PHÂN TÍCH

## 5.1. RQ1: Mô hình nào đạt hiệu quả tốt nhất?

Không chia thành 5.1.1–5.1.4. Mục bắt đầu bằng bảng benchmark của 17 cấu hình trên dev và test; việc lựa chọn, xếp hạng và phân tích mô hình dựa trên dev, còn test chỉ dùng để đánh giá khả năng tổng quát hóa cuối cùng.

Bảng tối thiểu gồm:

| Nhóm | Mô hình | Split | Macro-F1 | F1 L1 | Recall L1 | PR-AUC |
|---|---|---|---:|---:|---:|---:|

Mọi kết luận lựa chọn mô hình phải dựa trên dev. Từ bảng tổng thể, mạch phân tích lần lượt trả lời:

- PLM có vượt character-level không?
- Mô hình lớn có luôn tốt hơn bản base không?
- Mô hình noisy/social text có lợi thế không?
- Mô hình nhẹ đánh đổi bao nhiêu hiệu năng?

Sau đó so sánh trực tiếp distillation:

- BiLSTM hard-label và BiLSTM distilled.
- TextCNN hard-label và TextCNN distilled.

Không khái quát rằng distillation luôn hiệu quả nếu kết quả không nhất quán. Kết thúc mục bằng kết quả test sau khi đã chọn mô hình bằng dev.

Nên phân biệt:

- Mô hình được chọn theo tiêu chí chính.
- Các baseline quan trọng.
- Kết quả test cuối cùng.

## 5.2. RQ2: Đặc điểm nào làm thay đổi hiệu năng?

Không chia thành 5.2.1–5.2.4. Kể theo trật tự từ thuộc tính bề mặt dễ diễn giải đến miền dữ liệu: độ dài → mức độ phi chuẩn (sau khi triển khai) → nguồn dữ liệu → category và metadata.

Với mỗi lát cắt độ dài, báo cáo:

- Số mẫu.
- Phân phối nhãn.
- Macro-F1.
- F1/Recall Label 1.
- FP và FN.

Phải trả lời:

- Tin nhắn quá ngắn có thiếu ngữ cảnh không?
- Tin nhắn dài có bị cắt bởi max length không?
- Character-level và PLM phản ứng khác nhau như thế nào?

Sau khi có `text_noise_level`, trả lời:

- Hiệu năng có giảm khi mức độ phi chuẩn tăng không?
- Character-level có bền vững hơn PLM không?
- Những dạng teencode, viết tắt, leet hoặc ký tự đặc biệt nào vẫn gây lỗi?

`obfuscation_level` hiện tại chỉ được dùng như phân tích phụ trên Label 1. Luôn kèm số lượng mẫu để tránh kết luận mạnh từ nhóm quá nhỏ. Tiếp theo so sánh theo nguồn:

- `real`.
- `external_real`.
- `external_curated`.

Mục tiêu là phát hiện domain shift và sự khác biệt giữa miền SMS thật với dữ liệu chéo miền. Kết thúc bằng category và metadata:

- Nhóm OTP/ngân hàng.
- Tuyển dụng.
- Viễn thông.
- Dịch vụ công.
- URL.
- Số điện thoại.
- Sender type.

Chỉ trình bày các lát cắt có đủ số mẫu và có ý nghĩa giải thích.

## 5.3. RQ3: Mô hình sai ở đâu và vì sao?

Không chia thành 5.3.1–5.3.4. Bắt đầu bằng tổng quan FP/FN giữa các mô hình đại diện:

- Mô hình benchmark tốt nhất.
- Một PLM baseline.
- TextCNN hoặc BiLSTM.
- Một biến thể distilled nếu có ý nghĩa.

Từ thống kê tổng quan, xây dựng taxonomy lỗi:

- Smishing có bề mặt giống OTP hoặc brandname hợp lệ.
- Smishing không chứa URL hoặc lời kêu gọi hành động rõ ràng.
- Smishing có obfuscation/leet.
- Tin hợp lệ chứa URL, hotline hoặc ngôn ngữ cảnh báo.
- Tin hợp lệ liên quan bảo mật/tài khoản.
- Văn bản ngoài miền SMS.
- Lỗi do thiếu ngữ cảnh hoặc nhãn mơ hồ.

Sau taxonomy, chọn ví dụ tiêu biểu. Mỗi ví dụ cần có:

- Nội dung rút gọn.
- Nhãn thật.
- Dự đoán.
- Confidence nếu có.
- Nhóm lỗi.
- Giải thích.

Chỉ chọn 5–8 ví dụ tiêu biểu. Không dùng ví dụ thay thế cho thống kê. Kết thúc bằng so sánh tập lỗi giữa mô hình:

- Mẫu mọi mô hình đều sai.
- Mẫu PLM đúng nhưng character-level sai.
- Mẫu character-level đúng nhưng PLM sai.
- Tác động của obfuscation đối với từng nhóm.

## 5.4. RQ4: Dữ liệu tạo sinh có giá trị như thế nào?

Không chia thành 5.4.1–5.4.4. Mạch lập luận đi từ khả năng thay thế đến cách sử dụng phù hợp.

Trước hết, dùng Real-only và TSTR để trả lời synthetic có thể thay thế real data hay không. Sau đó so sánh Real-only với các mức bổ sung synthetic Label 1 để đánh giá positive augmentation.

Phân tích trade-off giữa:

- Recall.
- Precision.
- FP.
- FN.

Tiếp theo, dùng external challenge để giải thích vì sao cần mở rộng Label 0:

- Positive augmentation có thể làm mô hình quá nhạy.
- External curated Label 0 giúp mở rộng ranh giới âm tính.
- Không phải cứ thêm nhiều dữ liệu Label 0 là tốt; chất lượng và mức phù hợp miền quan trọng hơn số lượng.

Kết thúc mục bằng luận điểm tổng hợp:

> Dữ liệu tạo sinh chưa phù hợp để thay thế hoàn toàn dữ liệu thật, nhưng có giá trị khi được sử dụng như nguồn augmentation có kiểm soát. Real data giữ vai trò neo miền, synthetic Label 1 mở rộng miền smishing, còn Label 0 chất lượng giúp kiểm soát false positive và domain shift.

Mục 5.4 chỉ triển khai sâu bốn phép kiểm chứng đại diện đã chốt ở Mục 4.7. Không kể tuần tự mọi biến thể A–G. Các biến thể phụ chỉ được nhắc ngắn nếu củng cố, làm yếu hoặc tạo ngoại lệ cho kết luận chính.

## 5.5. Tổng hợp câu trả lời nghiên cứu

Kết thúc chương bằng bảng:

| Câu hỏi | Kết luận chính | Bằng chứng |
|---|---|---|
| RQ1 | Nhóm/mô hình nào hiệu quả nhất | Benchmark dev và test |
| RQ2 | Những đặc điểm dữ liệu ảnh hưởng mạnh | Slice analysis |
| RQ3 | Các vùng lỗi và nguyên nhân chính | FP/FN và ví dụ định tính |
| RQ4 | Vai trò phù hợp của synthetic data | TSTR và augmentation |

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
| Tổng quan hai nhánh thực nghiệm | 4.1 | Viết lại hoàn toàn theo RQ1–RQ4 |
| Nhánh 1: Đánh giá dữ liệu tạo sinh | 4.7 và 5.4 | Rút gọn, tổ chức theo câu hỏi |
| Setup A/B | 4.7 và 5.4 | Giữ làm baseline |
| Setup C/D – TSTR | 4.7 và 5.4 | Hạ thành phân tích khả năng thay thế real |
| Setup E | 4.7 và 5.4 | Dùng phân tích positive augmentation |
| Setup F/G | 4.7 và 5.4 | Dùng phân tích negative coverage/domain shift |
| Nhánh 2: Knowledge Distillation | 4.3 và 5.1 | Bỏ tư cách nhánh độc lập |
| Kết quả distillation cũ | 5.1 | Chỉ giữ nếu cùng giao thức benchmark |
| Confusion matrix theo từng setup | 5.3 và 5.4 | Chọn hình tiêu biểu, không liệt kê toàn bộ |
| Tổng kết các setup | 5.4 và 5.5 | Viết lại thành kết luận theo RQ |
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

- `setup_results/manual_error_analysis/thesis_ready_fp_fn_analysis.md`
- `setup_results/manual_error_analysis/all_errors_labeled.csv`
- `setup_results/manual_error_analysis/stable_error_cases.csv`
- `setup_results/manual_error_analysis/manual_review_candidates.csv`

### TSTR và augmentation

- `setup_results/setup_e_results/`
- `setup_results/setup_f_results/`
- `setup_results/setup_g_results/`

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
- [ ] TSTR có đang được đặt đúng trong phần phân tích synthetic data không?
- [ ] Phần RQ4 có tập trung vào các phép so sánh đại diện thay vì trình bày mọi biến thể ngang hàng không?
- [ ] Bảng từng seed và các biến thể kiểm tra bổ sung đã được chuyển xuống phụ lục chưa?
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
7. Rút gọn TSTR và các setup augmentation thành câu trả lời cho RQ4.
8. Viết bảng tổng hợp RQ1–RQ4.
9. Chỉnh lại phần EDA ở Chương 3 để tạo tiền đề cho phân tích kết quả.
