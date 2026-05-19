# Cấu trúc repo

Tài liệu này mô tả cây thư mục sau khi tái tổ chức hậu Phase 2.

## Thư mục chính

| Đường dẫn | Vai trò |
|:--|:--|
| `apps/` | Công cụ giao diện nhỏ phục vụ rà soát hoặc demo nội bộ. |
| `data/ground_truth/` | Dữ liệu thực đã gắn nhãn. |
| `data/synthetic/` | Dữ liệu synthetic đã tạo và hiệu chỉnh. |
| `data/final/` | Dataset cuối dùng cho các phase chính. |
| `data/normalization/` | Dataset và artifact chính của Phase 2 normalization. |
| `data/interim/` | File trung gian, split phụ, output thử nghiệm; không phải nguồn chính. |
| `data/archive/` | Bản cũ hoặc artifact cần giữ để truy vết nhưng không dùng trong pipeline hiện tại. |
| `data/reports/` | Báo cáo audit, kiểm tra, review dữ liệu. Mọi report mới nên viết bằng tiếng Việt. |
| `docs/` | Tài liệu tổng quan, audit dạng markdown, ghi chú quy trình. |
| `model/` | Code thử nghiệm mô hình phân loại. |
| `notebooks/` | Notebook phân tích, audit, fine-tuning. |
| `notebooks/archive/` | Notebook cũ hoặc notebook thao tác một lần đã hoàn tất. |
| `scripts/data_pipeline/` | Script tạo, kiểm tra, hiệu chỉnh và build dataset. |
| `scripts/one_off/` | Script thao tác một lần, giữ lại để truy vết lịch sử xử lý. |

## Dataset chính hiện tại

| Phase | File |
|:--|:--|
| Phase 1 final | `data/final/vismishds_phase1_final.csv` |
| Phase 2 normalization final | `data/normalization/phase2_full_normalization_content_only.csv` |
| Phase 2 normalization audit source | `data/normalization/phase2_full_normalization_final.csv` |
| Phase 2 plain normalized lines | `data/normalization/phase2_full_normalization_lines.txt` |

## Quy ước

- Không đặt notebook hoặc file markdown phân tích ở root.
- Không đặt file tạm trong `data/final/`; chỉ giữ dataset cuối ở đó.
- File output từ training hoặc split thử nghiệm nên đặt trong `data/interim/` và chỉ commit khi thật sự cần truy vết.
- Script một lần không dùng cho pipeline hiện hành nên đặt trong `scripts/one_off/`.
- Report mới viết bằng tiếng Việt và đặt trong `data/reports/`.
