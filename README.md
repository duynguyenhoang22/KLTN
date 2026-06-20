# ViSmishDS v2

Nhánh này tái xây dựng ViSmishDS theo nguyên tắc:

1. Dữ liệu nguồn bất biến, không sửa trực tiếp.
2. Metadata v2 độc lập với nhãn và có định nghĩa kiểm chứng được.
3. Annotation có bằng chứng, confidence và lịch sử adjudication.
4. Mọi dữ liệu xử lý, báo cáo và model artifact đều có thể tái tạo.
5. Không commit checkpoint, prediction dump hoặc output thí nghiệm.

## Cấu trúc

```text
configs/                 JSON Schema và taxonomy chính thức
data/
  sources/               dữ liệu nguồn bất biến
  reference/phase1/      snapshot Phase 1 để truy vết và tái gán
  annotations/           output annotation cục bộ, không commit
  processed/             dữ liệu trung gian tái tạo được, không commit
  releases/              bản phát hành đóng băng, không commit mặc định
docs/                    kiến trúc, guideline và kế hoạch migration
src/vismishds/           pipeline v2 có thể kiểm thử
tests/                   test tự động
thesis/drafts/           bản thảo luận văn đang sử dụng
```

## Khởi động

```powershell
python -m pip install -e .[dev]
python -m vismishds audit-reference
python -m vismishds init-pilot --size 400 --seed 42
python -m pytest
```

Dataset canonical v2 sử dụng JSONL vì nhiều metadata là multi-label. CSV chỉ
được dùng làm giao diện annotation hoặc export phẳng.

Đọc [phạm vi dataset](docs/dataset_scope.md),
[kiến trúc](docs/architecture.md), [annotation guideline](docs/annotation_guidelines.md)
và [kế hoạch migration](docs/migration_plan.md) trước khi sửa dữ liệu.
