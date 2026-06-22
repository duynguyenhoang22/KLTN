# Checklist human review P0.2

Taxonomy: `2.1.0-locked`

Hai thành viên review độc lập trước, sau đó hệ thống tạo danh sách bất đồng để
họp chốt. Không yêu cầu viết ví dụ/phản ví dụ trong review độc lập.

Với từng value, ghi `accept`, `rename`, `merge`, `split` hoặc `remove`.
Nếu khác `accept`, điền đề xuất và lý do ngắn.

## A. Message domain

- [ ] `commerce` và `logistics` cần tách riêng.
- [ ] `marketing_promotion` cần tồn tại như miền trung lập.
- [ ] Bảo hiểm nằm trong `banking_finance` có hợp lý.
- [ ] `personal_social` bao phủ OTP cá nhân và hội thoại thông thường.
- [ ] `gambling`/`adult_service` vẫn cần trong taxonomy dù nhiều mẫu có thể bị
  out of scope.
- [ ] `other` và `unknown` có ranh giới rõ.

## B. Sender type

- [x] Chỉ giữ sender type legacy human-verified cho real data.
- [x] Real chỉ dùng `brandname`, `shortcode`, `personal_number`.
- [x] Synthetic và external dùng `not_applicable`.
- [x] Không gán sender type từ content trong metadata pilot.
- [x] Không sử dụng sender type do generator tạo.

## C. Text phenomena và obfuscation

- [x] Mọi phenomenon được nhóm chấp nhận đã có trong danh sách.
- [x] Leetspeak và homoglyph gộp vào `character_substitution`.
- [x] `token_splitting` đổi thành `whitespace_splitting`.
- [x] `token_joining` đổi thành `word_concatenation`.
- [x] Không cần `mixed_technique` vì đã multi-label.
- [x] Noise score và obfuscation severity là hai trục khác nhau.

## D. Target audience

- [x] `child` bị loại và `young_adult` gộp vào `adult`.
- [x] Không suy tuổi từ `student`, `retired_person` nếu content không nêu tuổi.
- [x] Employee/worker được gộp thành `employee_or_worker`.
- [x] Account holder và shopper được gộp vào `customer`.
- [x] Taxpayer và benefit recipient được gộp vào `general_public`.
- [x] Mọi target cụ thể bắt buộc evidence.

## E. Tactics và actions

- [ ] `reward_incentive` trung lập hơn `reward_greed`.
- [ ] `social_proof` và `scarcity` có giá trị phân tích.
- [ ] Tactic có thể xuất hiện ở cả hai label.
- [ ] Requested actions bao phủ các hành động trong dữ liệu.
- [ ] Phân biệt `transfer_money`, `make_payment`, `deposit_or_top_up`.
- [ ] `none` và `unclear` không được trộn với action cụ thể.

## F. Quyết định khóa

- [ ] Không có value nào trực tiếp tiết lộ label.
- [ ] Data dictionary có định nghĩa và phản ví dụ.
- [ ] Hai người đồng ý toàn bộ thay đổi.
- [ ] Taxonomy/schema/validator cùng version.
- [x] Adjudication hoàn tất và taxonomy đã khóa `2.1.0-locked`.

Không bắt đầu metadata pilot 400 mẫu trước khi mục F hoàn thành.
