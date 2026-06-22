# Annotation guideline metadata v2

Phiên bản: `2.1.0-locked`

Phụ thuộc scope: `2.0.0-locked`

Trạng thái: taxonomy đã khóa; chờ metadata pilot

## 1. Nguyên tắc chung

- Chỉ sử dụng `content`; không xem label, data origin, category hoặc
  obfuscation legacy khi gán metadata.
- Gán điều được thể hiện, không gán điều có vẻ “thường đúng”.
- Metadata không được dùng để sửa nhãn trong vòng metadata annotation.
- Multi-label chỉ chọn các giá trị có bằng chứng.
- `unknown` là thiếu bằng chứng; `other` là có bằng chứng nhưng taxonomy chưa
  bao phủ; `not_applicable` là thuộc tính không có ý nghĩa với mẫu.
- Evidence là cụm từ ngắn trích nguyên văn từ `content`.

## 2. Message domain

Chọn một miền mô tả chủ đề chính của thông điệp, không mô tả thật/giả:

- `banking_finance`: tài khoản, giao dịch, ví điện tử, bảo hiểm/tài chính;
- `public_service`: thuế, BHXH, công an, dịch vụ hành chính;
- `telecom`: gói cước, data, nhà mạng, thuê bao;
- `commerce`: mua bán hàng hóa/dịch vụ, sàn thương mại;
- `logistics`: giao nhận, vận chuyển, bưu kiện;
- `marketing_promotion`: khuyến mãi/quảng cáo không thuộc miền chuyên biệt;
- `employment`: tuyển dụng, công việc, cộng tác viên;
- `investment`: đầu tư, chứng khoán, crypto, forex;
- `debt_collection`: khoản vay, nợ, thu hồi nợ;
- `gambling`: cá cược, casino, game bài;
- `adult_service`: dịch vụ tình dục/hẹn hò mang tính thương mại;
- `healthcare`: khám chữa bệnh, thuốc, bệnh viện;
- `personal_social`: giao tiếp cá nhân, OTP cá nhân không thuộc dịch vụ;
- `other`: nội dung rõ nhưng ngoài danh sách;
- `unknown`: nội dung không đủ để xác định.

Nếu nhiều miền xuất hiện, chọn miền điều khiển hành động chính. Ví dụ “việc
làm nhập đơn Shopee” vẫn là `employment`, không phải `commerce`.

## 3. Sender type

`sender_type` là metadata nguồn, không phải trường được annotator suy luận từ
`content`.

- Với `data_origin=real`, dùng trực tiếp sender type legacy đã được con người
  xác minh: `brandname`, `shortcode` hoặc `personal_number`.
- Với synthetic và external, luôn dùng `not_applicable`.
- Không sử dụng sender type do generator tự khai báo.
- Không gán lại hoặc sửa sender type trong metadata pilot.

Không suy sender type từ tên tổ chức, số điện thoại hoặc cách xưng hô được nhắc
trong nội dung.

## 4. Text phenomena và noise

`text_phenomena` mô tả bề mặt, áp dụng như nhau cho cả hai nhãn:

- `diacritic_omission`: bỏ dấu tiếng Việt;
- `abbreviation`: viết tắt thông dụng hoặc tự tạo;
- `teencode`: biến thể kiểu chat/teen;
- `character_substitution`: thay ký tự, gồm leetspeak và homoglyph;
- `punctuation_insertion`: chèn dấu vào giữa từ;
- `whitespace_splitting`: tách một từ thành nhiều phần bằng khoảng trắng;
- `word_concatenation`: nối các từ bằng cách bỏ khoảng trắng;
- `irregular_spacing`: khoảng trắng bất thường;
- `irregular_casing`: hoa/thường bất thường;
- `character_repetition`: lặp ký tự kéo dài;
- `lang_switching`: chuyển đổi Việt–Anh/ngôn ngữ khác;
- `natural_typo`: lỗi gõ/chính tả có vẻ tự nhiên.

`text_noise_score`:

- 0: chuẩn hoặc gần chuẩn;
- 1: có ít hiện tượng, đọc ngay không cần khôi phục;
- 2: nhiều hiện tượng nhưng ý nghĩa vẫn rõ;
- 3: phải khôi phục/suy luận đáng kể;
- 4: nhiều phần không thể giải mã chắc chắn.

Score đo độ khó đọc, không đo ý định che giấu.

## 5. Target audience

### Age group

- `adolescent`: thanh thiếu niên;
- `adult`: người trưởng thành;
- `older_adult`: người cao tuổi/nghỉ hưu khi có bằng chứng tuổi;
- `general`: hướng rộng đến mọi độ tuổi;
- `unknown`: có thể có nhóm đích nhưng không xác định;
- `not_applicable`: thông điệp không thực hiện việc nhắm đối tượng.

Không suy “sinh viên → adult”; chỉ gán `student` ở roles nếu không có bằng
chứng tuổi.

### Gender

- `female`, `male`: chỉ khi content gọi rõ;
- `all`: hướng đến mọi giới;
- `unknown`: không đủ bằng chứng hoặc không có giới đích cụ thể.

### Roles

Role là quan hệ/trạng thái mà thông điệp dùng để gọi hoặc nhắm đến người nhận:

`student`, `job_seeker`, `employee_or_worker`, `business_owner`, `customer`,
`debtor`, `investor`, `patient`, `vehicle_owner`, `retired_person`,
`general_public`, `other`, `unknown`, `not_applicable`.

Mọi age/gender/role cụ thể bắt buộc có evidence. Các sentinel
`general/unknown/not_applicable` không được trộn với giá trị cụ thể trong cùng
một trường.

## 6. Obfuscation

Obfuscation là biến đổi có dấu hiệu nhằm né lọc, che từ khóa hoặc làm khó nhận
diện. Nó khác với text noise:

- bỏ dấu/viết tắt tự nhiên có thể là noise nhưng không phải obfuscation;
- leetspeak có hệ thống trên từ nhạy cảm có thể vừa là phenomenon vừa là
  obfuscation technique.

Kỹ thuật là multi-label và dùng cùng tên tương ứng với text phenomena, trừ các
hiện tượng không biểu đạt che giấu. Leetspeak và homoglyph được biểu diễn chung
bằng `character_substitution`.

Severity:

- 0: không obfuscation;
- 1: cục bộ, không ảnh hưởng khả năng đọc;
- 2: lặp trên nhiều từ nhưng dễ khôi phục;
- 3: ảnh hưởng đáng kể;
- 4: cực đoan, nhiều phần không chắc chắn.

Bất biến:

- `present=false` → techniques rỗng, severity 0;
- `present=true` → ít nhất một technique, severity từ 1 đến 4.

Confidence biểu thị mức chắc chắn về **ý định che giấu**, không phải khả năng
đọc văn bản.

## 7. Persuasion tactics

Multi-label:

- `impersonation`: tự nhận/mạo danh cá nhân hoặc tổ chức;
- `urgency`: ép hành động trong thời gian ngắn;
- `fear`: tạo lo sợ thiệt hại;
- `authority`: viện dẫn quyền lực/quy định;
- `reward_incentive`: hứa lợi ích, thưởng hoặc ưu đãi;
- `social_proof`: dùng đám đông/người khác làm bằng chứng;
- `scarcity`: nhấn mạnh giới hạn suất/số lượng;
- `threat`: đe dọa trực tiếp;
- `credential_request`: yêu cầu OTP, mật khẩu hoặc xác thực;
- `payment_request`: yêu cầu thanh toán/chuyển/nạp tiền;
- `link_lure`: thúc đẩy truy cập liên kết;
- `off_platform_contact`: kéo sang Zalo, Telegram hoặc nền tảng khác.

Tin Label 0 vẫn có thể có urgency, reward incentive, link lure hoặc payment
request. Tactic không phải nhãn.

## 8. Requested actions

Gán hành động mà người nhận được yêu cầu thực hiện:

- `none`: không có yêu cầu hành động;
- `click_or_visit_link`;
- `call_phone`;
- `reply_message`;
- `provide_personal_information`;
- `transfer_money`;
- `make_payment`;
- `deposit_or_top_up`;
- `install_application`;
- `contact_off_platform`;
- `register_or_sign_up`;
- `visit_physical_location`;
- `other`;
- `unclear`: có yêu cầu nhưng không giải mã rõ.

Đây là multi-label. `none` và `unclear` không được trộn với hành động khác.
Mọi hành động cụ thể phải có evidence.

Phân biệt:

- `transfer_money`: chuyển tiền cho tài khoản/người nhận;
- `make_payment`: thanh toán hóa đơn/dịch vụ;
- `deposit_or_top_up`: nạp tiền/thẻ/số dư.

## 9. Annotation provenance

Mỗi record canonical phải có:

- `status`;
- annotator/model IDs;
- confidence từ 0 đến 1;
- guideline version;
- taxonomy version;
- note nếu cần.

LLM output là `auto_labeled`; chỉ con người mới chuyển thành
`human_reviewed` hoặc `adjudicated`.

## 10. Quality gate

Không chạy full annotation trước khi:

- hai người review toàn bộ data dictionary;
- metadata pilot có ít nhất hai annotator độc lập;
- Cohen's Kappa ≥ 0,70 cho `message_domain`;
- agreement multi-label được báo cáo bằng Jaccard/micro-F1;
- mọi giá trị có ví dụ và phản ví dụ đủ rõ;
- tỷ lệ `unknown`, `other`, `not_applicable` được báo cáo riêng.
