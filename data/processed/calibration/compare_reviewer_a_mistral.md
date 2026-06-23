# Báo cáo so sánh nhãn giữa Reviewer A và Mistral Small (100 mẫu pilot)

- **Tổng số mẫu chung:** 100

## 1. Tỷ lệ đồng thuận chi tiết (Agreement Rates)
| Trường thông tin | Loại so sánh | Độ đồng thuận (Exact Match hoặc Jaccard) | Chi tiết sai lệch |
|---|---|---|---|
| `message_domain` | Khớp chính xác | 69.0% | |
| `text_noise_score` | Khớp chính xác | 42.0% | Khác biệt trung bình: 0.69 |
| `obfuscation_present` | Khớp chính xác | 90.0% | |
| `obfuscation_severity` | Khớp chính xác | 82.0% | Khác biệt trung bình: 0.28 |
| `target_gender` | Khớp chính xác | 72.0% | |
| `text_phenomena` | Độ tương đồng Jaccard | 21.2% | |
| `target_age_groups` | Độ tương đồng Jaccard | 64.0% | |
| `target_roles` | Độ tương đồng Jaccard | 67.0% | |
| `persuasion_tactics` | Độ tương đồng Jaccard | 34.9% | |
| `requested_actions` | Độ tương đồng Jaccard | 63.2% | |

## 2. Chi tiết bất đồng tiêu biểu

### 2.1. Bất đồng về miền tin nhắn (`message_domain`) - 31 trường hợp

**1. Mã mẫu: `phase1_00526`**
- **Nội dung:** `TK ViettelPay 9704...1278 GD -1,000 VND luc 2023-08-11 14:13:34 So du 3,372 VND Phi: -0 VND ND: GD thanh toan 230811182319866 NAP TIEN DIEN THOAI cho Khach hang 0867256447`
- **Reviewer A:** `banking_finance`
- **Mistral:** `telecom`

**2. Mã mẫu: `phase1_01145`**
- **Nội dung:** `Bạn đã yêu cầu Google khôi phục quyền truy cập cho duyj4f2004@gmail.com? Nếu không phải thì hãy kiểm tra email để tìm hiểu cách DỪNG yêu cầu này.`
- **Reviewer A:** `other`
- **Mistral:** `public_service`

**3. Mã mẫu: `phase1_02325`**
- **Nội dung:** `Bắc, tài khoản tài chính của bạn đã được thêm vào. Tài khoản: Nay128 Mật khẩu: yk6698 USDT Số dư: 1,080,096.50 [ ehoaq. com ] Vui lòng giữ nó ở nơi an toàn.`
- **Reviewer A:** `banking_finance`
- **Mistral:** `investment`

**4. Mã mẫu: `phase1_02368`**
- **Nội dung:** `j)t.ly/Q5YuG Um Cu,u~Th,ua8% ZJ Na.pVao-LanD:au,UuDa'j:8Tr8 PJ wz8:88.Bma Gu.i_C:OT~6OKa:H'SD;2_4H[[H6MW9KD1X191> zHoa'n,Tr'a~1,4% Ge`
- **Reviewer A:** `gambling`
- **Mistral:** `unknown`

**5. Mã mẫu: `phase1_02399`**
- **Nội dung:** `E Ho Cho Cap Lai, lam Bang Lai Xe Cac Loai A,B,C,D..Cung Cap Cac Loai Giay To Khac CCCD,Bang DH,Cdang,TCap. GiaoHang va ThanhToan Tai Nha LH 0986557450 Rsmv`
- **Reviewer A:** `other`
- **Mistral:** `commerce`

**6. Mã mẫu: `phase1_02432`**
- **Nội dung:** `egeR #Ban da-du D1EU K1EN HOAN~THUE TNCN, tai:https://hoanthue-tncn.vip`
- **Reviewer A:** `public_service`
- **Mistral:** `employment`

**7. Mã mẫu: `phase1_02439`**
- **Nội dung:** `anh chị hãy chuyển số tiền cần nạp vào tài khoản này ạ, sau đó chụp lại màn hình em sẽ làm lệnh nạp vào tài khoản CSI giúp anh ạ Ngân hàng thương mại cổ phần Hàng hải Việt Nam MSB STK: 04001012266596 tên chủ TK: CÔNG TY TNHH DAU TU BAT DONG SAN SSG 10:30`
- **Reviewer A:** `investment`
- **Mistral:** `banking_finance`

**8. Mã mẫu: `phase1_02445`**
- **Nội dung:** `Hệ Thống Messenger Thông Báo: Xin chúc mừng tài khoản Messenger đã may mắn nhận được Giải Nhất từ sự kiện 'Tuần Lễ Vàng' tri ân khách hàng chào Quý 3, đón Năm Mới 2024. Bây giờ bạn vui lòng tiến hành truy cập vào trang địa chỉ website: TraoThuongQuy3.Com (viết liền nhau, không dấu) để đăng ký làm thủ tục hồ sơ nhận thưởng. Hoặc có thể truy cập công cụ tìm kiếm Google và gõ từ khóa: (TraoThuongQuy3.Com). Sau đó chọn kết quả tìm kiếm đầu tiên để truy cập trang website lãnh thưởng. Mọi thắc mắc xin liên hệ Tổng đài CSKH: [(08) 9921 4440]`
- **Reviewer A:** `other`
- **Mistral:** `marketing_promotion`

**9. Mã mẫu: `phase1_02462`**
- **Nội dung:** `KHÁCH HÀNG CHÚ Ý: Trong trường hợp Quý khách không phản hồi hoặc không yêu cầu hủy, hệ thống sẽ mặc định xác nhận sự đồng thuận tham gia gói bảo hiểm, dựa trên quy định tại Điều 38 - Luật Giao dịch điện tử năm 2005, áp dụng hình thức xác lập hợp đồng điện tử. Mọi thông tin chi tiết, phản hồi hoặc yêu cầu hỗ trợ, vui lòng liên hệ: Email: dvkh@dbvivn.com`
- **Reviewer A:** `banking_finance`
- **Mistral:** `commerce`

**10. Mã mẫu: `phase1_02493`**
- **Nội dung:** `Ben Em nhan lam cac loai gplx may,oto..chung minh thu,can cuoc,dang ki xe,bang cap 3 den dai hoc va tat ca giay to khac,LH 0877.607.954 giao hang thu tien`
- **Reviewer A:** `other`
- **Mistral:** `commerce`

**11. Mã mẫu: `phase1_02496`**
- **Nội dung:** `THE THAO THUONG 2TR3, SLOT THUONG 230K TANG 90K KHI XAC MINH TAI KHOAN NAP TIEN LAN DAU TANG NGAY 50K DKY TAI: https://t.ly/oScnl lMEtM`
- **Reviewer A:** `gambling`
- **Mistral:** `investment`

**12. Mã mẫu: `phase1_02498`**
- **Nội dung:** `taq ngay 8'8'8K khi d/ky tai:bit.ly/Frw2T5 diem danh nhan 124.3K rut lien 6Rg8`
- **Reviewer A:** `gambling`
- **Mistral:** `marketing_promotion`

**13. Mã mẫu: `phase1_02500`**
- **Nội dung:** `3Jfu Ng dung mo'i naq 1OOK V..N..D de nh@n 188k-1888k diem: bit.ly/46mkyZ2 Nhan ngay quå tåg DK n å p dau 1 7 7 K Nhän ngay 177 K Ta¡ : bit.ly/7Wi2nE NOmQ`
- **Reviewer A:** `gambling`
- **Mistral:** `investment`

**14. Mã mẫu: `phase1_02532`**
- **Nội dung:** `DvVCh:oj_Vu,jVe Ch.jenThan.g:H,OTz99N:g:in-M,ayMa'nsk<2srcfxcs.sh-n.com'KfQi`
- **Reviewer A:** `gambling`
- **Mistral:** `unknown`

**15. Mã mẫu: `phase1_02548`**
- **Nội dung:** `[Thông báo] Hội thảo trực tuyến "Không trúng tuyển nguyện vọng yêu thích? Biến nguy thành cơ" với sự tham gia của các khách mời, chuyên gia tâm lý đến từ nhiều trường đại học đang diễn ra. Để không bỏ lỡ cơ hội được tham dự, lắng nghe và đặt câu hỏi trực tiếp cho các chuyên gia, mời quý phụ huynh & thí sinh truy cập liên kết: https://us02web.zoom.us/j/81558445815. Hotline: (028) 7300 5588`
- **Reviewer A:** `other`
- **Mistral:** `employment`

### 2.2. Bất đồng về sự tồn tại của che giấu (`obfuscation_present`) - 10 trường hợp

**1. Mã mẫu: `phase1_02325`**
- **Nội dung:** `Bắc, tài khoản tài chính của bạn đã được thêm vào. Tài khoản: Nay128 Mật khẩu: yk6698 USDT Số dư: 1,080,096.50 [ ehoaq. com ] Vui lòng giữ nó ở nơi an toàn.`
- **Reviewer A:** `True`
- **Mistral:** `False`

**2. Mã mẫu: `phase1_02432`**
- **Nội dung:** `egeR #Ban da-du D1EU K1EN HOAN~THUE TNCN, tai:https://hoanthue-tncn.vip`
- **Reviewer A:** `True`
- **Mistral:** `False`

**3. Mã mẫu: `phase1_02445`**
- **Nội dung:** `Hệ Thống Messenger Thông Báo: Xin chúc mừng tài khoản Messenger đã may mắn nhận được Giải Nhất từ sự kiện 'Tuần Lễ Vàng' tri ân khách hàng chào Quý 3, đón Năm Mới 2024. Bây giờ bạn vui lòng tiến hành truy cập vào trang địa chỉ website: TraoThuongQuy3.Com (viết liền nhau, không dấu) để đăng ký làm thủ tục hồ sơ nhận thưởng. Hoặc có thể truy cập công cụ tìm kiếm Google và gõ từ khóa: (TraoThuongQuy3.Com). Sau đó chọn kết quả tìm kiếm đầu tiên để truy cập trang website lãnh thưởng. Mọi thắc mắc xin liên hệ Tổng đài CSKH: [(08) 9921 4440]`
- **Reviewer A:** `False`
- **Mistral:** `True`

**4. Mã mẫu: `phase1_02496`**
- **Nội dung:** `THE THAO THUONG 2TR3, SLOT THUONG 230K TANG 90K KHI XAC MINH TAI KHOAN NAP TIEN LAN DAU TANG NGAY 50K DKY TAI: https://t.ly/oScnl lMEtM`
- **Reviewer A:** `False`
- **Mistral:** `True`

**5. Mã mẫu: `phase1_02517`**
- **Nội dung:** `Täng 888K, 888K! 888K Nhän ngay 88K MPhi, tu: gv2xu.cc/WlhXzU ~u9pa`
- **Reviewer A:** `True`
- **Mistral:** `False`

**6. Mã mẫu: `phase1_07292`**
- **Nội dung:** `TB KHAN: Phong An ninh Dieu tra thong bao Ong Hoang Kieu Anh CMND: 272635418 vi pham hop dong tin dung voi so tien 19,453,000VND. Yeu cau thanh toan truoc 16H Ngay 30/05. Neu khong se tien hanh truy to toi chiem doat tai san. Lien he: 0944556677.`
- **Reviewer A:** `True`
- **Mistral:** `False`

**7. Mã mẫu: `phase1_08420`**
- **Nội dung:** `H;C_M-E:m;s_I_n:H_v;I_e:N:c_U_t_E. HCM – Telegram: https://t.me/hcm_cute_sv rT8p`
- **Reviewer A:** `True`
- **Mistral:** `False`

**8. Mã mẫu: `phase1_09215`**
- **Nội dung:** `Cuc Vien thong: Thue b4o cwa ban se bi thu hoi. Lien he 0345678901`
- **Reviewer A:** `True`
- **Mistral:** `False`

**9. Mã mẫu: `phase1_09361`**
- **Nội dung:** `ëM_dänG_ö_HCM_vA_rAt_cö_dOn. K-e-t b-a-n T-e-l-e: t.me/hcm_lonely_girl aS9d`
- **Reviewer A:** `True`
- **Mistral:** `False`

**10. Mã mẫu: `phase1_09636`**
- **Nội dung:** `B-o-d-y c-h-u-a-n e-m d-a-n-g o H-N Z-a-l-o k-e-t b-a-n: https://bit.ly/hn_body_chuan kI1u`
- **Reviewer A:** `True`
- **Mistral:** `False`

### 2.3. Bất đồng về Tác vụ yêu cầu / Chiến thuật thuyết phục - 97 trường hợp

**1. Mã mẫu: `phase1_00070`**
- **Nội dung:** `Mã xác thực GitHub của bạn là: 733792`
  - **Persuasion Tactics (Reviewer A):** `['none']`
  - **Persuasion Tactics (Mistral):** `[]`

**2. Mã mẫu: `phase1_00132`**
- **Nội dung:** `(QC) MKTAMDUC gui tang khach hang Uu Dai Sinh Nhat trong thang 2 ma "SN02" giam gia -49% 01 san pham Gong, Kinh mat.  CT: https://mktd.vn/sinhnhat .HSD 28/02. De tu choi QC, Soan TC MKTAMDUC gui 1313`
  - **Persuasion Tactics (Reviewer A):** `['reward_incentive', 'link_lure', 'scarcity']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`

**3. Mã mẫu: `phase1_00211`**
- **Nội dung:** `Quy khach co 14.985 dong trong tai khoan. Bam goi *098*3# de co 3GB voi 15.000d/3 ngay hoac *098*989# (30.000d/3 ngay) co 15GB (5GB/ngay), mien phi 10 phut/cuoc noi mang, 15 phut ngoai mang, SMS noi mang va TV360. Goi cuoc gia han khi het chu ky. De biet thong tin cac uu dai khac, bam goi *098# hoac truy cap My Viettel tai https://myvt.page.link/goidata . Chi tiet LH 198 (0d). Tran trong.`
  - **Persuasion Tactics (Reviewer A):** `['reward_incentive', 'link_lure']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`

**4. Mã mẫu: `phase1_00284`**
- **Nội dung:** `[TB] Mừng VIETTEL 35 năm - ra mắt gói cước với tính năng mới: Chỉ với 35.000đ/7 ngày, Quý khách có thể lựa chọn truy cập data, gọi điện theo nhu cầu, đặc biệt tặng thêm dịch vụ TV360 hoặc Mydio. Truy cập ứng dụng My Viettel tại https://viettel.vn/diy để trải nghiệm. LH 198 (0đ).`
  - **Persuasion Tactics (Reviewer A):** `['reward_incentive', 'link_lure']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`

**5. Mã mẫu: `phase1_00526`**
- **Nội dung:** `TK ViettelPay 9704...1278 GD -1,000 VND luc 2023-08-11 14:13:34 So du 3,372 VND Phi: -0 VND ND: GD thanh toan 230811182319866 NAP TIEN DIEN THOAI cho Khach hang 0867256447`
  - **Persuasion Tactics (Reviewer A):** `['none']`
  - **Persuasion Tactics (Mistral):** `[]`

**6. Mã mẫu: `phase1_00709`**
- **Nội dung:** `The Visa 452404...6779 su dung tai 2C2*AMAZON PRIME VIDEO VN6717 2333 SG so tien 13,608 VND luc 17-12-2022 17:37:45. SD TK trich no tam tinh 1033311702: 486,392VND`
  - **Persuasion Tactics (Reviewer A):** `['none']`
  - **Persuasion Tactics (Mistral):** `[]`

**7. Mã mẫu: `phase1_00718`**
- **Nội dung:** `Ok e .Đem luôn ao sưa dum c nha`
  - **Persuasion Tactics (Reviewer A):** `['none']`
  - **Persuasion Tactics (Mistral):** `[]`

**8. Mã mẫu: `phase1_00825`**
- **Nội dung:** `[TB] Soan F70 gui 191: 70.000d/30 ngay co 3GB, mien phi 10p/cuoc noi mang, 20p ngoai mang. Goi cuoc gia han sau 30 ngay. CT ap dung den 14/09. LH 198 (0d).`
  - **Persuasion Tactics (Reviewer A):** `['reward_incentive', 'scarcity']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`
  - **Requested Actions (Reviewer A):** `['reply_message']`
  - **Requested Actions (Mistral):** `['reply_message', 'call_phone']`

**9. Mã mẫu: `phase1_01145`**
- **Nội dung:** `Bạn đã yêu cầu Google khôi phục quyền truy cập cho duyj4f2004@gmail.com? Nếu không phải thì hãy kiểm tra email để tìm hiểu cách DỪNG yêu cầu này.`
  - **Persuasion Tactics (Reviewer A):** `['urgency', 'fear']`
  - **Persuasion Tactics (Mistral):** `['urgency']`
  - **Requested Actions (Reviewer A):** `['other']`
  - **Requested Actions (Mistral):** `['click_or_visit_link']`

**10. Mã mẫu: `phase1_01146`**
- **Nội dung:** `[QC] Quy khach co 5700 diem tieu dung Viettel++ tinh den het ngay 02/08/2020. Bam goi *098# hoac truy cap ung dung MyViettel tai https://viettel.vn/app (muc Viettel++) de doi diem thanh Data, phut goi, SMS hoac cac uu dai gia tri khac. LH 198 (0d). Tu choi QC, soan HUY gui 9000.`
  - **Persuasion Tactics (Reviewer A):** `['reward_incentive', 'link_lure']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`

**11. Mã mẫu: `phase1_01191`**
- **Nội dung:** `(TB) TẶNG 50% TRÊN APP MYVNPT! VinaPhone tặng Quý khách 50% khi nạp tiền điện thoại bằng hình thức trực tiếp DUY NHẤT trên ứng dụng My VNPT trong hôm nay 14/9/2025 tại: https://my.vnpt.com.vn/adv/napdt . Khuyến mãi được sử dụng gọi và nhắn tin trong 15 ngày. CSKH:18001091 (0đ).`
  - **Persuasion Tactics (Reviewer A):** `['reward_incentive', 'link_lure', 'scarcity']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive', 'scarcity']`
  - **Requested Actions (Reviewer A):** `['click_or_visit_link', 'call_phone']`
  - **Requested Actions (Mistral):** `['click_or_visit_link']`

**12. Mã mẫu: `phase1_01414`**
- **Nội dung:** `Sử dụng mã xác minh 074736 để xác thực Microsoft.`
  - **Persuasion Tactics (Reviewer A):** `['none']`
  - **Persuasion Tactics (Mistral):** `[]`

**13. Mã mẫu: `phase1_01509`**
- **Nội dung:** `(TB) Chúc mừng năm mới Giáp Thìn 2024! Người dân chủ động sắp xếp thời gian trở lại nơi làm việc và sinh sống tại các thành phố lớn, tránh tình trạng ùn tắc giao thông vào cuối dịp nghỉ lễ, tuyệt đối không điều khiển phương tiện khi đã sử dụng rượu, bia.`
  - **Persuasion Tactics (Reviewer A):** `['authority']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`
  - **Requested Actions (Reviewer A):** `['other']`
  - **Requested Actions (Mistral):** `['none']`

**14. Mã mẫu: `phase1_01518`**
- **Nội dung:** `(TB) Để phòng ngừa cháy, nổ trong dịp Tết Nguyên Đán, Công an tỉnh khuyến cáo: Không sắp xếp hàng hóa, vật dụng gần nguồn lửa, nguồn nhiệt và lấn chiếm lối đi; Trông coi khi đun nấu, thắp hương, đốt vàng mã, cỏ rác; Tắt thiết bị điện, khóa van gas khi không sử dụng; Mở lối thoát hiểm thứ hai, chuẩn bị phương án thoát nạn và các phương tiện chữa cháy; Tham gia “Tổ liên gia an toàn PCCC”; Khi có sự cố cháy, nổ gọi ngay 114 hoặc sử dụng App “Báo cháy 114”.`
  - **Requested Actions (Reviewer A):** `['other', 'call_phone', 'install_application']`
  - **Requested Actions (Mistral):** `['click_or_visit_link', 'call_phone']`

**15. Mã mẫu: `phase1_01600`**
- **Nội dung:** `(TB) Quy Khach da huy thanh cong goi MI_D7 trên app My VNPT. Thong tin chi tiet truy cap My VNPT http://onelink.to/v58hh4 hoac lien he 18001091`
  - **Persuasion Tactics (Reviewer A):** `['link_lure']`
  - **Persuasion Tactics (Mistral):** `['reward_incentive']`