# BÁO CÁO NỘI DUNG THỰC HIỆN SỐ 1
## Xây dựng bộ dữ liệu ViSmishDS sử dụng kỹ thuật Tăng cường dữ liệu bằng Mô hình ngôn ngữ lớn (LLM)

---

## 1. Tổng quan và Động lực nghiên cứu

### 1.1 Bài toán phân loại tin nhắn SMS
Nghiên cứu xác định việc phân loại tin nhắn văn bản tại Việt Nam là một bài toán phân loại nhị phân trọng yếu trong lĩnh vực an ninh mạng. Bài toán được định nghĩa qua hai nhãn chính:
* **Nhãn 0 (Legitimate SMS):** Tin nhắn hợp lệ từ các tổ chức chính thống hoặc cá nhân.
* **Nhãn 1 (Smishing SMS):** Tin nhắn lừa đảo có mục đích chiếm đoạt thông tin hoặc tài sản.

### 1.2 Thách thức về dữ liệu thực tế
Tập dữ liệu thu thập thực tế (Ground Truth) ghi nhận sự mất cân bằng đáng kể giữa các nhãn:
* **Nhãn 0:** 2.325 mẫu (chiếm ưu thế).
* **Nhãn 1:** 280 mẫu (mật độ thấp).

Sự thiếu hụt dữ liệu Nhãn 1 dẫn đến nguy cơ mô hình bị quá khớp (overfitting) và không đủ khả năng nhận diện các biến thể tinh vi. Do đó, kỹ thuật tăng cường dữ liệu dựa trên LLM được áp dụng để chuẩn hóa quy mô tập dữ liệu lên **3.000 mẫu mỗi nhãn**.

---

## 2. Cơ sở lý thuyết

Nghiên cứu kế thừa và phát triển từ các nền tảng khoa học sau:
1. **Nhận diện kỹ thuật lẩn tránh:** Dựa trên các nghiên cứu về *character obfuscation* và *lexical manipulation* [1] để xây dựng hệ thống phân tầng nhiễu.
2. **Đặc trưng phong cách ngôn ngữ:** Sử dụng các chỉ số về tính trang trọng và cấu trúc văn bản [6] để định nghĩa các mẫu tin nhắn hợp lệ.
3. **Tăng cường dữ liệu (Data Augmentation):** Tận dụng khả năng học phân phối xác suất của các mô hình ngôn ngữ lớn để sinh dữ liệu tổng hợp có kiểm soát.

---

## 3. Phân tích tập dữ liệu thực tế (Ground Truth)

### 3.1 Thống kê Nhãn 0 (Tin nhắn hợp lệ)
Tập dữ liệu Nhãn 0 tập trung chủ yếu vào lĩnh vực Viễn thông, trong khi các lĩnh vực khác như Vận chuyển và Y tế có sự hiện diện rất thấp.

| Lĩnh vực | Tỷ lệ (%) | Đặc trưng chủ đạo |
| :--- | :--- | :--- |
| Viễn thông | 41.5% | Thông báo nạp thẻ, gói cước. |
| Cá nhân & OTP | 10.8% | Mã xác thực và trao đổi cá nhân. |
| Quảng cáo | 7.3% | Khuyến mãi từ các ứng dụng thanh toán. |
| Vận chuyển | 0.0% | Thiếu hụt dữ liệu thực tế. |

### 3.2 Thống kê Nhãn 1 (Tin nhắn lừa đảo)
Dữ liệu Nhãn 1 thể hiện sự đa dạng trong kịch bản tấn công, với các chiến lược tâm lý rõ rệt.

| Kịch bản | Chiến lược tâm lý | Dấu hiệu nhận biết |
| :--- | :--- | :--- |
| Giả mạo ngân hàng | Sợ hãi (Fear) | Tên miền giả (.vip, .top), cảnh báo khóa tài khoản. |
| BHXH/Trợ cấp | Tham lam (Greed) | Thông báo nhận tiền hỗ trợ, thời hạn gấp rút. |
| Tuyển dụng | Tham lam | Thu nhập cao, không yêu cầu kinh nghiệm. |
| Đòi nợ/Đe dọa | Quyền lực (Authority) | Tên riêng, số CMND, đe dọa cưỡng chế. |

---

## 4. Hệ thống phân tầng đặc trưng (Label-aware Taxonomy)

### 4.1 Thang đo mức độ trang trọng (Nhãn 0)
Tin nhắn hợp lệ được phân tầng theo độ cứng nhắc của cấu trúc văn bản (Template Rigidity) thay vì các đặc trưng gây nhiễu.

| Cấp độ | Loại hình | Mô tả |
| :--- | :--- | :--- |
| **Cấp 0** | Template cứng | Định dạng cố định hoàn toàn (Ngân hàng, OTP). |
| **Cấp 1** | Template mềm | Cấu trúc ổn định với các trường dữ liệu động. |
| **Cấp 2** | Bán trang trọng | Ngôn ngữ linh hoạt hơn (Quảng cáo, doanh nghiệp vừa và nhỏ). |
| **Cấp 3** | Thân thiện | Văn phong giao tiếp gần gũi (Phòng khám, dịch vụ nhỏ). |
| **Cấp 4** | Cá nhân | Hoàn toàn tự nhiên, không theo khuôn mẫu. |

### 4.2 Thang đo mức độ gây nhiễu (Nhãn 1)
Áp dụng để mô phỏng các kỹ thuật lẩn tránh bộ lọc từ khóa của đối tượng lừa đảo.

| Cấp độ | Kỹ thuật | Ví dụ minh họa |
| :--- | :--- | :--- |
| **Cấp 0** | Formal | Giả mạo văn phong chuẩn mực của tổ chức. |
| **Cấp 1** | Leet nhẹ | Thay thế nguyên âm bằng số (o -> 0). |
| **Cấp 3** | Chèn ký tự | Dùng dấu gạch ngang/chấm để phá tokenizer (T-H-O-N-G-B-A-O). |
| **Cấp 5** | Nhiễu cực hạn | Kết hợp ký tự đặc biệt và biến dạng Unicode. |

---

## 5. Phương pháp Tăng cường dữ liệu bằng LLM

### 5.1 Kiến trúc Prompt 4 lớp
Hệ thống Prompt được thiết kế theo cấu trúc phân tầng để tối ưu hóa khả năng tạo sinh:
1. **Lớp 1 - Thiết lập vai trò (Persona):** Định nghĩa ngữ cảnh chuyên gia (An ninh mạng/Dữ liệu).
2. **Lớp 2 - Đặc tả nhiệm vụ:** Truyền danh sách thực thể (brand) và kịch bản mục tiêu.
3. **Lớp 3 - Học máy từ ví dụ (Few-shot):** Cung cấp các mẫu thực tế làm tham chiếu phong cách.
4. **Lớp 4 - Ràng buộc đầu ra:** Định dạng pipe-delimited (|) để xử lý dữ liệu tự động.

### 5.2 Thư viện ví dụ đối chiếu (Few-Shot Library)

| Nhãn | Kịch bản | Ví dụ minh họa (Tham chiếu) | Mức độ |
| :--- | :--- | :--- | :--- |
| 1 | Ngân hàng giả | `VCB Di9ibank: Tk ban bi kh0a... Dang nhap: vcb.vip` | Cấp 1 |
| 1 | BHXH lừa đảo | `Theo NQ-116, ban du dieu kien nhan ho tro... www.pwmgh.icu` | Cấp 2 |
| 0 | OTP Ngân hàng | `Ma OTP la 123456. Vui long khong chia se cho bat ky ai.` | Cấp 0 |
| 0 | Vận chuyển | `Đơn hàng #XYZ đã được bàn giao cho đơn vị vận chuyển.` | Cấp 1 |

---

## 6. Quy trình thực thi và Kiểm soát chất lượng

### 6.1 Quy trình Pipeline
1. **Khởi tạo:** Kiểm tra tập dữ liệu hiện có để loại bỏ trùng lặp.
2. **Tạo sinh:** LLM sinh dữ liệu dựa trên sự kết hợp ngẫu nhiên các tham số (brand x category x level).
3. **Hậu kiểm tự động (Hard Validation):**
   * Xác minh định dạng cột và nhãn.
   * Kiểm tra tính nhất quán của URL/Số điện thoại bằng Regex.
   * Loại bỏ các tên miền lừa đảo (fake TLDs) khỏi tập Nhãn 0.

### 6.2 Tiêu chí đánh giá chất lượng
* **Tính trung thực (Fidelity):** Mẫu tổng hợp phản ánh đúng phong cách tin nhắn thực tế tại Việt Nam.
* **Tính đa dạng (Diversity):** Đảm bảo phủ đủ 8 danh mục và các cấp độ trong Taxonomy.
* **Tính mới (Novelty):** Nội dung không được sao chép nguyên bản từ tập Ground Truth.

---

## 7. Kết luận và Hướng phát triển

Nghiên cứu đã thiết lập thành công quy trình tạo sinh dữ liệu có kiểm soát thông qua hệ thống phân tầng đặc trưng chuyên sâu. Kết quả là bộ dữ liệu ViSmishDS được cân bằng về quy mô, sẵn sàng cho việc huấn luyện các mô hình học máy.

**Hướng phát triển:**
* Điều chỉnh trọng số tạo sinh để bổ sung các lĩnh vực còn thiếu hụt (Vận chuyển, Y tế).
* Sử dụng độ đo tương tự Cosine (Cosine Similarity) để đánh giá định lượng tính đa dạng của dữ liệu.

---
[1] Mishra, S., & Soni, D. (2023). DSmishSMS — A System to Detect Smishing SMS.
[6] Sohn, D., Lee, J., & Rim, H. (2009). The Contribution of Stylistic Information to Content-Based Mobile Spam Filtering.