# Cleanup manifest

Ngày tái cấu trúc: 2026-06-20

## Đã giữ

- Dữ liệu real gốc trong `data/sources/real/`.
- Raw ViLexNorm trong `data/sources/external/vilexnorm/`.
- Một snapshot Phase 1 trong `data/reference/phase1/`.
- Bản thảo Chương 4, Chương 5 và kịch bản thuyết trình trong `thesis/drafts/`.

## Đã loại khỏi nhánh v2

- `model/`, `models/`: checkpoint, tokenizer copy và binary model.
- `setup_results/`: prediction dump, confusion matrix và kết quả Setup A–G.
- `notebooks/`: notebook thử nghiệm và notebook archive.
- `scripts/`: pipeline Phase 1/2, one-off scripts, distillation và scripts vẽ.
- synthetic cũ, normalization output, distillation split/teacher output.
- hard-negative output, report phát sinh và các bản dataset final trùng lặp.
- ứng dụng review cũ và các file tạm ở root.
- tài liệu prompt/taxonomy cũ có định nghĩa mâu thuẫn với v2.

Git history của nhánh gốc vẫn là nơi truy xuất các artifact đã loại. Không sao
chép chúng vào `legacy/`, vì việc đó chỉ chuyển sự lộn xộn sang vị trí khác.
