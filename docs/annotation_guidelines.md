# Annotation guideline v2

Phiên bản: `2.0.0-draft`

## Nguyên tắc chung

Chỉ gán thuộc tính có bằng chứng trong nội dung. Không suy diễn nhân khẩu học
từ stereotype. Nếu không đủ bằng chứng, dùng `unknown`; nếu thông điệp hướng
đến mọi người, dùng `general` hoặc `all`.

Mỗi mẫu được gán độc lập với `label`, `data_origin`, category cũ và
obfuscation level cũ. Các trường cũ chỉ phục vụ truy vết.

## Message domain

`message_domain` mô tả chủ đề, không mô tả thật/giả. Ví dụ tin ngân hàng hợp
lệ và tin giả mạo ngân hàng đều là `banking_finance`.

Nếu có nhiều domain, chọn domain điều khiển hành động chính mà tin nhắn yêu
cầu. Dùng `other` khi nội dung rõ nhưng ngoài taxonomy; dùng `unknown` khi
không xác định được.

## Target audience

- `age_groups`: chỉ gán nhóm tuổi khi có dấu hiệu như học sinh, sinh viên,
  người nghỉ hưu, người cao tuổi. Không suy tuổi chỉ từ tuyển dụng hoặc trợ cấp.
- `gender`: chỉ gán khi nội dung gọi đích danh giới hoặc dịch vụ mang tính
  giới rõ ràng.
- `occupations`: giữ cụm nghề nghiệp ngắn, chuẩn hóa chữ thường.
- `life_statuses`: ví dụ `student`, `job_seeker`, `retired`, `debtor`,
  `bank_customer`.
- `evidence`: chép đúng cụm từ ngắn làm căn cứ. Không có bằng chứng thì để
  mảng rỗng và chọn `unknown`.

## Text phenomena và noise

`text_phenomena` mô tả hiện tượng bề mặt, áp dụng giống nhau cho cả hai nhãn.
Viết tắt, teencode hoặc lỗi chính tả tự nhiên không mặc nhiên là che giấu.

`text_noise_score`:

- 0: văn bản chuẩn hoặc gần chuẩn;
- 1: ít hiện tượng, không cản trở đọc;
- 2: nhiều hiện tượng nhưng đọc trực tiếp được;
- 3: cần suy luận/khôi phục một phần đáng kể;
- 4: rất khó đọc hoặc nhiều đoạn không giải mã chắc chắn.

## Obfuscation

Obfuscation yêu cầu có dấu hiệu biến đổi nhằm né lọc, che từ khóa hoặc làm khó
nhận diện. Một mẫu có thể có nhiều `techniques`.

Severity:

- 0: không có;
- 1: cục bộ, ý nghĩa không bị ảnh hưởng;
- 2: lặp lại trên nhiều từ nhưng vẫn dễ đọc;
- 3: ảnh hưởng đáng kể đến khả năng đọc;
- 4: cực đoan, chỉ giải mã được nhờ ngữ cảnh.

Khi không chắc đó là chủ ý hay lỗi tự nhiên, đặt `present=false` và giảm
annotation confidence; không dùng severity để thay cho uncertainty.

## Persuasion tactics

Đây là multi-label. Chỉ chọn tactic xuất hiện:

- `impersonation`: tự nhận là cá nhân/tổ chức khác;
- `urgency`: tạo deadline hoặc yêu cầu hành động ngay;
- `fear`: gây lo sợ thiệt hại;
- `authority`: viện dẫn quyền lực/cơ quan/quy định;
- `reward_greed`: hứa thưởng, lợi nhuận hoặc lợi ích bất thường;
- `threat`: đe dọa trực tiếp;
- `credential_request`: yêu cầu mật khẩu, OTP hoặc xác thực;
- `payment_request`: yêu cầu chuyển/nạp tiền;
- `link_lure`: dẫn dụ bấm link;
- `off_platform_contact`: kéo sang Zalo, Telegram hoặc kênh khác.

## Quality gate

Pilot phải có ít nhất hai annotator độc lập trên một tập giao nhau. Không chạy
full annotation trước khi:

- guideline xử lý được các ca bất đồng phổ biến;
- Cohen's Kappa đạt tối thiểu 0,70 cho trường đơn nhãn cốt lõi;
- agreement theo từng nhãn đạt mức chấp nhận được cho trường multi-label;
- tỷ lệ `unknown` được báo cáo, không bị ép giảm bằng suy diễn.
