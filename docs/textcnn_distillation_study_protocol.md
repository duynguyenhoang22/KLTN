# Giao thức phân tích chuyên sâu distillation với TextCNN

BiLSTM hard-label và BiLSTM distilled vẫn được giữ trong benchmark mô hình tổng
thể. Phân tích chuyên sâu về tác động của knowledge distillation chỉ sử dụng
TextCNN để tránh trộn lẫn kết quả giữa nhiều kiến trúc student.

## Câu hỏi đánh giá

1. Soft target có cải thiện TextCNN so với cùng kiến trúc chỉ học hard label hay
   không?
2. Cơ chế risk-aware weighting có tốt hơn vanilla knowledge distillation hay
   không?
3. Kết quả có ổn định qua nhiều seed hay chỉ xuất hiện ở một lần chạy?

## Các cấu hình

| Cấu hình | Hard-label loss | Soft-target loss | Trọng số teacher |
|---|---:|---:|---|
| `hard` | Có | Không | Không áp dụng |
| `vanilla_kd` | Có | Có | Đồng đều bằng 1 |
| `risk_aware_kd` | Có | Có | Theo confidence; teacher false negative có trọng số 0 |

Các cấu hình sử dụng cùng benchmark split, tokenizer ký tự, vocabulary,
kiến trúc TextCNN, hyperparameter và quy tắc early stopping. Thiết lập mặc định:

- seed: 42, 123 và 2025;
- temperature của teacher output: 2;
- hệ số hard-label loss \(\alpha=0,8\);
- teacher false-negative weight: 0;
- lựa chọn checkpoint theo Macro-F1 trên dev;
- test chỉ dùng để xác nhận xu hướng sau khi giao thức đã khóa.

## Chạy thí nghiệm

```powershell
python scripts/distillation/run_textcnn_distillation_study.py
```

Chạy lại phần tổng hợp:

```powershell
python scripts/distillation/analyze_textcnn_distillation_study.py
```

Kết quả được lưu tại:

```text
setup_results/textcnn_distillation_study/phobert-base/
```

## Teacher khác

Pipeline chấp nhận một thư mục teacher output khác nếu có đủ ba tệp
`train_teacher.csv`, `dev_teacher.csv`, `test_teacher.csv` với cùng schema như
PhoBERT-base:

```powershell
python scripts/distillation/run_textcnn_distillation_study.py `
  --teacher-dir data/distillation/benchmark_teacher_outputs/cafebert `
  --teacher-name CafeBERT
```

Không được ghép dự đoán dev/test của teacher mạnh hơn với soft label train từ
PhoBERT-base. Cùng một teacher phải tạo output cho toàn bộ train/dev/test.

## Đánh giá tài nguyên

Sau khi chạy study, có thể đo ba checkpoint seed 42 trong cùng giao thức CPU:

```powershell
python scripts/distillation/deployment_feasibility_evaluation.py `
  --data-file data/distillation/benchmark_splits/test.csv `
  --teacher-output-file data/distillation/benchmark_teacher_outputs/phobert-base/test_teacher.csv `
  --student "TextCNN hard=setup_results/textcnn_distillation_study/phobert-base/hard/seed_42/char_textcnn_hard_seed_42_model.pt" `
  --student "TextCNN vanilla KD=setup_results/textcnn_distillation_study/phobert-base/vanilla_kd/seed_42/char_textcnn_vanilla_kd_seed_42_model.pt" `
  --student "TextCNN risk-aware KD=setup_results/textcnn_distillation_study/phobert-base/risk_aware_kd/seed_42/char_textcnn_risk_aware_kd_seed_42_model.pt"
```

Chênh lệch teacher–TextCNN phản ánh trade-off kiến trúc và triển khai. Chênh
lệch TextCNN hard–TextCNN KD mới phản ánh tác động của distillation.

## Tiêu chí kết luận

Risk-aware KD chỉ được nâng thành đóng góp chính nếu:

- Recall Label 1 tăng trung bình ít nhất 0,03 so với hard-label;
- Macro-F1 trung bình không giảm quá 0,01;
- cải thiện cùng chiều ở ít nhất hai trong ba seed;
- risk-aware KD tốt hơn vanilla KD trên metric mục tiêu.

Khoảng tin cậy bootstrap chứa 0 được xem là chưa đủ bằng chứng về khác biệt ổn
định. Nếu các điều kiện trên không đạt, distillation được giữ như một cấu hình
benchmark hoặc thí nghiệm phụ, không được quy toàn bộ mức giảm kích thước và độ
trễ của TextCNN thành lợi ích của distillation.
