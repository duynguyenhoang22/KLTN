# Huấn luyện CafeBERT và ViCLSR teacher trên Kaggle

Hai script sau thực hiện trọn quy trình trong một lần chạy:

1. fine-tune teacher trên `train.csv`;
2. chọn checkpoint tốt nhất theo Macro-F1 trên `dev.csv`;
3. đánh giá teacher;
4. sinh logits, xác suất \(T=1\), soft target \(T=2\) và distillation weight
   cho `train`, `dev`, `test`;
5. lưu model, teacher outputs, metrics và một tệp ZIP để tải về.

Các script:

- `scripts/distillation/kaggle_train_cafebert_teacher.py`;
- `scripts/distillation/kaggle_train_viclsr_teacher.py`.

ViCLSR dùng phần triển khai chung từ script CafeBERT, vì vậy khi chạy ViCLSR
phải đưa cả hai file Python lên Kaggle trong cùng thư mục.

## 1. Input bắt buộc

Sử dụng đúng benchmark split đã khóa trong repo:

```text
data/distillation/benchmark_splits/
├── train.csv
├── dev.csv
└── test.csv
```

Mỗi CSV tối thiểu phải có:

```text
sample_id,content,label
```

Pipeline hiện tại còn giữ các cột metadata như `data_origin`, `category`,
`sender_type`, `has_url`, `has_phone_number` và `obfuscation_level`. Các cột
này được sao chép sang teacher outputs để audit nhưng không được đưa vào đầu
vào mô hình.

Không dùng `splits_v2/train.csv`, `val.csv`, `test_real.csv` cho thí nghiệm
này. TextCNN study hiện tại sử dụng `benchmark_splits/train/dev/test`, nên
teacher mới phải sinh output trên đúng ba split đó.

## 2. Tạo Kaggle Dataset input

Tạo một Kaggle Dataset, ví dụ `vismish-benchmark`, chứa trực tiếp:

```text
train.csv
dev.csv
test.csv
```

Có thể tạo dataset từ ba file trong
`data/distillation/benchmark_splits/`. Sau khi gắn dataset vào notebook, đường
dẫn thường có dạng:

```text
/kaggle/input/vismish-benchmark/
```

Kiểm tra bằng cell:

```bash
!find /kaggle/input -maxdepth 3 -type f | sort
```

## 3. Thiết lập Kaggle Notebook

Trong phần Notebook Settings:

- Accelerator: GPU;
- Internet: On, để tải model từ Hugging Face;
- Persistence: Files only hoặc mặc định.

Cài thư viện:

```bash
!pip install -q -U \
  transformers datasets accelerate sentencepiece \
  scikit-learn pandas tabulate
```

Nếu phiên bản mới nhất gây xung đột với Kaggle image, dùng:

```bash
!pip install -q \
  "transformers>=4.45,<5" \
  "datasets>=2.20,<4" \
  "accelerate>=0.34,<2" \
  sentencepiece scikit-learn pandas tabulate
```

## 4. Đưa script lên Kaggle

Cách đơn giản nhất là tạo một Kaggle Dataset code chứa hai file:

```text
kaggle_train_cafebert_teacher.py
kaggle_train_viclsr_teacher.py
```

Sau khi attach dataset code, chép script sang working directory:

```bash
!cp /kaggle/input/vismish-distillation-code/kaggle_train_cafebert_teacher.py /kaggle/working/
!cp /kaggle/input/vismish-distillation-code/kaggle_train_viclsr_teacher.py /kaggle/working/
!ls -lh /kaggle/working/*.py
```

Thay `vismish-distillation-code` bằng slug dataset thực tế.

Bạn cũng có thể tạo hai file trực tiếp trong notebook nếu đã đồng bộ repo bằng
Git, miễn chúng nằm cùng thư mục khi chạy ViCLSR.

## 5. Chạy CafeBERT

Lệnh theo cấu hình benchmark đã dùng trước đây:

```bash
!python /kaggle/working/kaggle_train_cafebert_teacher.py \
  --split-dir /kaggle/input/vismish-benchmark \
  --output-dir /kaggle/working/cafebert_teacher \
  --epochs 3 \
  --train-batch-size 16 \
  --eval-batch-size 32 \
  --gradient-accumulation-steps 1 \
  --max-length 128 \
  --learning-rate 2e-5 \
  --seed 42 \
  --temperature 2 \
  --fp16
```

CafeBERT có quy mô lớn. Nếu GPU báo CUDA out-of-memory, giữ effective batch
size bằng 16 nhưng giảm batch thực:

```bash
!python /kaggle/working/kaggle_train_cafebert_teacher.py \
  --split-dir /kaggle/input/vismish-benchmark \
  --output-dir /kaggle/working/cafebert_teacher \
  --epochs 3 \
  --train-batch-size 4 \
  --eval-batch-size 8 \
  --gradient-accumulation-steps 4 \
  --max-length 128 \
  --learning-rate 2e-5 \
  --seed 42 \
  --temperature 2 \
  --fp16
```

Không tự ý giảm `max-length` hoặc đổi split giữa các teacher nếu mục tiêu là
so sánh teacher công bằng.

## 6. Chạy ViCLSR

Cấu hình benchmark:

```bash
!python /kaggle/working/kaggle_train_viclsr_teacher.py \
  --split-dir /kaggle/input/vismish-benchmark \
  --output-dir /kaggle/working/viclsr_teacher \
  --epochs 3 \
  --train-batch-size 8 \
  --eval-batch-size 16 \
  --gradient-accumulation-steps 2 \
  --max-length 128 \
  --learning-rate 2e-5 \
  --seed 42 \
  --temperature 2 \
  --fp16
```

Nếu ViCLSR yêu cầu mã model tùy biến trong một revision tương lai, thêm
`--trust-remote-code`. Không bật tùy chọn này nếu model tải bình thường.

## 7. Output

Sau khi chạy CafeBERT:

```text
/kaggle/working/cafebert_teacher/
├── model/
├── teacher_outputs/
│   ├── train_teacher.csv
│   ├── dev_teacher.csv
│   └── test_teacher.csv
├── teacher_config.json
├── teacher_metrics.json
├── teacher_metrics_by_split.csv
├── teacher_report.md
└── train_metrics.json

/kaggle/working/cafebert_teacher_artifacts.zip
```

ViCLSR tạo cấu trúc tương tự dưới `viclsr_teacher/` và tệp:

```text
/kaggle/working/viclsr_teacher_artifacts.zip
```

Các checkpoint theo epoch được xóa sau khi best model đã được lưu để tránh
nhân nhiều lần kích thước ZIP. Thêm `--keep-checkpoints` chỉ khi thật sự cần
phân tích quá trình huấn luyện.

Teacher CSV có schema tương thích trực tiếp với TextCNN study:

```text
teacher_logit_0
teacher_logit_1
teacher_p0_t1
teacher_p1_t1
teacher_p0_t2
teacher_p1_t2
teacher_temperature
teacher_pred
teacher_confidence
teacher_agree_label
distill_weight
```

## 8. Tải artifact về repo

Tải hai tệp ZIP từ mục Output của Kaggle và giải nén. Sao chép teacher outputs:

```text
cafebert_teacher/teacher_outputs/
→ data/distillation/benchmark_teacher_outputs/cafebert/

viclsr_teacher/teacher_outputs/
→ data/distillation/benchmark_teacher_outputs/viclsr/
```

Kết quả cuối cùng phải là:

```text
data/distillation/benchmark_teacher_outputs/cafebert/
├── train_teacher.csv
├── dev_teacher.csv
└── test_teacher.csv

data/distillation/benchmark_teacher_outputs/viclsr/
├── train_teacher.csv
├── dev_teacher.csv
└── test_teacher.csv
```

Nên lưu model teacher để tái lập:

```text
cafebert_teacher/model/
→ setup_results/distillation_benchmark/plm_cafebert/model/

viclsr_teacher/model/
→ setup_results/distillation_benchmark/plm_viclsr/model/
```

## 9. Chạy TextCNN study với teacher mới

CafeBERT:

```powershell
python scripts/distillation/run_textcnn_distillation_study.py `
  --teacher-dir data/distillation/benchmark_teacher_outputs/cafebert `
  --teacher-name CafeBERT `
  --seeds 42,123,2025 `
  --epochs 12 `
  --patience 3 `
  --skip-existing
```

ViCLSR:

```powershell
python scripts/distillation/run_textcnn_distillation_study.py `
  --teacher-dir data/distillation/benchmark_teacher_outputs/viclsr `
  --teacher-name ViCLSR `
  --seeds 42,123,2025 `
  --epochs 12 `
  --patience 3 `
  --skip-existing
```

Kết quả sẽ lần lượt nằm tại:

```text
setup_results/textcnn_distillation_study/cafebert/
setup_results/textcnn_distillation_study/viclsr/
```

## 10. Kiểm tra trước khi chạy student

Mỗi thư mục teacher phải thỏa mãn:

1. đủ ba file `train_teacher.csv`, `dev_teacher.csv`, `test_teacher.csv`;
2. số dòng bằng đúng split gốc;
3. `sample_id` không trùng và khớp split;
4. có cột `teacher_p1_t2`;
5. xác suất nằm trong `[0,1]`;
6. `teacher_agree_label` và `distill_weight` không rỗng.

Không ghép `train_teacher.csv` từ một model với `dev/test_teacher.csv` của model
khác. Cùng một teacher checkpoint phải sinh output cho cả ba split.

## 11. Diễn giải so sánh teacher

Teacher mạnh hơn trong benchmark không bảo đảm distillation tốt hơn. Cần so
sánh riêng:

- chất lượng teacher trên dev/test;
- hard-label TextCNN;
- vanilla KD theo từng teacher;
- risk-aware KD theo từng teacher;
- độ ổn định qua ba seed.

Việc chọn teacher hoặc hyperparameter phải dựa trên dev. Test chỉ được dùng để
xác nhận xu hướng sau khi giao thức đã khóa.
