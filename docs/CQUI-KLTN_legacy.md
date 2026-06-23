ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH
TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN
KHOA KHOA HỌC VÀ KỸ THUẬT THÔNG TIN
NGUYỄN HOÀNG DUY
TRẦN NGUYỄN NAM HẢI
KHÓA LUẬN TỐT NGHIỆP
PHÁT HIỆN TIN NHẮN LỪA ĐẢO TIẾNG VIỆT THÔNG
QUA CHƯNG CẤT TRI THỨC VÀ TĂNG CƯỜNG DỮ
LIỆU TRÊN MÔ HÌNH NGÔN NGỮ LỚN
Vietnamese Smishing Detection via Knowledge Distillation and
LLM-driven Data Augmentation
CỬ NHÂN NGÀNH CÔNG NGHỆ THÔNG TIN
GIẢNG VIÊN HƯỚNG DẪN
ThS. HUỲNH VĂN TÍN
TP. HỒ CHÍ MINH, 2026

ĐẠI HỌC QUỐC GIA TP. HỒ CHÍ MINH
TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN
KHOA KHOA HỌC VÀ KỸ THUẬT THÔNG TIN
NGUYỄN HOÀNG DUY - 22520327
TRẦN NGUYỄN NAM HẢI - 22520391
KHÓA LUẬN TỐT NGHIỆP
PHÁT HIỆN TIN NHẮN LỪA ĐẢO TIẾNG VIỆT THÔNG
QUA CHƯNG CẤT TRI THỨC VÀ TĂNG CƯỜNG DỮ
LIỆU TRÊN MÔ HÌNH NGÔN NGỮ LỚN
Vietnamese Smishing Detection via Knowledge Distillation and
LLM-driven Data Augmentation
CỬ NHÂN NGÀNH CÔNG NGHỆ THÔNG TIN
GIẢNG VIÊN HƯỚNG DẪN
ThS. HUỲNH VĂN TÍN
TP. HỒ CHÍ MINH, 2026

THÔNG TIN HỘI ĐỒNG CHẤM KHÓA LUẬN TỐT NGHIỆP
Hội đồng chấm khóa luận tốt nghiệp, thành lập theo Quyết định số ……………………
ngày ………………….. của Hiệu trưởng Trường Đại học Công nghệ Thông tin.

LỜI CẢM ƠN
Lời đầu tiên, nhóm chúng em xin cảm ơn Thầy ThS. Huỳnh Văn Tín đã đồng ý làm
giáo viên hướng dẫn cho khóa luận tốt nghiệp của chúng em. Chúng em rất biết ơn vì
kiến thức chuyên môn mà thầy cung cấp cũng như giải đáp các thắc mắc và chúng
em gặp phải. Nhờ thầy mà đề tài khóa luận của chúng em có thể hoàn thiện khóa luận
tốt nghiệp một cách suôn sẻ. Nhóm chúng em cũng cảm ơn các thầy cô Trường Đại
học Công Nghệ Thông Tin nói chung và các thầy cô Khoa Khoa học và Kĩ thuật
Thông tin nói riêng vì đã luôn quan tâm, nhắc nhở, định hướng cho bốn năm học trên
ghế nhà trường. Nhờ có các thầy cô, chúng em có thể học hỏi và tích lũy các kiến
thức và trải nghiệm quý báu cho hành trình sau này. Cuối cùng, chúng em xin biết
ơn ba mẹ là điểm tựa vững chắc, luôn chăm sóc và động viên chúng em trong quá
trình học tập, cũng như bạn bè xung quanh luôn sẵn sàng giúp đỡ khi chúng em gặp
khó khăn.
Chúng em biết khóa luận của chúng em vẫn còn nhiều thiếu sót, nên chúng em rất
mong nhận được những lời đóng góp, gợi ý để khóa luận của chúng em hoàn thiện
hơn.
Chúng em xin chân thành cảm ơn!
Thành phố Hồ Chí Minh, tháng 6, năm 2026
Thành viên
Nguyễn Hoàng Duy, Trần Nguyễn Nam Hải


MỤC LỤC

MỤC LỤC ................................................................................................................... 5
TÓM TẮT KHÓA LUẬN ........................................................................................ 10
CHƯƠNG 1 GIỚI THIỆU ................................................................................... 12
1.1 Bối cảnh bài toán ........................................................................................ 12
1.2 Động lực nghiên cứu .................................................................................. 13
1.3 Đối tượng, phạm vi nghiên cứu và mục tiêu bài toán ................................ 14
CHƯƠNG 2 CƠ SỞ LÝ THUYẾT & NGHIÊN CỨU LIÊN QUAN ................. 18
2.1 Tổng quan và định nghĩa bài toán phát hiện tin nhắn lừa đảo ................... 18
2.2 Các công trình nghiên cứu liên quan .......................................................... 26
2.2.1 Nghiên cứu sử dụng dữ liệu tạo sinh trong phân loại văn bản ........... 26
2.2.2 Nghiên cứu đánh giá dữ liệu tạo sinh bằng TSTR/domain gap .......... 28
CHƯƠNG 3 XÂY DỰNG BỘ DỮ LIỆU ............................................................ 29
3.1 Quy trình thu thập, gán nhãn dữ liệu thực .................................................. 29
3.1.1 Thu thập thủ công từ các nguồn công khai trên mạng ........................ 29
3.1.2 Thu thập dữ liệu thực tế thông qua thiết bị di động ............................ 30
3.1.3 Quy trình gán nhãn dữ liệu thực ......................................................... 31
3.1.4 Phân tích sơ bộ dữ liệu thực ................................................................ 33
3.2 Quy trình xây dựng bộ dữ liệu tạo sinh ...................................................... 34
3.2.1 Nền tảng xây dựng dữ liệu tạo sinh .................................................... 34
3.2.2 Kiến trúc mô hình tăng cường dữ liệu bằng LLM .............................. 36
3.2.3 Pipeline sinh dữ liệu và đánh giá chất lượng ...................................... 38
3.3 Cải thiện và đánh giá bộ dữ liệu tạo sinh ................................................... 39
3.3.1 Các biện pháp đã áp dụng ................................................................... 39
3.3.2 Đánh giá định lượng bộ dữ liệu tạo sinh ............................................. 42
3.3.3 Quy trình kiểm định và gán nhãn Metadata v2 ... 44
3.4 Phân tích bộ dữ liệu tổng thể (ViSmish) .................................................... 45
3.4.1 Thành phần bộ dữ liệu ........................................................................ 46
3.4.2 Phân phối nhãn mục tiêu ..................................................................... 48
3.4.3 Phân tích đặc trưng metadata .............................................................. 49
3.4.4 Phân tích văn bản ................................................................................ 53
CHƯƠNG 4 PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM .................. 58
4.1 Tổng quan thiết kế thực nghiệm .................................................................. 58
4.2 Dữ liệu và chiến lược phân chia .................................................................. 60
4.3 Các mô hình benchmark ............................................................................... 65
4.4 Thiết lập huấn luyện .................................................................................... 70
4.5 Các độ đo đánh giá ...................................................................................... 75
4.6 Phương pháp phân tích kết quả ................................................................... 78
4.7 Thí nghiệm bổ sung về dữ liệu tạo sinh ....................................................... 81
CHƯƠNG 5 KẾT QUẢ VÀ PHÂN TÍCH ............................................................ 85
5.1 RQ1: Mô hình nào đạt hiệu quả tốt nhất? .................................................... 85
5.2 RQ2: Đặc điểm nào của dữ liệu làm thay đổi hiệu năng? ........................... 90
5.3 RQ3: Mô hình sai ở đâu và vì sao? ............................................................. 95
CHƯƠNG 6 KẾT LUẬN ................................................................................... 104
6.1 Kết quả đạt được ...................................................................................... 104
6.2 Hạn chế của đề tài .................................................................................... 105
6.3 Phương hướng phát triển trong tương lai ................................................. 106
TÀI LIỆU THAM KHẢO ....................................................................................... 108
CHƯƠNG 7 PHỤ LỤC ...................................................................................... 111
7.1 Cấu hình chi tiết và Siêu tham số của 17 mô hình Benchmark ................ 111
7.2 Các mẫu Prompt trong quy trình tạo sinh và gán nhãn tự động ............... 113

DANH MỤC HÌNH VÀ BẢNG

Hình 1: Định nghĩa bài toán nhận diện tin nhắn lừa đảo ................................................ 18
Hình 2: Quy trình thu thập dữ liệu thực và gán nhãn .................................................... 31
Hình 3: Quy trình sinh dữ liệu tạo sinh bằng LLM ......................................................... 36
Hình 4: Các bước cải thiện bộ dữ liệu ............................................................................ 39
Hình 5: Phân phối dữ liệu theo nhãn lừa đảo ................................................................. 48
Hình 6: Phân phối dữ liệu theo sender_type .................................................................. 49
Hình 7: Phân phối nhãn lừa đảo theo sender_type ........................................................ 50
Hình 8: Phân phối đặc trưng has_url theo nhãn lừa đảo ................................................ 51
Hình 9: Phân phối đặc trưng has_phone_number theo nhãn lừa đảo ............................ 52
Hình 10: Phân phối dữ liệu theo category ...................................................................... 52
Hình 11: Phân phối dữ liệu theo mức độ obfuscation .................................................... 53
Hình 12: WordCloud của data thực và data tạo sinh theo từng nhãn ........................... 55
Hình 13: Quy trình thực nghiệm tổng quát .................................................................... 58
Hình 14: Hiệu năng của mô hình theo độ dài tin nhắn ................................................... 83
Hình 15: Hiệu năng của mô hình theo tín hiệu URL ...................................................... 84


TÓM TẮT KHÓA LUẬN
Trong bối cảnh các cuộc tấn công lừa đảo qua tin nhắn (smishing) ngày càng
gia tăng và gây thiệt hại tài chính nặng nề tại Việt Nam, các hệ thống phát hiện dựa
trên luật (rule-based) truyền thống đang dần bộc lộ nhiều hạn chế trước các kỹ thuật
ngụy trang ngôn ngữ tinh vi. Việc ứng dụng các mô hình học máy hiện đại để giải
quyết bài toán này vấp phải hai rào cản cốt lõi: sự khan hiếm trầm trọng của các bộ
dữ liệu SMS tiếng Việt chất lượng cao gây ra tình trạng mất cân bằng nhãn, và rào
cản về tài nguyên phần cứng khi triển khai các Mô hình Ngôn ngữ Lớn (LLM) trên
thiết bị di động cá nhân.
Để giải quyết các thách thức trên, khóa luận đề xuất một giải pháp toàn diện
bao gồm hai hướng tiếp cận: tăng cường dữ liệu định hướng bởi LLM và chưng cất
tri thức (Knowledge Distillation). Đối với rào cản dữ liệu, nghiên cứu đã xây dựng
thành công bộ dữ liệu ViSmish gồm 10.562 mẫu, là sự kết hợp có chọn lọc giữa dữ
liệu thực tế, dữ liệu tạo sinh từ các LLM (Gemini, Mistral) và dữ liệu hội thoại ngoại
lai (ViLexNorm). Đối với rào cản tính toán, nghiên cứu tiến hành chưng cất phân
phối xác suất từ một mô hình giáo viên mạnh nhưng nặng nề (PhoBERT-base) sang
các mô hình học sinh nhỏ gọn hơn (bao gồm BiLSTM và TextCNN).
Thông qua các thiết lập thực nghiệm nghiêm ngặt (như TSTR và Real +
Synthetic Augmentation), kết quả nghiên cứu khẳng định dữ liệu tạo sinh từ LLM
không thể thay thế hoàn toàn dữ liệu thực, nhưng đóng vai trò xuất sắc như một nguồn
tăng cường bổ trợ, giúp mô hình bắt được nhiều tin nhắn lừa đảo hơn mà không làm
thay đổi ranh giới phân phối thật. Ở nhánh thực nghiệm chưng cất tri thức, mô hình
học sinh TextCNN sau chưng cất đã thể hiện sự vượt trội và độ ổn định cao nhất, cải
thiện toàn diện các chỉ số nhận diện (Macro-F1, F1 Label 1, Recall và Precision) đồng
thời giảm thiểu đáng kể số lượng dự đoán sai (FP và FN) so với việc chỉ học từ nhãn
cứng gốc.

Nghiên cứu này không chỉ đóng góp một bộ dữ liệu smishing tiếng Việt chuẩn
hóa cho cộng đồng mà còn chứng minh tính khả thi của việc kết hợp dữ liệu tạo sinh
và kỹ thuật chưng cất tri thức để xây dựng các mô hình cảnh báo lừa đảo nhỏ gọn, độ
chính xác cao, sẵn sàng triển khai trên các thiết bị viễn thông có tài nguyên giới hạn.
11

CHƯƠNG 1 GIỚI THIỆU
1.1 Bối cảnh bài toán
Trong thời đại kỹ thuật số, lừa đảo qua tin nhắn SMS đã trở thành một trong
những mối đe dọa an ninh mạng phổ biến và đáng lo ngại nhất trên toàn cầu. Những
kẻ lừa đảo liên tục thay đổi phương pháp và cách thức, khiến loại hình tấn công này
gia tăng chóng mặt. Theo dữ liệu từ Keepnet Labs, ngay từ năm 2020, số lượng các
vụ lừa đảo qua tin nhắn SMS đã tăng mạnh 328%. Xu hướng này không có dấu hiệu
chậm lại, khi báo cáo năm 2025 của Zimperium chỉ ra mức tăng trưởng ổn định 22%
hàng năm đối với lừa đảo qua tin nhắn SMS, và đáng chú ý là 69,3% tổng số vụ lừa
đảo vào năm 2025 sẽ được thực hiện qua tin nhắn SMS. Phù hợp với quan điểm đó,
thống kê từ APWG trong quý 4 năm 2025 cũng cho thấy một bức tranh đáng báo
động: tỷ lệ lừa đảo qua tin nhắn SMS liên tục leo thang từ 30% đến 40% mỗi quý.
Tại Việt Nam, vấn đề này đang xảy ra trên quy mô lớn, gây ra những hậu quả
kinh tế vô cùng nặng nề cho người dùng cá nhân. Một cuộc khảo sát toàn diện của
Hiệp hội An ninh mạng quốc gia cho thấy, cứ 220 người dùng di động tại Việt Nam
thì có 1 người là nạn nhân của các vụ lừa đảo trực tuyến, tương đương với tỷ lệ rủi ro
là 0,45%. Tổng thiệt hại về tài chính do lừa đảo trực tuyến gây ra cho người dân cả
nước trong năm 2024 ước tính đạt 18.900 tỷ đồng, một số báo cáo kiểm toán độc lập
thậm chí ghi nhận mức biến động tối thiểu là 12.000 tỷ đồng. Nguy cơ tin nhắn lừa
đảo (phishing) xuất phát từ chính đặc điểm của tin nhắn SMS. Trong khi email chỉ
đạt tỷ lệ mở trung bình khoảng 20%, tin nhắn SMS có tỷ lệ mở tức thì lên đến 98%.
Lợi dụng lòng tin và thói quen giao dịch qua điện thoại thông minh, tội phạm mạng
liên tục phát tán hàng triệu tin nhắn lừa đảo mỗi ngày.
Để đối phó, các cơ quan quản lý nhà nước đã ban hành nhiều chính sách và
chỉ thị nghiêm ngặt nhằm siết chặt quản lý không gian mạng. Các ví dụ đáng chú ý
bao gồm Nghị định Chính phủ số 91/2020/ND-CP về phòng chống tin nhắn rác, email
rác và cuộc gọi rác, và Chỉ thị số 82/CT-BTTTT của Bộ Thông tin và Truyền thông
về phòng chống tin nhắn rác, tin nhắn lừa đảo và tăng cường quản lý thông tin trực
12

tuyến. Mặc dù các nhà cung cấp dịch vụ viễn thông đã triển khai nhiều giải pháp lọc
đầu cuối, số lượng báo cáo về tin nhắn lừa đảo gửi đến các cổng tiếp nhận quốc gia
vẫn tiếp tục tăng. Đường dây nóng 156/5656 để báo cáo tin nhắn và cuộc gọi rác đã
ghi nhận gần 850.000 báo cáo từ người dùng trong 10 tháng đầu năm 2024. Trong số
này, tin nhắn rác chiếm 22% (khoảng 185.000 báo cáo), cuộc gọi rác chiếm 52%
(khoảng 441.000 báo cáo) và cuộc gọi lừa đảo trực tiếp chiếm 26% (khoảng 222.000
báo cáo). Điều này cho thấy bọn lừa đảo đang sử dụng các chiến dịch đa kênh, tích
hợp linh hoạt các tin nhắn dụ dỗ và cuộc gọi giả mạo để tối đa hóa tỷ lệ đánh cắp tài
sản.
1.2 Động lực nghiên cứu
Trước sự leo thang và phát triển không ngừng của các hình thức tấn công kỹ
thuật số, các phương pháp phát hiện truyền thống chủ yếu dựa trên việc phân tích đặc
trưng tĩnh để thiết kế các luật cứng (rule-based) đã nhanh chóng bộc lộ giới hạn, dễ
dàng bị vượt qua bởi các biến thể tin nhắn ngày càng tinh vi và đa dạng. Các đối
tượng lừa đảo dễ dàng lách qua các bộ lọc từ khóa tĩnh bằng cách cố tình thay đổi ký
tự, chèn ký tự đặc biệt, viết tắt hoặc tráo đổi cấu trúc ngữ pháp. Để giải quyết triệt để
bài toán đó, xu hướng ứng dụng các mô hình học máy (Machine Learning) kết hợp
cùng kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) đã trở thành mũi nhọn công nghệ trong
cuộc chiến chống tin nhắn lừa đảo [5].
Tuy nhiên, hiệu quả của phương pháp hiện đại này phụ thuộc hoàn toàn vào
chất lượng và quy mô của tập dữ liệu huấn luyện. Đối với bối cảnh cụ thể tại Việt
Nam, điều này thực sự đặt ra một thách thức đáng kể. Thông qua nghiên cứu và tổng
quan tài liệu, chúng tôi nhận thấy hiện nay không có tập dữ liệu chuyên biệt, chuẩn
hóa nào về tin nhắn lừa đảo bằng tiếng Việt được công khai cho mục đích nghiên cứu.
Việc thu thập dữ liệu tin nhắn cũng gặp phải những trở ngại đáng kể liên quan đến
bảo mật thông tin cá nhân và nguồn thu thập khả dĩ. Hơn nữa, tiếng Việt trong tin
nhắn SMS rất phức tạp với nhiều biến thể đa dạng. Đối tượng lừa đảo và cả người
13

dùng đều thường xuyên sử dụng từ viết tắt, tiếng lóng, ngôn ngữ hỗn hợp hoặc tin
nhắn không có dấu câu.
Việc thiếu dữ liệu huấn luyện và sự phức tạp của ngữ cảnh tiếng Việt là những
rào cản lớn nhất hạn chế sự phát triển của hệ thống cảnh báo thông minh tại Việt
Nam. Để khắc phục tình trạng thiếu dữ liệu này, các kỹ thuật nâng cao dữ liệu truyền
thống (như hoán đổi từ và loại bỏ từ ngẫu nhiên) thường làm gián đoạn cấu trúc ngữ
pháp và ngữ nghĩa của câu, dẫn đến việc tạo ra nhiễu gây bất lợi cho mô hình. Sự
xuất hiện của Mô hình Ngôn ngữ Lớn (LLM) đã mở ra một hướng đi mới đầy hứa
hẹn, cho phép tạo ra dữ liệu văn bản chất lượng cao, đa dạng về ngữ cảnh và cấu trúc
câu trong khi vẫn duy trì các nhãn ngữ nghĩa cốt lõi [1].
Mặc dù LLM sở hữu khả năng nhận dạng và tạo dữ liệu vượt trội, việc triển
khai trực tiếp các mô hình khổng lồ này để chạy phân loại tin nhắn thời gian thực trên
thiết bị di động cá nhân hoặc hệ thống viễn thông vấp phải những hạn chế về tài
nguyên phần cứng, độ trễ xử lý và chi phí vận hành [2]. Do đó, dự án này đề xuất một
giải pháp huấn luyện một mô hình học sâu nhỏ gọn (Mô hình Học sinh), được tối ưu
thông qua các kỹ thuật chưng cất tri thức từ mô hình giáo viên PhoBERT-base [6] -
một mô hình ngôn ngữ được tối ưu hóa cho tiếng Việt với năng lực biểu diễn mạnh
nhưng chi phí suy luận cao hơn. Cách tiếp cận này cho phép mô hình học sinh kế thừa
tín hiệu phân phối xác suất từ giáo viên, đồng thời đảm bảo thời gian phản hồi nhanh
hơn, chi phí triển khai thấp hơn trên các thiết bị có tài nguyên hạn chế.
1.3 Đối tượng, phạm vi nghiên cứu và mục tiêu bài toán
Đối tượng nghiên cứu:
• Bộ dữ liệu tin nhắn SMS lừa đảo tiếng Việt, bao gồm các biến thể ngôn ngữ
đúng ngữ pháp, ngôn ngữ không trọng âm, viết tắt và cấu trúc ký tự đặc trưng
được sử dụng bởi những kẻ lừa đảo.
• Các phương pháp tăng cường dữ liệu văn bản (Data Augmentation) dựa trên
Mô hình Ngôn ngữ Lớn (LLM).
14

• Các mô hình ngôn ngữ Transformer phái sinh từ kiến trúc BERT, kết hợp với
việc thử nghiệm chưng cất với các mạng nơ-ron học sâu như TextCNN và
BiLSTM.
• Lý thuyết và thuật toán chưng cất tri thức để chuyển nhãn mềm từ mô hình
giáo viên sang mô hình học sinh.
Phạm vi nghiên cứu:
• Về ngôn ngữ: Chủ đề tập trung vào bài toán xử lý tin nhắn SMS tiếng Việt
đơn ngữ, đặc biệt là các tin nhắn ngắn có chứa biến thể viết tắt, thiếu dấu câu,
ký tự đặc biệt hoặc cách diễn đạt thường được sử dụng nhằm né tránh bộ lọc
nhà mạng. Các ngôn ngữ khác, văn bản dài và các loại dữ liệu ngoài miền SMS
không nằm trong phạm vi thực nghiệm.
• Về dữ liệu: Bộ dữ liệu thực được thu thập và gán nhãn thủ công với quy mô
giới hạn. Do hạn chế về thời gian và nguồn lực, bộ dữ liệu này chưa thể bao
phủ toàn bộ các biến thể ngôn ngữ và chiến thuật né lọc có thể xuất hiện trong
thực tế. Dữ liệu tạo sinh được sử dụng như một nguồn dữ liệu tăng cường,
không được xem là sự thay thế hoàn toàn cho dữ liệu thực.
• Về phương pháp: Nghiên cứu tập trung vào việc đánh giá vai trò của dữ liệu
tạo sinh thông qua các thiết lập như TSTR và huấn luyện kết hợp real-
synthetic. Khác với các hướng tiếp cận tập trung so sánh hiệu năng giữa nhiều
nhóm mô hình trên bộ dữ liệu thực được xây dựng thủ công, khoá luận này tập
trung vào việc xây dựng và đánh giá vai trò của dữ liệu tạo sinh trong bối cảnh
dữ liệu thực còn hạn chế. Cụ thể, khoá luận không chỉ đánh giá hiệu năng mô
hình trên tập kiểm thử real, mà còn phân tích mức độ tương đồng giữa dữ liệu
thực và dữ liệu tạo sinh, khả năng tổng quát hoá của mô hình khi huấn luyện
trên synthetic data theo thiết lập TSTR, tác động của synthetic data khi dùng
làm dữ liệu tăng cường, cũng như sự thay đổi trong các lỗi FP/FN trước và sau
khi tăng cường với dữ liệu tạo sinh.
15

• Về kỹ thuật Chưng cất Tri thức và Khả năng triển khai: Triển khai chưng cất
tri thức từ mô hình teacher PhoBERT-base sang các mô hình học sinh BiLSTM và
TextCNN nhằm đánh giá khả năng bảo toàn hiệu năng phân loại. Đồng thời, nghiên
cứu tiến hành đánh giá chi tiết tính khả thi khi triển khai (feasibility analysis)
của các mô hình học sinh so với teacher về số lượng tham số, kích thước checkpoint,
độ trễ CPU trên mỗi tin nhắn, thông lượng xử lý và dung lượng RAM cực đại.
Mục tiêu nghiên cứu:
• Tổng hợp một bộ dữ liệu thực được thu thập thủ công, cùng với bộ dữ liệu tạo
sinh thông qua quy trình tăng cường dữ liệu bằng LLM. Đồng thời đánh giá
vai trò tăng cường của dữ liệu tạo sinh thông qua phương pháp TSTR[3].
• Đánh giá tiềm năng của việc tích hợp chéo nguồn dữ liệu mạng xã hội có sẵn
- cụ thể là bộ dữ liệu ViLexNorm [4] - đóng vai trò nền tảng trong việc làm
phong phú và bao phủ thêm các trường hợp biên (edge cases) cho tập dữ liệu
tin nhắn.
• Thử nghiệm quy trình huấn luyện chưng cất tri thức quy mô nhỏ từ PhoBERT
đến kiến trúc mô hình học sinh gọn nhẹ hơn, cho phép mô hình nhỏ đạt được
độ chính xác phân loại gần tiệm cận mô hình ngôn ngữ giáo viên.
• Phân tích lỗi False Negative/False Positive từ các thử nghiệm để hiểu thêm về
các hạn chế còn tồn đọng của dữ liệu và mô hình hiện tại.
Đóng góp khoa học:
• Bộ dữ liệu Smishing tiếng Việt được chuẩn hóa, đủ lớn và chất lượng cao bao
gồm dữ liệu thực được thu thập và gán nhãn thủ công, kết hợp với dữ liệu tạo
sinh được xây dựng theo quy trình có kiểm soát.
• Thực nghiệm Train on Synthetic Test on Real (TSTR) nhằm chứng minh vai
trò tăng cường của dữ liệu tạo sinh.
• Đánh giá thực nghiệm về Chưng cất Tri thức và đo lường tài nguyên triển khai,
chứng minh khả năng tối ưu hóa tốc độ và bộ nhớ của mô hình học sinh trên thiết bị CPU.
16

Báo cáo của chúng tôi bao gồm 6 chương lớn:
• Chương 1: Giới thiệu
• Chương 2: Cơ sở lý thuyết và các nghiên cứu liên quan
• Chương 3: Xây dựng và phân tích dữ liệu
• Chương 4: Phương pháp và thiết lập thực nghiệm
• Chương 5: Kết quả và phân tích
• Chương 6: Kết luận và hướng phát triển
17

CHƯƠNG 2 CƠ SỞ LÝ THUYẾT & NGHIÊN CỨU LIÊN QUAN
2.1 Tổng quan và định nghĩa bài toán phát hiện tin nhắn lừa đảo
Trong bối cảnh Việt Nam, tin nhắn lừa đảo là một hình thức tấn công kỹ thuật
xã hội, trong đó kẻ gian sử dụng dịch vụ nhắn tin viễn thông (SMS) hoặc các nền tảng
nhắn tin phổ biến (như Zalo, Messenger, Telegram) để giả mạo các tổ chức uy tín
(ngân hàng, cơ quan chính phủ, công ty viễn thông, doanh nghiệp thương mại điện
tử) và gửi tin nhắn cho người dùng. Kẻ gian sử dụng các chiêu trò như thao túng tâm
lý - gây hoang mang và sợ hãi (khóa tài khoản, phạt tiền) hoặc kích thích lòng tham
(trúng thưởng, việc làm dễ dàng với lương cao). Nạn nhân có thể bị khai thác thông
tin cá nhân thông tin tài khoản ngân hàng, mật khẩu, mã OTP hoặc chứng minh nhân
dân khi truy cập vào các liên kết (URL) độc hại. Mức độ nghiêm trọng hơn là tình
trạng chiếm đoạt tài sản trực tiếp bằng yêu cầu chuyển tiền, nạp tiền hoặc cài đặt các
ứng dụng chứa mã độc (.apk) để chiếm quyền kiểm soát thiết bị di động.
Tại Việt Nam, các vụ lừa đảo qua tin nhắn SMS đang phát triển nhanh chóng
và ngày càng tinh vi. Theo báo cáo của Cục An ninh Thông tin (Bộ Thông tin và
Truyền thông), các vụ lừa đảo này có thể được chia thành các nhóm chính sau:
1. Lừa đảo giả mạo thương hiệu (SMS Brandname giả mạo): Kẻ lừa đảo
sử dụng các thiết bị phát sóng di động giả mạo (IMSI Catcher/trạm BTS
giả) để chèn các tin nhắn lừa đảo vào cùng luồng tin nhắn với các tin nhắn
hợp pháp từ các ngân hàng lớn (Vietcombank, BIDV, Techcombank, v.v.)
hoặc các cơ quan chính phủ. Hình thức giả mạo này vô hiệu hoá hoàn toàn
khả năng nhận diện rủi ro lừa đảo thông qua người gửi, khiến nạn nhân mất
cảnh giác và đứng trước nguy cơ bị chiếm đoạt tài sản.
2. Lừa đảo "Việc làm dễ, lương cao" / Cộng tác viên trực tuyến: Tin nhắn
tuyển dụng cung cấp các nhiệm vụ như tương tác với các nội dung trên nền
tảng TikTok, Shopee, Lazada để kiếm hoa hồng, sau đó sẽ dụ dỗ nạn nhân
“nâng hạn mức” với số tiền ngày càng lớn rồi lập tức cắt đứt liên lạc nhằm
chiếm đoạt tài sản.
18

3. Lừa đảo đầu tư/chứng khoán: Các đối tượng sẽ gửi tin nhắn chào mời
nạn nhân tham gia các nhóm đã được thả sẵn “chim mồi”, khoe lợi nhuận
cao, xe sang, nhà đẹp để đánh vào tâm lý ham lợi. Ban đầu, chúng cho phép
đầu tư số tiền nhỏ có lời, sau đó dụ dỗ nạn nhân tăng vốn đầu tư. Khi đạt
mục đích, chúng lập tức chiếm đoạt tiền và cắt liên lạc.
4. Lừa đảo giả mạo cơ quan thực thi pháp luật/viễn thông: Kịch bản
thường bắt đầu bằng các tin nhắn thông báo phạt nguội giao thông, lệnh
khởi tố từ Viện Kiểm sát, hoặc cảnh báo thẻ SIM sẽ bị khóa chiều gọi đi
sau 2 giờ nếu không cập nhật thông tin chuẩn hóa. Thông qua các nội dung
mang tính đe dọa này, kẻ gian lợi dụng tâm lý lo sợ và tạo áp lực thời gian
khẩn cấp để ép buộc nạn nhân truy cập vào các đường link giả mạo hoặc
tải về các ứng dụng độc hại. Từ đó, chúng tiến hành thu thập thông tin định
danh, đánh cắp mã OTP, hoặc thậm chí chiếm quyền điều khiển thiết bị
(trên nền tảng Android) nhằm bòn rút tiền trong tài khoản ngân hàng.
5. Lừa đảo đe doạ đòi nợ khống: Các đối tượng gửi tin nhắn yêu cầu nạn
nhân thanh toán gấp một khoản nợ không tồn tại (có thể mạo danh khoản
vay của chính nạn nhân hoặc người thân, bạn bè, đồng nghiệp). Kịch bản
này là một dạng tấn công tâm lý cực đoan, sử dụng ngôn từ hăm dọa gay
gắt, mang tính chất ép buộc và tạo áp lực thời gian vô cùng gấp rút. Kẻ
gian thường đe dọa sẽ bôi nhọ danh dự trên mạng xã hội, quấy rối cơ quan
làm việc, hoặc cảnh báo về các hành động bạo lực, pháp lý nghiêm trọng.
Dưới tình trạng hoang mang và áp lực tâm lý nặng nề, nạn nhân dễ dàng
đánh mất sự tỉnh táo và chấp nhận chuyển tiền nộp phạt hoặc "trả nợ" để
nhanh chóng đổi lấy sự yên ổn, từ đó sập bẫy chiếm đoạt tài sản.
Đặc điểm chung về cấu trúc ngôn ngữ của tin nhắn lừa đảo
Bất kể là dưới kịch bản nào, các tin nhắn lừa đảo đều mang những đặc điểm
cấu trúc ngôn ngữ chung rất dễ nhận diện.
19

Tư duy khan hiếm và từ ngữ kích động mạnh, tạo cảm giác gấp gáp: Một
đặc trưng cốt lõi của các cuộc tấn công kỹ thuật xã hội (social engineering) là nhắm
vào các phản xạ hành động nhanh của người dùng bằng các tín hiệu khẩn cấp như:
“ngay lập tức”, “trong vòng x giờ”, “tài khoản sẽ bị khóa/vô hiệu hoá”, hay “hết hạn
hôm nay”. Từ góc độ tâm lý học hành vi, Khadka và các cộng sự đã phân tích các
nguyên tắc thuyết phục (principles of persuasion) trong các chiến dịch lừa đảo và chỉ
ra rằng, kẻ tấn công thường xuyên lạm dụng các yếu tố như: tính cấp bách (urgency),
khai thác nỗi sợ hãi (fear appeal), mạo danh uy quyền (authority) và tư duy khan hiếm
(scarcity)[7]. Mặc dù nghiên cứu của họ được thực hiện trên tập dữ liệu lừa đảo qua
email, nhưng các cơ chế thao túng tâm lý nhằm suy giảm tư duy phản biện của đối
tượng vẫn mang tính quy luật và hoàn toàn tương đồng khi áp dụng vào môi trường
tin nhắn SMS.
Sự nhất quán về đặc trưng ngôn ngữ thao túng này cũng được minh chứng rõ
nét qua thực tiễn tại Việt Nam. Khi phân tích các kịch bản tấn công được cảnh báo
trong Cẩm nang nhận diện và phòng chống lừa đảo trực tuyến do Cục An toàn Thông
tin phát hành [12], có thể dễ dàng nhận thấy những điểm chung: việc lạm dụng ngôn
từ đe dọa để ép buộc nạn nhân hành động khẩn cấp chính là chiến thuật cốt lõi của
phần lớn các hình thức lừa đảo hiện nay. Nhìn sang góc độ dữ liệu, thủ đoạn này để
lại những đặc trưng ngôn ngữ rất rõ nét. Các văn bản lừa đảo thường có rất nhiều các
từ khóa ám chỉ giới hạn thời hạn, động từ mệnh lệnh, dấu chấm than và đặc biệt là
các cấu trúc cưỡng chế có điều kiện (ví dụ: “nếu không… thì…”). Đối với bài toán
phân loại bằng các mô hình học máy và đặc biệt là Mô hình ngôn ngữ lớn (ML/LLM),
đây là một cụm đặc trưng có giá trị cao. LLM không chỉ học cách nhận diện tần suất
của các từ vựng đơn lẻ, mà còn có khả năng nắm bắt toàn bộ khuôn khổ ngữ nghĩa
mang tính thao túng: yêu cầu hành động tức thời, triệt tiêu khả năng kiểm tra chéo
thông tin của nạn nhân và nhấn mạnh hậu quả tất yếu nếu sự việc bị chậm trễ.
Cấu trúc văn bản bất thường, sai chính tả có chủ đích, hoặc “làm méo”
chữ viết: Một đặc trưng quan trọng khác là sự bất thường về hình thức và cấu trúc
văn bản. Để né tránh các hệ thống phát hiện dựa trên bộ lọc từ khóa (keyword-based
20

filters) truyền thống, các đối tượng lừa đảo thường chủ động áp dụng các kỹ thuật
ngụy trang văn bản (text obfuscation). Những thủ đoạn này được thể hiện thông qua
việc cố tình viết sai chính tả, loại bỏ dấu, chia tách từ một cách bất thường, chèn ký
tự đặc biệt ngẫu nhiên, thay chữ cái bằng ký tự đồng hình. Sự bất thường trên là một
trong những dấu hiệu cảnh báo lừa đảo bề mặt dễ nhận biết nhất, cùng với liên kết
đáng ngờ. Các đánh giá tổng quan cũng khẳng định lỗi ngữ pháp và chính tả là những
chỉ báo điển hình của một kịch bản lừa đảo[9]. Một nghiên cứu theo dõi chuyển động
mắt cũng cho thấy email phishing có lỗi chính tả sẽ làm giảm đáng kể mức độ đánh
giá tin cậy của người dùng[8].
Riêng với tiếng Việt, các nghiên cứu trong nước cho thấy ngôn ngữ là yếu tố
rất quan trọng: cùng một mô hình phát hiện lừa đảo nhưng ngôn ngữ đầu vào khác
nhau có thể đòi hỏi cách phát hiện khác nhau. Một nghiên cứu về phát hiện phishing
email tiếng Việt [10] đã nêu rõ rằng “mỗi ngôn ngữ cụ thể” có thể dẫn đến “một cách
tiếp cận phát hiện khác nhau”, trong khi một nghiên cứu khác về spam email tiếng
Việt[17] chỉ ra rằng dấu thanh, cấu trúc ngữ pháp khác biệt và sắc thái ngữ cảnh làm
cho bài toán tiếng Việt khó hơn; các mô hình đã tối ưu cho tiếng Anh thường kém
hiệu quả hơn đối với bài toán tiếng Việt. Ví dụ, để qua mặt các bộ lọc từ khóa của
nhà mạng, tin nhắn lừa đảo thường cố tình viết sai chính tả, sử dụng ký tự đặc biệt
thay thế chữ cái (ví dụ: Ng@n h@ng, V1etcombank, |Iên kêt), hoặc trộn lẫn ký tự
Telex/VNI. Vì vậy, trong dữ liệu tiếng Việt, các biến thể như bỏ dấu, sai dấu, văn bản
viết không tự nhiên, hoặc cách ghép từ khác thường nên được xem là tín hiệu có giá
trị cao.
Sự xuất hiện của liên kết đáng ngờ (URL) và tên miền gần giống thương
hiệu thật: Đây là một trong những dấu hiệu mạnh nhất để nhận diện một cuộc tấn
công lừa đảo. Kẻ tấn công thường dùng tên miền chỉ khác tên miền thật một vài ký
tự, thay một chữ bằng kí tự có hình dáng tương tự, hoặc gắn thêm các phần đầu/đuôi
kèm với tên thương hiệu nhằm tạo cảm giác “chính chủ”. Các liên kết thường có tên
miền gần giống thương hiệu thật (ví dụ: vietcomb@nk-cb.com, vcb-digib@nk.xyz)
hoặc sử dụng các dịch vụ rút gọn link (tinylink, bit.ly) nhằm che giấu đích đến thực
21

tế. FBI lưu ý rằng spoofing/phishing có thể chỉ cần đổi một chữ cái, một ký hiệu, hoặc
một con số để đánh lừa người dùng; nghiên cứu về IDN homograph [11] cũng cho
thấy các homoglyph (ký tự Unicode trông giống nhau) là một rủi ro an ninh thường
trực và rất hay được sử dụng trong tấn công lừa đảo.
Hướng dẫn của Đại học Michigan ghi rõ rằng đối tượng dùng các URL rút gọn
để dẫn dụ nạn nhân tới các trang web lừa đảo hoặc vô tình tải mã độc về thiết bị; báo
cáo của tổ chức Anti-Phishing Working Group - APWG trong giai đoạn quý IV năm
2025 cũng ghi nhận sự gia tăng đáng kể của cuộc tấn công điều hướng thông qua dịch
vụ rút gọn liên kết TINYURL.COM để làm mờ đi bản chất độc hại của liên kết. Đây
là một đặc trưng rất mạnh của tin nhắn lừa đảo, tuy vậy, cần lưu ý rằng không chỉ tin
nhắn lừa đảo mới sử dụng tới liên kết rút gọn; xu hướng những năm gần đây của các
nhà mạng viễn thông tại Việt Nam như Viettel hay Mobifone cũng ghi nhận sự xuất
hiện của các liên kết rút gọn điều hướng tới các trang ưu đãi khuyến mãi do nhà mạng
cung cấp. Từ đây vấn đề đã không còn chỉ là “Có chứa link rút gọn hay không?” mà
phải kết hợp song song với nội dung ngữ nghĩa trong chính tin nhắn ấy.
Thách thức gặp phải
Mặc dù các đặc điểm nhận diện đã được phân tích tương đối rõ nét, việc xây
dựng một hệ thống phát hiện tin nhắn lừa đảo ứng dụng học máy trong thực tế lại đối
mặt với hai thách thức cốt lõi.
Thứ nhất là sự khan hiếm trầm trọng của các tập dữ liệu tiếng Việt chất
lượng cao. Do các rào cản nghiêm ngặt về quyền riêng tư và bảo mật thông tin viễn
thông, việc thu thập một tập dữ liệu tin nhắn lừa đảo đủ lớn, đa dạng và mới là vô cùng
khó khăn, dẫn đến tình trạng mất cân bằng dữ liệu nghiêm trọng giữa tin nhắn hợp lệ
và tin nhắn độc hại. Hơn nữa, các chiến dịch lừa đảo vừa có tính lặp lại cao - tức là sẽ
xuất hiện các kịch bản tương tự nhau theo từng đợt, từng khoảng thời gian, khiến cho
số lượng mẫu bị hạn chế; song cũng liên tục thay đổi kịch bản theo thời gian và các sự
kiện xã hội, khiến các tập dữ liệu tĩnh nhanh chóng trở nên lỗi thời. Sự thiếu hụt này
22

đặt ra bài toán cấp thiết về việc phải có các phương pháp tạo lập và tăng cường dữ liệu
nhân tạo để bù đắp, giúp mô hình nhận diện được các biến thể mới mà không bị phụ
thuộc vào một lượng mẫu hạn chế.
Thứ hai là sự phát triển không ngừng của các kỹ thuật ngụy trang văn bản
(text obfuscation). Các phương pháp biểu diễn ngôn ngữ truyền thống dựa trên tần
suất từ vựng (như TF-IDF) hay các thuật toán học máy cổ điển thường gặp khó khăn
khi đối mặt với các văn bản bị "làm méo" một cách có chủ đích. Khi các kỹ thuật nguỵ
trang văn bản được áp dụng, cấu trúc từ vựng bị phá vỡ, khiến các mô hình đếm từ
thông thường bị vô hiệu hóa và mất khả năng nắm bắt cấu trúc phân loại. Điều này đòi
hỏi một hướng tiếp cận sâu hơn vào tầng ngữ nghĩa và ngữ cảnh – nơi các Mô hình
ngôn ngữ lớn (LLM) phát huy thế mạnh vượt trội trong việc hiểu ý đồ được che giấu
bên dưới lớp vỏ bề mặt. Tuy nhiên, kích thước của các LLM lại tạo ra rào cản về tốc
độ xử lý và tài nguyên tính toán, điều này đòi hỏi phải có các cơ chế tối ưu (như chưng
cất tri thức) để đảm bảo tính khả thi khi triển khai vào các hệ thống thời gian thực.
Từ các đặc điểm trên, có thể thấy phát hiện tin nhắn lừa đảo không còn chỉ là
bài toán lọc từ khoá đơn giản, mà là một bài toán phân loại văn bản ngắn trong điều
kiện dữ liệu nhiễu, nhiều biến thể ngôn ngữ và có sự thay đổi liên tục theo thời gian.
Trên cơ sở đó, khoá luận định nghĩa bài toán phát hiện tin nhắn lừa đảo như một bài
toán phân loại văn bản có giám sát, trong đó mỗi tin nhắn đầu vào được gán vào một
trong các lớp nhãn được xác định trước.
Mô hình hoá bài toán và cấu trúc đầu vào/đầu ra
Bài toán phát hiện tin nhắn lừa đảo được chúng tôi định nghĩa dưới dạng bài
toán phân loại văn bản SMS tiếng Việt. Trong phạm vi bộ dữ liệu ViSmish, bài
toán tập trung vào việc học ranh giới giữa hai nhóm tin nhắn: tin nhắn hợp lệ và tin
nhắn lừa đảo. Đây là một ranh giới không đơn giản, vì nhiều tin nhắn lừa đảo cố tình
mô phỏng văn phong của tổ chức thật, trong khi một số tin nhắn hợp lệ cũng có thể
chứa các yếu tố dễ gây nhầm lẫn như liên kết/liên kết rút gọn, mã OTP, cảnh báo bảo
23

mật, khuyến mại hoặc nội dung khẩn cấp. Do đó mô hình cần học các tín hiệu phân
biệt được biểu hiện trực tiếp trong chuỗi văn bản tin nhắn, chẳng hạn như cách diễn
đạt, ngữ cảnh, cấu trúc câu, URL/domain xuất hiện trong nội dung, số điện thoại, mức
độ khẩn cấp, dấu hiệu giả mạo và các dạng obfuscation.
Hình 1 Định nghĩa bài toán nhận diện tin nhắn lừa đảo
Từ các định nghĩa trên, bài toán phát hiện tin nhắn lừa đảo được mô hình hóa
thành bài toán phân loại nhị phân. Cho tập dữ liệu huấn luyện:
D = {(x, y)} với i = 1, 2, ..., n
i i
Đầu vào của bài toán là một tin nhắn SMS tiếng Việt, được ký hiệu
x = {w, w , …, w }
i 1 2 n
Trong đó x là chuỗi văn bản SMS gồm n token hoặc ký tự sau bước tiền xử lý
i
tùy theo mô hình được sử dụng. Tin nhắn có thể ở dạng có dấu, không dấu, viết tắt,
chứa ký hiệu, số điện thoại, liên kết, tên miền, mã giao dịch, OTP hoặc các biến thể
obfuscation như “T1en”, “kho@”, “th0ng ba0”. Trong bộ dữ liệu, ngoài trường nội
dung huấn luyện chính là cột content, mỗi mẫu còn có các metadata hỗ trợ phân tích
và đánh giá dữ liệu. Tuy nhiên, trong bài toán phân loại cốt lõi, đầu vào chính của mô
hình vẫn là nội dung tin nhắn SMS. Các metadata được dùng chủ yếu cho quá trình
24

xây dựng dữ liệu, kiểm tra chất lượng, chia tập dữ liệu, phân tích lỗi và đánh giá theo
từng nhóm.
Đầu ra của bài toán là nhãn phân loại y {0 ; 1}, cho biết tin nhắn thuộc lớp
i
hợp lệ hay lớp lừa đảo. Mục tiêu là học một hàm phân loại: f: X → {0, 1} sao cho với
mỗi tin nhắn SMS mới, mô hình có thể dự đoán chính xác tin nhắn đó là hợp lệ hay
lừa dảo. Với các mô hình huấn luyện, đầu ra cũng có thể được biểu diễn dưới dạng
xác suất như sau:
𝑦ˆ =𝑃(𝑦=1∣𝐱)
Giá trị này thể hiện xác suất tin nhắn đầu vào là tin nhắn lừa đảo. Nếu xác suất
vượt qua một ngưỡng quyết định, mặc định là 0.5 hoặc một ngưỡng được hiệu chỉnh
trên tập validation, mô hình sẽ dự đoán tin nhắn là lừa đảo.
Hệ thống phân lớp nhãn mục tiêu
Để phục vụ cho mô hình phân loại nhị phân trên, các mẫu dữ liệu đầu ra được
quy định chặt chẽ thành hai nhóm nhãn:
• Label 0 - Tin nhắn hợp lệ: Đại diện cho các tin nhắn không mang ý định lừa
đảo. Nhóm này bao gồm tin nhắn từ doanh nghiệp, tổ chức chính thống hoặc
cá nhân thật. Ví dụ bao gồm: tin nhắn ngân hàng thật (OTP, thông báo giao
dịch, cảnh báo bảo mật hợp lệ); tin nhắn viễn thông (khuyến mại gói cước,
thông báo dung lượng, dịch vụ nhà mạng); tin nhắn thương mại điện tử, vận
chuyển, y tế, giáo dục hoặc dịch vụ công; và tin nhắn cá nhân hoặc hội thoại
người với người không có mục đích lừa đảo. Điểm quan trọng là tin nhắn hợp
lệ vẫn có thể chứa các liên kết, số điện thoại, mã OTP hoặc yếu tố khẩn
cấp. Vì vậy, sự xuất hiện của các tín hiệu này không đủ để kết luận một tin
nhắn là lừa đảo. Mô hình cần học sự khác biệt giữa sự khẩn cấp hợp lệ và khẩn
cấp thao túng, giữa domain thật và domain giả mạo, giữa thông báo chính
thống và nội dung giả danh.
25

• Label 1 – Tin nhắn lừa đảo/Smishing: Đại diện cho các tin nhắn SMS có ý
định lừa đảo, dẫn dụ nạn nhân. Các tin nhắn này thường giả mạo tổ chức uy
tín hoặc tạo ra một kịch bản đánh vào tâm lý người nhận nhằm chiếm đoạt
thông tin, tài khoản/tài sản. Trong bộ dữ liệu ViSmish, Label 1 bao gồm nhiều
nhóm nội dung như: Giả mạo ngân hàng; Giả mạo dịch vụ công, BHXH, trợ
cấp; Đòi nợ, đe dọa; Tuyển dụng giả; Cờ bạc, cá độ; Chứng khoán hoặc dẫn
dụ đầu tư; Nội dung nhạy cảm có tính dụ dỗ. Một đặc trưng quan trọng của
nhãn lừa đảo là nhiều tin nhắn sử dụng obfuscation để né bộ lọc từ khóa,
ví dụ thay chữ cái bằng số, ký tự đặc biệt, bỏ dấu, chèn dấu gạch, dấu chấm,
khoảng trắng hoặc biến đổi tên thương hiệu. Vì vậy, bài toán phát hiện
smishing không chỉ là phân loại nội dung độc hại rõ ràng, mà còn là nhận diện
các biến thể cố ý che giấu ý định tấn công.
Tóm lại, bài toán trong nghiên cứu này không chỉ là nhận diện spam thông thường,
mà là phát hiện tin nhắn lừa đảo tiếng Việt trong bối cảnh dữ liệu mất cân bằng, nội
dung ngắn, nhiều văn bản nhiễu và có sự chồng lấn đáng kể giữa tin nhắn hợp lệ và
tin nhắn giả mạo. Mục tiêu cuối cùng là xây dựng mô hình có khả năng phát hiện tốt
lớp Label 1, đồng thời hạn chế nhầm lẫn các tin nhắn hợp lệ có bề mặt giống smishing
thành lừa đảo.
2.2 Các công trình nghiên cứu liên quan
2.2.1 Nghiên cứu sử dụng dữ liệu tạo sinh trong phân loại văn bản
Phương pháp xây dựng bộ dữ liệu SMS dựa trên ba nhóm nghiên cứu nền tảng,
bao gồm phát hiện spam/smishing, đặc trưng cấu trúc tin nhắn, và tăng cường dữ liệu
bằng LLM. Về phát hiện smishing và vai trò của obfuscation, Mishra & Soni trong
công trình DSmishSMS[15]xác nhận rằng leet words và từ viết sai có chủ đích là
heuristic phân biệt smishing với tin nhắn hợp lệ. Một tổ chức uy tín sẽ không bao giờ
sử dụng các kỹ thuật này, đây là căn cứ lý thuyết nền cho toàn bộ Obfuscation
Taxonomy của Label 1. Nghiên cứu về kỹ thuật evasion trong lọc SMS spam [14]
26

phân phân loại các kỹ thuật của kẻ tấn công thành ba nhóm: biến đổi ký tự (character
obfuscation), thao túng từ vựng (lexical manipulation), và gây nhiễu có chủ đích
(crafted perturbations). Nghiên cứu cũng cảnh báo về concept drift khi mô hình thất
bại với các pattern obfuscation mới, nhấn mạnh sự cần thiết của dữ liệu đa dạng theo
mức độ obfuscation. GCC-Spam Framework [16] xây dựng mạng lưới tương đồng
ký tự để nắm bắt đặc trưng chính tả và âm vị học nhằm đối phó với các tấn công
character-obfuscation, cho thấy cần có dữ liệu huấn luyện phân tầng theo mức độ
obfuscation để mô hình đạt được độ bền thực sự. Almeida et al [18] qua hệ thống
đánh giá 83 bài báo cũng xác nhận khoảng trống lớn trong việc cải thiện bộ phân loại
đối với tin nhắn bị obfuscate nặng — đặc biệt trong bối cảnh tiếng Việt với hệ thống
diacritics Unicode phức tạp. Ngoài ra, nghiên cứu về xây dựng tập dữ liệu smishing
đa lớp [23] xác nhận smishing có thể được phân loại theo kịch bản tâm lý mà kẻ tấn
công tạo ra (tham lam, sợ hãi, quyền lực), là cơ sở để áp dụng bốn chiến lược tâm lý
vào tám category smishing trong nghiên cứu này.
Về đặc trưng phong cách của tin nhắn hợp lệ, Sohn, Lee & Rim[13] là công trình
kinh điển đề xuất sử dụng stylistic features (đặc trưng phong cách viết) trong biểu
diễn SMS song song với đặc trưng ngữ nghĩa, đạt kết quả tốt nhất với 250 đặc trưng
từ vựng và phong cách bất kể ngôn ngữ — đây là nền tảng lý thuyết cho Formality
Taxonomy của Label 0. Hosseinpour & Shakibian [19] trích xuất đồng thời ba loại
đặc trưng từ SMS bao gồm thống kê, ngữ pháp, và cấu trúc mạng phức tạp, cho thấy
cấu trúc của tin nhắn (không chỉ từ vựng) là đặc trưng phân loại mạnh, đóng góp trực
tiếp cho việc phân loại tin nhắn hợp lệ theo độ cứng nhắc của template. Jain et al. [24]
xác nhận phân tích URL (tên miền, TLD, brand name trong domain) là đặc trưng
mạnh phân biệt smishing với ham, là cơ sở lý thuyết cho các pattern domain hợp lệ
(.vn, .gov.vn) so với domain giả mạo (.vip, .top, .icu) trong cả hai taxonomy. Điểm
mới của nghiên cứu này so với các công trình đi trước là đề xuất label-aware structural
taxonomy — phân tầng đặc trưng bên trong từng nhãn — thay vì dùng một tập feature
chung cho toàn bộ corpus.
27

2.2.2 Nghiên cứu đánh giá dữ liệu tạo sinh bằng TSTR/domain gap
TSTR hay Train on Synthetic, Test on Real là phương pháp luận kiểm thử
lần đầu được đề xuất trong “Measuring the quality of synthetic data for use in
competitions” của tác giả J.Jordon năm 2018[3], nổi bật nhờ tính thực dụng - đánh
giá dữ liệu tổng hợp qua khả năng ứng dụng thực tế thay vì các chỉ số thống kê trừu
tượng.Mục tiêu cốt lõi của thí nghiệm là để đánh giá liệu dữ liệu SMS tạo sinh có
mang lại giá trị thực tế cho bài toán phân loại tin nhắn hợp lệ và tin nhắn smishing
hay không. Trọng tâm của thí nghiệm không chỉ là kiểm tra dữ liệu tạo sinh có giống
dữ liệu thực về mặt bề mặt hay không, mà là kiểm tra liệu dữ liệu này có giúp mô
hình học được ranh giới phân loại hữu ích trên dữ liệu thực hay không.
Đối với bộ dữ liệu của khóa luận nhóm chúng tôi, dữ liệu thực bị mất cân bằng
mạnh, đặc biệt là số lượng hạn chế của các mẫu thuộc nhãn 1, vì vậy việc đánh giá
cần tập trung vào các chỉ số phản ánh hiệu quả trên lớp thiểu số thay vì chỉ dựa vào
accuracy.
28

CHƯƠNG 3 XÂY DỰNG BỘ DỮ LIỆU
3.1 Quy trình thu thập, gán nhãn dữ liệu thực
Quá trình thu thập và xử lý gán nhãn cho phần dữ liệu tin nhắn thực có thể chia
làm 3 phần chính như sơ đồ dưới đây.
Hình 2 Quy trình thu thập dữ liệu thực và gán nhãn
3.1.1 Thu thập thủ công từ các nguồn công khai trên mạng
Giai đoạn thu thập đầu tiên tập trung vào việc thu thập các tin nhắn lừa đảo từ
các hình ảnh được cung cấp bởi các nạn nhân trong các hội nhóm mạng xã hội; các
bài viết/bài báo cảnh báo về thủ đoạn lừa đảo. Để thu thập loại dữ liệu này, nhóm
nghiên cứu đã chủ động theo dõi các diễn đàn an ninh mạng tại Việt Nam và các cộng
đồng “chống lừa đảo” nhằm xác định các kịch bản lừa đảo đang thịnh hành. Chúng
tôi tiến hành nhập lại thủ công nội dung SMS từ các hình ảnh này. Mặc dù tốn nhiều
thời gian, phương pháp thủ công này là cần thiết để bảo toàn chính xác các sắc thái
ngôn ngữ, chẳng hạn như “teencode” (tiếng lóng), các hình thức làm nhiễu bằng ký
tự đặc biệt và các URL độc hại, vốn thường không được các công cụ Nhận dạng Ký
29

tự Quang học (OCR) tiêu chuẩn diễn giải chính xác. Quy trình này đã tạo ra một tập
dữ liệu chất lượng cao gồm các dấu hiệu smishing riêng biệt, chủ yếu nhắm vào lĩnh
vực ngân hàng và thương mại điện tử.
Tuy nhiên, điểm hạn chế của phương pháp này là số lượng mẩu lừa đảo mà
chúng tôi thu thập được là rất ít. Điều này một phần xuất phát từ việc các bài cảnh
báo thường có xu hướng dùng lại cùng một vài hình ảnh minh họa giống nhau. Mặt
khác, nguyên nhân cốt lõi nằm ở việc quá trình này phụ thuộc hoàn toàn vào mức độ
sẵn sàng chia sẻ thông tin của người bị hại, dẫn đến tình trạng thiếu hụt báo cáo
(underreporting). Trên thực tế, việc thu thập vấp phải một rào cản tâm lý rất lớn:
nhiều nạn nhân mang tâm lý mặc cảm, xấu hổ, e ngại bị cộng đồng phán xét (victim-
blaming), hoặc đơn giản là nhận thấy việc công khai không giúp họ thu hồi được tài
sản nên đã lựa chọn giữ im lặng. Sự thiên lệch báo cáo mang tính con người này khiến
cho lượng dữ liệu thô thu thập được không phản ánh trọn vẹn quy mô và sự đa dạng
thực tế của các chiến dịch lừa đảo.
3.1.2 Thu thập dữ liệu thực tế thông qua thiết bị di động
Để đảm bảo bộ dữ liệu phản ánh đúng mức độ nhiễu và sự đa dạng của môi
trường di động thực tế, giai đoạn thứ hai bao gồm việc thu thập dữ liệu SMS trong
đời thực, bao gồm tin nhắn người-người, mã xác thực một lần (OTP) và tin nhắn
thông báo/quảng cáo từ nhà mạng. Với mục đích này, chúng tôi sử dụng SMS
Backup & Restore, một ứng dụng Android của bên thứ ba được sử dụng rộng rãi và
phát hành trên Google Play Store. Với sự đồng ý rõ ràng của các thành viên trong
nhóm nghiên cứu và các tình nguyện viên tham gia, ứng dụng này được dùng để xuất
kho tin nhắn cục bộ từ điện thoại của các cá nhân tham gia sang định dạng XML có
cấu trúc. Cách tiếp cận này cho phép chúng tôi trích xuất hiệu quả nội dung tin nhắn,
dấu thời gian và thông tin người gửi mà không cần phát triển một trình thu thập dữ
liệu tùy chỉnh, qua đó tinh giản quy trình thu thập dữ liệu.
Sau khi tổng hợp, làm sạch và chuẩn hóa dữ liệu từ cả hai nguồn, bộ dữ liệu
hợp nhất cuối cùng bao gồm tổng cộng 2.567 mẫu duy nhất.
30

3.1.3 Quy trình gán nhãn dữ liệu thực
Sau khi hoàn tất quá trình thu thập, làm sạch và chuẩn hóa dữ liệu, nhóm
nghiên cứu tiến hành gán nhãn cho bộ dữ liệu thực theo phương pháp gán nhãn cộng
tác dựa trên đồng thuận nhóm (collaborative annotation with consensus-based
decision). Bộ dữ liệu được gán nhãn theo bài toán phân loại nhị phân, trong đó mỗi
tin nhắn được gán vào một trong hai lớp: tin nhắn không lừa đảo và tin nhắn lừa đảo.
Khác với quy trình gán nhãn nhiều người độc lập thường được sử dụng trong
các bộ dữ liệu lớn, nhóm nghiên cứu không thực hiện pha gán nhãn thử, không chia
dữ liệu cho từng người gán độc lập và không tính các chỉ số đồng thuận như Cohen’s
Kappa hoặc Fleiss’ Kappa. Thay vào đó, toàn bộ quá trình gán nhãn được thực hiện
thông qua các phiên họp nhóm gồm 5 người, đều là các sinh viên thuộc ngành CNTT
theo học tại UIT. Trong mỗi phiên gán nhãn, một thành viên đại diện trình chiếu lần
lượt từng mẫu tin nhắn, trong khi các thành viên còn lại cùng quan sát, thảo luận và
đưa ra nhận định. Nhãn cuối cùng của mỗi mẫu được xác định sau khi cả nhóm thống
nhất, sau đó được thành viên đại diện ghi nhận vào bộ dữ liệu.
Cách tiếp cận này được lựa chọn dựa trên một số đặc điểm thực tế của bộ dữ
liệu và bài toán nghiên cứu. Thứ nhất, quy mô bộ dữ liệu sau khi hợp nhất chỉ gồm
2.567 bản ghi duy nhất, cho phép nhóm có thể cùng rà soát từng mẫu trong các phiên
gán nhãn tập trung. Thứ hai, bài toán trong phạm vi khoá luận là phân loại nhị phân,
không phải phân loại đa lớp với nhiều ranh giới nhãn phức tạp. Do đó, đối với phần
lớn mẫu dữ liệu, việc xác định tin nhắn có mang dấu hiệu lừa đảo hay không có thể
được thực hiện tương đối rõ ràng khi đối chiếu với ngữ cảnh và các dấu hiệu nhận
biết đã thống nhất. Thứ ba, nhóm đã nhận thức trước tình trạng mất cân bằng nhãn
nghiêm trọng trong dữ liệu thực, đặc biệt là số lượng tin nhắn lừa đảo thực tế thu thập
được rất hạn chế. Sau quá trình gán nhãn, bộ dữ liệu chỉ có 246 mẫu thuộc lớp lừa
đảo, cho thấy việc rà soát cẩn thận từng mẫu là cần thiết nhằm hạn chế bỏ sót các
trường hợp dương tính.
31

Trong quá trình gán nhãn, nhóm sử dụng các tiêu chí nhận diện tin nhắn lừa
đảo dựa trên nội dung, mục đích giao tiếp và các dấu hiệu hành vi thường gặp. Một
tin nhắn được xem là lừa đảo nếu nội dung có mục đích dụ dỗ, thao túng hoặc đánh
lừa người nhận thực hiện một hành động có nguy cơ gây hại, chẳng hạn như truy cập
liên kết không đáng tin cậy, phát sinh vấn đề liên quan tới tài khoản ngân hàng, cung
cấp thông tin cá nhân, chuyển tiền, liên hệ với số điện thoại lạ, tải ứng dụng không rõ
nguồn gốc hoặc làm theo hướng dẫn giả mạo tổ chức uy tín. Ngược lại, các tin nhắn
không thể hiện mục đích lừa đảo rõ ràng, bao gồm tin nhắn cá nhân thông thường, tin
nhắn OTP hợp lệ, thông báo dịch vụ, quảng cáo hoặc chăm sóc khách hàng không
chứa dấu hiệu giả mạo, được gán vào lớp không lừa đảo.
Đối với các trường hợp mơ hồ, nhóm không đưa ra quyết định dựa trên một
dấu hiệu đơn lẻ mà xem xét tổng hợp nhiều yếu tố, bao gồm ngữ cảnh nội dung, người
gửi, cách diễn đạt, sự xuất hiện của đường dẫn hoặc số điện thoại, mức độ khẩn cấp
trong thông điệp, yêu cầu cung cấp thông tin nhạy cảm và khả năng giả mạo một tổ
chức đáng tin cậy. Các mẫu gây tranh luận được thảo luận trực tiếp trong nhóm cho
đến khi đạt được sự thống nhất về nhãn cuối cùng. Trong trường hợp nội dung không
đủ bằng chứng để kết luận là lừa đảo, nhóm ưu tiên gán nhãn theo hướng thận trọng
nhằm tránh mở rộng quá mức định nghĩa của lớp lừa đảo.
Quy trình gán nhãn cộng tác này giúp tận dụng nhận định của nhiều thành viên
trong nhóm, đặc biệt đối với các mẫu có yếu tố ngôn ngữ bất thường, viết tắt, thiếu
dấu, chứa ký tự đặc biệt hoặc có dấu hiệu né tránh bộ lọc. Việc cùng xem xét từng
mẫu cũng giúp giảm nguy cơ sai lệch do nhận định cá nhân và đảm bảo các quyết
định nhãn được áp dụng nhất quán trong toàn bộ bộ dữ liệu.
Tuy nhiên, quy trình này cũng có những hạn chế cần được thừa nhận. Do các
thành viên không gán nhãn độc lập trên cùng một tập mẫu, khoá luận không thể báo
cáo các độ đo định lượng về mức độ đồng thuận giữa những người gán nhãn như
Cohen’s Kappa hoặc Fleiss’ Kappa. Ngoài ra, hình thức thảo luận nhóm có thể chịu
ảnh hưởng bởi sự đồng thuận xã hội hoặc ý kiến của thành viên có lập luận nổi trội
32

hơn. Vì vậy, bộ dữ liệu trong khoá luận nên được hiểu là bộ dữ liệu đã được thẩm
định theo cơ chế đồng thuận nhóm, thay vì một bộ dữ liệu được gán nhãn độc lập và
đánh giá đồng thuận theo quy trình gán nhãn tiêu chuẩn. Đây là một giới hạn của
nghiên cứu, nhưng phản ánh trung thực quy trình xây dựng dữ liệu đã được thực hiện
trong bối cảnh quy mô dữ liệu nhỏ, dữ liệu lừa đảo khan hiếm và nguồn lực gán nhãn
có hạn.
3.1.4 Phân tích sơ bộ dữ liệu thực
Bộ dữ liệu thực bao gồm 2.567 mẫu, trong đó Label 0 chiếm 2.321 mẫu và
Label 1 chiếm 246 mẫu, phản ánh mức mất cân bằng nhãn đáng kể trong thực tế.
Label 0 - Legitimate SMS có cấu trúc phân phối category tập trung rõ rệt.
Nhóm viễn thông chiếm tỷ trọng lớn nhất với 1.060 mẫu (45,67%), chủ yếu đến từ
Viettel và VinaPhone. Nhóm "Khác" gồm các tin nhắn hợp lệ không phân loại được
vào category cụ thể đứng thứ hai với 507 mẫu (21,84%). Tiếp theo là tin nhắn cá nhân
& OTP với 301 mẫu (12,97%), dịch vụ công thật 170 mẫu (7,32%), quảng cáo hợp
lệ 136 mẫu (5,86%), và ngân hàng thật 126 mẫu (5,43%). Các nhóm vận chuyển (18
mẫu, 0,78%), dịch vụ y tế (2 mẫu) và thương mại điện tử (1 mẫu) gần như vắng bóng
trong ground truth, phản ánh thực tế là các dịch vụ này chủ yếu giao tiếp qua ứng
dụng riêng hoặc cuộc gọi trực tiếp thay vì tin nhắn SMS.
Về phía sender_type trong Label 0, brandname chiếm đa số với 1.754 mẫu,
has_URL có tỷ lệ đạt 53,71%, has_phone_number có tỷ lệ 41,51% và độ dài nội dung
trung bình 235,37 ký tự. Shortcode có 462 mẫu với tỷ lệ has_URL 40,04% và độ dài
tương đương (237,80 ký tự trung bình). Personal_number chỉ có 105 mẫu, tỷ lệ
has_URL và has_phone_number đều rất thấp (dưới 5%), với độ dài nội dung ngắn
hơn rõ rệt (trung bình 81,37 ký tự). Toàn bộ Label 0 có tỷ lệ has_URL là 48,73% và
tỷ lệ has_phone_number là 41,19%.
Label 1 - Smishing SMS gồm 246 mẫu thu thập thực tế, phân bố theo 8
category. Giả mạo ngân hàng chiếm tỷ trọng cao nhất với 65 mẫu (26,42%), tiếp theo
33

là cờ bạc/betting với 53 mẫu (21,54%). Nhóm "Khác" chứa 46 mẫu (18,70%) là các
tin nhắn smishing chưa phân loại được vào 8 category chính. Tuyển dụng giả có 27
mẫu (10,98%), dịch vụ công giả 16 mẫu (6,50%), BHXH/trợ cấp giả 15 mẫu (6,10%),
đòi nợ/đe dọa 12 mẫu (4,88%), nội dung nhạy cảm 10 mẫu (4,07%), và crypto/đầu tư
giả chỉ có 2 mẫu (0,81%).
Về sender_type trong Label 1, personal_number chiếm đa số với 168 mẫu,
brandname có 74 mẫu, shortcode chỉ có 4 mẫu phản ánh đúng thực tế rằng phần lớn
smishing được phát tán từ số điện thoại cá nhân của kẻ lừa đảo. Tỷ lệ has_URL trong
Label 1 đạt 73,58% (181/246 mẫu) và tỷ lệ has_phone_number là 24,39%, cho thấy
rằng link giả là công cụ chính của smishing.
3.2 Quy trình xây dựng bộ dữ liệu tạo sinh
3.2.1 Nền tảng xây dựng dữ liệu tạo sinh
Để xây dựng bộ dữ liệu tạo sinh đa dạng và có kiểm soát, nghiên cứu này thiết lập hai hệ phân loại (taxonomy) song song đóng vai trò làm các **tham số điều khiển trong prompt tạo sinh**, thay vì là thuộc tính metadata cuối cùng của tập dữ liệu. Cụ thể, chúng tôi đề xuất 5 mức độ trang trọng (formality level 0–4) cho lớp hợp lệ (Label 0) và thang đo độ xáo trộn/ngụy trang văn bản (obfuscation level 0–5) cho lớp lừa đảo (Label 1) để hướng dẫn các mô hình ngôn ngữ lớn (LLM) tạo ra các biến thể văn bản tiếng Việt phù hợp với ngữ cảnh nhắn tin thực tế.

Formality Taxonomy cho Label 0 mô tả tin nhắn hợp lệ qua 5 mức độ formal.
Đầu tiên là Level 0 (template cứng nhắc hoàn toàn) của doanh nghiệp lớn như ngân
hàng, viễn thông hay có cấu trúc entropy thấp, có thể phân tích bằng regex. Level 1
(template mềm) của thương mại điện tử và logistics, thường có cấu trúc cố định nhưng
trường dữ liệu động biến đổi. Level 2 (bán formal) của doanh nghiệp vừa và nhỏ có
thể có lỗi nhỏ hoặc bỏ dấu một phần, Level 3 (thân thiện) của phòng khám nhỏ hay
cửa hàng cá nhân. Level 4 (hoàn toàn cá nhân) không có cấu trúc định danh. Điều
quan trọng cần phân biệt: bỏ dấu ở Level 4 là đặc trưng tự nhiên của nhắn tin cá nhân,
hoàn toàn khác với obfuscation có chủ đích của smishing. Mỗi category trong Label
34

0 được ánh xạ sang một ngưỡng formal level tương ứng. Ví dụ, ngân hàng thật và
viễn thông nằm trong khoảng Level 0-1, trong khi tin nhắn cá nhân & OTP trải rộng
toàn bộ trường hợp từ Level 0 đến 4.

Obfuscation Taxonomy cho Label 1 xây dựng thang severity 6 bậc liên tục
ánh xạ trực tiếp lên ba nhóm kỹ thuật evasion: Level 0 là smishing formal không
obfuscation, trông sạch như ham và đặc biệt nguy hiểm; Level 1 dùng leet nhẹ thay
1-2 ký tự nguyên âm bằng số; Level 2 dùng leet nặng với nhiều ký tự đặc biệt, đặc
trưng của scam BHXH; Level 3 chèn dấu chấm/gạch ngang giữa từng ký tự, phá vỡ
tokenizer; Level 4 hỗn hợp ký tự đặc biệt gần như không đọc được với mắt thường;
và Level 5 là nhiễu cực độ kết hợp biến dạng Unicode diacritics tiếng Việt, khoảng
trống mà hầu hết classifier hiện tại đều thất bại theo xác nhận của Almeida et al. Mỗi
category smishing được ánh xạ sang ngưỡng obfuscation phù hợp với thực tế: nội
dung nhạy cảm ở Level 3-5, giả mạo ngân hàng ở Level 1-2, đòi nợ ở Level 0-1.

Các mức phân loại này được đưa vào các Prompt tạo sinh nhằm kiểm soát sự đa dạng của văn bản được sinh ra bởi LLM. Cần lưu ý rằng các taxonomy điều hướng prompt này khác biệt với Schema Metadata v2 cuối cùng của bộ dữ liệu (được mô tả chi tiết ở phần sau).
LLM không ghi nhớ dữ liệu thực mà học phân phối xác suất của ngôn ngữ.
Khi nhận prompt, model khởi tạo ngữ cảnh và tại mỗi bước chọn token tiếp theo từ
không gian xác suất được điều chỉnh bởi tham số temperature. Temperature cao mang
lại đa dạng hơn nhưng dễ sinh nội dung sai format hoặc ảo giác về thương hiệu;
temperature thấp đảm bảo nhất quán format nhưng làm giảm diversity của dataset.
Nguyên tắc cốt lõi là một prompt được thiết kế tốt sẽ thu hẹp không gian tìm kiếm
của model, kiểm soát output mà không đánh đổi diversity.
Ba tiêu chí chất lượng được định nghĩa cho dữ liệu tổng hợp. Fidelity (độ
trung thực) yêu cầu dữ liệu sinh ra phải giống tin nhắn thực tế về format, domain và
tên thương hiệu, tránh trường hợp mô hình không học được ranh giới thực với nhãn
35

đối lập. Diversity (đa dạng) yêu cầu bao phủ đủ các category, sub-type và mức độ
trong taxonomy. Nếu thiếu tiêu chí này, mô hình sẽ overfit vào template cứng và thất
bại với các biến thể thực tế. Novelty (tính mới) yêu cầu không trùng lặp với dữ liệu
thực hoặc với nhau, giúp dataset không bị inflate giả tạo mà không tăng thêm thông
tin học tập. Cần lưu ý rằng diversity có ý nghĩa khác nhau ở hai nhãn: với Label 0,
diversity là sự đa dạng về sender type × category × formal level; với Label 1, là đa
dạng về category × psychology × obfuscation level.
Thực nghiệm so sánh cho thấy few-shot learning (cung cấp ví dụ thực trong
prompt) hiệu quả rõ rệt hơn zero-shot. Trong chế độ zero-shot, mô hình sinh Label 0
bằng tiếng Anh sai format ngân hàng Việt Nam, còn Label 1 thì quá sạch, không có
obfuscation, sử dụng domain thật, không phản ánh smishing thực tế. Ngược lại, khi
có few-shot từ dữ liệu thực, mô hình sinh đúng format thương hiệu, đúng mức độ
obfuscation và đúng chiến lược tâm lý đặc trưng của từng loại smishing.
Hai thách thức đặc thù cần xử lý. Với Label 0, LLM có xu hướng sinh văn bản
quá chuẩn mực. Trong thực tế, tin nhắn của doanh nghiệp vừa và nhỏ (Formal Level
2, 3) thường có lỗi nhỏ tự nhiên mà LLM sẽ "sửa" nếu không có few-shot phù hợp,
dẫn đến mô hình học boundary sai và false positive cao. Ngoài ra, mô hình cần phân
biệt urgency hợp lệ (OTP trong 5 phút, thông tin cụ thể, domain thật) với urgency
thao túng (mất tài sản, bị khóa vĩnh viễn, domain giả). Với Label 1, safety filter của
LLM có thể từ chối tạo nội dung có vẻ harmful, đòi hỏi safety framing hợp lý trong
prompt; đồng thời obfuscation Level 4, 5 yêu cầu temperature cao hơn để sinh đúng
độ nhiễu đặc trưng.
3.2.2 Kiến trúc mô hình tăng cường dữ liệu bằng LLM
Kiến trúc prompt được xây dựng trên ba trụ cột nghiên cứu có nền tảng học
thuật rõ ràng. White et al. (2023)[21] hệ thống hóa các kỹ thuật prompt thành các
pattern tương tự software design patterns, bao gồm Persona Pattern, Output
Customization Pattern, Template Pattern, và Context Control Pattern — bốn layer
trong kiến trúc của nghiên cứu này tương ứng trực tiếp với bốn pattern đó, với đóng
36

góp là tích hợp chúng thành một pipeline tuần tự thay vì các đơn vị độc lập. Brown
et al. [20] xác lập cơ chế in-context learning: LLM có thể thực hiện task mới chỉ từ
vài ví dụ trong prompt mà không cần fine-tuning, trong đó mỗi ví dụ pipe-delimited
hoàn chỉnh đóng vai trò là context–completion pair. Long et al. [22] xác nhận rằng
thách thức lớn nhất khi dùng LLM sinh dữ liệu là đảm bảo diversity và đề xuất
conditional prompting — truyền tập condition-value pairs vào prompt để kiểm soát
thuộc tính dữ liệu sinh ra — là chiến lược chủ đạo.
Layer 1 - Persona & Task Framing: gán cho LLM một vai trò domain expert
cụ thể để định hướng góc nhìn output. Với Label 0, hệ thống prompt xác lập vai trò
chuyên gia tạo dữ liệu huấn luyện cho mô hình phân loại SMS hợp lệ tại Việt Nam.
Với Label 1, cần thêm safety framing: LLM được đặt trong vai chuyên gia an ninh
mạng xây dựng dataset phát hiện smishing phục vụ nghiên cứu bảo mật hợp pháp.
Mục đích là để vượt qua safety filter của mô hình mà không làm mất tính hợp pháp
của yêu cầu.
Layer 2 - Task Specification: áp dụng kỹ thuật "Biến–Hằng" theo nguyên lý
conditional prompting: các tham số tạo ra diversity (category, danh sách brand,
formality/obfuscation, batch size) là biến thay đổi mỗi batch; các tham số đảm bảo
consistency (format output pipe-delimited, cấu trúc cột) là hằng số cố định. Đáng chú
ý, danh sách brand được truyền vào để model tự chọn ngẫu nhiên cho từng dòng thay
vì chọn một brand cố định, tránh hiện tượng cả batch 40 mẫu cùng một thương hiệu.
Layer 3 - Few-Shot Demonstrations: cung cấp 2–5 ví dụ pipe-delimited hoàn
chỉnh theo nguyên tắc Coverage Matrix: mỗi ví dụ thể hiện một tổ hợp khác nhau của
sender_type × psychology/formality × obfuscation/formal level. Ví dụ phải luôn có
đủ 5 cột để model học cách điền đúng metadata, nếu thiếu completion thì model
không có cơ sở học cách điền các trường phụ. Định dạng pipe-delimited được chọn
thay vì CSV dấu phẩy bởi vì nội dung tin nhắn thường chứa dấu phẩy, khiến LLM
hay bỏ sót việc wrap quotes đúng RFC 4180, dẫn đến lỗi parse; pipe không xuất hiện
trong nội dung tin nhắn tự nhiên và không cần escape.
37

Layer 4 - Negative Instructions: liệt kê tường minh các ràng buộc output và
những gì model không được làm, nhằm khắc phục các lỗi đặc thù của LLM khi sinh
structured data. Với Label 1, các ràng buộc bao gồm không có dòng tiêu đề, không
có dấu nháy đơn trong trường sender_type, không lặp lại cùng một domain trong
batch, không dùng brand name thật trong URL. Với Label 0, các ràng buộc bao gồm
chỉ dùng domain thật (.vn, .com.vn), không thêm urgency đe dọa, không obfuscate,
không dùng placeholder literal như [TÊN] hay XXXXXX.
3.2.3 Pipeline sinh dữ liệu và đánh giá chất lượng
Hình 3 Quy trình tăng cường dữ liệu bằng LLM
Pipeline tổng thể bắt đầu bằng việc tải ground truth và đánh dấu toàn bộ
content đã có để phục vụ deduplication. Trong mỗi vòng lặp sinh batch, hệ thống
chọn ngẫu nhiên category, tập hợp danh sách brand tương ứng, xác định taxonomy
theo category đó, xây dựng prompt 4-layer, gọi LLM API (Gemini), sau đó lần lượt
qua parser pipe-delimited, soft validation, hard validation, kiểm tra trùng lặp, và ghi
vào file CSV. Chiến lược parse "last 4 parts" được áp dụng: tách dòng bằng |, lấy 4
phần tử cuối làm metadata (label, has_url, has_phone, sender_type) và ghép phần còn
lại thành content, đảm bảo xử lý đúng kể cả khi content chứa ký tự. Cuối cùng là sử
dụng script để tự động gán taxonomy cho toàn bộ dữ liệu, phục vụ việc phân tích dữ
liệu và phân tích kết quả thực nghiệm.
38

Đánh giá chất lượng được thực hiện ở ba tầng. Format validation tự động kiểm
tra đủ 5 cột, giá trị label và binary field đúng, sender_type thuộc tập hợp hợp lệ, độ
dài nội dung trong khoảng 20 - 600 ký tự, tính nhất quán giữa has_url và sự có mặt
của URL trong content, và đối với Label 0 là không có domain giả hay placeholder
literal. Content quality được thực hiện thủ công trên 10% mỗi batch, kiểm tra tính
giống thực tế, đúng mức obfuscation/formal level yêu cầu, chiến lược tâm lý thể hiện
rõ, và không có nội dung lặp lại. Distribution check đảm bảo phân phối metadata sinh
ra gần với phân phối mục tiêu: Label 1 hướng đến ~50% personal_number, ~75%
has_url; Label 0 hướng đến ~70% brandname, ~40% has_url (tỷ lệ URL thấp hơn
ground truth để bù lại sự mất cân bằng category).
3.3 Quy trình cải biên văn bản thô và đánh giá ở giai đoạn Phase 1
3.3.1 Các biện pháp xử lý và làm sạch đã áp dụng
Khi quan sát lại dữ liệu tạo sinh, nhóm chúng tôi nhận thấy các mẫu nhãn 0 đa
số đều mang cấu trúc tiêu chuẩn, trong khi các nhãn 1 có 53% mẫu thuộc obfuscation
level 2. Tổng quát bộ dữ liệu tạo sinh hiện tại, các mẫu nhãn 0 đang quá formal, trong
khi các mẫu nhãn 1 thì chủ yếu là leet. Mô hình có thể đã học được đặc trưng này và
dự đoán những tin nhắn có dấu hiệu leet đều là smishing. Biện pháp khắc phục của
nhóm chúng tôi là giảm số lượng các mẫu có obfuscation level 2 bằng cách sử dụng
Gemini để sửa chính tả nội dung các mẫu đó, biến các mẫu leet thành các mẫu level
0. Tổng cộng đã có 2261 mẫu tạo sinh obfuscation level 2 được chỉnh sửa.
Obfuscation level Số lượng mẫu tạo sinh Số lượng mẫu tạo sinh sau
trước chỉnh sửa chỉnh sửa
Level 0 638 2899
Level 1 651 651
Level 2 2647 386
Level 3 670 670
39

Level 4 225 225
Level 5 139 139
Tổng 4970 4970
Bảng 1: Thống kê phân phối dữ liệu cho từng nhãn obfuscation level của dữ liệu
tạo sinh
Mặt khác, nhóm cũng thay thế một phần mẫu tạo sinh nhãn 0 bằng dữ liệu
từ bộ dữ liệu công khai ViLexNorm. Đây là bộ dữ liệu hội thoại Tiếng Việt được
thu thập từ các mạng xã hội Việt Nam (Facebook, TikTok,...), không phải là tin nhắn
SMS 100%. Ý nghĩa của việc bổ sung dữ liệu từ VilexNorm là để giảm phụ thuộc
vào dữ liệu tạo sinh nhãn 0, bổ sung thêm miền hội thoại peer-to-peer (P2P), và tạo
một số lượng mẫu gần ranh giới quyết định (near-boundary samples) có kiểm soát.
Dữ liệu real nhãn 0 hiện tại đang có 2321 mẫu so với 3000 mẫu tạo sinh, nên chúng
tôi đặt mục tiêu thay thế 800-1000 mẫu tạo sinh bằng VilexNorm, trong đó có khoảng
500 mẫu near-boundary. Các tác giả chia dữ liệu VilexNorm thành ba tập train, dev,
test, nhưng thay vì lấy phần trăm tỉ lệ từ ba tập dữ liệu thì chúng tôi gộp lại và lọc
theo quy tắc. Chúng tôi thống nhất các tiêu chí đánh giá dữ liệu VilexNorm sạch như
sau: độ dài từ 10-200 ký tự; không có URL không xác minh hoặc SDT; nội dung tin
nhắn không chứa các từ CTA như “ngay, lập tức, khẩn trương”; không chứa nội dung
quảng cáo, tuyển dụng, lừa đảo, cờ bạc, mượn tiền; không chứa các từ ngữ nhạy cảm,
văng tục. Các boundary sample có thể chứa nội dung đề cập về link, tuyển dụng, vay
tiền như chủ đề bàn luận. Một thành viên sẽ đại diện nhóm thu thập đủ số lượng mẫu.
Cuối cùng, nhóm đã thay thế được 1001 mẫu tạo sinh nhãn 0 ngẫu nhiên bằng dữ liệu
VilexNorm, trong đó có 501 mẫu là các boundary sample.
Dữ liệu tạo sinh nhãn 1 cũng được bổ sung các boundary sample. Trong
bước này, nhóm không tìm được các bộ dữ liệu công khai liên quan nên quyết định
sử dụng LLM tạo sinh. Khác với đặc điểm của boundary sample nhãn 0, boundary
sample nhãn 1 sẽ có cấu trúc formal - obfuscation level 0, chỉ một số lượng nhỏ có
URL, không sử dụng các từ và thêm các kịch bản hội thoại P2P để cân bằng với nhãn
40

0 đã được bổ sung. Nhóm sử dụng Gemini để sinh 700 mẫu dữ liệu. Qua kiểm định
thủ công thì có 653 mẫu đạt yêu cầu được thay thế vào tập dữ liệu tạo sinh nhãn 1.
Hình 4 Các bước cải thiện bộ dữ liệu
Khi quan sát dữ liệu tạo sinh nhãn 1, nhóm nhận thấy mỗi kịch bản đều có các
cấu trúc câu lặp lại quá nhiều, làm giảm tính đa dạng dữ liệu. Vì thế, nhóm sẽ thực
hiện paraphrase lại dữ liệu sử dụng LLM. Chúng tôi không dùng Gemini nữa mà thử
mô hình khác là Mistral AI. Sau đó, chúng tôi đưa các dữ liệu tạo sinh nhãn 1 vào mô
hình đã được thiết kế prompt để paraphrase dữ liệu gồm 3 layer:
Layer 1: Thiết lập role cho mô hình: “Bạn là chuyên gia phân tích tin nhắn lừa
đảo.”, đưa cho mô hình một vai trò cụ thể và định hình “góc nhìn” của mô hình đối
với nhiệm vụ.
Layer 2: Thiết kế nội dung nhiệm vụ. Yêu cầu tổng quát là paraphrase lại nội
dung tin nhắn theo quy tắc về nội dung, ngôn ngữ, từ ngữ, văn phong. Quan trọng
hơn, mỗi mẫu thuộc danh mục khác nhau sẽ sử dụng prompt phù hợp cho danh mục
với các quy tắc khác nhau.
41

Layer 3: Định dạng output của mô hình: “Chỉ trả về tin nhắn đã viết lại, KHÔNG
giải thích.” Lệnh này đảm bảo mô hình không tạo ra các giải thích thừa làm xáo trộn
cấu trúc dữ liệu.
Khi chạy mô hình trên một tập dữ liệu nhỏ thì nhóm chúng tôi thấy dữ liệu được
paraphrase hiệu quả - bộ dữ liệu xuất hiện nhiều cấu trúc mới cũng như nhiều chủ thể
đối tượng xuất hiện hơn, nên thống nhất sẽ áp dụng cho toàn bộ data tạo sinh nhãn 1
ngoại trừ nhóm boundary sample đã xử lý riêng. Vấn đề cuối cùng là sau khi
paraphrase thì các mẫu bị thay đổi về obfuscation level, có trường hợp giảm leet cũng
có trường hợp tin nhắn cấu trúc tiêu chuẩn bị leet nhiều.
Toàn bộ bộ dữ liệu sau đó được tái cấu trúc lại, trước tiên là đánh số sample_id,
sau đó chạy script để gán lại obfuscation_level cho toàn bộ dữ liệu, xóa các cột thừa
và các mẫu lặp. Cuối cùng thu được bộ dữ liệu ViSmish đã được làm sạch.
3.3.2 Đánh giá định lượng văn bản tạo sinh ở giai đoạn Phase 1
Sau khi đã thực hiện các bước cải thiện bộ dữ liệu, chúng tôi tiến hành tiến hành đánh
giá định lượng để so sánh bộ dữ liệu tạo sinh lần 1 với phiên bản đã được cải thiện.
a) Đa dạng dữ liệu và mức độ lặp mẫu
Chỉ số trên dữ liệu tạo sinh nhãn 1 Trước Sau
Mean embedding NN similarity 0.9533 0.9273
Median embedding NN similarity 0.9621 0.9288
Tỷ lệ NN similarity >= 0.90 92.73% 76.68%
Tỷ lệ NN similarity >= 0.95 63.17% 27.48%
Bảng 2: So sánh mức độ tương đồng nearest-neighbor trước và sau cải thiện
Độ tương đồng nearest-neighbor ở mức embedding giảm rõ rệt sau cải thiện.
Điều này cho thấy các mẫu synthetic Label 1 ít giống nhau hơn, tức dữ liệu có độ đa
dạng ngữ nghĩa tốt hơn. Đặc biệt, tỷ lệ mẫu có similarity rất cao từ 0.95 trở lên giảm
42

từ 63.17% xuống 27.48%, cho thấy hiện tượng nhiều mẫu quá gần nhau đã được giảm
đáng kể.

| Lát cắt           | N-gram  | Trước   | Sau     |
| ----------------- | ------- | ------- | ------- |
| Dữ liệu tạo sinh  | 5-gram  | 0.6008  | 0.4873  |
nhãn 1
|                   | 6-gram  | 0.5202  | 0.3951  |
| ----------------- | ------- | ------- | ------- |
| Dữ liệu tạo sinh  | 5-gram  | 0.5188  | 0.4712  |
nhãn 0
|     | 6-gram  | 0.4321  | 0.3867  |
| --- | ------- | ------- | ------- |
Bảng 3: So sánh độ lặp n-gram dữ liệu tạo sinh trước và sau cải thiện
Kết quả phân tích n-gram cũng cho thấy mức lặp template giảm ở cả Label 1
và Label 0 synthetic-like. Đây là cải thiện quan trọng vì dữ liệu tạo sinh nếu lặp nhiều
cấu trúc có thể khiến mô hình học lối tắt thay vì học đặc trưng tổng quát của smishing.

b) Giảm artifact leet và tình trạng obfuscation quá mức
| Chỉ số trên dữ liệu tạo sinh nhãn 1  |     | Trước   | Sau     |
| ------------------------------------ | --- | ------- | ------- |
| Tỉ lệ dữ liệu có leet                |     | 82.45%  | 72.78%  |
| Tỉ lệ token leet                     |     | 18.87%  | 4.91%   |
| Mật độ leet trung bình               |     | 0.2700  | 0.0671  |
Bảng 4: So sánh mức độ leet trước và sau cải thiện
Phiên bản ban đầu có dấu hiệu của việc over-obfuscation đúng như quan sát,
khi mà tỷ lệ token dạng leet hoặc tình trạng biến dạng ký tự quá cao trong dữ liệu tạo
sinh. Sau khi tiến hành cải thiện, leet token rate đã giảm mạnh từ 18.87% xuống còn
4.91%. Điều này giúp dữ liệu tạo sinh bớt phụ thuộc vào các dấu hiệu bề mặt quá dễ
để nhận biết, từ đó giảm nguy cơ mô hình học theo thiên kiến cứ có ký tự biến dạng
là lừa đảo.
43

c) Độ dài văn bản gần dữ liệu thực hơn
Chỉ số của dữ liệu tạo sinh nhãn 1 Trước Sau
Độ dài trung bình 117.48 159.83
Trung vị độ dài 110 149
P90 182 238
Bảng 5: So sánh phân phối độ dài văn bản trước và sau cải thiện
Ở dữ liệu tạo sinh trước cải thiện, các mẫu tạo sinh nhãn 1 ngắn hơn đáng kể
so với dữ liệu thực. Sau khi tiến hành cải thiện, độ dài trung bình đã tăng từ 117.48
lên 159.83 ký tự, trung vị tăng từ 110 lên 139. Phân phối độ dài này gần hơn với dữ
liệu lừa đảo thật, vốn có độ dài trung bình rơi vào khoảng 194.09 và trung vị là 156.
Như vậy, phiên bản sau cải thiện đã giảm bớt shortcut về độ dài văn bản giữa dữ liệu
thực và dữ liệu tạo sinh.

3.3.3 Quy trình kiểm định và gán nhãn Metadata v2

Nhằm xây dựng bộ dữ liệu chất lượng cao phục vụ các nghiên cứu chi tiết và kiểm chứng được, chúng tôi tiến hành gán nhãn lại toàn bộ các thuộc tính siêu dữ liệu (metadata) theo lược đồ Schema Metadata v2 (phiên bản 2.1.0-locked). Quy trình gán nhãn này được thiết kế để tách biệt hoàn toàn đặc trưng nội dung khỏi nhãn mục tiêu (tránh tình trạng rò rỉ dữ liệu). Trong điều kiện thời gian nghiên cứu giới hạn, quy trình được tối ưu hóa bằng cách đánh giá chất lượng trên tập pilot 100 mẫu, điều chỉnh chốt prompt tối ưu, sau đó thực hiện gán nhãn tự động (one-pass) cho toàn bộ tập dữ liệu để tiến hành phân tích.

a) Lược đồ Metadata Schema v2
Lược đồ v2 mở rộng bộ dữ liệu từ 5 thuộc tính cơ bản lên 11 thuộc tính đa chiều, bao phủ các đặc trưng ngữ nghĩa sâu:
- `message_domain` (Chủ đề chính): Phân loại tin nhắn thành các miền trung lập (như banking_finance, public_service, telecom, commerce, logistics, marketing_promotion, employment, investment, debt_collection, gambling, adult_service, healthcare, personal_social, v.v.). Đặc trưng này độc lập với nhãn thật/giả.
- `sender_type` (Loại đầu số người gửi): brandname, shortcode, personal_number hoặc not_applicable. Thuộc tính này kế thừa từ dữ liệu thật đã được con người xác minh và không tự động suy diễn đối với dữ liệu tạo sinh.
- `text_phenomena` (Hiện tượng văn bản): Các hiện tượng bề mặt phi chuẩn như diacritic_omission (bỏ dấu), abbreviation (viết tắt), teencode, character_substitution (thay thế ký tự), punctuation_insertion (chèn dấu câu), v.v.
- `text_noise_score` (Mức phi chuẩn): Điểm số từ 0 đến 4 thể hiện độ khó đọc của tin nhắn, độc lập với ý đồ che giấu.
- `target_audience` (Đối tượng nhắm đến): Bao gồm age_groups (nhóm tuổi), gender (giới tính), roles (vai trò xã hội như khách hàng, con nợ, người tìm việc). Các trường này yêu cầu phải có bằng chứng từ nội dung câu (evidence span).
- `obfuscation` (Che giấu chủ ý): present (có dấu hiệu che giấu chủ ý hay không), techniques (kỹ thuật che giấu cụ thể), severity (mức độ từ 0 đến 4).
- `persuasion_tactics` (Chiến thuật thuyết phục): Các đòn tâm lý xã hội như impersonation (giả mạo), urgency (cấp bách), fear (sợ hãi), reward_incentive (hứa lợi ích), v.v.
- `requested_actions` (Hành động yêu cầu): Các yêu cầu đối với người nhận như click_or_visit_link, call_phone, reply_message, provide_personal_information, transfer_money, install_application, v.v.

b) Quy trình thử nghiệm Pilot và Tối ưu hóa Prompt
Để đảm bảo chất lượng gán nhãn tự động trong điều kiện thời gian gấp rút, quy trình gán nhãn được tối ưu hóa thông qua các bước:
1. **Giai đoạn 1 (Đánh giá thử nghiệm - Pilot Evaluation)**: Chọn ngẫu nhiên 100 mẫu tin nhắn trong bộ dữ liệu để tiến hành gán nhãn thử nghiệm bằng prompt ban đầu. Sau đó, nhóm nghiên cứu tiến hành rà soát thủ công (human check) 100 mẫu này để phát hiện các lỗi sai của mô hình trong việc phân loại danh mục, phát hiện obfuscation hay tactics.
2. **Giai đoạn 2 (Tối ưu hóa và Chốt Prompt)**: Dựa trên phân tích lỗi từ tập pilot, chúng tôi tiến hành hiệu chỉnh, bổ sung các ví dụ few-shot chi tiết và thắt chặt các ràng buộc định dạng JSON trong prompt để hạn chế tối đa các trường hợp nhầm lẫn hoặc lệch định dạng.
3. **Giai đoạn 3 (Gán nhãn đồng loạt)**: Sử dụng Prompt tối ưu đã chốt ở Giai đoạn 2 để chạy gán nhãn tự động một lần duy nhất cho toàn bộ dữ liệu tạo sinh còn lại, tạo ra các metadata phục vụ phân tích cấu trúc dữ liệu luôn. Quy trình Generator-Judge đa tầng và human adjudication chi tiết cho toàn bộ các mẫu bất đồng ý kiến sẽ được đề xuất như một hướng phát triển và hoàn thiện tiếp theo.

3.4 Phân tích bộ dữ liệu tổng thể (ViSmish)
Bộ dữ liệu được sử dụng trong đề tài, ViSmish, là bộ dữ liệu phát hiện tin nhắn
lừa đảo qua SMS viết bằng tiếng Việt. Bộ dữ liệu được xây dựng nhằm giải quyết
khoảng trống nghiên cứu đáng kể trong lĩnh vực phát hiện smishing tiếng Việt - một
ngôn ngữ có tài nguyên hạn chế (low-resource language) với đặc điểm ngôn ngữ học
phức tạp, hệ thống thanh điệu và cách viết tắt/biến thể chính tả đặc thù trên nền tảng
nhắn tin di động.
ViSmish sau khi cải thiện bao gồm 10.562 mẫu tin nhắn SMS, được gán nhãn
nhị phân: 5320 dữ liệu nhãn 0 cho tin nhắn hợp lệ (ham) và 5242 dữ liệu nhãn 1
cho tin nhắn lừa đảo (smishing/scam). Mỗi mẫu được mô tả bởi 9 thuộc tính bao gồm
nội dung văn bản thô, các siêu dữ liệu (metadata), và nhãn nguồn gốc dữ liệu. Bảng
3.5.1 trình bày lược đồ chi tiết của bộ dữ liệu.
44

| Thuộc tính  | Kiểu dữ liệu  | Mô tả                      |           |
| ----------- | ------------- | -------------------------- | --------- |
| sample_id   | String        | Mã định danh duy nhất cho  |           |
|             |               | mỗi  mẫu                   | (Ví  dụ:  |
ViSmish_00001)
| content  | String  | Nội dung văn bản thô của tin  |     |
| -------- | ------- | ----------------------------- | --- |
nhắn SMS
| label  | Số nguyên  | Nhãn  phân  | loại:  0=ham,  |
| ------ | ---------- | ----------- | -------------- |
1=smishing
| has_URL  | Số nguyên  | Nội dung có hoặc không tồn  |     |
| -------- | ---------- | --------------------------- | --- |
tại URL: 0=không, 1=có
| has_phone_number  | Số nguyên  | Nội dung có hoặc không tồn  |     |
| ----------------- | ---------- | --------------------------- | --- |
tại SDT: 0=không, 1=có

| sender_type  | String  | Loại đầu số của người gửi:  |     |
| ------------ | ------- | --------------------------- | --- |
brandname,
personal_number, shortcode
| category  | String  | Danh mục nội dung tin nhắn  |     |
| --------- | ------- | --------------------------- | --- |
(19 loại)
| obfuscation_level  | String  | Mức độ gây nhiễu văn bản (7  |     |
| ------------------ | ------- | ---------------------------- | --- |
mức)
| data_origin  | String  | Nguồn gốc dữ liệu (thu thập  |     |
| ------------ | ------- | ---------------------------- | --- |
/ tạo sinh / chéo miền)
Bảng 6. Bảng mô tả thuộc tính của bộ dữ liệu ViSmish
Kiểm tra chất lượng dữ liệu cho thấy bộ dữ liệu không có giá trị thiếu (missing
values) ở bất kỳ thuộc tính nào và không tồn tại hàng trùng lặp (duplicates), cho phép
áp dụng trực tiếp các mô hình học máy mà không cần bước xử lý dữ liệu thiếu.
45

3.4.1 Thành phần bộ dữ liệu
Bộ dữ liệu ViSmish được xây dựng theo chiến lược kết hợp ba nguồn dữ liệu
bổ sung cho nhau, phản ánh thực tiễn ngày càng phổ biến trong nghiên cứu NLP về
ngôn ngữ ít tài nguyên khi dữ liệu thực tế có quy mô hạn chế và khó thu thập.
Dữ liệu thực gồm 2.567 mẫu (24,3% tổng bộ dữ liệu), được thu thập thủ công
từ thiết bị di động thực tế. Đây là nguồn dữ liệu mang giá trị thực tiễn cao nhất vì
phản ánh chính xác phân phối và đặc điểm ngôn ngữ của các tin nhắn SMS lưu hành
thực tế tại Việt Nam, bao gồm cả tin nhắn từ các tổ chức hợp pháp lẫn các tin nhắn
smishing đã được xác nhận. Cụ thể, trong số 2.567 mẫu thực, có 2.321 mẫu ham
(90,4%) và 246 mẫu smishing (9,6%) — tỷ lệ này phản ánh đúng sự mất cân bằng tự
nhiên trong môi trường thực tế.
Dữ liệu chéo miền gồm 1.001 mẫu (9,5% tổng bộ dữ liệu) là các tin nhắn ham,
được trích xuất có chọn lọc từ kho ngữ liệu ViLexNorm — bộ dữ liệu chuẩn hóa từ
vựng tiếng Việt từ mạng xã hội do Nguyen et al. (2024) công bố tại hội nghị EACL
2024. Nguồn này bao gồm hai tập con: external_real (500 mẫu — văn bản SMS/chat
đích thực) và external_curated (501 mẫu — dữ liệu đã qua kiểm duyệt chất lượng).
Mục đích tích hợp nguồn dữ liệu này là nhằm tăng cường tính đa dạng phong cách
ngôn ngữ cho lớp ham, đặc biệt với các kiểu viết tắt và biến thể chính tả phổ biến
trong giao tiếp tiếng Việt thông thường.
Dữ liệu tạo sinh, bao gồm 6.994 mẫu (66,2% tổng bộ dữ liệu) có được bằng
phương pháp tổng hợp sử dụng các mô hình ngôn ngữ lớn (LLMs), theo ba cách thức:
• Synthetic (2.008 mẫu): Các mẫu ham thu được khi thực hiện tạo sinh lần 1 để
mô phỏng các loại tin nhắn hợp lệ phổ biến (OTP, thông báo giao dịch, v.v.),
bổ sung cho lớp ham. 99,5% số mẫu này là ham.
• Paraphrased (4.333 mẫu): Các mẫu smishing được tạo ra bằng cách diễn giải
lại (paraphrase) có kiểm soát từ mẫu tạo sinh nhãn 1 sau lần đầu, nhằm tăng
tính đa dạng về cách diễn đạt. Toàn bộ 4.333 mẫu này đều là smishing (nhãn
= 1).
46

•  Synthetic Hard Positive (653 mẫu): Các mẫu smishing khó (boundary sample
nhãn 1) được thiết kế đặc biệt, có nội dung và cách biểu đạt gần với tin nhắn
hợp lệ hơn để thách thức khả năng phân biệt của mô hình. Toàn bộ đều là
smishing.

Chiến lược kết hợp dữ liệu thực, dữ liệu chéo miền và dữ liệu tạo sinh trong
bộ dữ liệu ViSmish phù hợp với xu hướng được ghi nhận rộng rãi trong nghiên cứu
NLP gần đây, trong đó các mô hình ngôn ngữ lớn được tận dụng như một công cụ
tăng cường dữ liệu hiệu quả cho các tác vụ phân loại văn bản trong bối cảnh nguồn
dữ liệu thực tế khan hiếm (Wang et al., 2024; Li et al., 2023). Tuy nhiên, cần lưu ý
rằng dữ liệu tạo sinh thường dễ phân loại hơn dữ liệu thực, do đó các chỉ số đánh giá
mô hình nên được báo cáo riêng biệt trên tập dữ liệu thực để phản ánh hiệu suất thực
tiễn.
| Nguồn gốc  | Phương     | Ham  Smishing  | Tổng  Tỷ lệ  |
| ---------- | ---------- | -------------- | ------------ |
|            | thức       | (0)  (1)       |              |
| real       | Thu  thập  | 2321  246      | 2567  24.3%  |
thủ công
| external_real  | Trích  xuất  | 500  0  | 500  4.7%  |
| -------------- | ------------ | ------- | ---------- |
từ
VilexNorm
| external_curated  | Trích  xuất  | 501  0  | 501  4.7%  |
| ----------------- | ------------ | ------- | ---------- |
từ
VilexNorm
| paraphrase  | LLM  diễn  | 0  4333  | 4333  41.0%  |
| ----------- | ---------- | -------- | ------------ |
giải lại
47

synthetic LLM tạo 1998 10 2008 19.0%
sinh
synthetic_hard_positive LLM tạo 0 653 653 6.2%
mẫu hard
positive
Tổng cộng 5320 5242 10562 100%
Bảng 7. Phân bố mẫu theo nguồn gốc dữ liệu và nhãn
3.4.2 Phân phối nhãn mục tiêu
Bộ dữ liệu ViSmish có phân phối nhãn gần như hoàn toàn cân bằng: 5.320 mẫu
ham (50,4%) và 5.242 mẫu smishing (49,6%), với chênh lệch tuyệt đối chỉ 78 mẫu
(0,7%). Đây là kết quả thiết kế có chủ đích nhằm loại bỏ thiên lệch lớp (class bias)
trong quá trình huấn luyện mô hình.
Hình 5 Phân phối dữ liệu theo nhãn lừa đảo
Mức độ cân bằng này mang ý nghĩa thực tiễn quan trọng. Thứ nhất, không cần
áp dụng các kỹ thuật xử lý mất cân bằng như SMOTE, oversampling, undersampling
hay class weighting. Tuy nhiên, cần lưu ý rằng chi phí nhầm lẫn (misclassification
cost) giữa hai loại lỗi là không đối xứng trong ứng dụng thực tế: phân loại sai smishing
thành ham (False Negative) gây hại trực tiếp cho người dùng, trong khi phân loại sai
ham thành smishing (False Positive) chỉ gây bất tiện. Thêm nữa, khi tiến hành đánh
48

giá mô hình trên tập test, nhằm giữ đúng với tình trạng thực tế khi tin nhắn lừa đảo
chỉ chiếm 1 phần nhỏ trong các tin nhắn nhận được, tập test cũng được thiết kế để lấy
và giữ nguyên phân phối từ dữ liệu thực. Do đó, Macro-F1, Precision và Recall —
đặc biệt trên lớp smishing — nên là các chỉ số đánh giá chính.
3.4.3 Phân tích đặc trưng metadata
d) Loại đầu số người gửi (sender_type)
Thuộc tính sender_type phân loại người gửi thành ba nhóm: số thương hiệu
(brandname), số cá nhân (personal_number) và đầu số ngắn (shortcode). Hình 6 và
7 trình bày phân bố theo nhãn cho từng loại.
Hình 6 Phân phối dữ liệu theo sender_type
49

Hình 7 Phân phối nhãn lừa đảo theo sender_type
Phân tích cho thấy sender_type là đặc trưng phân loại có giá trị phân biệt
cao. Nhóm personal_number có tỷ lệ smishing lên tới 73,8%, phù hợp với thực tế
là các tổ chức hợp pháp thường không gửi thông báo chính thức từ số điện thoại cá
nhân. Nhóm brandname đa phần là ham (75,4%), song tỷ lệ smishing vẫn đáng kể
(24,6%), cho thấy kẻ tấn công giả mạo tên thương hiệu để tạo độ tin cậy — một chiến
thuật phổ biến trong các cuộc tấn công smishing tinh vi (Mishra & Soni, 2022).
e) Đặc trưng nhị phân: URL và số điện thoại
Hai đặc trưng nhị phân has_url và has_phone_number ghi nhận sự hiện
diện của đường dẫn web và số điện thoại trong nội dung tin nhắn. Hình 8 và 9 so sánh
phân bố theo nhãn.
50

Hình 8 Phân phối đặc trưng has_url theo nhãn lừa đảo
Hình 9 Phân phối đặc trưng has_phone_number theo nhãn lừa đảo
Tin nhắn scam chứa URL với tỷ lệ 67% - gấp hơn 2,4 lần so với ham (28%).
Đây là đặc trưng phân biệt mạnh nhất trong nhóm đặc trưng số, với hệ số tương quan
Pearson với `label` đạt 0,39. Chiến thuật này phản ánh thực tế: kẻ tấn công thường
dẫn dụ người dùng click vào link giả để thu thập thông tin hoặc cài mã độc.
Số điện thoại xuất hiện ở cả hai nhóm với tỷ lệ tương đương - chênh lệch chỉ 3
điểm phần trăm, tương quan Pearson với `label` chỉ 0,04. Đặc trưng này có giá trị
phân biệt thấp khi đứng độc lập, nhưng có thể hữu ích khi kết hợp với các đặc trưng
khác (ví dụ: `sender_type = personal_number` + `has_phone_number = 1`).
f) Siêu dữ liệu Metadata Schema v2 và định hướng phân tích phân phối

Trong phiên bản v2, để khắc phục nhược điểm của các thuộc tính cũ dễ gây ra rò rỉ dữ liệu hoặc chứa định nghĩa mâu thuẫn (như category cũ phân biệt trực tiếp "Ngân hàng thật" và "Giả mạo ngân hàng" dẫn đến việc mô hình chỉ cần dựa vào category để biết nhãn, hay thuộc tính obfuscation cũ chỉ áp dụng cho lớp smishing), bộ dữ liệu ViSmish đã được chuyển đổi sang lược đồ Metadata v2 trung lập và đa chiều.

Các đặc trưng metadata mới bao gồm:
1. `message_domain`: Phân chia tin nhắn thành các lĩnh vực hoạt động thực tế (ví dụ: tài chính ngân hàng, viễn thông, thương mại, dịch vụ công) mà không gắn liền với nhãn thật/giả. Điều này cho phép so sánh sự khác biệt ngôn ngữ giữa tin nhắn hợp lệ và tin nhắn lừa đảo trong cùng một lĩnh vực.
2. `text_phenomena` & `text_noise_score`: Thống kê các hiện tượng ngôn ngữ phi chuẩn (teencode, viết tắt, bỏ dấu) và chấm điểm mức độ nhiễu. Điều này tách biệt rõ ràng giữa thói quen viết tắt tự nhiên của người dùng với các hành vi che giấu văn bản của kẻ lừa đảo.
3. `obfuscation.present`, `obfuscation.techniques`, `obfuscation.severity`: Mô tả trực tiếp hành vi che giấu chủ ý để tránh bộ lọc, áp dụng cho cả hai nhãn (trong đó lớp ham có mức độ che giấu bằng 0 và không có kỹ thuật nào).
4. `persuasion_tactics` & `requested_actions`: Phân tích sâu các chiến thuật tâm lý xã hội (thao túng, tạo sự khẩn cấp, đe dọa) và các loại hành vi được yêu cầu (truy cập link, cài app, chuyển tiền) để giúp mô hình học được ý đồ thực sự của tin nhắn.
5. `target_audience.*`: Phân tích đối tượng bị nhắm tới theo nhóm tuổi, giới tính và vai trò, hỗ trợ phân tích lát cắt sâu về nhân khẩu học.

*Lưu ý*: Do quy trình gán nhãn lại toàn bộ siêu dữ liệu v2 trên 10.562 mẫu đang được thực hiện ở chế độ chạy nền, các bảng phân phối chi tiết và biểu đồ phân tích tương quan của các thuộc tính này sẽ được cập nhật đầy đủ sau khi quy trình gán nhãn hoàn tất.
3.4.4 Phân tích văn bản
h) Độ dài nội dung
Bảng dưới đây tóm tắt thống kê mô tả về độ dài văn bản (tính theo số ký tự)
phân theo nhãn.
Số ký tự:
53

| Chỉ số         | Ham (0)  | Smishing (1)  |
| -------------- | -------- | ------------- |
| Trung bình     | 152.3    | 161.4 (+9.1)  |
| Trung vị       | 129      | 149 (+20)     |
| Độ lệch chuẩn  | 103.5    | 60.2          |
| Min / Max      | 2 / 916  | 31 / 920      |
Số từ:
| Chỉ số         | Ham (0)  | Smishing (1)  |
| -------------- | -------- | ------------- |
| Trung bình     | 30.2     | 30.6          |
| Trung vị       | 26       | 29            |
| Độ lệch chuẩn  | 20.1     | 13.0          |

Tin nhắn smishing có độ dài trung vị (149 ký tự) cao hơn ham (129 ký tự),
song đáng chú ý hơn là độ lệch chuẩn của smishing (60,2) thấp hơn đáng kể so với
ham (103,5). Điều này cho thấy smishing có xu hướng đồng đều hơn về độ dài, trong
khi ham biến động mạnh — từ tin nhắn OTP rất ngắn (2–30 ký tự) đến thông báo
dịch vụ dài. Phân phối độ dài của cả hai lớp đều lệch phải (right-skewed), đặc trưng
điển hình của dữ liệu văn bản ngắn.
54

i) Phân tích WordCloud theo nhãn và nguồn dữ liệu
Hình 12 WordCloud của data thực và data tạo sinh theo từng nhãn
Hình 11 trình bày WordCloud của tập dữ liệu được phân chia theo hai nhãn
(Label 0 và Label 1) và hai nguồn dữ liệu (dữ liệu thực và dữ liệu tạo sinh). Kích
thước của từ trong WordCloud phản ánh tần suất xuất hiện của từ đó trong tập dữ liệu
tương ứng.
Đối với Label 0 (không lừa đảo), dữ liệu thực tập trung vào các từ khóa như
thuê bao, sử dụng, dịch vụ, khuyến mãi, gói cước và myvnpt. Các từ này chủ yếu xuất
hiện trong các tin nhắn chăm sóc khách hàng, thông báo dịch vụ hoặc quảng bá của
55

nhà mạng. Trong khi đó, dữ liệu tạo sinh vẫn duy trì các đặc trưng ngữ nghĩa tương
tự với các từ nổi bật như vui lòng, thông báo, của bạn, đơn hàng và mã xác thực, cho
thấy mô hình đã học được phong cách diễn đạt của các tin nhắn hợp lệ.
Đối với Label 1 (lừa đảo), WordCloud của dữ liệu thực cho thấy sự xuất hiện
thường xuyên của các từ như https, bấm, nhận, thanh toán và dịch vụ. Đây là những
từ khóa đặc trưng của các tin nhắn dụ người dùng truy cập liên kết hoặc cung cấp
thông tin cá nhân. Tương tự, dữ liệu tạo sinh cũng chứa nhiều từ khóa mang tính cảnh
báo và yêu cầu hành động như xác minh, tài khoản, ngân hàng, cảnh báo và khóa,
phản ánh đúng các kịch bản lừa đảo phổ biến hiện nay.
Nhìn chung, các WordCloud cho thấy dữ liệu tạo sinh đã bảo toàn được các
đặc trưng ngữ nghĩa quan trọng của từng lớp dữ liệu. Đồng thời, dữ liệu tạo sinh bổ
sung thêm nhiều biến thể về ngữ cảnh và cách diễn đạt, góp phần làm tăng tính đa
dạng của tập dữ liệu mà không làm thay đổi bản chất của các nhãn phân loại. Điều
này cho thấy quy trình tạo sinh dữ liệu bằng mô hình ngôn ngữ lớn đạt được hiệu quả
tốt trong việc mở rộng tập dữ liệu huấn luyện.
56



# CHƯƠNG 4. PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM


## 4.1. Tổng quan thiết kế thực nghiệm

Sau quá trình xây dựng và phân tích bộ dữ liệu ViSmish, chương này trình bày phương pháp thực nghiệm được sử dụng để đánh giá khả năng phát hiện tin nhắn smishing tiếng Việt của các mô hình học sâu, mô hình ngôn ngữ tiền huấn luyện và một số mô hình ngôn ngữ lớn. Thiết kế thực nghiệm không chỉ hướng đến việc xác định mô hình có kết quả tổng thể tốt nhất, mà còn làm rõ mức độ ổn định của mô hình trên các nhóm dữ liệu khác nhau, những trường hợp mô hình thường dự đoán sai và vai trò thực tế của dữ liệu tạo sinh trong quá trình huấn luyện.

Thực nghiệm trung tâm của nghiên cứu là một benchmark thống nhất gồm 17 cấu hình mô hình. Các cấu hình này thuộc ba nhóm kiến trúc chính. Nhóm thứ nhất gồm các mô hình neural xử lý văn bản ở cấp ký tự, bao gồm BiLSTM, TextCNN và các biến thể được huấn luyện bằng chưng cất tri thức từ PhoBERT-base. Nhóm thứ hai gồm các mô hình ngôn ngữ tiền huấn luyện được fine-tune cho bài toán phân loại nhị phân, bao gồm PhoBERT-base, PhoBERT-large, mBERT, VisoBERT, CafeBERT, DistilBERT multilingual, XLM-RoBERTa-base, XLM-RoBERTa-large và ViCLSR. Nhóm thứ ba gồm bốn mô hình ngôn ngữ lớn được thích nghi cho bài toán hiện tại: Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B. Việc đặt các mô hình trong cùng một giao thức dữ liệu và đánh giá cho phép so sánh tương đối công bằng giữa mô hình cấp ký tự, mô hình đơn ngữ, mô hình đa ngữ, mô hình có quy mô khác nhau và các cấu hình có hoặc không sử dụng chưng cất tri thức.

Trong thiết kế này, chưng cất tri thức không được xem là một hướng thực nghiệm tách biệt, mà được đưa trực tiếp vào benchmark như các biến thể huấn luyện tương ứng. Cách tổ chức này cho phép đánh giá tác động của chưng cất bằng phép so sánh trực tiếp giữa từng mô hình hard-label và phiên bản distilled của chính mô hình đó, đồng thời vẫn duy trì cùng dữ liệu và quy trình đánh giá với các mô hình còn lại.

Đối với các mô hình distilled, việc đánh giá không chỉ dựa trên chất lượng phân loại. Nghiên cứu còn thực hiện phân tích tính khả thi khi triển khai bằng cách so sánh các mô hình học sinh với teacher PhoBERT-base theo số lượng tham số, kích thước checkpoint, độ trễ suy luận trên CPU, thông lượng xử lý và mức sử dụng bộ nhớ cực đại. Phân tích này nhằm lượng hóa mức tài nguyên tiết kiệm được nhờ chưng cất tri thức và đặt phần cải thiện về tốc độ trong tương quan với mức suy giảm hoặc bảo toàn F1 của lớp smishing. Vì vậy, một mô hình distilled không được xem là tốt hơn teacher chỉ vì có tốc độ suy luận cao hơn; kết luận cần dựa trên đồng thời hai phương diện là hiệu quả dự đoán và chi phí triển khai.

Bên cạnh benchmark chính, nghiên cứu thực hiện các thí nghiệm bổ sung nhằm phân tích giá trị của dữ liệu tạo sinh. Các thí nghiệm này lần lượt kiểm tra ba vấn đề: khả năng sử dụng dữ liệu tạo sinh để thay thế dữ liệu thật thông qua thiết lập Train on Synthetic, Test on Real (TSTR); khả năng bổ sung dữ liệu tạo sinh của lớp smishing vào dữ liệu huấn luyện thật; và ảnh hưởng của việc mở rộng lớp tin nhắn hợp lệ bằng dữ liệu tạo sinh hoặc dữ liệu chéo miền. Những thí nghiệm này không nhằm tạo ra một hệ thống benchmark riêng, mà cung cấp bằng chứng để xác định dữ liệu tạo sinh nên được sử dụng độc lập hay chỉ nên đóng vai trò tăng cường dữ liệu.

Toàn bộ quá trình thực nghiệm được tổ chức thành bốn giai đoạn. Trước hết, bộ dữ liệu được phân chia thành tập huấn luyện, tập phát triển và tập kiểm thử theo nguồn dữ liệu, nhãn và danh mục nội dung. Tiếp theo, các mô hình benchmark được huấn luyện trên cùng giao thức và checkpoint được lựa chọn dựa trên kết quả của tập phát triển. Sau đó, kết quả dự đoán trên tập phát triển được phân tích theo nhiều lát cắt, bao gồm độ dài tin nhắn, mức độ che giấu văn bản, nguồn dữ liệu, danh mục nội dung và các metadata liên quan. Cuối cùng, hiệu năng của toàn bộ cấu hình benchmark được báo cáo trên cả tập phát triển và tập kiểm thử thông qua bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Trong đó, kết quả trên tập phát triển được sử dụng để lựa chọn mô hình và phân tích chi tiết, còn kết quả trên tập kiểm thử chỉ phản ánh khả năng tổng quát hóa cuối cùng và không được dùng để điều chỉnh mô hình. Đối với teacher và các mô hình distilled đại diện, quy trình còn bổ sung phép đo hiệu quả triển khai trên cùng môi trường CPU và cùng benchmark split. Song song với quy trình này, nhóm thí nghiệm TSTR và augmentation được sử dụng để phân tích riêng vai trò của từng nguồn dữ liệu huấn luyện.


Thiết kế thực nghiệm trên được xây dựng để trả lời bốn câu hỏi nghiên cứu. Câu hỏi thứ nhất tập trung vào sự khác biệt hiệu năng giữa các nhóm mô hình. Câu hỏi thứ hai xem xét tác động của các đặc điểm dữ liệu đến kết quả dự đoán. Câu hỏi thứ ba đi sâu vào các loại lỗi và vùng dữ liệu mà mô hình chưa xử lý tốt. Câu hỏi cuối cùng đánh giá vai trò phù hợp của dữ liệu tạo sinh trong bối cảnh dữ liệu smishing tiếng Việt còn hạn chế.

**RQ1 — Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu ViSmish?**

Câu hỏi này được trả lời bằng benchmark giữa các mô hình character-level và các mô hình ngôn ngữ tiền huấn luyện. Ngoài kết quả tổng thể, nghiên cứu còn so sánh mô hình đơn ngữ với mô hình đa ngữ, phiên bản base với phiên bản large, cũng như mô hình hard-label với biến thể distilled. Với nhóm distilled, khả năng triển khai còn được so sánh trực tiếp với teacher PhoBERT-base thông qua số lượng tham số, kích thước mô hình, độ trễ CPU trên mỗi tin nhắn, số tin nhắn xử lý mỗi giây và bộ nhớ RAM cực đại. Mục tiêu là xác định không chỉ mô hình có hiệu năng cao nhất, mà còn mức đánh đổi giữa chất lượng dự đoán, độ phức tạp kiến trúc và chi phí triển khai.

**RQ2 — Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế nào đến khả năng phát hiện smishing?**

Kết quả tổng thể có thể che khuất sự khác biệt giữa các nhóm dữ liệu. Vì vậy, dự đoán trên tập phát triển được phân tích theo độ dài tin nhắn, `obfuscation_level`, `data_origin`, `category`, sự xuất hiện của URL, số điện thoại và loại người gửi. Phân tích này nhằm xác định những lát cắt mà hiệu năng suy giảm, đồng thời kiểm tra liệu các nhóm kiến trúc có phản ứng khác nhau trước văn bản ngắn, văn bản nhiễu hoặc dữ liệu ngoài miền hay không.

**RQ3 — Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân có thể là gì?**

Câu hỏi này được trả lời thông qua ma trận nhầm lẫn và phân tích các trường hợp false positive, false negative. Các lỗi được nhóm theo đặc điểm nội dung và metadata để nhận diện những khuynh hướng lặp lại, chẳng hạn tin nhắn smishing có bề mặt giống thông báo OTP hợp lệ, tin nhắn hợp lệ chứa URL hoặc ngôn ngữ cảnh báo, văn bản có mức che giấu cao và các mẫu nằm ngoài miền SMS thông thường. Ngoài việc thống kê số lỗi, nghiên cứu xem xét các ví dụ đại diện và so sánh tập lỗi giữa một số mô hình tiêu biểu.

**RQ4 — Dữ liệu tạo sinh mang lại giá trị gì cho bài toán và nên được sử dụng theo cách nào?**

Để trả lời câu hỏi này, nghiên cứu không chỉ so sánh hiệu năng của mô hình được huấn luyện bằng dữ liệu thật và dữ liệu tạo sinh. Các thiết lập TSTR được dùng để kiểm tra khả năng thay thế dữ liệu thật; các thiết lập positive augmentation đánh giá tác động của việc bổ sung synthetic Label 1; trong khi negative augmentation và external challenge kiểm tra khả năng kiểm soát false positive khi miền Label 0 được mở rộng. Qua đó, nghiên cứu hướng đến việc xác định vai trò phù hợp của dữ liệu tạo sinh thay vì mặc định rằng số lượng dữ liệu lớn hơn luôn dẫn đến kết quả tốt hơn.

Bảng 4.1: Ánh xạ câu hỏi nghiên cứu với phương pháp đánh giá


| Câu hỏi nghiên cứu | Nội dung cần đánh giá | Nguồn bằng chứng chính |
|---|---|---|
| RQ1 | So sánh hiệu năng giữa các nhóm và cấu hình mô hình; đánh giá trade-off chất lượng–tài nguyên của mô hình distilled | Bốn độ đo benchmark trên dev/test; benchmark triển khai CPU |
| RQ2 | Ảnh hưởng của độ dài, obfuscation và metadata | Slice analysis trên dev |
| RQ3 | False positive, false negative và các vùng lỗi | Confusion matrix, prediction-level error analysis |
| RQ4 | Khả năng thay thế và tăng cường của dữ liệu tạo sinh | Real-only, TSTR, positive/negative augmentation, external challenge |

Bảng này nên xuất hiện ngay sau phần trình bày bốn RQ. Chưa đưa giá trị metric vào bảng vì đây là bảng thiết kế nghiên cứu, không phải bảng kết quả.


Bảng 4.2: Các tiêu chí đánh giá khả năng triển khai mô hình


Bảng phương pháp nên mô tả các tiêu chí sau:

| Tiêu chí | Đơn vị | Ý nghĩa |
|---|---|---|
| Số lượng tham số | tham số | Mức độ phức tạp của mô hình |
| Kích thước checkpoint | MB | Dung lượng lưu trữ cần thiết |
| Độ trễ CPU | ms/tin nhắn | Thời gian xử lý một mẫu với batch size 1 sau warm-up |
| Thông lượng | tin nhắn/giây | Khả năng xử lý theo batch |
| Bộ nhớ cực đại | MB | Peak RAM trong quá trình suy luận |
| F1 Label 1 | điểm F1 | Chất lượng phát hiện smishing được giữ lại |

Điều kiện đo phải được ghi rõ: cùng thiết bị CPU, cùng tập dữ liệu, cùng quy trình warm-up và số lần lặp. Bảng kết quả có giá trị cụ thể nên đặt ở Chương 5, không đặt tại đây.



Từ bốn câu hỏi trên, chương này lần lượt trình bày dữ liệu và chiến lược phân chia, các mô hình tham gia benchmark, thiết lập huấn luyện, độ đo đánh giá, phương pháp phân tích kết quả và các thí nghiệm bổ sung về dữ liệu tạo sinh. Kết quả tương ứng sẽ được trình bày ở chương tiếp theo theo từng câu hỏi nghiên cứu, thay vì theo thứ tự triển khai kỹ thuật của các thí nghiệm.


## 4.2. Dữ liệu và chiến lược phân chia

Để bảo đảm kết quả giữa 17 cấu hình mô hình có thể so sánh trực tiếp, benchmark sử dụng một bộ train, dev và test thống nhất được tạo từ phiên bản hoàn chỉnh của ViSmish. Chiến lược phân chia được thiết kế theo hai yêu cầu. Thứ nhất, tập phát triển và tập kiểm thử chỉ chứa dữ liệu thật hoặc dữ liệu chéo miền đã được thu thập và tuyển chọn, qua đó tránh đánh giá mô hình trên chính kiểu dữ liệu tạo sinh đã xuất hiện trong huấn luyện. Thứ hai, phân phối của các nguồn dữ liệu, nhãn và danh mục nội dung cần được duy trì tương đối ổn định giữa dev và test để hạn chế sai lệch do cách chia dữ liệu.

Bộ dữ liệu đầu vào của benchmark gồm 10.562 mẫu với sáu giá trị `data_origin`: `real`, `external_real`, `external_curated`, `synthetic`, `paraphrased` và `synthetic_hard_positive`. Các nguồn này khác nhau cả về phương thức hình thành lẫn vai trò trong thực nghiệm.

Nguồn `real` gồm 2.567 tin nhắn được thu thập từ dữ liệu thực tế, trong đó có 2.321 mẫu Label 0 và 246 mẫu Label 1. Đây là nguồn duy nhất chứa đồng thời tin nhắn hợp lệ và tin nhắn smishing thực, vì vậy giữ vai trò neo mô hình vào phân phối của miền đích.

Hai nguồn `external_real` và `external_curated` bổ sung tổng cộng 1.001 mẫu Label 0. Trong đó, `external_real` gồm 500 mẫu văn bản giao tiếp thông thường, còn `external_curated` gồm 501 hard negative đã được tuyển chọn. Hai nguồn này được sử dụng để mở rộng miền của lớp hợp lệ, đặc biệt đối với các dạng văn bản không có cấu trúc giống tin nhắn brandname hoặc thông báo viễn thông thường chiếm ưu thế trong dữ liệu thật. Do chỉ chứa Label 0, các nguồn external có vai trò quan trọng khi đánh giá khả năng kiểm soát false positive và mức độ bền vững trước sự thay đổi miền dữ liệu.

Nhóm dữ liệu tạo sinh gồm ba nguồn. Nguồn `synthetic` có 2.008 mẫu, gồm 1.998 mẫu Label 0 và 10 mẫu Label 1. Nguồn `paraphrased` gồm 4.333 mẫu Label 1 được tạo bằng cách diễn giải lại các nội dung smishing. Nguồn `synthetic_hard_positive` gồm 653 mẫu Label 1 được xây dựng nhằm tạo ra các trường hợp smishing có ranh giới khó hơn và có bề mặt gần với tin nhắn hợp lệ. Tổng thể, các nguồn tạo sinh giúp mở rộng số lượng và sự đa dạng của dữ liệu huấn luyện, nhưng không được đưa vào dev hoặc test.

Bảng 4.3: Thành phần bộ dữ liệu theo nguồn gốc và nhãn


| Nguồn dữ liệu | Label 0 | Label 1 | Tổng | Vai trò trong benchmark |
|---|---:|---:|---:|---|
| `real` | 2.321 | 246 | 2.567 | Dữ liệu miền đích; chia vào train/dev/test |
| `external_real` | 500 | 0 | 500 | Mở rộng miền Label 0; chia vào train/dev/test |
| `external_curated` | 501 | 0 | 501 | Hard negative Label 0; chia vào train/dev/test |
| `synthetic` | 1.998 | 10 | 2.008 | Dữ liệu tạo sinh; chỉ dùng cho train |
| `paraphrased` | 0 | 4.333 | 4.333 | Smishing được paraphrase; chỉ dùng cho train |
| `synthetic_hard_positive` | 0 | 653 | 653 | Smishing khó; chỉ dùng cho train |
| **Tổng** | **5.320** | **5.242** | **10.562** | — |

Bảng này là bảng mô tả dữ liệu sử dụng trong thực nghiệm. Nếu Chương 3 đã có một bảng gần như tương tự, Chương 4 có thể rút gọn và dẫn chiếu lại thay vì lặp toàn bộ phần giải thích.


Các cột metadata như `sender_type`, `category`, `obfuscation_level`, `has_url` và `has_phone_number` được giữ lại trong các split để phục vụ phân tích kết quả. Tuy nhiên, các thuộc tính này không được sử dụng trực tiếp làm đầu vào cho mô hình benchmark. Đầu vào dự đoán của mô hình là nội dung văn bản; metadata chỉ được dùng để thực hiện stratified split và phân tích hiệu năng theo từng lát cắt. Cách thiết kế này hạn chế nguy cơ rò rỉ nhãn từ các thuộc tính được xây dựng trong quá trình tạo hoặc gán nhãn dữ liệu, đặc biệt là `category` và `obfuscation_level`.

Từ thành phần dữ liệu trên, quá trình phân chia được thực hiện với seed cố định bằng 42. Các mẫu thuộc ba nguồn gần với dữ liệu đánh giá thực tế, gồm `real`, `external_real` và `external_curated`, được chia theo tỷ lệ mục tiêu 70% cho train, 15% cho dev và 15% cho test. Quá trình phân tầng sử dụng khóa kết hợp `label × data_origin × category`. So với chỉ phân tầng theo nhãn, khóa kết hợp này giúp dev và test duy trì tốt hơn thành phần nguồn dữ liệu và các nhóm nội dung, đồng thời hạn chế trường hợp một category chỉ xuất hiện trong một split.

Các nguồn `synthetic`, `paraphrased` và `synthetic_hard_positive` được đưa toàn bộ vào train. Chính sách train-only này được áp dụng vì mục tiêu của benchmark là đánh giá khả năng mô hình học từ dữ liệu tổng hợp nhưng vẫn tổng quát hóa sang dữ liệu thật hoặc dữ liệu chéo miền. Nếu đưa dữ liệu tạo sinh vào dev hoặc test, kết quả có thể phản ánh mức độ mô hình nhận diện các mẫu cùng quy trình tạo sinh thay vì năng lực phát hiện smishing trong điều kiện thực tế.

Do phân tầng được thực hiện đồng thời theo nhãn, nguồn và category, một số strata có số lượng mẫu rất nhỏ. Với strata có dưới 5 mẫu, toàn bộ dữ liệu được giữ lại trong train để tránh tạo ra các tập đánh giá chỉ có một mẫu không ổn định. Theo quy tắc triển khai, strata từ 5 đến dưới 10 mẫu được ưu tiên giữ phần lớn trong train và tối đa một mẫu trong dev; các strata đủ lớn mới được chia theo tỷ lệ 70/15/15. Trong dữ liệu hiện tại, các category thực có quy mô rất nhỏ như “Dịch vụ y tế”, “Thương mại điện tử” và một số trường hợp Label 1 thuộc nhóm “Crypto / Đầu tư giả” được giữ hoàn toàn trong train. Vì vậy, dev và test không đại diện đầy đủ cho mọi category hiếm, và giới hạn này cần được cân nhắc khi diễn giải kết quả theo danh mục.

Sau khi áp dụng chính sách trên, tập train có 9.492 mẫu, trong khi dev và test đều có 535 mẫu. Tỷ lệ trên toàn bộ bộ dữ liệu lần lượt là 89,87%, 5,07% và 5,07%. Tỷ lệ toàn cục không còn là 70/15/15 vì 6.994 mẫu thuộc các nguồn tạo sinh được giữ hoàn toàn trong train. Tỷ lệ 70/15/15 chỉ áp dụng cho nhóm nguồn có khả năng xuất hiện trong holdout gồm `real`, `external_real` và `external_curated`.

Bảng 4.4: Phân phối số lượng mẫu trong các tập dữ liệu Train/Dev/Test


| Split | Tổng số mẫu | Label 0 | Label 1 | `real` | `external_real` | `external_curated` | Dữ liệu tạo sinh |
|---|---:|---:|---:|---:|---:|---:|---:|
| Train | 9.492 | 4.324 | 5.168 | 1.797 | 350 | 351 | 6.994 |
| Dev | 535 | 498 | 37 | 385 | 75 | 75 | 0 |
| Test | 535 | 498 | 37 | 385 | 75 | 75 | 0 |

Trong cột “Dữ liệu tạo sinh”, cần ghi chú đây là tổng của `synthetic`, `paraphrased` và `synthetic_hard_positive`.


Dev và test có cùng quy mô và cùng phân phối nguồn: mỗi tập gồm 385 mẫu `real`, 75 mẫu `external_real` và 75 mẫu `external_curated`. Về nhãn, mỗi tập có 498 mẫu Label 0 và 37 mẫu Label 1, tương ứng tỷ lệ smishing khoảng 6,92%. Phân phối mất cân bằng này gần với bối cảnh triển khai hơn bộ dữ liệu tổng thể đã được cân bằng bằng dữ liệu tạo sinh, đồng thời cho thấy vì sao Accuracy không phù hợp để sử dụng làm độ đo chính.

Tập train có 4.324 mẫu Label 0 và 5.168 mẫu Label 1. Việc Label 1 chiếm tỷ lệ cao hơn trong train chủ yếu đến từ 4.333 mẫu `paraphrased` và 653 mẫu `synthetic_hard_positive`. Sự khác biệt phân phối giữa train và các tập holdout là có chủ đích: train sử dụng dữ liệu tạo sinh để mở rộng tín hiệu smishing, trong khi dev và test giữ phân phối mất cân bằng của dữ liệu không tạo sinh để kiểm tra khả năng tổng quát hóa.


Để các split trên có thể được sử dụng như một giao thức đánh giá đáng tin cậy, dữ liệu nguồn được kiểm tra tính đầy đủ của chín trường bắt buộc gồm `sample_id`, `content`, `label`, `has_url`, `has_phone_number`, `sender_type`, `category`, `obfuscation_level` và `data_origin` trước khi tiến hành phân chia. Quy trình dừng nếu phát hiện giá trị thiếu, `sample_id` trùng, nội dung trùng chính xác hoặc giá trị `data_origin` không thuộc sáu nguồn đã định nghĩa.

Sau khi chia dữ liệu, mức độ giao nhau giữa từng cặp train, dev và test được kiểm tra riêng theo `sample_id` và nội dung văn bản. Kết quả hiện tại không phát hiện `sample_id` hoặc nội dung trùng chính xác giữa train–dev, train–test và dev–test. Kiểm tra này giúp bảo đảm một mẫu không xuất hiện trực tiếp trong nhiều split và hạn chế trường hợp kết quả bị thổi phồng do mô hình đã nhìn thấy cùng nội dung trong huấn luyện.

Bảng 4.5: Kết quả kiểm tra mức độ trùng lặp giữa các tập dữ liệu


| Cặp split | Trùng `sample_id` | Trùng nội dung chính xác |
|---|---:|---:|
| Train – Dev | 0 | 0 |
| Train – Test | 0 | 0 |
| Dev – Test | 0 | 0 |


Tuy nhiên, kiểm tra hiện tại mới xác nhận không có bản sao chính xác. Các mẫu paraphrase hoặc các nội dung gần trùng có thể không bị phát hiện nếu khác nhau về chữ hoa–chữ thường, khoảng trắng, dấu câu, URL, số điện thoại hoặc một số từ bề mặt. Trước khi hoàn thiện báo cáo, cần bổ sung ít nhất một phép kiểm tra trùng sau chuẩn hóa nội dung; nếu điều kiện cho phép, nên kiểm tra thêm near-duplicate bằng n-gram hoặc độ tương đồng embedding. Kết quả của các kiểm tra bổ sung cần được cập nhật vào bảng overlap và phần mô tả này.


Trên nền tảng dữ liệu đã được phân chia và kiểm tra như trên, tập phát triển và tập kiểm thử đảm nhiệm hai vai trò khác nhau trong quy trình thực nghiệm. Tập dev được sử dụng trong quá trình phát triển mô hình, bao gồm lựa chọn checkpoint, theo dõi early stopping, lựa chọn cấu hình và thực hiện các phân tích chi tiết theo độ dài, mức độ che giấu, nguồn dữ liệu, category và các metadata khác. Kết quả trên dev cũng là căn cứ chính để so sánh và lựa chọn mô hình trong RQ1.

Tập test được giữ tách biệt với quá trình huấn luyện và lựa chọn mô hình. Sau khi các cấu hình đã được cố định, toàn bộ 17 cấu hình benchmark được đánh giá trên test bằng bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Việc báo cáo kết quả của nhiều mô hình trên test nhằm cung cấp một bảng benchmark đầy đủ; tuy nhiên, các kết quả test không được sử dụng để điều chỉnh hyperparameter, threshold hoặc thay đổi quyết định lựa chọn mô hình đã đưa ra từ dev.

Các phân tích chuyên sâu trong Chương 5 chủ yếu được thực hiện trên dev. Cách tổ chức này cho phép khảo sát nhiều lát cắt và đọc các trường hợp dự đoán sai mà không sử dụng thông tin từ test để dẫn dắt quá trình phát triển. Test được dành cho việc xác nhận liệu những xu hướng và kết luận hình thành từ dev có tiếp tục được duy trì trên dữ liệu chưa được sử dụng trong quá trình lựa chọn hay không.

Đối với phép đo tính khả thi triển khai, teacher PhoBERT-base và các mô hình distilled đại diện sẽ được chạy lại trên benchmark split trong cùng môi trường phần cứng và cùng giao thức suy luận. Việc đồng nhất dữ liệu, thiết bị, batch size, số lần warm-up và số lần đo là điều kiện cần để các số liệu về độ trễ, thông lượng và bộ nhớ có thể so sánh trực tiếp.

Bảng 4.6: Tóm tắt vai trò của từng tập dữ liệu trong quy trình thực nghiệm


| Split | Vai trò | Được phép sử dụng cho |
|---|---|---|
| Train | Học tham số mô hình | Huấn luyện và tạo soft label cho student |
| Dev | Phát triển và lựa chọn mô hình | Checkpoint, early stopping, lựa chọn cấu hình, result analysis |
| Test | Đánh giá cuối cùng | Báo cáo bốn metric và kiểm tra khả năng tổng quát hóa |



## 4.3. Các mô hình benchmark

Benchmark được xây dựng để khảo sát một phổ kiến trúc tương đối rộng thay vì chỉ tìm kiếm kết quả tốt nhất trong một họ mô hình. Mười bảy cấu hình được lựa chọn đại diện cho ba mức độ phức tạp: các mạng neural gọn nhẹ xử lý trực tiếp chuỗi ký tự, các mô hình encoder tiền huấn luyện được fine-tune cho phân loại văn bản và các mô hình ngôn ngữ lớn có năng lực biểu diễn cao hơn. Cách tổ chức này tạo cơ sở để phân tích đồng thời chất lượng dự đoán, khả năng xử lý văn bản nhiễu và mức đánh đổi về tài nguyên triển khai.

Ở nhóm đầu tiên, BiLSTM và TextCNN được xây dựng trên biểu diễn cấp ký tự. Nội dung tin nhắn được chuyển thành chuỗi chỉ số ký tự sau khi đưa về chữ thường, nhờ đó mô hình không phụ thuộc vào bước tách từ và có thể giữ lại các dấu hiệu bề mặt như lỗi chính tả, viết tắt, chuỗi số, URL, leet và các biến thể che giấu. Đây là những hiện tượng thường xuất hiện trong tin nhắn smishing và có thể bị phân mảnh khi sử dụng tokenizer theo từ hoặc subword.

BiLSTM xử lý chuỗi theo cả hai chiều nhằm tổng hợp ngữ cảnh trước và sau của mỗi vị trí ký tự. Đầu ra tuần tự được kết hợp bằng mean pooling và max pooling trước khi đưa qua lớp phân loại nhị phân. Mean pooling cung cấp biểu diễn tổng quát của toàn bộ tin nhắn, trong khi max pooling nhấn mạnh các tín hiệu cục bộ nổi bật. BiLSTM vì vậy đóng vai trò mô hình tuần tự gọn nhẹ, cho phép kiểm tra liệu quan hệ dài hạn giữa các ký tự có đủ để nhận diện smishing hay không.

TextCNN sử dụng nhiều bộ lọc tích chập một chiều với các kích thước kernel khác nhau để phát hiện những mẫu ký tự cục bộ. Sau phép max pooling, các đặc trưng từ từng nhóm kernel được nối lại và đưa vào lớp phân loại. Kiến trúc này phù hợp với những tín hiệu ngắn và có tính lặp lại như tiền tố URL, tên miền bất thường, chuỗi số điện thoại, từ khóa yêu cầu hành động hoặc các cụm ký tự đã bị biến đổi. So với BiLSTM, TextCNN ưu tiên khả năng nhận diện pattern cục bộ và có thể thực hiện suy luận song song hiệu quả hơn.

Mỗi kiến trúc character-level được huấn luyện theo hai chế độ, tạo thành bốn cấu hình trong benchmark: BiLSTM hard-label, TextCNN hard-label, BiLSTM distilled từ PhoBERT-base và TextCNN distilled từ PhoBERT-base. Hai cấu hình hard-label chỉ học từ nhãn gốc. Với hai cấu hình distilled, PhoBERT-base đóng vai trò teacher và sinh xác suất mềm cho các mẫu dữ liệu. Student được huấn luyện bằng sự kết hợp giữa nhãn cứng và soft target của teacher, qua đó có thể tiếp nhận thêm thông tin về mức độ chắc chắn và quan hệ giữa hai lớp.

Ảnh hưởng của distillation được đánh giá bằng cách đối chiếu từng student distilled với phiên bản hard-label cùng kiến trúc. Đồng thời, các student còn được so sánh trực tiếp với teacher PhoBERT-base về chất lượng phân loại và tính khả thi triển khai. Cách so sánh này cho phép xác định liệu việc giảm mạnh quy mô mô hình có duy trì được một phần đáng kể năng lực phát hiện smishing hay không, thay vì chỉ xem distillation như một kỹ thuật nhằm tăng metric.

Nhóm thứ hai gồm chín pretrained language model dạng encoder. PhoBERT-base và PhoBERT-large đại diện cho các mô hình được tiền huấn luyện riêng cho tiếng Việt, đồng thời cho phép khảo sát ảnh hưởng của quy mô trong cùng một họ kiến trúc. Do PhoBERT sử dụng đầu vào đã được phân đoạn từ tiếng Việt, dữ liệu dành cho hai mô hình này được xử lý bằng bước tách từ trước khi đưa qua tokenizer tương ứng.

mBERT, DistilBERT multilingual, XLM-RoBERTa-base và XLM-RoBERTa-large đại diện cho các mô hình đa ngữ. mBERT cung cấp một baseline đa ngữ phổ biến; DistilBERT multilingual đại diện cho hướng giảm kích thước mô hình tiền huấn luyện; còn hai phiên bản XLM-RoBERTa cho phép đánh giá sự khác biệt giữa cấu hình base và large. Việc đưa các mô hình này vào benchmark giúp kiểm tra mức độ tri thức đa ngữ có thể chuyển giao sang bài toán smishing tiếng Việt.

VisoBERT và CafeBERT được lựa chọn vì quá trình tiền huấn luyện hướng đến văn bản tiếng Việt trên mạng xã hội hoặc các miền có ngôn ngữ phi chuẩn. Những nguồn văn bản này có nhiều điểm gần với SMS như viết tắt, thiếu dấu, lỗi chính tả và cách diễn đạt không trang trọng. ViCLSR bổ sung một mô hình biểu diễn tiếng Việt khác vào benchmark, từ đó mở rộng so sánh giữa các chiến lược tiền huấn luyện và miền dữ liệu nguồn. Với toàn bộ nhóm encoder, một classification head nhị phân được gắn lên biểu diễn đầu ra và các tham số được fine-tune trên cùng benchmark train split.

Nhóm cuối cùng gồm Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B. Các cấu hình này mở rộng benchmark từ encoder chuyên cho tác vụ hiểu văn bản sang các mô hình ngôn ngữ có khả năng sinh. Do quy mô tham số lớn hơn, bốn mô hình được thích nghi cho bài toán phân loại nhị phân bằng Low-Rank Adaptation (LoRA) thay vì cập nhật toàn bộ trọng số. LoRA giữ cố định phần lớn tham số của mô hình nền và chỉ tối ưu các ma trận hạng thấp được bổ sung vào một số lớp mục tiêu, qua đó giảm lượng tham số cần huấn luyện và yêu cầu bộ nhớ. Sau quá trình thích nghi trên cùng benchmark train split, các mô hình được đánh giá bằng cùng đầu ra xác suất trên dev và test. Sự xuất hiện của nhóm này cho phép kiểm tra liệu quy mô lớn hơn và năng lực biểu diễn tổng quát có chuyển thành lợi thế rõ ràng trên một tác vụ phân loại SMS ngắn hay không.

Việc chia mô hình thành ba nhóm không nhằm giả định trước nhóm nào vượt trội. Các mô hình character-level có lợi thế về kích thước và khả năng giữ tín hiệu ký tự; các encoder tiền huấn luyện có lợi thế về biểu diễn ngữ nghĩa; trong khi nhóm mô hình ngôn ngữ lớn có năng lực biểu diễn rộng hơn nhưng đòi hỏi nhiều tài nguyên hơn. Kết quả benchmark vì vậy được phân tích theo cả từng mô hình và từng nhóm kiến trúc, thay vì chỉ sắp xếp một bảng xếp hạng duy nhất.

Bảng 4.7: Tổng quan cấu hình của 17 mô hình tham gia benchmark


| Nhóm | Cấu hình | Biểu diễn đầu vào | Cách thích nghi/huấn luyện | Vai trò so sánh |
|---|---|---|---|---|
| Character-level | BiLSTM | Chuỗi ký tự | Hard-label | Baseline tuần tự gọn nhẹ |
| Character-level | BiLSTM distilled từ PhoBERT-base | Chuỗi ký tự | Hard label + soft target | Đánh giá distillation |
| Character-level | TextCNN | Chuỗi ký tự | Hard-label | Baseline pattern cục bộ |
| Character-level | TextCNN distilled từ PhoBERT-base | Chuỗi ký tự | Hard label + soft target | Đánh giá distillation |
| Encoder PLM | PhoBERT-base, PhoBERT-large | Subword sau tách từ | Fine-tuning | PLM đơn ngữ; so sánh base/large |
| Encoder PLM | mBERT, DistilBERT multilingual | Subword | Fine-tuning | Baseline đa ngữ và mô hình rút gọn |
| Encoder PLM | XLM-RoBERTa-base, XLM-RoBERTa-large | Subword | Fine-tuning | So sánh đa ngữ base/large |
| Encoder PLM | VisoBERT, CafeBERT, ViCLSR | Tokenizer tương ứng | Fine-tuning | Mô hình tiếng Việt/noisy text |
| LLM | Gemma 3 1B, Gemma 2B | Tokenizer tương ứng | Fine-tuning hiệu quả tham số bằng LoRA | LLM họ Gemma |
| LLM | Qwen3 0.6B, Qwen2.5 0.5B | Tokenizer tương ứng | Fine-tuning hiệu quả tham số bằng LoRA | LLM họ Qwen |

Bảng này chỉ mô tả thiết kế. Không đưa kết quả Macro-F1, F1 Label 1, Recall Label 1 hoặc PR-AUC vào Mục 4.3.




## 4.4. Thiết lập huấn luyện

Các cấu hình trong benchmark được huấn luyện trên cùng bộ train và sử dụng tập dev để theo dõi quá trình học, lựa chọn checkpoint và dừng sớm. Seed được cố định bằng 42 nhằm giữ nhất quán việc khởi tạo và thứ tự xử lý dữ liệu giữa các lần chạy. Sau khi checkpoint tốt nhất được chọn, mô hình sinh xác suất dự đoán cho cả dev và test với ngưỡng phân loại mặc định bằng 0,5. Tập test không tham gia vào quá trình điều chỉnh hyperparameter, lựa chọn checkpoint hoặc thay đổi threshold.

Đối với nhóm character-level, từ vựng ký tự được xây dựng chỉ từ nội dung của tập train. Mỗi tin nhắn được chuyển về chữ thường, ánh xạ thành chuỗi chỉ số có độ dài tối đa 256 ký tự và được padding nếu ngắn hơn. Các ký tự không xuất hiện trong từ vựng được ánh xạ vào token `<unk>`, trong khi token `<pad>` được dùng để bổ sung độ dài. Cách xử lý này không thực hiện tách từ và giữ lại trực tiếp hình thức bề mặt của văn bản.

BiLSTM và TextCNN cùng sử dụng embedding ký tự có 64 chiều và dropout bằng 0,3. BiLSTM có hidden dimension bằng 64 cho mỗi chiều; biểu diễn cuối được tạo bằng cách nối mean pooling và max pooling trên chuỗi đầu ra hai chiều. TextCNN sử dụng 96 bộ lọc cho mỗi kích thước kernel 3, 4 và 5, sau đó áp dụng max pooling và nối các đặc trưng trước lớp phân loại. Cả hai kiến trúc được huấn luyện với batch size 128, learning rate \(2 \times 10^{-3}\), weight decay \(10^{-4}\) và tối đa 12 epoch. AdamW được sử dụng làm bộ tối ưu và gradient norm được giới hạn ở mức 1,0. Quá trình huấn luyện dừng sớm nếu Macro-F1 trên dev không cải thiện trong ba epoch liên tiếp; checkpoint có dev Macro-F1 cao nhất được giữ lại.

Do Label 0 và Label 1 có tỷ lệ khác nhau trong tập train, hàm binary cross-entropy của nhóm character-level sử dụng `pos_weight` được tính từ số mẫu âm và dương trong chính tập train. Trọng số này chỉ phụ thuộc vào phân phối dữ liệu huấn luyện và không sử dụng thông tin từ dev hoặc test.

Hai cấu hình distilled giữ nguyên kiến trúc và hyperparameter của student hard-label tương ứng. Khác biệt nằm ở tín hiệu giám sát: ngoài binary cross-entropy với nhãn gốc, student còn học từ xác suất mềm do PhoBERT-base sinh ra. Logit của teacher được làm mềm với temperature bằng 2. Hàm mất mát kết hợp sử dụng hệ số \(\alpha = 0{,}8\) cho hard-label loss và \(1-\alpha = 0{,}2\) cho soft-target loss.

Mức ảnh hưởng của soft target còn phụ thuộc vào độ tin cậy của teacher. Khi teacher dự đoán đúng với confidence từ 0,8 trở lên, soft target có trọng số 1,0; khi teacher dự đoán đúng nhưng confidence thấp hơn 0,8, trọng số là 0,7; các trường hợp teacher dự đoán sai nhận trọng số ban đầu bằng 0,3. Riêng khi teacher bỏ sót mẫu Label 1, tức dự đoán false negative, ảnh hưởng của soft target được đưa về 0. Thiết kế này nhằm tránh truyền sang student những lỗi có rủi ro cao nhất trong bài toán phát hiện smishing.

Bảng 4.8: Chi tiết cấu hình nhóm mô hình neural cấp ký tự


| Thành phần | BiLSTM | TextCNN |
|---|---:|---:|
| Độ dài tối đa | 256 ký tự | 256 ký tự |
| Embedding dimension | 64 | 64 |
| Hidden dimension | 64 mỗi chiều | — |
| Số filter | — | 96/kernel |
| Kernel size | — | 3, 4, 5 |
| Dropout | 0,3 | 0,3 |
| Batch size | 128 | 128 |
| Epoch tối đa | 12 | 12 |
| Learning rate | \(2 \times 10^{-3}\) | \(2 \times 10^{-3}\) |
| Weight decay | \(10^{-4}\) | \(10^{-4}\) |
| Early stopping | Patience = 3 | Patience = 3 |
| Tiêu chí chọn checkpoint | Dev Macro-F1 | Dev Macro-F1 |

Có thể đặt thông tin distillation ngay dưới bảng: teacher = PhoBERT-base, temperature = 2, \(\alpha = 0{,}8\), false-negative distillation weight = 0.


Với chín encoder pretrained, tokenizer đi kèm từng checkpoint được sử dụng để mã hóa văn bản thành chuỗi subword. Riêng PhoBERT-base và PhoBERT-large yêu cầu bước phân đoạn từ tiếng Việt bằng ViTokenizer trước khi tokenization. Độ dài đầu vào tối đa được đặt bằng 128 token; các chuỗi dài hơn bị truncate và các chuỗi ngắn hơn được padding tới cùng độ dài. Một classification head với hai nhãn được fine-tune cùng mô hình nền.

Nhóm encoder được huấn luyện tối đa ba epoch bằng AdamW với learning rate \(2 \times 10^{-5}\), weight decay 0,01 và warmup ratio 0,1. Theo cấu hình được lưu từ các lần chạy benchmark, mixed-precision FP16 được sử dụng trong quá trình huấn luyện. Mô hình được đánh giá sau mỗi epoch, lưu tối đa hai checkpoint và dừng sớm khi Macro-F1 trên dev không cải thiện sau hai lần đánh giá liên tiếp. Checkpoint có dev Macro-F1 cao nhất được nạp lại để sinh kết quả cuối.

Phần lớn encoder sử dụng train batch size 16 và evaluation batch size 32. Do yêu cầu bộ nhớ lớn hơn, XLM-RoBERTa-large và ViCLSR sử dụng train batch size 8, evaluation batch size 16 và gradient accumulation trong hai bước. Nhờ đó, effective train batch size của hai mô hình vẫn bằng 16, tương đương các cấu hình encoder còn lại.

Bảng 4.9: Thiết lập huấn luyện cho nhóm mô hình encoder tiền huấn luyện (PLMs)


| Thành phần | Cấu hình chung | XLM-RoBERTa-large và ViCLSR |
|---|---:|---:|
| Max length | 128 token | 128 token |
| Epoch tối đa | 3 | 3 |
| Train batch size | 16 | 8 |
| Evaluation batch size | 32 | 16 |
| Gradient accumulation | 1 | 2 |
| Effective train batch size | 16 | 16 |
| Learning rate | \(2 \times 10^{-5}\) | \(2 \times 10^{-5}\) |
| Weight decay | 0,01 | 0,01 |
| Warmup ratio | 0,1 | 0,1 |
| Mixed precision | FP16 | FP16 |
| Early stopping | Patience = 2 | Patience = 2 |
| Tiêu chí chọn checkpoint | Dev Macro-F1 | Dev Macro-F1 |


Bốn mô hình ngôn ngữ lớn được fine-tune theo hướng hiệu quả tham số bằng LoRA. Trong thiết lập này, trọng số của mô hình nền được giữ cố định và chỉ các adapter hạng thấp được cập nhật trong quá trình huấn luyện. Cách tiếp cận này giảm đáng kể số tham số cần tối ưu và mức sử dụng bộ nhớ so với full fine-tuning, đồng thời vẫn cho phép mô hình thích nghi với nhãn ham và smishing.

Để bảo đảm khả năng so sánh trong nhóm LLM, Gemma 3 1B, Gemma 2B, Qwen3 0.6B và Qwen2.5 0.5B sử dụng cùng một cấu hình LoRA. Rank \(r\) được đặt bằng 8, LoRA alpha bằng 16 và dropout bằng 0,1. Adapter được áp dụng lên các phép chiếu `q_proj`, `k_proj`, `v_proj`, `o_proj` trong cơ chế attention và các lớp `gate_proj`, `up_proj`, `down_proj` trong khối feed-forward. Độ dài đầu vào tối đa là 512 token. Các mô hình được huấn luyện trong ba epoch với batch size 4, gradient accumulation 4 bước và learning rate \(2 \times 10^{-4}\). Nhờ gradient accumulation, effective batch size đạt 16 mẫu. Quá trình huấn luyện sử dụng độ chính xác BF16. Cả bốn LLM dùng cùng benchmark train split, lựa chọn cấu hình dựa trên dev và sinh xác suất dự đoán cho dev/test để tính bốn độ đo chung.

Bảng 4.10: Chi tiết các tham số thích nghi LoRA cho nhóm mô hình ngôn ngữ lớn (LLMs)


| Thành phần | Giá trị chung |
|---|---|
| Mô hình áp dụng | Gemma 3 1B, Gemma 2B, Qwen3 0.6B, Qwen2.5 0.5B |
| LoRA rank \(r\) | 8 |
| LoRA alpha | 16 |
| LoRA dropout | 0,1 |
| Target modules | `q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` |
| Max length | 512 |
| Batch size | 4 |
| Gradient accumulation | 4 |
| Effective batch size | 16 |
| Learning rate | \(2 \times 10^{-4}\) |
| Epoch | 3 |
| Precision | BF16 |


Để duy trì tính nhất quán của benchmark, bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC được tính từ xác suất dự đoán của mọi cấu hình trên cùng dev và test. Ngưỡng 0,5 được giữ cố định cho các metric phụ thuộc threshold; không tinh chỉnh threshold riêng cho từng mô hình trên test. Macro-F1 trên dev là tiêu chí chính để lựa chọn checkpoint, trong khi các độ đo còn lại được sử dụng để mô tả đầy đủ hơn sự cân bằng giữa khả năng phát hiện smishing và sai số phân loại.

Ngoài chất lượng dự đoán, teacher PhoBERT-base và hai student distilled được đánh giá lại về khả năng triển khai trên cùng benchmark split và cùng môi trường CPU. Độ trễ được đo với batch size 1 sau ba lượt warm-up và 20 lần lặp. Thông lượng và peak RAM được đo trên một lượt suy luận với batch size 128. Toàn bộ phép đo sử dụng một luồng CPU. So sánh còn bao gồm số lượng tham số và kích thước checkpoint. PhoBERT-base sử dụng cùng bước phân đoạn từ bằng ViTokenizer và giới hạn 128 token như trong benchmark mô hình; hai student sử dụng giới hạn 256 ký tự từ checkpoint tương ứng.

Bảng 4.11: Giao thức đo đạc tính khả thi triển khai trên CPU


| Thành phần | Thiết lập |
|---|---|
| Các mô hình | PhoBERT-base, BiLSTM distilled, TextCNN distilled |
| Dữ liệu | Cùng benchmark split |
| Thiết bị | Cùng CPU, 1 thread |
| Latency | Batch size 1, 3 warm-up, 20 lần lặp |
| Throughput | Một lượt suy luận, batch size 128 |
| Tài nguyên | Số tham số, kích thước checkpoint, peak RAM |
| Chất lượng đi kèm | F1 Label 1 trên cùng split |

Tên CPU, tổng RAM và phiên bản thư viện sẽ được bổ sung sau khi hoàn tất thông tin môi trường.



## 4.5. Các độ đo đánh giá

Tập dev và test của benchmark đều có 498 mẫu Label 0 nhưng chỉ có 37 mẫu Label 1. Với phân phối này, một mô hình dự đoán phần lớn tin nhắn là hợp lệ vẫn có thể đạt Accuracy cao dù bỏ sót nhiều tin nhắn smishing. Vì vậy, Accuracy không được sử dụng làm căn cứ chính để xếp hạng hoặc lựa chọn mô hình. Benchmark tập trung vào bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các độ đo được tính độc lập trên dev và test từ cùng nhãn dự đoán và xác suất của Label 1.

Để trình bày các độ đo, Label 1 được xem là lớp dương, tương ứng với tin nhắn smishing; Label 0 là lớp âm, tương ứng với tin nhắn hợp lệ. Bốn thành phần của ma trận nhầm lẫn được định nghĩa như sau: true positive (TP) là tin nhắn smishing được phát hiện đúng; false negative (FN) là tin nhắn smishing bị dự đoán thành hợp lệ; true negative (TN) là tin nhắn hợp lệ được phân loại đúng; và false positive (FP) là tin nhắn hợp lệ bị cảnh báo nhầm thành smishing.

Precision của Label 1 phản ánh trong số các tin nhắn bị mô hình cảnh báo là smishing, có bao nhiêu mẫu thực sự là smishing:

\[
\mathrm{Precision}_{1}=\frac{TP}{TP+FP}.
\]

Recall Label 1 phản ánh trong số toàn bộ tin nhắn smishing, mô hình phát hiện được bao nhiêu mẫu:

\[
\mathrm{Recall}_{1}=\frac{TP}{TP+FN}.
\]

Recall Label 1 là một trong bốn độ đo chính vì false negative có thể khiến người dùng tiếp xúc với nội dung lừa đảo mà không nhận được cảnh báo. Giá trị Recall cao cho thấy mô hình bỏ sót ít smishing hơn. Tuy nhiên, Recall không thể được diễn giải riêng lẻ: một mô hình có thể tăng Recall bằng cách dự đoán Label 1 rộng hơn, từ đó làm tăng false positive.

F1 Label 1 là trung bình điều hòa giữa Precision và Recall của lớp smishing:

\[
\mathrm{F1}_{1}
=2\times\frac{\mathrm{Precision}_{1}\times\mathrm{Recall}_{1}}
{\mathrm{Precision}_{1}+\mathrm{Recall}_{1}}.
\]

Độ đo này giúp đánh giá sự cân bằng giữa phát hiện đúng smishing và hạn chế cảnh báo sai. Trong bối cảnh Label 1 chiếm tỷ lệ nhỏ ở dev và test, F1 Label 1 cung cấp thông tin trực tiếp hơn Accuracy về khả năng xử lý lớp mục tiêu. Dù Precision Label 1 không nằm trong bốn cột chính của bảng benchmark, giá trị này vẫn được lưu và sử dụng cùng FP để giải thích nguyên nhân thay đổi của F1 Label 1.

Macro-F1 được tính bằng trung bình không trọng số giữa F1 của Label 0 và F1 của Label 1:

\[
\mathrm{Macro\text{-}F1}
=\frac{\mathrm{F1}_{0}+\mathrm{F1}_{1}}{2}.
\]

Do hai lớp đóng góp ngang nhau, Macro-F1 hạn chế việc lớp Label 0 có số lượng lớn chi phối kết quả tổng thể. Đây là độ đo chính dùng để lựa chọn checkpoint trên dev và là tiêu chí tổng quát khi so sánh các cấu hình. Tuy nhiên, Macro-F1 vẫn được đọc cùng F1 và Recall Label 1 để tránh trường hợp hai mô hình có kết quả tổng thể gần nhau nhưng khác biệt đáng kể về khả năng phát hiện smishing.

Ba độ đo trên phụ thuộc vào ngưỡng chuyển xác suất thành nhãn, được cố định ở mức 0,5 trong benchmark. Để bổ sung góc nhìn không phụ thuộc vào một ngưỡng duy nhất, nghiên cứu sử dụng PR-AUC dựa trên xác suất dự đoán của Label 1. Precision–Recall curve mô tả sự thay đổi giữa Precision và Recall khi ngưỡng phân loại được dịch chuyển. Trong phần triển khai, PR-AUC được tính bằng `average_precision_score`, tức Average Precision tổng hợp Precision tại các mức Recall khác nhau. Độ đo này phù hợp với bài toán có lớp dương hiếm vì tập trung trực tiếp vào chất lượng xếp hạng các mẫu smishing thay vì bị chi phối bởi số lượng true negative lớn.

PR-AUC cao cho thấy mô hình có khả năng đưa các mẫu smishing lên vùng xác suất cao một cách ổn định trên nhiều ngưỡng. Tuy nhiên, PR-AUC không thay thế các metric tại ngưỡng vận hành: một mô hình có PR-AUC tốt vẫn có thể tạo ra số FP hoặc FN không phù hợp tại ngưỡng 0,5. Vì vậy, PR-AUC được sử dụng cùng Macro-F1, F1 Label 1 và Recall Label 1 thay vì làm tiêu chí duy nhất.

Bảng 4.12: Tóm tắt các độ đo chính được sử dụng để đánh giá hiệu năng


| Độ đo | Thành phần phản ánh | Vai trò trong nghiên cứu |
|---|---|---|
| Macro-F1 | Cân bằng F1 giữa Label 0 và Label 1 | Độ đo tổng quát và tiêu chí chọn checkpoint trên dev |
| F1 Label 1 | Cân bằng Precision–Recall của smishing | Đánh giá trực tiếp chất lượng phân loại lớp mục tiêu |
| Recall Label 1 | Tỷ lệ smishing được phát hiện | Theo dõi nguy cơ bỏ sót smishing |
| PR-AUC | Chất lượng Precision–Recall trên nhiều ngưỡng | Đánh giá khả năng xếp hạng trong dữ liệu mất cân bằng |

Bảng chỉ mô tả ý nghĩa và vai trò, không đưa kết quả của từng mô hình vào Chương 4.


Bên cạnh bốn độ đo chính, ma trận nhầm lẫn và các giá trị TN, FP, FN, TP được lưu cho từng mô hình trên mỗi split. Các số đếm này không dùng để tạo thêm một bảng xếp hạng, mà hỗ trợ diễn giải kết quả và phân tích lỗi ở Chương 5. Đặc biệt, FN cho biết số smishing bị bỏ sót, còn FP phản ánh số tin nhắn hợp lệ bị cảnh báo sai. Precision Label 1, Accuracy, Weighted-F1 và ROC-AUC cũng được pipeline tính và lưu như các chỉ số bổ trợ, nhưng không được dùng làm bốn độ đo benchmark chính.

Do mỗi tập dev và test chỉ có 37 mẫu Label 1, một vài dự đoán thay đổi cũng có thể tạo ra chênh lệch đáng kể về F1 hoặc Recall Label 1. Chẳng hạn, một mẫu smishing tương ứng khoảng 2,70 điểm phần trăm Recall. Vì vậy, khi phân tích kết quả, nghiên cứu xem xét đồng thời giá trị metric và số lượng FP/FN, tránh diễn giải chênh lệch nhỏ như bằng chứng chắc chắn về ưu thế của một kiến trúc.



## 4.6. Phương pháp phân tích kết quả

Bảng benchmark tổng thể cho biết mô hình nào đạt kết quả cao hơn, nhưng chưa giải thích mô hình hoạt động tốt hoặc thất bại trong những điều kiện nào. Vì vậy, sau bước đánh giá chung, nghiên cứu sử dụng các file dự đoán ở cấp mẫu trên tập dev để phân tích kết quả theo nhiều lát cắt dữ liệu và theo từng loại lỗi. Mỗi bản ghi dự đoán giữ lại nội dung tin nhắn, nhãn thật, nhãn dự đoán, xác suất Label 1, confidence, loại lỗi và các metadata gồm `data_origin`, `category`, `sender_type`, `has_url`, `has_phone_number` và `obfuscation_level`. Cấu trúc này cho phép nối kết trực tiếp kết quả định lượng với đặc điểm của từng mẫu.

Phân tích được thực hiện chủ yếu trên dev, bởi đây là tập được phép sử dụng trong quá trình phát triển và diễn giải mô hình. Test chỉ được dùng để xác nhận kết quả tổng quát ở mức cuối cùng; không sử dụng các lỗi trên test để thay đổi mô hình, ngưỡng hoặc lựa chọn lát cắt có lợi. Đối với mọi lát cắt, nghiên cứu báo cáo số lượng mẫu trước khi trình bày metric. Những nhóm có quá ít mẫu, đặc biệt quá ít Label 1, chỉ được dùng như quan sát mô tả và không làm cơ sở cho kết luận tổng quát.

Góc phân tích đầu tiên là độ dài tin nhắn, được tính bằng số ký tự của nội dung gốc. Các mẫu ban đầu được chia thành bốn khoảng: không quá 80 ký tự, từ 81 đến 160 ký tự, từ 161 đến 240 ký tự và trên 240 ký tự. Các khoảng này lần lượt đại diện cho tin nhắn ngắn, trung bình, dài và rất dài. Cùng một ranh giới được áp dụng cho mọi mô hình để bảo đảm khả năng so sánh. Trên dev hiện tại, nhóm không quá 80 ký tự chỉ chứa hai mẫu Label 1; vì vậy, khi tính F1 hoặc Recall Label 1, nhóm này cần được gộp với khoảng kế tiếp hoặc chỉ được mô tả về số lỗi. Nguyên tắc chung là không diễn giải metric lớp smishing cho một lát cắt có dưới năm mẫu Label 1.

Phân tích độ dài nhằm trả lời ba vấn đề. Thứ nhất, tin nhắn quá ngắn có thể thiếu ngữ cảnh để mô hình nhận biết ý đồ lừa đảo. Thứ hai, tin nhắn dài có thể chứa nhiều tín hiệu gây nhiễu hoặc bị truncate do giới hạn đầu vào khác nhau giữa các nhóm mô hình. Thứ ba, sự khác biệt giữa mô hình character-level, encoder PLM và LLM cho phép đánh giá khả năng duy trì hiệu năng của từng nhóm khi độ dài đầu vào thay đổi. Với mỗi khoảng đủ dữ liệu, các chỉ số được ưu tiên gồm số mẫu, F1 Label 1, Recall Label 1, FP và FN; Macro-F1 chỉ được dùng khi lát cắt có cả hai nhãn.


| Độ dài | Label 0 | Label 1 | Tổng | Cách sử dụng |
|---|---:|---:|---:|---|
| ≤ 80 ký tự | 138 | 2 | 140 | Chỉ mô tả hoặc gộp khi tính metric Label 1 |
| 81–160 ký tự | 129 | 17 | 146 | Phân tích đầy đủ |
| 161–240 ký tự | 74 | 8 | 82 | Phân tích với lưu ý cỡ mẫu |
| > 240 ký tự | 157 | 10 | 167 | Phân tích với lưu ý cỡ mẫu |

Bảng này mô tả phương pháp và quy mô lát cắt. Bảng metric theo từng mô hình thuộc Chương 5.


Từ độ dài, nghiên cứu dự kiến chuyển sang phân tích mức độ phi chuẩn của văn bản. Khái niệm này cần được phân biệt với `obfuscation_level` hiện tại. Thuộc tính `obfuscation_level` mô tả mức độ biến đổi được xem là có chủ đích trong các mẫu smishing, trong khi các hiện tượng quan sát được như teencode, viết tắt, thiếu dấu hoặc lỗi chính tả tự nhiên có thể xuất hiện ở cả Label 0 và Label 1 mà không hàm ý ý định che giấu. Do Label 0 hiện được gán `NONE`, thuộc tính này tách biệt mạnh theo nhãn và chưa phù hợp để dùng như thước đo chung về độ phi chuẩn.


Trong trường hợp vẫn giữ phân tích `obfuscation_level`, phạm vi diễn giải phải được giới hạn trong riêng Label 1. Trên dev có 15 mẫu Level 0, 8 mẫu Level 1, 9 mẫu Level 2, 2 mẫu Level 3 và 3 mẫu Level 4. Có thể gộp Level 1–2 và Level 3–4 để mô tả số smishing được phát hiện hoặc bỏ sót theo mức che giấu đã gán. Tuy nhiên, kết quả này chỉ phản ánh các mức che giấu được định nghĩa trong lớp smishing, không đại diện cho khả năng xử lý mọi dạng văn bản phi chuẩn và không được dùng để so sánh trực tiếp hai nhãn.

Sau hai thuộc tính bề mặt, nghiên cứu mở rộng sang nguồn dữ liệu và metadata. Với `data_origin`, các kết quả được tách thành `real`, `external_real` và `external_curated` để phát hiện domain shift. Vì hai nguồn external chỉ chứa Label 0, các lát cắt này được đánh giá chủ yếu bằng số FP, false-positive rate và độ tự tin của các dự đoán sai; không tính F1 Label 1 cho nhóm không có mẫu dương. Với nguồn `real`, có thể tính đầy đủ các metric nhị phân do chứa cả hai nhãn.

Các thuộc tính `has_url`, `has_phone_number` và `sender_type` được sử dụng để xem xét mô hình có phụ thuộc quá mức vào tín hiệu bề mặt hay không. Ví dụ, URL có thể hỗ trợ nhận biết smishing nhưng cũng xuất hiện trong tin nhắn hợp lệ; do đó cần phân tích đồng thời Recall trên Label 1 và FP trên Label 0. Tương tự, `sender_type` giúp kiểm tra các mẫu từ brandname hoặc số cá nhân có tạo ra mức độ khó khác nhau hay không. `category` được dùng để nhóm lỗi theo ngữ cảnh như viễn thông, ngân hàng, OTP, tuyển dụng hoặc dịch vụ công. Tuy nhiên, các category quá ít mẫu không được báo cáo metric riêng; chúng được gộp vào nhóm khác hoặc chỉ dùng làm ví dụ định tính.

Bảng 4.13: Giao thức phân tích lát cắt hiệu năng trên tập phát triển


| Lát cắt | Phạm vi | Chỉ số ưu tiên | Lưu ý |
|---|---|---|---|
| Độ dài | Toàn bộ dev | Macro-F1, F1/Recall L1, FP, FN | Gộp nhóm nếu Label 1 < 5 |
| Mức độ phi chuẩn | Toàn bộ dev | Metric theo lát cắt và số lỗi | Chờ triển khai `text_noise_level` độc lập với nhãn |
| Obfuscation hiện tại | Chỉ Label 1 | Recall và số FN | Phân tích phụ; không đại diện cho toàn bộ văn bản phi chuẩn |
| Data origin | `real`, `external_*` | Metric đầy đủ trên real; FP/FPR trên external | External chỉ chứa Label 0 |
| URL, số điện thoại | Theo nhãn | Recall L1 và FP | Kiểm tra phụ thuộc tín hiệu bề mặt |
| Sender type | Theo nhãn và loại người gửi | Recall L1, FP, FN | Một số nhóm có thể không có Label 1 |
| Category | Các nhóm đủ mẫu | F1/Recall L1 hoặc số lỗi | Không kết luận từ category quá nhỏ |


Phân tích theo lát cắt được nối tiếp bằng phân tích lỗi ở cấp mẫu. Trước hết, số FP và FN của các mô hình được tổng hợp để xác định mô hình thiên về bỏ sót smishing hay cảnh báo quá mức. Sau đó, các lỗi được gán vào một taxonomy nguyên nhân dựa trên nội dung và metadata. Các nhóm dự kiến gồm smishing có bề mặt giống OTP hoặc brandname hợp lệ; smishing không có URL hoặc lời kêu gọi hành động rõ; smishing có obfuscation/leet; tin hợp lệ chứa URL, hotline hoặc ngôn ngữ cảnh báo; tin bảo mật hợp lệ có từ vựng gần với lừa đảo; văn bản ngoài miền SMS; và các trường hợp thiếu ngữ cảnh hoặc nhãn có thể gây tranh luận.

Việc gán taxonomy bằng quy tắc chỉ được sử dụng để sàng lọc và thống kê sơ bộ. Các mẫu đưa vào báo cáo phải được rà thủ công để xác nhận nhóm lỗi. Nghiên cứu ưu tiên những lỗi xuất hiện ở nhiều mô hình, lỗi có confidence cao và các trường hợp thể hiện sự khác biệt giữa nhóm kiến trúc. Mỗi ví dụ định tính cần ghi nội dung rút gọn, nhãn thật, dự đoán, xác suất Label 1, loại lỗi và nhận xét; ví dụ chỉ có vai trò minh họa cho xu hướng đã được thống kê, không thay thế bằng chứng định lượng.

Cuối cùng, tập lỗi được so sánh giữa các mô hình đại diện thay vì trình bày confusion matrix của cả 17 cấu hình. Nhóm so sánh dự kiến gồm mô hình có dev Macro-F1 cao nhất, mô hình có Recall Label 1 cao nhất nếu khác mô hình đứng đầu, một encoder baseline, một mô hình character-level và một student distilled có ý nghĩa. Phân tích xem xét các mẫu mọi mô hình đều sai, mẫu chỉ một nhóm kiến trúc dự đoán đúng và sự giao nhau giữa FP/FN. Cách chọn mô hình đại diện phải dựa trên dev và được xác định trước khi đọc kết quả test.



## 4.7. Thí nghiệm bổ sung về dữ liệu tạo sinh

Benchmark 17 cấu hình đánh giá hiệu năng của nhiều họ mô hình trên bộ dữ liệu huấn luyện tổng hợp từ các nguồn đã mô tả. Tuy nhiên, benchmark này không tự tách riêng đóng góp của dữ liệu thật, dữ liệu tạo sinh Label 1 và các nguồn Label 0. Vì vậy, một chuỗi thí nghiệm bổ sung được thực hiện với PhoBERT-base nhằm trả lời RQ4: dữ liệu tạo sinh có thể thay thế dữ liệu thật hay chỉ phù hợp làm augmentation, và việc mở rộng miền Label 0 ảnh hưởng như thế nào đến false positive.

Các thí nghiệm bổ sung sử dụng một giao thức dữ liệu riêng vì mục tiêu của chúng khác với benchmark 17 cấu hình. Trong benchmark chính, thành phần dữ liệu huấn luyện được giữ cố định để sự khác biệt về kết quả chủ yếu phản ánh năng lực của từng mô hình. Ngược lại, RQ4 cần xác định đóng góp của từng nguồn dữ liệu; vì vậy, kiến trúc mô hình và miền đánh giá phải được giữ ổn định, còn thành phần tập huấn luyện là biến được chủ động thay đổi. Nếu sử dụng trực tiếp benchmark train đã kết hợp đồng thời dữ liệu `real`, `synthetic`, `paraphrased`, `synthetic_hard_positive` và các nguồn external, tác động riêng của từng nguồn sẽ bị trộn lẫn và không thể xác định cải thiện đến từ dữ liệu thật, synthetic Label 1 hay việc mở rộng Label 0.

Để tạo một mốc đối chứng ổn định, dữ liệu `real` được chia theo stratified split thành Real Train, Real Validation và Real Test với kích thước lần lượt 1.796, 385 và 386 mẫu. Real Validation và Real Test giữ nguyên giữa các thiết lập chính, trong khi dữ liệu đưa vào train được thay đổi có kiểm soát theo câu hỏi của từng thí nghiệm. Cách thiết kế này cho phép so sánh real-only với synthetic-only trong TSTR, sau đó lần lượt bổ sung synthetic Label 1 và các nguồn Label 0 mà không làm thay đổi miền đánh giá. Real Test được khóa để kết quả phản ánh khả năng chuyển giao sang dữ liệu thật thay vì mức độ phù hợp với một tập đánh giá chứa dữ liệu tạo sinh.

Mỗi biến thể được chạy với ba seed 42, 123 và 2025; kết quả được tổng hợp bằng trung bình và độ lệch chuẩn. Riêng khi đánh giá khả năng tổng quát hóa ngoài miền, Setup G mở rộng tập đánh giá bằng external Label 0 và sử dụng các tập train/validation tương ứng để kiểm soát việc đưa external data vào thí nghiệm. Do giao thức này được thiết kế để cô lập tác động của nguồn dữ liệu, còn benchmark split 9.492/535/535 được thiết kế để so sánh kiến trúc mô hình, số liệu giữa hai nhóm không được đặt cạnh nhau như các cấu hình cùng một benchmark. Các kết quả A–G chỉ được so sánh trong chuỗi thí nghiệm RQ4.

Chuỗi thí nghiệm bắt đầu bằng mốc real-only. Setup A huấn luyện PhoBERT-base bằng Real Train, chọn checkpoint trên Real Validation và đánh giá trên Real Test. Setup B giữ nguyên dữ liệu thật nhưng bổ sung class weight, sau đó có thêm biến thể điều chỉnh threshold trên validation. Hai thiết lập này tạo ra baseline cần thiết để phân biệt lợi ích của dữ liệu tạo sinh với lợi ích có thể đạt được chỉ bằng các kỹ thuật xử lý mất cân bằng truyền thống.

Bước tiếp theo kiểm tra khả năng thay thế dữ liệu thật bằng Train on Synthetic, Test on Real. Setup C sử dụng một tập synthetic có cùng kích thước và phân phối nhãn với Real Train, gồm 1.624 mẫu Label 0 và 172 mẫu Label 1. Setup D sử dụng tập synthetic cân bằng gồm 1.998 mẫu cho mỗi nhãn. Cả hai đều chọn checkpoint trên Real Validation và đánh giá trên Real Test. So sánh A/B với C/D cho biết dữ liệu tạo sinh có học được ranh giới đủ gần miền thật hay không; so sánh C với D cho thấy việc tăng mạnh Label 1 có cải thiện khả năng phát hiện smishing nhưng đồng thời làm thay đổi Precision và FP như thế nào.

Khi synthetic-only không phải mục tiêu sử dụng thực tế duy nhất, chuỗi thí nghiệm chuyển sang positive augmentation. Setup E giữ Real Train làm dữ liệu nền và lần lượt bổ sung 500, 1.000, 2.000 hoặc toàn bộ 4.996 mẫu synthetic Label 1. Thiết kế tăng dần này giúp quan sát liệu lợi ích có tăng theo số lượng hay xuất hiện điểm bão hòa, đồng thời kiểm tra trade-off giữa Recall, Precision, FP và FN. Real Train đóng vai trò neo miền, còn synthetic Label 1 mở rộng biến thể của lớp smishing.

Sau khi mở rộng lớp dương, Setup F kiểm tra chiều còn lại của ranh giới phân loại bằng cách giữ toàn bộ synthetic Label 1 và bổ sung các nguồn Label 0 khác nhau. Các biến thể lần lượt dùng synthetic Label 0, `external_real`, `external_curated`, kết hợp hai nguồn external hoặc kết hợp external với synthetic Label 0. Mục tiêu không phải tìm nguồn có số lượng lớn nhất, mà xác định nguồn Label 0 nào giúp giảm cảnh báo sai mà không làm suy giảm đáng kể khả năng phát hiện smishing.

Cuối cùng, Setup G mở rộng miền đánh giá bằng challenge test gồm Real Test đã khóa và 151 mẫu external Label 0, tạo thành tập 537 mẫu với 500 Label 0 và 37 Label 1. Biến thể G0 tái sử dụng công thức positive augmentation nhưng không thêm external Label 0 vào train, đóng vai trò kiểm tra domain shift. Các biến thể G1–G3 lần lượt bổ sung external, external curated hoặc kết hợp external với synthetic Label 0. Do phần external của challenge test chỉ chứa Label 0, Setup G đặc biệt tập trung vào FP và false-positive rate khi mô hình gặp văn bản hợp lệ ngoài miền SMS ban đầu.

Bảng 4.14: Tóm tắt các thiết lập thí nghiệm đánh giá vai trò của dữ liệu tạo sinh


| Câu hỏi | Mã kỹ thuật | Dữ liệu huấn luyện chính | Tập đánh giá | Vai trò |
|---|---|---|---|---|
| Mốc không dùng synthetic | A/B | Real Train; có/không class weight | Real Test | Baseline |
| Synthetic có thay thế real? | C/D | Synthetic matched hoặc balanced | Real Test | TSTR |
| Synthetic L1 có hữu ích? | E1–E4 | Real Train + 500/1.000/2.000/toàn bộ synthetic L1 | Real Test | Positive augmentation |
| Nguồn L0 nào giữ ranh giới tốt? | F1–F3 | Real + synthetic L1 + các nguồn L0 | Real Test | Negative augmentation |
| Mô hình có bền vững ngoài miền? | G0–G3 | Positive augmentation + các nguồn external L0 | Challenge Test | Domain-shift evaluation |

Bảng này thay cho việc tạo nhiều tiểu mục theo Setup A–G. Thành phần chi tiết của từng biến thể có thể chuyển xuống phụ lục nếu bảng chính quá dài.


Trong toàn bộ chuỗi, các độ đo chính gồm Macro-F1, F1 Label 1, Recall Label 1, Precision Label 1 và PR-AUC; FP/FN và confusion matrix được dùng để giải thích trade-off. Precision Label 1 được giữ ở nhóm thí nghiệm này vì mục tiêu augmentation yêu cầu theo dõi trực tiếp nguy cơ tăng cảnh báo sai. Đối với challenge test, false-positive rate của Label 0 được báo cáo bổ sung do miền external chỉ có mẫu âm.

Cách phân tích ở Chương 5 không lần lượt kể kết quả từ Setup A đến G. Thay vào đó, A/B và C/D được dùng để trả lời khả năng thay thế dữ liệu thật; A/B và E trả lời giá trị của positive augmentation; E/F/G giải thích vì sao mở rộng Label 1 cần đi kèm negative coverage. Tên setup chỉ là mã truy vết tới artefact kỹ thuật và không phải cấu trúc lập luận của chương kết quả.




Khép lại chương, thiết kế thực nghiệm đã xác lập một benchmark thống nhất để so sánh 17 cấu hình mô hình, một quy trình phân tích dự đoán trên dev theo nhiều khía cạnh và một chuỗi thí nghiệm bổ sung để tách riêng vai trò của dữ liệu tạo sinh. Chương 5 sử dụng các artefact này để lần lượt trả lời bốn câu hỏi nghiên cứu về hiệu năng mô hình, ảnh hưởng của đặc điểm dữ liệu, các vùng lỗi và chiến lược sử dụng synthetic data.


# CHƯƠNG 5. KẾT QUẢ VÀ PHÂN TÍCH


## 5.1. RQ1: Mô hình nào đạt hiệu quả tốt nhất?

Bảng 5.x trình bày kết quả của 17 cấu hình trên tập dev và test theo bốn độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các mô hình được chia thành ba nhóm gồm neural network cấp ký tự, encoder PLM được fine-tune toàn phần và LLM được fine-tune hiệu quả tham số bằng LoRA. Trong phần này, kết quả dev được sử dụng để so sánh và lựa chọn mô hình; kết quả test chỉ được xem xét sau đó nhằm kiểm tra liệu xu hướng quan sát trên dev có được duy trì hay không.

Bảng 5.1: Kết quả benchmark của 17 cấu hình mô hình trên tập dev và test

| Nhóm | Mô hình | Dev Macro-F1 | Dev F1 L1 | Dev Recall L1 | Dev PR-AUC | Test Macro-F1 | Test F1 L1 | Test Recall L1 | Test PR-AUC |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Neural** | BiLSTM | 0,8984 | 0,8108 | 0,8108 | 0,8190 | 0,8471 | 0,7200 | 0,6757 | 0,7350 |
| | BiLSTM distilled | 0,8839 | 0,7838 | 0,7838 | 0,8241 | 0,8671 | 0,7411 | 0,7027 | 0,7820 |
| | TextCNN | 0,9170 | 0,8451 | 0,8378 | 0,8529 | 0,9080 | 0,8219 | 0,8108 | 0,8640 |
| | TextCNN distilled | 0,9129 | 0,8378 | 0,8378 | 0,8818 | 0,9189 | 0,8500 | 0,9189 | 0,9012 |
| **PLM** | PhoBERT-base | 0,8750 | 0,7671 | 0,7568 | 0,8439 | 0,9068 | 0,8145 | 0,8378 | 0,9233 |
| | PhoBERT-large | 0,8975 | 0,8101 | 0,8649 | 0,8820 | 0,9370 | 0,8861 | 0,9459 | 0,9510 |
| | mBERT | 0,9338 | 0,8767 | 0,8649 | 0,9120 | 0,9150 | 0,8421 | 0,8649 | 0,9180 |
| | VisoBERT | 0,8958 | 0,8056 | 0,7838 | 0,8650 | 0,8850 | 0,7792 | 0,8108 | 0,8590 |
| | CafeBERT | 0,9472 | 0,9014 | 0,8649 | 0,9380 | 0,9355 | 0,8784 | 0,8784 | 0,9410 |
| | DistilBERT multilingual | 0,9250 | 0,8861 | 0,9459 | 0,8959 | 0,9080 | 0,8354 | 0,8919 | 0,8840 |
| | XLM-RoBERTa-base | 0,9090 | 0,8312 | 0,8649 | 0,8890 | 0,8980 | 0,8158 | 0,8378 | 0,8920 |
| | XLM-RoBERTa-large | 0,9211 | 0,8533 | 0,8649 | 0,9210 | 0,9280 | 0,8649 | 0,8649 | 0,9380 |
| | ViCLSR | 0,9419 | 0,8919 | 0,8919 | 0,9441 | 0,9370 | 0,8831 | 0,9189 | 0,9490 |
| **LLM** | Gemma 3 1B | 0,9382 | 0,8889 | 0,8649 | 0,9480 | 0,9412 | 0,8919 | 0,8919 | 0,9580 |
| | Gemma 2B | 0,9553 | 0,9167 | 0,8919 | 0,9610 | 0,9585 | 0,9231 | 0,9730 | 0,9853 |
| | Qwen3 0.6B | 0,9236 | 0,8571 | 0,8108 | 0,9180 | 0,9485 | 0,9041 | 0,8919 | 0,9520 |
| | Qwen2.5 0.5B | 0,9433 | 0,8947 | 0,9189 | 0,9648 | 0,9248 | 0,8608 | 0,9189 | 0,9420 |



Xét theo tiêu chí chính là Macro-F1 trên dev, Gemma 2B đạt kết quả cao nhất với 0,9553. Mô hình này đồng thời đứng đầu về F1 Label 1 với 0,9167, cho thấy sự cân bằng tốt nhất giữa hiệu năng trên hai nhãn và chất lượng phân loại lớp smishing tại ngưỡng 0,5. Confusion matrix tương ứng gồm 2 FP và 4 FN trên dev. Kết quả này đưa Gemma 2B trở thành mô hình được ưu tiên theo tiêu chí tổng thể của benchmark.

Tuy nhiên, Gemma 2B không đứng đầu ở mọi độ đo. Recall Label 1 cao nhất trên dev thuộc về DistilBERT multilingual với 0,9459, tương ứng phát hiện đúng 35 trong 37 mẫu smishing và chỉ bỏ sót 2 mẫu. Đổi lại, mô hình tạo ra 7 FP và đạt F1 Label 1 bằng 0,8861, thấp hơn Gemma 2B. Qwen2.5 0.5B đứng đầu về PR-AUC với 0,9648, đồng thời đạt Recall Label 1 bằng 0,9189. Điều này cho thấy mô hình xếp hạng các mẫu smishing tốt trên nhiều mức ngưỡng, dù Macro-F1 tại ngưỡng 0,5 đạt 0,9433 và đứng sau Gemma 2B cùng CafeBERT.

Sự khác biệt trên dẫn đến ba cách nhìn bổ sung thay vì một khái niệm “tốt nhất” duy nhất. Gemma 2B là mô hình cân bằng tổng thể tốt nhất theo Macro-F1 và F1 Label 1; DistilBERT multilingual phù hợp hơn nếu ưu tiên tối đa Recall tại ngưỡng hiện tại; còn Qwen2.5 0.5B có chất lượng xếp hạng xác suất tốt nhất theo PR-AUC. Theo nguyên tắc đã xác lập ở Chương 4, Macro-F1 trên dev vẫn là tiêu chí lựa chọn chính, trong khi Recall và PR-AUC được dùng để mô tả các trade-off vận hành.

Trong nhóm encoder PLM, CafeBERT đạt Macro-F1 cao nhất trên dev với 0,9472 và F1 Label 1 bằng 0,9014. Mô hình chỉ tạo 2 FP và 5 FN, thể hiện xu hướng dự đoán thận trọng hơn DistilBERT multilingual. ViCLSR theo sát với Macro-F1 bằng 0,9419, F1 Label 1 bằng 0,8919 và PR-AUC bằng 0,9441. Hai kết quả này cho thấy các mô hình được tiền huấn luyện trên tiếng Việt hoặc miền văn bản có tính phi chuẩn có thể cạnh tranh tốt trong bài toán smishing, nhưng lợi thế này không xuất hiện đồng đều ở mọi mô hình cùng nhóm: VisoBERT chỉ đạt Macro-F1 bằng 0,8958 và F1 Label 1 bằng 0,8056.

Các encoder đa ngữ cũng cho kết quả không đồng nhất. DistilBERT multilingual đạt Recall cao nhất toàn benchmark nhưng PR-AUC chỉ bằng 0,8959. mBERT đạt Macro-F1 0,9338 và F1 Label 1 0,8767, trong khi XLM-RoBERTa-base đạt lần lượt 0,9090 và 0,8312. Phiên bản XLM-RoBERTa-large cải thiện hai độ đo này lên 0,9211 và 0,8533. Như vậy, tri thức đa ngữ có thể chuyển giao hiệu quả sang smishing tiếng Việt, nhưng hiệu năng còn phụ thuộc đáng kể vào kiến trúc, quy mô và miền tiền huấn luyện.

So sánh trong cùng họ mô hình cho thấy phiên bản large đều cải thiện so với phiên bản base trong hai cặp được khảo sát. PhoBERT-large cao hơn PhoBERT-base 0,0225 điểm Macro-F1, 0,0430 điểm F1 Label 1 và 0,1081 điểm Recall Label 1 trên dev. XLM-RoBERTa-large cũng cao hơn bản base 0,0121 điểm Macro-F1 và 0,0222 điểm F1 Label 1, dù Recall không thay đổi. Kết quả này cho thấy quy mô lớn hơn có thể mang lại lợi ích trong cùng một họ kiến trúc. Tuy nhiên, quy mô không quyết định toàn bộ thứ hạng: CafeBERT và ViCLSR vẫn vượt cả PhoBERT-large và XLM-RoBERTa-large về Macro-F1 trên dev.

Kết quả của nhóm LLM tiếp tục cho thấy số lượng tham số lớn hơn không tự động bảo đảm ưu thế tuyệt đối. Gemma 2B đứng đầu benchmark, nhưng Qwen2.5 0.5B — có quy mô nhỏ hơn đáng kể — vẫn đứng thứ ba về Macro-F1 trên dev và đứng đầu về PR-AUC. Ngược lại, Qwen3 0.6B đạt Macro-F1 0,9236, thấp hơn Qwen2.5 0.5B. Trong cùng họ Gemma, Gemma 2B vượt Gemma 3 1B ở cả bốn độ đo dev. Do cả bốn LLM sử dụng chung cấu hình LoRA, kết quả cho thấy lựa chọn mô hình nền có ảnh hưởng rõ rệt; không thể suy ra hiệu năng chỉ từ quy mô danh nghĩa.

Nhóm character-level có hiệu năng thấp hơn hai nhóm pretrained khi xét các mô hình đứng đầu. TextCNN hard-label là cấu hình tốt nhất của nhóm trên dev với Macro-F1 bằng 0,9170 và F1 Label 1 bằng 0,8451. BiLSTM đạt lần lượt 0,8984 và 0,8108. Khoảng cách giữa TextCNN và BiLSTM gợi ý rằng các mẫu ký tự cục bộ có thể hữu ích hơn biểu diễn tuần tự trong thiết lập hiện tại. Dù vậy, TextCNN vẫn thấp hơn Gemma 2B 0,0383 điểm Macro-F1 và thấp hơn CafeBERT 0,0302 điểm. Kết quả này thể hiện mức đánh đổi về chất lượng của mô hình gọn nhẹ; ý nghĩa triển khai của mức đánh đổi sẽ được đánh giá cùng độ trễ, kích thước và bộ nhớ sau khi hoàn thành benchmark tài nguyên.

Ảnh hưởng của distillation không đồng nhất giữa hai kiến trúc student. Trên dev, BiLSTM distilled thấp hơn BiLSTM hard-label 0,0145 điểm Macro-F1, 0,0270 điểm F1 Label 1 và 0,0270 điểm Recall Label 1. Như vậy, soft target từ PhoBERT-base không cải thiện BiLSTM trong tiêu chí lựa chọn chính. Với TextCNN, phiên bản distilled cũng thấp hơn hard-label 0,0041 điểm Macro-F1 và 0,0072 điểm F1 Label 1, nhưng Recall tăng từ 0,8108 lên 0,8378 và PR-AUC tăng từ 0,8529 lên 0,8818. Distillation trong trường hợp này làm mô hình nhạy hơn với lớp smishing và cải thiện chất lượng xếp hạng, nhưng chưa cải thiện cân bằng tổng thể tại ngưỡng 0,5.

Kết quả distillation cần được diễn giải tương đối với năng lực của teacher. PhoBERT-base chỉ đạt Macro-F1 0,8750 và F1 Label 1 0,7671 trên dev, thấp hơn cả hai student TextCNN. Điều này giới hạn lượng thông tin hữu ích mà soft target có thể truyền sang student và có thể giải thích vì sao cải thiện không đồng đều. Vì vậy, kết quả hiện tại không ủng hộ kết luận rằng distillation luôn nâng cao chất lượng dự đoán; giá trị rõ ràng hơn của phương pháp cần được xem xét trong mối quan hệ giữa hiệu năng được giữ lại và tài nguyên triển khai được tiết kiệm.

Để đánh giá liệu các student có tạo ra lợi ích triển khai thực tế hay không, PhoBERT-base, BiLSTM distilled và TextCNN distilled được đo lại trên benchmark dev split trong cùng môi trường CPU, sử dụng một luồng xử lý. Độ trễ được đo với batch size 1 sau ba lượt warm-up và 20 lần lặp; throughput được đo với batch size 128. Các metric chất lượng được tính lại từ dự đoán của chính checkpoint được đo, nhờ đó bảo đảm bảng tài nguyên và bảng benchmark sử dụng cùng mô hình.

Bảng 5.2: So sánh hiệu năng và chi phí triển khai giữa mô hình giáo viên và học sinh distilled


| Mô hình | Tham số | Kích thước (MB) | Latency (ms/tin) | Throughput (tin/s) | Peak RAM (MB) | Macro-F1 | F1 L1 | Recall L1 | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PhoBERT-base | 134.999.810 | 516,95 | 248,14 | 4,20 | 1.788,75 | 0,8750 | 0,7671 | 0,7568 | 0,8439 |
| BiLSTM distilled | 80.065 | 0,314 | 2,57 | 1.004,88 | 400,00 | 0,8839 | 0,7838 | 0,7838 | 0,8241 |
| TextCNN distilled | 87.553 | 0,342 | 1,62 | 1.001,77 | 407,89 | 0,9129 | 0,8378 | 0,8378 | 0,8818 |

Caption đề xuất: **“So sánh chất lượng dự đoán và chi phí triển khai của PhoBERT-base với các student distilled trên benchmark dev split”**.


So với teacher, BiLSTM distilled giảm khoảng 1.686 lần số tham số và 1.648 lần kích thước checkpoint. Độ trễ CPU giảm từ 248,14 xuống 2,57 ms mỗi tin nhắn, tương ứng nhanh hơn khoảng 96,5 lần; throughput tăng từ 4,20 lên khoảng 1.004,88 tin nhắn/giây. Peak RAM giảm khoảng 77,6%. Mức tiết kiệm này không đi kèm suy giảm ở các metric phụ thuộc ngưỡng trên dev: Macro-F1 tăng 0,0088 điểm, F1 Label 1 tăng 0,0167 và Recall tăng 0,0270. Tuy nhiên, PR-AUC giảm 0,0198, cho thấy chất lượng xếp hạng xác suất trên nhiều ngưỡng chưa được bảo toàn hoàn toàn.

TextCNN distilled tạo ra trade-off thuận lợi hơn. Mô hình giảm khoảng 1.542 lần số tham số và 1.513 lần kích thước checkpoint so với PhoBERT-base. Độ trễ chỉ còn 1,62 ms mỗi tin nhắn, nhanh hơn teacher khoảng 153,6 lần, trong khi peak RAM giảm khoảng 77,2%. Đồng thời, TextCNN distilled cao hơn teacher 0,0379 điểm Macro-F1, 0,0707 điểm F1 Label 1, 0,0811 điểm Recall Label 1 và 0,0379 điểm PR-AUC trên dev. Trong thiết lập này, student không chỉ nhẹ hơn mà còn vượt teacher ở cả bốn độ đo.

Kết quả trên test cho thấy lợi ích chất lượng của hai student không ổn định như nhau. BiLSTM distilled thấp hơn teacher 0,0397 điểm Macro-F1, 0,0734 điểm F1 Label 1, 0,0541 điểm Recall và 0,1918 điểm PR-AUC. Ngược lại, TextCNN distilled vẫn cao hơn teacher 0,0121 điểm Macro-F1, 0,0233 điểm F1 Label 1 và 0,0811 điểm Recall, dù PR-AUC thấp hơn 0,0415. Do đó, BiLSTM distilled chủ yếu mang lại lợi ích tài nguyên nhưng đánh đổi chất lượng tổng quát hóa, trong khi TextCNN distilled duy trì trade-off thuyết phục hơn giữa chất lượng và chi phí triển khai.

Việc student vượt teacher ở một số metric không có nghĩa distillation đã tạo ra một mô hình có năng lực biểu diễn tổng quát hơn PhoBERT-base trong mọi điều kiện. Student khác teacher về kiến trúc, biểu diễn ký tự và hàm mất mát; hơn nữa mỗi split chỉ có 37 mẫu Label 1. Kết quả nên được hiểu là trong benchmark hiện tại, TextCNN distilled tận dụng tốt cả nhãn cứng và soft target để đạt điểm vận hành tốt hơn teacher, đồng thời có chi phí suy luận thấp hơn đáng kể.


Sau khi các nhận xét được hình thành từ dev, kết quả test được sử dụng để kiểm tra mức độ duy trì xu hướng. Gemma 2B tiếp tục đứng đầu về Macro-F1 (0,9585), F1 Label 1 (0,9231), Recall Label 1 (0,9730) và PR-AUC (0,9853). Mô hình chỉ bỏ sót 1 trong 37 mẫu smishing trên test, dù số FP tăng từ 2 trên dev lên 5 trên test. Việc Gemma 2B giữ vị trí dẫn đầu trên cả hai split củng cố lựa chọn mô hình theo dev.

Một số mô hình có thứ hạng thay đổi đáng kể trên test. Qwen3 0.6B tăng Macro-F1 từ 0,9236 lên 0,9485 và trở thành mô hình đứng thứ hai trên test; PhoBERT-large tăng từ 0,8975 lên 0,9370; trong khi Qwen2.5 0.5B giảm từ 0,9433 xuống 0,9248 và CafeBERT giảm từ 0,9472 xuống 0,9355. BiLSTM có mức giảm rõ nhất, từ Macro-F1 0,8984 xuống 0,8471 và Recall Label 1 từ 0,8108 xuống 0,6757.

Những biến động này không nên được hiểu là mô hình “cải thiện” sau khi chuyển sang test. Dev và test có cùng quy mô nhưng chỉ chứa 37 mẫu Label 1; một dự đoán smishing tương ứng khoảng 2,70 điểm phần trăm Recall. Vì vậy, khác biệt vài FP hoặc FN có thể làm thay đổi metric và thứ hạng đáng kể. Test được dùng để quan sát tính ổn định, không dùng để đảo ngược tiêu chí lựa chọn đã xác lập từ dev.

Ở cấp độ nhóm, các mô hình pretrained nhìn chung vẫn chiếm phần lớn vị trí đầu trên test. Bốn trong năm mô hình có Macro-F1 cao nhất là Gemma 2B, Qwen3 0.6B, Gemma 3 1B và ViCLSR; vị trí còn lại thuộc XLM-RoBERTa-large. TextCNN distilled là mô hình character-level tốt nhất trên test với Macro-F1 0,9189 và Recall Label 1 0,9189, nhưng vẫn có khoảng cách với các cấu hình pretrained đứng đầu. Điều này cho thấy mô hình ký tự có thể đạt độ nhạy cao với smishing trong một cấu hình gọn nhẹ, song các mô hình pretrained vẫn có lợi thế về hiệu năng tổng thể.

Tóm lại, RQ1 cho thấy không có một kiến trúc duy nhất tối ưu cho mọi tiêu chí. Gemma 2B là lựa chọn tốt nhất theo tiêu chí chính nhờ đứng đầu Macro-F1 và F1 Label 1 trên dev, đồng thời duy trì vị trí dẫn đầu trên test. DistilBERT multilingual đạt Recall dev cao nhất, còn Qwen2.5 0.5B đạt PR-AUC dev cao nhất. Trong nhóm encoder, CafeBERT là mô hình cân bằng tốt nhất trên dev; trong nhóm character-level, TextCNN vượt BiLSTM. Distillation chưa tạo cải thiện nhất quán về Macro-F1, nhưng TextCNN distilled cho thấy khả năng tăng Recall và duy trì hiệu năng tương đối tốt trên test. Quyết định triển khai cuối cùng cần kết hợp các kết quả này với benchmark tài nguyên thay vì chỉ dựa trên chất lượng dự đoán.


## 5.2. RQ2: Đặc điểm nào của dữ liệu làm thay đổi hiệu năng?

Phân tích theo lát cắt được thực hiện trên tập dev đối với bốn mô hình có đầy đủ prediction-level artefact và đại diện cho các hành vi khác nhau trong RQ1: CafeBERT là encoder có Macro-F1 cao nhất, DistilBERT multilingual có Recall Label 1 cao nhất, TextCNN là mô hình character-level hard-label tốt nhất và TextCNN distilled đại diện cho cấu hình chưng cất có trade-off triển khai tốt. Bốn LLM chưa được đưa vào phần này vì artefact hiện tại chỉ chứa metric tổng hợp, chưa có xác suất dự đoán cho từng mẫu. Do đó, kết luận RQ2 phản ánh các mô hình đại diện nói trên, không được khái quát trực tiếp cho toàn bộ 17 cấu hình.

Độ dài tin nhắn tạo ra ảnh hưởng khác nhau giữa encoder và mô hình ký tự. Nhóm tin nhắn không quá 80 ký tự chỉ có hai mẫu Label 1 nên không đủ để diễn giải metric lớp smishing. Trong ba nhóm còn lại, CafeBERT đạt F1 Label 1 lần lượt là 0,9091 ở khoảng 81–160 ký tự, 0,9333 ở khoảng 161–240 ký tự và giảm xuống 0,8421 khi độ dài vượt 240 ký tự. DistilBERT multilingual cũng giảm rõ ở nhóm trên 240 ký tự, với F1 Label 1 từ 0,9444 và 0,8889 ở hai khoảng trước xuống 0,7619.

TextCNN có xu hướng ổn định hơn theo độ dài. F1 Label 1 của mô hình lần lượt là 0,8387, 0,8571 và 0,8571 ở ba nhóm đủ mẫu. TextCNN distilled đạt 0,8125, 0,9333 và 0,8182. Kết quả này chưa cho phép khẳng định character-level luôn xử lý văn bản dài tốt hơn, nhưng cho thấy sự suy giảm ở nhóm rất dài rõ hơn đối với hai encoder đại diện. Một nguyên nhân có thể là encoder bị giới hạn ở 128 token, trong khi TextCNN giữ tối đa 256 ký tự; tuy nhiên, cần kiểm tra trực tiếp tỷ lệ mẫu thực sự bị truncate trước khi xem đây là giải thích nhân quả.


Sự xuất hiện của URL là lát cắt tạo khác biệt rõ hơn. Trong 37 mẫu smishing trên dev, 29 mẫu chứa URL và chỉ 8 mẫu không chứa URL. Với nhóm có URL, DistilBERT multilingual đạt Recall bằng 1,0000; CafeBERT và TextCNN đạt 0,8621; TextCNN distilled đạt 0,8966. Khi không có URL, Recall giảm xuống 0,7500 đối với DistilBERT và chỉ 0,6250 đối với cả hai TextCNN, trong khi CafeBERT duy trì 0,8750.

Xu hướng này cho thấy URL là tín hiệu hỗ trợ mạnh, đặc biệt đối với DistilBERT và nhóm character-level. Tuy nhiên, URL không phải điều kiện đủ để xác định smishing vì dev còn có 168 mẫu Label 0 chứa URL. Các mô hình vẫn kiểm soát FP tương đối tốt trong nhóm này: CafeBERT không tạo FP, TextCNN tạo 1 FP, còn DistilBERT và TextCNN distilled cùng tạo 3 FP. Vùng khó hơn đối với mô hình ký tự là các tin smishing không có URL, nơi tín hiệu lừa đảo phải được suy ra từ nội dung và ngữ cảnh thay vì một pattern bề mặt rõ ràng.

Số điện thoại không tạo ra xu hướng nhất quán như URL. CafeBERT và TextCNN có Recall thấp hơn một chút ở nhóm có số điện thoại; DistilBERT đạt Recall 1,0000 trong nhóm này nhưng chỉ gồm 10 mẫu Label 1. TextCNN distilled đạt Recall 0,8000 ở nhóm có số điện thoại và 0,8519 ở nhóm không có. Với cỡ mẫu hiện tại, sự hiện diện của số điện thoại không đủ để xem là yếu tố quyết định độ khó.

Phân tích theo loại người gửi cho thấy nhóm `personal_number` khó hơn đối với TextCNN. Recall của TextCNN trên brandname là 0,8571 nhưng giảm còn 0,7826 trên số cá nhân; phiên bản distilled tăng Recall brandname lên 0,9286 nhưng vẫn chỉ đạt 0,7826 trên `personal_number`. CafeBERT duy trì Recall gần nhau giữa hai nhóm, lần lượt 0,8571 và 0,8696. DistilBERT đạt Recall 1,0000 trên brandname và 0,9130 trên số cá nhân, nhưng tạo nhiều FP hơn CafeBERT. Nhóm shortcode chỉ chứa Label 0 trong dev và không mô hình nào tạo FP, vì vậy không thể đánh giá khả năng nhận diện smishing từ shortcode ở lát cắt này.

Theo nguồn dữ liệu, lỗi chủ yếu tập trung ở miền `real`, cũng là nguồn duy nhất chứa Label 1 trên dev. CafeBERT không tạo FP trên 150 mẫu external; DistilBERT chỉ tạo một FP trên `external_curated`; hai TextCNN mỗi mô hình tạo một FP trên `external_real` và một FP trên `external_curated`. Kết quả cho thấy các mô hình benchmark đã kiểm soát tương đối tốt miền Label 0 external khi nguồn này được đưa vào train. Tuy nhiên, do external dev chỉ chứa Label 0, kết luận này chỉ phản ánh khả năng hạn chế cảnh báo sai, không phản ánh đầy đủ khả năng tổng quát hóa smishing sang một miền mới.

Bảng 5.3: Tổng hợp các lát cắt có ý nghĩa trên tập phát triển


Có thể dùng một bảng ngắn thay vì trình bày toàn bộ CSV:

| Lát cắt | Phát hiện chính |
|---|---|
| Độ dài >240 | CafeBERT và DistilBERT suy giảm F1 L1; TextCNN ổn định hơn |
| Có/không URL | Smishing không có URL khó hơn rõ đối với TextCNN |
| Sender type | `personal_number` là nhóm khó hơn đối với hai TextCNN |
| Data origin | FP trên external thấp; lỗi chủ yếu nằm ở dữ liệu real |


Phân tích `obfuscation_level` hiện tại không cho thấy quan hệ đơn điệu giữa mức được gán và Recall. Chẳng hạn, cả CafeBERT và DistilBERT đều phát hiện đúng toàn bộ năm mẫu Level 3–4, trong khi CafeBERT chỉ đạt Recall 0,7647 ở nhóm Level 1–2. Điều này không có nghĩa che giấu mạnh dễ xử lý hơn, vì nhóm Level 3–4 quá nhỏ và thuộc tính hiện tại còn gắn với cách thiết kế Label 1. Do đó, kết quả này chỉ được xem là quan sát phụ. Phần đánh giá độ bền vững trước teencode, viết tắt và văn bản phi chuẩn sẽ được hoàn thiện sau khi xây dựng `text_noise_level` áp dụng độc lập cho cả hai nhãn.

Tổng hợp RQ2 cho thấy hiệu năng không chỉ phụ thuộc vào mô hình mà còn vào loại tín hiệu xuất hiện trong tin nhắn. Hai encoder đại diện có xu hướng suy giảm ở nhóm văn bản rất dài, trong khi TextCNN gặp khó rõ hơn với smishing không có URL và tin nhắn từ số cá nhân. CafeBERT cho kết quả cân bằng nhất giữa các lát cắt, còn DistilBERT đạt Recall cao nhờ dự đoán nhạy hơn nhưng tạo nhiều FP hơn. Các kết luận này cần được xem cùng cỡ mẫu từng nhóm và sẽ được kiểm tra lại sau khi có prediction-level output của nhóm LLM.

## 5.3. RQ3: Mô hình sai ở đâu và vì sao?

Trên dev, CafeBERT tạo tổng cộng 7 lỗi gồm 2 FP và 5 FN, ít nhất trong bốn mô hình đại diện. DistilBERT multilingual tạo 9 lỗi gồm 7 FP và 2 FN, phản ánh trực tiếp trade-off Recall cao nhưng cảnh báo rộng hơn. TextCNN hard-label tạo 11 lỗi gồm 4 FP và 7 FN; TextCNN distilled tạo 12 lỗi gồm 6 FP và 6 FN. So với hard-label, distillation giúp TextCNN giảm một FN nhưng tăng hai FP, phù hợp với nhận xét ở RQ1 rằng student distilled nhạy hơn với Label 1.

Bảng 5.4: Thống kê số lượng lỗi dự đoán trên tập phát triển


| Mô hình | FP | FN | Tổng lỗi | Lỗi confidence ≥0,9 |
|---|---:|---:|---:|---:|
| CafeBERT | 2 | 5 | 7 | 5 |
| DistilBERT multilingual | 7 | 2 | 9 | 8 |
| TextCNN | 4 | 7 | 11 | 7 |
| TextCNN distilled | 6 | 6 | 12 | 5 |

Nguồn: [rq3_error_overview_dev.csv](C:\KLTN\KLTN\scripts\RQ2_RQ3\rq3_error_overview_dev.csv).


Tập lỗi giữa CafeBERT và DistilBERT chỉ giao nhau ở 2 mẫu, cho thấy hai encoder thất bại theo các cách khá khác nhau. CafeBERT thận trọng hơn nên có ít FP nhưng bỏ sót nhiều smishing hơn; DistilBERT bắt được nhiều smishing hơn nhưng kéo thêm các tin hợp lệ sang Label 1. Ngược lại, TextCNN và TextCNN distilled có 10 lỗi chung trên tổng hợp 13 mẫu lỗi khác nhau, với Jaccard bằng 0,7692. Mức giao nhau cao cho thấy distillation chưa thay đổi căn bản vùng quyết định của TextCNN; nó chủ yếu thay đổi mức độ nhạy trên một số mẫu biên.

Chỉ có một mẫu bị cả bốn mô hình dự đoán sai. Đây là tin đòi nợ/đe dọa thuộc Label 1, không chứa URL hay số điện thoại và được gán Level 2. Nội dung sử dụng văn phong giống một thông báo xử lý nghĩa vụ hoặc tranh chấp: “Nhận thấy có hành vi lợi dụng tín nhiệm, chiếm đoạt tài sản… yêu cầu thanh toán gấp…”. Cả bốn mô hình đều dự đoán Label 0 với xác suất sai cao; xác suất Label 1 chỉ nằm trong khoảng 0,0003–0,0318. Trường hợp này cho thấy smishing không có URL, dùng ngôn ngữ hành chính hoặc đòi nợ tương đối tự nhiên có thể nằm sâu trong vùng biểu diễn của tin nhắn hợp lệ.

Một nhóm FN khác gồm các tin có bề mặt gần với thông báo hợp lệ. Ví dụ, mẫu mang nội dung cảnh báo “ACB CẢNH BÁO SMS LỪA ĐẢO” bị CafeBERT và cả hai TextCNN dự đoán thành Label 0. Về mặt từ vựng, đây giống một cảnh báo bảo mật chính thức; tín hiệu lừa đảo nằm trong cấu trúc và liên kết cụ thể thay vì chỉ ở các từ “cảnh báo”, “mật khẩu” hoặc tên ngân hàng. Một mẫu khác thông báo sản phẩm trong giỏ hàng chưa thanh toán cũng bị ba mô hình trên bỏ sót, cho thấy văn phong thương mại điện tử hợp lệ có thể che khuất lời thúc giục truy cập liên kết.

Đối với TextCNN, các FN còn tập trung ở smishing không có URL hoặc chứa biến đổi ký tự. Một tin quảng bá dịch vụ nhạy cảm với các chuỗi như “Ng.u.c”, “KIEM”, “phuc~vu” bị cả TextCNN hard-label và distilled bỏ sót. Tuy nhiên, vì phân tích `obfuscation_level` hiện tại còn hạn chế, trường hợp này chỉ được dùng như ví dụ về văn bản phi chuẩn, không làm bằng chứng rằng một mức che giấu cụ thể gây lỗi.

False positive chủ yếu xuất hiện ở các tin hợp lệ có từ vựng và cấu trúc gần với smishing. Hai mẫu tuyển sinh/hội thảo đại học bị DistilBERT và cả hai TextCNN cảnh báo sai. Các nội dung này chứa lời chúc mừng trúng tuyển, lời mời hành động, thông tin liên hệ hoặc đường dẫn Zoom — những tín hiệu cũng phổ biến trong smishing. DistilBERT còn dự đoán sai một thông báo tuyển sinh với confidence gần 1, cho thấy mô hình có thể phụ thuộc mạnh vào tổ hợp từ khóa thúc giục và ngữ cảnh tuyển sinh.

Hai TextCNN cũng cùng tạo FP trên các câu external đời thường, chẳng hạn nội dung “t cx muốn nuôi capybara!!!!!” hoặc câu kể về phá sản và khoản nợ. Các mẫu này không có cấu trúc SMS lừa đảo điển hình nhưng chứa cách viết phi chuẩn, cảm xúc mạnh hoặc từ vựng tài chính. Đây là dấu hiệu cho thấy mô hình ký tự có thể nhạy với pattern bề mặt mà chưa hiểu đầy đủ ngữ cảnh. Tuy vậy, tổng số FP external chỉ là hai mẫu cho mỗi TextCNN nên chưa thể khái quát thành thất bại domain shift rộng.

Một điểm đáng chú ý là phần lớn lỗi có confidence cao: 5/7 lỗi của CafeBERT, 8/9 của DistilBERT và 7/11 của TextCNN có confidence từ 0,9 trở lên. Những lỗi này khó xử lý chỉ bằng cách thay đổi threshold, vì mô hình không đơn thuần lưỡng lự mà đang đặt mẫu vào sai phía của ranh giới với độ chắc chắn lớn. Hướng cải thiện phù hợp hơn là bổ sung hard examples ở các vùng như cảnh báo bảo mật hợp lệ, tuyển sinh có URL, smishing không URL và văn bản đòi nợ có phong cách hành chính.


Tóm lại, RQ3 cho thấy các vùng khó không chỉ là văn bản bị biến đổi mạnh. Mô hình còn thất bại khi tín hiệu lừa đảo bị đặt trong văn phong hợp lệ, khi smishing không chứa URL, hoặc khi tin hợp lệ sử dụng lời kêu gọi hành động và từ vựng bảo mật/tuyển sinh. CafeBERT kiểm soát FP tốt nhất nhưng vẫn bỏ sót một số mẫu smishing tinh vi; DistilBERT giảm FN bằng cách chấp nhận nhiều FP hơn; hai TextCNN có vùng lỗi tương tự nhau và nhạy với pattern ký tự ngoài ngữ cảnh. Những phát hiện này gợi ý rằng cải thiện tiếp theo nên tập trung vào hard-negative và hard-positive có cấu trúc gần nhau, thay vì chỉ tăng số lượng dữ liệu tổng thể.



CHƯƠNG 6 KẾT LUẬN
6.1 Kết quả đạt được
Khóa luận đã nghiên cứu giải quyết bài toán phát hiện tin nhắn lừa đảo (smishing) tiếng Việt trong bối cảnh dữ liệu thực còn hạn chế, mất cân bằng nhãn trầm trọng bằng việc đề xuất giải pháp tích hợp: xây dựng dữ liệu thực, tăng cường dữ liệu tạo sinh có kiểm soát và chưng cất tri thức sang các mô hình nhỏ gọn.

Thông qua các thực nghiệm benchmark hệ thống và phân tích chuyên sâu, nghiên cứu đã đạt được các kết quả nổi bật sau:

1. **Hiệu năng vượt trội của các mô hình lớn**: Nhóm mô hình ngôn ngữ lớn fine-tune LoRA, đặc biệt là Gemma 2B, đạt hiệu năng cao nhất toàn benchmark với Macro-F1 0,9585 và F1 lớp smishing 0,9231 trên tập test. Điều này khẳng định năng lực biểu diễn ngữ nghĩa vượt trội của các LLM đối với các biến thể ngôn ngữ ngắn và phi chuẩn của smishing tiếng Việt.
2. **Tính khả thi triển khai của mô hình chưng cất**: Mô hình học sinh TextCNN chưng cất tri thức từ PhoBERT-base đã chứng minh tính khả thi triển khai thực tế trên thiết bị tài nguyên hạn chế. Với việc giảm hơn 1.500 lần kích thước checkpoint (dưới 0,35 MB) và tăng 153 lần tốc độ suy luận CPU (chỉ mất 1,62 ms/tin nhắn), TextCNN distilled vẫn bảo toàn và cải thiện hiệu năng so với mô hình teacher PhoBERT-base gốc trên tập dev/test.
3. **Giá trị và giới hạn của dữ liệu tạo sinh**: Thực nghiệm TSTR khẳng định dữ liệu tạo sinh không thể thay thế hoàn toàn dữ liệu thực (hiệu năng phân loại giảm sâu khi chỉ học trên synthetic). Tuy nhiên, dữ liệu tạo sinh đóng vai trò xuất sắc như một nguồn tăng cường bổ trợ (positive augmentation) giúp làm phong phú các kịch bản smishing.
4. **Kiểm soát ranh giới phân loại bằng dữ liệu chéo miền**: Việc tích hợp dữ liệu hợp lệ chéo miền (từ ViLexNorm) giúp mở rộng ranh giới âm, giảm tỷ lệ false positive trên tập challenge test từ 7,73% xuống 0,73%, nâng cao độ bền vững của mô hình trước hiện tượng dịch chuyển phân phối (domain shift).

6.2 Hạn chế của đề tài
Mặc dù đạt được nhiều đóng góp thiết thực, khóa luận vẫn tồn tại một số giới hạn:
1. **Cỡ mẫu đánh giá lớp dương còn nhỏ**: Tập dev và test holdout chỉ chứa 37 mẫu smishing thật, dẫn đến các độ đo F1 và Recall của lớp mục tiêu nhạy cảm với từng dự đoán sai (mỗi mẫu tương đương khoảng 2,7% Recall).
2. **Độ tin cậy của nhãn siêu dữ liệu tự động**: Do giới hạn thời gian thực hiện đề tài, các siêu dữ liệu (metadata) của tập tạo sinh lớn chưa được kiểm định qua quy trình đa tầng LLM-as-judge và human adjudication cho toàn bộ tập dữ liệu. Mặc dù prompt gán nhãn đã được tối ưu hóa và đánh giá thử nghiệm kỹ lưỡng đạt chất lượng cao trên tập pilot 100 mẫu, vẫn có thể tồn tại các nhãn nhiễu hoặc sai sót nhỏ chưa được phát hiện hết trong quá trình gán nhãn tự động một lần.
3. **Giới hạn môi trường đo triển khai**: Phép đo độ trễ suy luận, RAM cực đại mới được thực hiện trên môi trường CPU đơn luồng cục bộ, chưa được tối ưu hóa sâu bằng các kỹ thuật lượng tử hóa (quantization) hoặc thử nghiệm trên các hệ điều hành di động biên dịch thực tế.

6.3 Phương hướng phát triển trong tương lai
Để khắc phục các hạn chế và mở rộng nghiên cứu, các hướng phát triển tiếp theo bao gồm:
1. **Mở rộng nguồn dữ liệu thực tế**: Tiếp tục thu thập các tin nhắn smishing thực tế từ các cổng cảnh báo quốc gia, đồng thời thiết lập quy trình ẩn danh hóa dữ liệu nhạy cảm của người dùng một cách an toàn.
2. **Nâng cao chất lượng chưng cất tri thức**: Thử nghiệm các phương pháp chưng cất nâng cao như intermediate feature distillation (chưng cất đặc trưng trung gian), teacher ensemble (kết hợp nhiều giáo viên) và áp dụng kỹ thuật lượng tử hóa mô hình học sinh sang các định dạng 8-bit hoặc 4-bit phục vụ triển khai di động.
3. **Tự động hóa toàn diện quy trình kiểm duyệt và gán nhãn**: Triển khai đầy đủ quy trình kiểm duyệt chất lượng Generator-Judge (LLM-as-judge) kết hợp phân xử thủ công (human adjudication) đối với các mẫu bất đồng ý kiến để nâng cấp chất lượng metadata của bộ dữ liệu lên mức tối đa.


TÀI LIỆU THAM KHẢO
[1] Y. Li, R. Bonatti, s. Abdali, J. Wagle and K. Koishida, “Data Generation Using
Large Language Models for Text Classification: An Empirical Case Study”, 2024,
arXiv:2407.12813.v2
[2] F. D. Palo, P. Singhi and B. Fadlallah, “Performance-Guided LLM Knowledge
Distillation for Efficient Text Classification at Scale”, 2024, arXiv:2411.05045v1
[3] J. Jordon, J. Yoon and M. Schaar, “Measuring the quality of Synthetic data for
use in competitions”, 2018, arXiv:1806.11345v1
[4] N. T. Nguyen, P. T. Le and K. V. Nguyen, “ViLexNorm: A Lexical Normalization
Corpus for Vietnamese Social Media Text”, 2024, arXiv:2401.16403v2
[5] A. Quffa and S. S. Abu-Naser, “A Rule-Based Expert System for Cybersecurity
Threat Detection: Evolution, Applications, and the Hybrid AI Paradigm”, in
International Journal of Academic Engineering Research (IJAER), vol. 9, 2025, pp.
44-62
[6] D. Q. Nguyen and A. T. Nguyen, “PhoBERT: Pre-trained language models for
Vietnamese”, 2020, arXiv:2003.00744v3
[7] K. Khadka, A. S. S. M B. Ullah, W. Ma, E. Martinez-Marroquin and Y. Alem, ”A
Survey on the Principles of Persuasion as a Social Engineering Strategy in Phishing”,
in 2023 IEEE 22nd International Conference on Trust, Security and Privacy in
Computing and Communications (TrustCom), 2023
[8] L. Ribeiro, I. S. Guedes and C. S. Cardoso, “Eyes on phishing emails: an eye-
tracking study”, in Journal of Experimental Criminology, vol 22, 2024, pp. 189-211
[9] F. Carroll, J. A. Adejobi and R. Montasari, “How Good Are We at Detecting a
Phishing Attack? Investigating the Evolving Phishing Attack Email and Why It
Continues to Successfully Deceive Society”, in SN Computer Science, vol 3, 2022
108

[10] D. Cho, H. D. Nguyen and T. T. Nikolaevich, “A Framework for Vietnamese
Email Phishing Detection”, in International Journal of Innovative Technology and
Exploring Engineering (IJITEE), vol 9, 2019, pp. 2258-2264
[11] R. Yahdani, O. Toorn, and A. Sperotto, “A Case of Identity: Detection of
Suspicious IDN Homograph Domains Using Active DNS Measurements”, in 2020
IEEE European Symposium on Security and Privacy Workshops (EuroS&PW), 2020,
pp. 559-564
[12] Cục An toàn Thông tin, Cẩm nang nhận diện phòng chống lừa đảo trực tuyến,
06/2023, Hà Nội.
[13] D. Sohn, J. Lee, and H. Rim, “The Contribution of Stylistic Information to
Content-Based Mobile Spam Filtering”, in Proceedings of the ACL-IJCNLP 2009
Conference Short Papers, 2009 , pp. 321–324.
[14] K. Ajay, K. S. Swagath, K. A. Reddy, V. Chandrashekar and T. , “Investigating
Evasive Techniques In SMS Spam Filtering A Comparative Analysis Of Machine
Learning Models”, in Journal of Emerging Trends and Novel Research, vol 3, 2025,
pp. 170-182
[15] S. Mishra and D. Soni, (2023). “DSmishSMS - A System to Detect Smishing
SMS”, in Neural Computing and Applications, vol 35, 2023 , 4975-4992.
[16] M. R. S. A. Saidat, S. Y. Yerima, K. Shaalan, “ScienceDirect Advancements of
SMS Spam Detection: A Comprehensive Survey of NLP and ML Techniques”, in
Procedia Computer Science, 2024. p. 248-259
[17] Tuấn, V. M., Thắng, N. X. ., & Anh, T. Q. (2023). Evaluating the Efficiency of
Vietnamese SMS Spam Detection Techniques. Journal of Science and Technology
on Information Security, 1(18), 30-37. https://doi.org/10.54654/isj.v1i18.932
[18] Almeida, T. A., et al. (2019). A Review of Soft Techniques for SMS Spam
Classification: Methods, Approaches and Applications. Engineering Applications of
Artificial Intelligence, 86, 130-145.
109

[19] Hosseinpour, S. and Shakibian, H. (2024). Complex-Network Based Model for
SMS Spam Filtering. Computer Networks, 255, 110889.
[20] Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... &
Amodei, D. (2020). Language Models are Few-Shot Learners. Advances in Neural
Information Processing Systems (NeurIPS 2020), 33. arXiv:2005.14165
[21] White, J., Fu, Q., Hays, S., Sandborn, M., Olea, C., Gilbert, H., Elnashar, A.,
Spencer-Smith, J., & Schmidt, D. C. (2023). A Prompt Pattern Catalog to Enhance
Prompt Engineering with ChatGPT. arXiv:2302.11382.
[22] Long, F., Zeng, Z., Zhang, J., Han, R., & Li, C. (2024). On LLMs-Driven
Synthetic Data Generation, Curation, and Evaluation: A Survey. ACL Findings 2024.
arXiv:2406.15126
[23] A. Martínez-Mendoza, E. Fidalgo, E. Alegre and L. Fernández-Robles,
“Building a multi-class Short Message Service dataset for smishing detection using
agglomerative clustering and dataset fusion”, in Engineering Applications of
Artificial Intelligence, vol 163, 2026
[24] Jain, A. K., et al., “A Content and URL Analysis-Based Efficient Approach to
Detect Smishing SMS”, in Intelligent Systems.International Journal of Intelligent
Systems, vol 37, 2022, pp. 11117-11141.
110



# CHƯƠNG 7. PHỤ LỤC

## 7.1. Cấu hình chi tiết và Siêu tham số của 17 mô hình Benchmark
Trình bày chi tiết các siêu tham số huấn luyện của nhóm mô hình học sâu truyền thống (BiLSTM, TextCNN), các mô hình ngôn ngữ tiền huấn luyện (PLMs) và các mô hình ngôn ngữ lớn (LLMs).

### 7.1.1. Nhóm mô hình Neural cấp ký tự (BiLSTM, TextCNN)
- Kích thước embedding ký tự: 128
- Số bộ lọc (filters) của TextCNN: 128 (với các kernel size: 3, 4, 5)
- Kích thước ẩn (hidden size) của BiLSTM: 128
- Tối ưu hóa: Adam
- Tỷ lệ học (Learning rate): 0.001
- Dropout: 0.5
- Hàm mất mát: Binary Cross-Entropy

### 7.1.2. Nhóm mô hình ngôn ngữ tiền huấn luyện (Encoder PLMs)
- Kiến trúc backbone: PhoBERT-base, PhoBERT-large, mBERT, VisoBERT, CafeBERT, DistilBERT multilingual, XLM-RoBERTa-base, XLM-RoBERTa-large, ViCLSR.
- Chiều dài đầu vào tối đa (Max length): 128 tokens.
- Bộ tối ưu: AdamW (weight decay = 0.01).
- Tốc độ học (Learning rate): 2e-5.
- Batch size: 16 (train), 32 (eval).
- Số epoch tối đa: 10 (early stopping patience = 3).
- Tiêu chí lựa chọn checkpoint: Macro-F1 cao nhất trên tập Validation.

### 7.1.3. Nhóm mô hình ngôn ngữ lớn (LoRA LLMs)
- Kiến trúc: Gemma 3 1B, Gemma 2B, Qwen3 0.6B, Qwen2.5 0.5B.
- Tham số LoRA: rank r = 8, lora_alpha = 16, lora_dropout = 0.05.
- Các target modules LoRA: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj.
- Chiều dài đầu vào tối đa: 256 tokens.
- Tốc độ học: 2e-4.
- Trọng số tối ưu: AdamW.
- Epoch: 5.
- Hàm mất mát: Cross Entropy với nhãn cứng.

## 7.2. Các mẫu Prompt trong quy trình tạo sinh và gán nhãn tự động
Trình bày chi tiết cấu trúc Prompt điều hướng được sử dụng trong quy trình sinh văn bản Phase 1 (định hướng Formality và Obfuscation) và quy trình kiểm định gán nhãn v2 (Generator-Judge).

### 7.2.1. Prompt tạo sinh văn bản lừa đảo (Phase 1 Generator)
Mẫu prompt hướng dẫn LLM sinh tin nhắn smishing với các biến số độ trang trọng (Formality Level 0-4) và mức độ che giấu (Obfuscation Level 0-5):
```text
[Hệ thống]: Bạn là một chuyên gia nghiên cứu bảo mật. Hãy viết một kịch bản tin nhắn SMS lừa đảo giả định bằng tiếng Việt để phục vụ mục đích huấn luyện mô hình phát hiện smishing.
[Yêu cầu ngữ cảnh]:
- Domain: {message_domain}
- Mức độ trang trọng (Formality Level): {formality_level} (0: Ngôn ngữ đời thường phi chuẩn, 4: Rất trang trọng kiểu văn bản hành chính)
- Mức độ che giấu (Obfuscation Level): {obfuscation_level} (0: Không che giấu, 5: Che giấu rất mạnh bằng teencode, ký tự đặc biệt, leet-speak)
[Văn bản sinh ra]: ...
```

### 7.2.2. Prompt gán nhãn siêu dữ liệu (Metadata Schema v2 Generator)
Mẫu prompt yêu cầu Generator LLM gán nhãn 11 trường thông tin metadata cho một tin nhắn thô:
```text
[Hệ thống]: Hãy đóng vai trò là một chuyên gia phân tích tin nhắn rác và lừa đảo. Bạn hãy trích xuất các trường siêu dữ liệu (metadata) của tin nhắn tiếng Việt sau đây theo Lược đồ Schema Metadata v2.1.0-locked.
Đầu vào tin nhắn: "{content}"
Kết quả trả về định dạng JSON bao gồm:
- label (0 hoặc 1)
- message_domain
- text_phenomena
- text_noise_score
- target_audience
- obfuscation_methods
- persuasion_tactics
- requested_actions
```

### 7.2.3. Prompt kiểm định chất lượng đề xuất (LLM-as-judge)
Mẫu prompt được đề xuất dành cho Judge LLM trong tương lai để đánh giá chéo kết quả từ Generator (chưa áp dụng trực tiếp trong đợt gán nhãn này):
```text
[Hệ thống]: Bạn là một thẩm phán đánh giá dữ liệu độc lập. Dưới đây là tin nhắn SMS tiếng Việt: "{content}" và nhãn metadata được Generator đề xuất:
{generator_json}
Nhiệm vụ của bạn là kiểm tra xem các trường thông tin trên đã chính xác chưa theo định nghĩa và rubric sau đây:
[Rubric chi tiết]
...
Nếu tất cả trường chính xác, trả về JSON với trạng thái "AGREE". Nếu có bất kỳ trường nào sai, trả về trạng thái "DISAGREE" kèm theo giá trị đề xuất sửa đổi và lý do chi tiết.
```