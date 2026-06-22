# Sổ tay thực hành gán metadata

Taxonomy: `2.1.0-locked`  
Scope: `2.0.0-locked`  
Áp dụng cho: human metadata pilot

Tài liệu này hướng dẫn thao tác nhanh. Khi có xung đột, định nghĩa trong
`annotation_guidelines.md` và `dataset_scope.md` có ưu tiên cao hơn.

## 1. Trước khi bắt đầu

Annotator chỉ được xem:

- `sample_id`;
- `content`;
- các cột metadata cần điền.

Không xem:

- label;
- data origin;
- category/obfuscation legacy;
- output Mistral;
- file của annotator còn lại;
- thông tin tra cứu bên ngoài.

Chỉ gán điều có thể suy ra từ chính `content`.

## 2. Thứ tự gán khuyến nghị

Đi theo thứ tự này để giảm ảnh hưởng chéo:

1. Đọc toàn bộ content một lần.
2. Chọn `message_domain`.
3. Gán `text_phenomena` và `text_noise_score`.
4. Gán `requested_actions` và evidence.
5. Gán `target_audience` và evidence.
6. Gán `persuasion_tactics`.
7. Gán `obfuscation`.
8. Điền confidence và review note.

Không nhìn obfuscation trước text phenomena. Nếu làm ngược, annotator dễ xem
mọi lỗi chính tả là hành vi che giấu.

## 3. Cú pháp điền CSV

### Single-label

Ghi đúng một giá trị:

```text
telecom
```

### Multi-label

Dùng dấu `|`, không thêm khoảng trắng:

```text
urgency|fear|impersonation
```

Không lặp giá trị.

### Evidence

Nhiều evidence phân tách bằng ` || `:

```text
truy cập đường dẫn || xác thực tài khoản
```

Evidence phải là cụm từ xuất hiện trong content. Không viết diễn giải mới vào
cột evidence.

### Boolean, score và confidence

- Boolean: `true` hoặc `false`.
- Noise/severity: số nguyên `0`, `1`, `2`, `3`, `4`.
- Confidence: số từ `0` đến `1`, ví dụ `0.9`.

## 4. Decision tree tổng quát

### Bước A — Content có đọc được không?

- Đọc rõ → tiếp tục.
- Đọc được một phần đáng kể → tiếp tục, noise score 2–3.
- Hầu như không giải mã chắc chắn → noise score 4, ưu tiên
  `unknown`/`unclear`, ghi `review_notes`.

### Bước B — Nội dung chủ yếu nói về lĩnh vực nào?

Chọn domain theo hoạt động chính, không theo thương hiệu/kênh thanh toán.

Phép thử:

> Bỏ tên thương hiệu/app khỏi tin nhắn; phần còn lại đang nói về gì?

### Bước C — Người nhận được yêu cầu làm gì?

- Không có yêu cầu → `none`.
- Có hành động rõ → chọn tất cả action phù hợp và trích evidence.
- Biết có yêu cầu nhưng không giải mã được → `unclear`.

### Bước D — Content có chỉ rõ đang nói với ai?

- Có age/gender/role rõ → gán giá trị cụ thể và evidence.
- Hướng đến số đông → sentinel general/all/general_public phù hợp.
- Có người nhận nhưng không biết nhóm → `unknown`.
- Thuộc tính không có ý nghĩa → `not_applicable` nếu taxonomy cho phép.

### Bước E — Có text phenomena nào?

Chỉ mô tả biểu hiện nhìn thấy. Không suy ý định.

### Bước F — Có bằng chứng chủ ý che giấu không?

- Không → `present=false`, techniques trống, severity 0.
- Có → `present=true`, chọn kỹ thuật và severity 1–4.
- Không chắc → chọn quyết định hợp lý nhất, hạ confidence và ghi note.

## 5. Message domain

Chỉ chọn một domain.

| Domain | Dùng khi nội dung chính nói về |
|---|---|
| `banking_finance` | tài khoản, giao dịch, ví, thanh toán, bảo hiểm tài chính |
| `public_service` | thuế, BHXH, công an, thủ tục hành chính |
| `telecom` | data, gói cước, thuê bao, nạp thẻ nhà mạng |
| `commerce` | mua bán hàng hóa/dịch vụ |
| `logistics` | vận chuyển, bưu kiện, trạng thái giao hàng |
| `marketing_promotion` | quảng bá chung không có domain chuyên biệt |
| `employment` | tuyển dụng, việc làm, cộng tác viên |
| `investment` | đầu tư, crypto, forex, lợi nhuận vốn |
| `debt_collection` | khoản vay, nợ, thu hồi nợ |
| `gambling` | casino, cá cược, game bài |
| `adult_service` | dịch vụ người lớn/hẹn hò thương mại |
| `healthcare` | bệnh viện, thuốc, khám chữa bệnh |
| `personal_social` | chào hỏi, trao đổi cá nhân |
| `other` | hiểu rõ domain nhưng danh sách không bao phủ |
| `unknown` | không đủ nội dung để xác định domain |

### Commerce và logistics

- “Đơn hàng đang được giao” → `logistics`.
- “Đặt mua sản phẩm, thanh toán đơn hàng” → `commerce`.
- Tin có cả hai: chọn hoạt động được nhấn mạnh hoặc hành động chính được yêu
  cầu. Không tự động chọn logistics chỉ vì có mã vận đơn.

### Marketing promotion và domain chuyên biệt

- Khuyến mãi data → `telecom`.
- Ưu đãi thanh toán ví → `banking_finance`.
- Voucher chung, không rõ sản phẩm/dịch vụ → `marketing_promotion`.

## 6. Text phenomena

Đây là multi-label.

| Value | Định nghĩa | Ví dụ |
|---|---|---|
| `diacritic_omission` | bỏ dấu tiếng Việt | `tai khoan cua ban` |
| `abbreviation` | viết tắt | `QK`, `LH`, `CSKH` |
| `teencode` | biến thể chat | `ko`, `k`, `j`, `zậy` |
| `character_substitution` | thay ký tự, gồm leet/homoglyph | `nh4n t1en`, `ZAL0` |
| `punctuation_insertion` | chèn dấu trong từ | `V.C.B`, `n_h_ậ_n` |
| `whitespace_splitting` | tách một từ bằng khoảng trắng | `n h a n t i e n` |
| `word_concatenation` | nối nhiều từ | `dangnhapngay` |
| `irregular_spacing` | khoảng trắng bất thường | nhiều space hoặc thiếu space cục bộ |
| `irregular_casing` | hoa/thường bất thường | `nHaN ThuOnG` |
| `character_repetition` | lặp ký tự | `HOTTTT`, `ngayyyy` |
| `lang_switching` | chuyển ngôn ngữ | Việt–Anh xen kẽ |
| `natural_typo` | lỗi gõ tự nhiên | sai một ký tự không có hệ thống |

### Ranh giới quan trọng

- `nhan_tien` → `punctuation_insertion`.
- `V.C.B` → `punctuation_insertion`.
- `V C B` → `whitespace_splitting`.
- `nhantien` → `word_concatenation`.
- Một tin có thể chứa nhiều phenomenon độc lập.

### Noise score

- 0: chuẩn/gần chuẩn.
- 1: có hiện tượng nhẹ, đọc ngay.
- 2: nhiều hiện tượng nhưng ý nghĩa rõ.
- 3: phải khôi phục đáng kể.
- 4: phần lớn khó giải mã chắc chắn.

## 7. Requested actions

Đây là multi-label.

| Value | Hành động |
|---|---|
| `none` | không yêu cầu gì |
| `click_or_visit_link` | bấm/truy cập link |
| `call_phone` | gọi điện |
| `reply_message` | phản hồi/soạn tin |
| `provide_personal_information` | cung cấp OTP, mật khẩu, giấy tờ, thông tin cá nhân |
| `transfer_money` | chuyển tiền cho tài khoản/người khác |
| `make_payment` | thanh toán hóa đơn/dịch vụ |
| `deposit_or_top_up` | nạp tiền, nạp thẻ, nạp số dư |
| `install_application` | tải/cài app |
| `contact_off_platform` | liên hệ Zalo/Telegram/Facebook… |
| `register_or_sign_up` | đăng ký tài khoản/dịch vụ |
| `visit_physical_location` | đến địa điểm |
| `other` | hành động rõ nhưng ngoài danh sách |
| `unclear` | có yêu cầu nhưng không giải mã rõ |

`none` và `unclear` không đi cùng action khác.

### Phân biệt thao tác tiền

- “Chuyển 5 triệu vào STK…” → `transfer_money`.
- “Thanh toán hóa đơn trước ngày…” → `make_payment`.
- “Nạp 50k nhận thưởng…” → `deposit_or_top_up`.

## 8. Target audience

Metadata này mô tả nhóm mà **content thể hiện đang hướng đến**, không phải
demographic thật của người nhận.

### Age groups

`adolescent`, `adult`, `older_adult`, `general`, `unknown`,
`not_applicable`.

- Không suy tuổi từ `student`.
- Không suy `older_adult` chỉ từ trợ cấp/BHXH.
- `general`: nội dung rõ ràng hướng rộng đến mọi tuổi.
- `unknown`: có đối tượng nhưng không biết tuổi.

### Gender

`female`, `male`, `all`, `unknown`.

- Chỉ gán female/male khi content gọi rõ.
- Không suy giới từ gambling, adult service hoặc nghề nghiệp.

### Roles

`student`, `job_seeker`, `employee_or_worker`, `business_owner`, `customer`,
`debtor`, `investor`, `patient`, `vehicle_owner`, `retired_person`,
`general_public`, `other`, `unknown`, `not_applicable`.

Ví dụ:

- “Sinh viên năm cuối” → role `student`; không tự gán age.
- “Chủ shop” → `business_owner`.
- “Tài khoản của quý khách” → `customer`.
- “Khoản vay của ông/bà” → `debtor`.

Mọi age/gender/role cụ thể cần evidence. Sentinel không trộn với giá trị cụ
thể trong cùng trường.

## 9. Persuasion tactics

Multi-label:

- `impersonation`: tự nhận/mạo danh tổ chức/cá nhân;
- `urgency`: tạo áp lực thời gian;
- `fear`: gây sợ mất tiền/quyền lợi;
- `authority`: viện dẫn quyền lực/quy định;
- `reward_incentive`: hứa thưởng/ưu đãi;
- `social_proof`: viện dẫn nhiều người/người khác;
- `scarcity`: giới hạn suất/số lượng;
- `threat`: đe dọa trực tiếp;
- `credential_request`: yêu cầu OTP/mật khẩu/xác thực;
- `payment_request`: thúc đẩy thanh toán/chuyển/nạp tiền;
- `link_lure`: thúc đẩy truy cập link;
- `off_platform_contact`: kéo sang nền tảng khác.

Tactic có thể xuất hiện trong Label 0. Ví dụ quảng cáo hợp lệ vẫn có
`reward_incentive` và `scarcity`.

## 10. Obfuscation

### Câu hỏi quyết định

> Biến đổi này có vẻ nhằm che từ khóa/né lọc/làm khó nhận diện, hay chỉ là cách
> viết tự nhiên?

Không obfuscation:

```text
ko biet nua
```

Có teencode/noise nhưng không có dấu hiệu né lọc.

Có obfuscation:

```text
n.h.ậ.n t1ề.n, c-a-s-i-n-o
```

Biến đổi có hệ thống trên từ nhạy cảm.

### Techniques

`character_substitution`, `punctuation_insertion`, `whitespace_splitting`,
`word_concatenation`, `irregular_spacing`, `irregular_casing`,
`character_repetition`.

### Severity

- 0: không có.
- 1: cục bộ.
- 2: lặp lại nhưng dễ đọc.
- 3: ảnh hưởng đáng kể.
- 4: cực đoan/khó giải mã.

Nếu `present=false`: techniques trống, severity 0.

## 11. Ví dụ hoàn chỉnh

Content giả lập:

```text
TH0NG BA0: Tai khoan cua ban sap bi khoa. Truy cap vcb-xacminh.top ngay de xac thuc.
```

Một annotation hợp lệ:

```text
message_domain = banking_finance
text_phenomena = diacritic_omission|character_substitution
text_noise_score = 1
target_age_groups = unknown
target_gender = unknown
target_roles = customer
target_evidence = Tai khoan cua ban
obfuscation_present = true
obfuscation_techniques = character_substitution
obfuscation_severity = 1
obfuscation_confidence = 0.9
persuasion_tactics = urgency|fear|impersonation|link_lure
requested_actions = click_or_visit_link|provide_personal_information
requested_action_evidence = Truy cap || xac thuc
overall_confidence = 0.9
review_notes =
```

## 12. Khi nào dùng review note?

Ghi note khi:

- domain có hai cách hiểu gần ngang nhau;
- content khó đọc;
- không chắc biến đổi có chủ ý obfuscation;
- taxonomy không bao phủ;
- evidence cho target yếu;
- một quyết định cần adjudication.

Không dùng note để thay cho việc điền metadata bắt buộc.

## 13. Checklist trước khi nộp

- [ ] Đủ 100 dòng, không thay đổi thứ tự hoặc sample ID.
- [ ] Mọi single-label dùng đúng enum.
- [ ] Multi-label dùng `|`.
- [ ] Không có khoảng trắng quanh `|`.
- [ ] Target cụ thể có evidence.
- [ ] Requested action cụ thể có evidence.
- [ ] `none`/`unclear` không đi cùng action khác.
- [ ] Obfuscation false → techniques trống, severity 0.
- [ ] Confidence nằm trong khoảng 0–1.
- [ ] Không dùng label/category/output LLM.
