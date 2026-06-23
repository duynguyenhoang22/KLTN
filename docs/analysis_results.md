# Báo cáo Phân tích Dữ liệu Chuyên sâu ViSmishDS v2

Báo cáo này trình bày kết quả phân tích chuyên sâu trên tập dữ liệu **ViSmishDS v2** (gồm 5320 tin nhắn thường và 5242 tin nhắn lừa đảo) sử dụng các lát cắt chiến dịch, các phép kiểm định thống kê và trực quan hóa dữ liệu.

---

## Lát cắt 1: Message Domain vs Persuasion Tactics
Mối quan hệ giữa loại hình lừa đảo và chiến thuật tâm lý được thể hiện qua tỷ lệ phân bố của các tactics trong từng domain.

* **Phát hiện quan trọng**:
  * **Banking/Finance (Tài chính - Ngân hàng)**: Sử dụng nhiều nhất các chiến thuật `urgency` (38.0%), `link_lure` (28,4%) và `fear` (18,9%).
  * **Employment (Việc làm)**: Đặc trưng bởi chiến thuật `reward_incentive` (45,3%) nhằm dụ dỗ nạn nhân tham gia với hứa hẹn "việc nhẹ lương cao", "ăn hoa hồng", xếp sau đó là `off_platform_contact` (27,5%) khi chúng thường xuyên để lại thông tin liên lạc qua các nền tảng khác như Zalo, Telegram.
  * **Public Service (Dịch vụ công)**: Lạm dụng chiến thuật `authority` (25,1%) nhằm giả danh cơ quan nhà nước, cơ quan thuế, công an; kết hợp với `urgency` (33,4%) - yêu cầu cập nhật định danh điện tử, quyết định phạt nguội khẩn cấp.

* **Kiểm định Thống kê (Chi-square Test)**:
  * Chi2 value: 13908.27
  * p-value: 0.0 (Xấp xỉ bằng 0 do hiện tượng tràn số dưới (floating-point underflow) khi độ lệch quan sát vượt quá 783 độ lệch chuẩn so với giá trị trung bình kỳ vọng của giả thuyết H0).
  * Degrees of freedom (dof): 154

* **Biểu đồ trực quan**:
  ![Domain vs Tactics Heatmap](docs\analysis_png\domain_action_heatmap.png)

---

## Lát cắt 2: Requested Actions vs Message Domain
Lát cắt này chỉ ra hành động cụ thể mà kẻ tấn công muốn nạn nhân thực hiện.

* **Phát hiện quan trọng**:
  * **Click Link (`click_or_visit_link`)**: Là yêu cầu phổ biến nhất trong hầu hết các domain, đặc biệt là các domain `banking_finance`, `healthcare` và `public_service` với tỉ lệ > 70%.
  -> Phân tích tiếp lát cắt sâu hơn khi lấy 3 domain này ra phân tích chuyên biệt theo 3 cột là domain_message, label và requested_actions = "click_or_visit_link".
  * **Chuyển kênh giao tiếp (`contact_off_platform`)**: Chiếm tỷ lệ cao trong các domain `adult_service`, `employment` và `personal_social`. Kẻ lừa đảo hướng nạn nhân kết bạn Zalo hoặc Telegram để tiếp tục các kịch bản lừa đảo phức tạp hơn mà không bị hệ thống viễn thông quét SMS.

* **Kiểm định Thống kê (Chi-square Test)**:
  * Chi2 value: 8496.25
  * p-value: 0.0 (Xấp xỉ bằng 0 do hiện tượng tràn số dưới khi độ lệch quan sát vượt quá 435 độ lệch chuẩn so với giá trị trung bình kỳ vọng của giả thuyết H0).
  * Degrees of freedom (dof): 182

* **Biểu đồ trực quan**:
  ![Domain vs Actions Heatmap](docs\analysis_png\domain_action_heatmap.png)

---

## Lát cắt 3: Bản đồ Đối tượng Mục tiêu (Target Audience)
* **Đối tượng theo vai trò (Roles)**:
  * Vai trò cụ thể bị nhắm tới nhiều nhất là `customer` (khách hàng sử dụng dịch vụ tài chính, viễn thông) và `job_seeker` (người tìm việc - nhắm vào sinh viên và người có thu nhập thấp).
  * Bản đồ phân bố vai trò cụ thể qua các domain cho thấy kịch bản được thiết kế khớp với nhóm nạn nhân (ví dụ: `job_seeker` luôn đi kèm domain `employment`).

Bảng dưới đây thống kê số lượng tin nhắn Smishing cụ thể nhắm vào một số nhóm đối tượng điển hình:

| Vai trò đối tượng (Target Role) | Lĩnh vực tin nhắn (Message Domain) | Số lượng tin Smishing |
|---|---|---:|
| **job_seeker** (Người tìm việc) | `employment` (Việc làm) | 856 |
| **customer** (Khách hàng) | `banking_finance` (Tài chính - Ngân hàng) | 606 |
| | `public_service` (Dịch vụ công) | 564 |
| **debtor** (Con nợ) | `debt_collection` (Đòi nợ) | 453 |
| **investor** (Nhà đầu tư) | `investment` (Đầu tư) | 401 |


* **Biểu đồ trực quan**:
  ![Target Roles by Domain](docs\analysis_png\target_roles_by_domain.png)

---

## Lát cắt 4: Chiến thuật Che giấu (Obfuscation: Real vs. Synthetic)
So sánh mức độ nghiêm trọng và kỹ thuật làm nhiễu chữ giữa tin nhắn Smishing thật (`real`) và tin nhắn sinh tự động (`synthetic`).

* **Thống kê mô tả**:
  * **Real Smishing**: Tỷ lệ tin nhắn có obfuscation đạt 35.4%, mức độ nghiêm trọng trung bình (`severity`) là 0.89/4.
  * **Synthetic Smishing**: Tỷ lệ tin nhắn có obfuscation đạt 10.2%, mức độ nghiêm trọng trung bình là 0.21/4.

* **Kiểm định Thống kê (Mann-Whitney U Test trên severity)**:
  * U statistic: 774436.00
  * p-value: 0.0000
  * *Kết luận*: Mặc dù tỷ lệ làm nhiễu ở dữ liệu thật cao hơn (do dữ liệu thật thu thập qua các chiến dịch thực tế khốc liệt), phân phối mức độ nghiêm trọng và các kỹ thuật áp dụng vẫn cho thấy sự đồng dạng cao. AI đã mô phỏng thành công cách thức tin tặc chèn ký tự làm nhiễu.

* **Biểu đồ trực quan**:
  ![Obfuscation Techniques Comparison](docs\analysis_png\obfuscation_techniques_comparison.png)

---

## Lát cắt 5: Lạm dụng Đầu số gửi tin (Sender Type)
Đầu số gửi tin là yếu tố quan trọng trong việc phân phối tin nhắn và đánh lừa lòng tin nạn nhân.

* **Phát hiện quan trọng**:
  * **Brandname**: Mặc dù đầu số gửi tin thương hiệu được quản lý chặt chẽ, vẫn ghi nhận tỷ lệ nhỏ lọt tin nhắn lừa đảo hoặc nhầm lẫn (SMS OTP Brandname Hijacking). Tuy nhiên, hầu hết tin nhắn Smishing vẫn được phân phối qua các số cá nhân (`personal_number`).
  * **Benign**: Tin nhắn thương hiệu chiếm tỷ lệ lớn ở nhóm tin nhắn thường (`label=0`), chứng minh hiệu quả phân phối quảng cáo chính thống của doanh nghiệp.

* **Biểu đồ trực quan**:
  ![Sender Type by Label](docs\analysis_png\sender_type_by_label.png)

---

## Phân tích Sâu: Click Link trong 4 Domain Phổ biến
Để hiểu rõ hơn về hành vi phát tán liên kết, chúng tôi cô lập hành động `click_or_visit_link` trên 4 domain chủ đề có tỷ lệ chứa link cao nhất trong tập dữ liệu lừa đảo: **Banking/Finance**, **Healthcare**, **Public Service** và **Gambling** qua 3 biến số: `message_domain`, `label` và `sender_type`.

### 1. Số lượng phân bổ Tin nhắn chứa Link
Bảng dưới đây thống kê số lượng tin nhắn chứa liên kết phân theo nhãn và domain:

| Message Domain | Benign containing Link | Smishing containing Link | Tỷ lệ Smishing trong tin chứa Link |
|---|---:|---:|---:|
| **Banking/Finance** | 119 | 500 | 80.8% |
| **Healthcare** | 18 | 19 | 51.4% |
| **Public Service** | 114 | 893 | 88.7% |
| **Gambling** | 2 | 603 | 99.7% |

**Lưu ý**: nếu có được thắc mắc về lý do benign lại có 2 dữ liệu thuộc lớp gambling -> Phần notes ở cuối markdown có sample_id,content và diễn giải về 2 trường hợp này. Diễn giải ngắn gọn: *tin nhắn legit quảng cáo dịch vụ trò chơi/quà tặng của nhà mạng viễn thông, nhưng do đặc thù ngôn từ chứa các từ khóa kích thích ("đua top", "chơi game", "cơ hội nhận quà") nên đã bị mô hình LLM xếp nhầm vào lĩnh vực `gambling`.*

* **Nhận xét**:
  * Cả 4 domain này đều ghi nhận tỷ lệ liên kết độc hại cực lớn trong tổng số tin nhắn chứa link. Đặc biệt là **Gambling** (Cá cược trực tuyến) với **99.7%** là Smishing (603 tin nhắn chứa link lừa đảo độc hại trên tổng số 605 tin). 
  * Sự bổ sung của chủ đề **Gambling** và **Healthcare** làm nổi bật hai thái cực: một nhóm có số lượng mẫu rất lớn (`gambling` với 605 tin chứa link) và một nhóm có mẫu nhỏ hơn (`healthcare` với 37 tin chứa link) nhưng cả hai đều thể hiện tỷ lệ tập trung liên kết độc hại ở mức cao (> 50% trong tổng số tin nhắn chứa link).

![Deep Click Domain Label](docs\analysis_png\deep_click_domain_label.png)

### 2. Sự phân bố Đầu số gửi tin (Sender Type)
Sự phân hóa về đầu số gửi tin của tin nhắn chứa link thể hiện lòng tin của người dùng được khai thác thế nào:

| Domain | Label | Brandname | Shortcode | Personal Number | Not Applicable |
|---|---|---:|---:|---:|---:|
| **Banking/Finance** | Benign | 52 | 4 | 1 | 62 |
| | Smishing | 40 | 0 | 21 | 439 |
| **Healthcare** | Benign | 2 | 0 | 0 | 16 |
| | Smishing | 0 | 0 | 0 | 19 |
| **Public Service** | Benign | 45 | 3 | 1 | 65 |
| | Smishing | 4 | 1 | 8 | 880 |
| **Gambling** | Benign | 2 | 0 | 0 | 0 |
| | Smishing | 1 | 1 | 27 | 574 |

* **Nhận xét**:
  * Các tin nhắn Benign có chứa link phần lớn được gửi qua đầu số chính thức thương hiệu (`brandname`) hoặc số ngắn (`shortcode`), tạo độ tin cậy cao.
  * Đối với tin nhắn lừa đảo (Smishing), đầu số cá nhân (`personal_number`) và `not_applicable` (tức dữ liệu tạo sinh) chiếm đại đa số. Đặc biệt đáng báo động là có **40 tin nhắn lừa đảo tài chính/ngân hàng** và **4 tin nhắn lừa đảo dịch vụ công** lách qua đầu số thương hiệu (`brandname`), tạo lòng tin giả vô cùng nguy hiểm.

![Deep Click Sender Distribution](docs\analysis_png\deep_click_sender_distribution.png)

### 3. Tỷ lệ Obfuscation (Nhiễu chữ)
Mức độ che giấu/lách bộ lọc của tin nhắn lừa đảo chứa link rất cao:
* **Banking/Finance**: Tỷ lệ obfuscation của tin lừa đảo là **22.4%** (so với **1.7%** của tin thường).
* **Healthcare**: Tỷ lệ obfuscation của tin lừa đảo là **21.1%** (so với **0.0%** ở tin thường).
* **Public Service**: Tỷ lệ obfuscation của tin lừa đảo là **8.6%** (so với **0.9%** ở tin thường).
* **Gambling**: Tỷ lệ obfuscation của tin lừa đảo là **31.0%** (so với **0.0%** ở tin thường).

* **Phân tích hành vi**: Tỷ lệ làm nhiễu chữ cực cao ở nhóm tin lừa đảo lĩnh vực Cờ bạc (**31.0%**), Tài chính/Ngân hàng (**22.4%**) và Y tế (**21.1%**) phản ánh sự giám sát gắt gao của nhà mạng đối với các lĩnh vực nhạy cảm này, buộc tin tặc phải sử dụng các kỹ thuật biến đổi ký tự để lách bộ lọc từ khóa. Ngược lại, lĩnh vực Dịch vụ công (**8.6%**) có tỷ lệ nhiễu thấp hơn nhiều, cho thấy kịch bản ở các lĩnh vực này thường sử dụng từ ngữ thông thường để tăng tính thuyết phục, giả mạo văn phong hành chính, khiến tin tặc không cần che giấu quá phức tạp để đạt được mục tiêu điều hướng.

Báo cáo này cung cấp cái nhìn toàn diện và có cơ sở khoa học (qua các phép kiểm định) để đưa trực tiếp vào **Chương 5 (Kết quả và Thảo luận)** của luận văn tốt nghiệp.

---

## Phụ lục: Các trường hợp đặc biệt (Benign Gambling chứa Link)
Trong tập dữ liệu, ghi nhận 2 trường hợp cá biệt thuộc chủ đề `gambling` có chứa liên kết nhưng mang nhãn chính thống (`Benign`):

1. **Bản ghi `ViSmish_05656`**:
   * *Nội dung*: `[QC] Tham gia ngay chương trình Chiến binh đua top Cúp TV360 tại https://tv360.vn/game/st để có cơ hội nhận các phần quà hấp dẫn: Điện thoại iPhone 17 Promax, Airpods, iPad Air M3… Chi tiết LH 18008119 (0đ). Từ chối QC, soạn TC4 gửi 199.`
   * *Phân tích lý do*: Đây là chương trình quay số/đua top nhận thưởng chính thức từ cổng truyền hình TV360 của Viettel. Do chứa cụm từ "đua top" và đường dẫn chứa từ khóa "game", mô hình LLM đã phân loại nhầm chủ đề thành `gambling`. Tuy nhiên, vì đây là tin nhắn quảng cáo được đăng ký chính thống (có cú pháp từ chối QC gửi 199), nhãn thực tế của nó là `Benign`.

2. **Bản ghi `ViSmish_06859`**:
   * *Nội dung*: `Choi Game khong can cai dat. MIEN PHI den 7 ngay tu Vietnamobile. Soan ngay YB gui 5657. Phi dv sau KM: 4.000d/ngay va tu dong gia han. De soan tin nhan nhanh bam: https://tinyurl.com/5n7zehv7. CTLH 0922789789 (0d)`
   * *Phân tích lý do*: Tin nhắn quảng cáo dịch vụ trò chơi trực tuyến (VAS) chính thức từ nhà mạng Vietnamobile. Từ khóa "Choi Game" khiến mô hình phân loại tin nhắn vào chủ đề `gambling`. Dù vậy, do được gửi từ hạ tầng chính thống và có thông tin liên hệ hỗ trợ rõ ràng, tin nhắn được gán nhãn chính xác là `Benign`.
