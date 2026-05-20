# Nội dung thực hiện số 2: Xây dựng bộ dữ liệu chuẩn hóa văn bản SMS tiếng Việt cho ViSmishDS

> **Phạm vi:** Phase 2 - Text Normalization cho dữ liệu SMS tiếng Việt sau Phase 1  
> **File liên quan:** `vismishds_phase1_final.csv` · `build_phase2_accent_restore_pairs.py` · `build_phase2_full_normalization_dataset_label0.py` · `phase2_accent_restore_pairs.csv` · `phase2_full_normalization_final.csv`

---

## Mục lục

1. [Tổng quan bài toán và động lực nghiên cứu](#1-tổng-quan-bài-toán-và-động-lực-nghiên-cứu)
2. [Cơ sở lý thuyết](#2-cơ-sở-lý-thuyết)
3. [Nguồn dữ liệu Phase 1](#3-nguồn-dữ-liệu-phase-1)
4. [Thiết kế bài toán Phase 2](#4-thiết-kế-bài-toán-phase-2)
5. [Bộ dữ liệu Accent Restoration](#5-bộ-dữ-liệu-accent-restoration)
6. [Bộ dữ liệu Full SMS Normalization](#6-bộ-dữ-liệu-full-sms-normalization)
7. [Prompt Engineering và LLM-assisted Normalization](#7-prompt-engineering-và-llm-assisted-normalization)
8. [Validation, Manual Review và Kiểm soát chất lượng](#8-validation-manual-review-và-kiểm-soát-chất-lượng)
9. [Hướng fine-tuning BARTpho](#9-hướng-fine-tuning-bartpho)
10. [Giới hạn hiện tại và hướng mở rộng](#10-giới-hạn-hiện-tại-và-hướng-mở-rộng)
11. [Tài liệu tham khảo](#11-tài-liệu-tham-khảo)

---

## 1. Tổng quan bài toán và động lực nghiên cứu

### 1.1 Từ phát hiện smishing sang chuẩn hóa văn bản

Phase 1 của ViSmishDS tập trung xây dựng bộ dữ liệu phân loại SMS nhị phân:

- **Label 0:** Tin nhắn hợp lệ.
- **Label 1:** Tin nhắn smishing/lừa đảo.

Tuy nhiên, dữ liệu SMS tiếng Việt trong thực tế không chỉ khác nhau ở nhãn mà còn rất nhiễu ở tầng biểu diễn văn bản:

- Tin nhắn không dấu: `Quy khach da dung het luu luong data...`
- Viết tắt: `TB`, `QC`, `LH`, `CT`, `QK`.
- Dạng ký hiệu/đơn vị: `50K`, `0d`, `30GB`, `9h00`.
- Teencode hoặc obfuscation trong smishing: `th0ng ba0`, `d!eu k!en`, `N-H-A-N`.
- URL, domain, OTP, mã giao dịch, mã gói cước cần được giữ nguyên.

Do đó, Phase 2 được thiết kế như một bước tiền xử lý có kiểm soát nhằm biến SMS nhiễu thành dạng tiếng Việt dễ đọc hơn nhưng vẫn bảo toàn thông tin quan trọng cho bài toán an ninh.

### 1.2 Mục tiêu của Phase 2

Phase 2 có hai mục tiêu dữ liệu:

1. **Accent Restoration:** Tạo cặp dữ liệu `không dấu -> có dấu` từ các SMS đã có dấu trong Phase 1.
2. **Full SMS Normalization:** Chuẩn hóa toàn diện SMS Phase 1 từ dạng không dấu/viết tắt/ký hiệu/obfuscation sang tiếng Việt tự nhiên, bảo toàn số, mã, URL, domain và các tín hiệu an ninh quan trọng.

Điểm quan trọng là Phase 2 không chỉ "làm đẹp câu chữ". Chuẩn hóa sai có thể làm mất tín hiệu phân loại:

- Đổi URL/domain thật thành domain khác làm sai `has_url`.
- Diễn giải OTP/mã giao dịch làm mất định danh nhạy cảm.
- Đổi tag `[VCB]`, `[MSB]`, `[EVN]` thành `[Thông báo]` làm mất sender signal.
- Sửa obfuscation smishing quá mạnh có thể làm mất đặc trưng tấn công.

Vì vậy, Phase 2 được xây dựng theo nguyên tắc **fidelity-first normalization**: chuẩn hóa để dễ học hơn, nhưng không được thay đổi nội dung quan trọng của SMS.

---

## 2. Cơ sở lý thuyết

### 2.1 Text normalization là bài toán biến đổi chuỗi có điều kiện

Text normalization thường được định nghĩa là quá trình chuyển văn bản về một dạng chuẩn/canonical form phục vụ các hệ thống downstream. Các nghiên cứu cổ điển chỉ ra rằng text normalization không có một công thức chung cho mọi ngữ cảnh; nó phụ thuộc vào loại văn bản, ngôn ngữ và mục tiêu xử lý phía sau.

**Graliński et al. (2006)** [1] xem text normalization như một trường hợp đặc biệt của machine translation: nguồn là văn bản nhiễu hoặc dạng viết tắt, đích là dạng đã chuẩn hóa. Cách nhìn này phù hợp trực tiếp với Phase 2 vì mỗi mẫu có thể được biểu diễn như một cặp Seq2Seq:

```text
source_text      = SMS gốc không dấu / viết tắt / nhiễu
normalized_text  = SMS tiếng Việt đã khôi phục dấu và chuẩn hóa có kiểm soát
```

**Aw et al. (2006)** [2] nghiên cứu chuẩn hóa SMS bằng mô hình phrase-based statistical machine translation, cho thấy SMS normalization có thể được mô hình hóa như bài toán dịch từ ngôn ngữ SMS không chuẩn sang ngôn ngữ chuẩn. Điều này hỗ trợ quyết định xây dựng dataset dạng cặp nguồn-đích thay vì chỉ dùng rule-based replacement rời rạc.

**Zhang et al. (2019)** [3] và **Neural Inverse Text Normalization (2021)** [4] tiếp tục củng cố hướng tiếp cận neural Seq2Seq, đồng thời nhấn mạnh rằng rule/FST vẫn hữu ích để kiểm soát lỗi có thể khôi phục. Phase 2 áp dụng tinh thần hybrid này: dùng LLM để sinh candidate normalization nhưng dùng validator/rule để bảo vệ token quan trọng.

### 2.2 Denoising Seq2Seq và BART/BARTpho

**BART (Lewis et al., 2020)** [5] là mô hình denoising autoencoder cho Seq2Seq: làm nhiễu văn bản đầu vào rồi học tái tạo văn bản gốc. Cơ chế này rất gần với bài toán Phase 2, trong đó SMS đầu vào có thể xem như một dạng "corrupted text" do mất dấu, viết tắt, thiếu chuẩn hóa hoặc bị nhiễu ký tự.

**BARTpho (Tran, Le & Nguyen, 2021)** [6] là mô hình Seq2Seq tiền huấn luyện đơn ngữ đầu tiên cho tiếng Việt, gồm hai biến thể:

- `vinai/bartpho-syllable`: xử lý theo âm tiết tiếng Việt.
- `vinai/bartpho-word`: xử lý theo từ sau word segmentation.

BARTpho được báo cáo hiệu quả trên các tác vụ sinh tiếng Việt như tóm tắt, khôi phục viết hoa và khôi phục dấu câu. Vì Phase 2 cũng là bài toán sinh lại chuỗi tiếng Việt chuẩn hóa, BARTpho là lựa chọn tự nhiên cho fine-tuning.

### 2.3 Đặc thù tiếng Việt: dấu, âm tiết và word segmentation

Tiếng Việt dùng chữ Quốc ngữ với hệ thống dấu thanh và dấu nguyên âm giàu thông tin. Mất dấu có thể tạo nhiều nhập nhằng:

```text
ma  -> má / mà / mã / mạ / ma
goi -> gói / gọi / gởi
san -> săn / sàn / san
```

Với SMS, nhập nhằng còn tăng do viết tắt và mã kỹ thuật. Ví dụ `goi cuoc` trong ngữ cảnh viễn thông phải là `gói cước`, không phải `gọi cước`; `san sale` thường là `săn sale`, không phải `sắn sale`.

**VnCoreNLP (Vu et al., 2018)** [7] cung cấp pipeline xử lý tiếng Việt, trong đó word segmentation là bước quan trọng vì tiếng Việt phân tách bằng khoảng trắng theo âm tiết chứ không phải luôn theo từ. Điều này giải thích vì sao Phase 2 ghi chú hai hướng fine-tuning:

- **Syllable-level:** giữ dạng âm tiết, ít phụ thuộc segmenter, phù hợp dữ liệu SMS ngắn và nhiễu.
- **Word-level:** dùng VnCoreNLP để phân đoạn từ, có thể giúp mô hình học đơn vị ngữ nghĩa rõ hơn nhưng dễ chịu ảnh hưởng bởi lỗi segmenter trên SMS nhiễu.

### 2.4 Normalization trong bài toán smishing

Trong phát hiện smishing, normalization là con dao hai lưỡi:

- Với **Label 0**, chuẩn hóa giúp mô hình giảm nhiễu do thiếu dấu, viết tắt, lỗi gõ và format không thống nhất.
- Với **Label 1**, chuẩn hóa quá mạnh có thể xóa mất obfuscation - một tín hiệu tấn công quan trọng đã được Phase 1 dùng để xây dựng taxonomy.

Vì vậy, Phase 2 tách riêng nhãn:

- Label 0 có thể full-normalize vì mục tiêu là phục hồi dạng tin nhắn hợp lệ tự nhiên.
- Label 1 được normalize theo workflow thủ công có AI hỗ trợ, chia batch nhỏ theo mức obfuscation để người thực hiện kiểm soát phần nào cần phục hồi để đọc hiểu và phần nào cần giữ lại như bằng chứng evasion.

---

## 3. Nguồn dữ liệu Phase 1

Phase 2 sử dụng file tổng hợp sau Phase 1:

```text
data/final/vismishds_phase1_final.csv
```

### 3.1 Quy mô tổng thể

| Thành phần | Số dòng |
|---|---:|
| Tổng số SMS Phase 1 | 10,562 |
| Label 0 | 5,320 |
| Label 1 | 5,242 |
| Real data | 2,567 |
| Synthetic data | 7,995 |

### 3.2 Phân phối source dataset

| Source dataset | Số dòng |
|---|---:|
| `synthetic_label_1` | 4,996 |
| `synthetic_label_0` | 2,999 |
| `real_label_0` | 2,321 |
| `real_label_1` | 246 |

### 3.3 Metadata được kế thừa

Các dataset Phase 2 giữ lại metadata từ Phase 1 để phục vụ audit, splitting và phân tích lỗi:

```text
sample_id
content
label
has_url
has_phone_number
sender_type
category
obfuscation_level
data_origin
source_dataset
source_row_id
```

Việc giữ metadata là cần thiết vì chất lượng normalization phụ thuộc mạnh vào ngữ cảnh:

- `category` giúp hiểu miền nội dung: ngân hàng, viễn thông, vận chuyển, dịch vụ công.
- `sender_type` giúp kiểm soát tag đầu tin và văn phong.
- `obfuscation_level` giúp tách Label 1 thành các mức nhiễu khác nhau.
- `data_origin` giúp phân tích khác biệt giữa real và synthetic data.

---

## 4. Thiết kế bài toán Phase 2

### 4.1 Hai task thay vì một task duy nhất

Phase 2 không gom mọi thứ vào một bài toán normalization duy nhất. Thay vào đó, dự án tách thành hai cấp độ:

| Task | Input | Target | Phạm vi | Mục đích |
|---|---|---|---|---|
| `accent_restore` | SMS đã bỏ dấu | SMS gốc có dấu | Label 0 + Label 1 có dấu trong Phase 1 | Huấn luyện phục hồi dấu tiếng Việt |
| `sms_full_normalization` | SMS gốc Phase 1 | SMS đã chuẩn hóa đầy đủ | Label 0 + Label 1 | Huấn luyện khôi phục dấu, viết tắt, đơn vị, casing và giải nhiễu có kiểm soát |

### 4.2 Vì sao cần tách Accent Restoration và Full Normalization

Accent Restoration là bài toán hẹp, ít rủi ro hơn:

```text
source_text:  Bo Thong tin va Truyen thong...
target_text:  Bộ Thông tin và Truyền thông...
```

Full Normalization là bài toán rộng hơn:

```text
source_text:      [TB] Goi ST5K het hieu luc. LH 198 (0d).
normalized_text:  [Thông báo] Gói ST5K hết hiệu lực. Liên hệ 198 (0đ).
```

Full Normalization cần quyết định theo ngữ cảnh:

- `TB` có thể là "thông báo" hoặc "thuê bao".
- `LH` là "liên hệ".
- `CT` có thể là "chương trình".
- `{num}K` trong giá tiền nên là `{num} ngàn đồng`, nhưng trong mã gói `ST5K` phải giữ nguyên.
- `[QC]` có thể đổi thành `[Quảng cáo]`, nhưng `[VCB]` không được đổi thành `[Thông báo]`.

Do độ rủi ro cao hơn, Full Normalization cần validator và review workflow riêng.

### 4.3 Nguyên tắc fidelity-first

Phase 2 áp dụng bốn nguyên tắc:

1. **Bảo toàn nội dung:** Không thêm, xóa, đổi ý nghĩa thông tin trong SMS.
2. **Bảo toàn token nhạy cảm:** Giữ nguyên URL, domain, email, số điện thoại, OTP, mã giao dịch, mã gói cước, mã khuyến mãi.
3. **Chuẩn hóa theo ngữ cảnh:** Mở rộng viết tắt và khôi phục dấu dựa trên miền nội dung.
4. **Tách nhãn theo rủi ro:** Label 0 dùng pipeline LLM + validator; Label 1 dùng manual normalization có AI webchat hỗ trợ theo batch nhỏ để kiểm soát chất lượng.

---

## 5. Bộ dữ liệu Accent Restoration

### 5.1 Mục tiêu

Dataset Accent Restoration được tạo tự động từ các SMS có dấu sẵn trong Phase 1. Mỗi dòng tạo một cặp:

```text
source_text = content sau khi strip Vietnamese accents
target_text = content gốc có dấu
```

Ví dụ:

```text
source_text: [TB] Bo Thong tin va Truyen thong: Hay cai dat su dung ung dung i-Speed...
target_text: [TB] Bộ Thông tin và Truyền thông: Hãy cài đặt sử dụng ứng dụng i-Speed...
```

Task này không xử lý leet, không sửa dấu câu, không mở rộng viết tắt và không sửa casing ngoài những gì đã có trong target gốc.

### 5.2 Pipeline tạo dữ liệu

Script:

```text
scripts/data_pipeline/build_phase2_accent_restore_pairs.py
```

Pipeline:

```text
vismishds_phase1_final.csv
    ↓
Lọc các dòng có dấu tiếng Việt
    ↓
strip_vietnamese_accents(content)
    ↓
Tạo pair_id + source_text + target_text
    ↓
Validate schema, non-empty, source != target
    ↓
phase2_accent_restore_pairs.csv
```

### 5.3 Kết quả dataset

Output:

```text
data/normalization/phase2_accent_restore_pairs.csv
data/reports/phase2_accent_restore_pairs_report.md
```

| Chỉ số | Giá trị |
|---|---:|
| Số cặp cuối cùng | 2,440 |
| Label 0 | 1,397 |
| Label 1 | 1,043 |
| Real data | 1,168 |
| Synthetic data | 1,272 |
| Source length trung bình | 198.23 ký tự |
| Target length trung bình | 198.35 ký tự |

### 5.4 Phân phối theo source dataset

| Source dataset | Số cặp |
|---|---:|
| `real_label_0` | 1,058 |
| `synthetic_label_1` | 933 |
| `synthetic_label_0` | 339 |
| `real_label_1` | 110 |

### 5.5 Phân phối theo obfuscation level

| Obfuscation level | Số cặp |
|---|---:|
| `NONE` | 1,507 |
| `LEVEL 0 – Không obfuscation (formal)` | 499 |
| `LEVEL 2 – Leet nặng + tên riêng` | 225 |
| `LEVEL 3 – Dot/dash insertion` | 65 |
| `LEVEL 4 – Mixed special chars` | 54 |
| `LEVEL 5 – Extreme noise` | 47 |
| `LEVEL 1 – Leet nhẹ (thay 1-2 ký tự)` | 43 |

### 5.6 Ý nghĩa nghiên cứu

Accent Restoration dataset đóng vai trò tầng cơ sở cho tiếng Việt:

- Học khôi phục dấu từ SMS thật/synthetic trong đúng miền smishing.
- Giữ nguyên phân phối domain-specific: ngân hàng, viễn thông, dịch vụ công, scam.
- Có thể dùng như pre-task trước khi fine-tune full normalization.

Tuy nhiên, dataset này không đủ cho chuẩn hóa toàn diện vì nó không học cách mở rộng `LH`, `CT`, `QK`, không sửa `0d -> 0đ`, không xử lý teencode hoặc leet.

---

## 6. Bộ dữ liệu Full SMS Normalization

### 6.1 Mục tiêu

Full SMS Normalization nhằm tạo tập dữ liệu Seq2Seq cuối cùng cho toàn bộ Phase 1:

```text
source_text      = SMS gốc từ Phase 1
normalized_text  = SMS đã khôi phục dấu và chuẩn hóa có kiểm soát
```

Trong triển khai thực tế, Phase 2 được chia thành hai nhánh xử lý:

- **Label 0:** normalize bằng pipeline LLM + validator + manual review.
- **Label 1:** normalize thủ công với sự trợ giúp của AI webchat, copy-paste từng batch nhỏ để kiểm soát chất lượng, đặc biệt với các mức obfuscation cao.

### 6.2 Output

Script chính cho nhánh Label 0:

```text
scripts/data_pipeline/build_phase2_full_normalization_dataset_label0.py
```

File append/manual cho nhánh Label 1:

```text
data/interim/phase2_append/ds012.csv
data/interim/phase2_append/ds345.csv
```

File final chỉ giữ lại hai cột Seq2Seq cần cho BARTpho, kèm định danh:

```text
data/normalization/phase2_full_normalization_content_only.csv
```

### 6.3 Quy mô dataset

| Chỉ số | Giá trị |
|---|---:|
| Tổng cặp Seq2Seq final | 10,562 |
| Label 0 | 5,320 |
| Label 1 | 5,242 |
| Real rows | 2,567 |
| Synthetic rows | 7,995 |
| Source length trung bình | 142.27 ký tự |
| Normalized length trung bình | 153.45 ký tự |
| Dòng có thay đổi so với source | 9,814 |

File final có schema tối giản:

```text
norm_id,sample_id,source_text,normalized_text
```

Thiết kế này cố ý loại bỏ metadata khỏi file huấn luyện trực tiếp để phù hợp với BARTpho Seq2Seq. Metadata vẫn có thể truy ngược qua `sample_id` trong `vismishds_phase1_final.csv`.

### 6.4 Phân phối category

**Label 0:**

| Category | Số dòng |
|---|---:|
| Viễn thông | 1,360 |
| Ngân hàng thật | 576 |
| Khác | 507 |
| Tin nhắn cá nhân và OTP | 500 |
| Quảng cáo hợp lệ | 486 |
| Dịch vụ công thật | 470 |
| Vận chuyển | 418 |
| Thương mại điện tử | 400 |
| Cá nhân & OTP | 301 |
| Dịch vụ y tế | 300 |
| Y tế | 2 |

**Label 1:**

| Category | Số dòng |
|---|---:|
| Nội dung nhạy cảm | 732 |
| Cờ bạc / Betting | 721 |
| Crypto / Đầu tư giả | 719 |
| Tuyển dụng giả | 703 |
| BHXH / Trợ cấp | 678 |
| Dịch vụ công giả | 565 |
| Giả mạo ngân hàng | 519 |
| Đòi nợ / Đe dọa | 477 |
| Cờ bạc/Betting | 53 |
| Khác | 46 |
| BHXH/Trợ cấp giả | 15 |
| Đòi nợ/Đe doạ | 12 |
| Đầu tư/Crypto giả | 2 |

### 6.5 Phân phối sender type toàn bộ file final

| Sender type | Số dòng |
|---|---:|
| `brandname` | 4,680 |
| `personal_number` | 4,617 |
| `shortcode` | 1,265 |

### 6.6 Label 1 manual normalization

Label 1 được chia thành hai nhóm append để phù hợp với độ khó của obfuscation:

| File | Phạm vi | Số dòng |
|---|---|---:|
| `ds012.csv` | Level 0, 1, 2 và một số dòng real/synthetic ít nhiễu | 4,160 |
| `ds345.csv` | Level 3, 4, 5 - dot/dash insertion, mixed special chars, extreme noise | 1,082 |

Mỗi file giữ cột:

```text
content        = SMS gốc
content_after  = SMS đã normalize thủ công có AI hỗ trợ
```

Workflow thực hiện:

```text
Chọn batch nhỏ theo obfuscation level/category
    ↓
Copy source SMS vào AI webchat
    ↓
Yêu cầu normalize nhưng giữ URL/domain/số/mã quan trọng
    ↓
Người thực hiện đọc lại và chỉnh thủ công
    ↓
Ghi vào content_after
    ↓
Append vào dataset final Seq2Seq
```

Lý do dùng manual-in-the-loop cho Label 1:

- Obfuscation là đặc trưng tấn công, không thể tự động xóa sạch.
- Nhiều dòng Level 3-5 gần như không đọc được nếu không xét ngữ cảnh category.
- URL/domain giả, random token, số tiền, số điện thoại scam cần giữ nguyên.
- AI webchat dễ hallucinate hoặc "làm sạch quá mức", nên phải copy-paste ít dòng và kiểm tra từng đợt.

### 6.7 Quy tắc chuẩn hóa chính

Full normalization xử lý các nhóm biến đổi:

| Nhóm | Ví dụ source | Ví dụ normalized | Ghi chú |
|---|---|---|---|
| Khôi phục dấu | `Quy khach` | `Quý khách` | Theo ngữ cảnh |
| Viết tắt | `LH` | `Liên hệ` | Không mở rộng nếu là mã |
| Message tag | `[TB]` | `[Thông báo]` | Chỉ với tag thông báo thật |
| Quảng cáo tag | `[QC]` | `[Quảng cáo]` | Chỉ với tag quảng cáo thật |
| Tiền tệ | `50K`, `0d` | `50 ngàn đồng`, `0đ` | Không sửa mã gói như `ST5K` |
| Giờ | `9h00` | `9 giờ 00` hoặc giữ `9h00` | Không được biến thành số điện thoại |
| Data unit | `30GB`, `500MB` | `30 GB`, `500 MB` | Giá trị phải giữ nguyên |
| URL/domain | `https://viettel.vn` | giữ nguyên | Token bảo vệ |
| Mã định danh | `MA005.N24`, `ST5K` | giữ nguyên | Không tách/diễn giải |
| Leet/obfuscation | `Th0ng ba0`, `N@p_50k` | `Thông báo`, `Nạp 50k` | Chỉ giải nhiễu phần nội dung, giữ URL/domain scam |

### 6.8 Ví dụ lỗi được kiểm soát

Trong pilot và review, một số lỗi LLM thường gặp đã được đưa vào validator:

```text
Sai: [VCB] -> [Thông báo]
Đúng: [VCB] phải giữ nguyên vì là sender/brand tag.

Sai: 9h00 -> Số điện thoại: 00
Đúng: 9h00 là mốc thời gian.

Sai: ST5K -> ST 5 ngàn đồng
Đúng: ST5K là mã gói cước, phải giữ nguyên.

Sai: san sale -> sắn sale
Đúng: săn sale.

Sai: goi cuoc -> gọi cước
Đúng: gói cước trong ngữ cảnh viễn thông.
```

---

## 7. Prompt Engineering và LLM-assisted Normalization

### 7.1 Vai trò của LLM

Full normalization dùng LLM/AI webchat như công cụ hỗ trợ normalization, không dùng như nguồn chân lý tuyệt đối. Với Label 0, LLM được gọi qua pipeline batch có validator. Với Label 1, AI webchat được dùng theo cách thủ công: copy-paste số lượng nhỏ từng đợt, đọc lại output và chỉnh trước khi ghi vào `content_after`.

LLM giúp xử lý các trường hợp cần hiểu ngữ cảnh:

- Khôi phục dấu tiếng Việt.
- Phân biệt nghĩa của viết tắt.
- Chọn cách viết tự nhiên cho SMS doanh nghiệp.
- Giữ nguyên cấu trúc chính của tin nhắn.

Sau đó, validator và manual review quyết định output có được chấp nhận hay không.

### 7.2 System prompt

Prompt hệ thống được thiết kế theo hướng "công cụ normalization", không phải chatbot:

```text
Bạn là công cụ Text Normalization cho SMS tiếng Việt.

Nhiệm vụ: khôi phục tin nhắn SMS không dấu, viết tắt, teencode hoặc bị
obfuscated thành tiếng Việt đầy đủ, tự nhiên, đúng ngữ cảnh.

Chỉ trả về duy nhất câu đã chuẩn hóa. Không giải thích. Không markdown.
Không thêm thông tin mới.
```

Các ràng buộc chính:

- Giữ nguyên ý nghĩa, thứ tự thông tin và cấu trúc chính.
- Không thêm hotline, số điện thoại hoặc thông tin liên hệ.
- Giữ nguyên URL, domain, email, OTP, mã giao dịch, tên gói, mã khuyến mãi.
- Không đổi sender/brand tag như `[VCB]`, `[MSB]`, `[HDBank]`, `[VNU-HCM]`, `[MTTQ Viet Nam]`, `[GHN]`, `[EVN]`.
- Chỉ `[TB]`, `(TB)`, `[T.B]`, `(T.B)` được đổi thành `[Thông báo]`.
- Chỉ `[QC]`, `(QC)` được đổi thành `[Quảng cáo]`.

### 7.3 Batch JSON generation

Để giảm lỗi format, pipeline yêu cầu LLM trả JSON theo batch:

```json
{
  "items": [
    {
      "norm_id": "sms_norm_00001",
      "normalized_text": "..."
    }
  ]
}
```

Thiết kế này có ba lợi ích:

1. Gắn output với `norm_id`, tránh lệch dòng khi batch có nhiều mẫu.
2. Parser có thể kiểm tra schema rõ ràng.
3. Có thể retry hoặc revise từng nhóm lỗi mà không sinh lại toàn bộ dataset.

### 7.4 LLM reviewer

Ngoài generator, pipeline còn có reviewer prompt:

```text
Bạn là reviewer chất lượng cho dataset Text Normalization SMS tiếng Việt.
Nhiệm vụ: so sánh source_text và normalized_text, quyết định output có dùng được không.
```

Reviewer trả về:

```json
{
  "items": [
    {
      "norm_id": "...",
      "verdict": "accept|revise",
      "feedback": "..."
    }
  ]
}
```

Với các dòng cần sửa, pipeline gọi tiếp revision model để tạo bản sửa dựa trên feedback.

---

## 8. Validation, Manual Review và Kiểm soát chất lượng

### 8.1 Validation tự động

Validator trong `build_phase2_full_normalization_dataset_label0.py` kiểm tra nhiều lớp:

| Lớp kiểm tra | Mục tiêu |
|---|---|
| Empty/multiline/explanation | Chặn output rỗng, nhiều dòng, hoặc có giải thích |
| Number preservation | Bảo toàn số trong source |
| Protected token preservation | Bảo toàn URL, email, domain, phone, code token |
| Sender tag preservation | Không đổi tag thương hiệu thành tag generic |
| Hallucination detection | Chặn thêm `Số điện thoại: 00` |
| Length sanity | Chặn output dài bất thường |
| Remaining obfuscation warning | Phát hiện ký tự nhiễu còn sót |
| Suspicious title case | Phát hiện viết hoa tùy tiện |

### 8.2 Trạng thái kết quả

Kết quả cuối cùng của Label 0:

| Validation status | Số dòng |
|---|---:|
| `pass` | 5,267 |
| `manual_pass` | 53 |

| Manual status | Số dòng |
|---|---:|
| `generated` | 5,184 |
| `llm_revised` | 83 |
| `manual_reviewed` | 53 |

Điều này nghĩa là 5,320/5,320 dòng Label 0 đã có `normalized_text` hoàn tất. Các dòng còn rủi ro cao đã được LLM revise hoặc con người review. Sau đó, 5,242 dòng Label 1 được normalize thủ công có AI webchat hỗ trợ qua `ds012.csv` và `ds345.csv`, rồi gộp vào file final Seq2Seq 10,562 dòng.

### 8.3 Manual review app

Ứng dụng review:

```text
scripts/data_pipeline/review_phase2_normalization_app.py
```

Chức năng:

- Mở working CSV.
- Lọc theo `needs_review`, `warning`, `generated`, `manual_reviewed`.
- So sánh `source_text` và `normalized_text`.
- Sửa trực tiếp normalized text.
- `Save & Next` để đánh dấu `manual_reviewed`.

Workflow này giúp xử lý các lỗi mà rule không thể quyết định chắc chắn, ví dụ:

- Cách mở rộng viết tắt phụ thuộc ngữ cảnh.
- Dòng có nhiều mã kỹ thuật.
- Tin nhắn cá nhân ngắn, ít ngữ cảnh.
- Tag đầu tin giống `[TB]` nhưng thực chất là tên riêng/brand.

### 8.4 Final Seq2Seq output

File final phục vụ BARTpho là:

```text
data/normalization/phase2_full_normalization_content_only.csv
```

File này cố ý chỉ giữ lại thông tin tối thiểu cho Seq2Seq:

```text
norm_id,sample_id,source_text,normalized_text
```

Trong đó:

- `source_text` là SMS gốc từ Phase 1.
- `normalized_text` là target normalization sau xử lý Label 0 bằng pipeline và Label 1 bằng manual-in-the-loop.
- `sample_id` giúp truy ngược metadata nếu cần phân tích theo label/category/obfuscation level.

---

## 9. Hướng fine-tuning BARTpho

### 9.1 Mục tiêu fine-tuning

Sau khi có dataset normalization, mô hình BARTpho có thể được fine-tune để học ánh xạ:

```text
source_text -> normalized_text
```

Phase 2 đã có ghi chú Colab tại:

```text
notebooks/BARTpho_Colab_Finetune.md
notebooks/bartpho_normalization_colab.py
```

### 9.2 Cấu hình dữ liệu

Input chính:

```text
data/normalization/phase2_full_normalization_content_only.csv
```

Theo ghi chú hiện tại, file fine-tuning có:

- Cột input: `source_text`.
- Cột target: `normalized_text`.
- Tổng số cặp Seq2Seq: 10,562.
- Không khuyết.
- Không duplicate theo cặp `source_text - normalized_text` trước xử lý sâu hơn.
- Tỉ lệ chia: 90% train, 5% validation, 5% test.

### 9.3 Hai biến thể BARTpho

**BARTpho-syllable**

```python
RUN_VARIANTS = ["syllable"]
```

Ưu điểm:

- Phù hợp bản chất âm tiết của tiếng Việt.
- Ít phụ thuộc word segmentation.
- Có thể bền hơn với SMS ngắn, thiếu dấu, viết tắt.

**BARTpho-word**

```python
RUN_VARIANTS = ["word"]
```

Ưu điểm:

- Học trên đơn vị từ sau phân đoạn.
- Có thể hiểu cụm từ tốt hơn: `gói_cước`, `quý_khách`, `liên_hệ`.

Nhược điểm:

- Cần VnCoreNLP segmentation.
- SMS nhiễu hoặc chứa mã kỹ thuật có thể làm segmenter sai.

### 9.4 Đánh giá đề xuất

Các chỉ số nên dùng:

| Nhóm chỉ số | Mục tiêu |
|---|---|
| Exact Match | Tỷ lệ output trùng target tuyệt đối |
| Character Error Rate | Mức sai khác ký tự, phù hợp restoration |
| Word Error Rate | Mức sai khác token/từ |
| Protected Token Accuracy | URL, phone, OTP, code có được giữ nguyên không |
| Numeric Preservation Rate | Tỷ lệ số trong source còn trong output |
| Human Review Sample | Đánh giá lỗi ngữ nghĩa trên mẫu ngẫu nhiên |

Với bài toán này, Exact Match không nên là chỉ số duy nhất vì một SMS có thể có nhiều bản chuẩn hóa chấp nhận được. Ví dụ `0đ` và `0 đồng` đều hợp lệ nếu giá trị không đổi.

---

## 10. Giới hạn hiện tại và hướng mở rộng

### 10.1 Label 1 đã normalize nhưng cần ghi rõ phạm vi

Phase 2 hiện đã có normalized target cho toàn bộ Label 1 trong file final Seq2Seq. Tuy nhiên, Label 1 không được xử lý bằng cùng pipeline tự động như Label 0 mà được normalize thủ công với sự trợ giúp của AI webchat. Đây là quyết định phù hợp vì smishing có các đặc thù:

- URL/domain giả phải giữ nguyên để phục vụ detection.
- Random suffix token trong BHXH scam có thể là đặc trưng thật.
- Leet trong từ nhạy cảm là tín hiệu evasion.
- Dot/dash insertion và special chars có thể vừa là nhiễu cần đọc hiểu vừa là feature cần bảo toàn.

Do đó, target của Label 1 trong Phase 2 nên được hiểu là **readability-oriented normalization có kiểm soát**, không phải xóa sạch mọi bằng chứng tấn công:

```text
normalize_for_readability != erase_attack_evidence
```

### 10.2 Hướng mở rộng target cho Label 1

Dataset hiện tại chỉ giữ một cặp `source_text -> normalized_text` để phù hợp với BARTpho. Nếu nghiên cứu mở rộng sang explainability/rationale hoặc forensic analysis, có thể cân nhắc tạo thêm nhiều target cho Label 1:

| Hướng | Mô tả | Rủi ro |
|---|---|---|
| Preserve-first | Chỉ khôi phục dấu/viết tắt nhẹ, giữ obfuscation | Output còn nhiễu, khó đọc |
| Readability-first | Giải mã mạnh obfuscation | Mất feature tấn công |
| Dual-target | Tạo hai cột: `readable_text` và `attack_preserving_text` | Tốn công review hơn |

Hướng khả thi nhất cho giai đoạn sau là **dual-target**:

- `readable_text`: phục vụ giải thích/rationale/human inspection.
- `attack_preserving_text`: phục vụ model detection, giữ lại URL/domain/obfuscation cues.

### 10.3 Chuẩn hóa taxonomy category

Trong Phase 1 final hiện còn một số biến thể category lịch sử:

```text
Cờ bạc / Betting
Cờ bạc/Betting

BHXH / Trợ cấp
BHXH/Trợ cấp giả

Đòi nợ / Đe dọa
Đòi nợ/Đe doạ

Crypto / Đầu tư giả
Đầu tư/Crypto giả
```

Trước khi train/evaluate nghiêm ngặt, nên canonicalize category để tránh split hoặc report bị phân mảnh.

### 10.4 Repo hygiene

Một số lưu ý trước khi commit/chia sẻ:

- Không hard-code API key trong script.
- Dùng `MISTRAL_API_KEY` qua environment variable hoặc `.env` bị ignore.
- Thêm `.gitignore` cho `__pycache__/`, `*.py[cod]`, `.env`, `.env.*`.
- Có thể tổ chức lại output theo phase để phân biệt file làm việc, file append thủ công và file final Seq2Seq:

```text
data/outputs/phase2_label0/
data/outputs/phase2_label1/
data/reports/phase2/
scripts/data_pipeline/phase2/
```

---

## 11. Tài liệu tham khảo

```text
[1] Graliński, F., Jassem, K., Wagner, A., & Wypych, M. (2006).
    Text Normalization as a Special Case of Machine Translation.
    Proceedings of the International Multiconference on Computer Science
    and Information Technology, 1, 51-56.
    https://mt-archive.net/IMCSIT-2006-Gralinski.pdf

[2] Aw, A., Zhang, M., Xiao, J., & Su, J. (2006).
    A Phrase-Based Statistical Model for SMS Text Normalization.
    Proceedings of COLING/ACL 2006.
    https://aclanthology.org/P06-2005/

[3] Zhang, H., Sproat, R., Ng, A. H., Stahlberg, F., Peng, X.,
    Gorman, K., & Roark, B. (2019).
    Neural Models of Text Normalization for Speech Applications.
    Computational Linguistics, 45(2), 293-337.
    https://doi.org/10.1162/coli_a_00349

[4] Sunkara, M., Shivade, C., Bodapati, S., & Kirchhoff, K. (2021).
    Neural Inverse Text Normalization.
    arXiv:2102.06380.
    https://arxiv.org/abs/2102.06380

[5] Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed, A.,
    Levy, O., Stoyanov, V., & Zettlemoyer, L. (2020).
    BART: Denoising Sequence-to-Sequence Pre-training for Natural
    Language Generation, Translation, and Comprehension.
    ACL 2020.
    https://arxiv.org/abs/1910.13461

[6] Tran, N. L., Le, D. M., & Nguyen, D. Q. (2021).
    BARTpho: Pre-trained Sequence-to-Sequence Models for Vietnamese.
    arXiv:2109.09701.
    https://arxiv.org/abs/2109.09701

[7] Vu, T., Nguyen, D. Q., Nguyen, D. Q., Dras, M., & Johnson, M. (2018).
    VnCoreNLP: A Vietnamese Natural Language Processing Toolkit.
    NAACL-HLT 2018 Demonstrations.
    https://arxiv.org/abs/1801.01331
```
