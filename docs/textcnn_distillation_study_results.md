# Kết quả phân tích chuyên sâu distillation với TextCNN

Phân tích này giữ BiLSTM hard-label và BiLSTM distilled trong benchmark tổng
thể, nhưng chỉ sử dụng TextCNN để cô lập tác động của distillation. Ba cấu hình
TextCNN có cùng kiến trúc, dữ liệu, preprocessing và hyperparameter; khác biệt
duy nhất là tín hiệu giám sát.

## Kết quả trung bình qua ba seed

| Split | Cấu hình | Macro-F1 | F1 Label 1 | Recall Label 1 | PR-AUC |
|---|---|---:|---:|---:|---:|
| Dev | Hard-label | 0,9213 ± 0,0111 | 0,8532 ± 0,0207 | 0,8378 ± 0,0270 | 0,8772 ± 0,0356 |
| Dev | Vanilla KD | 0,9147 ± 0,0112 | 0,8411 ± 0,0213 | 0,8378 ± 0,0541 | 0,8710 ± 0,0324 |
| Dev | Risk-aware KD | 0,9202 ± 0,0146 | 0,8514 ± 0,0275 | 0,8559 ± 0,0563 | 0,8896 ± 0,0135 |
| Test | Hard-label | 0,8898 ± 0,0202 | 0,7949 ± 0,0374 | 0,8018 ± 0,0413 | 0,8706 ± 0,0145 |
| Test | Vanilla KD | 0,8774 ± 0,0032 | 0,7726 ± 0,0058 | 0,8108 ± 0,0000 | 0,8789 ± 0,0195 |
| Test | Risk-aware KD | 0,9069 ± 0,0176 | 0,8276 ± 0,0332 | 0,8919 ± 0,0715 | 0,8791 ± 0,0287 |

Trên dev, risk-aware KD tăng Recall Label 1 trung bình 0,0180 và PR-AUC
0,0124 so với hard-label, trong khi Macro-F1 và F1 Label 1 gần như được giữ
nguyên. Tuy nhiên, các khoảng tin cậy bootstrap của chênh lệch trên dev đều chứa
0; do đó chưa đủ bằng chứng để khẳng định cải thiện ổn định trên dev.

Trên test, risk-aware KD tăng trung bình:

- Macro-F1: +0,0172; bootstrap CI 95% `[-0,0062; 0,0410]`;
- F1 Label 1: +0,0328; bootstrap CI 95% `[-0,0106; 0,0776]`;
- Recall Label 1: +0,0900; bootstrap CI 95% `[0,0357; 0,1476]`;
- PR-AUC: +0,0083; bootstrap CI 95% `[-0,0126; 0,0290]`.

Recall tăng ở hai trong ba seed và chênh lệch bootstrap trên test không chứa 0.
Macro-F1 và F1 Label 1 của risk-aware KD cao hơn hard-label ở cả ba seed,
nhưng CI vẫn chứa 0 do tập test chỉ có 37 mẫu Label 1.

Vanilla KD không tạo ra xu hướng cải thiện nhất quán. Trên dev, cấu hình này
thấp hơn hard-label ở cả bốn metric trung bình. Trên test, Recall tăng nhẹ nhưng
Macro-F1 và F1 Label 1 giảm. Kết quả cho thấy việc truyền đồng đều mọi soft
target, bao gồm các dự đoán teacher không đáng tin cậy, không mang lại lợi ích
rõ ràng cho TextCNN.

## Diễn giải đóng góp

Kết quả hỗ trợ một kết luận có phạm vi:

> Trong benchmark hiện tại, risk-aware distillation làm TextCNN nhạy hơn với
> lớp smishing và cải thiện Recall trên test, trong khi vanilla distillation
> không tạo lợi ích tương tự. Cơ chế giảm ảnh hưởng của soft target không đáng
> tin cậy có vai trò quan trọng hơn việc chỉ bổ sung soft label một cách đồng
> đều.

Không nên kết luận distillation làm mô hình nhỏ hơn hoặc nhanh hơn. Cả ba biến
thể TextCNN đều có 87.553 tham số và checkpoint khoảng 0,342 MB. Mức giảm hơn
1.500 lần kích thước so với PhoBERT-base đến từ lựa chọn kiến trúc TextCNN,
không phải từ distillation. Đóng góp của distillation nằm ở thay đổi chất lượng
dự đoán của cùng student.

Phép đo CPU cho thấy cả ba TextCNN đều nằm trong cùng vùng chi phí triển khai
khoảng 1–3 ms mỗi tin nhắn và hàng trăm tin nhắn mỗi giây. Chênh lệch nhỏ giữa
ba checkpoint không được diễn giải là lợi thế tốc độ của một loss, vì kiến trúc
và số phép tính suy luận giống nhau và phép đo runtime có nhiễu hệ thống.

## Giới hạn

1. Mỗi dev/test split chỉ có 37 mẫu Label 1; một dự đoán tương ứng khoảng 2,7
   điểm phần trăm Recall.
2. Bằng chứng cải thiện mạnh nhất xuất hiện ở Recall trên test, trong khi CI của
   các metric dev vẫn chứa 0.
3. Teacher PhoBERT-base không phải mô hình mạnh nhất trong benchmark.
4. Kết quả mới chỉ kiểm tra ba seed và một bộ hyperparameter distillation.

Vì vậy, distillation có thể được trình bày như một đóng góp về **risk-aware
knowledge transfer cho TextCNN tài nguyên thấp**, nhưng không nên tuyên bố là
phương pháp cải thiện toàn diện hoặc luôn hiệu quả.

Artefact đầy đủ:

- `setup_results/textcnn_distillation_study/phobert-base/summary/textcnn_kd_report.md`;
- `setup_results/textcnn_distillation_study/phobert-base/summary/textcnn_kd_mean_sd.csv`;
- `setup_results/textcnn_distillation_study/phobert-base/summary/textcnn_kd_paired_bootstrap.csv`;
- `setup_results/textcnn_distillation_study/phobert-base/deployment/deployment_feasibility_test.csv`.
