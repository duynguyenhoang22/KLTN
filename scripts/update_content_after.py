import csv
import io

# Data pasted by user (sample_id -> content_after)
new_data_raw = """sample_id,content
"phase1_09662","Gái xinh gọi là có Hồ Chí Minh Zalo liên hệ: https://zalo.me/g/hcm_call_me aS1d"
"phase1_09663","Em rảnh tối nay Hà Nội Telegram đi chơi không: https://t.me/hn_tonight_fun mK7h"
"phase1_09731","Hỗ trợ dịch bệnh COVID-19: Ông Bà đã đủ điều kiện NHẬN TIỀN hỗ trợ. Bấm vào www.mju78.icu. QUÁ HẠN SẼ KHÔNG ĐƯỢC CHẤP NHẬN! lZ4x"
"phase1_09733","Trợ cấp Nghị quyết 116: Bạn đã đủ điều kiện NHẬN TIỀN theo Nghị quyết 116. Nhận tại mo.lo098.com. QUÁ HẠN SẼ KHÔNG ĐƯỢC CHẤP NHẬN! xC2v"
"phase1_09801","Bạn đã được xác nhận vào nhóm đầu tư Telegram kiếm 1 triệu trên ngày. Bấm vào liên kết: t.me/invest_group_vip"
"phase1_09805","Bạn muốn kiếm thêm thu nhập không? Thả tim TikTok nhé, mỗi ngày chỉ cần 10 phút là có 150 nghìn nhé."
"phase1_09808","Đặt đơn hàng Shopee nhận hoa hồng cực khủng. Không cần kinh nghiệm, chỉ cần rảnh 20 phút hằng ngày."
"phase1_09816","Anh chị nạp vốn để bắt đầu giao dịch sao chép nhé. Số tài khoản: 0771122334 - Ngân hàng Quân Đội - CÔNG TY CỔ PHẦN ĐẦU TƯ QUỐC TẾ. Em lên lệnh ngay."
"phase1_09820","Nạp tiền vào tài khoản đầu tư: 0022334455 - Ngân hàng Vietcombank - CÔNG TY TNHH PHÁT TRIỂN CÔNG NGHỆ MỚI. Em duyệt đơn."
"phase1_09865","Kwin668 tặng 99 nghìn. Nạp X nhận Y! Nổ Hũ Bắn Cá Baccarat... Rút tối đa 10.000 nghìn. Liên kết: h7v2p.cc/mKz8"
"phase1_09867","Kim Long Casino tặng 88 nghìn! Nạp 100 nghìn nhận 300 nghìn. 1 vòng cược rút tối đa. Liên kết: bz9q1.tech/xY6t"
"phase1_09944","Em mới đi làm cần tìm anh vui vẻ tại Hà Nội – Zalo: zalo.me/g/hn_baby69_v1 Tr9X"
"phase1_09945","Cần tìm người tâm sự đêm khuya Hà Nội – Telegram: t.me/hanoi_dem_vui_77 G8wP"
"phase1_09946","Dịch vụ Gái gọi Hạng sang Hồ Chí Minh – Zalo: bit.ly/hcm_luxury_33 K9vL"
"phase1_09947","Em đang rảnh vui vẻ cùng anh Đà Nẵng – Telegram: t.ly/danang_hot_girl_9x Qz4M"
"phase1_09948","Tìm anh trai nuôi sinh viên Hạng vip Hà Nội – Telegram: t.me/hn_student_vip_ss R5tK"
"phase1_09949","Anh muốn vui vẻ không Hà Nội – Zalo: zalo.me/g/em_xinh_hn77_m B2nQ"
"phase1_09950","Gái xinh phục vụ tận nơi Hồ Chí Minh – Telegram: t.me/hcm_4u_now_vip P8mJ"
"phase1_09951","Sinh viên tìm người giúp đỡ Hồ Chí Minh – Zalo: bit.ly/hcm_sv_tro_giup_68 L1cH"
"phase1_09952","Anh ơi em mới lên vui vẻ Đà Nẵng – Telegram: t.me/dn_em_moi_99_hot S7dG"
"phase1_09953","Kết bạn vui vẻ nhận hình Hà Nội – Telegram: t.ly/hn_xinh_tuoi_vnp F4vR"
"phase1_09954","Em đang ở khách sạn Hồ Chí Minh – Zalo: zalo.me/g/hcm_hot_em_x8 X5kN"
"phase1_09955","Tìm kế hoạch vui vẻ cùng em Hà Nội – Telegram: t.me/hn_vui_v3_999 W3pZ"
"phase1_09956","Em xinh ngon cần chủ nhân Hồ Chí Minh – Zalo: bit.ly/hcm_sugar_68_v M9jK"
"phase1_09957","Tìm bạn hẹn hò kín đáo Hồ Chí Minh - Telegram t.me/hcm_kin_dao Gz2X"
"phase1_09958","Gái xinh sinh viên làm thêm Hà Nội - Zalo bitly/hn_sv_xinh T7vY"
"phase1_09959","Cho thuê phục vụ vui vẻ Đà Nẵng - Telegram t.me/dn_vip_69 L1mB"
"phase1_09960","Em đang cô đơn tại Hồ Chí Minh - Zalo zalome/g/hcm_pv_now J6rK"
"phase1_09961","Kết bạn vui vẻ cùng em Hà Nội - Telegram t.ly/hn_vui_ve R9tD"
"phase1_09962","Em mới về Hồ Chí Minh chưa có ai - Zalo bitly/hcm_moi_ve H4sW"
"phase1_09963","Dịch vụ em út Hà Nội - Telegram t.me/hn_em_ut_vip V2nQ"
"phase1_09964","Sinh viên nhẹ nhàng vui vẻ Đà Nẵng - Telegram t.me/dn_sv_ne P3vL"
"phase1_09965","Anh có muốn gặp em không Hồ Chí Minh - Zalo zalome/g/hcm_x8 K5fJ"
"phase1_09966","Hẹn hò vui vẻ qua đêm Hà Nội - Zalo bitly/hn_dem_vip F8mH"
"phase1_09967","Em tên Ly 20 tuổi xinh tươi Hồ Chí Minh - Telegram t.me/hcm_ly_x S1vG"
"phase1_09968","Tìm anh trai nuôi Hà Nội - Zalo bitly/hn_sugar_vn D4wX"
"phase1_09969","Em ở khu vực Đà Nẵng vui vẻ - Telegram t.me/dn_em_ne G7hP"
"phase1_09970","Tìm bạn vui vẻ Hồ Chí Minh Telegram: bit.ly/hcm_hot_68_xx XyZ1"
"phase1_09971","Gái xinh vui vẻ Hà Nội Zalo: zalo.me/g/hn_vui_v3_99_vv B2nQ"
"phase1_09972","Phục vụ tận nơi Hà Nội Telegram: t.me/hn_tan_noi_vip_88 R5tK"
"phase1_09973","Em mới lên vui vẻ Đà Nẵng Telegram: t.ly/dn_moi_len_vui_55 S7dG"
"phase1_09974","Anh ơi em xinh Hồ Chí Minh Zalo: bit.ly/hcm_em_xinh_2024_n P8mJ"
"phase1_09975","Kết bạn vui vẻ Hà Nội Telegram: t.me/hn_ket_ban_vui_vip F4vR"
"phase1_09976","Sinh viên tìm người giúp Hồ Chí Minh Zalo: bit.ly/hcm_sv_can_giup_77 L1cH"
"phase1_09977","Dịch vụ vui vẻ Đà Nẵng Telegram: t.me/dn_dich_vu_vui_99 Qz4M"
"phase1_09978","Em đang rảnh Hà Nội Zalo: zalo.me/g/hn_em_ranh_69_x W3pZ"
"phase1_09979","Gặp em vui vẻ Hồ Chí Minh Telegram: t.me/hcm_gap_em_vui_68 X5kN"
"phase1_09980","Hẹn hò vui vẻ Hà Nội Zalo: bit.ly/hn_hen_ho_kin_dao_1 D4wX"
"phase1_09981","Tìm anh trai nuôi sinh viên Hồ Chí Minh Telegram: t.me/hcm_anh_trai_nuoi_sv S1vG"
"phase1_09982","Em tên Hương Đà Nẵng Telegram: t.ly/dn_em_huong_99_hot G7hP"
"phase1_09983","Kết bạn xem hình Hà Nội Zalo: zalo.me/g/hn_xem_hinh_vip_n M9jK"
"phase1_10034","Chào bạn, mình là Long. Công việc sao chép giao dịch thị trường ngoại hối Forex kiếm 1 triệu mỗi ngày. Không cần vốn, chỉ cần 10 phút."
"phase1_10035","Đầu tư sàn XYZ với chuyên gia kiếm 2 triệu đến 5 triệu mỗi ngày. Thêm Telegram bắt đầu: t.me/group_dautu_xyz_99"
"phase1_10036","Anh chị chuyển khoản vào Số tài khoản: 12345678 Ngân hàng ACB Tài khoản: CÔNG TY TRUYỀN THÔNG để nhận việc thả tim TikTok ngay."
"phase1_10037","Chào bạn, mình là Vi. Công việc đặt đơn hàng kiếm 300 nghìn mỗi ngày. Không cần vốn, trả tiền cuối ngày."
"phase1_10038","Bạn muốn kiếm tiền từ thị trường ngoại hối Forex không? Liên hệ giáo viên tại Telegram: t.me/forex_huongdan_mienphi"
"phase1_10039","Nạp tiền vào Số tài khoản: 8899776655 Ngân hàng MB Tài khoản: CÔNG TY ĐẦU TƯ XUẤT NHẬP KHẨU để nhận lãi suất đầu tư sàn XYZ nhé."
"phase1_10040","Chào bạn, mình là Kiệt. Công việc thả tim video TikTok kiếm 200 nghìn mỗi ngày. Không cần kinh nghiệm."
"phase1_10041","Muốn kiếm 400 nghìn đến 800 nghìn mỗi ngày? Chỉ cần đặt đơn hàng. Thêm Telegram nhận việc: t.me/donhang_online_vn88"
"phase1_10042","Anh chị chuyển khoản vào Số tài khoản: 1010202030 Ngân hàng Techcombank Tài khoản: CÔNG TY ĐẦU TƯ ĐẠI NAM để sao chép giao dịch Forex nhé."
"phase1_10043","Bạn đã đủ ĐIỀU KIỆN nhận ưu đãi từ sàn XYZ. Kiếm 1 triệu mỗi ngày. Không cần vốn, chỉ cần 15 phút."
"phase1_10046","Bạn đã đủ ĐIỀU KIỆN nhận TIỀN hỗ trợ. Chuyển vào Số tài khoản: 1903348572910 Công ty TNHH ĐẦU TƯ FINTECH. Bảo hộ vốn."
"phase1_10049","Sao chép giao dịch thị trường ngoại hối Forex với chuyên gia. Lãi như ý 20 phần trăm mỗi ngày. Không rủi ro. Tham gia nhóm Telegram: t.me/copytrade_pro_vn"
"phase1_10052","Nhân viên Shopee tuyển mới. Đặt đơn hàng nhận hoa hồng 20 phần trăm. Số tài khoản nạp tiền: 00410003221 KHUẤT DUY NAM."
"phase1_10055","Thu nhập thụ động 3 đến 5 triệu trên tuần. Không cần kinh nghiệm. Giáo viên hướng dẫn 1 kèm 1. t.me/dau_tu_thong_minh_vnn"
"phase1_10058","Đầu tư sàn XYZ lãi suất cao. Nhận vốn trải nghiệm miễn phí. Số tài khoản ĐẦU TƯ: 1022334455 Ngân hàng MB BANK."
"phase1_10061","BẠN ĐỦ ĐIỀU KIỆN NHẬN QUÀ TIỀN MẶT 500 NGHÌN. Chuyển khoản phí kích hoạt 100 nghìn vào Số tài khoản 0391223344 Ngân hàng Vietcombank."
"phase1_10064","Sao chép giao dịch thị trường ngoại hối FOREX nhận lãi khủng. Không cần kinh nghiệm. Chuyển vào Số tài khoản ĐẦU TƯ: 19022334455018 Ngân hàng Techcombank."
"phase1_10067","Đầu tư 4.0 cam kết lãi 30 phần trăm. Không rủi ro. Nhấp vào nhóm Telegram để được hỗ trợ: t.me/dautu_taichinh_40"
"phase1_10070","CHUYỂN KHOẢN VÀO SỐ TÀI KHOẢN: 1122334455 NGÂN HÀNG BIDV ĐỂ NHẬN GÓI ĐẦU TƯ NHÂN 2 TÀI KHOẢN. CÔNG TY CỔ PHẦN ĐẦU TƯ SAO MAI."
"phase1_10073","THẢ TIM VIDEO NHẬN 100 NGHÌN MỖI NGÀY. Không cần vốn đầu tư. Nhấp vào nhóm Telegram: t.me/tiktok_kiemtien_free"
"phase1_10076","ĐẦU TƯ CHỨNG KHOÁN QUỐC TẾ LÃI SUẤT CAO. SỐ TÀI KHOẢN NẠP TIỀN: 0491000123456 NGÂN HÀNG VIETCOMBANK. CHỦ TÀI KHOẢN: LÊ THÀNH BÌNH. BẢO HỘ VỐN."
"phase1_10079","NHÂN VIÊN QUẢN LÝ ĐƠN HÀNG TRỰC TUYẾN. Thu nhập 500 nghìn đến 2 triệu trên ngày. Không thu phí. Nhấp vào t.me/shopee_official_vn"
"phase1_10082","ĐẦU TƯ CỔ PHIẾU TIỀM NĂNG. LÃI SUẤT 20 PHẦN TRĂM TRÊN THÁNG. CHUYỂN VÀO SỐ TÀI KHOẢN CÔNG TY: 101122334455 NGÂN HÀNG VIB BANK."
"phase1_10487","Kwin668 Nạp 100 nghìn nhận 300 nghìn rút liền tay - 1 vòng cược - Nổ Hũ - Bắn Cá - Baccarat - Đăng ký: t.ly/mN5vR - kL9p"
"phase1_10489","Kim Long Casino tặng 58 nghìn trải nghiệm - Nạp 50 nghìn nhận 128 nghìn - Rút tối đa 5.000 nghìn - Nổ Hũ - Baccarat - t.ly/vR4sT - iO1q"
"phase1_10490","8Day tặng 88 nghìn cho thành viên mới! Nạp 50 nghìn nhận 150 nghìn 1 vòng cược rút tối đa 8.888 nghìn t.ly/bN2mX-zS4d"
"phase1_10494","789Bet Nạp 100 nghìn nhận 200 nghìn rút liền tay! 1 vòng cược rút tối đa 15.000 nghìn - Nổ Hũ - t.ly/tG7fD-sX3c"
"phase1_10496","V7Bet tải ứng dụng nhận 128 nghìn nhân 3 nạp đầu rút không cần nạp, Tiến Lên Miền Nam - Xóc Đĩa - Nổ Hũ - Liên kết: xd82k.cc"
"phase1_10497","Kim Long Casino tải ứng dụng tặng 158 nghìn nhân 3 nạp đầu rút không cần nạp, Tiến Lên Miền Nam - Xóc Đĩa - nhấp vào: m91vj.tech"
"phase1_10499","JILI tải ứng dụng nhận 88 nghìn nhân 3 nạp đầu rút không cần nạp, Tiến Lên Miền Nam - Xóc Đĩa - Nổ Hũ - Liên kết: b41nz.tech"
"phase1_10501","Giải trí 2Q tải ứng dụng nhận 199 nghìn nhân 3 nạp đầu rút ngay, Tiến Lên Miền Nam, Xóc Đĩa, Nổ Hũ, Liên kết: k52mp.tech"
"phase1_10503","Kwin668 tải ứng dụng nhận 222 nghìn nhân 3 nạp đầu rút không cần nạp, Tiến Lên Miền Nam, Xóc Đĩa - Liên kết: f82ps.tech"
"phase1_10505","Kim Long Casino tải ứng dụng nhận 99 nghìn nhân 3 nạp đầu rút không cần nạp - Tiến Lên Miền Nam - Xóc Đĩa - Liên kết: l82ws.tech"
"phase1_10506","8Day Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 gửi và rút trong 3 phút. Đăng ký: d82ms.com"
"phase1_10507","JILI Baccarat trực tiếp! chơi gà xổ số Chăm sóc khách hàng 24/24 gửi và rút trong 3 phút. Liên kết: j82ks.com"
"phase1_10508","Awin Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 gửi và rút trong 3 phút. Đăng ký: a11nz.com"
"phase1_10509","Giải trí 2Q Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 rút trong 3 phút. Liên kết: g72bq.com"
"phase1_10510","789Bet Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 gửi và rút trong 3 phút. Đăng ký: s52kp.com"
"phase1_10511","Kwin668 Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 gửi và rút trong 3 phút. Liên kết: k32vw.com"
"phase1_10512","V7Bet Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 gửi và rút trong 3 phút. Đăng ký: v92zq.com"
"phase1_10513","Kim Long Casino Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 rút trong 3 phút. Liên kết: m21yt.com"
"phase1_10515","JILI Baccarat trực tiếp chơi gà xổ số Chăm sóc khách hàng 24/24 rút trong 3 phút. Liên kết: i72xw.com"
"phase1_10516","Awin tuyển đại lý hoa hồng 50% trả nhiều hình thức liên hệ zalo: 0938123456. Liên kết: awin.vip"
"phase1_10517","Giải trí 2Q tuyển đại lý hoa hồng 55% trả nhiều hình thức Zalo: 0388776655. Liên kết: g2q.bet"
"phase1_10519","Kwin668 tuyển đại lý hoa hồng 45% trả nhiều hình thức Zalo: 0912334455. Liên kết: kwin.bet"
"phase1_10521","Kim Long tuyển đại lý hoa hồng 60% trả nhiều hình thức Zalo: 0908554433. Liên kết: klong.bet"
"phase1_10523","JILI tuyển đại lý hoa hồng 55% trả nhiều hình thức Zalo: 0944221166. Liên kết: jili.bet"
"phase1_10525","Giải trí 2Q tuyển đại lý hoa hồng 50% trả nhiều hình thức Zalo: 0911002299. Liên kết: g2qvn.bet"
"phase1_02364","Trao đổi tình tiền: Mạng lưới nhận tiền thưởng, Hãy gia nhập nhận tiền thưởng, Hướng dẫn bảo toàn tiền hay tại đây P3m56"
"phase1_02365","Đăng nhập chơi ngay tặng phong bao lì xì 8888 nghìn miễn phí. Đăng ký tại liên kết: fr3e.win/z1r5Dd"
"phase1_02367","Nhóm nhận liền quà hằng ngày. Hội viên mới nạp vào tài khoản lần đầu tiên tặng hai trăm ngàn miễn phí tại UWIN nhóm 66f7fxxzz.r-kl.com"
"phase1_02368","Liên kết: bit.ly/Q5YuG Bảo hiểm cứu thua 8 phần trăm. Nạp vào lần đầu ưu đãi 8 triệu 8. Bấm gửi mã xác thực nhận quà hằng ngày phục vụ 24 giờ hoàn trả 1,4 phần trăm."
"phase1_02373","Đăng nhập chơi ngay tặng phong bao lì xì 8888 nghìn miễn phí. Đăng ký liên kết: fr3e.win/hNgfZh"
"phase1_02385","(Bảo hiểm xã hội tỉnh) Bạn thỏa điều kiện nhận tiền hỗ trợ từ quỹ Bảo hiểm thất nghiệp, vui lòng nhập NGAY >> m.bidstk.icu để lấy. QUÁ HẠN SẼ KHÔNG ĐƯỢC CHẤP NHẬN! ErHg"
"phase1_02395","https://www.google.com/search?q=cash288699.com lì xì 108 đến 188 nghìn. Chương trình quà tặng."
"phase1_02396","Anh ơi Em vừa tròn 20 tuổi Ngực đẹp dáng chuẩn dịu dàng Muốn kiếm thêm thu nhập Em có thể đến tận nơi phục vụ Liên hệ zalo: 528450052 chăm sóc"
"phase1_02397","https://www.google.com/search?q=cash688299.com thưởng 108 đến 188 nghìn. Chương trình ưu đãi."
"phase1_02424","Xin chúc mừng thuê bao 0912345678 đã trúng thưởng một điện thoại iPhone 14 Pro Max trong chương trình dự thưởng cuối năm. Liên hệ: 19001995 để nhận giải. Đề nghị liên hệ trước ngày 28/01"
"phase1_02432","Cục thuế: Bạn đã đủ ĐIỀU KIỆN HOÀN THUẾ Thu nhập cá nhân, tải tại: https://hoanthue-tncn.vip"
"phase1_02433","Nhóm nhận liền quà hằng ngày. Hội viên mới nạp vào tài khoản lần đầu tiên tặng hai trăm ngàn miễn phí tại UWIN nhóm 66f7fxxzz.r-kl.com"
"phase1_02434","Liên kết: bit.ly/Q5YuG Bảo hiểm cứu thua 8 phần trăm. Nạp vào lần đầu ưu đãi 8 triệu 8. Bấm gửi mã xác thực nhận quà hằng ngày phục vụ 24 giờ hoàn trả 1,4 phần trăm."
"phase1_02435","Lấy ngay bảy mươi chín nghìn khi tải ứng dụng về và xác nhận số điện thoại. Khuyến mãi vòng quay phát tài 159 nghìn tại liên kết vbu_los_ng.qcpo.bid"
"phase1_02476","(Thông báo) - Bạn đã đủ điều kiện NHẬN TIỀN hỗ trợ từ quỹ Bảo hiểm thất nghiệp. Bấm vào www.movnb.icy để lấy. QUÁ HẠN SẼ KHÔNG ĐƯỢC CHẤP NHẬN!"
"phase1_02541","https://www.google.com/search?q=cash688299.com Vào Google nhận thưởng 108-188 nghìn."
"phase1_02544","Liên kết: t.ly/xZ4h Hoàn trả hoàn toàn 1888 nghìn. Nạp và Thưởng cho anh em 50 nghìn. Bảo chứng an toàn 30 phần trăm."
"phase1_02554","1 tháng 6 cập nhật game DWIN tặng mã quà tặng 99 nghìn. Nhân 3 nạp lần đầu. Chơi game bài, nổ hũ... tải tại: http://chutjf.space/r/Dbc8O0iBQe Liên hệ nhận mã quà tặng qua Telegram: http://chutjf.space/r/osO0ewBiiX"
"""

# Parse new data into a dict
update_map = {}
reader = csv.DictReader(io.StringIO(new_data_raw))
for row in reader:
    update_map[row['sample_id']] = row['content']

print(f"Parsed {len(update_map)} entries to update")

# Read the original CSV
csv_path = r'c:\KLTN\KLTN\data\final\ds345.csv'
with open(csv_path, encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

# Update content_after
updated = 0
already_had = 0
for row in rows:
    sid = row['sample_id']
    if sid in update_map:
        if row['content_after'].strip():
            already_had += 1
        row['content_after'] = update_map[sid]
        updated += 1

print(f"Updated: {updated} rows (of which {already_had} already had a value - overwritten)")
print(f"Still empty: {sum(1 for r in rows if not r['content_after'].strip())}")

# Write back
with open(csv_path, encoding='utf-8', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames

with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)

print("Done! File updated.")
