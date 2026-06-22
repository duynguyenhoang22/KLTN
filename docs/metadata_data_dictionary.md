# Data dictionary — ViSmishDS metadata v2

Taxonomy: `2.1.0-locked`  
Scope: `2.0.0-locked`

## Hợp đồng trường

| Trường | Kiểu | Bắt buộc | Ý nghĩa | Không được hiểu là |
|---|---|---:|---|---|
| `message_domain` | single | Có | Chủ đề chính | Nhãn thật/giả |
| `sender_type` | single | Có | Sender legacy human-verified của real data | Metadata suy từ content hoặc generator |
| `text_phenomena` | multi | Có | Hiện tượng bề mặt | Ý định che giấu |
| `text_noise_score` | ordinal 0–4 | Có | Độ khó đọc | Obfuscation severity |
| `target_audience.age_groups` | multi | Có | Tuổi được content nhắm rõ | Tuổi “thường gặp” của domain |
| `target_audience.gender` | single | Có | Giới được gọi rõ | Giới suy từ stereotype |
| `target_audience.roles` | multi | Có | Vai trò/trạng thái được nhắm | Nghề nghiệp người nhận thật |
| `obfuscation.present` | boolean | Có | Có dấu hiệu chủ ý che giấu | Có text noise |
| `obfuscation.techniques` | multi | Có | Kỹ thuật chủ ý | Level cũ |
| `obfuscation.severity` | ordinal 0–4 | Có | Mức ảnh hưởng của che giấu | Số kỹ thuật |
| `persuasion_tactics` | multi | Có | Chiến thuật thuyết phục | Label 1 |
| `requested_actions.types` | multi | Có | Hành động được yêu cầu | Hành động người nhận thực sự làm |

## Quy tắc sentinel

| Giá trị | Khi dùng | Ví dụ |
|---|---|---|
| `unknown` | Thuộc tính có thể tồn tại nhưng thiếu bằng chứng | Tin tuyển dụng không nói nhóm tuổi |
| `other` | Xác định được nhưng taxonomy không có | Một role chuyên biệt mới |
| `not_applicable` | Thuộc tính không có ý nghĩa | Sender không được cung cấp trong input |
| `general` / `all` / `general_public` | Content hướng rõ đến số đông | “Kính gửi toàn thể khách hàng” |
| `none` | Không có requested action | Thông báo giao dịch thuần túy |
| `unclear` | Có yêu cầu nhưng không giải mã được | Nhiễu nặng, còn thấy động từ yêu cầu |

Sentinel không được trộn với giá trị cụ thể trong cùng trường.

## Chính sách sender type

- `real` → bắt buộc một trong `brandname`, `shortcode`, `personal_number`;
- `synthetic`, `external_real`, `external_curated` → `not_applicable`;
- không đưa sender type vào metadata annotation;
- không dùng sender type do generator tạo;
- không xác minh lại sender type real vì nguồn legacy đã human-verified.

## Các ranh giới cần human review

Các ranh giới dưới đây không bắt buộc phải được giải quyết hoặc viết thêm ví
dụ trong review độc lập. Nếu hai reviewer đưa ra decision khác nhau, chúng sẽ
được chuyển sang taxonomy adjudication để thảo luận.

### `commerce` và `marketing_promotion`

- `commerce`: nội dung xoay quanh giao dịch hàng hóa/dịch vụ cụ thể.
- `marketing_promotion`: quảng cáo/khuyến mãi chung, không có miền chuyên biệt.
- Khuyến mãi nhà mạng vẫn là `telecom`, không phải `marketing_promotion`.

### Quy tắc xác định `message_domain` khi nội dung được gửi từ hệ sinh thái đa dịch vụ (super-app / nhà mạng / ví điện tử)

**Nguyên tắc cốt lõi**

`message_domain` được xác định theo **dịch vụ hoặc hoạt động chính đang được truyền đạt / thúc đẩy trong nội dung**, **không theo đơn vị sở hữu ứng dụng, thương hiệu hoặc kênh gửi**.

App, ví điện tử hoặc hệ sinh thái (ví dụ: My Viettel, My VNPT, Viettel Money…) chỉ được xem là **phương tiện phân phối**, không tự động quyết định domain.

Khi phân vân, áp dụng phép thử:

> **Xóa tên app / thương hiệu khỏi tin nhắn rồi đọc lại. Nội dung còn lại đang nói về điều gì → đó là domain.**

---

### Quy tắc ưu tiên

1. Nếu nội dung nói rõ một **miền nghiệp vụ cụ thể**, chọn miền đó.
2. Chỉ dùng `marketing_promotion` khi nội dung chủ yếu là **quảng bá chung**, không thể xác định miền chuyên biệt.
3. Không gán domain theo công ty sở hữu app hoặc nơi phát sinh giao dịch.
4. Với nội dung khuyến mại, xác định domain theo **đối tượng được quảng bá hoặc hành vi được kích hoạt**, không theo chương trình khuyến mại.

---

### Ví dụ

| Nội dung chính                                             | Không chọn                               | Chọn                  |
| ---------------------------------------------------------- | ---------------------------------------- | --------------------- |
| Đăng ký gói data trên My VNPT                              | `marketing_promotion`                    | `telecom`             |
| Mua data Viettel nhận cơ hội trúng thưởng từ Viettel Money | `banking_finance`, `marketing_promotion` | `telecom`             |
| Nạp tiền / thanh toán qua VNPT Money                       | `telecom`                                | `banking_finance`     |
| Thanh toán hóa đơn điện nước bằng ví điện tử               | `marketing_promotion`                    | `banking_finance`     |
| Đăng ký bảo hiểm và bị trừ tiền qua Viettel Money          | `telecom`                                | `banking_finance`     |
| Đặt vé máy bay qua My Viettel                              | `telecom`                                | `commerce`            |
| Voucher ưu đãi chung, không gắn sản phẩm/dịch vụ cụ thể    | `telecom`, `banking_finance`             | `marketing_promotion` |

---

### Ví dụ biên

**SMS:**
“Chúc mừng bạn có cơ hội trúng thưởng từ chương trình Ngày Vàng Viettel Money cho giao dịch mua data Viettel…”

→ Domain: `telecom`

Giải thích: chương trình được tổ chức bởi Viettel Money nhưng hành vi được thúc đẩy là **mua data viễn thông**.

---

**Ghi nhớ**

> Campaign owner ≠ message domain
> Payment channel ≠ message domain
> Object being promoted ≈ message domain


### `customer`

Bao gồm shopper và account holder; chỉ dùng khi content gọi người nhận trong
vai trò khách hàng hoặc người sử dụng dịch vụ.

### `employee_or_worker`

Gộp nhân viên và người lao động vì tin nhắn ngắn thường không đủ bằng chứng để
phân biệt ổn định hai khái niệm.

### `unknown` và `not_applicable` ở target audience

- `unknown`: tin đang nói với một người/nhóm nhưng không biết nhóm nào.
- `not_applicable`: tin không thực hiện việc nhắm đối tượng, ví dụ chuỗi kỹ
  thuật không có lời gọi/người nhận.

### `reward_incentive` và `scarcity`

- `reward_incentive`: hứa lợi ích.
- `scarcity`: nhấn mạnh suất/số lượng hữu hạn.
- Có thể cùng xuất hiện.

### `payment_request`, `make_payment`, `transfer_money`

`payment_request` là tactic gây sức ép/thuyết phục về tiền; requested action mô
tả thao tác cụ thể. Một thông báo hóa đơn hợp lệ có thể có `make_payment` nhưng
không nhất thiết có tactic `payment_request` nếu chỉ thông báo trung tính.

## Bất biến validator

1. Target cụ thể phải có evidence.
2. Requested action cụ thể phải có evidence.
3. Obfuscation false → severity 0 và techniques rỗng.
4. Obfuscation true → severity > 0 và techniques không rỗng.
5. Annotation taxonomy version phải trùng taxonomy đang hoạt động.
6. Không dùng giá trị chứa “real”, “fake”, “legitimate”, “scam” trong metadata
   taxonomy ngoài trường `label`.
