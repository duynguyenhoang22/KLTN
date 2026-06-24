# PHỤ LỤC CHƯƠNG 4. GHI CHÚ CHI TIẾT CHO THIẾT LẬP THỰC NGHIỆM

Tài liệu này lưu các chi tiết có giá trị tái lập nhưng làm Chương 4 quá dài nếu đặt toàn bộ trong phần thân chính. Khi đưa vào báo cáo cuối, có thể tách thành các phụ lục 4.A, 4.B và 4.C.

## Phụ lục 4.A. Chi tiết dữ liệu, phân chia và kiểm tra rò rỉ

### Thành phần dữ liệu theo nguồn

| Nguồn dữ liệu | Label 0 | Label 1 | Tổng | Vai trò trong benchmark |
|---|---:|---:|---:|---|
| `real` | 2.321 | 246 | 2.567 | Dữ liệu miền đích; chia vào train/dev/test |
| `external_real` | 500 | 0 | 500 | Mở rộng miền Label 0; chia vào train/dev/test |
| `external_curated` | 501 | 0 | 501 | Hard negative Label 0; chia vào train/dev/test |
| `synthetic` | 1.998 | 10 | 2.008 | Dữ liệu tạo sinh; chỉ dùng cho train |
| `paraphrased` | 0 | 4.333 | 4.333 | Smishing được paraphrase; chỉ dùng cho train |
| `synthetic_hard_positive` | 0 | 653 | 653 | Smishing khó; chỉ dùng cho train |
| **Tổng** | **5.320** | **5.242** | **10.562** | - |

Nguồn `real` là nguồn duy nhất chứa đồng thời tin nhắn hợp lệ và smishing thực, nên giữ vai trò neo mô hình vào phân phối miền đích. Hai nguồn `external_real` và `external_curated` bổ sung các mẫu Label 0 ngoài miền SMS quen thuộc, giúp đánh giá false positive trên văn bản chéo miền. Ba nguồn `synthetic`, `paraphrased` và `synthetic_hard_positive` mở rộng dữ liệu huấn luyện nhưng không xuất hiện trong dev/test.

### Phân phối train/dev/test

| Split | Tổng số mẫu | Label 0 | Label 1 | `real` | `external_real` | `external_curated` | Dữ liệu tạo sinh |
|---|---:|---:|---:|---:|---:|---:|---:|
| Train | 9.492 | 4.324 | 5.168 | 1.797 | 350 | 351 | 6.994 |
| Dev | 535 | 498 | 37 | 385 | 75 | 75 | 0 |
| Test | 535 | 498 | 37 | 385 | 75 | 75 | 0 |

Quá trình phân tầng sử dụng nhãn, nguồn dữ liệu và các nhóm metadata sẵn có tại thời điểm chia. Với strata có dưới 5 mẫu, toàn bộ dữ liệu được giữ lại trong train để tránh tạo holdout quá nhỏ; với strata từ 5 đến dưới 10 mẫu, quy trình ưu tiên giữ phần lớn trong train và tối đa một mẫu trong dev. Vì vậy, một số nhóm metadata hiếm không đại diện đầy đủ trong dev/test và cần được diễn giải thận trọng ở Chương 5.

### Kiểm tra overlap

| Cặp split | Trùng `sample_id` | Trùng nội dung chính xác |
|---|---:|---:|
| Train - Dev | 0 | 0 |
| Train - Test | 0 | 0 |
| Dev - Test | 0 | 0 |

Các kiểm tra cần hoàn thiện trước bản cuối gồm: chuẩn hóa lowercase, khoảng trắng và dấu câu rồi kiểm tra duplicate; chuẩn hóa URL và số điện thoại thành placeholder; kiểm tra near-duplicate giữa dữ liệu tạo sinh/paraphrase trong train và mẫu `real` ở dev/test bằng n-gram hoặc embedding nếu điều kiện cho phép.

## Phụ lục 4.B. Hyperparameter và thiết lập huấn luyện đầy đủ

### Character-level models

| Thành phần | BiLSTM | TextCNN |
|---|---:|---:|
| Độ dài tối đa | 256 ký tự | 256 ký tự |
| Embedding dimension | 64 | 64 |
| Hidden dimension | 64 mỗi chiều | - |
| Số filter | - | 96/kernel |
| Kernel size | - | 3, 4, 5 |
| Dropout | 0,3 | 0,3 |
| Batch size | 128 | 128 |
| Epoch tối đa | 12 | 12 |
| Learning rate | \(2 \times 10^{-3}\) | \(2 \times 10^{-3}\) |
| Weight decay | \(10^{-4}\) | \(10^{-4}\) |
| Early stopping | Patience = 3 | Patience = 3 |
| Tiêu chí chọn checkpoint | Dev Macro-F1 | Dev Macro-F1 |

Benchmark distilled dùng teacher PhoBERT-base, temperature = 2 và \(\alpha = 0{,}8\). Study RQ4 dùng TextCNN với ba teacher PhoBERT-base, CafeBERT và ViCLSR, chạy ba seed 42/123/2025.

### Encoder PLM fine-tuning

| Thành phần | Cấu hình chung | XLM-RoBERTa-large và ViCLSR |
|---|---:|---:|
| Max length | 128 token | 128 token |
| Epoch tối đa | 3 | 3 |
| Train batch size | 16 | 8 |
| Evaluation batch size | 32 | 16 |
| Gradient accumulation | 1 | 2 |
| Effective train batch size | 16 | 16 |
| Learning rate | \(2 \times 10^{-5}\) | \(2 \times 10^{-5}\) |
| Weight decay | 0,01 | 0,01 |
| Warmup ratio | 0,1 | 0,1 |
| Mixed precision | FP16 | FP16 |
| Early stopping | Patience = 2 | Patience = 2 |
| Tiêu chí chọn checkpoint | Dev Macro-F1 | Dev Macro-F1 |

PhoBERT-base và PhoBERT-large dùng bước phân đoạn từ tiếng Việt trước tokenization. Các encoder còn lại dùng tokenizer đi kèm checkpoint.

### LLM LoRA fine-tuning

| Thành phần | Giá trị chung |
|---|---|
| Mô hình áp dụng | Gemma 3 1B, Gemma 2B, Qwen3 0.6B, Qwen2.5 0.5B |
| LoRA rank \(r\) | 8 |
| LoRA alpha | 16 |
| LoRA dropout | 0,1 |
| Target modules | `q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
| Max length | 512 |
| Batch size | 4 |
| Gradient accumulation | 4 |
| Effective batch size | 16 |
| Learning rate | \(2 \times 10^{-4}\) |
| Epoch | 3 |
| Precision | BF16 |

### Deployment feasibility protocol

| Thành phần | Thiết lập |
|---|---|
| Các mô hình | PhoBERT-base đại diện; TextCNN hard, vanilla KD và risk-aware KD |
| Dữ liệu | Benchmark test split 535 mẫu |
| Thiết bị | Cùng CPU, 1 thread |
| Latency | Batch size 1, 3 warm-up, 20 lần lặp; chỉ báo cáo cho TextCNN đã đo runtime |
| Throughput | Một lượt suy luận, batch size 128 |
| Tài nguyên | Số tham số, kích thước checkpoint, peak RAM |
| Chất lượng đi kèm | F1 Label 1 trên cùng split |

## Phụ lục 4.C. Quy tắc phân tích lát cắt và lỗi

### Phân phối dev theo độ dài

| Độ dài | Label 0 | Label 1 | Tổng | Cách sử dụng |
|---|---:|---:|---:|---|
| <= 80 ký tự | 138 | 2 | 140 | Chỉ mô tả hoặc gộp khi tính metric Label 1 |
| 81-160 ký tự | 129 | 17 | 146 | Phân tích đầy đủ |
| 161-240 ký tự | 74 | 8 | 82 | Phân tích với lưu ý cỡ mẫu |
| > 240 ký tự | 157 | 10 | 167 | Phân tích với lưu ý cỡ mẫu |

### Quy tắc đánh giá theo lát cắt

| Lát cắt | Phạm vi | Chỉ số ưu tiên | Lưu ý |
|---|---|---|---|
| Độ dài | Toàn bộ dev | Macro-F1, F1/Recall L1, FP, FN | Gộp nhóm nếu Label 1 < 5 |
| Đặc trưng bề mặt | Toàn bộ dev | Recall L1, FP, FN | Bao gồm URL, số điện thoại, loại người gửi và tín hiệu văn bản phi chuẩn nếu có |
| Data origin | `real`, `external_*` | Metric đầy đủ trên real; FP/FPR trên external | External chỉ chứa Label 0 |
| URL, số điện thoại | Theo nhãn | Recall L1 và FP | Kiểm tra phụ thuộc tín hiệu bề mặt |
| Sender type | Theo nhãn và loại người gửi | Recall L1, FP, FN | Một số nhóm có thể không có Label 1 |
| Lĩnh vực tin nhắn | Các nhóm đủ mẫu | F1/Recall L1 hoặc số lỗi | Không kết luận từ nhóm quá nhỏ |
| Hành động yêu cầu | Các nhóm đủ mẫu | F1/Recall L1, FP, FN | So sánh các yêu cầu truy cập link, gọi điện, cung cấp thông tin |
| Vai trò đối tượng | Các nhóm đủ mẫu | F1/Recall L1, FP, FN | Kiểm tra các nhóm như khách hàng, con nợ hoặc người nhận thông báo |
| Thủ đoạn thuyết phục | Các nhóm đủ mẫu | F1/Recall L1, FP, FN | Phân tích các tactic như dụ dỗ qua link, khẩn cấp, đe dọa, mạo danh |

Các tên cột cụ thể cần được đồng bộ với bộ metadata v2.1 dùng trong Chương 5. Khi một lát cắt có quá ít mẫu Label 1, kết quả chỉ nên được mô tả định tính hoặc gộp nhóm thay vì dùng để khẳng định ưu thế mô hình.
