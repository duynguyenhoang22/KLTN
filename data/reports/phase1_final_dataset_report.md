# Báo cáo Dataset Cuối Phase 1

Báo cáo này được cập nhật theo snapshot hiện tại của `data/final/vismishds_phase1_final.csv` vào ngày 2026-05-19.

## Đầu ra

- Dataset: `data/final/vismishds_phase1_final.csv`
- Số dòng: 10,562
- Các cột: `sample_id`, `content`, `label`, `has_url`, `has_phone_number`, `sender_type`, `category`, `obfuscation_level`, `data_origin`, `source_dataset`, `source_file`, `source_row_id`
- Tổng số dòng nguồn trước khi loại trùng nội dung đã chuẩn hoá: 10,574
- Số dòng bị loại do trùng nội dung đã chuẩn hoá: 12
- Số nội dung trùng còn lại trong dataset cuối: 0
- Giá trị dùng cho mức obfuscation không áp dụng: `NONE`

## Kiểm kê nguồn dữ liệu

| source_dataset    | source_file                                           |   số dòng trước dedup |   số dòng sau dedup |
|:------------------|:------------------------------------------------------|----------------------:|--------------------:|
| real_label_0      | data/ground_truth/dataset_label_0_with_categories.csv |                  2327 |                2321 |
| real_label_1      | data/ground_truth/dataset_label_1_with_categories.csv |                   247 |                 246 |
| synthetic_label_0 | data/synthetic/synthetic_label_0.csv                  |                  3000 |                2999 |
| synthetic_label_1 | data/synthetic/synthetic_label_1.csv                  |                  5000 |                4996 |

## Cân bằng nhãn

|   label |   số dòng |   tỷ lệ (%) |
|--------:|----------:|------------:|
|       0 |      5320 |       50.37 |
|       1 |      5242 |       49.63 |

## Cân bằng nguồn gốc dữ liệu

| data_origin   |   số dòng |   tỷ lệ (%) |
|:--------------|----------:|------------:|
| real          |      2567 |       24.30 |
| synthetic     |      7995 |       75.70 |

## Số lượng theo nhãn và nguồn gốc

|   label | data_origin   |   số dòng |
|--------:|:--------------|----------:|
|       0 | real          |      2321 |
|       0 | synthetic     |      2999 |
|       1 | real          |       246 |
|       1 | synthetic     |      4996 |

## Số lượng theo loại người gửi

|   label | sender_type     |   số dòng |
|--------:|:----------------|----------:|
|       0 | brandname       |      4020 |
|       0 | shortcode       |       831 |
|       0 | personal_number |       469 |
|       1 | personal_number |      4148 |
|       1 | brandname       |       660 |
|       1 | shortcode       |       434 |

## Metadata URL và số điện thoại

|   label |   has_url |   has_phone_number |   số dòng |
|--------:|----------:|-------------------:|----------:|
|       0 |         0 |                  0 |      2739 |
|       0 |         0 |                  1 |       913 |
|       0 |         1 |                  0 |       987 |
|       0 |         1 |                  1 |       681 |
|       1 |         0 |                  0 |       634 |
|       1 |         0 |                  1 |       670 |
|       1 |         1 |                  0 |      3155 |
|       1 |         1 |                  1 |       783 |

## Số lượng theo danh mục

|   label | category                |   số dòng |
|--------:|:------------------------|----------:|
|       0 | Viễn thông              |      1360 |
|       0 | Ngân hàng thật          |       576 |
|       0 | Khác                    |       507 |
|       0 | Tin nhắn cá nhân và OTP |       500 |
|       0 | Quảng cáo hợp lệ        |       486 |
|       0 | Dịch vụ công thật       |       470 |
|       0 | Vận chuyển              |       418 |
|       0 | Thương mại điện tử      |       400 |
|       0 | Cá nhân & OTP           |       301 |
|       0 | Dịch vụ y tế            |       300 |
|       0 | Y tế                    |         2 |
|       1 | Nội dung nhạy cảm       |       732 |
|       1 | Cờ bạc / Betting        |       721 |
|       1 | Crypto / Đầu tư giả     |       719 |
|       1 | Tuyển dụng giả          |       703 |
|       1 | BHXH / Trợ cấp          |       678 |
|       1 | Dịch vụ công giả        |       565 |
|       1 | Giả mạo ngân hàng       |       519 |
|       1 | Đòi nợ / Đe dọa         |       477 |
|       1 | Cờ bạc/Betting          |        53 |
|       1 | Khác                    |        46 |
|       1 | BHXH/Trợ cấp giả        |        15 |
|       1 | Đòi nợ/Đe doạ           |        12 |
|       1 | Đầu tư/Crypto giả       |         2 |

## Số lượng theo mức obfuscation

| obfuscation_level                    |   số dòng |
|:-------------------------------------|----------:|
| NONE                                 |      7823 |
| LEVEL 3 – Dot/dash insertion         |       670 |
| LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)  |       651 |
| LEVEL 0 – Không obfuscation (formal) |       638 |
| LEVEL 2 – Leet nặng + tên riêng      |       386 |
| LEVEL 4 – Mixed special chars        |       255 |
| LEVEL 5 – Extreme noise              |       139 |

## Mức obfuscation trong synthetic smishing

Bảng này chỉ tính các dòng có `source_dataset = synthetic_label_1`.

| obfuscation_level                    |   số dòng |
|:-------------------------------------|----------:|
| NONE                                 |      2257 |
| LEVEL 3 – Dot/dash insertion         |       670 |
| LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)  |       651 |
| LEVEL 0 – Không obfuscation (formal) |       638 |
| LEVEL 2 – Leet nặng + tên riêng      |       386 |
| LEVEL 4 – Mixed special chars        |       255 |
| LEVEL 5 – Extreme noise              |       139 |

## Tóm tắt kiểm tra

- Các cột bắt buộc đều tồn tại và không có giá trị thiếu trong dataset cuối hiện tại.
- `sample_id` là duy nhất trên toàn bộ 10,562 dòng.
- `content` sau khi chuẩn hoá bằng lowercasing, trim và gộp khoảng trắng không còn trùng lặp.
- Hai nhãn gần cân bằng: label 0 có 5,320 dòng và label 1 có 5,242 dòng.
- Dataset vẫn thiên về dữ liệu synthetic: 7,995 dòng synthetic so với 2,567 dòng real.
- Các cột truy vết nguồn (`source_dataset`, `source_file`, `source_row_id`) đều được điền cho mọi dòng.

## Ghi chú kết thúc Phase 1

- Báo cáo này audit snapshot dataset cuối hiện tại, không tái sinh dataset từ các file nguồn.
- Dataset cuối hiện tại phù hợp để dùng cho các bước phase 2 normalization và các baseline phân loại smishing.
- Khi đánh giá mô hình cuối, nên giữ tập test chỉ gồm dữ liệu real hoặc báo cáo riêng metric cho real và synthetic, vì dữ liệu synthetic chiếm 75.70% file hiện tại.
- Nhãn danh mục vẫn có một số quy ước đặt tên gần trùng nhau, ví dụ `Cờ bạc / Betting` và `Cờ bạc/Betting`; cần lưu ý khi gom nhóm metric theo category.
- `obfuscation_level = NONE` bao gồm các dòng benign/real không áp dụng obfuscation và 2,257 dòng synthetic smishing chưa có mức obfuscation cụ thể.
