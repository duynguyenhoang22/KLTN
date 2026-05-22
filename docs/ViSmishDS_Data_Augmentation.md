# Nội dung thực hiện số 1: Xây dựng bộ dữ liệu ViSmishDS sử dụng kỹ thuật Tăng Cường Dữ Liệu bằng LLM

> **Phạm vi:** Label 0 – Tin nhắn hợp lệ (Legitimate SMS) & Label 1 – Tin nhắn lừa đảo (Smishing SMS) tại Việt Nam
> **File liên quan:** `gen_label_0.py` · `gen_label_1.py` · `dataset_label_0.csv` · `dataset_label_1.csv`

---

## Mục lục

1. [Tổng quan bài toán và động lực nghiên cứu](#1-tổng-quan-bài-toán-và-động-lực-nghiên-cứu)
2. [Cơ sở lý thuyết](#2-cơ-sở-lý-thuyết)
3. [Bộ dữ liệu Ground Truth](#3-bộ-dữ-liệu-ground-truth)
4. [Taxonomy đặc trưng cấu trúc theo nhãn](#4-taxonomy-đặc-trưng-cấu-trúc-theo-nhãn)
5. [Phương pháp Tăng Cường Dữ Liệu bằng LLM](#5-phương-pháp-tăng-cường-dữ-liệu-bằng-llm)
6. [Kỹ thuật Prompt Engineering hệ thống](#6-kỹ-thuật-prompt-engineering-hệ-thống)
7. [Thiết kế Prompt theo Category](#7-thiết-kế-prompt-theo-category)
8. [Thư viện Few-Shot Examples](#8-thư-viện-few-shot-examples)
9. [Pipeline sinh dữ liệu và Đánh giá chất lượng](#9-pipeline-sinh-dữ-liệu-và-đánh-giá-chất-lượng)
10. [Tài liệu tham khảo](#10-tài-liệu-tham-khảo)

---

## 1. Tổng quan bài toán và động lực nghiên cứu

### 1.1 Bài toán phân loại SMS nhị phân

Bài toán phân loại tin nhắn SMS tại Việt Nam được định nghĩa là bài toán phân loại nhị phân với hai nhãn:

- **Label 0 – Legitimate SMS:** Tin nhắn hợp lệ từ doanh nghiệp, tổ chức chính thống hoặc cá nhân thực sự. Bao gồm thông báo ngân hàng, viễn thông, thương mại điện tử, dịch vụ công thật, và tin nhắn cá nhân.
- **Label 1 – Smishing SMS:** Tin nhắn lừa đảo (SMS Phishing), cố ý giả mạo tổ chức uy tín hoặc tạo kịch bản giả để đánh cắp thông tin, tài sản nạn nhân.

Mô hình cần học được **ranh giới quyết định (decision boundary)** giữa hai lớp này — đặc biệt trong các trường hợp khó như: tin nhắn ngân hàng thật vs. giả mạo ngân hàng, tin nhắn BHXH thật vs. BHXH scam, quảng cáo hợp lệ vs. cờ bạc/betting.

### 1.2 Thách thức dữ liệu

Bộ dữ liệu thu thập thủ công (ground truth) có quy mô nhỏ: **2,325 mẫu Label 0** và **280 mẫu Label 1**. Sự mất cân bằng nhãn và số lượng mẫu hạn chế dẫn đến hai nguy cơ chính:

- **Overfitting:** Mô hình ghi nhớ pattern cụ thể thay vì học đặc trưng tổng quát.
- **Bias:** Mô hình không nhận diện được các biến thể mới của smishing (concept drift).

Kỹ thuật **Tăng Cường Dữ Liệu bằng LLM (LLM-based Data Augmentation)** được áp dụng để sinh thêm dữ liệu tổng hợp (synthetic data) bổ sung cho ground truth, hướng tới tổng cộng **3,000 mẫu cho nhãn 0 và 5,000 mẫu cho nhãn 1**.

---

## 2. Cơ sở lý thuyết

Phương pháp xây dựng ViSmishDS dựa trên ba nhóm nghiên cứu nền tảng: phát hiện spam/smishing, đặc trưng cấu trúc tin nhắn, và tăng cường dữ liệu bằng LLM.

### 2.1 Phát hiện Smishing và vai trò của obfuscation

**Mishra & Soni (2023) – DSmishSMS** [1] là công trình nền tảng trực tiếp xác nhận rằng *leet words* và *misspelled words* là heuristic phân biệt smishing với tin nhắn hợp lệ: một tin nhắn từ tổ chức uy tín sẽ không bao giờ chứa leet words hay từ viết sai có chủ đích. Đây là căn cứ lý thuyết cho toàn bộ Obfuscation Taxonomy (Label 1) trong nghiên cứu này.

**"Investigating Evasive Techniques in SMS Spam Filtering" (2025)** [2] phân loại các kỹ thuật evasion của spammer thành ba nhóm: (a) *character obfuscation* — thay ký tự bằng ký hiệu tương tự, (b) *lexical manipulation* — biến đổi từ ngữ để qua bộ lọc từ khóa, (c) *crafted perturbations* — gây nhiễu có chủ đích để phá vỡ tokenizer. Paper cũng cảnh báo hiện tượng *concept drift*: mô hình huấn luyện trên dữ liệu lịch sử sẽ thất bại với các pattern obfuscation mới — nhấn mạnh sự cần thiết của dữ liệu đa dạng theo mức độ obfuscation.

**GCC-Spam Framework (2024)** [3] xây dựng *character similarity network* để nắm bắt đặc trưng *orthographic* và *phonetic* nhằm đối phó với character-obfuscation attacks — bằng chứng rằng cần có training data phân tầng theo mức độ obfuscation để mô hình học được robustness thực sự.

**Almeida et al. (2019)** [4] trong systematic review trên 83 paper khẳng định: vẫn còn khoảng trống lớn trong việc cải thiện classifier cho tin nhắn bị obfuscate nặng — khoảng trống mà Obfuscation Level 4–5 trong nghiên cứu này hướng tới lấp đầy, đặc biệt trong bối cảnh tiếng Việt với Unicode diacritics.

**"Building a Multi-class SMS Dataset for Smishing Detection" (2025)** [5] xác nhận rằng smishing có thể được phân loại theo *scenario* mà attacker tạo ra: tin nhắn dạng phần thưởng (greed), gây sợ hãi (fear/urgency), hay giả mạo quyền lực (authority) — và các loại scenario khác nhau gây phản ứng khác nhau ở người dùng. Đây là cơ sở cho cách map 4 chiến lược tâm lý vào 8 category smishing của nghiên cứu này.

### 2.2 Đặc trưng phong cách của tin nhắn hợp lệ

**Sohn, Lee & Rim (2009) – ACL-IJCNLP** [6] là công trình kinh điển đầu tiên đề xuất sử dụng *stylistic features* (đặc trưng phong cách viết) trong biểu diễn SMS bên cạnh content-based features. Nghiên cứu đạt kết quả tốt nhất với 250 lexical và stylistic features, bất kể ngôn ngữ — nền tảng lý thuyết cho Formality Taxonomy (Label 0) trong nghiên cứu này.

**Hosseinpour & Shakibian (2024)** [7] trích xuất 3 loại đặc trưng đồng thời từ SMS: statistical features (TF-IDF), grammatical rule-based features, và *complex network-based structural features* — bằng chứng rằng *cấu trúc* của tin nhắn (không chỉ từ vựng) là đặc trưng phân loại mạnh. Điều này trực tiếp hỗ trợ việc phân loại tin nhắn ham theo độ cứng nhắc của template (template rigidity).

**Jain et al. (2022)** [8] xác nhận URL analysis (domain TLD, brand name trong domain) là đặc trưng mạnh phân biệt smishing với ham — cơ sở lý thuyết cho các pattern domain hợp lệ (`.vn`, `.gov.vn`) vs. domain giả mạo (`.vip`, `.top`, `.icu`) trong cả hai taxonomy.

### 2.3 Điểm mới của nghiên cứu này

Các nghiên cứu trước tập trung vào binary classification (ham vs. spam) với feature engineering chung cho toàn bộ corpus. Nghiên cứu này đề xuất **label-aware structural taxonomy** — phân tầng đặc trưng bên trong từng nhãn — phục vụ cho mục tiêu tạo sinh dữ liệu có kiểm soát:

| Khía cạnh | Nghiên cứu đi trước | Nghiên cứu này |
|---|---|---|
| **Phân loại ham (Label 0)** | Binary, không phân tầng bên trong | 5 mức Formality theo sender type + template rigidity |
| **Phân loại spam (Label 1)** | Nhận diện có/không obfuscation, hoặc phân loại kỹ thuật theo class rời rạc | Thang severity liên tục 6 bậc (Level 0–5) |
| **Ngôn ngữ** | Chủ yếu tiếng Anh, một số multilingual | Tiếng Việt với Unicode diacritics, brand Việt, domain `.vn` |
| **Mục đích taxonomy** | Feature engineering cho detection | Label-aware data generation: hướng dẫn LLM sinh đúng đặc trưng theo category |

---

## 3. Bộ dữ liệu Ground Truth

### 3.1 Label 0 – Legitimate SMS

> Nguồn: `dataset_label_0.csv` — 2,325 mẫu thu thập thủ công

**Phân phối category (heuristic classification):**

| Category | Mẫu | % | Ghi chú |
|---|---|---|---|
| Viễn thông | 1061 | 45.63% | Dominant — Viettel chiếm đa số |
| Cá nhân & OTP | 303 | 13.03% | Personal chat + OTP từ các tổ chức/dịch vụ không phải ngân hàng|
| Dịch vụ công thật | 174 | 7.48% | PCGV, MTTQ, Bộ Công an |
| Quảng cáo hợp lệ | 135 | 5.81% | MoMo chiếm nhiều mẫu lặp |
| Ngân hàng thật | 125 | 5.38% | Chủ yếu OTP + cảnh báo bảo mật |
| Vận chuyển | 18 | 0.77% | Rất ít mẫu thực |
| Thương mại điện tử | 1 | 0.04% | Gần như không có mẫu thực |
| Y tế | 1 | 0.04% | Gần như không có mẫu thực |


**Thống kê metadata:**

| Bên gửi | Số lượng | Tỷ lệ URL (%) | Tỷ lệ SĐT (%) | Content length (mean) |
|---|---|---|---|---|
| brandname | 1757 | 53.78 | 41.61 | 235.64 |
| shortcode | 462 | 40.04 | 48.27 | 237.82 |
| personal_number | 106 | 3.77 | 4.72 | 80.80 |


**Quan sát quan trọng:** Các mẩu tin nhắn về Y tế hay sàn TMĐT cũng như Vận chuyển có rất ít — vì hầu hết để đã có app riêng, nội dung vận đơn thì thường gọi điện trực tiếp chứ không nhắn tin SMS.

### 3.2 Label 1 – Smishing SMS

> Nguồn: `dataset_label_1.csv` — 280 mẫu thu thập thủ công

**Phân loại 8 Category chính:**

| # | Category | Sub-type | Đặc trưng nhận dạng | Ví dụ thực |
|---|---|---|---|---|
| 1 | **Giả mạo ngân hàng** | Account lock, OTP steal, point expiry | Domain giả (.vip, .top, .cc), brandname sender | `"VCB Digibank tran trong thong bao...tai khoan...bi khoa. Dang nhap www.vcbtiebink.com"` |
| 2 | **Đòi nợ / Đe dọa** | Threatening, debt collection | Tên người + CMND + số tiền + deadline + đe dọa gia đình | `"CANH BAO LAN CUOI!!! Trong 24H nua Ong/Ba...phai lien he...thanh toan KHOAN VAY"` |
| 3 | **BHXH / Trợ cấp giả** | BHTN support, COVID support, tax refund | Quy BHTN, NQ-116, deadline "QUA HAN", random code cuối | `"Theo NQ-116, Ong(Ba) da du d!eu k!en NHAN TIEN ho tro tu quy B/H/T/N"` |
| 4 | **Tuyển dụng giả** | Fake job (TikTok, Amazon, eBay, Tiki) | Lương cao (15–30tr/tháng), Zalo contact, không cần vốn | `"Amazon can tuyen nhan vien lam viec tai nha...thu nhap 10tr-50tr/thang...zalo.me/..."` |
| 5 | **Cờ bạc / Betting** | Casino, game bài, xổ số | Bonus code, link ngắn (t.ly, bit.ly), hoa hồng | `"Dang ky + 558k! Nap 50k nhan 108k...No Hu, Ban Ca. DK: t.ly/..."` |
| 6 | **Giả mạo dịch vụ công** | CSGT, Bộ GTVT, Bộ Y Tế, Thuế | Biên lai phạt, "thông báo cuối cùng", link .top/.xyz | `"Cảnh sát Giao thông Việt Nam: Hồ sơ vi phạm...vui lòng truy cập https://dichvucongs.top"` |
| 7 | **Nội dung nhạy cảm** | Dịch vụ tình dục, hẹn hò | Obfuscation nặng ký tự đặc biệt, Telegram/Zalo link | `"Hen h0 tinh m0t dem cung nhung em g@! xinh dep...Telegram;https://sourl.cn/..."` |
| 8 | **Crypto / Đầu tư giả** | "Kiếm tiền online", thả tim, đặt đơn | Telegram group, task farming, "100k/ngày" | `"Chi can 20 phut moi ngay giao vien chuyen nghiep co the huong dan ban kiem 500k-3000k"` |

**Phân phối sender_type theo category:**

```
Giả mạo ngân hàng → brandname (~60%), shortcode (~40%) – KHÔNG dùng personal_number
Đòi nợ / Đe dọa   → 95% personal_number
BHXH / Trợ cấp    → 90% personal_number
Tuyển dụng giả    → 85% personal_number (Zalo cá nhân)
Cờ bạc / Betting  → 70% personal_number, 20% shortcode
Dịch vụ công      → 50% brandname, 30% personal_number, 20% shortcode
Nội dung nhạy cảm → 95% personal_number
Crypto / Đầu tư   → 100% personal_number
```

**Patterns URL / Domain giả mạo:**

```python
FAKE_DOMAIN_PATTERNS = {
    "TLD lạ":      [".vip", ".top", ".xyz", ".cc", ".icu", ".cfd", ".life", ".biz", ".me", ".info"],
    "Brand + TLD": ["vcb-online.vIp", "vietinbank.top", "bidv.xyz", "acb-online-center.com"],
    "Gov giả":     ["dichvucongs.top", "vnta-gov.cc", "hoanthue-tncn.vip", "phatnguoi.xyz"],
    "Subdomain":   ["vietcombank.vn-ms.top", "shb.com.vn-kps.top", "msb.vn-cvs.top"],
    "URL ngắn":    ["bit.ly/...", "t.ly/...", "tinyurl.com/...", "shorturl.at/..."],
    "Homoglyph":   ["vcbtiebink.com", "vniatinbanks.cc", "vovietcombanks.cc"],
}
```

**Chiến lược tâm lý (Social Engineering):**

Dựa trên phân loại scenario của nghiên cứu [5], 4 chiến lược tâm lý được map vào 8 category smishing:

```
URGENCY:  "trước 17h", "trong 24H", "HẾT HẠN", "không thể khôi phục"
FEAR:     "bị khóa tài khoản", "chuyển sang cơ quan điều tra", "nợ xấu CIC"
GREED:    "trúng thưởng iPhone", "điểm thưởng sắp hết hạn", "lương 15-30tr/tháng"
AUTHORITY:"[BỘ CÔNG AN]", "theo NQ-116", "căn cứ Điều 38 Luật Giao dịch điện tử"
```

---

## 4. Taxonomy đặc trưng cấu trúc theo nhãn

Điểm cốt lõi của phương pháp là xây dựng hai taxonomy song song — mỗi taxonomy định nghĩa cấu trúc đặc trưng riêng của từng nhãn — thay vì dùng một tập feature chung cho cả hai lớp.

### 4.1 Formality Taxonomy — Label 0 (Legitimate SMS)

Thay vì obfuscation, tin nhắn hợp lệ được mô tả qua **5 mức độ formality**, từ template cứng nhắc của doanh nghiệp lớn đến tin nhắn cá nhân hoàn toàn. Taxonomy này được xây dựng trên nền tảng của Sohn et al. [6] về stylistic features và Hosseinpour & Shakibian [7] về structural features.

```
LEVEL 0 – Template cứng (doanh nghiệp lớn):
  "[MB] TK 123456****7890 +500,000VND luc 14:23 27/03/26. So du: 2,345,678VND."
  → Ngân hàng, viễn thông lớn: format cố định, không biến thể.
    Structural feature: độ entropy thấp, regex-parseable hoàn toàn.

LEVEL 1 – Template mềm (có biến thể nhỏ):
  "Shopee: Don hang #240327XXXXX cua ban da duoc xac nhan. Du kien giao 28-30/3."
  → TMĐT, logistics: template cố định nhưng trường dữ liệu động biến đổi.
    Structural feature: structure cố định, data fields thay đổi.

LEVEL 2 – Bán formal (doanh nghiệp vừa + nhỏ):
  "KFC Quan 1 xin thong bao: Tu 26-28/3, mua combo bat ky giam 30%. Xem menu: kfc.com.vn/menu"
  → Nhà hàng, siêu thị: ít cứng nhắc, có thể có lỗi nhỏ, bỏ dấu một phần.
    Structural feature: có brand prefix nhưng không strict format.

LEVEL 3 – Thân thiện (dịch vụ tư nhân nhỏ + lễ tân):
  "Phong kham Dr. Lan nhac ban: Lich kham ngay mai 27/3 luc 9h. Co gi thay doi lien he 0901234567 nhe."
  → Phòng khám nhỏ, cửa hàng cá nhân: nhắn như người quen.
    Structural feature: không có brand template cứng, ngữ điệu thân mật.

LEVEL 4 – Cá nhân hoàn toàn:
  "Chieu nay hop 3h nhe. Nho mang tai lieu du an"
  → Tin nhắn cá nhân: không brand, không template, ngắn gọn tự nhiên.
    Structural feature: không có cấu trúc định danh, có thể bỏ dấu hoàn toàn.
    LƯU Ý: Bỏ dấu ở Level 4 là đặc trưng tự nhiên — KHÔNG phải obfuscation.
```

**Mapping Category → Formal Level:**

```python
CATEGORY_FORMAL_RANGE = {
    "Ngân hàng thật":          (0, 1),   # Template cứng → mềm
    "Viễn thông":              (0, 1),   # Template cứng → mềm
    "Thương mại điện tử":      (1, 1),   # Template mềm nhất quán
    "Vận chuyển":              (0, 1),   # Template cứng → mềm
    "Quảng cáo hợp lệ":       (1, 2),   # Mềm → bán formal
    "Dịch vụ y tế":            (2, 3),   # Bán formal → thân thiện
    "Dịch vụ công thật":       (0, 1),   # Template cứng → mềm
    "Tin nhắn cá nhân & OTP":  (0, 4),   # Toàn spectrum: OTP cứng → personal hoàn toàn
}
```

### 4.2 Obfuscation Taxonomy — Label 1 (Smishing SMS)

Tin nhắn smishing sử dụng obfuscation có chủ đích để qua bộ lọc từ khóa. Taxonomy 6 bậc này ánh xạ trực tiếp lên ba nhóm kỹ thuật evasion của nghiên cứu [2]: character obfuscation (Level 1–2), lexical manipulation (Level 2–3), crafted perturbations (Level 4–5). Bậc 0 được thêm vào để mô hình học phân biệt smishing formal (giả mạo tổ chức uy tín) với ham.

```
LEVEL 0 – Không obfuscation (formal, giả mạo tổ chức uy tín):
  "Vietcombank tran trong thong bao tai khoan cua quy khach hien tai da bi khoa."
  → Dùng cho: Giả mạo ngân hàng, Dịch vụ công. Nguy hiểm vì trông "sạch" như ham.

LEVEL 1 – Leet nhẹ (thay 1–2 ký tự):
  "Th0ng ba0: BIDV nang cap he thong. Vui l0ng dang nhap https://b0dv.xyz"
  → Thay vowel bằng số (o→0, a→4, i→1). Đủ đọc hiểu, qua được keyword filter cơ bản.

LEVEL 2 – Leet nặng + tên riêng (pattern: j=d, f=ph, z=d, w=qu):
  "Ong(Ba) da du d!eu k!en NHAN T1EN h0 tro tu quy BH-TN. Bam vao www.mvndc.icu"
  → Obfuscation nhiều ký tự, đặc trưng BHXH scam với random code cuối.

LEVEL 3 – Dot/dash insertion (tách từng ký tự):
  "[A-M-A-Z-O-N] C-h-u-c m-u-n-g b-4-n d-u-o-c t-u-y-3-n. L-u-o-n-g 500k/n-g-4-y"
  → Chèn dấu chấm/gạch ngang giữa ký tự. Phá tokenizer, khó với bag-of-words.

LEVEL 4 – Mixed special chars (nhiễu loạn ký tự):
  "tORKiM! ay:Ma\"n;N,ha7lXklq,uoacx.tech*;G^ja*nh$ap! nhan:thu\"0g"
  "GR N'ha'nL,jen:Qu.a;HangN,gay y H,ojV'ienM:Oj;N'apV,aoT K..."
  → Hỗn hợp ký tự đặc biệt lẫn vào text. Gần như không đọc được với mắt thường.

LEVEL 5 – Extreme noise (gần như không đọc được):
  "j)t.ly/Q5YuG Um Cu,u~Th,ua8% ZJ Na.pVao-LanD:au,UuDa'j:8Tr8 PJ wz8:88.Bma"
  "ỢờỘỤ ĐặngNh_Ảp Chỗ'iNga_y TPNỜH'Ủ NhắnLỉX_ị 8888(Kắ) FrỀ'ễ..."
  → Extreme noise với Unicode diacritics tiếng Việt bị biến dạng. Khoảng trống
    được xác nhận bởi Almeida et al. [4] — hầu hết classifier hiện tại thất bại.
```

**Mapping Category → Obfuscation Level:**

```python
CATEGORY_OBF_RANGE = {
    "Giả mạo ngân hàng": (1, 2),   # Formal giả mạo → leet nhẹ
    "Đòi nợ / Đe dọa":   (0, 1),   # Thường formal/bán formal
    "BHXH / Trợ cấp":    (2, 3),   # Leet nặng → dot/dash insertion
    "Tuyển dụng giả":    (0, 2),   # Đa dạng từ formal đến leet nặng
    "Cờ bạc / Betting":  (2, 3),   # Leet nặng đến dot-split
    "Dịch vụ công":      (1, 2),   # Leet nhẹ đến nặng
    "Nội dung nhạy cảm": (3, 5),   # Dot-split đến extreme noise
    "Crypto / Đầu tư":   (1, 3),   # Leet nhẹ đến dot-split
}
```

### 4.3 So sánh Label 0 vs. Label 1 theo đặc trưng metadata

| Tiêu chí | Label 0 (Legitimate) | Label 1 (Smishing) |
|---|---|---|
| **Obfuscation** | Không có (Level 0 hoàn toàn) | Level 0–5, chủ ý gây nhiễu |
| **Domain** | `.vn`, `.com.vn`, `.gov.vn` — brand name đúng | `.vip`, `.top`, `.cc`, `.icu` — brand name giả |
| **Urgency** | Có nhưng thực chất ("OTP trong 5 phút") | Giả tạo, đe dọa ("mặc định đồng ý", "tài sản mất") |
| **Sender** | Brandname/shortcode chính thống | Giả mạo brandname hoặc personal_number scammer |
| **CTA** | Domain thật, hotline thật | Link giả, Zalo lừa đảo |
| **Grammar** | Chuẩn đến semi-formal, ít lỗi | Chủ ý lỗi (leet), nhiều ký tự đặc biệt [1] |
| **has_url** | ~49% (quảng cáo, logistics có link) | ~75% (link giả là vũ khí chính) [8] |
| **has_phone_number** | ~41% (hotline thật, Viettel nặng dataset) | ~30% (Zalo scam, đòi nợ) |
| **Content length** | 20–300 ký tự (template + data động) | 40–600 ký tự (rất đa dạng) |

---

## 5. Phương pháp Tăng Cường Dữ Liệu bằng LLM

### 5.1 Nguyên lý hoạt động

LLM không "nhớ" dữ liệu thật mà **học phân phối xác suất** của ngôn ngữ. Khi nhận prompt, model khởi tạo ngữ cảnh và tại mỗi token tiếp theo chọn từ top-k tokens có xác suất cao nhất (được điều chỉnh bởi `temperature`). Với data augmentation, điều này có nghĩa:

- `temperature` cao → đa dạng hơn nhưng dễ sinh nội dung không đúng format hoặc brand hallucination.
- `temperature` thấp → nhất quán format nhưng dataset thiếu diversity.
- **Prompt tốt** = thu hẹp không gian tìm kiếm của model → kiểm soát output mà không mất diversity.

### 5.2 Ba tiêu chí chất lượng của Synthetic Data

Dựa trên nghiên cứu về SMS spam [4] và đặc thù của từng nhãn, ba tiêu chí được định nghĩa:

| Tiêu chí | Giải thích | Lý thuyết nền | Hậu quả nếu thiếu |
|---|---|---|---|
| **Fidelity (Độ trung thực)** | Giống với tin nhắn thực tế về format, domain, tên thương hiệu | Sohn et al. [6]: stylistic features là discriminative | Model không học được ranh giới thực với nhãn đối lập |
| **Diversity (Đa dạng)** | Đủ các category, sub-type, và mức độ trong taxonomy | Nghiên cứu [2]: concept drift do pattern mới | Model overfit vào template cứng, thất bại với biến thể thực tế |
| **Novelty (Tính mới)** | Không trùng lặp với data thật hoặc với nhau | Almeida et al. [4]: duplicate inflate dataset giả tạo | Dataset bị inflate, không tăng thông tin học tập thực sự |

**Lưu ý quan trọng về Diversity cho từng nhãn:**
- Label 0: Diversity = đa dạng về *sender type* × *category* × *formal level*. Không phải về obfuscation.
- Label 1: Diversity = đa dạng về *category* × *psychology* × *obfuscation level*.

### 5.3 Few-Shot vs. Zero-Shot

Few-shot learning (cung cấp ví dụ thực trong prompt) hiệu quả hơn rõ rệt so với zero-shot:

```
Zero-shot (không ví dụ):
  Label 0 → Model sinh: "Your account has been credited with 500,000 VND."
             (Tiếng Anh, sai format ngân hàng VN, không có brandname VN)

  Label 1 → Model sinh: "Tài khoản VCB của bạn bị khóa. Xác thực tại vcb.com.vn"
             (Quá sạch, không obfuscation, domain thật — không phải smishing thực tế)

Few-shot (ví dụ thực từ dataset):
  Label 0 → "[MB] TK 123456****7890 +500,000VND luc 14:23 27/03/26. So du: 2,345,678VND.
              Truy van giao dich: 1800 54 54 26."
             (Đúng format MB, số che, hotline thực tế, timestamp VN)

  Label 1 → "VCB Di9ibank: Tk ban bi kh0a bat thuong! Xac thuc NGAY tai vcb-online.vIp
              hoac mat toan bo so du. KHAN CAP!"
             (Obfuscation Level 1, domain giả .vIp, urgency đặc trưng smishing)
```

### 5.4 Thách thức đặc thù của từng nhãn

**Thách thức của Label 0 — "Too clean" problem:**
LLM có xu hướng sinh văn bản quá chuẩn mực. Tin nhắn ham từ doanh nghiệp vừa và nhỏ (Formal Level 2–3) trong thực tế thường có lỗi nhỏ tự nhiên — nhưng LLM sẽ "sửa" thành văn bản hoàn hảo nếu không có few-shot phù hợp. Hệ quả: mô hình học boundary sai, false positive cao với tin nhắn hợp lệ có lỗi nhỏ. Giải pháp: ưu tiên real data làm few-shot cho các category có thể lấy được (Cat1–Cat3, Cat5, Cat7, Cat8).

**Thách thức của Label 0 — Legitimate urgency vs. Smishing urgency:**
Tin nhắn OTP thật CÓ urgency ("sử dụng trong 5 phút") nhưng KHÔNG phải smishing. Mô hình cần học phân biệt urgency hợp lệ (thông tin cụ thể, domain thật, không đe dọa) vs. urgency thao túng (mất tài sản, bị khóa vĩnh viễn, domain giả). Giải pháp: constraint rõ trong prompt, few-shot thể hiện đúng OTP hợp lệ.

**Thách thức của Label 1 — Concept drift và safety filter:**
LLM có safety filter từ chối tạo nội dung harmful. Cần safety framing hợp lệ (nghiên cứu bảo mật) để model hợp tác. Ngoài ra, Level 4–5 obfuscation đòi hỏi temperature cao hơn để sinh được đúng độ nhiễu.

---

## 6. Kỹ thuật Prompt Engineering hệ thống

### 6.0 Cơ sở lý thuyết

Các kỹ thuật trong Section này được xây dựng trên ba trụ cột nghiên cứu có nền tảng học thuật rõ ràng, tích hợp và mở rộng chúng thành một pipeline thống nhất cho bài toán sinh dữ liệu có kiểm soát theo nhãn.

#### Trụ cột 1 — Prompt Pattern (Nền tảng cho kiến trúc Layer)

**White et al. (2023) – "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT"** [P1]
*arXiv:2302.11382, Vanderbilt University. 1,600+ citations.*

Đây là công trình nền tảng hệ thống hóa các kỹ thuật prompt dưới dạng *pattern* tương tự software design patterns. Paper định nghĩa và phân loại các pattern độc lập gồm: **Persona Pattern** (gán vai trò để định hướng góc nhìn output), **Output Customization Pattern** (quy định định dạng và ràng buộc output), **Template Pattern** (cung cấp cấu trúc output mà model phải điền vào), và **Context Control Pattern** (quản lý thông tin ngữ cảnh). Bốn layer trong kiến trúc prompt của nghiên cứu này tương ứng trực tiếp với bốn pattern đó.

Tuy nhiên, White et al. (2023) mô tả các pattern như các đơn vị *độc lập*. Đóng góp của nghiên cứu này là **tích hợp chúng thành một pipeline tuần tự có thứ tự** (Layer 1 → 2 → 3 → 4) được tối ưu cho bài toán sinh batch dữ liệu có nhãn — một use case mà paper gốc không xét đến.

#### Trụ cột 2 — Few-Shot In-Context Learning (Nền tảng cho Layer 3)

**Brown et al. (2020) – "Language Models are Few-Shot Learners" (GPT-3)** [P2]
*NeurIPS 2020. arXiv:2005.14165.*

Công trình nền tảng xác lập cơ chế *in-context learning*: LLM có thể thực hiện task mới chỉ từ vài ví dụ được cung cấp trong prompt mà không cần fine-tuning. Brown et al. định nghĩa chính xác thiết lập few-shot là "model được cung cấp K ví dụ context–completion tại inference time như là điều kiện hóa". Đây là cơ sở lý thuyết cho toàn bộ chiến lược few-shot trong Layer 3: các ví dụ dạng pipe-delimited `content|label|has_url|has_phone_number|sender_type` đóng vai trò là "context–completion pairs" giúp model học cách điền đúng tất cả cột metadata — không chỉ riêng content.

#### Trụ cột 3 — Conditional Prompting cho LLM Data Generation (Nền tảng cho Layer 2)

**Long et al. (2024) – "On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation"** [P3]
*ACL Findings 2024. arXiv:2406.15126.*

Survey có hệ thống về LLM-driven synthetic data generation xác nhận rằng thách thức lớn nhất khi dùng LLM sinh dữ liệu là đảm bảo **diversity**: "trực tiếp prompt LLM tạo dữ liệu cho một task thường cho kết quả lặp lại nhiều". Giải pháp được đề xuất là **conditional prompting** — truyền vào prompt một tập điều kiện (condition-value pairs) để kiểm soát thuộc tính của dữ liệu sinh ra: "với các tổ hợp điều kiện khác nhau, ta có thể tạo ra sự đa dạng được định nghĩa nhân tạo một cách tự động". Kỹ thuật "Biến–Hằng" trong Layer 2 của nghiên cứu này là một hiện thực hóa cụ thể của conditional prompting, trong đó `category × brands_str × style_range` tạo nên condition-value pairs xác định loại và mức độ của mỗi batch.

Paper cũng xác nhận cấu trúc cơ bản của một prompt hiệu quả cho data generation gồm ba thành phần: *task specification*, *in-context demonstrations* (few-shot), và *output format constraints* — tương ứng lần lượt với Layer 2, 3, và 4 trong kiến trúc của nghiên cứu này.

#### Tóm tắt mapping lý thuyết — thực tiễn

| Layer | Kỹ thuật trong nghiên cứu này | Cơ sở lý thuyết |
|---|---|---|
| **Layer 1** — Persona & Task Framing | Gán vai trò domain expert + safety framing cho Label 1 | Persona Pattern — White et al. [P1] |
| **Layer 2** — Task Specification (Biến–Hằng) | Condition-value pairs kiểm soát category, brand, style level per batch | Conditional Prompting — Long et al. [P3] |
| **Layer 3** — Few-Shot Demonstrations | K ví dụ pipe-delimited hoàn chỉnh làm context–completion pairs | In-Context Learning — Brown et al. [P2] |
| **Layer 4** — Output Constraints (Negative Instructions) | Ràng buộc format + danh sách tường minh những gì KHÔNG làm | Output Customization / Template Pattern — White et al. [P1] |

---

### 6.1 Kiến trúc 4-Layer

Prompt hiệu quả được xây dựng theo 4 lớp đồng nhất cho cả hai nhãn, tích hợp trực tiếp Persona Pattern, Conditional Prompting, Few-Shot In-Context Learning, và Output Customization Pattern [P1, P2, P3]:

```
┌─────────────────────────────────────────────────────┐
│  LAYER 1: PERSONA & TASK FRAMING           [P1]    │
│  Vai trò + bối cảnh + (safety framing cho Label 1) │
├─────────────────────────────────────────────────────┤
│  LAYER 2: TASK SPECIFICATION (Biến – Hằng) [P3]    │
│  Category + Brand list + Style range + Batch size  │
├─────────────────────────────────────────────────────┤
│  LAYER 3: FEW-SHOT DEMONSTRATIONS          [P2]    │
│  2–5 examples thực từ dataset (pipe-delimited)     │
├─────────────────────────────────────────────────────┤
│  LAYER 4: OUTPUT CONSTRAINTS               [P1]    │
│  Format + Validation rules + Negative Instructions │
└─────────────────────────────────────────────────────┘
```

### 6.2 Layer 1: Persona & Task Framing

Dựa trên **Persona Pattern** của White et al. [P1]: gán cho LLM một vai trò cụ thể giúp model tập trung vào đúng loại output cần thiết và điều chỉnh "góc nhìn" khi sinh văn bản.

**Label 0** — Không cần safety framing (nội dung hoàn toàn lành mạnh):

```python
SYSTEM_PROMPT_LABEL0 = """Bạn là chuyên gia tạo dữ liệu huấn luyện cho mô hình
phân loại SMS tại Việt Nam. Nhiệm vụ là tạo dữ liệu mô phỏng tin nhắn SMS hợp lệ
(label=0) — bao gồm thông báo từ ngân hàng, viễn thông, thương mại điện tử,
và tin nhắn cá nhân — phản ánh đúng thực tế SMS tại Việt Nam."""
```

**Label 1** — Cần safety framing để tránh LLM từ chối:

```python
SYSTEM_PROMPT_LABEL1 = """Bạn là chuyên gia an ninh mạng đang xây dựng dataset
huấn luyện mô hình phát hiện smishing cho dự án bảo vệ người dùng di động tại
Việt Nam (phối hợp với Bộ TT&TT). Đây là dữ liệu giả lập phục vụ nghiên cứu
bảo mật hợp pháp."""
```

Lý do framing hoạt động: LLM được fine-tune với RLHF để từ chối nội dung harmful trong ngữ cảnh thực. Khi frame rõ là "dữ liệu huấn luyện mô hình bảo mật", model phân loại đây là task hợp pháp và hợp tác. Đây là ứng dụng thực tiễn của Persona Pattern — trong đó persona không chỉ định hướng phong cách mà còn phục vụ mục đích kiểm soát safety boundary [P1].

### 6.3 Layer 2: Task Specification — Kỹ thuật "Biến – Hằng"

Dựa trên **Conditional Prompting** của Long et al. [P3]: truyền tập condition-value pairs vào prompt để kiểm soát thuộc tính của dữ liệu sinh ra, đảm bảo diversity "được định nghĩa nhân tạo" thay vì để model tự quyết định.

Thiết kế theo nguyên tắc: các tham số tạo ra **diversity** là biến thay đổi mỗi batch; các tham số đảm bảo **consistency** là hằng số cố định.

```python
# ─── BIẾN (condition-value pairs) – thay đổi mỗi batch ──────────────────────
category    = random.choice(SCENARIOS.keys())
# Condition 1: loại smishing/ham → xác định psychology, obfuscation range

brands_str  = ", ".join(SCENARIOS[category])
# Condition 2: danh sách brand → model tự mix ngẫu nhiên từng dòng
# (Không chọn 1 brand rồi truyền → tránh batch monotone: 40/40 mẫu cùng 1 brand)

(lo, hi), style_prompt = pick_mixed_style(category)  # Label 1
(lo, hi), style_prompt = pick_formality_style(category)  # Label 0
# Condition 3: style range → gộp MÔ TẢ + FEW-SHOT của TẤT CẢ mức trong [lo, hi]
# → model phân bổ đều các mức trong range, đảm bảo diversity trong batch

batch_size  = min(BATCH_SIZE, TOTAL_SAMPLES - current_total)
# Batch cuối không bao giờ overshoot

# ─── HẰNG – giữ nguyên mọi batch ────────────────────────────────────────────
output_format  = "content|label|has_url|has_phone_number|sender_type"
# Pipe-delimited thay vì comma → tránh escape khi content chứa dấu phẩy
# Parser: lấy 4 phần tử CUỐI làm metadata, phần còn lại ghép lại thành content
```

### 6.4 Layer 3: Few-Shot — Nguyên tắc Coverage Matrix

Dựa trên **In-Context Learning** của Brown et al. [P2]: cung cấp K ví dụ context–completion pairs để model học cách thực hiện task mà không cần fine-tuning. Trong nghiên cứu này, mỗi dòng pipe-delimited hoàn chỉnh đóng vai trò là một context–completion pair, trong đó *context* là phần content và *completion* là bộ metadata `label|has_url|has_phone_number|sender_type`.

**4 nguyên tắc cốt lõi:**
1. **Bao phủ đa dạng:** Mỗi example thể hiện 1 combination khác nhau của `(sender_type × psychology/formality × obfuscation/formal_level)`.
2. **Đủ ngắn:** 2–5 examples là tối ưu (quá nhiều → tốn token, model bị distracted).
3. **Trích từ real data:** Ưu tiên mẫu từ dataset thực vì đã được xác nhận thực tế.
4. **Luôn dùng đầy đủ 5 cột:** Few-shot phải là dòng pipe-delimited hoàn chỉnh `content|label|has_url|has_phone_number|sender_type`. Model cần thấy ground truth của tất cả cột để học cách điền đúng metadata — đây chính là nguyên tắc context–completion pair của Brown et al. [P2]: thiếu completion thì model không có cơ sở học cách điền metadata.

**Coverage Matrix lý tưởng:**

```
Label 1:  Example 1 → brandname + fear    + Level 1  (bank impersonation)
          Example 2 → personal_number + greed + Level 3  (job/gambling scam)
          Example 3 → shortcode + urgency + Level 2  (government fake)

Label 0:  Example 1 → brandname + Level 0  (OTP hoặc giao dịch ngân hàng)
          Example 2 → shortcode + Level 1  (TMĐT hoặc logistics)
          Example 3 → personal_number + Level 3–4  (SME hoặc cá nhân)
```

**Tại sao dùng pipe `|` thay vì comma CSV:**

```
❌ CSV với dấu phẩy: "Nhấp vào ""link"" này",1,1,0,brandname
   → LLM thường không escape đúng RFC 4180 → parse error
   → Content chứa dấu phẩy cần wrap quotes → LLM hay bỏ sót

✅ Pipe-delimited: Nhấp vào "link" này|1|1|0|brandname
   → Không cần escape, không cần wrap quotes
   → Parser dùng split("|") → lấy 4 phần tử cuối → re-serialize bằng csv.writer
```

### 6.5 Layer 4: Negative Instructions

Dựa trên **Output Customization Pattern** và **Template Pattern** của White et al. [P1]: quy định tường minh cấu trúc output và các ràng buộc mà model phải tuân theo. Nghiên cứu này mở rộng thêm chiều **Negative Instructions** — liệt kê rõ những gì KHÔNG được làm — để khắc phục các lỗi đặc thù của LLM khi sinh structured data (quote escaping sai, lặp domain, thêm placeholder literal).

**Cho Label 1:**
```
- "KHÔNG có dòng tiêu đề"
- "KHÔNG có dấu nháy đơn trong sender_type" (fix bug 'brandname')
- "KHÔNG giải thích, KHÔNG markdown fence"
- "KHÔNG lặp lại cùng 1 domain trong batch"
- "KHÔNG dùng brand name thật trong URL"
```

**Cho Label 0:**
```
- "KHÔNG dùng domain giả (.vip, .top, .xyz) — chỉ domain thật (.vn, .com.vn)"
- "KHÔNG thêm urgency đe dọa ('tài khoản bị khóa vĩnh viễn', 'mất toàn bộ số dư')"
- "KHÔNG obfuscate — viết đúng chính tả (có thể bỏ dấu nhưng KHÔNG leet)"
- "KHÔNG dùng placeholder literal ('XXXXXX', '[TÊN]', '[SỐ TIỀN]')"
- "KHÔNG lặp lại cùng 1 mã OTP/mã đơn hàng trong batch"
```

---

## 7. Thiết kế Prompt theo Category

### 7.1 Label 1 — Category Mapping Table

| Category | Sender Type | Psychology chính | Obfuscation Level | Unique patterns |
|---|---|---|---|---|
| Giả mạo ngân hàng | brandname (60%), shortcode (40%) | fear + urgency | 1–2 | Domain `bank.vn-xx.top`, masked account |
| Đòi nợ / Đe dọa | personal_number | fear + authority | 0–1 | Tên + CMND + SĐT Zalo, deadline giờ cụ thể |
| BHXH / Trợ cấp | personal_number | greed + urgency | 2–3 | "NQ-116", random code cuối (4 ký tự), `.icu` |
| Tuyển dụng giả | personal_number | greed | 0–2 | Zalo link, "bán thời gian", lương 15–30tr |
| Cờ bạc / Betting | personal_number, shortcode | greed | 2–3 | Link t.ly/bit.ly, "nạp X nhận Y", bonus code |
| Dịch vụ công | brandname (50%), shortcode (30%), personal_number (20%) | fear + authority | 1–2 | "biên lai phạt", "thông báo cuối cùng", `.top` |
| Nội dung nhạy cảm | personal_number | greed (nhu cầu) | 3–5 | Telegram, Zalo, mix tiếng Anh, ký tự đặc biệt |
| Crypto / Đầu tư | personal_number | greed | 1–3 | Telegram group, "nhiệm vụ", "thả tim", "đặt đơn" |

### 7.2 Label 0 — Category Mapping Table

| Category | Sender Type | Formality Level | has_url | Unique patterns |
|---|---|---|---|---|
| Ngân hàng thật | brandname (70%), shortcode (30%) | 0–1 | OTP: 0%; Giao dịch: 0%; Nhắc nhở: ~20% | Masked account (****), hotline 1800xxxx, prefix brand |
| Viễn thông | brandname (60%), shortcode (40%) | 0–1 | ~30% | Mã USSD (*098#), tên gói, ngày hết hạn |
| Thương mại điện tử | brandname (80%), shortcode (20%) | 1 | ~70% | Mã đơn hàng #, link sàn thật, trạng thái đơn |
| Vận chuyển | brandname (70%), shortcode (30%) | 0–1 | ~30% | Tracking ID, kho phân loại, khung giờ giao |
| Quảng cáo hợp lệ | shortcode (55%), brandname (45%) | 1–2 | ~60% | Mã khuyến mãi, ngày hết hạn, domain thật |
| Dịch vụ y tế | brandname (60%), shortcode (30%), personal_number (10%) | 2–3 | ~20% | Tên bệnh viện/phòng, số phòng, tên khoa |
| Dịch vụ công thật | brandname (70%), shortcode (30%) | 0–1 | ~40% | Domain .gov.vn, tên đơn vị chính xác, không đe dọa |
| Tin nhắn cá nhân & OTP | personal_number (60%), shortcode (30%), brandname (10%) | 3–4 (OTP: 0) | ~10% | OTP 4–8 chữ số, văn phong thân mật, không template |

### 7.3 Prompt Templates (tóm lược cấu trúc)

Mỗi prompt template được cấu trúc theo 4 block tương ứng với 4 Layer:

```python
TEMPLATE = """
[LAYER 1] Bạn là chuyên gia {role}...

NHIỆM VỤ: Tạo đúng {size} dòng CSV tin nhắn {type} (label={label}).
{category_name}: {brands}
Chiến lược: {psychology / formality_description}

[LAYER 2] ĐẶC TRƯNG BẮT BUỘC:
  - YÊU CẦU TRỘN BRAND: BẮT BUỘC chọn NGẪU NHIÊN một brand từ danh sách trên cho mỗi dòng.
  - [Các đặc trưng đặc thù của category]

PHONG CÁCH {NHIỄU / FORMAL}:
{style}  ← Gộp mô tả của tất cả mức trong range, model tự phân bổ đều

[LAYER 3] VÍ DỤ (few-shot – pipe-delimited, KHÔNG copy nguyên, dùng làm tham chiếu style):
{few_shot_examples}

[LAYER 4] QUY TẮC FORMAT (pipe-delimited):
  content|{label}|has_url|has_phone_number|sender_type
  [Các negative constraints đặc thù của category]

QUAN TRỌNG: Đúng {size} dòng pipe-delimited. Không header. Không giải thích. Không markdown.
"""
```

**Trạng thái hoàn thành (Label 1 — 8/8 templates):**

| Category | Few-shot | Prompt Template | Trạng thái |
|---|---|---|---|
| 1 – Giả mạo ngân hàng | 3 candidates | Hoàn chỉnh | ✅ |
| 2 – Đòi nợ / Đe dọa | 3 candidates | Hoàn chỉnh | ✅ |
| 3 – BHXH / Trợ cấp | 4 candidates | Hoàn chỉnh | ✅ |
| 4 – Tuyển dụng giả | 5 candidates | Hoàn chỉnh | ✅ |
| 5 – Cờ bạc / Betting | 5 candidates | Hoàn chỉnh | ✅ |
| 6 – Dịch vụ công | 4 candidates | Hoàn chỉnh | ✅ |
| 7 – Nội dung nhạy cảm | 3 candidates | Hoàn chỉnh | ✅ |
| 8 – Crypto / Đầu tư | 3 candidates | Hoàn chỉnh | ✅ |

**Trạng thái hoàn thành (Label 0 — 2/8 templates đầy đủ, 6/8 có draft):**

| Category | Few-shot | Prompt Template | Trạng thái |
|---|---|---|---|
| 1 – Ngân hàng thật | 3 (real data) | Hoàn chỉnh | ✅ |
| 2 – Viễn thông | 3 (real data) | Hoàn chỉnh | ✅ |
| 3 – Thương mại điện tử | 3 (real data) | Draft | 🔄 |
| 4 – Vận chuyển | 3 (synthetic) | Draft | 🔄 |
| 5 – Quảng cáo hợp lệ | 3 (real data) | Draft | 🔄 |
| 6 – Dịch vụ y tế | 1 real + 3 syn | Draft | 🔄 |
| 7 – Dịch vụ công thật | 3 (real data) | Draft | 🔄 |
| 8 – Tin nhắn cá nhân & OTP | 4 (real data) | Draft | 🔄 |

---

## 8. Thư viện Few-Shot Examples

### 8.1 Nguyên tắc anonymization

Tất cả few-shot examples trích từ real data phải được anonymize trước khi đưa vào tài liệu:

- **Tên người:** Thay bằng tên Việt ngẫu nhiên khác (Lê Hoàng Nam → Nguyen Thi Lan).
- **CMND/CCCD:** Thay bằng số giả đúng format (9 hoặc 12 chữ số, không toàn 0 hoặc toàn 1).
- **Số điện thoại của nạn nhân:** Thay bằng số giả đúng format. Số của scammer giữ nguyên (vì là thông tin của đối tượng lừa đảo).
- **Telegram/Zalo handle thật:** Thay bằng handle giả có cùng structure.
- **Domain giả của scammer:** Giữ nguyên (không phải thông tin cá nhân thật).

### 8.2 Few-Shot Library — Label 1

**Giả mạo ngân hàng (3 candidates — bao phủ fear/greed/fear × Level 1–2):**

```
C1 (brandname + fear + Level 1):
VCB Digibank tran trong thong bao.tai khoan cua quy khach hien tai da bi khoa.
Dang nhap www.vcbtiebink.com de xac thuc ngay hom nay|1|1|0|brandname

C2 (brandname + greed + Level 1):
Vietcombank lưu ý: Bạn có 18699 điểm thưởng sẽ hết hạn sau 24 giờ, vui lòng
truy cập: https://vietcombankd.cfd/vn để đổi quà.|1|1|0|brandname

C3 (brandname + fear + Level 2):
UNG DUNG VCB DIGIBANK cua ban duoc PHAT HIEN KICH HOAT tren thiet bi la.
Neu KHONG PHA BAN KICH HOAT vui long bam vao https://vietcombank.vn-ms.top
de doi thiet bi hoac huy de tranh mat tai san|1|1|0|brandname
```

**BHXH / Trợ cấp (4 candidates — bao phủ Level 1–3 × .icu/.com):**

```
C1 (Level 2, random code, TLD .icu):
[T.B] BHXH: Ong (Ba) da du d!eu k!en NHAN T1EN h0 tro tu quy BH-TN.
Bam vao www.mvndc.icu de lay. QUA HAN SE KH0NG_DUOC CHAP NHAN! oZGa|1|1|0|personal_number

C2 (Level 3, NQ-116, TLD .icu):
Theo _NQ_116, Ong (Ba) da du d!eu k!en NHAN TIEN ho tro tu quy BHTN.
Bam vao www.pwmgh.icu de lay. QUA HAN SE KHONG_DUOC CHAP NHAN! hkDF|1|1|0|personal_number

C3 (Level 1, với dấu, TLD .icu):
Ong/(Ba) da du d!eu'k!en NHAN'TIEN ho tro tu quy-BHTN. Bam'vao www.opaxa.icu
de_'lay. QUA-HAN' SE KH0ng DUOC CHAP_NAHN! JKqc|1|1|0|personal_number

C4 (Level 2, TLD .com — biến thể mo.[random].com):
BHXH VN: Ong(Ba) DU DIEU KIEN nhan tien ho tro BHTN dot 3.
Nhan tai: mo.cvxqa.com truoc khi QUA HAN. tPkm|1|1|0|personal_number
```

> **Phân biệt Level A vs. Level B overlap trong BHXH:**
> Nhiều messages cùng dùng TLD `.icu` với random chars khác nhau là **Level A** — chấp nhận được, đúng thực tế. Cùng string `www.mvndc.icu` xuất hiện nhiều lần trong batch là **Level B** — gây hại vì TF-IDF học chuỗi cụ thể thay vì pattern tổng quát. Negative constraint trong prompt phải chặn Level B.

**Tuyển dụng giả (5 candidates — bao phủ 5 platform × sub-type):**

| Candidate | Platform | Kiểu | has_url | has_phone | Level |
|---|---|---|---|---|---|
| C1 | Amazon | xử lý đơn TMĐT + Zalo link | 1 | 1 | 0 |
| C2 | Cty HVS (generic) | tuyển bán thời gian, formal | 1 | 1 | 0 |
| C3 | Tiki | đặt đơn nâng rank cửa hàng | 0 | 1 | 0 |
| C4 | TikTok | xử lý đơn + nhận tiền 13–25 phút | 1 | 1 | 1 |
| C5 | Shopee/Lazada | xử lý đơn + đánh giá sản phẩm | 1 | 0 | 0 |

> **Phân biệt `has_phone` vs `has_url`:** Khi số điện thoại chỉ nằm trong path của Zalo URL (`zalo.me/84xxx`) và không được liệt kê lại riêng → `has_phone=0`, `has_url=1`. Khi số được liệt kê lại sau link hoặc trực tiếp trong text → `has_phone=1`.

**Cờ bạc / Betting (5 candidates — bao phủ 4 sub-type × Level 1–3):**

| Candidate | Style | Obf Level | URL type | sender_type |
|---|---|---|---|---|
| C1 | "nạp X nhận Y", No Hũ/Bắn Cá | 1 | t.ly | personal_number |
| C2 | App promo, platform list | 2 | .cc domain | personal_number |
| C3 | Casino formal, CSKH 24/24 | 0 | short domain .com | personal_number |
| C4 | Đại lý / hoa hồng recruit | 1 | .vip domain | **shortcode** |
| C5 | Slash-dash obfuscation nặng | 3 | .cc domain | personal_number |

**Đòi nợ / Đe dọa (3 candidates — bao phủ Sub-A/B × Level 0–1):**

| Candidate | Sub-type | Level | has_url | has_phone |
|---|---|---|---|---|
| C1 | Công ty tài chính, tên + CMND + SĐT Zalo | 0 | 0 | 1 |
| C2 | Trung tâm tín dụng formal, 2 mức tiền | 0 | 0 | 0 |
| C3 | Phòng AN NINH ĐIỀU TRA, deadline giờ | 1 | 0 | 0 |

> `has_phone` convention: SĐT local 10 số (0xxxxxxxxx) trong nội dung → `has_phone=1`. SĐT dạng quốc tế (84xxxxxxxxx) → `has_phone=0` theo convention của `dataset_label_1.csv`.

**Dịch vụ công (4 candidates — bao phủ CSGT/GTVT/Thuế × Level 0–2 × brandname/shortcode):**

| Candidate | Cơ quan | Sub-type | sender_type | Level |
|---|---|---|---|---|
| C1 | CSGT | Hồ sơ vi phạm + link .top | brandname | 0 |
| C2 | Bộ GTVT | Biên lai phạt + SĐT | brandname | 0 |
| C3 | CSGT | Tiền phạt chưa thanh toán + link .top | shortcode | 0 |
| C4 | Tổng cục Thuế | Hoàn thuế TNCN + link .vip, obfuscated | personal_number | 2 |

**Nội dung nhạy cảm (3 candidates — bao phủ Level 3–4 × Telegram/Zalo):**

| Candidate | Sub-type | Obf Level | Platform |
|---|---|---|---|
| C1 | Hẹn hò, leet nặng | 3 | Telegram t.me |
| C2 | Hẹn hò, vowel-leet | 3 | Zalo group |
| C3 | Dot-split extreme | 4 | Telegram shortlink |

**Crypto / Đầu tư (3 candidates — bao phủ thả tim/Telegram/chuyển khoản):**

| Candidate | Sub-type | Obf Level | has_url |
|---|---|---|---|
| C1 | Thả tim / 10 nhiệm vụ/ngày | 0 | 0 |
| C2 | Giáo viên hướng dẫn + Telegram | 2 | 1 |
| C3 | Chuyển khoản đầu tư + STK ngân hàng | 0 | 0 |

> **Phân biệt Crypto vs. Tuyển dụng giả:** Crypto KHÔNG đề cập nền tảng TMĐT (Shopee, TikTok Shop), KHÔNG có Zalo phone contact, thu nhập được frame là "đầu tư/nhiệm vụ" thay vì "lương tháng/ngày".

### 8.3 Few-Shot Library — Label 0

**Ngân hàng thật (3 candidates — OTP/giao dịch/cảnh báo × Level 0–1):**

```
C1 (OTP, brandname, Techcombank):
Ma OTP la 22085377. de xac nhan giao dich (TRU TIEN) tu The cua quy khach.
Vui long giu bao mat va khong chia se OTP cho bat cu ai. LH Techcombank: 1800588822
|0|0|1|brandname

C2 (OTP giao dịch, brandname, VCB):
Ma OTP xac thuc GD la 972501, hieu luc 1 phut. Chi tiet GD:Chuyen khoan nhanh
qua so TK,so tien 22,700,000 VND tren kenh Internet cua dich vu VCB Digibank.
|0|0|0|brandname

C3 (Cảnh báo bảo mật, brandname, Vietcombank):
Vietcombank KHONG yeu cau cung cap TEN DANG NHAP, MAT KHAU, OTP qua cac duong
link gui qua SMS. Quy khach hay canh giac va TUYET DOI KHONG cung cap thong tin.
|0|0|0|brandname
```

**Viễn thông (3 candidates — gói cước/cảnh báo/khuyến mãi × Level 0–1):**

```
C1 (Khuyến mãi nạp thẻ, brandname, Viettel):
[TB] NẠP THẺ ĐỦ ĐẦY - DATA XÀI NGAY! Tặng 20% giá trị tất cả thẻ nạp vào
tài khoản viễn thông trong ngày 25/11/2025. Tiền KM sử dụng truy cập Internet
trong 15 ngày. Nạp thẻ online tại https://viettel.vn/naptienkm. Chi tiết gọi 197 bấm 19 (0đ).|0|1|0|brandname

C2 (Cảnh báo hết data, shortcode, Viettel):
Quy khach da dung het luu luong data cua CT Viettel++ va tiep tuc truy cap theo
goi Mobile Internet dang su dung (neu co). Chi tiet LH 198 (0d). Tran trong.|0|0|0|shortcode

C3 (Điểm thành viên, brandname, iTel):
iTel TB: Den het thang 01/2023, Quy khach dang la hoi vien Than Thiet, so diem
iTel Club la 200. Diem iTel Club co gia tri su dung trong vong 12 thang. Truy cap
app MyiTel tai http://onelink.to/myitel de nhan uu dai.|0|1|1|brandname
```

---

## 9. Pipeline sinh dữ liệu và Đánh giá chất lượng

### 9.1 Pipeline tổng thể

```
Ground Truth (dataset_label_0.csv, dataset_label_1.csv)
    ↓
load_seen_contents()  ← Deduplication: loại bỏ content đã có trong ground truth
    ↓
Vòng lặp sinh batch:
    category    = random.choice(SCENARIOS.keys())
    brands_str  = ", ".join(SCENARIOS[category])
    style       = pick_mixed_style(category)  /  pick_formality_style(category)
    batch_size  = min(BATCH_SIZE, remaining)
    prompt      = build_prompt(category, brands_str, style, batch_size)
        ↓
    LLM API call (Gemini) → raw output
        ↓
    extract_valid_rows()  ← Parser pipe-delimited + soft validation
        ↓
    validate_row()  ← Hard validation: columns, label, sender_type, domain check
        ↓
    dedup_check()  ← Loại bỏ duplicate trong batch hiện tại
        ↓
    csv.writer append → synthetic_label_{0/1}.csv
    ↓
Kết thúc khi đạt TOTAL_SAMPLES = 3,000
```

**Chiến lược parse "last 4 parts":**

```python
line.split("|") → parts
content  = "|".join(parts[:-4])   # Nếu content có |, ghép lại đúng
metadata = parts[-4:]              # label, has_url, has_phone, sender — luôn ở cuối
```

### 9.2 Format Validation — Checklist tự động

```python
def validate_row(row: list[str], expected_label: str) -> dict:
    checks = {}
    checks["f1_columns"]   = len(row) == 5
    checks["f2_label"]     = row[1].strip() == expected_label
    checks["f3_has_url"]   = row[2].strip() in ("0", "1")
    checks["f4_has_phone"] = row[3].strip() in ("0", "1")
    checks["f5_sender"]    = row[4].strip() in ("personal_number", "brandname", "shortcode")
    checks["f6_length"]    = 20 <= len(row[0].strip()) <= 600

    # URL consistency check
    import re
    has_url_in_content = bool(re.search(r'https?://|www\.|bit\.ly|t\.ly|tinyurl', row[0]))
    checks["f7_url_consistency"] = not (has_url_in_content and row[2].strip() == "0")

    # Label 0 specific: phát hiện domain giả
    if expected_label == "0":
        fake_tlds = [".vip", ".top", ".xyz", ".cc", ".icu", ".cfd"]
        checks["f8_no_fake_domain"] = not any(tld in row[0].lower() for tld in fake_tlds)
        checks["f9_no_placeholder"] = not any(p in row[0] for p in ["[BRAND]", "[OTP]", "XXXXXX"])

    return checks
```

### 9.3 Content Quality — Checklist review thủ công (10% mỗi batch)

**Cho Label 1:**
- Content có giống smishing thực tế không? (không quá "polished")
- Obfuscation style đúng với level yêu cầu không?
- Domain URL trông như domain giả mạo không?
- Chiến lược tâm lý (fear/greed/urgency) thể hiện rõ không?
- sender_type khớp với loại smishing không?
- Nội dung không lặp lại với mẫu khác trong batch?

**Cho Label 0:**
- Content có đúng format của brand/category không?
- Data động (mã OTP, số tài khoản, mã đơn hàng) đúng format thực tế không?
- Không có domain giả, urgency đe dọa, hay placeholder literal?
- Formal level phù hợp với category không?
- Không "quá sạch" bất thường so với tin nhắn thực tế không?

### 9.4 Distribution Check — Target phân phối

**Cho Label 1 (3,000 mẫu synthetic):**

```
sender_type: ~50% personal_number, ~35% brandname, ~15% shortcode
has_url:     ~75% = 1
has_phone:   ~30% = 1
```

**Cho Label 0 (3,000 mẫu synthetic):**

```
sender_type: ~70% brandname, ~20% shortcode, ~10% personal_number
has_url:     ~40% = 1  (thấp hơn ground truth do bù category imbalance)
has_phone:   ~25% = 1
```

### 9.5 Câu hỏi mở — Sprint tiếp theo

1. **Category imbalance khi sinh Label 0:** Hiện tại `random.choice()` chọn đều 8 categories. Có nên dùng `random.choices()` với trọng số ưu tiên Cat4 (Vận chuyển — 0 mẫu thực) và Cat6 (Y tế — 8 mẫu) không?
2. **Personal message (Cat 8, Label 0):** Ground truth chỉ có 4.6% personal_number. Có nên boost synthetic lên ~15–20% vì đây là hard negative quan trọng để model học phân biệt với crypto scam "thả tim" không?
3. **Temperature riêng theo category:** Level 4–5 obfuscation cần temperature cao hơn (0.95+) để sinh đúng độ nhiễu. Category debt/threat cần temperature thấp hơn để giữ format structured.
4. **Fidelity measurement:** Sau khi có đủ data, đo KNN similarity giữa synthetic và real data để đánh giá fidelity thực sự.
5. **Diversity measurement:** Đo inter-sample cosine similarity để phát hiện nếu model sinh batch quá đồng nhất.

---

## 10. Tài liệu tham khảo

```
[1] Mishra, S., & Soni, D. (2023). DSmishSMS — A System to Detect Smishing SMS.
    Neural Computing and Applications, 35(7), 4975–4992.
    https://doi.org/10.1007/s00521-021-06305-y
    PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC8318556/

[2] Anonymous (2025). Investigating Evasive Techniques in SMS Spam Filtering:
    A Comparative Analysis of Machine Learning Models. JETNR.
    https://www.rjpn.org/jetnr/papers/JETNR2506021.pdf

[3] GCC-Spam Framework (2024). Advancements of SMS Spam Detection:
    A Comprehensive Survey of NLP and ML Techniques. ResearchGate.
    https://www.researchgate.net/publication/385251725

[4] Almeida, T. A., et al. (2019). A Review of Soft Techniques for SMS Spam
    Classification: Methods, Approaches and Applications.
    Engineering Applications of Artificial Intelligence, 86, 130–145.
    https://doi.org/10.1016/j.engappai.2019.08.026

[5] Anonymous (2025). Building a Multi-class Short Message Service Dataset for
    Smishing Detection using Agglomerative Clustering and Dataset Fusion.
    ScienceDirect. https://doi.org/10.1016/j.engappai.2025.XXXXXX
    [Cần cập nhật DOI đầy đủ]

[6] Sohn, D., Lee, J., & Rim, H. (2009). The Contribution of Stylistic
    Information to Content-Based Mobile Spam Filtering.
    Proceedings of ACL-IJCNLP 2009 Conference Short Papers, pp. 321–324.
    [Không có DOI trực tiếp — paper hội nghị ACL 2009;
    được trích dẫn qua Springer 2022: doi.org/10.1007/s11042-022-12991-0]

[7] Hosseinpour, S., & Shakibian, H. (2024). Complex-Network Based Model for
    SMS Spam Filtering. Computer Networks, 255, 110889.
    https://doi.org/10.1016/j.comnet.2024.110889

[8] Jain, A. K., et al. (2022). A Content and URL Analysis-Based Efficient
    Approach to Detect Smishing SMS in Intelligent Systems.
    International Journal of Intelligent Systems, 37(12), 11117–11141.
    https://doi.org/10.1002/int.23035

--- Tài liệu tham khảo bổ sung cho Section 6 (Prompt Engineering) ---

[P1] White, J., Fu, Q., Hays, S., Sandborn, M., Olea, C., Gilbert, H.,
     Elnashar, A., Spencer-Smith, J., & Schmidt, D. C. (2023).
     A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT.
     arXiv:2302.11382. DOI: 10.48550/arXiv.2302.11382
     https://arxiv.org/abs/2302.11382
     → Cơ sở cho Layer 1 (Persona Pattern) và Layer 4 (Output Customization /
       Template Pattern). 1,600+ citations tính đến 2025.

[P2] Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P.,
     ... & Amodei, D. (2020). Language Models are Few-Shot Learners.
     Advances in Neural Information Processing Systems (NeurIPS 2020), 33.
     arXiv:2005.14165
     https://arxiv.org/abs/2005.14165
     → Cơ sở cho Layer 3 (In-Context Learning / Few-Shot Demonstrations).
       Định nghĩa chính xác thiết lập few-shot: "K context–completion pairs
       được cung cấp tại inference time như là điều kiện hóa, không có
       weight updates."

[P3] Long, F., Zeng, Z., Zhang, J., Han, R., & Li, C. (2024).
     On LLMs-Driven Synthetic Data Generation, Curation, and Evaluation:
     A Survey. ACL Findings 2024.
     arXiv:2406.15126
     https://arxiv.org/abs/2406.15126
     → Cơ sở cho Layer 2 (Conditional Prompting). Xác nhận rằng "conditional
       prompting — truyền tập condition-value pairs — là chiến lược chủ đạo
       để đảm bảo diversity trong LLM-driven synthetic data generation."
       Cũng xác nhận cấu trúc 3 thành phần của prompt hiệu quả: task
       specification + demonstrations + output format constraints.
```
