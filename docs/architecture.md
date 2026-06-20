# Kiến trúc ViSmishDS v2

## Nguồn sự thật

Luồng dữ liệu một chiều:

```text
sources + Phase 1 reference
          ↓
annotation batches
          ↓
human review / adjudication
          ↓
canonical JSONL
          ↓
frozen splits and experiment inputs
          ↓
reports and model artifacts
```

Không có bước nào được sửa ngược dữ liệu nguồn. Dữ liệu canonical không lấy
metadata từ tên file, tên setup hoặc prediction của mô hình.

## Ranh giới trách nhiệm

- `configs/`: hợp đồng dữ liệu. Thay đổi taxonomy phải tăng phiên bản.
- `src/vismishds/`: code duy nhất được xem là pipeline chính thức.
- `data/sources/`: nguyên liệu bất biến.
- `data/reference/`: bằng chứng lịch sử, không phải release mới.
- `data/annotations/`: giao diện làm việc, chưa phải ground truth.
- `data/releases/`: output được đóng băng sau quality gate.
- `thesis/`: văn bản học thuật; không chứa source code hoặc output lớn.

## Artifact policy

Checkpoint, prediction-level dump, hình, bảng kết quả và cache không được
commit. Chúng phải được sinh từ manifest thí nghiệm và ghi vào `artifacts/`
hoặc `reports/generated/`, đều bị Git ignore.

Một kết quả chỉ được trích vào luận văn khi có:

1. dataset release ID;
2. commit hash;
3. config và random seed;
4. metric script;
5. đường dẫn artifact bên ngoài Git.
