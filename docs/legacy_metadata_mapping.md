# Mapping metadata legacy → taxonomy v2

Tài liệu này chỉ dùng để audit coverage và migration planning. Mapping legacy
không được hiển thị cho annotator và không được tự động xem là ground truth.

| Legacy category | Candidate `message_domain` |
|---|---|
| Ngân hàng thật / Giả mạo ngân hàng | `banking_finance` |
| Dịch vụ công thật / Dịch vụ công giả / BHXH | `public_service` |
| Viễn thông | `telecom` |
| Thương mại điện tử | `commerce` |
| Vận chuyển | `logistics` |
| Quảng cáo hợp lệ | `marketing_promotion` hoặc miền chuyên biệt theo content |
| Tuyển dụng giả | `employment` |
| Đầu tư/Crypto giả | `investment` |
| Đòi nợ/Đe dọa | `debt_collection` |
| Cờ bạc/Betting | `gambling` |
| Nội dung nhạy cảm | `adult_service` nếu content phù hợp |
| Y tế | `healthcare` |
| Cá nhân & OTP | `personal_social` hoặc miền dịch vụ theo content |
| Khác | phải gán lại từ content |

Không có mapping legacy → obfuscation v2. Level cũ trộn kỹ thuật, severity và
thiết kế prompt nên chỉ được dùng để lấy mẫu audit.

Sender type là ngoại lệ:

- sender type legacy của real data được giữ nguyên vì đã human-verified;
- sender type synthetic không được migration;
- external và synthetic dùng `not_applicable`;
- annotator không gán lại sender type từ content.
