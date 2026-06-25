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
Hội đồng chấm khóa luận tốt nghiệp, thành lập theo Quyết định số 646/QĐ-ĐHCNTT
ngày 09 tháng 06 năm 2026 của Hiệu trưởng Trường Đại học Công nghệ Thông tin.

LỜI CẢM ƠN
Lời đầu tiên, nhóm chúng em xin cảm ơn Thầy ThS. Huỳnh Văn Tín đã đồng
ý làm giáo viên hướng dẫn cho khóa luận tốt nghiệp của chúng em. Chúng em rất biết
ơn vì kiến thức chuyên môn mà thầy cung cấp cũng như giải đáp các thắc mắc và
chúng em gặp phải. Nhờ thầy mà đề tài khóa luận của chúng em có thể hoàn thiện
khóa luận tốt nghiệp một cách suôn sẻ. Nhóm chúng em cũng cảm ơn các thầy cô
Trường Đại học Công Nghệ Thông Tin nói chung và các thầy cô Khoa Khoa học và
Kĩ thuật Thông tin nói riêng vì đã luôn quan tâm, nhắc nhở, định hướng cho bốn năm
học trên ghế nhà trường. Nhờ có các thầy cô, chúng em có thể học hỏi và tích lũy các
kiến thức và trải nghiệm quý báu cho hành trình sau này. Cuối cùng, chúng em xin
biết ơn ba mẹ là điểm tựa vững chắc, luôn chăm sóc và động viên chúng em trong
quá trình học tập, cũng như bạn bè xung quanh luôn sẵn sàng giúp đỡ khi chúng em
gặp khó khăn.
Chúng em biết khóa luận của chúng em vẫn còn nhiều thiếu sót, nên chúng em
rất mong nhận được những lời đóng góp, gợi ý để khóa luận của chúng em hoàn thiện
hơn.
Chúng em xin chân thành cảm ơn!
Thành phố Hồ Chí Minh, tháng 6 năm 2026
Thành viên
Nguyễn Hoàng Duy, Trần Nguyễn Nam Hải
4

MỤC LỤC
MỤC LỤC ................................................................................................................... 5
PHỤ LỤC HÌNH ......................................................................................................... 8
PHỤ LỤC BẢNG ....................................................................................................... 9
TÓM TẮT KHÓA LUẬN ........................................................................................ 10
CHƯƠNG 1 GIỚI THIỆU ................................................................................... 12
1.1 Bối cảnh bài toán ........................................................................................ 12
1.2 Động lực nghiên cứu .................................................................................. 13
1.3 Đối tượng, phạm vi nghiên cứu và mục tiêu bài toán ................................ 14
CHƯƠNG 2 CƠ SỞ LÝ THUYẾT & NGHIÊN CỨU LIÊN QUAN ................. 18
2.1 Tổng quan và định nghĩa bài toán phát hiện tin nhắn lừa đảo ................... 18
2.2 Các công trình nghiên cứu liên quan .......................................................... 26
2.2.1 Nghiên cứu sử dụng dữ liệu tạo sinh trong phân loại văn bản ........... 26
2.2.2 Nghiên cứu về Chưng cất tri thức trên mô hình ngôn ngữ ................. 28
CHƯƠNG 3 XÂY DỰNG VÀ PHÂN TÍCH DỮ LIỆU ..................................... 29
3.1 Quy trình thu thập, gán nhãn dữ liệu thực .................................................. 29
3.1.1 Thu thập thủ công từ các nguồn công khai trên mạng ........................ 30
3.1.2 Thu thập dữ liệu thực tế thông qua thiết bị di động ............................ 31
3.1.3 Quy trình gán nhãn dữ liệu thực ......................................................... 32
3.1.4 Phân tích sơ bộ dữ liệu thực ................................................................ 34
3.2 Quy trình xây dựng bộ dữ liệu tạo sinh vòng đầu tiên (Phase 1) ............... 34
3.2.1 Nền tảng xây dựng dữ liệu tạo sinh và hệ phân tầng .......................... 35
3.2.2 Kiến trúc Prompt 4 Tầng ..................................................................... 38
3.2.3 Pipeline sinh dữ liệu và đánh giá chất lượng ...................................... 40
5

3.3 Cải thiện và đánh giá định lượng dữ liệu ................................................... 41
3.3.1 Các biện pháp đã áp dụng ................................................................... 41
3.3.2 Đánh giá định lượng bộ dữ liệu tạo sinh ............................................. 44
a) Đa dạng dữ liệu và mức độ lặp mẫu ................................................... 44
b) Giảm artifact leet và tình trạng obfuscation quá mức ......................... 45
c) Độ dài văn bản gần dữ liệu thực hơn .................................................. 45
3.4 Quy trình mở rộng bộ siêu dữ liệu (Metadata Schema v2) ........................ 46
3.4.1 Lược đồ Metadata Schema v2 ............................................................ 46
3.4.2 Quy trình thử nghiệm Pilot và tối ưu hóa Prompt .............................. 46
3.5 Phân tích bộ dữ liệu tổng thể (ViSmish) .................................................... 50
3.5.1 Thành phần cấu trúc bộ dữ liệu ........................................................... 50
3.5.2 Phân phối đặc trưng siêu dữ liệu (Metadata) ...................................... 51
CHƯƠNG 4 PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM .................... 61
4.1 Tổng quan thiết kế thực nghiệm ................................................................. 61
4.2 Các phương pháp đánh giá ......................................................................... 62
4.3 Các độ đo đánh giá ..................................................................................... 63
4.4 Thiết lập môi trường và tham số ................................................................ 66
CHƯƠNG 5 KẾT QUẢ VÀ PHÂN TÍCH .......................................................... 70
5.1 RQ1: Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu
ViSmish? ............................................................................................................... 70
5.2 RQ2: Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế
nào đến khả năng phát hiện smishing? .................................................................. 71
5.3 RQ3: Mô hình sai ở đâu và tại sao? ........................................................... 76
6

5.4 RQ4: Knowledge distillation có giúp mô hình nhẹ hơn đạt trade-off tốt hơn
không? ................................................................................................................... 80
CHƯƠNG 6 KẾT LUẬN ..................................................................................... 83
6.1 Kết quả đạt được ........................................................................................ 83
6.2 Hạn chế ....................................................................................................... 84
6.3 Phương hướng phát triển trong tương lai ................................................... 85
TÀI LIỆU THAM KHẢO ......................................................................................... 87
PHỤ LỤC .................................................................................................................. 92
7

PHỤ LỤC HÌNH
Hình 1 Định nghĩa bài toán nhận diện tin nhắn lừa đảo ........................................... 24
Hình 2 Quy trình thu thập dữ liệu thực và gán nhãn ................................................. 30
Hình 3 Quy trình tăng cường dữ liệu bằng LLM ...................................................... 38
Hình 4 Các bước cải thiện bộ dữ liệu ........................................................................ 43
Hình 5 Tương quan giữa chủ đề tin nhắn và hành động được yêu cầu thực hiện .... 55
Hình 6 Phân phối chiến thuật thuyết phục theo miền tin nhắn ................................. 56
Hình 7 Biểu đồ so sánh tỉ lệ các kĩ thuật che giấu văn bản trong tin nhắn thực và tạo
sinh ............................................................................................................................ 57
Hình 8 Biểu đồ thống kê mối liên hệ giữa đối tượng được nhận và chủ đề tin nhắn58
Hình 9 WordCloud của data thực và data tạo sinh theo từng nhãn .......................... 59
Hình 10 Quy trình thực nghiệm tổng quát ................................................................ 62
Hình 11 Hiệu năng của mô hình theo độ dài tin nhắn............................................... 72
8

PHỤ LỤC BẢNG
Bảng 1. Thống kê phân phối dữ liệu cho từng nhãn obfuscation level của dữ liệu tạo
sinh ............................................................................................................................ 42
Bảng 2. So sánh mức độ tương đồng nearest-neighbor trước và sau cải thiện ......... 44
Bảng 3. So sánh độ lặp n-gram dữ liệu tạo sinh trước và sau cải thiện .................... 44
Bảng 4. So sánh mức độ leet trước và sau cải thiện.................................................. 45
Bảng 5. So sánh phân phối độ dài văn bản trước và sau cải thiện ............................ 45
Bảng 6. Mức độ đồng thuận sau từng lần cải thiện prompt. ..................................... 49
Bảng 7. Phân bố mẫu theo nguồn gốc dữ liệu và nhãn ............................................. 51
Bảng 8. Thống kê độ dài theo nhãn phân loại tin nhắn ............................................. 51
Bảng 9. Thống kê phân phối chủ đề tin nhắn theo 2 nhãn ham và smishing ............ 53
Bảng 10. Thống kê thuộc tính has_URL với từng nhãn phân loại ........................... 53
Bảng 11. Phân phối của đặc trưng thủ thuật che giấu văn bản ................................. 54
Bảng 12. Định nghĩa 4 độ đo chính .......................................................................... 66
Bảng 13. Phân phối train/dev/test ............................................................................. 67
Bảng 14. Thiết lập tham số nhóm Character-level model......................................... 68
Bảng 15. Thiết lập tham số nhóm Encoder PLM fine-tuning ................................... 69
Bảng 16 Thiết lập tham số nhóm LLM fine-tuning .................................................. 69
Bảng 17 Kết quả benchmark 17 cấu hình trên 2 tập dev, test ................................... 70
Bảng 18. Phân tích kết quả theo một số lát cắt khác ................................................. 73
Bảng 19. Phân tích hiệu quả của mô hình đối với một số thủ đoạn lừa đảo ............. 75
Bảng 20. Phân loại số lượng mẫu lỗi của các mô hình ............................................. 76
Bảng 21. Bảng ma trận giao thoa lỗi Jaccard giữa các mô hình ............................... 77
Bảng 22. Bảng phân tích tất cả lí do lỗi mô hình gặp phải ....................................... 80
Bảng 23. Chênh lệch Recall Label 1 trên test so với TextCNN hard baseline ......... 81
Bảng 24. So sánh chi phí triển khai của PhoBERT-base với các TextCNN student 82
9

TÓM TẮT KHÓA LUẬN
Trong bối cảnh các cuộc tấn công lừa đảo qua tin nhắn (smishing) tại Việt Nam
ngày càng tinh vi, các phương pháp phát hiện dựa trên luật truyền thống gặp nhiều
hạn chế trước văn bản ngắn, phi chuẩn, có dấu hiệu ngụy trang và thường xuyên thay
đổi về ngữ cảnh. Bài toán phát hiện smishing tiếng Việt còn chịu hai thách thức lớn:
thiếu bộ dữ liệu SMS chất lượng cao có nhãn đáng tin cậy, và khó triển khai các mô
hình ngôn ngữ lớn trong môi trường tài nguyên hạn chế.
Khóa luận xây dựng bộ dữ liệu ViSmish gồm 10.562 mẫu, kết hợp dữ liệu thật,
dữ liệu chéo miền, dữ liệu tạo sinh, dữ liệu paraphrase và các mẫu hard positive/hard
negative. Trên cơ sở đó, nghiên cứu thiết lập một benchmark thống nhất gồm 17 cấu
hình mô hình, bao gồm mô hình cấp ký tự, mô hình ngôn ngữ tiền huấn luyện được
fine-tune và các mô hình ngôn ngữ lớn được thích nghi bằng LoRA. Các mô hình
được đánh giá trên cùng train/dev/test split bằng bốn độ đo chính: Macro-F1, F1 Label
1, Recall Label 1 và PR-AUC.
Kết quả thực nghiệm cho thấy Gemma 2B là mô hình tốt nhất theo tiêu chí chính
Macro-F1 trên tập dev và tiếp tục duy trì kết quả cao nhất trên tập test. Tuy nhiên,
không có một mô hình duy nhất tối ưu cho mọi mục tiêu vận hành: DistilBERT
multilingual nổi bật khi ưu tiên Recall Label 1, trong khi Qwen2.5 0.5B đạt PR-AUC
cao nhất trên dev. Phân tích theo lát cắt metadata v2.1 cho thấy hiệu năng mô hình
thay đổi đáng kể theo độ dài tin nhắn, sự xuất hiện của URL, lĩnh vực tin nhắn, hành
động yêu cầu, vai trò đối tượng và thủ đoạn thuyết phục. Các lỗi khó nhất thường rơi
vào smishing không chứa URL, tin nhắn đòi nợ có văn phong pháp lý, thông báo hợp
lệ có lời kêu gọi hành động giống lừa đảo, và văn bản hội thoại phi chuẩn.
Bên cạnh benchmark chính, khóa luận phân tích chuyên sâu knowledge
distillation trên TextCNN với ba teacher: PhoBERT-base, CafeBERT và ViCLSR.
Kết quả cho thấy distillation không tự động cải thiện student; hiệu quả phụ thuộc
mạnh vào teacher và chiến lược sử dụng soft label. Risk-aware KD cải thiện Recall
10

Label 1 rõ nhất khi dùng PhoBERT-base, trong khi vanilla KD phù hợp hơn với
CafeBERT, còn ViCLSR không mang lại lợi ích trong cấu hình hiện tại. Về triển
khai, TextCNN cho thấy lợi thế lớn về kích thước và độ trễ suy luận; tuy nhiên lợi
thế này đến từ kiến trúc nhẹ, còn distillation chủ yếu tác động đến chất lượng dự đoán.
Nhìn chung, khóa luận đóng góp một benchmark có hệ thống cho bài toán phát
hiện smishing tiếng Việt, cung cấp phân tích sâu về các yếu tố dữ liệu ảnh hưởng đến
hiệu năng mô hình, chỉ ra các nhóm lỗi quan trọng cần cải thiện, và đánh giá thận
trọng vai trò của knowledge distillation trong việc cân bằng giữa chất lượng phát hiện
và chi phí triển khai.
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
gia tăng chóng mặt. Theo dữ liệu từ Allure Security, năm 2020 ghi nhận số vụ lừa
đảo qua tin nhắn SMS đã tăng mạnh 328%1. Xu hướng này không có dấu hiệu chậm
lại, khi báo cáo năm 2025 của Zimperium chỉ ra mức tăng trưởng ổn định 22% hàng
năm đối với lừa đảo qua tin nhắn SMS, và đáng chú ý là 69,3% tổng số vụ lừa đảo
vào năm 2025 được thực hiện qua tin nhắn SMS2.
Tại Việt Nam, vấn đề này đang xảy ra trên quy mô lớn, gây ra những hậu quả
kinh tế vô cùng nặng nề cho người dùng cá nhân. Một cuộc khảo sát toàn diện của
Hiệp hội An ninh mạng quốc gia cho thấy, cứ 220 người dùng di động tại Việt Nam
thì có 1 người là nạn nhân của các vụ lừa đảo trực tuyến, tương đương với tỷ lệ rủi ro
là 0,45%. Tổng thiệt hại về tài chính do lừa đảo trực tuyến gây ra cho người dân cả
nước trong năm 2024 ước tính đạt 18.900 tỷ đồng, một số báo cáo kiểm toán độc lập
thậm chí ghi nhận mức biến động tối thiểu là 12.000 tỷ đồng3. Nguy cơ tin nhắn lừa
đảo (phishing) xuất phát từ chính đặc điểm của tin nhắn SMS. Trong khi email chỉ
đạt tỷ lệ mở trung bình khoảng 20%, tin nhắn SMS có tỷ lệ mở tức thì lên đến 98%.
Lợi dụng lòng tin và thói quen giao dịch qua điện thoại thông minh, tội phạm mạng
liên tục phát tán hàng triệu tin nhắn lừa đảo mỗi ngày.
Để đối phó, các cơ quan quản lý nhà nước đã ban hành nhiều chính sách và
chỉ thị nghiêm ngặt nhằm siết chặt quản lý không gian mạng. Các ví dụ đáng chú ý
bao gồm Nghị định Chính phủ số 91/2020/ND-CP về phòng chống tin nhắn
rác, email rác và cuộc gọi rác, và Chỉ thị số 82/CT-BTTTT của Bộ Thông tin và
1 Smishing Statistics: Why SMS Phishing Grew 328% Since 2020 - Allure Security
2 2025 Global Mobile Threat Report
3 Thiệt hại do lừa đảo trực tuyến ước tính 18.900 tỷ đồng năm 2024
12

Truyền thông về phòng chống tin nhắn rác, tin nhắn lừa đảo và tăng cường quản lý
thông tin trực tuyến. Mặc dù các nhà cung cấp dịch vụ viễn thông đã triển khai nhiều
giải pháp lọc đầu cuối, số lượng báo cáo về tin nhắn lừa đảo gửi đến các cổng tiếp
nhận quốc gia vẫn tiếp tục tăng. Theo kết quả khảo sát của Hiệp hội An ninh mạng
quốc gia, 70,72% người dùng từng nhận được lời mời đầu tư tài chính vào các sàn
giao dịch không rõ nguồn gốc nhưng cam kết không rủi ro, lợi nhuận cao. 62,08%
người dùng cho biết, gặp phải các cuộc gọi mạo danh cơ quan, tổ chức (công
an, toà án, thuế, ngân hàng…) thúc giục cài phần mềm hoặc đe doạ phải chuyển tiền
để chứng minh trong sạch do liên quan vi phạm pháp luật. 60,01% người dùng cho
biết, nhận được các thông báo trúng thưởng, khuyến mãi cao nhưng thông tin rất mập
mờ, bất thường. Điều này cho thấy bọn lừa đảo đang sử dụng các chiến dịch đa kênh,
tích hợp linh hoạt các tin nhắn dụ dỗ và cuộc gọi giả mạo để tối đa hóa tỷ lệ đánh cắp
tài sản.
1.2 Động lực nghiên cứu
Trước sự leo thang và phát triển không ngừng của các hình thức tấn công kỹ
thuật số, các phương pháp phát hiện truyền thống chủ yếu dựa trên việc phân tích đặc
trưng tĩnh để thiết kế các luật cứng (rule-based) đã nhanh chóng bộc lộ giới hạn, dễ
dàng bị vượt qua bởi các biến thể tin nhắn ngày càng tinh vi và đa dạng. Các đối
tượng lừa đảo dễ dàng lách qua các bộ lọc từ khóa tĩnh bằng cách cố tình thay đổi ký
tự, chèn ký tự đặc biệt, viết tắt hoặc tráo đổi cấu trúc ngữ pháp. Để giải quyết triệt để
bài toán đó, xu hướng ứng dụng các mô hình học máy (Machine Learning) kết hợp
cùng kỹ thuật xử lý ngôn ngữ tự nhiên (NLP) đã trở thành mũi nhọn công nghệ trong
cuộc chiến chống tin nhắn lừa đảo [1].
Tuy nhiên, hiệu quả của phương pháp hiện đại này phụ thuộc hoàn toàn vào
chất lượng và quy mô của tập dữ liệu huấn luyện. Đối với bối cảnh cụ thể tại Việt
Nam, điều này thực sự đặt ra một thách thức đáng kể. Thông qua nghiên cứu và tổng
quan tài liệu, chúng tôi nhận thấy hiện nay không có tập dữ liệu chuyên biệt, chuẩn
hóa nào về tin nhắn lừa đảo bằng tiếng Việt được công khai cho mục đích nghiên cứu.
13

Việc thu thập dữ liệu tin nhắn cũng gặp phải những trở ngại đáng kể liên quan đến
bảo mật thông tin cá nhân và nguồn thu thập khả dĩ. Hơn nữa, tiếng Việt trong tin
nhắn SMS rất phức tạp với nhiều biến thể. Đối tượng lừa đảo và cả người dùng đều
thường xuyên sử dụng từ viết tắt, tiếng lóng, ngôn ngữ hỗn hợp hoặc tin nhắn không
dấu.
Việc thiếu dữ liệu huấn luyện và sự phức tạp của ngữ cảnh tiếng Việt là những
rào cản lớn nhất hạn chế sự phát triển của hệ thống cảnh báo thông minh tại Việt
Nam. Để khắc phục tình trạng thiếu dữ liệu này, các kỹ thuật nâng cao dữ liệu truyền
thống (như hoán đổi từ và loại bỏ từ ngẫu nhiên) thường làm gián đoạn cấu trúc ngữ
pháp và ngữ nghĩa của câu, dẫn đến việc tạo ra nhiễu gây bất lợi cho mô hình. Sự
xuất hiện của Mô hình Ngôn ngữ Lớn (LLM) đã mở ra một hướng đi mới đầy hứa
hẹn, cho phép tạo ra dữ liệu văn bản chất lượng cao, đa dạng về ngữ cảnh và cấu trúc
câu trong khi vẫn duy trì các nhãn ngữ nghĩa cốt lõi .
Mặc dù LLM sở hữu khả năng nhận dạng và tạo dữ liệu vượt trội, việc triển
khai trực tiếp các mô hình khổng lồ này để chạy phân loại tin nhắn thời gian thực trên
thiết bị di động cá nhân hoặc hệ thống viễn thông vấp phải những hạn chế về tài
nguyên phần cứng, độ trễ xử lý và chi phí vận hành [2]. Do đó, nghiên cứu này thử
nghiệm một giải pháp huấn luyện một mô hình học sâu nhỏ gọn (Mô hình Học sinh),
được tối ưu thông qua các kỹ thuật chưng cất tri thức từ các mô hình giáo viên thuộc
nhóm mô hình Transformer NLP. Cách tiếp cận này cho phép mô hình học sinh kế
thừa tín hiệu phân phối xác suất từ giáo viên, đồng thời đảm bảo thời gian phản hồi
nhanh hơn, chi phí triển khai thấp hơn trên các thiết bị có tài nguyên hạn chế.
1.3 Đối tượng, phạm vi nghiên cứu và mục tiêu bài toán
Đối tượng nghiên cứu:
• Bộ dữ liệu tin nhắn SMS lừa đảo tiếng Việt, bao gồm các biến thể ngôn ngữ
đúng ngữ pháp, ngôn ngữ không trọng âm, viết tắt và cấu trúc ký tự đặc trưng
được sử dụng bởi những kẻ lừa đảo.
14

• Các phương pháp tăng cường dữ liệu văn bản (Data Augmentation) dựa trên
Mô hình Ngôn ngữ Lớn (LLM).
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
• Về dữ liệu: Bộ dữ liệu sử dụng trong nghiên cứu bao gồm dữ liệu SMS thực
được thu thập, gán nhãn thủ công và dữ liệu tạo sinh dùng để tăng cường tập
huấn luyện. Do giới hạn về thời gian, nguồn lực và khả năng tiếp cận dữ liệu
lừa đảo thực tế, tập dữ liệu chưa thể bao phủ đầy đủ toàn bộ biến thể ngôn ngữ,
lĩnh vực lừa đảo, nhà mạng, vùng miền, thời điểm phát sinh chiến dịch và
chiến thuật né lọc có thể xuất hiện trong môi trường thực tế. Dữ liệu tạo sinh
chỉ được sử dụng như nguồn bổ sung cho quá trình huấn luyện, không được
đưa vào tập phát triển và tập kiểm thử, nhằm hạn chế việc đánh giá mô hình
trên các mẫu có phân phối quá gần với dữ liệu sinh. Vì vậy, kết quả thực
nghiệm phản ánh hiệu quả của mô hình trên phạm vi bộ dữ liệu ViSmish và
giao thức đánh giá đã xây dựng trong nghiên cứu này.
• Về phương pháp: Nghiên cứu tập trung vào bài toán phân loại nhị phân tin
nhắn SMS tiếng Việt thành hai nhóm: tin nhắn hợp lệ và tin nhắn lừa đảo. Các
phương pháp được khảo sát bao gồm mô hình học sâu cấp ký tự như BiLSTM
15

và TextCNN, các mô hình ngôn ngữ tiền huấn luyện được fine-tune như
PhoBERT, CafeBERT, ViCLSR, mBERT, XLM-RoBERTa, DistilBERT
multilingual, và một số mô hình ngôn ngữ lớn được thích nghi bằng LoRA [3]
như Gemma và Qwen. Việc đánh giá được thực hiện trong cùng một giao thức
dữ liệu train/dev/test, sử dụng các độ đo Macro-F1, F1 cho lớp smishing,
Recall cho lớp smishing và PR-AUC. Nghiên cứu không đi sâu vào các
phương pháp dựa trên luật thủ công, hệ thống lọc thời gian thực của nhà mạng,
hoặc các cơ chế phát hiện đa phương thức ngoài nội dung văn bản SMS.
• Về kỹ thuật Chưng cất Tri thức: Nghiên cứu sử dụng chưng cất tri thức như
một hướng nhằm chuyển một phần năng lực dự đoán từ các mô hình teacher
lớn hơn sang các mô hình student nhẹ hơn, phù hợp hơn với bối cảnh triển
khai có giới hạn tài nguyên. Trong benchmark chính, PhoBERT-base được sử
dụng làm teacher để sinh soft label cho hai student cấp ký tự là BiLSTM và
TextCNN. Student được huấn luyện bằng hàm mất mát kết hợp giữa nhãn cứng
gốc và xác suất mềm từ teacher. Ngoài cấu hình chưng cất cơ bản, nghiên cứu
còn thực hiện phân tích chuyên sâu trên TextCNN với ba teacher gồm
PhoBERT-base, CafeBERT và ViCLSR, so sánh các chế độ hard-label, vanilla
knowledge distillation và risk-aware knowledge distillation. Phạm vi chưng
cất chỉ giới hạn ở phân loại nhị phân trên dữ liệu SMS tiếng Việt; nghiên cứu
không xem xét các kỹ thuật chưng cất phức tạp hơn như chưng cất tầng ẩn,
chưng cất attention, chưng cất chuỗi sinh hoặc chưng cất đa nhiệm.
Mục tiêu nghiên cứu:
• Xây dựng bộ dữ liệu SMS tiếng Việt phục vụ bài toán phát hiện tin nhắn lừa
đảo, kết hợp dữ liệu thực được gán nhãn thủ công và dữ liệu tạo sinh bằng
LLM.
• Đánh giá hiệu quả của nhiều nhóm mô hình phân loại, bao gồm mô hình học
sâu cấp ký tự, mô hình ngôn ngữ tiền huấn luyện và mô hình ngôn ngữ lớn
được fine-tune.
16

• Khảo sát khả năng chưng cất tri thức từ mô hình teacher sang các mô hình
student gọn nhẹ hơn nhằm phục vụ bối cảnh triển khai hạn chế tài nguyên.
• Phân tích các lỗi False Positive và False Negative để nhận diện những hạn chế
còn tồn tại của dữ liệu và mô hình.
Đóng góp khoa học:
• Xây dựng bộ dữ liệu smishing tiếng Việt gồm dữ liệu thực được gán nhãn thủ
công và dữ liệu tạo sinh theo quy trình có kiểm soát.
• Đề xuất quy trình tăng cường dữ liệu bằng LLM cho bài toán phát hiện tin
nhắn lừa đảo tiếng Việt.
• Thực nghiệm và so sánh nhiều nhóm mô hình trên cùng một giao thức đánh
giá, từ mô hình học sâu gọn nhẹ đến các mô hình ngôn ngữ tiền huấn luyện và
LLM fine-tune.
• Khảo sát bước đầu hiệu quả của chưng cất tri thức trong việc chuyển tri thức
từ mô hình teacher sang mô hình student nhẹ hơn cho bài toán phân loại SMS.
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
(scarcity) [4]. Mặc dù nghiên cứu của họ được thực hiện trên tập dữ liệu lừa đảo qua
email, nhưng các cơ chế thao túng tâm lý nhằm suy giảm tư duy phản biện của đối
tượng vẫn mang tính quy luật và hoàn toàn tương đồng khi áp dụng vào môi trường
tin nhắn SMS.
Sự nhất quán về đặc trưng ngôn ngữ thao túng này cũng được minh chứng rõ
nét qua thực tiễn tại Việt Nam. Khi phân tích các kịch bản tấn công được cảnh báo
trong Cẩm nang nhận diện và phòng chống lừa đảo trực tuyến do Cục An toàn Thông
tin phát hành, có thể dễ dàng nhận thấy những điểm chung: việc lạm dụng ngôn từ đe
dọa để ép buộc nạn nhân hành động khẩn cấp chính là chiến thuật cốt lõi của phần
lớn các hình thức lừa đảo hiện nay4. Nhìn sang góc độ dữ liệu, thủ đoạn này để lại
những đặc trưng ngôn ngữ rất rõ nét. Các văn bản lừa đảo thường có rất nhiều các từ
khóa ám chỉ giới hạn thời hạn, động từ mệnh lệnh, dấu chấm than và đặc biệt là các
cấu trúc cưỡng chế có điều kiện (ví dụ: “nếu không… thì…”). Đối với bài toán phân
loại bằng các mô hình học máy và đặc biệt là Mô hình ngôn ngữ lớn (ML/LLM), đây
là một cụm đặc trưng có giá trị cao. LLM không chỉ học cách nhận diện tần suất của
các từ vựng đơn lẻ, mà còn có khả năng nắm bắt toàn bộ khuôn khổ ngữ nghĩa mang
tính thao túng: yêu cầu hành động tức thời, triệt tiêu khả năng kiểm tra chéo thông tin
của nạn nhân và nhấn mạnh hậu quả tất yếu nếu sự việc bị chậm trễ.
4 Cam-nang-nhan-dien-va-phong-chong-lua-dao-truc-tuyen.pdf
20

Cấu trúc văn bản bất thường, sai chính tả có chủ đích, hoặc “làm méo”
chữ viết: Một đặc trưng quan trọng khác là sự bất thường về hình thức và cấu trúc
văn bản. Để né tránh các hệ thống phát hiện dựa trên bộ lọc từ khóa (keyword-based
filters) truyền thống, các đối tượng lừa đảo thường chủ động áp dụng các kỹ thuật
ngụy trang văn bản (text obfuscation). Những thủ đoạn này được thể hiện thông qua
việc cố tình viết sai chính tả, loại bỏ dấu, chia tách từ một cách bất thường, chèn ký
tự đặc biệt ngẫu nhiên, thay chữ cái bằng ký tự đồng hình. Sự bất thường trên là một
trong những dấu hiệu cảnh báo lừa đảo bề mặt dễ nhận biết nhất, cùng với liên kết
đáng ngờ. Các đánh giá tổng quan cũng khẳng định lỗi ngữ pháp và chính tả là những
chỉ báo điển hình của một kịch bản lừa đảo [5]. Một nghiên cứu theo dõi chuyển động
mắt cũng cho thấy email phishing có lỗi chính tả sẽ làm giảm đáng kể mức độ đánh
giá tin cậy của người dùng [6].
Riêng với tiếng Việt, các nghiên cứu trong nước cho thấy ngôn ngữ là yếu tố
rất quan trọng: cùng một mô hình phát hiện lừa đảo nhưng ngôn ngữ đầu vào khác
nhau có thể đòi hỏi cách phát hiện khác nhau. Một nghiên cứu về phát hiện phishing
email tiếng Việt [7] đã nêu rõ rằng “mỗi ngôn ngữ cụ thể” có thể dẫn đến “một cách
tiếp cận phát hiện khác nhau”, trong khi một nghiên cứu khác về spam email tiếng
Việt [8] chỉ ra rằng dấu thanh, cấu trúc ngữ pháp khác biệt và sắc thái ngữ cảnh làm
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
21

kèm với tên thương hiệu nhằm tạo cảm giác “chính chủ”. Các liên kết thường có tên
miền gần giống thương hiệu thật (ví dụ: vietcomb@nk-cb.com, vcb-digib@nk.xyz)
hoặc sử dụng các dịch vụ rút gọn link (tinylink, bit.ly) nhằm che giấu đích đến thực
tế. FBI lưu ý rằng spoofing/phishing có thể chỉ cần đổi một chữ cái, một ký hiệu, hoặc
một con số để đánh lừa người dùng; nghiên cứu về IDN homograph [9] cũng cho thấy
các homoglyph (ký tự Unicode trông giống nhau) là một rủi ro an ninh thường trực
và rất hay được sử dụng trong tấn công lừa đảo.
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
22

xuất hiện các kịch bản tương tự nhau theo từng đợt, từng khoảng thời gian, khiến cho
số lượng mẫu bị hạn chế; song cũng liên tục thay đổi kịch bản theo thời gian và các sự
kiện xã hội, khiến các tập dữ liệu tĩnh nhanh chóng trở nên lỗi thời. Sự thiếu hụt này
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
23

toán tập trung vào việc học ranh giới giữa hai nhóm tin nhắn: tin nhắn hợp lệ và tin
nhắn lừa đảo. Đây là một ranh giới không đơn giản, vì nhiều tin nhắn lừa đảo cố tình
mô phỏng văn phong của tổ chức thật, trong khi một số tin nhắn hợp lệ cũng có thể
chứa các yếu tố dễ gây nhầm lẫn như liên kết/liên kết rút gọn, mã OTP, cảnh báo bảo
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
x = {w , w , …, w }
i 1 2 n
Trong đó x là chuỗi văn bản SMS gồm n token hoặc ký tự sau bước tiền xử lý
i
tùy theo mô hình được sử dụng. Tin nhắn có thể ở dạng có dấu, không dấu, viết tắt,
chứa ký hiệu, số điện thoại, liên kết, tên miền, mã giao dịch, OTP hoặc các biến thể
obfuscation như “T1en”, “kho@”, “th0ng ba0”. Trong bộ dữ liệu, ngoài trường nội
24

dung huấn luyện chính là cột content, mỗi mẫu còn có các metadata hỗ trợ phân tích
và đánh giá dữ liệu. Tuy nhiên, trong bài toán phân loại cốt lõi, đầu vào chính của mô
hình vẫn là nội dung tin nhắn SMS. Các metadata được dùng chủ yếu cho quá trình
xây dựng dữ liệu, kiểm tra chất lượng, chia tập dữ liệu, phân tích lỗi và đánh giá theo
từng nhóm.
Đầu ra của bài toán là nhãn phân loại y {0 ; 1}, cho biết tin nhắn thuộc lớp
i
hợp lệ hay lớp lừa đảo. Mục tiêu là học một hàm phân loại: f: X → {0, 1} sao cho với
mỗi tin nhắn SMS mới, mô hình có thể dự đoán chính xác tin nhắn đó là hợp lệ hay
lừa dảo. Với các mô hình huấn luyện, đầu ra cũng có thể được biểu diễn dưới dạng
xác suất như sau:
𝑦ˆ = 𝑃(𝑦 = 1 ∣ 𝐱)
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
25

nhắn là lừa đảo. Mô hình cần học sự khác biệt giữa sự khẩn cấp hợp lệ và khẩn
cấp thao túng, giữa domain thật và domain giả mạo, giữa thông báo chính
thống và nội dung giả danh.
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
Tóm lại, bài toán trong nghiên cứu này không chỉ là nhận diện spam thông
thường, mà là phát hiện tin nhắn lừa đảo tiếng Việt trong bối cảnh dữ liệu mất cân
bằng, nội dung ngắn, nhiều văn bản nhiễu và có sự chồng lấn đáng kể giữa tin nhắn
hợp lệ và tin nhắn giả mạo. Mục tiêu cuối cùng là xây dựng mô hình có khả năng phát
hiện tốt lớp Label 1, đồng thời hạn chế nhầm lẫn các tin nhắn hợp lệ có bề mặt giống
smishing thành lừa đảo.
2.2 Các công trình nghiên cứu liên quan
2.2.1 Nghiên cứu sử dụng dữ liệu tạo sinh trong phân loại văn bản
Phương pháp xây dựng bộ dữ liệu SMS dựa trên ba nhóm nghiên cứu nền tảng,
bao gồm phát hiện spam/smishing, đặc trưng cấu trúc tin nhắn, và tăng cường dữ liệu
bằng LLM. Về phát hiện smishing và vai trò của obfuscation, Mishra & Soni trong
công trình DSmishSMS [10] xác nhận rằng leet words và từ viết sai có chủ đích là
26

heuristic phân biệt smishing với tin nhắn hợp lệ. Một tổ chức uy tín sẽ không bao giờ
sử dụng các kỹ thuật này, đây là căn cứ lý thuyết nền cho toàn bộ Obfuscation
Taxonomy của Label 1. Nghiên cứu về kỹ thuật evasion trong lọc SMS spam [11]
phân phân loại các kỹ thuật của kẻ tấn công thành ba nhóm: biến đổi ký tự (character
obfuscation), thao túng từ vựng (lexical manipulation), và gây nhiễu có chủ đích
(crafted perturbations). Nghiên cứu cũng cảnh báo về concept drift khi mô hình thất
bại với các pattern obfuscation mới, nhấn mạnh sự cần thiết của dữ liệu đa dạng theo
mức độ obfuscation. GCC-Spam Framework [12] xây dựng mạng lưới tương đồng
ký tự để nắm bắt đặc trưng chính tả và âm vị học nhằm đối phó với các tấn công
character-obfuscation, cho thấy cần có dữ liệu huấn luyện phân tầng theo mức độ
obfuscation để mô hình đạt được độ bền thực sự. Almeida et al [13] qua hệ thống
đánh giá 83 bài báo cũng xác nhận khoảng trống lớn trong việc cải thiện bộ phân loại
đối với tin nhắn bị obfuscate nặng - đặc biệt trong bối cảnh tiếng Việt với hệ thống
diacritics Unicode phức tạp. Ngoài ra, nghiên cứu về xây dựng tập dữ liệu smishing
đa lớp của tác giả Alicia Martínez-Mendoza cũng xác nhận smishing có thể được
phân loại theo kịch bản tâm lý mà kẻ tấn công tạo ra (tham lam, sợ hãi, quyền lực)
[14], là cơ sở để áp dụng bốn chiến lược tâm lý vào tám category smishing trong
nghiên cứu này.
Về đặc trưng phong cách của tin nhắn hợp lệ, Sohn, Lee & Rim [15] là công
trình kinh điển đề xuất sử dụng stylistic features (đặc trưng phong cách viết) trong
biểu diễn SMS song song với đặc trưng ngữ nghĩa, đạt kết quả tốt nhất với 250 đặc
trưng từ vựng và phong cách bất kể ngôn ngữ - đây là nền tảng lý thuyết cho Formality
Taxonomy của Label 0. Hosseinpour & Shakibian [16] trích xuất đồng thời ba loại
đặc trưng từ SMS bao gồm thống kê, ngữ pháp, và cấu trúc mạng phức tạp, cho thấy
cấu trúc của tin nhắn (không chỉ từ vựng) là đặc trưng phân loại mạnh, đóng góp trực
tiếp cho việc phân loại tin nhắn hợp lệ theo độ cứng nhắc của template. Jain et al. [17]
xác nhận phân tích URL (tên miền, TLD, brand name trong domain) là đặc trưng
mạnh phân biệt smishing với ham, là cơ sở lý thuyết cho các pattern domain hợp lệ
(.vn, .gov.vn) so với domain giả mạo (.vip, .top, .icu) trong cả hai taxonomy. Điểm
27

mới của nghiên cứu này so với các công trình đi trước là đề xuất label-aware structural
taxonomy - phân tầng đặc trưng bên trong từng nhãn - thay vì dùng một tập feature
chung cho toàn bộ corpus.
2.2.2 Nghiên cứu về Chưng cất tri thức trên mô hình ngôn ngữ
Chưng cất tri thức (Knowledge Distillation - KD) là hướng tiếp cận nhằm
chuyển tri thức từ một mô hình lớn, thường gọi là teacher, sang một mô hình nhỏ
hơn, gọi là student. Ý tưởng này bắt nguồn từ hướng nén mô hình của Buciluă et al.
[18] và được hệ thống hóa rõ ràng hơn bởi Hinton, Vinyals & Dean [19]. Thay vì chỉ
huấn luyện student bằng nhãn cứng 0/1, KD sử dụng thêm phân phối xác suất đầu ra
của teacher. Các xác suất mềm này chứa thông tin về mức độ chắc chắn của teacher
đối với từng lớp, nhờ đó student có thể học được quan hệ ranh giới giữa các lớp tốt
hơn so với việc chỉ học từ nhãn phân loại cuối cùng.
Trong công trình nền tảng của tác giả Hinton, temperature được sử dụng để
làm mềm phân phối xác suất của teacher. Khi temperature lớn hơn 1, phân phối đầu
ra bớt cực đoan hơn, giúp student nhận thêm tín hiệu về các trường hợp không hoàn
toàn rõ ràng. Cách tiếp cận này đặc biệt phù hợp với bài toán phân loại văn bản ngắn
như SMS, nơi nhiều tin nhắn smishing và tin nhắn hợp lệ có thể chia sẻ các đặc trưng
bề mặt tương tự nhau, chẳng hạn lời kêu gọi hành động, đường dẫn URL, số điện
thoại hoặc giọng điệu khẩn cấp.
Trong lĩnh vực xử lý ngôn ngữ tự nhiên, nhiều nghiên cứu đã áp dụng KD để
giảm chi phí triển khai của các mô hình Transformer lớn. DistilBERT của Sanh et al.
[20] là một ví dụ tiêu biểu, cho thấy có thể tạo ra mô hình nhỏ hơn và nhanh hơn
BERT trong khi vẫn giữ phần lớn năng lực hiểu ngôn ngữ. Công trình của Tang et al.
[21], trong đó tri thức từ BERT được chưng cất sang các mạng neural đơn giản hơn
như BiLSTM. Kết quả của nghiên cứu này cho thấy các mô hình student nhẹ vẫn có
thể đạt hiệu quả cạnh tranh trên một số tác vụ NLP khi được học từ teacher mạnh
hơn, đồng thời giảm đáng kể số tham số và thời gian suy luận. Mukherjee &
Awadallah [22] cũng chỉ ra rằng việc chưng cất BERT sang các student đơn giản có
28

thể hữu ích trong bối cảnh dữ liệu gán nhãn hạn chế, đặc biệt khi có thêm tập dữ liệu
transfer phù hợp miền.
Từ các nghiên cứu trên, có thể thấy phát hiện tin nhắn lừa đảo không còn chỉ
là bài toán lọc từ khoá đơn giản, mà là một bài toán phân loại văn bản ngắn trong đi
ều kiện dữ liệu nhiễu, nhiều biến thể ngôn ngữ và có sự thay đổi liên tục theo thời gi
an. Trên cơ sở đó, khoá luận định nghĩa bài toán phát hiện tin nhắn lừa đảo như một
bài toán phân loại văn bản có giám sát, trong đó mỗi tin nhắn đầu vào được gán vào
một trong các lớp nhãn được xác định trước.
CHƯƠNG 3 XÂY DỰNG VÀ PHÂN TÍCH DỮ LIỆU
Chương này trình bày chi tiết về quy trình xây dựng bộ dữ liệu phát hiện tin nhắn
lừa đảo tiếng Việt (ViSmish). Quy trình bao gồm: thu thập và gán nhãn tập dữ liệu
thực (ground truth), thiết kế pipeline tạo sinh dữ liệu vòng đầu bằng các Mô hình
Ngôn ngữ Lớn (LLM), thực hiện các biện pháp cải biên kỹ thuật để nâng cao chất
lượng và kiểm soát hiện tượng rò rỉ dữ liệu, quy trình gán nhãn siêu dữ liệu mở rộng
(Metadata Schema v2), và phân tích các đặc trưng phân phối tĩnh của bộ dữ liệu tổng
thể.
3.1 Quy trình thu thập, gán nhãn dữ liệu thực
Bộ dữ liệu thực tế (real data) đóng vai trò nền tảng, phản ánh chính xác nhất
phân phối của các tin nhắn SMS trong thế giới thực tại Việt Nam. Quá trình thu thập
và xử lý gán nhãn cho phần dữ liệu tin nhắn thực có thể chia làm 3 phần chính như
sơ đồ dưới đây.
29

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
tự Quang học (OCR) tiêu chuẩn diễn giải chính xác. Quy trình này đã tạo ra một tập
dữ liệu chất lượng cao gồm các dấu hiệu smishing riêng biệt, chủ yếu nhắm vào lĩnh
vực ngân hàng và thương mại điện tử.
Tuy nhiên, điểm hạn chế của phương pháp này là số lượng mẩu lừa đảo mà
chúng tôi thu thập được là rất ít. Điều này một phần xuất phát từ việc các bài cảnh
30

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
thông báo/quảng cáo từ nhà mạng. Với mục đích này, Nhóm nghiên cứu tiến hành
trích xuất tin nhắn SMS trực tiếp từ thiết bị di động cá nhân của các thành viên và
tình nguyện viên là sinh viên ngành CNTT thuộc Trường Đại học Công nghệ Thông
tin (UIT), trong độ tuổi 21-22; dữ liệu tin nhắn được chốt vào tháng 11/2025. Luồng
dữ liệu này chủ yếu cung cấp các tin nhắn hợp lệ bao gồm: thông báo mã OTP từ
ngân hàng/dịch vụ trực tuyến, tin nhắn chăm sóc khách hàng (SMS Brandname) của
các nhà mạng, tin nhắn quảng cáo và tin nhắn trao đổi cá nhân.. Với sự đồng ý rõ
ràng của các thành viên trong nhóm nghiên cứu và các tình nguyện viên tham gia,
ứng dụng này được dùng để xuất kho tin nhắn cục bộ từ điện thoại của các cá nhân
tham gia sang định dạng XML có cấu trúc. Cách tiếp cận này cho phép chúng tôi trích
xuất hiệu quả nội dung tin nhắn, dấu thời gian và thông tin người gửi mà không cần
phát triển một trình thu thập dữ liệu tùy chỉnh, qua đó tinh giản quy trình thu thập dữ
liệu. Sau khi tổng hợp, làm sạch và chuẩn hóa dữ liệu từ cả hai nguồn, bộ dữ liệu hợp
nhất cuối cùng bao gồm tổng cộng 2.567 mẫu duy nhất.
31

3.1.3 Quy trình gán nhãn dữ liệu thực
Sau khi hoàn tất quá trình thu thập, làm sạch và chuẩn hóa dữ liệu, nhóm
nghiên cứu tiến hành gán nhãn cho bộ dữ liệu thực theo phương pháp gán nhãn cộng
tác dựa trên đồng thuận nhóm (collaborative annotation with consensus-based
decision). Bộ dữ liệu được gán nhãn theo bài toán phân loại nhị phân, trong đó mỗi
tin nhắn được gán vào một trong hai lớp: tin nhắn không lừa đảo (nhãn 0) và tin nhắn
lừa đảo (nhãn 1).
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
liệu và bài toán nghiên cứu:
Thứ nhất, quy mô bộ dữ liệu sau khi hợp nhất chỉ gồm 2.567 bản ghi duy
nhất, cho phép nhóm có thể cùng rà soát từng mẫu trong các phiên gán nhãn tập trung.
Thứ hai, bài toán trong phạm vi khoá luận là phân loại nhị phân, không phải
phân loại đa lớp với nhiều ranh giới nhãn phức tạp. Do đó, đối với phần lớn mẫu dữ
liệu, việc xác định tin nhắn có mang dấu hiệu lừa đảo hay không có thể được thực
hiện tương đối rõ ràng khi đối chiếu với ngữ cảnh và các dấu hiệu nhận biết đã thống
nhất.
Thứ ba, nhóm đã nhận thức trước tình trạng mất cân bằng nhãn nghiêm trọng
trong dữ liệu thực, đặc biệt là số lượng tin nhắn lừa đảo thực tế thu thập được rất hạn
chế. Sau quá trình gán nhãn, bộ dữ liệu chỉ có 246 mẫu thuộc lớp lừa đảo, cho thấy
32

việc rà soát cẩn thận từng mẫu là cần thiết nhằm hạn chế bỏ sót các trường hợp dương
tính.
Trong quá trình gán nhãn, nhóm sử dụng các tiêu chí nhận diện tin nhắn lừa
đảo dựa trên nội dung, mục đích giao tiếp và các dấu hiệu hành vi thường gặp. Một
tin nhắn được xem là lừa đảo nếu nội dung có mục đích dụ dỗ, thao túng hoặc đánh
lừa người nhận thực hiện một hành động có nguy cơ gây hại, chẳng hạn như truy cập
liên kết không đáng tin cậy, phát sinh vấn đề liên quan tới tài khoản ngân hàng, cung
cấp thông tin cá nhân, chuyển tiền, liên hệ với số điện thoại lạ, tải ứng dụng không rõ
nguồn gốc hoặc làm theo hướng dẫn giả mạo tổ chức uy tín. Ngược lại, các tin nhắn
không thể hiện mục đích lừa đảo rõ ràng, bao gồm tin nhắn cá nhân thông thường, tin
nhắn OTP hợp lệ, thông báo dịch vụ, quảng cáo hoặc chăm sóc khách hàng không
chứa dấu hiệu giả mạo, được gán vào lớp không lừa đảo
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
33

Cohen’s Kappa hoặc Fleiss’ Kappa. Ngoài ra, hình thức thảo luận nhóm có thể chịu
ảnh hưởng bởi sự đồng thuận xã hội hoặc ý kiến của thành viên có lập luận nổi
trội hơn. Vì vậy, bộ dữ liệu trong khoá luận nên được hiểu là bộ dữ liệu đã được thẩm
định theo cơ chế đồng thuận nhóm, thay vì một bộ dữ liệu được gán nhãn độc lập và
đánh giá đồng thuận theo quy trình gán nhãn tiêu chuẩn.
3.1.4 Phân tích sơ bộ dữ liệu thực
Bộ dữ liệu real gồm 2.567 mẫu, bao gồm 5 cột đặc trưng dữ liệu (content,
label, sender_type, has_URL, has_phoe_number), trong đó label 0 (tin hợp lệ) chiếm
2.321 mẫu (90,4%) và label 1 (smishing) chỉ có 246 mẫu (9,6%). Đây là mức mất cân
bằng khá nặng, tỉ lệ xấp xỉ 9,4:1, phản ánh mức mất cân bằng nhãn đáng kể trong
thực tế. Xét về độ dài, tin label 1 có xu hướng ngắn hơn tin label 0 một cách rõ rệt.
Theo số ký tự, trung vị của label 0 là 227 ký tự so với 156 ký tự ở label 1; theo số từ,
trung vị là 45 từ so với 30 từ. Độ lệch chuẩn ở cả hai nhóm đều lớn (khoảng 100 ký
tự/20 từ), cho thấy độ dài dao động nhiều trong từng label, nhưng xu hướng smishing
ngắn gọn, đi thẳng vào yêu cầu hành động vẫn là tín hiệu khá ổn định.
Tỉ lệ has_URL ở label 1 cao hơn rõ rệt so với label 0: 73,6% tin smishing có
URL, trong khi chỉ 48,7% tin hợp lệ có URL. Điều này phù hợp với bản chất smishing
thường kèm liên kết để dẫn dụ người dùng click, nhập thông tin hoặc tải app giả.
Ngược lại với URL, tỉ lệ chứa số điện thoại ở label 1 lại thấp hơn label 0: chỉ 24,4%
tin smishing có số điện thoại so với 41,2% ở tin hợp lệ. Điều này có thể vì tin hợp lệ
thường là các thông báo có kèm hotline chăm sóc khách hàng (ngân hàng, dịch vụ
công, viễn thông), còn smishing ưu tiên dẫn người dùng qua URL/landing page hơn
là để lại số điện thoại có thể truy ngược.
3.2 Quy trình xây dựng bộ dữ liệu tạo sinh vòng đầu tiên (Phase 1)
Nhằm bù đắp sự khan hiếm nghiêm trọng của dữ liệu smishing thực tế và
chuẩn bị một tập dữ liệu huấn luyện phong phú cho các mô hình học máy, nghiên cứu
34

thiết lập một quy trình tạo sinh dữ liệu có kiểm soát sử dụng các Mô hình Ngôn ngữ
Lớn (LLM). Quy trình này được xây dựng trên nền tảng kết hợp các hệ phân tầng
thuộc tính (taxonomy) và kỹ thuật thiết kế prompt nghiêm ngặt để tối ưu hóa chất
lượng dữ liệu.
3.2.1 Nền tảng xây dựng dữ liệu tạo sinh và hệ phân tầng
Để dữ liệu tạo sinh không bị chung chung hay quá xa rời thực tế, nghiên cứu
thiết lập hai hệ phân lớp (taxonomy) song song đóng vai trò là các tham số điều khiển
ngữ cảnh trong prompt tạo sinh, thay vì là thuộc tính siêu dữ liệu tĩnh cuối cùng của
tập dữ liệu:
Hệ phân tầng mức độ trang trọng (Formality Taxonomy) cho Nhãn 0 (Tin
nhắn hợp lệ): Mô tả cấu trúc tin nhắn hợp lệ qua 5 mức độ trang trọng từ Level 0
đến Level 4:
1. Level 0 (Cứng hoàn toàn): Template cố định có entropy thông tin thấp, sử
dụng bởi các tổ chức lớn (ngân hàng, nhà mạng) phục vụ mã OTP hoặc biến
động số dư, dễ dàng phân tích bằng biểu thức chính quy (regex).
2. Level 1 (Mềm): Template có cấu trúc cố định nhưng chứa các trường dữ liệu
động biến đổi cao như thông báo giao hàng (logistics) hay cập nhật trạng thái
đơn hàng (e-commerce).
3. Level 2 (Bán trang trọng): Tin nhắn giao dịch từ các doanh nghiệp vừa và
nhỏ (SMEs), đôi khi chứa lỗi viết tắt hoặc bỏ dấu một phần do thói quen soạn
thảo.
4. Level 3 (Thân thiện): Tin nhắn chăm sóc khách hàng từ các cơ sở dịch vụ
nhỏ (phòng khám tư, cửa hàng thời trang) với giọng văn gần gũi.
5. Level 4 (Cá nhân hoàn toàn): Tin nhắn trao đổi không chính thống giữa các
cá nhân (P2P), sử dụng ngôn ngữ tự nhiên, viết tắt, không dấu hoặc tiếng lóng.
Cần phân biệt rõ: hiện tượng bỏ dấu ở Level 4 là đặc trưng phong cách tự
nhiên, hoàn toàn khác biệt với hành vi che giấu chữ viết (obfuscation) có chủ
đích của tin nhắn lừa đảo.
Ánh xạ điều khiển: Các danh mục tin nhắn hợp lệ được gán các mức formal
tương ứng. Ví dụ, ngân hàng và viễn thông được giới hạn trong Level 0–1, trong khi
tin nhắn cá nhân và OTP có thể trải rộng từ Level 0 đến Level 4.
35

Hệ phân tầng mức độ che giấu chữ viết (Obfuscation Taxonomy) cho
Nhãn 1 (Tin nhắn lừa đảo): Xây dựng thang đo độ nghiêm trọng gồm 6 bậc liên tục
(từ Level 0 đến Level 5) đại diện cho các chiến thuật ngụy trang văn bản nhằm trốn
tránh các bộ lọc từ khóa của nhà mạng:
1. Level 0 (Không che giấu): Tin nhắn smishing viết chuẩn chỉnh, trang trọng
tương tự tin nhắn thật của tổ chức để tạo lòng tin tối đa (dạng tin nhắn này đặc
biệt nguy hiểm và khó phân biệt nếu chỉ dựa trên đặc trưng bề mặt).
2. Level 1 (Leet nhẹ): Thay thế 1–2 ký tự nguyên âm bằng số có hình dạng tương
đồng (ví dụ: ng@n h@ng, li3n k3t).
3. Level 2 (Leet nặng): Viết chệch ký tự ở hầu hết các từ nhạy cảm và kết hợp
loại bỏ dấu thanh để phá vỡ đặc trưng từ vựng (thường xuất hiện trong kịch
bản giả mạo BHXH, trợ cấp).
4. Level 3 (Chèn ký tự ngăn cách): Chèn dấu chấm, dấu phẩy hoặc dấu gạch
dưới giữa từng chữ cái của các từ khóa nhạy cảm (ví dụ:
K.h.ó.a_t.à.i_k.h.o.ả.n, N_ạ_p_t_i_ề_n) nhằm phá vỡ cơ chế tách từ
(tokenization) của mô hình phân loại.
5. Level 4 (Trộn ký tự đặc biệt): Trộn lẫn ký tự Unicode lạ, ký tự đồng hình
(homoglyphs) hoặc biểu tượng toán học để biểu diễn từ ngữ nhạy cảm.
6. Level 5 (Gây nhiễu cực đoan): Văn bản bị xáo trộn cấu trúc nặng nề, kết hợp
sai lệch dấu thanh Unicode (Unicode diacritics) phức tạp, gây cản trở lớn đối
với con người khi đọc trực tiếp nhưng vẫn truyền tải được ý đồ lừa đảo cơ bản.
Ánh xạ điều khiển: Các kịch bản smishing được ghép cặp với các mức độ che
giấu phù hợp trong thực tế. Ví dụ, kịch bản đòi nợ/đe dọa thường ở Level 0–1, giả
mạo ngân hàng ở Level 1–2, và các nội dung nhạy cảm/quảng cáo đen thường xuất
hiện ở Level 3–5.
Cơ chế điều phối không gian xác suất của LLM: LLM không ghi nhớ trực
tiếp dữ liệu huấn luyện mà tạo văn bản bằng cách dự đoán token tiếp theo từ không
gian phân phối xác suất. Việc thiết kế prompt tốt đóng vai trò thu hẹp không gian tìm
kiếm của mô hình, đảm bảo tính nhất quán của định dạng đầu ra mà không làm triệt
tiêu tính đa dạng (diversity) của nội dung. Trong quy trình này, tham số temperature
được điều chỉnh linh hoạt: giữ ở mức thấp (0.2 - 0.4) cho các nhóm dữ liệu formal
(Level 0, 1) để bảo toàn cấu trúc template, và tăng lên mức cao (0.7 - 0.9) cho các
36

nhóm tin nhắn có độ nhiễu cao (obfuscation Level 4, Level 5) nhằm khuyến khích
mô hình sinh ra các biến thể ký tự phi chuẩn phong phú.
Ba tiêu chí chất lượng cốt lõi của dữ liệu tổng hợp:
• Fidelity (Độ trung thực): Nội dung sinh ra phải mô phỏng chính xác văn
phong, cấu trúc câu, cách phân bổ liên kết (URL) và tên thương hiệu của SMS
thực tế tại Việt Nam, tránh tạo ra ranh giới quyết định ảo (artificial boundary)
khiến mô hình học sai lệch.
• Diversity (Đa dạng): Phủ đều các kịch bản, mức độ trong hệ phân tầng. Đối
với Nhãn 0, sự đa dạng được đo bằng tổ hợp: sender_type, category,
formal_level. Đối với Nhãn 1, sự đa dạng được quyết định bởi: category,
psychology (chiến thuật tâm lý), obfuscation_level.
• Novelty (Tính mới): Các mẫu sinh ra không được trùng lặp ngữ nghĩa với tập
dữ liệu thực ground truth hoặc lặp lại lẫn nhau trong cùng một batch.
Sự vượt trội của Few-Shot so với Zero-Shot: Thực nghiệm sơ bộ cho thấy
chế độ sinh zero-shot (chỉ cung cấp mô tả nhiệm vụ) khiến mô hình dễ gặp hiện tượng
ảo giác (hallucination): sinh tin nhắn Nhãn 0 bằng tiếng Anh hoặc tiếng Việt dịch
máy thô sơ, không đúng định dạng của ngân hàng Việt Nam; đồng thời sinh tin nhắn
Nhãn 1 quá "sạch", thiếu hoàn toàn các biến thể viết tắt và kỹ thuật che giấu chữ viết.
Ngược lại, kỹ thuật few-shot cung cấp từ 3–5 ví dụ mẫu cụ thể của từng kịch bản tin
nhắn thật tương ứng giúp LLM nhanh chóng học văn phong, cấu trúc viết tắt đặc
trưng, cách sử dụng các liên kết giả mạo, các chiến thuật tâm lý và các mức độ
obfuscate thích hợp.
Giải quyết các thách thức đặc thù:
• Thách thức đối với Nhãn 0: LLM có xu hướng tự động hiệu chỉnh văn
bản về dạng chuẩn ngữ pháp. Để mô phỏng đúng tin nhắn Level 2 và 3
chứa lỗi viết tắt tự nhiên của các cửa hàng/doanh nghiệp nhỏ, prompt
few-shot cần cung cấp các ví dụ chứa lỗi thực tế để mô hình không tự
động "sửa sai", hạn chế lỗi nhận nhầm (False Positive) sau này. Ngoài
ra, mô hình cần học cách phân biệt sự khẩn cấp hợp lệ (ví dụ: OTP hết
hạn sau 5 phút) với sự khẩn cấp đe dọa (ví dụ: khóa tài khoản trong 2
giờ).
• Thách thức đối với Nhãn 1: Các bộ lọc an toàn mặc định (safety filters)
của LLM thương mại thường từ chối sinh nội dung lừa đảo. Để giải
37

quyết rào cản này, chúng tôi áp dụng kỹ thuật safety framing trong
prompt để thiết lập bối cảnh nghiên cứu học thuật hợp pháp.
3.2.2 Kiến trúc Prompt 4 Tầng
Hình 3 Quy trình tăng cường dữ liệu bằng LLM
Hệ thống prompt tạo sinh được thiết kế theo cấu trúc phân tầng gồm 4 lớp
(layer) độc lập nhằm đáp ứng các nguyên lý kỹ thuật prompt hiện đại, được tham
khảo từ các nghiên cứu đi trước như Brown và các cộng sự năm 2020 [23];White và
các cộng sự năm 2023 [24] và Long cùng các đồng tác giả vào năm 2024 [25]:
Layer 1 - Persona & Task Framing (Chỉ dẫn vai trò và Bối cảnh): Thiết
lập vai trò chuyên môn sâu cho LLM để định hình phân phối từ vựng đầu ra.
• Với Nhãn 0: Thiết lập vai trò chuyên gia phân tích dữ liệu viễn thông
xây dựng bộ dữ liệu SMS hợp lệ tại Việt Nam.
• Với Nhãn 1 (Safety Framing): Định hình mô hình là "Chuyên gia an
ninh mạng đang xây dựng tập dữ liệu mô phỏng smishing phục vụ mục
đích nghiên cứu phòng chống lừa đảo trực tuyến". Bối cảnh này giúp
mô hình vượt qua bộ lọc an toàn nhưng vẫn tập trung vào việc tạo ra
các kịch bản lừa đảo thực tế.
Layer 2 - Task Specification (Định nghĩa Nhiệm vụ & Kỹ thuật Biến -
Hằng): Áp dụng nguyên lý conditional prompting để phân tách các tham số đầu vào:
38

• Các Hằng số: Định dạng đầu ra nghiêm ngặt (chuỗi thô phân tách bằng
ký tự đường ống |), cấu trúc các trường thông tin cố định trong kết quả
trả về.
• Các Biến số: Các tham số thay đổi theo từng batch để tạo sự đa dạng,
bao gồm: danh mục kịch bản (category), danh sách tên thương hiệu
(brands), mức độ trang trọng hoặc mức độ che giấu chữ viết
(formal_level/obfuscation_level), và số lượng mẫu cần sinh
(batch_size). Danh sách các brands được truyền vào dạng một mảng để
mô hình tự lựa chọn ngẫu nhiên cho từng dòng, tránh hiện tượng toàn
bộ một batch chỉ lặp lại một tên thương hiệu cố định.
Layer 3 - Few-Shot Demonstrations (Thư viện ví dụ Few-shot): Cung cấp
từ 3–5 ví dụ thực tế (lấy từ tập ground truth thực) tương ứng với từng danh mục dưới
định dạng phân tách bằng dấu gạch đứng (|). Các ví dụ được lựa chọn dựa trên nguyên
lý Coverage Matrix (Ma trận bao phủ) để đảm bảo mô hình tiếp xúc đồng thời với
các tổ hợp đa dạng của loại người gửi ($\text{sender_type}$), chiến thuật thuyết phục
và mức độ che giấu chữ viết. Mô hình học từ cách viết tắt, cấu trúc viết lách phi tiêu
chuẩn, và cách cài cắm link độc hại từ các ví dụ này. Định dạng | được chọn thay vì
dấu phẩy (CSV) truyền thống vì tin nhắn SMS tiếng Việt thường chứa dấu phẩy tự
nhiên; việc dùng CSV dễ gây lỗi phân tích cú pháp (parsing error) khi LLM quên
đóng mở ngoặc kép theo chuẩn RFC 4180.
Layer 4 - Negative Instructions (Chỉ dẫn loại trừ/Ràng buộc tiêu cực):
Đưa ra danh sách các hành vi bị cấm để khắc phục triệt để các lỗi hệ thống của LLM:
• Với Nhãn 1: Không tạo dòng tiêu đề hoặc markdown block phụ, không
sử dụng dấu nháy đơn trong trường sender_type để tránh lỗi parse cơ
sở dữ liệu, không lặp lại cùng một tên miền (domain) giả mạo trong
một batch, không sử dụng tên thương hiệu thật trong đường link độc
hại (phải dùng domain giả lập có dạng như vcb-digibank.xyz).
• Với Nhãn 0: Chỉ sử dụng các liên kết thật (.vn, .com.vn), không đưa
các từ ngữ thúc giục đe dọa vào nội dung, không sử dụng bất kỳ hình
thức che giấu chữ viết nào, đặc biệt không sử dụng các chuỗi giữ chỗ
(placeholders) như [TÊN], [SỐ ĐIỆN THOẠI], XXXXXX để tránh
làm nhiễu dữ liệu huấn luyện.
39

3.2.3 Pipeline sinh dữ liệu và đánh giá chất lượng
Quy trình tạo sinh dữ liệu được vận hành tự động thông qua API của các mô
hình ngôn ngữ lớn (chủ đạo là Gemini 2.5 Flash). Quy trình hoạt động theo mô hình
lặp (loop):
Chiến lược Parse "Last 4 Parts": Khi LLM trả về chuỗi văn bản, hệ thống
thực hiện tách chuỗi dựa trên ký tự phân tách |. Do nội dung tin nhắn SMS có thể vô
tình chứa ký tự | do mô hình tự sinh, hệ thống áp dụng kỹ thuật lấy 4 phần tử cuối
cùng làm các trường siêu dữ liệu tương ứng (label, has_url, has_phone, sender_type),
và ghép toàn bộ các phần tử phía trước lại làm trường nội dung content. Giải pháp
này đảm bảo độ bền vững của parser tự động.
Quy trình đánh giá chất lượng 3 tầng (3-Tier Quality Validation): Để đảm
bảo dữ liệu sinh ra đạt chuẩn học máy, mỗi batch dữ liệu phải vượt qua ba tầng kiểm
duyệt nghiêm ngặt:
Tầng 1: Format Validation (Tự động): Hệ thống kiểm tra tự động xem mẫu
dữ liệu có đủ 5 trường thông tin hay không; kiểm tra kiểu dữ liệu của các trường nhị
phân (has_url, has_phone); xác định trường sender_type phải nằm trong tập xác định
(brandname, Shortcode, personal_number, not_applicable); giới hạn độ dài tin nhắn
từ 20 đến 600 ký tự; và đối chiếu tính nhất quán logic (ví dụ: nếu has_url bằng 1 thì
trong content bắt buộc phải chứa chuỗi định dạng URL). Với Nhãn 0, bổ sung kiểm
tra loại trừ sự xuất hiện của các domain giả mạo hoặc ký tự placeholder literal.
Tầng 2: Data Quality Check (Tự động + Thủ công): Để hạn chế tình trạng
hallucination của Gemini, chúng tôi sử dụng một LLM-as-judge (Mistral AI) đẻ đánh
giá nhãn sinh có đúng với nội dung được sinh hay không; Kết quả thu được độ đồng
thuận giữa 2 LLM là 75,65% - tương đương 1703 nhãn bất đồng. Nhóm tiến hành
kiểm tra thủ công các mẫu này đẻ sữa chữa và thống nhất nhãn đúng. Song song với
đó, nhóm nghiên cứu cũng thực hiện rà soát thủ công ngẫu nhiên 10% số mẫu của
mỗi batch. Quá trình kiểm tra tập trung vào việc đánh giá tính thực tế của kịch bản,
độ tự nhiên của câu văn tiếng Việt, sự phù hợp của văn phong so với mức độ che
40

giấu/trang trọng yêu cầu trong prompt, và kiểm tra xem có xuất hiện các mẫu lỗi lặp
template quá mức hay không.
Tầng 3: Distribution Check (Đánh giá phân phối mục tiêu): Sau khi gom
đủ số lượng mẫu, hệ thống đánh giá phân phối tổng thể của các siêu dữ liệu so với
phân phối mục tiêu đã thiết lập dựa trên thực tế:
a. Nhãn 1: Định hướng đạt tỷ lệ khoảng ~50% personal_number và ~75%
has_url.
b. Nhãn 0: Định hướng đạt tỷ lệ khoảng ~70% brandname và ~40%
has_url.
Kết quả sau vòng sinh đầu tiên (Phase 1): Trải qua quy trình lọc và kiểm
định 3 tầng, vòng tạo sinh đầu tiên thu được 4,996 mẫu tạo sinh Nhãn 1 và 2,999
mẫu tạo sinh Nhãn 0 đảm bảo đúng định dạng cấu trúc kỹ thuật và sẵn sàng đưa vào
các bước cải biên chất lượng tiếp theo.
3.3 Cải thiện và đánh giá định lượng dữ liệu
Sau khi thu được dữ liệu vòng đầu, nhóm nghiên cứu phát hiện các "artifact"
tạo sinh điển hình: dữ liệu tạo sinh nhãn 0 quá trang trọng (formal), dữ liệu tạo sinh
nhãn 1 quá lạm dụng kỹ thuật viết chệch ký tự (leet/obfuscation) một cách không thực
tế, tạo ra các lối tắt (shortcuts) khiến mô hình học máy dễ dàng phân loại dựa trên đặc
trưng bề mặt thay vì hiểu sâu ngữ nghĩa. Do đó, một quy trình cải biên chất lượng dữ
liệu được triển khai.
3.3.1 Các biện pháp đã áp dụng
1. Giảm thiểu hiện tượng “Over-Obfuscation” ở Nhãn 1
Trong dữ liệu tạo sinh nhãn 1 ban đầu, có đến 53% số mẫu thuộc mức độ che giấu
nặng (Level 2), nơi hầu như mọi từ nhạy cảm đều bị leet (ví dụ: kh0ng, t13n, n4p).
Để sửa chữa, nhóm sử dụng Gemini 1.5 Flash để chuẩn hóa chính tả cho các từ
context/glue không nhạy cảm (như chuyển kh0ng về không, v4o về vào), chỉ giữ lại
leet ở các từ mang tính lừa đảo chính (như tài khoản, nạp tiền, bảo mật). Quy trình đã
41

hiệu chỉnh thành công 2.261 mẫu từ Level 2 về Level 0 (văn phong tự nhiên không
che giấu).
Obfuscation level  Số lượng mẫu tạo sinh  Số lượng mẫu tạo sinh
| trước chỉnh sửa            | sau chỉnh sửa  |       |
| -------------------------- | -------------- | ----- |
| Level 0 (Không che giấu)   | 638            | 2899  |
| Level 1 (Leet nhẹ)         | 651            | 651   |
| Level 2 (Leet nặng)        | 2647           | 386   |
| Level 3 (Chèn dấu cách)    | 670            | 670   |
| Level 4 (Ký tự đặc biệt)   | 225            | 225   |
| Level 5 (Nhiễu cực đoan)   | 139            | 139   |
| Tổng                       | 4970           | 4970  |
Bảng 1. Thống kê phân phối dữ liệu cho từng nhãn obfuscation level của dữ liệu tạo
sinh
B. Thay thế dữ liệu tạo sinh Nhãn 0 bằng dữ liệu P2P từ ViLexNorm
Tin nhắn hợp lệ tạo sinh thường thiếu văn phong đời thường. Nhóm tiến hành
thay thế 1.001 mẫu nhãn 0 tạo sinh bằng dữ liệu hội thoại thực tế được lọc từ bộ dữ
liệu ViLexNorm [26] (Facebook, TikTok). Tiêu chuẩn lọc bao gồm: độ dài 10-200
ký tự, không chứa hotline/URL chưa xác minh, không chứa các từ thúc giục (CTA)
độc hại, không văng tục. Trong đó, có 501 mẫu là boundary samples (chứa các cuộc
hội thoại đời thường bàn luận về chủ đề tiền bạc, link, tuyển dụng nhưng hoàn toàn
lành mạnh).

C. Bổ sung Boundary Samples cho Nhãn 1
Để tăng độ khó cho ranh giới quyết định, nhóm tạo thêm 653 mẫu boundary
samples nhãn 1. Đây là những tin nhắn lừa đảo có cấu trúc formal tương tự tin nhắn
42

ngân hàng thật (obfuscation level 0), không sử dụng từ ngữ kích động mạnh và sử
dụng kịch bản hội thoại P2P để mô phỏng các trường hợp lừa đảo nhắm vào cá nhân.
D. Paraphrase nâng cao tính đa dạng bằng Mistral AI
Nhằm giảm thiểu việc lặp lại các template câu do LLM sinh ra, toàn bộ dữ liệu
tạo sinh nhãn 1 (trừ boundary samples) được đưa qua pipeline paraphrase sử dụng
Mistral AI với prompt 3 tầng:
1. Layer 1 (Role): Định hình vai trò chuyên gia phân tích tin nhắn lừa đảo.
2. Layer 2 (Rules): Đưa ra các quy tắc paraphrase chi tiết theo 8 danh mục nội
dung để đa dạng hóa chủ thể, tên thương hiệu, cấu trúc câu.
3. Layer 3 (Output Format): Chỉ trả về nội dung tin nhắn mới, không kèm giải
thích.
Hình 4 Các bước cải thiện bộ dữ liệu
43

3.3.2  Đánh giá định lượng bộ dữ liệu tạo sinh
Sau khi đã thực hiện các bước cải thiện bộ dữ liệu, chúng tôi tiến hành tiến hành đánh
giá định lượng để so sánh bộ dữ liệu tạo sinh lần 1 với phiên bản đã được cải thiện.
a)  Đa dạng dữ liệu và mức độ lặp mẫu
| Chỉ số trên dữ liệu tạo sinh nhãn 1  |     | Trước   | Sau     |
| ------------------------------------ | --- | ------- | ------- |
| Mean embedding NN similarity         |     | 0.9533  | 0.9273  |
| Median embedding NN similarity       |     | 0.9621  | 0.9288  |
| Tỷ lệ NN similarity >= 0.90          |     | 92.73%  | 76.68%  |
| Tỷ lệ NN similarity >= 0.95          |     | 63.17%  | 27.48%  |
Bảng 2. So sánh mức độ tương đồng nearest-neighbor trước và sau cải thiện
Độ tương đồng nearest-neighbor ở mức embedding giảm rõ rệt sau cải thiện.
Điều này cho thấy các mẫu synthetic Label 1 ít giống nhau hơn, tức dữ liệu có độ đa
dạng ngữ nghĩa tốt hơn. Đặc biệt, tỷ lệ mẫu có similarity rất cao từ 0.95 trở lên giảm
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
Bảng 3. So sánh độ lặp n-gram dữ liệu tạo sinh trước và sau cải thiện
Kết quả phân tích n-gram cũng cho thấy mức lặp template giảm ở cả Label 1
và Label 0 synthetic-like. Đây là cải thiện quan trọng vì dữ liệu tạo sinh nếu lặp nhiều
cấu trúc có thể khiến mô hình học lối tắt thay vì học đặc trưng tổng quát của smishing.
44

b) Giảm artifact leet và tình trạng obfuscation quá mức
| Chỉ số trên dữ liệu tạo sinh nhãn 1  |     |                         |     | Trước   |     | Sau     |
| ------------------------------------ | --- | ----------------------- | --- | ------- | --- | ------- |
|                                      |     | Tỉ lệ dữ liệu có leet   |     | 82.45%  |     | 72.78%  |
|                                      |     | Tỉ lệ token leet        |     | 18.87%  |     | 4.91%   |
|                                      |     | Mật độ leet trung bình  |     | 0.2700  |     | 0.0671  |
Bảng 4. So sánh mức độ leet trước và sau cải thiện
Phiên bản ban đầu có dấu hiệu của việc over-obfuscation đúng như quan sát,
khi mà tỷ lệ token dạng leet hoặc tình trạng biến dạng ký tự quá cao trong dữ liệu tạo
sinh. Sau khi tiến hành cải thiện, leet token rate đã giảm mạnh từ 18.87% xuống còn
4.91%. Điều này giúp dữ liệu tạo sinh bớt phụ thuộc vào các dấu hiệu bề mặt quá dễ
để nhận biết, từ đó giảm nguy cơ mô hình học theo thiên kiến cứ có ký tự biến dạng
là lừa đảo.
c)  Độ dài văn bản gần dữ liệu thực hơn
| Chỉ số của dữ liệu tạo sinh  |     |     |  Trước  |     | Sau  | Dữ liệu thực  |
| ---------------------------- | --- | --- | ------- | --- | ---- | ------------- |
nhãn 1
|     | Độ dài trung bình  |      | 117.48  |     | 159.83  | 194.09  |
| --- | ------------------ | ---- | ------- | --- | ------- | ------- |
|     | Trung vị độ dài    |      | 110     |     | 149     | 156     |
|     |                    | P90  | 182     |     | 238     | 321     |
Bảng 5. So sánh phân phối độ dài văn bản trước và sau cải thiện
Ở dữ liệu tạo sinh trước cải thiện, các mẫu tạo sinh nhãn 1 ngắn hơn đáng kể
so với dữ liệu thực. Sau khi tiến hành cải thiện, độ dài trung bình đã tăng từ 117.48
lên 159.83 ký tự, trung vị tăng từ 110 lên 139. Phân phối độ dài này gần hơn với dữ
liệu lừa đảo thật, vốn có độ dài trung bình rơi vào khoảng 194.09 và trung vị là 156.
Như vậy, phiên bản sau cải thiện đã giảm bớt shortcut về độ dài văn bản giữa dữ liệu
thực và dữ liệu tạo sinh.
45

3.4 Quy trình mở rộng bộ siêu dữ liệu (Metadata Schema v2)
3.4.1 Lược đồ Metadata Schema v2
Để phục vụ cho các thực nghiệm đánh giá lát cắt chi tiết ở Chương 3 và 5, bộ
dữ liệu ViSmish được gắn nhãn lại toàn bộ các thuộc tính siêu dữ liệu theo lược đồ
dưới đây, mở rộng thêm 11 thuộc tính đa chiều:
• message_domain (Chủ đề chính): Phân loại tin nhắn thành các miền trung
lập (như banking_finance, public_service, telecom, commerce, logistics,
marketing_promotion, employment, investment, debt_collection, gambling,
adult_service, personal_social).
• text_phenomena (Hiện tượng văn bản): abbreviation, teencode,
diacritic_omission, character_substitution, punctuation_insertion, v.v.
• text_noise_score (Mức phi chuẩn): Thang điểm từ 0 đến 4 thể hiện độ khó
đọc của tin nhắn do lỗi chính tả hoặc cách viết phi chuẩn.
• target_audience (Đối tượng nhắm đến, 3 trường dữ liệu): nhóm tuổi, giới
tính, vai trò xã hội của nạn nhân (khách hàng, người tìm việc, con nợ) đi kèm
bằng chứng cụ thể (evidence span).
• obfuscation (Che giấu chủ ý, 3 trường dữ liệu): present (có/không),
techniques (kỹ thuật cụ thể), severity (mức độ từ 0 đến 4).
• requested_actions (Hành động yêu cầu): click_or_visit_link, call_phone,
reply_message, provide_personal_information, transfer_money,
install_application.
• persuasion_tactics (Chiến thuật thuyết phục): impersonation (giả mạo),
urgency (cấp bách), fear (sợ hãi), reward_incentive (lợi ích), v.v.
3.4.2 Quy trình thử nghiệm Pilot và tối ưu hóa Prompt
Để đảm bảo chất lượng và tính nhất quán khi gán nhãn tự động các trường
metadata bằng LLM, nghiên cứu không triển khai gán nhãn đồng loạt ngay từ đầu mà
thực hiện một quy trình hiệu chỉnh theo nhiều vòng. Mục tiêu của quy trình này là
kiểm tra mức độ phù hợp giữa kết quả gán nhãn của mô hình và đánh giá thủ công
của con người, từ đó điều chỉnh prompt trước khi áp dụng trên toàn bộ tập dữ liệu.
Quy trình được triển khai trên 100 mẫu pilot, bao gồm các tin nhắn được chọn để đại
diện cho nhiều nguồn dữ liệu và nhiều kiểu biểu hiện khác nhau trong bộ dữ liệu.
46

Ở Giai đoạn 1 - Pilot Evaluation, một phiên bản prompt ban đầu được sử dụng
để gọi Mistral Small qua API và sinh nhãn metadata cho từng mẫu. Để hạn chế hiện
tượng nhiễm chéo ngữ cảnh giữa các tin nhắn trong cùng batch, phiên bản tối ưu cuối
cùng sử dụng cấu hình batch_size = 1, tức mỗi lần gọi mô hình chỉ xử lý một tin nhắn.
Kết quả gán nhãn tự động sau đó được so sánh với nhãn rà soát thủ công của Reviewer
A. Các trường metadata được đánh giá theo nhiều loại độ đo khác nhau tùy bản chất
của trường: các trường đơn nhãn như message_domain, obfuscation_present,
target_gender được đánh giá bằng độ khớp chính xác và Cohen’s Kappa; các trường
dạng điểm như text_noise_score, obfuscation_severity được đánh giá bằng độ khớp
chính xác và sai số tuyệt đối trung bình (MAE); các trường đa nhãn như
text_phenomena, target_age_groups, target_roles, persuasion_tactics,
requested_actions được đánh giá bằng độ tương đồng Jaccard.
Kết quả pilot ban đầu cho thấy mô hình có khả năng nhận diện khá tốt một số
thuộc tính rõ ràng, nhưng vẫn gặp khó khăn với những trường đòi hỏi phân biệt tinh
tế giữa hiện tượng bề mặt của văn bản và ý đồ né lọc. Cụ thể, mô hình dễ nhầm giữa
nhiễu văn bản thông thường như viết tắt, thiếu dấu, cách viết rút gọn trong SMS
với obfuscation có chủ đích nhằm che giấu nội dung lừa đảo. Sự nhầm lẫn này ảnh
hưởng trực tiếp đến các trường text_noise_score, text_phenomena,
obfuscation_present và obfuscation_severity. Ngoài ra, ở các trường đa nhãn liên
quan đến chiến thuật thuyết phục, mô hình đôi khi bỏ sót các tín hiệu gián tiếp như
dụ bấm liên kết, yêu cầu liên hệ ngoài nền tảng, hoặc nhầm lẫn giữa tính khan hiếm
và tính khẩn cấp.
Ở Giai đoạn 2 - Tối ưu hóa và chốt prompt, prompt được hiệu chỉnh theo
hướng bổ sung quy tắc quyết định rõ ràng hơn. Thứ nhất, prompt phân định lại ranh
giới giữa text_noise_score và obfuscation_severity: text_noise_score phản ánh mức
độ phi chuẩn bề mặt của văn bản, bao gồm thiếu dấu, viết tắt, lỗi chính tả hoặc cú
pháp SMS thông thường; trong khi obfuscation_severity chỉ phản ánh mức độ che
giấu có khả năng phục vụ né lọc, chẳng hạn thay ký tự, chèn ký hiệu bất thường, viết
biến dạng domain hoặc cố tình làm méo từ khóa nhạy cảm. Thứ hai, prompt bổ sung
47

các hard-rules cho những trường thường bị bỏ sót, ví dụ tin nhắn có URL phải được
xem xét chiến thuật link_lure, tin nhắn yêu cầu chuyển sang Zalo/Telegram được ánh
xạ với off_platform_contact, và các trường hợp giới hạn thời gian cần được phân biệt
giữa urgency và scarcity. Thứ ba, cấu trúc JSON đầu ra được thắt chặt để giảm lỗi
định dạng, giúp pipeline có thể parse tự động ổn định hơn.
Bảng dưới đây tóm tắt sự thay đổi độ đồng thuận giữa Reviewer A và Mistral
Small qua các phiên bản prompt chính. Trong đó, P0.1 là phiên bản sơ khai, P3 là
phiên bản đã bổ sung logic quyết định và chạy với batch_size = 1, còn P4 là phiên
bản đã hiệu chỉnh sâu các nhóm chỉ số về nhiễu văn bản, hiện tượng chữ viết và chiến
thuật thuyết phục.
P4 - prompt
| Trường metadata  | Loại độ đo  | P0.1  | P3  |     |
| ---------------- | ----------- | ----- | --- | --- |
chốt
Accuracy /
| message_domain  |     | 69,0% / 0,659  | 75,0% / 0,724  | 74,0% / 0,713  |
| --------------- | --- | -------------- | -------------- | -------------- |
Kappa
Accuracy /
obfuscation_present  90,0% / 0,675  96,0% / 0,880  98,0% / 0,938
Kappa
Accuracy /
| target_gender  |     | 72,0% / 0,318  | 84,0% / 0,689  | 79,0% / 0,605  |
| -------------- | --- | -------------- | -------------- | -------------- |
Kappa
Accuracy /
| text_noise_score  |     | 42,0% / 0,69  | 42,0% / 0,61  | 62,0% / 0,39  |
| ----------------- | --- | ------------- | ------------- | ------------- |
MAE
Accuracy /
obfuscation_severity  82,0% / 0,28  85,0% / 0,18  88,0% / 0,13
MAE
| text_phenomena      | Jaccard  | 21,2%  | 27,5%  | 53,9%  |
| ------------------- | -------- | ------ | ------ | ------ |
| target_age_groups   | Jaccard  | 64,0%  | 85,0%  | 78,0%  |
| target_roles        | Jaccard  | 67,0%  | 82,0%  | 81,0%  |
| persuasion_tactics  | Jaccard  | 34,9%  | 51,3%  | 62,6%  |
48

requested_actions Jaccard 63,2% 77,2% 80,0%
Bảng 6. Mức độ đồng thuận sau từng lần cải thiện prompt.
Kết quả cho thấy quá trình hiệu chỉnh prompt mang lại cải thiện rõ rệt ở những
trường trước đó có độ bất định cao. Trường text_noise_score tăng từ 42,0% ở P3 lên
62,0% ở P4, đồng thời MAE giảm từ 0,61 xuống 0,39. Điều này cho thấy mô hình đã
nhất quán hơn khi đánh giá mức độ nhiễu bề mặt của tin nhắn. Trường
text_phenomena cũng tăng mạnh từ 27,5% lên 53,9% theo Jaccard, phản ánh việc
prompt mới giúp mô hình nhận diện tốt hơn các hiện tượng như viết tắt, bỏ dấu, dùng
ký tự lạ hoặc lỗi chính tả. Với nhóm obfuscation, obfuscation_present đạt 98,0%
accuracy và Kappa 0,938, trong khi obfuscation_severity đạt 88,0% accuracy với
MAE chỉ còn 0,13. Đây là dấu hiệu quan trọng cho thấy prompt đã phân biệt tốt hơn
giữa nhiễu văn bản thông thường và hành vi che giấu có chủ đích.
Các trường đa nhãn về hành vi và chiến thuật cũng có mức cải thiện đáng kể.
persuasion_tactics tăng từ 51,3% lên 62,6%, nhờ việc bổ sung các quy tắc ánh xạ rõ
ràng cho URL, liên hệ ngoài nền tảng, khẩn cấp và khan hiếm. requested_actions đạt
80,0% Jaccard, cho thấy mô hình tương đối ổn định khi nhận diện hành động mà tin
nhắn yêu cầu người nhận thực hiện. Một số trường như target_gender và
target_age_groups có giảm nhẹ so với P3, tuy nhiên vẫn đạt mức chấp nhận được
trong bối cảnh đây là các thuộc tính thường phải suy luận gián tiếp từ nội dung, không
phải lúc nào cũng được biểu hiện rõ trong tin nhắn SMS ngắn.
Ở Giai đoạn 3 - Gán nhãn đồng loạt, phiên bản prompt P4 được chốt làm
prompt chính thức để chạy trên phần dữ liệu còn lại. Các nhãn metadata sinh ra không
được dùng như nhãn phân loại chính thay thế cho nhãn smishing/ham, mà đóng vai
trò là metadata tĩnh phục vụ phân tích dữ liệu, phân tích lỗi và phân tích lát cắt ở các
chương sau. Cách tổ chức này giúp tận dụng khả năng mở rộng của LLM trong gán
nhãn thuộc tính chi tiết, đồng thời vẫn giữ kiểm soát chất lượng thông qua bước pilot
thủ công. Nhìn chung, kết quả pilot cho thấy prompt sau hiệu chỉnh đã đạt mức ổn
49

định đủ để áp dụng diện rộng, đặc biệt ở các nhóm trường quan trọng đối với nghiên
cứu như obfuscation, nhiễu văn bản, hiện tượng chữ viết và chiến thuật thuyết phục.
3.5 Phân tích bộ dữ liệu tổng thể (ViSmish)
Bộ dữ liệu được sử dụng trong đề tài, ViSmish, là bộ dữ liệu phát hiện tin nhắn
lừa đảo qua SMS viết bằng tiếng Việt. Bộ dữ liệu được xây dựng nhằm giải quyết
khoảng trống nghiên cứu đáng kể trong lĩnh vực phát hiện smishing tiếng Việt - một
ngôn ngữ có tài nguyên hạn chế (low-resource language) với đặc điểm ngôn ngữ học
phức tạp, hệ thống thanh điệu và cách viết tắt/biến thể chính tả đặc thù trên nền tảng
nhắn tin di động.
3.5.1 Thành phần cấu trúc bộ dữ liệu
Bộ dữ liệu tổng thể bao gồm 10.562 mẫu, được phân bổ chi tiết theo nguồn dữ liệu
(data_origin):
• Dữ liệu thực tế (Real Data): 2.567 mẫu (bao gồm 2.321 mẫu nhãn 0 và 246
mẫu nhãn 1).
• Dữ liệu tạo sinh bằng LLM (Synthetic Data):
o synthetic: 2.008 mẫu (bao gồm 1.998 mẫu nhãn 0 và 10 mẫu nhãn 1).
o paraphrased: 4.333 mẫu nhãn 1 được paraphrase lại để đa dạng hóa cách
diễn đạt.
o synthetic_hard_positive: 653 mẫu nhãn 1 boundary samples có văn
phong nghiêm túc tương tự tin nhắn thật.
• Dữ liệu chéo miền (External Data):
o external_real (thuộc ViLexNorm): 500 mẫu hội thoại P2P thực tế trên
mạng xã hội.
o external_curated (thuộc ViLexNorm): 501 mẫu hội thoại P2P được
chọn lọc kỹ có chứa các từ khóa nhạy cảm nhưng lành mạnh.
Chiến lược kết hợp dữ liệu thực, dữ liệu chéo miền và dữ liệu tạo sinh trong
bộ dữ liệu ViSmish phù hợp với xu hướng được ghi nhận rộng rãi trong nghiên cứu
NLP gần đây, trong đó các mô hình ngôn ngữ lớn được tận dụng như một công cụ
tăng cường dữ liệu hiệu quả cho các tác vụ phân loại văn bản trong bối cảnh nguồn
dữ liệu thực tế khan hiếm. Tuy nhiên, cần lưu ý rằng dữ liệu tạo sinh thường dễ phân
loại hơn dữ liệu thực, do đó các chỉ số đánh giá mô hình nên được báo cáo riêng biệt
trên tập dữ liệu thực để phản ánh hiệu suất thực tiễn.
50

| Nguồn gốc  |     | Phương     | Ham   | Smishing  | Tổng  | Tỷ lệ  |
| ---------- | --- | ---------- | ----- | --------- | ----- | ------ |
|            |     | thức       | (0)   | (1)       |       |        |
| real       |     | Thu  thập  | 2321  | 246       | 2567  | 24.3%  |
thủ công
| external_real  |     | Trích  xuất  | 500  | 0   | 500  | 4.7%  |
| -------------- | --- | ------------ | ---- | --- | ---- | ----- |
từ
VilexNorm
| external_curated  |     | Trích  xuất  | 501  | 0   | 501  | 4.7%  |
| ----------------- | --- | ------------ | ---- | --- | ---- | ----- |
từ
VilexNorm
| paraphrase  |     | LLM  diễn  | 0   | 4333  | 4333  | 41.0%  |
| ----------- | --- | ---------- | --- | ----- | ----- | ------ |
giải lại
| synthetic  |     | LLM  tạo  | 1998  | 10  | 2008  | 19.0%  |
| ---------- | --- | --------- | ----- | --- | ----- | ------ |
sinh
| synthetic_hard_positive  |     | LLM  tạo  | 0   | 653  | 653  | 6.2%  |
| ------------------------ | --- | --------- | --- | ---- | ---- | ----- |
mẫu  hard
positive
| Tổng cộng  |     |     | 5320  | 5242  | 10562  | 100%  |
| ---------- | --- | --- | ----- | ----- | ------ | ----- |
Bảng 7. Phân bố mẫu theo nguồn gốc dữ liệu và nhãn
3.5.2  Phân phối đặc trưng siêu dữ liệu (Metadata)
| Nhãn dữ liệu  | Trung bình  | Trung vị  | Độ lệch      |     | Min  | Max  |
| ------------- | ----------- | --------- | ------------ | --- | ---- | ---- |
|               | (Mean)      | (Median)  | chuẩn (Std)  |     |      |      |
| Nhãn 0 (Ham)  | 152.28      | 129       | 103.53       |     | 2    | 916  |
| Nhãn 1        | 161.08      | 149       | 60.33        |     | 31   | 920  |
(Smishing)
Bảng 8. Thống kê độ dài theo nhãn phân loại tin nhắn
51

Nhãn 0 (Ham) có chiều dài câu trung bình là 152.28 ký tự, trung vị rơi vào
129 ký tự, độ lệch chuẩn rất cao (103.53 ký tự) vì chứa các tin nhắn OTP biến động
số dư cực ngắn kết hợp với các bài tin nhắn quảng cáo nhà mạng cực dài. Trong khi
đó, nhãn 1 (Smishing) có chiều dài câu trung bình cao hơn rõ rệt: 161.08 ký tự, trung
vị 149 ký tự, biên độ phân tán hẹp hơn với độ lệch chuẩn là 60.33 ký tự (kịch bản lừa
đảo được dàn dựng có tổ chức với mật độ chữ tối ưu).

| Message_domain             | Số lượng  | Tỷ lệ %   | Số lượng  | Tỷ lệ %   |
| -------------------------- | --------- | --------- | --------- | --------- |
|                            | (Nhãn 0)  |           | (Nhãn 1)  |           |
|                            |           | (Nhãn 0)  |           | (Nhãn 1)  |
| adult_service              | 33        | 0.62%     | 479       | 9.14%     |
| banking_finance            | 819       | 15.39%    | 621       | 11.85%    |
| commerce                   | 501       | 9.42%     | 59        | 1.13%     |
| debt_collection            | 26        | 0.49%     | 454       | 8.66%     |
| employment                 | 82        | 1.54%     | 871       | 16.62%    |
| gambling                   | 7         | 0.13%     | 662       | 12.63%    |
| healthcare                 | 201       | 3.78%     | 22        | 0.42%     |
| investment                 | 15        | 0.28%     | 478       | 9.12%     |
| logistics                  | 318       | 5.98%     | 63        | 1.20%     |
| marketing_promotion  150   |           | 2.82%     | 71        | 1.35%     |
| other                      | 82        | 1.54%     | 62        | 1.18%     |
| personal_social            | 1,079     | 20.28%    | 156       | 2.98%     |
| public_service             | 490       | 9.21%     | 1,129     | 21.54%    |
| telecom                    | 1,463     | 27.50%    | 90        | 1.72%     |
| unknown                    | 54        | 1.02%     | 25        | 0.48%     |
52

Bảng 9. Thống kê phân phối chủ đề tin nhắn theo 2 nhãn ham và smishing
Nhãn 0 tập trung áp đảo ở nhóm dịch vụ viễn thông viễn thông telecom (1,463
mẫu) và tương tác personal_social (1,079 mẫu). Nhãn 1 bùng nổ mạnh mẽ tại nhóm
dịch vụ công public_service (1,129 mẫu), tuyển dụng việc làm giả mạo employment
(871 mẫu), và cờ bạc gambling (662 mẫu).

|     | has_URL  | Số lượng   |     | Tỷ lệ %    |     | Số lượng   |        | Tỷ lệ %    |
| --- | -------- | ---------- | --- | ---------- | --- | ---------- | ------ | ---------- |
|     |          | (Nhãn 0)   |     | (Nhãn 0)   |     | (Nhãn 1)   |        | (Nhãn 1)   |
|     | False    | 3,836      |     | 72.11%     |     |            | 1,751  | 33.40%     |
|     | True     | 1,484      |     | 27.89%     |     |            | 3,491  | 66.60%     |
Bảng 10. Thống kê thuộc tính has_URL với từng nhãn phân loại
Nhãn 0 phần lớn không chứa liên kết URL (3,836 mẫu không chứa vs 1,484
mẫu chứa), ngược lại Nhãn 1 sử dụng liên kết làm mồi nhử cốt lõi với 3,491 mẫu
chứa URL độc hại trên tổng số mẫu cùng loại.
Nhãn 0 phần lớn không chứa liên kết URL (3,836 mẫu không chứa vs 1,484
mẫu chứa), ngược lại Nhãn 1 sử dụng liên kết làm mồi nhử cốt lõi với 3,491 mẫu
chứa URL độc hại trên tổng số mẫu cùng loại.

|                           | obfuscation_technique  |     | Số lượng  |     | Tỷ lệ %   |     | Số lượng  | Tỷ lệ %   |
| ------------------------- | ---------------------- | --- | --------- | --- | --------- | --- | --------- | --------- |
|                           |                        |     | (Nhãn 0)  |     | (Nhãn 0)  |     | (Nhãn 1)  | (Nhãn 1)  |
| none (Không ngụy trang -  |                        |     | 5,285     |     | 99.10%    |     | 4,643     | 74.34%    |
Văn bản sạch)
| whitespace_splitting (Cố  |     |     |     | 19  | 0.36%  |     | 447  | 7.16%  |
| ------------------------- | --- | --- | --- | --- | ------ | --- | ---- | ------ |
tình tách khoảng trắng)
53

| character_substitution (Thay  | 22  | 0.41%  | 297  | 4.75%  |
| ----------------------------- | --- | ------ | ---- | ------ |
thế ký tự ẩn/đồng dạng)
| irregular_casing (Viết hoa  | 7   | 0.13%  | 181  | 2.90%  |
| --------------------------- | --- | ------ | ---- | ------ |
thường lộn xộn/bất thường)
| punctuation_insertion (Chèn  | 12  | 0.23%  | 268  | 4.29%  |
| ---------------------------- | --- | ------ | ---- | ------ |
các dấu câu tùy tiện)
| word_concatenation (Dính  | 7   | 0.13%  | 167  | 2.67%  |
| ------------------------- | --- | ------ | ---- | ------ |
liền các từ lại với nhau)
| irregular_spacing (Khoảng  | 8   | 0.15%  | 112  | 1.79%  |
| -------------------------- | --- | ------ | ---- | ------ |
cách không đều/quá rộng)
| character_repetition (Cố  | 6   | 0.11%  | 31  | 0.50%  |
| ------------------------- | --- | ------ | --- | ------ |
tình lặp lại một ký tự nhiều
lần)
Bảng 11. Phân phối của đặc trưng thủ thuật che giấu văn bản
Các hành vi ngụy trang văn bản (obfuscation_techniques) thể hiện sự phân hóa rõ
rệt và là dấu hiệu nhận diện mạnh mẽ giữa hai lớp nhãn. Trong khi nhóm tin nhắn
lành mạnh (Nhãn 0) gần như nói không với ngụy trang (chỉ chiếm 0.66%), thì nhóm
lừa đảo (Nhãn 1) có tới 11.43% (599 mẫu) chủ động sử dụng các kỹ thuật này để qua
mặt các bộ lọc chặn tin rác của nhà mạng. Phương thức được kẻ tấn công ưa chuộng
nhất là cố tình tách khoảng trắng ký tự (whitespace_splitting với 447 lần) và thay thế
ký tự ẩn/đồng dạng (character_substitution với 297 lần), kết hợp dày đặc với việc
chèn dấu câu tùy tiện (punctuation_insertion với 268 lần). Việc tổng số lượt áp dụng
kỹ thuật (1,503 lần) vượt xa số lượng tin nhắn thực tế chứng minh một xu hướng nguy
hiểm: kẻ lừa đảo thường kết hợp đồng thời từ 2 đến 3 thủ thuật ngụy trang trên cùng
một tin nhắn (ví dụ biến đổi từ nhạy cảm thành Z_a l_0), tạo ra độ nhiễu phức tạp
thách thức các bộ lọc chuỗi thông thường và đòi hỏi các mô hình AI phải có khả năng
bóc tách nhiễu mạnh mẽ.
54

Hình 5 Tương quan giữa chủ đề tin nhắn và hành động được yêu cầu thực hiện
Hành động phổ biến nhất trong hầu hết các miền smishing là
click_or_visit_link. Tỷ lệ này đạt 79,2% ở healthcare, 77,3% ở banking_finance,
76,4% ở public_service và 63,6% ở gambling. Một số miền lại có hành vi đặc thù
hơn, chẳng hạn telecom chủ yếu yêu cầu call_phone (69,6%) trong khi logistics cũng
có tỷ lệ gọi điện rất cao (65,7%). Miền debt_collection nổi bật với hành động
call_phone chiếm 53,3% và make_payment chiếm 23,2%. Trong khi đó, miền
employment chủ yếu yêu cầu contact_off_platform (57,9%) nhằm đưa nạn nhân
sang các kênh liên lạc bên ngoài. Kết quả cho thấy việc truy cập liên kết vẫn là phương
thức lừa đảo chủ đạo, nhưng mỗi lĩnh vực lại khai thác những hành vi tương tác khác
nhau để đạt mục tiêu lừa đảo.
55

Hình 6 Phân phối chiến thuật thuyết phục theo miền tin nhắn
Chiến thuật link_lure xuất hiện rộng rãi trong nhiều miền, đặc biệt ở
adult_service (40,5%), healthcare (37,2%), gambling (36,8%) và other (35,6%). Yếu
tố urgency cũng được sử dụng rất thường xuyên, đạt 38,0% trong banking_finance,
37,2% trong healthcare, 33,4% trong public_service và 32,9% trong telecom. Một số
miền sử dụng các chiến thuật chuyên biệt hơn như reward_incentive trong
employment (45,3%) và investment (43,0%), hay fear trong debt_collection (23,7%).
Đáng chú ý, authority chiếm 25,1% trong public_service, phản ánh xu hướng giả mạo
cơ quan nhà nước hoặc tổ chức chính thống. Các kết quả này cho thấy smishing không
chỉ dựa vào liên kết độc hại mà còn kết hợp nhiều chiến thuật tâm lý nhằm gia tăng
khả năng nạn nhân thực hiện hành động mong muốn.
56

Hình 7 Biểu đồ so sánh tỉ lệ các kĩ thuật che giấu văn bản trong tin nhắn thực và
tạo sinh
Nhìn chung, phân bố các kỹ thuật làm nhiễu trong dữ liệu tạo sinh tương đối
gần với dữ liệu thực. Kỹ thuật phổ biến nhất ở cả hai tập là whitespace_splitting,
chiếm 24,4% trong dữ liệu thực và 30,8% trong dữ liệu tạo sinh.
Character_substitution đứng thứ hai với 23,2% ở dữ liệu thực và 18,9% ở dữ liệu tạo
sinh. Một số kỹ thuật được tăng cường trong dữ liệu tạo sinh như irregular_casing
(12,3% so với 10,1%) và word_concatenation (11,4% so với 9,4%). Ngược lại,
character_repetition giảm từ 4,1% xuống còn 1,6%. Kết quả này cho thấy quá trình
tạo sinh đã bảo toàn tương đối tốt các đặc trưng làm nhiễu của dữ liệu thực, đồng thời
tăng cường một số biến thể nhằm nâng cao tính đa dạng của bộ dữ liệu.
57

Hình 8 Biểu đồ thống kê mối liên hệ giữa đối tượng được nhận và chủ đề tin nhắn
Đối tượng bị nhắm đến nhiều nhất là customer với khoảng 1.400 tin nhắn, vượt
xa các nhóm còn lại. Trong nhóm này, hai miền đóng góp lớn nhất là banking_finance
(khoảng 610 tin nhắn) và public_service (khoảng 570 tin nhắn). Nhóm job_seeker
đứng thứ hai với khoảng 850 tin nhắn, gần như toàn bộ đến từ miền employment.
Tiếp theo là debtor với khoảng 500 tin nhắn, chủ yếu thuộc miền debt_collection, và
investor với khoảng 400 tin nhắn thuộc miền investment. Các vai trò như patient,
student, business_owner hay vehicle_owner xuất hiện với tần suất thấp hơn nhiều.
Kết quả này phản ánh rằng các chiến dịch smishing thường tập trung vào những nhóm
người dùng có khả năng mang lại lợi ích tài chính trực tiếp hoặc dễ bị khai thác theo
từng ngữ cảnh chuyên biệt của từng lĩnh vực.
Phân tích WordCloud theo nhãn và nguồn dữ liệu
58

Hình 9 WordCloud của data thực và data tạo sinh theo từng nhãn
Hình 11 trình bày WordCloud của tập dữ liệu được phân chia theo hai nhãn
(Label 0 và Label 1) và hai nguồn dữ liệu (dữ liệu thực và dữ liệu tạo sinh). Kích
thước của từ trong WordCloud phản ánh tần suất xuất hiện của từ đó trong tập dữ liệu
tương ứng.
Đối với Label 0 (không lừa đảo), dữ liệu thực tập trung vào các từ khóa như
thuê bao, sử dụng, dịch vụ, khuyến mãi, gói cước và myvnpt. Các từ này chủ yếu xuất
hiện trong các tin nhắn chăm sóc khách hàng, thông báo dịch vụ hoặc quảng bá của
nhà mạng. Trong khi đó, dữ liệu tạo sinh vẫn duy trì các đặc trưng ngữ nghĩa tương
59

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
60

CHƯƠNG 4 PHƯƠNG PHÁP VÀ THIẾT LẬP THỰC NGHIỆM
4.1 Tổng quan thiết kế thực nghiệm
Sau quá trình xây dựng và phân tích bộ dữ liệu ViSmish, chương này trình bày
phương pháp thực nghiệm được sử dụng để đánh giá khả năng phát hiện tin nhắn
smishing tiếng Việt của các mô hình học sâu, mô hình ngôn ngữ tiền huấn luyện và
một số mô hình ngôn ngữ lớn. Thiết kế thực nghiệm không chỉ hướng đến việc xác
định mô hình có kết quả tổng thể tốt nhất, mà còn làm rõ mức độ ổn định của mô hình
trên các nhóm dữ liệu khác nhau, những trường hợp mô hình thường dự đoán sai và
vai trò thực tế của dữ liệu tạo sinh trong quá trình huấn luyện.
Trong thiết kế này, chưng cất tri thức không được xem là một hướng thực
nghiệm tách biệt, mà được đưa trực tiếp vào benchmark như các biến thể huấn luyện
tương ứng. Cách tổ chức này cho phép đánh giá tác động của chưng cất bằng phép so
sánh trực tiếp giữa từng mô hình hard-label và phiên bản distilled của chính mô hình
đó, đồng thời vẫn duy trì cùng dữ liệu và quy trình đánh giá với các mô hình còn lại.
Thiết kế thực nghiệm trên được xây dựng để trả lời bốn câu hỏi nghiên cứu.
Câu hỏi thứ nhất (RQ1) tập trung vào sự khác biệt hiệu năng giữa các nhóm mô hình.
Câu hỏi thứ hai (RQ2) xem xét tác động của các đặc điểm dữ liệu đến kết quả dự
đoán. Câu hỏi thứ ba (RQ3) đi sâu vào các loại lỗi và vùng dữ liệu mà mô hình chưa
xử lý tốt. Câu hỏi cuối cùng (RQ4) phân tích chuyên sâu hiệu quả của distillation khi
thay đổi teacher và chiến lược truyền soft label cho cùng một student TextCNN.
61

Hình 10 Quy trình thực nghiệm tổng quát
*RQ1 — Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ liệu
ViSmish?
*RQ2 — Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như thế
nào đến khả năng phát hiện smishing?
*RQ3 — Các mô hình thường thất bại ở những trường hợp nào và nguyên nhân
có thể là gì?
*RQ4 — RQ4: Knowledge distillation có giúp mô hình nhẹ hơn đạt trade-off tốt
hơn không??
4.2 Các phương pháp đánh giá
Benchmark được xây dựng để khảo sát 17 cấu hình mô hình thuộc ba nhóm
kiến trúc: mô hình neural cấp ký tự, encoder tiền huấn luyện và mô hình ngôn ngữ
lớn fine-tune bằng LoRA. Cách chia này cho phép so sánh nhiều mức độ phức tạp
khác nhau, từ student nhẹ có chi phí triển khai thấp đến các mô hình tiền huấn luyện
có năng lực biểu diễn mạnh hơn.
Nhóm character-level gồm BiLSTM [27] và TextCNN [28], mỗi kiến trúc
được huấn luyện theo hai chế độ: hard-label và distilled từ PhoBERT-base. Nhóm
62

này được dùng để đánh giá khả năng khai thác tín hiệu bề mặt của SMS như chuỗi
số, URL, viết tắt, lỗi chính tả và các biến thể ký tự phi chuẩn. Đồng thời, các biến thể
distilled cho phép so sánh trực tiếp tác động của soft label trên cùng kiến trúc student.
Nhóm encoder PLM gồm PhoBERT-base, PhoBERT-large [29], mBERT
[30], DistilBERT multilingual [31], XLM-RoBERTa-base, XLM-RoBERTa-large
[32], VisoBERT [33], CafeBERT [34] và ViCLSR. Nhóm này đại diện cho các mô
hình đơn ngữ, đa ngữ và các mô hình được tiền huấn luyện trên miền văn bản tiếng
Việt hoặc noisy text, qua đó kiểm tra lợi ích của biểu diễn ngữ nghĩa tiền huấn luyện
đối với smishing tiếng Việt.
Nhóm LLM gồm Gemma 3 1B [35], Gemma 2B [36], Qwen3 0.6B [37] và
Qwen2.5 0.5B [38], được thích nghi bằng LoRA để giảm chi phí huấn luyện. Nhóm
này được đưa vào benchmark để kiểm tra liệu năng lực biểu diễn rộng hơn của mô
hình sinh có tạo ra lợi thế rõ ràng trên tác vụ phân loại SMS ngắn hay không.
Bộ dữ liệu đầu vào của benchmark gồm 10.562 mẫu với sáu giá trị data_origin.
Các nguồn này khác nhau cả về phương thức hình thành lẫn vai trò trong thực nghiệm.
4.3 Các độ đo đánh giá
Tập dev và test của benchmark đều có 498 mẫu Label 0 nhưng chỉ có 37 mẫu
Label 1. Với phân phối này, một mô hình dự đoán phần lớn tin nhắn là hợp lệ vẫn có
thể đạt Accuracy cao dù bỏ sót nhiều tin nhắn smishing. Vì vậy, Accuracy không
được sử dụng làm căn cứ chính để xếp hạng hoặc lựa chọn mô hình. Benchmark tập
trung vào bốn độ đo gồm Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các độ
đo được tính độc lập trên dev và test từ cùng nhãn dự đoán và xác suất của Label 1.
Để trình bày các độ đo, Label 1 được xem là lớp dương, tương ứng với tin
nhắn smishing; Label 0 là lớp âm, tương ứng với tin nhắn hợp lệ. Bốn thành phần của
ma trận nhầm lẫn được định nghĩa như sau:
Thành phần Ý nghĩa
True Negative (TN) Tin nhắn hợp lệ được dự đoán đúng là hợp lệ
False Positive (FP) Tin nhắn hợp lệ bị dự đoán nhầm thành smishing
False Negative (FN) Tin nhắn smishing bị dự đoán nhầm thành hợp lệ
63

True Positive (TP)  Tin nhắn smishing được dự đoán đúng là smishing

Precision Label 1 đo trong số các mẫu được mô hình dự đoán là smishing, có
bao nhiêu mẫu thật sự là smishing:
𝑻𝑷
| 𝑷𝒓𝒆𝒄𝒊𝒔𝒊𝒐𝒏 | =   |     |
| --------- | --- | --- |
𝟏
𝑻𝑷+𝑭𝑷
Recall Label 1 phản ánh trong số toàn bộ tin nhắn smishing, mô hình phát
hiện được bao nhiêu mẫu:
𝑻𝑷
| 𝑹𝒆𝒄𝒂𝒍𝒍 | =   |     |
| ------ | --- | --- |
𝟏 𝑻𝑷+𝑭𝑵
Recall Label 1 là một trong bốn độ đo chính vì false negative có thể khiến
người dùng tiếp xúc với nội dung lừa đảo mà không nhận được cảnh báo. Giá trị
Recall cao cho thấy mô hình bỏ sót ít smishing hơn. Tuy nhiên, Recall không thể
được diễn giải riêng lẻ: một mô hình có thể tăng Recall bằng cách dự đoán Label 1
rộng hơn, từ đó làm tăng false positive.
F1 Label 1 là trung bình điều hòa giữa Precision và Recall của lớp lừa đảo:
| 𝑷𝒓𝒆𝒄𝒊𝒔𝒊𝒐𝒏   | × 𝑹𝒆𝒄𝒂𝒍𝒍 |     |
| ----------- | -------- | --- |
|             | 𝟏        | 𝟏   |
| 𝑭𝟏 = 𝟐×     |          |     |
| 𝟏 𝑷𝒓𝒆𝒄𝒊𝒔𝒊𝒐𝒏 | +𝑹𝒆𝒄𝒂𝒍𝒍  |     |
|             | 𝟏        | 𝟏   |
  Độ đo này giúp đánh giá sự cân bằng giữa phát hiện đúng smishing và hạn chế
cảnh báo sai. Trong bối cảnh Label 1 chiếm tỷ lệ nhỏ ở dev và test, F1 Label 1 cung
cấp thông tin trực tiếp hơn Accuracy về khả năng xử lý lớp mục tiêu. Dù Precision
Label 1 không nằm trong bốn cột chính của bảng benchmark, giá trị này vẫn được
lưu và sử dụng cùng FP để giải thích nguyên nhân thay đổi của F1 Label 1.
Macro-F1 là trung bình cộng F1-score của hai lớp Label 0 và Label 1:
𝑭𝟏 +𝑭𝟏
|          | 𝟎   | 𝟏   |
| -------- | --- | --- |
| 𝑴𝒂𝒄𝒓𝒐−𝑭𝟏 | =   |     |
𝟐
64

Do hai lớp đóng góp ngang nhau, Macro-F1 hạn chế việc lớp Label 0 có số
lượng lớn chi phối kết quả tổng thể. Đây là độ đo chính dùng để lựa chọn checkpoint
trên dev và là tiêu chí tổng quát khi so sánh các cấu hình. Tuy nhiên, Macro-F1 vẫn
được đọc cùng F1 và Recall Label 1 để tránh trường hợp hai mô hình có kết quả tổng
thể gần nhau nhưng khác biệt đáng kể về khả năng phát hiện smishing.
Ba độ đo trên phụ thuộc vào ngưỡng chuyển xác suất thành nhãn, được cố định
ở mức 0,5 trong benchmark. Để bổ sung góc nhìn không phụ thuộc vào một ngưỡng
duy nhất, nghiên cứu sử dụng thêm độ đo PR-AUC dựa trên xác suất dự đoán của
Label 1. Đường cong Precision–Recall giúp mô tả sự thay đổi giữa Precision và
Recall khi ngưỡng phân loại được dịch chuyển. Trong phần triển khai, PR-AUC được
tính bằng average_precision_score, tức Average Precision tổng hợp Precision tại các
mức Recall khác nhau. Độ đo này phù hợp với bài toán có lớp dương hiếm vì tập
trung trực tiếp vào chất lượng xếp hạng các mẫu smishing thay vì bị chi phối bởi số
lượng true negative lớn.
PR-AUC cao cho thấy mô hình có khả năng đưa các mẫu smishing lên vùng
xác suất cao một cách ổn định trên nhiều ngưỡng. Tuy nhiên, PR-AUC không thay
thế các metric tại ngưỡng vận hành: một mô hình có PR-AUC tốt vẫn có thể tạo ra số
FP hoặc FN không phù hợp tại ngưỡng 0,5. Vì vậy, PR-AUC được sử dụng cùng
Macro-F1, F1 Label 1 và Recall Label 1 thay vì làm tiêu chí duy nhất.
Độ đo Thành phần phản ánh Vai trò trong nghiên cứu
Macro-F1 Cân bằng F1 giữa Label 0 và Độ đo tổng quát và tiêu chí chọn
Label 1 checkpoint trên dev
F1 Label 1 Cân bằng Precision–Recall Đánh giá trực tiếp chất lượng
của smishing phân loại lớp mục tiêu
Recall Label 1 Tỷ lệ smishing được phát Theo dõi nguy cơ bỏ sót
hiện smishing
65

PR-AUC Chất lượng Precision–Recall Đánh giá khả năng xếp hạng
trên nhiều ngưỡng trong dữ liệu mất cân bằng
Bảng 12. Định nghĩa 4 độ đo chính
Bên cạnh bốn độ đo chính, ma trận nhầm lẫn và các giá trị TN, FP, FN, TP
được lưu cho từng mô hình trên mỗi split. Các con số này sẽ hỗ trợ diễn giải kết quả
và phân tích lỗi ở Chương 5. Cụ thể, FN có thể cho biết số smishing bị bỏ sót, còn FP
phản ánh số tin nhắn hợp lệ bị cảnh báo sai. Precision Label 1, Accuracy, Weighted-
F1 và ROC-AUC cũng được pipeline tính và lưu như các chỉ số bổ trợ, nhưng không
được dùng làm bốn độ đo benchmark chính.
Do mỗi tập dev và test chỉ có 37 mẫu Label 1, một vài dự đoán thay đổi cũng
có thể tạo ra chênh lệch đáng kể về F1 hoặc Recall Label 1. Chẳng hạn, một mẫu
smishing tương ứng khoảng 2,70 điểm phần trăm Recall. Vì vậy, khi phân tích kết
quả, nghiên cứu xem xét đồng thời giá trị metric và số lượng FP/FN nhằm tránh diễn
giải chênh lệch nhỏ như bằng chứng chắc chắn về ưu thế của một kiến trúc.
4.4 Thiết lập môi trường và tham số
Để bảo đảm kết quả giữa 17 cấu hình mô hình có thể so sánh trực tiếp,
benchmark sử dụng một bộ train, dev và test thống nhất được tạo từ phiên bản hoàn
chỉnh của ViSmish. Chiến lược phân chia được thiết kế theo hai yêu cầu. Thứ nhất,
tập phát triển và tập kiểm thử chỉ chứa dữ liệu thật hoặc dữ liệu chéo miền đã được
thu thập và tuyển chọn, qua đó tránh đánh giá mô hình trên chính kiểu dữ liệu tạo
sinh đã xuất hiện trong huấn luyện. Thứ hai, phân phối của các nguồn dữ liệu, nhãn
và danh mục nội dung cần được duy trì tương đối ổn định giữa dev và test để hạn chế
sai lệch do cách chia dữ liệu.
Đầu vào dự đoán của mô hình là nội dung văn bản; metadata chỉ được dùng
để thực hiện stratified split và phân tích hiệu năng theo từng lát cắt. Cách thiết kế này
hạn chế nguy cơ rò rỉ nhãn từ các thuộc tính được xây dựng trong quá trình tạo sinh
hoặc gán nhãn dữ liệu, đặc biệt là category và obfuscation_level.
66

Từ thành phần dữ liệu trên, quá trình phân chia được thực hiện với seed cố
định 42. Các mẫu thuộc ba nguồn gần với dữ liệu đánh giá thực tế, gồm real,
external_real và external_curated, được chia theo tỷ lệ mục tiêu 70% cho train, 15%
cho dev và 15% cho test. Quá trình phân tầng sử dụng khóa kết hợp label ×
data_origin × category. So với chỉ phân tầng theo nhãn, khóa kết hợp này giúp dev
và test duy trì tốt hơn thành phần nguồn dữ liệu và các nhóm nội dung, đồng thời hạn
chế trường hợp một category chỉ xuất hiện trong một split.
Các nguồn synthetic, paraphrased và synthetic_hard_positive được đưa toàn
bộ vào train, vì mục tiêu của benchmark là đánh giá khả năng mô hình học từ dữ liệu
tổng hợp nhưng vẫn tổng quát hóa sang dữ liệu thật hoặc dữ liệu chéo miền. Nếu đưa
dữ liệu tạo sinh vào dev hoặc test, kết quả có thể phản ánh mức độ mô hình nhận diện
các mẫu cùng quy trình tạo sinh thay vì năng lực phát hiện smishing trong điều kiện
thực tế.
Do phân tầng được thực hiện đồng thời theo nhãn, nguồn và category, cần phải
có chiến lược xử lý cụ thể cho trường hợp strata có số lượng mẫu rất nhỏ. Với strata
có dưới 5 mẫu, toàn bộ dữ liệu được giữ lại trong train để tránh tạo ra các tập đánh
giá chỉ có một mẫu không ổn định. Theo quy tắc triển khai đang áp dụng, strata từ 5
đến dưới 10 mẫu được ưu tiên giữ phần lớn trong train và tối đa một mẫu trong dev;
các strata đủ lớn mới được chia theo tỷ lệ 70/15/15.
Sau khi áp dụng chính sách trên, tập train có 9.492 mẫu, trong khi dev và test
đều có 535 mẫu. Tỷ lệ trên toàn bộ bộ dữ liệu lần lượt là 89,87%, 5,07% và 5,07%.
Tỷ lệ toàn cục không còn là 70/15/15 vì 6.994 mẫu thuộc các nguồn tạo sinh được
giữ hoàn toàn trong train. Tỷ lệ 70/15/15 chỉ áp dụng cho nhóm nguồn có khả năng
xuất hiện trong holdout gồm real, external_real và external_curated.
Split Real External_real External_curated Paraphrased Synthetic Synthetic_hard_pos. Total
train 1,797 350 351 4,333 2,008 653 9,492
dev 385 75 75 0 0 0 535
test 385 75 75 0 0 0 535
Total 2,567 500 501 4,333 2,008 653 10,562
Bảng 13. Phân phối train/dev/test
67

Về môi trường, các mô hình thực nghiệm được cài đặt trên môi trường máy ảo
của Kaggle, sử dụng Nvidia GPU T4 16GB RAM x 2. Các tham số cho từng nhóm
mô hình thực nghiệm được trình bày ở 3 bảng sau đây:
| Thành phần                | BiLSTM         | TextCNN        |
| ------------------------- | -------------- | -------------- |
| Độ dài tối đa             | 256 ký tự      | 256 ký tự      |
| Embedding dimension       | 64             | 64             |
| Hidden dimension          | 64 mỗi chiều   | -              |
| Số filter                 | -              | 96/kernel      |
| Kernel size               | -              | 3,4,5          |
| Dropout                   | 0.3            | 0.3            |
| Batch size                | 128            | 128            |
| Epoch tối đa              |  12            |  12            |
| Learning rate             |  2*10^-3       |  2*10^-3       |
|  Weight decay             |  10^-4         |  10^-4         |
|  Early stopping           |  Patience=3    |  Patience=3    |
| Tiêu chí chọn checkpoint  |  Dev Macro-F1  |  Dev Macro-F1  |

Bảng 14. Thiết lập tham số nhóm Character-level model
Benchmark distilled dùng teacher PhoBERT-base, temperature = 2 và alpha = 0.
Study RQ4 dùng TextCNN với ba teacher PhoBERT-base, CafeBERT và ViCLSR,
chạy ba seed 42/123/2025. PhoBERT-base và PhoBERT-large dùng bước phân đoạn
từ  tiếng  Việt  trước  tokenization.  Các  encoder  còn  lại  dùng  tokenizer  đi  kèm
checkpoint.
| Thành phần  | Cấu hình chung  | XLM-RoBERTa-large  |
| ----------- | --------------- | ------------------ |
và ViCLSR
| Max length    | 128 token  | 128 token  |
| ------------- | ---------- | ---------- |
| Epoch tối đa  | 3          | 3          |
68

| Train batch size            | 16            |     | 8             |     |     |
| --------------------------- | ------------- | --- | ------------- | --- | --- |
| Evaluation batch size       | 32            |     | 16            |     |     |
| Gradient accumulation       | 1             |     | 2             |     |     |
| Effective train batch size  | 16            |     | 16            |     |     |
| Learning rate               | 2*10^-5       |     | 2*10^-5       |     |     |
| Weight decay                | 0,01          |     | 0,01          |     |     |
| Warmup ratio                | 0,1           |     | 0,1           |     |     |
| Mixed precision             | FP16          |     | FP16          |     |     |
| Early stopping              | Patience = 2  |     | Patience = 2  |     |     |
| Tiêu chí chọn checkpoint    | Dev Macro-F1  |     | Dev Macro-F1  |     |     |
 Bảng 15. Thiết lập tham số nhóm Encoder PLM fine-tuning

| Thành phần       |     | Giá trị cấu hình                   |     |     |     |
| ---------------- | --- | ---------------------------------- | --- | --- | --- |
| Mô hình áp dụng  |     | Gemma 3 1B, Gemma 2B, Qwen3 0.6B,  |     |     |     |
Qwen2.5 0.5B
| LoRA rank (r)   |     | 8        |          |          |          |
| --------------- | --- | -------- | -------- | -------- | -------- |
| LoRA alpha      |     | 16       |          |          |          |
| LoRA dropout    |     | 0.1      |          |          |          |
| Target modules  |     | q_proj,  | v_proj,  | k_proj,  | o_proj,  |
gate_proj, up_proj, down_proj
| Max length             |     | 512      |     |     |     |
| ---------------------- | --- | -------- | --- | --- | --- |
| Batch size             |     | 4        |     |     |     |
| Gradient accumulation  |     | 4        |     |     |     |
| Effective batch size   |     | 16       |     |     |     |
| Learning rate          |     | 2*10^-4  |     |     |     |
| Epoch                  |     | 3        |     |     |     |
| Precision              |     | BF16     |     |     |     |
 Bảng 16 Thiết lập tham số nhóm LLM fine-tuning
69

CHƯƠNG 5 KẾT QUẢ VÀ PHÂN TÍCH
5.1 RQ1: Các nhóm mô hình khác nhau đạt hiệu quả như thế nào trên bộ dữ
liệu ViSmish?
Bảng dưới đây trình bày kết quả của 17 cấu hình trên tập dev và test theo bốn
độ đo Macro-F1, F1 Label 1, Recall Label 1 và PR-AUC. Các mô hình được chia
thành ba nhóm gồm neural network cấp ký tự, encoder PLM được fine-tune toàn phần
và LLM được fine-tune hiệu quả tham số bằng LoRA. Trong phần này, kết quả dev
được sử dụng để so sánh và lựa chọn mô hình; kết quả test chỉ được xem xét sau đó
nhằm kiểm tra liệu xu hướng quan sát trên dev có được duy trì hay không.
Bảng 17 Kết quả benchmark 17 cấu hình trên 2 tập dev, test
Theo tiêu chí chính là Macro-F1 trên dev, Gemma 2B là cấu hình tốt nhất với
0,9553. Mô hình này đồng thời đứng đầu F1 Label 1 với 0,9167 và chỉ tạo 2 FP, 4
FN trên dev, nên được chọn là mô hình cân bằng tổng thể tốt nhất trong benchmark.
Tuy vậy, “tốt nhất” còn phụ thuộc mục tiêu vận hành: DistilBERT multilingual đạt
Recall Label 1 cao nhất trên dev (0,9459), còn Qwen2.5 0.5B đạt PR-AUC cao nhất
(0,9648), cho thấy khả năng xếp hạng mẫu smishing tốt trên nhiều ngưỡng.
70

Xét theo nhóm mô hình, các mô hình pretrained chiếm ưu thế rõ rệt so với
nhóm character-level. Trong nhóm encoder PLM, CafeBERT là cấu hình tốt nhất trên
dev với Macro-F1 0,9472 và F1 Label 1 0,9014; ViCLSR theo sát với Macro-F1
0,9419. Nhóm LLM cho kết quả mạnh nhất về tổng thể, nhưng quy mô tham số không
quyết định hoàn toàn thứ hạng: Qwen2.5 0.5B vượt nhiều mô hình lớn hơn ở PR-
AUC, trong khi Gemma 2B vượt Gemma 3 1B ở cả bốn độ đo dev.
Nhóm character-level có hiệu năng thấp hơn các mô hình pretrained nhưng có
ý nghĩa triển khai. TextCNN là cấu hình tốt nhất của nhóm trên dev với Macro-F1
0,9170 và F1 Label 1 0,8451, vượt BiLSTM ở cả hai độ đo này. Distillation chưa tạo
cải thiện nhất quán về Macro-F1: BiLSTM distilled thấp hơn BiLSTM hard-label,
còn TextCNN distilled thấp hơn TextCNN hard-label nhẹ về Macro-F1 nhưng tăng
Recall Label 1 từ 0,8108 lên 0,8378 và PR-AUC từ 0,8529 lên 0,8818. Do đó,
distillation trong benchmark chính nên được hiểu là một trade-off về độ nhạy và chất
lượng xếp hạng, không phải một cải thiện mặc định.
Tóm lại, Gemma 2B là mô hình tốt nhất theo tiêu chí chính của RQ1. Nếu ưu
tiên giảm bỏ sót smishing tại ngưỡng hiện tại, DistilBERT multilingual là lựa chọn
đáng chú ý; nếu ưu tiên xếp hạng xác suất trên nhiều ngưỡng, Qwen2.5 0.5B nổi bật
theo PR-AUC. Với triển khai nhẹ, TextCNN distilled là cấu hình character-level
thuyết phục nhất, nhưng quyết định cuối cùng vẫn cần cân bằng giữa chất lượng dự
đoán và chi phí suy luận.
5.2 RQ2: Độ dài, mức độ che giấu và các đặc điểm metadata ảnh hưởng như
thế nào đến khả năng phát hiện smishing?
Để hiểu sâu sắc về cách thức các đặc trưng dữ liệu ảnh hưởng đến khả năng
nhận diện của mô hình, phân tích theo lát cắt (slice evaluation) được thực hiện trên
tập dev đối với bốn mô hình đại diện: CafeBERT (PLM đơn ngữ tiếng Việt xuất sắc
nhất), DistilBERT multilingual (PLM đa ngữ có Recall cao nhất), TextCNN (mô
hình character-level nguyên bản tốt nhất) và TextCNN distilled (mô hình chưng cất
71

tri thức có trade-off triển khai tốt). Phân tích sử dụng bộ nhãn metadata v2 để khảo
sát theo độ dài, đặc trưng bề mặt, lĩnh vực tin nhắn, hành động yêu cầu, đối tượng
nhắm đến và thủ đoạn thuyết phục.
Hình 11 Hiệu năng của mô hình theo độ dài tin nhắn
Từ hình trên, có thể thấy khi độ dài vượt quá 240 ký tự, hiệu năng F1-score
của CafeBERT giảm từ 0,9333 xuống 0,8421, và DistilBERT multilingual giảm mạnh
từ 0,8889 xuống 0,7619. Sự suy giảm này chủ yếu do mô hình PLM bị giới hạn độ
dài tokenizer hoặc bị loãng thông tin ngữ cảnh trong các tin nhắn quá dài. Ngược lại,
TextCNN thể hiện sự ổn định cao hơn với F1-score duy trì ở mức 0,8571 ở cả nhóm
161–240 và nhóm >240 ký tự, đồng thời Recall Label 1 tăng từ 0,7500 lên 0,9000.
Điều này chỉ ra rằng các bộ lọc tích chập cục bộ (CNN) trên biểu diễn ký tự có lợi
thế trong việc bắt được các tín hiệu đặc trưng (như từ khóa hoặc liên kết độc hại) bất
kể vị trí của chúng trong các đoạn văn bản dài.
Phân
Lát cắt phối mẫu Phát hiện chính
(n0/n1)
Tín hiệu mạnh hỗ trợ phát hiện smishing. Recall đạt
Có URL 168 / 29
mức rất cao (DistilBERT: 100%, TextCNN distilled:
72

89,66%, CafeBERT & TextCNN: 86,21%). Kiểm soát
FP cực tốt (CafeBERT: 0, TextCNN: 1).
|        | Là                                                | nhóm  khó  | đối  | với  mô  hình  | ký  tự.  | Recall  của  |
| ------ | ------------------------------------------------- | ---------- | ---- | -------------- | -------- | ------------ |
| Không  | TextCNN & TextCNN distilled giảm mạnh còn 62,5%,  |            |      |                |          |              |
330 / 8
| URL  | DistilBERT giảm còn 75%, riêng CafeBERT duy trì ổn  |     |     |     |     |     |
| ---- | --------------------------------------------------- | --- | --- | --- | --- | --- |
định ở 87,5%.
|                      | Recall  | đạt  | mức  cao  | (DistilBERT:  | 100%,  | TextCNN  |
| -------------------- | ------- | ---- | --------- | ------------- | ------ | -------- |
| Brandname  260 / 14  |         |      |           |               |        |          |
distilled: 92,86%, CafeBERT & TextCNN: 85,71%).
Là nhóm khó đối với mô hình ký tự (TextCNN &
Personal  TextCNN distilled: Recall chỉ đạt 78,26%). CafeBERT
16 / 23
| Number  | và DistilBERT xử lý tốt hơn với Recall lần lượt là  |     |     |     |     |     |
| ------- | --------------------------------------------------- | --- | --- | --- | --- | --- |
86,96% và 91,30%.
Lỗi của mô hình tập trung chủ yếu ở dữ liệu Real. Các
348  /  37
mô hình kiểm soát FP trên dữ liệu hội thoại đời thường
| Nguồn  dữ  (Real)  |     |     |     |     |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- |
và bài viết mạng xã hội (tập External) cực tốt (tổng cộng
| liệu  150  | /  0  |     |     |     |     |     |
| ---------- | ----- | --- | --- | --- | --- | --- |
chỉ có 1 FP với DistilBERT, và 2 FP với mỗi mô hình
(External)
TextCNN).
Bảng 18. Phân tích kết quả theo một số lát cắt khác

|                     | Số   |         |           | F1      | Recall  |         |
| ------------------- | ---- | ------- | --------- | ------- | ------- | ------- |
| Thủ đoạn thuyết     |      | Nhãn 1  |           |         |         |         |
|                     | mẫu  |         | Mô hình   | Label   | Label   | FP  FN  |
| phục                |      | (n1)    |           |         |         |         |
|                     | (n)  |         |           | 1       | 1       |         |
| Dụ dỗ qua liên kết  | 168  | 26      | CafeBERT  | 0,9388  | 0,8846  | 0  3    |
(link_lure)
DistilBERT
|     |     |     |     | 0.9811  | 1.0000  | 1  0  |
| --- | --- | --- | --- | ------- | ------- | ----- |
multilingual
|     |     |     | TextCNN  | 0.9167  | 0.8462  | 0  4  |
| --- | --- | --- | -------- | ------- | ------- | ----- |
73

TextCNN
|     |     |     | 0.9020  0.8846  | 2  3  |
| --- | --- | --- | --------------- | ----- |
distilled
| Quà tặng /  | 150  | 17  CafeBERT  | 0.9697  0.9412  | 0  1  |
| ----------- | ---- | ------------- | --------------- | ----- |
Khuyến mại
DistilBERT
|     |     |     | 0.9714  1.0000  | 1  0  |
| --- | --- | --- | --------------- | ----- |
(reward_incentive)
multilingual
|     |     | TextCNN  | 0.9032  0.8235  | 0  3  |
| --- | --- | -------- | --------------- | ----- |
TextCNN
|     |     |     | 0.8750  0.8235  | 1  3  |
| --- | --- | --- | --------------- | ----- |
distilled
| Thúc giục thời  | 69  | 15  CafeBERT  | 0.8889  0.8000  | 0  3  |
| --------------- | --- | ------------- | --------------- | ----- |
gian (urgency)
DistilBERT
|     |     |     | 0.8966  0.8667  | 1  2  |
| --- | --- | --- | --------------- | ----- |
multilingual
|     |     | TextCNN  | 0.8889  0.8000  | 0  3  |
| --- | --- | -------- | --------------- | ----- |
TextCNN
|     |     |     | 0.9286  0.8667  | 0  2  |
| --- | --- | --- | --------------- | ----- |
distilled
| Mạo danh uy  | 29  | 3  CafeBERT  | 0.6667  0.6667  | 1  1  |
| ------------ | --- | ------------ | --------------- | ----- |
quyền (authority)
DistilBERT
|     |     |     | 0.5714  0.6667  | 2  1  |
| --- | --- | --- | --------------- | ----- |
multilingual
|     |     | TextCNN  | 0.8000  0.6667  | 0  1  |
| --- | --- | -------- | --------------- | ----- |
TextCNN
|     |     |     | 0.8000  0.6667  | 0  1  |
| --- | --- | --- | --------------- | ----- |
distilled
| Đánh vào nỗi sợ  | 20  | 3  CafeBERT  | 0.4000  0.3333  | 1  2  |
| ---------------- | --- | ------------ | --------------- | ----- |
(fear)
DistilBERT
|     |     |     | 0.8000  0.6667  | 0  1  |
| --- | --- | --- | --------------- | ----- |
multilingual
|     |     | TextCNN  | 0.5000  0.3333  | 0  2  |
| --- | --- | -------- | --------------- | ----- |
74

TextCNN
0.5000 0.3333 0 2
distilled
Đe dọa trừng phạt 15 6 CafeBERT 0.9091 0.8333 0 1
(threat)
DistilBERT
0.8000 0.6667 0 2
multilingual
TextCNN 0.8000 0.6667 0 2
TextCNN
0.9091 0.8333 0 1
distilled
Bảng 19. Phân tích hiệu quả của mô hình đối với một số thủ đoạn lừa đảo
Ghi chú: Thủ đoạn scarcity (n1=4, F1=1.0 và Recall=1.0 đối với tất cả mô hình) và
off_platform_contact (n1=8, F1 và Recall đều \(\ge 0,93\)) được bỏ qua để tập trung
vào các nhóm phức tạp.
Thủ đoạn dụ dỗ qua liên kết (link_lure) và Quà tặng (reward_incentive): Đây
là nhóm thủ đoạn dễ phát hiện nhất. DistilBERT multilingual đạt Recall 100% trên
cả hai nhóm này. CafeBERT cũng đạt F1-score rất cao (lần lượt là 0,9388 và 0,9697).
Lý do là các thủ đoạn này thường đi kèm các cấu trúc từ vựng mang tính chào mời,
chúc mừng trúng thưởng và các URL rõ ràng, tạo điều kiện thuận lợi cho cơ chế chú
ý của transformer nhận diện.
Thủ đoạn thúc giục thời gian (urgency): Có độ khó trung bình. Các mô hình
bỏ sót từ 2 đến 3 mẫu (Recall dao động từ 80,00% đến 86,67%), do các từ khóa thúc
giục thời gian (như "ngay", "trong 24h", "hạn chót") cũng xuất hiện thường xuyên
trong tin nhắn OTP hoặc quảng cáo viễn thông hợp lệ.
Thủ đoạn đánh vào nỗi sợ (fear) và Mạo danh uy quyền (authority): Đây là
những nhóm thủ đoạn khó nhất. Khi kẻ xấu đe dọa tài khoản bị khóa hoặc yêu cầu
cập nhật khẩn cấp dưới danh nghĩa cơ quan công quyền, Recall của CafeBERT và
hai mô hình TextCNN trên nhóm fear chỉ đạt 33,33% (bỏ sót 2 trên 3 mẫu).
75

DistilBERT multilingual đạt Recall tốt hơn ở mức 66,67% nhưng đổi lại phải đánh
đổi bằng việc tăng FP trên nhóm authority (F1-score giảm xuống 0,5714).
Thủ đoạn đe dọa trừng phạt (threat): CafeBERT và TextCNN distilled đạt hiệu
năng vượt trội với F1-score 0,9091 và Recall 83,33% (chỉ bỏ sót 1 mẫu). Điều này
cho thấy khả năng hiểu ngữ cảnh đe dọa mang tính hình sự/pháp luật của CafeBERT
đã được chuyển giao một cách hiệu quả sang student TextCNN thông qua hàm mục
tiêu chưng cất tri thức.
5.3 RQ3: Mô hình sai ở đâu và tại sao?
Để làm rõ nguyên nhân sâu xa dẫn đến các thất bại phân loại, chúng ta tiến hành
khảo sát thống kê trên tập lỗi của 4 mô hình đại diện trên tập dev trong bảng dưới
đây:
Mô hình FP FN Tổng lỗi Lỗi confidence >= 0,9
CafeBERT 2 5 7 5
DistilBERT multilingual 7 2 9 8
TextCNN 4 7 11 7
TextCNN distilled 6 6 12 5
Bảng 20. Phân loại số lượng mẫu lỗi của các mô hình
Một điểm đáng chú ý là phần lớn các lỗi phân loại của mô hình đều có mức độ
tự tin (confidence score) cực kỳ cao (ví dụ: 5 trên 7 lỗi của CafeBERT và 8 trên 9 lỗi
của DistilBERT có độ tin cậy từ 0,9 trở lên). Điều này chứng tỏ mô hình không đơn
thuần là phân vân ở ranh giới quyết định, mà thực sự bị đánh lừa sâu sắc bởi các đặc
trưng gây nhiễu trong tin nhắn.
Để kiểm tra xem các mô hình có hành vi lỗi tương đồng hay khác biệt, chúng
ta tính toán ma trận độ giao thoa lỗi (Jaccard similarity) được trình bày trong Bảng
dưới đây.
76

|           |           | DistilBERT    |          | TextCNN    |
| --------- | --------- | ------------- | -------- | ---------- |
| Mô hình   | CafeBERT  |               | TextCNN  |            |
|           |           | multilingual  |          | distilled  |
| CafeBERT  | 1,0000    | 0,1429        | 0,2857   | 0,2667     |
DistilBERT
|     | 0,1429  | 1,0000  | 0,1765  | 0,1667  |
| --- | ------- | ------- | ------- | ------- |
multilingual
| TextCNN  | 0,2857  | 0,1765  | 1,0000  | 0,7692  |
| -------- | ------- | ------- | ------- | ------- |
TextCNN
|     | 0,2667  | 0,1667  | 0,7692  | 1,0000  |
| --- | ------- | ------- | ------- | ------- |
distilled
Bảng 21. Bảng ma trận giao thoa lỗi Jaccard giữa các mô hình
Kết quả chỉ ra rằng:
•  CafeBERT và DistilBERT multilingual: Có mức độ giao thoa lỗi cực kỳ thấp
(Jaccard = 0,1429, chỉ chung nhau đúng 2 lỗi). Điều này khẳng định hai kiến
trúc này học được các không gian biểu diễn rất khác nhau: CafeBERT đơn ngữ
hóa tối ưu việc kiểm soát FP, trong khi DistilBERT đa ngữ hóa nhạy bén tối
đa hóa Recall và chấp nhận nhiều FP hơn.
•  TextCNN và TextCNN distilled: Có mức độ giao thoa lỗi rất lớn (Jaccard =
0,7692, chung nhau đến 10 lỗi trên tổng số 13 lỗi gộp). Sự tương đồng cao này
chứng tỏ cơ chế chưng cất tri thức từ PhoBERT-base sang TextCNN chủ yếu
giúp student tinh chỉnh xác suất đầu ra ở các mẫu biên để tăng độ nhạy, nhưng
chưa thể tái định hình hoàn toàn ranh giới quyết định vốn bị giới hạn bởi cấu
trúc trích xuất đặc trưng dạng ký tự cục bộ của TextCNN.
Phân tích định tính các nhóm lỗi tiêu biểu
| Nhóm  Loại  |     | Mẫu tiêu  | Mô hình bị  |     |
| ----------- | --- | --------- | ----------- | --- |
Metadata  nổi bật  Diễn giải
| lỗi  lỗi  |     | biểu  | ảnh hưởng  |     |
| --------- | --- | ----- | ---------- | --- |
message_domain
|     | =debt_collecti | ViSmis | Cả 4 mô hình ở  | Ngôn ngữ pháp lý và  |
| --- | -------------- | ------ | --------------- | -------------------- |
Đòi  nợ
|     | on;  | h_0796 | ViSmish_0 | nhắc  nợ  giống thông  |
| --- | ---- | ------ | --------- | ---------------------- |
không
|           | roles=debtor;   | 0,     | 7960;       | báo hợp lệ, không có  |
| --------- | --------------- | ------ | ----------- | --------------------- |
| URL,  FN  |                 |        |             |                       |
|           |                 | ViSmis |             | URL làm tín hiệu bề   |
|           | has_url=false;  |        | DistilBERT  | ở                     |
vai  trò
|     |     | h_0336 | ViSmish_0 | mặt nên mô hình dễ bỏ  |
| --- | --- | ------ | --------- | ---------------------- |
tactics=urgenc
con nợ
|     | y/threat/fear/ | 8   | 3368  | sót.  |
| --- | -------------- | --- | ----- | ----- |
authority;
77

actions=call_p
hone/visit_phy
sical_location
message_domain
=banking_finan
ViSmis
|     | ce/commerce;  | h_0324 |     |     |     |
| --- | ------------- | ------ | --- | --- | --- |
Link-
| lure  | has_url=true;  | 9,  |     | Tin  nhắn  | mô  phỏng  |
| ----- | -------------- | --- | --- | ---------- | ---------- |
CafeBERT,
| giống  | actions=click_ | ViSmis |     | cảnh báo bảo mật, giao  |     |
| ------ | -------------- | ------ | --- | ----------------------- | --- |
TextCNN,
| thông  FN  | or_visit_link/ | h_0499 |     | hàng  hoặc  | ứng  dụng  |
| ---------- | -------------- | ------ | --- | ----------- | ---------- |
TextCNN
| báo giao  | provide_person | 5,  |     | ngân hàng quá giống  |     |
| --------- | -------------- | --- | --- | -------------------- | --- |
distilled
ViSmis
| dịch/cản | al_information;  |        |     | thông báo dịch vụ thật.  |     |
| -------- | ---------------- | ------ | --- | ------------------------ | --- |
| h báo    | tactics=link_l   | h_0539 |     |                          |     |
|          | ure/urgency/au   | 9      |     |                          |     |
thority/fear
message_domain
=gambling/adul
t_service;
sender_type=pe
rsonal_number;
|     | obfuscation.pr | ViSmis |     | Ký  tự  | bị  biến  dạng  |
| --- | -------------- | ------ | --- | ------- | --------------- |
Miền
|           | esent=true;    | h_0162 |           | mạnh                 | làm  tín  hiệu  |
| --------- | -------------- | ------ | --------- | -------------------- | --------------- |
| nhạy      |                |        | CafeBERT  | và                   |                 |
|           | obfuscation.se | 4,     |           | smishing             | bị  phân        |
| cảm,  FN  |                |        | hai  mô   | hình                 |                 |
|           |                | ViSmis |           | mảnh, khiến mô hình  |                 |
verity=3;
| nhiễu bề  |                |        | TextCNN  |                       |     |
| --------- | -------------- | ------ | -------- | --------------------- | --- |
|           | text_phenomena | h_0826 |          | không nhận ra ý định  |     |
mặt cao
|     | =character_sub | 9   |     | lừa đảo.  |     |
| --- | -------------- | --- | --- | --------- | --- |
stitution/punc
tuation_insert
ion/whitespace
_splitting/tee
ncode
| Hội  | message_domain | ViSmis | DistilBERT  | Văn  bản  | phi  chuẩn  |
| ---- | -------------- | ------ | ----------- | --------- | ----------- |
FP
thoại  cá  =personal_soci h_0142 multilingual,  hoặc  cảm  xúc  mạnh
| nhân  | al;  | 9,  | TextCNN,  | kích  hoạt  | nhầm,  dù  |
| ----- | ---- | --- | --------- | ----------- | ---------- |
78

| không  | actions=none;  | ViSmis | TextCNN  | metadata v2 không có  |     |
| ------ | -------------- | ------ | -------- | --------------------- | --- |
có  hành  has_url=false;  h_0476 distilled;  một  yêu cầu truy cập, liên
| động     | has_phone=fals | 5,     | mẫu       | với  hệ hay cung cấp thông  |     |
| -------- | -------------- | ------ | --------- | --------------------------- | --- |
| yêu cầu  | e;             | ViSmis | CafeBERT  | tin.                        |     |
h_0610
text_phenomena
9,
=teencode/diac
|     | ritic_omission | ViSmis |     |     |     |
| --- | -------------- | ------ | --- | --- | --- |
|     | /abbreviation/ | h_0806 |     |     |     |
|     | character_repe | 0      |     |     |     |
tition
message_domain
=employment;
Tuyển
roles=student;
| sinh/hội   | actions=click_ | ViSmis |                |                          |     |
| ---------- | -------------- | ------ | -------------- | ------------------------ | --- |
|            |                |        | DistilBERT     | Tin hợp lệ vẫn có link,  |     |
| thảo hợp   | or_visit_link/ | h_0691 |                |                          |     |
|            |                |        | multilingual,  | lời mời đăng ký và yêu   |     |
| lệ có yêu  | provide_person | 7,     |                |                          |     |
| FP         |                |        | TextCNN,       | cầu liên hệ, nên giống   |     |
|            | al_information | ViSmis |                |                          |     |
cầu
|          |                |        | TextCNN    | hard  negative  | của  |
| -------- | -------------- | ------ | ---------- | --------------- | ---- |
| đăng     | /contact_off_p | h_0754 |            |                 |      |
|          |                |        | distilled  | smishing.       |      |
| ký/liên  | latform;       | 5      |            |                 |      |
| hệ       | sender_type=br |        |            |                 |      |
andname/person
al_number
message_domain
ViSmis
=public_servic
h_0437
Thông báo hợp lệ từ tổ
|     | e/marketing_pr |     | Chủ  | yếu  |     |
| --- | -------------- | --- | ---- | ---- | --- |
3,
| Brandna |                |     |             | chức/cơ  | quan  có  cấu  |
| ------- | -------------- | --- | ----------- | -------- | -------------- |
|         | omotion/commer |     | DistilBERT  |          |                |
ViSmis
| me/cơ     |      |        |               | trúc  giống  | cảnh  báo  |
| --------- | ---- | ------ | ------------- | ------------ | ---------- |
|           | ce;  | h_0543 | multilingual  |              |            |
| quan  có  |      |        |               | hoặc  yêu    | cầu  hành  |
sender_type=br
| FP       |     | 2,  | và  TextCNN  |             |           |
| -------- | --- | --- | ------------ | ----------- | --------- |
| authorit |     |     |              | động,  làm  | mô  hình  |
andname;
|          |                | ViSmis | distilled;  | một   |       |
| -------- | -------------- | ------ | ----------- | ----- | ----- |
| y  hoặc  |                |        |             | đánh  | đồng  |
|          | tactics=author |        | mẫu         | với   |       |
h_0802
| link  |                 |     |           | authority/link  | với  |
| ----- | --------------- | --- | --------- | --------------- | ---- |
|       | ity/link_lure;  |     | CafeBERT  |                 |      |
9,
smishing.
|     | có  thể  có   | ViSmis |     |     |     |
| --- | ------------- | ------ | --- | --- | --- |
|     | has_url=true  | h_0824 |     |     |     |
79

6,
ViSmis
h_1044
3
Bảng 22. Bảng phân tích tất cả lí do lỗi mô hình gặp phải
Tóm lại, RQ3 cho thấy các lỗi FP/FN trên dev có thể được giải thích tốt hơn bằng
tổ hợp metadata v2 thay vì các nhãn cũ. FN tập trung ở ba kiểu chính: đòi nợ không
URL, smishing có link nhưng giống thông báo chính thống, và tin nhắn miền nhạy
cảm có nhiễu bề mặt cao. FP tập trung ở các hard negative hợp lệ: hội thoại cá nhân
phi chuẩn, tuyển sinh/hội thảo có yêu cầu đăng ký, và thông báo brandname/cơ quan
có authority hoặc link. Định hướng cải thiện tiếp theo nên bổ sung hard positives/hard
negatives theo đúng các tổ hợp metadata này, thay vì chỉ tăng thêm mẫu theo nhãn
tổng quát.
5.4 RQ4: Knowledge distillation có giúp mô hình nhẹ hơn đạt trade-off tốt hơn
không?
RQ4 đánh giá liệu soft label từ các teacher Transformer có giúp cùng một student
TextCNN cải thiện so với hard-label baseline hay không. Ba teacher được khảo sát
gồm PhoBERT-base, CafeBERT và ViCLSR; mỗi teacher được so sánh với hai chiến
lược distillation: vanilla_kd và risk_aware_kd. Các kết quả được báo cáo theo trung
bình ba seed và paired bootstrap trên tập test.
Hiệu quả distillation phụ thuộc vào teacher và chiến lược dùng soft label
Delta Recall
Teacher Chế độ KD Diễn giải
Label 1
Tăng rất nhẹ, chưa đủ
Vanilla KD +0,0093
rõ.
PhoBERT-base
Tăng recall rõ nhất; CI
Risk-aware KD +0,0900
95% nằm trên 0.
Có xu hướng cải thiện
CafeBERT Vanilla KD +0,0185
nhẹ.
80

Risk-aware KD -0,0723 Làm giảm recall rõ rệt.
Vanilla KD -0,0898 Làm giảm recall.
ViCLSR
Vẫn thấp hơn hard
Risk-aware KD -0,0633
baseline.
Bảng 23. Chênh lệch Recall Label 1 trên test so với TextCNN hard baseline
Kết quả cho thấy distillation không tự động cải thiện TextCNN. Với
PhoBERT-base, risk_aware_kd là cấu hình tốt nhất vì tăng Recall Label 1 khoảng
+0,09 trên test, phù hợp với mục tiêu giảm false negative trong bài toán smishing.
Với CafeBERT, teacher mạnh hơn nhưng vanilla_kd lại phù hợp hơn risk_aware_kd;
điều này cho thấy khi soft label đáng tin, việc giảm trọng số quá mạnh có thể làm mất
tín hiệu hữu ích. Với ViCLSR, cả hai chế độ KD đều làm giảm chất lượng so với hard
baseline, nên không nên dùng ViCLSR làm teacher cho TextCNN trong cấu hình hiện
tại.
Về triển khai, lợi thế kích thước và tốc độ đến từ kiến trúc TextCNN chứ không
phải từ distillation. Distillation không làm mô hình nhỏ hơn, vì TextCNN hard,
vanilla KD và risk-aware KD có cùng số tham số xấp xỉ 87,5 nghìn và kích thước
khoảng 0,342 MB. Vai trò của distillation chỉ là thay đổi chất lượng dự đoán của cùng
một student. Trong phép đo đại diện với PhoBERT-base, TextCNN risk-aware KD
đạt F1 Label 1 = 0,8500 với latency CPU khoảng 1,42 ms/tin, cho thấy đây là điểm
trade-off tốt nhất giữa độ nhạy phát hiện smishing và chi phí suy luận.
Tóm lại, RQ4 cho thấy knowledge distillation là một kỹ thuật có điều kiện. Nó
có thể giúp TextCNN nhẹ cải thiện recall khi teacher và chiến lược dùng soft label
phù hợp, nhưng cũng có thể làm giảm hiệu năng nếu soft target không tương thích
với student. Vì vậy, mọi mô hình distilled cần được so sánh trực tiếp với hard-label
baseline cùng kiến trúc, đặc biệt theo Recall Label 1 chứ không chỉ theo Accuracy
hoặc Macro-F1.
81

Trade-off triển khai: TextCNN nhẹ là do kiến trúc, KD chỉ thay đổi chất lượng
dự đoán
|     |     | TextCNN  | TextCNN  | TextCNN  |
| --- | --- | -------- | -------- | -------- |
PhoBERT-base
|              |              | hard    | vanilla   | risk_aware  |
| ------------ | ------------ | ------- | --------- | ----------- |
| Params       | 134,999,810  | 87,553  | 87,553    | 87,553      |
| Size (MB)    | 516.95       | 0.3417  | 0.3417    | 0.3417      |
| CPU latency  | 248.142      | 2.19    | 2.43      | 1.42        |
(ms/msg)
| Throughput  | 4.1966  | 566.42  | 602,23  | 902,58  |
| ----------- | ------- | ------- | ------- | ------- |
(SMS/s)
| F1 Label 1  | 0,8267  | 0,8378  | 0,7692  | 0,8500  |
| ----------- | ------- | ------- | ------- | ------- |
Bảng 24. So sánh chi phí triển khai của PhoBERT-base với các TextCNN student

Kết quả này cần được diễn giải tách bạch giữa hai nguồn lợi ích. TextCNN
nhỏ và nhanh hơn PhoBERT-base là do kiến trúc cấp ký tự, không phải do distillation.
Distillation không làm giảm số tham số, vì cả ba cấu hình TextCNN đều có cùng số
tham số xấp xỉ 87,5 nghìn và kích thước khoảng 0,342 MB. Nói cách khác, KD chỉ
thay đổi chất lượng dự đoán của cùng một student, còn lợi thế triển khai đến từ việc
chọn student nhẹ.
Trong cấu hình đại diện này, TextCNN risk-aware KD đạt F1 Label 1 cao nhất
trong nhóm đo deployment (0,8500), đồng thời có latency CPU khoảng 1,42 ms/tin.
TextCNN hard cũng đã có F1 Label 1 cao hơn PhoBERT-base trong phép đo này
(0,8378 so với 0,8267), cho thấy student nhẹ có thể cạnh tranh tốt nếu dữ liệu và huấn
luyện phù hợp. Ngược lại, TextCNN vanilla KD là phản ví dụ quan trọng: cùng kiến
trúc nhẹ nhưng F1 Label 1 giảm xuống 0,7692. Điều này củng cố kết luận rằng chiến
lược dùng soft label quyết định chất lượng của student distilled.
82

Tóm lại, RQ4 cho thấy knowledge distillation là một kỹ thuật có điều kiện. Nó
có thể giúp TextCNN nhẹ cải thiện recall và giữ chi phí suy luận thấp khi teacher và
chiến lược KD phù hợp, nhưng cũng có thể làm giảm hiệu năng nếu soft target không
tương thích với student. Vì vậy, mọi mô hình distilled cần được so sánh trực tiếp với
hard-label baseline cùng kiến trúc, đặc biệt theo Recall Label 1 và F1 Label 1 thay vì
chỉ theo Accuracy hoặc Macro-F1.
CHƯƠNG 6 KẾT LUẬN
6.1 Kết quả đạt được
Khóa luận đã nghiên cứu bài toán phát hiện tin nhắn lừa đảo tiếng Việt trong
bối cảnh dữ liệu thực còn hạn chế, mất cân bằng nhãn và có nhiều biến thể ngôn ngữ
đặc thù như viết tắt, thiếu dấu, chèn ký tự đặc biệt, sử dụng URL giả mạo và các biểu
hiện che giấu văn bản. Trên cơ sở đó, khóa luận đề xuất hướng tiếp cận kết hợp giữa
xây dựng dữ liệu thực, tăng cường dữ liệu bằng mô hình ngôn ngữ lớn và thử nghiệm
chưng cất tri thức nhằm hướng tới một hệ thống phát hiện smishing có khả năng ứng
dụng thực tế hơn.
Trước hết, khóa luận đã xây dựng được bộ dữ liệu tin nhắn tiếng Việt phục vụ
bài toán phân loại nhị phân giữa tin nhắn hợp lệ và tin nhắn lừa đảo. Dữ liệu thực
được thu thập từ các nguồn công khai trên mạng và từ thiết bị di động, sau đó được
làm sạch, chuẩn hóa, loại bỏ trùng lặp và gán nhãn theo phương pháp thảo luận nhóm
dựa trên đồng thuận. Bên cạnh đó, khóa luận cũng xây dựng quy trình sinh dữ liệu
tạo sinh bằng LLM với các ràng buộc về nhãn, định dạng, metadata, URL, số điện
thoại và loại người gửi nhằm kiểm soát chất lượng dữ liệu sinh ra.
Về thực nghiệm chưng cất tri thức, khóa luận đã thử nghiệm chuyển giao tri
thức từ PhoBERT-base sang các mô hình học sinh nhẹ hơn như TF-IDF + Logistic
Regression, BiLSTM và TextCNN. Kết quả cho thấy distillation không mang lại hiệu
quả đồng đều cho mọi mô hình. Trong đó, TextCNN distilled là mô hình học sinh khả
83

quan nhất, cho thấy khả năng cải thiện hiệu năng so với huấn luyện bằng nhãn cứng
và phù hợp với bài toán SMS nhờ khả năng khai thác các mẫu cục bộ như URL, chuỗi
số, ký tự bất thường và các biến thể obfuscation.
Tổng thể, khóa luận đã đạt được ba kết quả chính: xây dựng được quy trình dữ
liệu cho bài toán smishing tiếng Việt; chứng minh dữ liệu tạo sinh có giá trị khi được
dùng như augmentation có kiểm soát thay vì thay thế dữ liệu thực; và chỉ ra tiềm năng
của chưng cất tri thức trong việc xây dựng mô hình nhẹ cho bài toán phát hiện tin
nhắn lừa đảo.
6.2 Hạn chế
Mặc dù đạt được một số kết quả tích cực, khóa luận vẫn còn nhiều hạn chế. Thứ
nhất, quy mô dữ liệu thực còn nhỏ, đặc biệt là số lượng mẫu tin nhắn lừa đảo thật còn
hạn chế. Điều này khiến bộ dữ liệu chưa thể bao phủ đầy đủ các kịch bản lừa đảo
mới, các biến thể URL, các hình thức giả mạo brandname và các thủ đoạn đa kênh
trong thực tế.
Thứ hai, quy trình gán nhãn được thực hiện thông qua thảo luận nhóm nên chưa
có các chỉ số định lượng về mức độ đồng thuận giữa người gán nhãn như Cohen’s
Kappa hoặc Fleiss’ Kappa. Cách làm này phù hợp với quy mô dữ liệu hiện tại, nhưng
vẫn có thể chịu ảnh hưởng bởi sự đồng thuận xã hội hoặc ý kiến nổi trội trong nhóm.
Thứ ba, dữ liệu tạo sinh vẫn tồn tại domain gap so với dữ liệu thực. Mặc dù đã
có các bước kiểm soát chất lượng, dữ liệu synthetic vẫn có thể bị ảnh hưởng bởi
prompt, taxonomy và danh sách tri thức miền được cung cấp trước. Vì vậy, dữ liệu
tạo sinh trong khóa luận chỉ nên được xem là nguồn hỗ trợ tăng cường, không phải
nguồn thay thế dữ liệu thực.
Thứ tư, phần chưng cất tri thức mới được triển khai ở mức proof-of-concept.
Khóa luận chưa tối ưu sâu các siêu tham số như temperature, alpha, chiến lược chọn
mẫu hoặc các kỹ thuật distillation nâng cao. Ngoài ra, phạm vi mô hình thử nghiệm
còn giới hạn, chưa khảo sát nhiều kiến trúc tiếng Việt nhỏ gọn khác.
84

Cuối cùng, nghiên cứu chưa đánh giá mô hình trong môi trường triển khai thực
tế. Các yếu tố như độ trễ suy luận, bộ nhớ sử dụng, tốc độ xử lý, khả năng cập nhật
mô hình, bảo mật dữ liệu người dùng và hiệu quả vận hành trên thiết bị di động hoặc
hệ thống SMS gateway chưa được phân tích đầy đủ.
6.3 Phương hướng phát triển trong tương lai
Trong tương lai, hướng phát triển đầu tiên là mở rộng bộ dữ liệu thực, đặc biệt
là tăng số lượng mẫu tin nhắn lừa đảo thật và các mẫu hợp lệ dễ gây nhầm lẫn. Quá
trình thu thập cần đi kèm với cơ chế ẩn danh hóa chặt chẽ nhằm bảo vệ thông tin cá
nhân như số điện thoại, mã OTP, số tài khoản và nội dung nhạy cảm.
Hướng phát triển thứ hai là cải thiện quy trình gán nhãn. Khi dữ liệu được mở
rộng, nên áp dụng gán nhãn độc lập bởi nhiều người, tính toán độ đồng thuận và xử
lý các trường hợp bất đồng thông qua vòng thảo luận hoặc đánh giá chuyên gia. Điều
này sẽ giúp tăng độ tin cậy của bộ dữ liệu nếu được dùng như một benchmark nghiên
cứu.
Hướng phát triển thứ ba là mở rộng nghiên cứu chưng cất tri thức. Các nghiên
cứu tiếp theo có thể thử nghiệm thêm temperature scaling, confidence-aware
distillation, intermediate feature distillation hoặc multi-teacher distillation. Bên cạnh
đó, cần đánh giá thêm các mô hình học sinh nhỏ gọn khác để tìm ra kiến trúc phù hợp
hơn cho triển khai thực tế.
Hướng phát triển cuối cùng là đưa mô hình đến gần môi trường ứng dụng thực
tế hơn. Ngoài các chỉ số phân loại, cần đánh giá thêm thời gian suy luận, kích thước
mô hình, bộ nhớ sử dụng và khả năng xử lý trên thiết bị di động hoặc hệ thống lọc tin
nhắn quy mô lớn. Đồng thời, nên xây dựng cơ chế cập nhật định kỳ để mô hình thích
nghi với các chiến dịch smishing mới theo thời gian.
Tóm lại, khóa luận đã chứng minh rằng việc kết hợp dữ liệu thực, dữ liệu tạo
sinh có kiểm soát và chưng cất tri thức là một hướng tiếp cận khả thi cho bài toán
85

phát hiện tin nhắn lừa đảo tiếng Việt. Mặc dù vẫn còn nhiều hạn chế, các kết quả đạt
được đã tạo nền tảng cho việc phát triển các hệ thống phát hiện smishing nhẹ, hiệu
quả và có khả năng thích nghi tốt hơn trong thực tế
86

TÀI LIỆU THAM KHẢO
[1] A. &. A.-N. S. Quffa, "A Rule-Based Expert System for Cybersecurity Threat
Detection: Evolution, Applications, and the Hybrid AI Paradigm," International
Journal of Academic Engineering Research, vol. 9, no. 8, pp. 44-62, 2025.
[2] P. S. a. B. H. F. Flavio Di Palo, "Performance-Guided LLM Knowledge
Distillation for Efficient Text Classification at Scale," in Proceedings of the
2024 Conference on Empirical Methods in Natural Language Processing,
Florida, 2024.
[3] E. &. S. Y. &. W. P. &. A.-Z. Z. &. L. Y. &. W. S. &. C. W. Hu, "LoRA: Low-
Rank Adaptation of Large Language Models," in The International Conference
on Learning Representations (ICLR), 2021.
[4] A. B. U. W. M. E. M. M. a. Y. A. K. Khadka, "A Survey on the Principles of
Persuasion as a Social Engineering Strategy in Phishing," in 2023 IEEE 22nd
International Conference on Trust, Security and Privacy in Computing and
Communications (TrustCom), Exeter, 2023.
[5] F. A. J. &. M. R. Carroll, "How Good Are We at Detecting a Phishing Attack?
Investigating the Evolving Phishing Attack Email and Why It Continues to
Successfully Deceive Society," SN Computer Science, vol. 3, 2022.
[6] I. S. G. a. C. S. C. L. Ribeiro, "Eyes on phishing emails: an eye-tracking study,"
Journal of Experimental Criminology, vol. 22, pp. 189-211, 2024.
[7] H. D. N. T. T. N. D. Cho, "A Framework for Vietnamese Email Phishing
Detection," International Journal of Innovative Technology and Exploring
Engineering, vol. 9, no. 1, pp. 2258-2264, 2019.
87

[8] V. M. T. N. X. .. &. A. T. Q. Tuấn, "Evaluating the Efficiency of Vietnamese
SMS Spam Detection Techniques," Journal of Science and Technology on
Information Security, vol. 1, no. 18, pp. 30-37, 2023.
[9] "A Case of Identity: Detection of Suspicious IDN Homograph Domains Using
Active DNS Measurements," in 2020 IEEE European Symposium on Security
and Privacy Workshops (EuroS&PW), Genoa, 2020.
[10] S . S. D. Mishra, "DSmishSMS-A System to Detect Smishing SMS," Neural
Comput & Applic, vol. 35, p. 4975–4992, 2023.
[11] M . &. I. M. &. K. D. Salman, "Investigating Evasive Techniques in SMS Spam
Filtering: A Comparative Analysis of Machine Learning Models," IEEE Access,
vol. 12, pp. 24306-24324, 2024.
[12] S . Y. Y. K. S. Mohammed Rasol Al Saidat, "Advancements of SMS Spam
Detection: A Comprehensive Survey of NLP and ML Techniques," Procedia
Computer Science , vol. 244, pp. 248-259, 2024.
[13] S . M. A. A.-A. M. O. Olusola Abayomi-Alli, "A review of soft techniques for
SMS spam classification: Methods, approaches and applications," Engineering
Applications of Artificial Intelligence, vol. 86, pp. 197-212, 2019.
[14] E . F. E. A. L. F.-R. Alicia Martínez-Mendoza, "Building a multi-class Short
Message Service dataset for smishing detection using agglomerative clustering
and dataset fusion," Engineering Applications of Artificial Intelligence, vol.
163, 2026.
[15] J .-T. L. H.-C. R. Dae-Neung Sohn, "The Contribution of Stylistic Information
to Content-based Mobile Spam Filtering," in Proceedings of the ACL-IJCNLP
2009 Conference Short Papers, Suntec, 2009.
88

[16] H . S. Shaghayegh Hosseinpour, "Complex-network based model for SMS spam
filtering," Computer Networks, vol. 255, 2024.
[17] A . &. G. B. B. &. K. K. &. B. P. &. A. W. &. A. A. Jain, "A content and URL
analysis‐based efficient approach to detect smishing SMS in intelligent
systems," International Journal of Intelligent Systems, vol. 37, 2022.
[18] C . &. C. R. &. N.-M. A. Bucila, "Model compression," in Proceedings of the
Twelfth ACM SIGKDD International Conference on Knowledge Discovery and
Data Mining, Pennsylvania, 2006.
[19] G . V. O. &. D. J. Hinton, "Distilling the Knowledge in a Neural Network,"
ArXiv, 2015.
[20] V . &. D. L. &. C. J. &. W. T. Sanh, "DistilBERT, a distilled version of BERT:
smaller, faster, cheaper and lighter," 2019.
[21] R . &. L. Y. &. L. L. &. M. L. &. V. O. &. L. J. Tang, "Distilling Task-Specific
Knowledge from BERT into Simple Neural Networks," 2019.
[22] S . &. A. A. Mukherjee, "Distilling Transformers into Simple Neural Networks
with Unlabeled Transfer Data," 2019.
[23] B . M. N. R. M. S. e. a. Tom B. Brown, "Language models are few-shot
learners," in In Proceedings of the 34th International Conference on Neural
Information Processing Systems (NIPS '20), New York, 2020.
[24] Q . F. S. H. M. S. C. O. H. G. A. E. J. S.-S. a. D. C. S. Jules White, "A Prompt
Pattern Catalog to Enhance Prompt Engineering with ChatGPT," in In
Proceedings of the 30th Conference on Pattern Languages of Programs (PLoP
'23), The Hillside Group, 2023.
89

[25] R . W. R. X. J. Z. X. D. G. C. a. H. W. Lin Long, "On LLMs-Driven Synthetic
Data Generation, Curation, and Evaluation: A Survey," in Findings of the
Association for Computational Linguistics: ACL 2024, Bangkok, 2024.
[26] T .-P. L. a. K. N. Thanh-Nhi Nguyen, "ViLexNorm: A Lexical Normalization
Corpus for Vietnamese Social Media Text," in Proceedings of the 18th
Conference of the European Chapter of the Association for Computational
Linguistics, St. Julian’s, 2024.
[27] M . E. H. S. Zahra Jamshidzadeh, "Bidirectional Long Short-Term Memory
(BILSTM) - Support Vector Machine: A new machine learning model for
predicting water quality parameters," Ain Shams Engineering Journal, vol. 15,
no. 3, 2024.
[28] Y . Kim, "Convolutional Neural Networks for Sentence Classification," 2014.
[29] A . T. N. Dat Quoc Nguyen, "PhoBERT: Pre-trained language models for
Vietnamese," in Findings of the Association for Computational Linguistics:
EMNLP 2020, 2020.
[30] E . S. a. D. G. Telmo Pires, "How Multilingual is Multilingual BERT?," in In
Proceedings of the 57th Annual Meeting of the Association for Computational
Linguistics, Florence, 2019.
[31] L . D. J. C. T. W. Victor Sanh, "DistilBERT, a distilled version of BERT:
smaller, faster, cheaper and lighter," 2019.
[32] K . K. N. G. V. C. G. W. F. G. E. G. M. O. L. Z. V. S. Alexis Conneau,
"Unsupervised Cross-lingual Representation Learning at Scale," 2019.
[33] T . P. D.-V. N. a. K. N. Nam Nguyen, "ViSoBERT: A Pre-Trained Language
Model for Vietnamese Social Media Text Processing," in In Proceedings of the
90

2023 Conference on Empirical Methods in Natural Language Processing,
Singapore, 2023.
[34] S . Q. T. P. G. H. K. V. N. N. L.-T. N. Phong Nguyen-Thuan Do, "VLUE: A
New Benchmark and Multi-task Knowledge Transfer Learning for Vietnamese
Natural Language Understanding," in Findings of the Association for
Computational Linguistics: NAACL 2024, Mexico City, 2024.
[35] G . Team, "Gemma 3 Technical Report," 2025.
[36] G . Team, "Gemma: Open Models Based on Gemini Research and Technology,"
2024.
[37] Q . Team, "Qwen3 Technical Report," 2025.
[38] Q . Team, "Qwen2.5 Technical Report," 2024.
91

PHỤ LỤC
92
