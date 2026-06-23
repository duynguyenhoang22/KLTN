# Báo cáo liên gán nhãn (Inter-Annotator Agreement) Pilot 100 mẫu

- **Tổng số mẫu pilot:** 100
- **Số mẫu cần đối chiếu và giải quyết bất đồng (Adjudication Queue):** 68

## 1. So sánh tổng quan (Overall Metrics)
| Trường thông tin | Đo lường | A vs B (Human-Human) | A vs Mistral | B vs Mistral |
|---|---|---|---|---|
| `message_domain` | Cohen's Kappa (Exact Match) | **0.627** (66.0%) | 0.659 (69.0%) | 0.454 (50.0%) |
| `obfuscation_present` | Cohen's Kappa (Exact Match) | **0.827** (95.0%) | 0.675 (91.0%) | 0.608 (90.0%) |
| `target_gender` | Cohen's Kappa (Exact Match) | **0.463** (78.0%) | 0.318 (72.0%) | 0.494 (88.0%) |
| `text_noise_score` | Khớp chính xác (MAE) | **45.0%** (0.57) | 42.0% (0.69) | 49.0% (0.72) |
| `obfuscation_severity` | Khớp chính xác (MAE) | **84.0%** (0.24) | 82.0% (0.28) | 81.0% (0.36) |
| `text_phenomena` | Độ tương đồng Jaccard | **64.6%** | 21.2% | 17.2% |
| `target_age_groups` | Độ tương đồng Jaccard | **60.0%** | 64.0% | 77.5% |
| `target_roles` | Độ tương đồng Jaccard | **44.0%** | 67.0% | 43.0% |
| `persuasion_tactics` | Độ tương đồng Jaccard | **52.1%** | 34.9% | 28.9% |
| `requested_actions` | Độ tương đồng Jaccard | **62.1%** | 63.2% | 56.3% |

## 2. Nhận xét quan trọng
- **Độ đồng thuận miền tin nhắn (Human-Human `message_domain`):** Chỉ đạt **0.627** (Thấp hơn ngưỡng 0.70). Điều này cho thấy tài liệu hướng dẫn gán nhãn cần được bổ sung thêm quy định cụ thể cho các ca ranh giới.
- **Sự che giấu văn bản (`obfuscation_present`):** Hai annotator đạt độ tương đồng rất cao (**95.0%**), tuy nhiên mức độ đồng thuận với Mistral (A vs Mistral: 0.675, B vs Mistral: 0.608) thấp hơn rõ rệt. Điều này khẳng định Mistral đang bỏ sót nhiều trường hợp che giấu văn bản tinh vi mà cả 2 annotator đều nhận diện được.
- **Tactics & Phenomena:** Độ tương đồng Jaccard của `persuasion_tactics` giữa 2 annotator chỉ đạt **52.1%** và `text_phenomena` đạt **64.6%**. Đây là điểm yếu phổ biến trong gán nhãn đa nhãn; cần thống nhất lại danh sách tactic và hiện tượng văn bản trong buổi Adjudication.

## 3. Danh sách bất đồng tiêu biểu giữa Reviewer A và Reviewer B (Trích 15 mẫu)

**1. Mã mẫu: `phase1_00109`**
- **Nội dung:** `[TB] CHỈ 5K, CÓ DATA SIÊU TỐC! Soạn ST5K gửi 191: Chỉ 5.000đ/ngày có ngay 500MB tốc độ cao sử dụng đến 24h. Gói cước gia hạn hàng ngày. ĐẶC BIỆT: TẶNG THÊM 500MB khi mua lần thứ 2 trong ngày. LH 198 (0đ).`
- **Loại bất đồng:** `message_domain|requested_actions`
  - **message_domain:** Reviewer A: `telecom` | Reviewer B: `marketing_promotion` | Mistral: `telecom`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `reply_message|call_phone` | Reviewer B: `none` | Mistral: `reply_message|call_phone`

**2. Mã mẫu: `phase1_00132`**
- **Nội dung:** `(QC) MKTAMDUC gui tang khach hang Uu Dai Sinh Nhat trong thang 2 ma "SN02" giam gia -49% 01 san pham Gong, Kinh mat.  CT: https://mktd.vn/sinhnhat .HSD 28/02. De tu choi QC, Soan TC MKTAMDUC gui 1313`
- **Loại bất đồng:** `message_domain|requested_actions`
  - **message_domain:** Reviewer A: `commerce` | Reviewer B: `marketing_promotion` | Mistral: `commerce`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `click_or_visit_link|reply_message` | Reviewer B: `click_or_visit_link` | Mistral: `click_or_visit_link|reply_message`

**3. Mã mẫu: `phase1_00709`**
- **Nội dung:** `The Visa 452404...6779 su dung tai 2C2*AMAZON PRIME VIDEO VN6717 2333 SG so tien 13,608 VND luc 17-12-2022 17:37:45. SD TK trich no tam tinh 1033311702: 486,392VND`
- **Loại bất đồng:** `message_domain|requested_actions`
  - **message_domain:** Reviewer A: `banking_finance` | Reviewer B: `other` | Mistral: `banking_finance`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `none` | Reviewer B: `other` | Mistral: `none`

**4. Mã mẫu: `phase1_00718`**
- **Nội dung:** `Ok e .Đem luôn ao sưa dum c nha`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `none` | Reviewer B: `visit_physical_location` | Mistral: `none`

**5. Mã mẫu: `phase1_00825`**
- **Nội dung:** `[TB] Soan F70 gui 191: 70.000d/30 ngay co 3GB, mien phi 10p/cuoc noi mang, 20p ngoai mang. Goi cuoc gia han sau 30 ngay. CT ap dung den 14/09. LH 198 (0d).`
- **Loại bất đồng:** `message_domain|requested_actions`
  - **message_domain:** Reviewer A: `telecom` | Reviewer B: `marketing_promotion` | Mistral: `telecom`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `reply_message` | Reviewer B: `make_payment` | Mistral: `reply_message|call_phone`

**6. Mã mẫu: `phase1_01146`**
- **Nội dung:** `[QC] Quy khach co 5700 diem tieu dung Viettel++ tinh den het ngay 02/08/2020. Bam goi *098# hoac truy cap ung dung MyViettel tai https://viettel.vn/app (muc Viettel++) de doi diem thanh Data, phut goi, SMS hoac cac uu dai gia tri khac. LH 198 (0d). Tu choi QC, soan HUY gui 9000.`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `call_phone|click_or_visit_link|reply_message` | Reviewer B: `click_or_visit_link` | Mistral: `click_or_visit_link|call_phone|reply_message`

**7. Mã mẫu: `phase1_01191`**
- **Nội dung:** `(TB) TẶNG 50% TRÊN APP MYVNPT! VinaPhone tặng Quý khách 50% khi nạp tiền điện thoại bằng hình thức trực tiếp DUY NHẤT trên ứng dụng My VNPT trong hôm nay 14/9/2025 tại: https://my.vnpt.com.vn/adv/napdt . Khuyến mãi được sử dụng gọi và nhắn tin trong 15 ngày. CSKH:18001091 (0đ).`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `click_or_visit_link|call_phone` | Reviewer B: `click_or_visit_link|deposit_or_top_up` | Mistral: `click_or_visit_link`

**8. Mã mẫu: `phase1_01509`**
- **Nội dung:** `(TB) Chúc mừng năm mới Giáp Thìn 2024! Người dân chủ động sắp xếp thời gian trở lại nơi làm việc và sinh sống tại các thành phố lớn, tránh tình trạng ùn tắc giao thông vào cuối dịp nghỉ lễ, tuyệt đối không điều khiển phương tiện khi đã sử dụng rượu, bia.`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `other` | Reviewer B: `none` | Mistral: `none`

**9. Mã mẫu: `phase1_01518`**
- **Nội dung:** `(TB) Để phòng ngừa cháy, nổ trong dịp Tết Nguyên Đán, Công an tỉnh khuyến cáo: Không sắp xếp hàng hóa, vật dụng gần nguồn lửa, nguồn nhiệt và lấn chiếm lối đi; Trông coi khi đun nấu, thắp hương, đốt vàng mã, cỏ rác; Tắt thiết bị điện, khóa van gas khi không sử dụng; Mở lối thoát hiểm thứ hai, chuẩn bị phương án thoát nạn và các phương tiện chữa cháy; Tham gia “Tổ liên gia an toàn PCCC”; Khi có sự cố cháy, nổ gọi ngay 114 hoặc sử dụng App “Báo cháy 114”.`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `call_phone|install_application|other` | Reviewer B: `call_phone|install_application` | Mistral: `click_or_visit_link|call_phone`

**10. Mã mẫu: `phase1_01600`**
- **Nội dung:** `(TB) Quy Khach da huy thanh cong goi MI_D7 trên app My VNPT. Thong tin chi tiet truy cap My VNPT http://onelink.to/v58hh4 hoac lien he 18001091`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `click_or_visit_link|call_phone` | Reviewer B: `click_or_visit_link` | Mistral: `click_or_visit_link|call_phone`

**11. Mã mẫu: `phase1_01719`**
- **Nội dung:** `OTP cua Quy Khach la: 20666970. Ma xac thuc giao dich tren vi co hieu luc trong vong 2 phut. QK TUYET DOI khong cung cap OTP cho nguoi khac tranh bi lua dao!`
- **Loại bất đồng:** `message_domain`
  - **message_domain:** Reviewer A: `banking_finance` | Reviewer B: `other` | Mistral: `banking_finance`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`

**12. Mã mẫu: `phase1_01772`**
- **Nội dung:** `Hưởng ứng Ngày Pháp luật nước Cộng hòa xã hội chủ nghĩa Việt Nam 09/11, toàn dân nâng cao ý thức tôn trọng, tuân theo Hiến pháp và pháp luật.`
- **Loại bất đồng:** `message_domain`
  - **message_domain:** Reviewer A: `public_service` | Reviewer B: `other` | Mistral: `public_service`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`

**13. Mã mẫu: `phase1_01928`**
- **Nội dung:** `[QC] DATA LƯỚT MẠNG CẢ NGÀY. Soạn GIC70N gửi 191: Chỉ 70K/30 ngày, có 1GB/ngày, nghe toàn bộ nội dung sách nói Mydio. DV gia hạn sau 30 ngày.  Lưu ý: CT dành riêng cho thuê bao từ 6-22 tuổi đang sử dụng gói cước GIC của Viettel. Để chuyển đổi sang gói cước GIC, soạn GIC gửi 195. LH 198 (0đ). Từ chối QC, soạn TC4 gửi 199.`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `reply_message` | Reviewer B: `make_payment` | Mistral: `reply_message|click_or_visit_link`

**14. Mã mẫu: `phase1_01954`**
- **Nội dung:** `Viettel thong bao: Quy khach da duoc lap hoa don so K25TVA2611398, ngay lap 14/09/2025, so tien 0 VND. Quy khach co the tra cuu hoa don dien tu tai http://www.vietteltelecom.vn/hdbh theo ma so bi mat 5HK2M9SZP5.`
- **Loại bất đồng:** `requested_actions`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `click_or_visit_link` | Reviewer B: `none` | Mistral: `click_or_visit_link`

**15. Mã mẫu: `phase1_02142`**
- **Nội dung:** `(TB) Chốt ngay - Quà tới tay! Quý khách nhận được tin nhắn có ngay 20% giá trị thẻ nạp trong NGÀY MAI 17/6/2025. Khuyến mại được sử dụng gọi/nhắn tin trong 15 ngày. Thêm ưu đãi hời khi nạp thẻ tại https://my.vnpt.com.vn/adv/napthe .  CSKH: 18001091 (0đ).`
- **Loại bất đồng:** `message_domain|requested_actions`
  - **message_domain:** Reviewer A: `telecom` | Reviewer B: `marketing_promotion` | Mistral: `telecom`
  - **obfuscation_present:** Reviewer A: `False` | Reviewer B: `false` | Mistral: `false`
  - **requested_actions:** Reviewer A: `click_or_visit_link|call_phone` | Reviewer B: `click_or_visit_link|deposit_or_top_up` | Mistral: `click_or_visit_link|make_payment`