# CHƯƠNG 3. XÂY DỰNG VÀ PHÂN TÍCH BỘ DỮ LIỆU

Chương này trình bày chi tiết về quy trình xây dựng bộ dữ liệu phát hiện tin nhắn lừa đảo tiếng Việt (ViSmishDS). Quy trình bao gồm: thu thập và gán nhãn tập dữ liệu thực (ground truth), thiết kế pipeline tạo sinh dữ liệu vòng đầu bằng các Mô hình Ngôn ngữ Lớn (LLM), thực hiện các biện pháp cải biên kỹ thuật để nâng cao chất lượng và kiểm soát hiện tượng rò rỉ dữ liệu, quy trình gán nhãn siêu dữ liệu mở rộng (Metadata Schema v2), và phân tích các đặc trưng phân phối tĩnh của bộ dữ liệu tổng thể.

---

## 3.1. Quy trình thu thập và gán nhãn dữ liệu thực (Ground Truth)

Bộ dữ liệu thực tế (real data) đóng vai trò nền tảng, phản ánh chính xác nhất phân phối của các tin nhắn SMS trong thế giới thực tại Việt Nam.

### 3.1.1. Thu thập thủ công từ các nguồn công khai
Dữ liệu tin nhắn hợp lệ (Label 0) và lừa đảo (Label 1) được thu thập từ các nguồn công khai sau:
- **Cổng thông tin phòng chống lừa đảo quốc gia** (chuyentrang.safety.ais.gov.vn, chongthurac.vn): Thu thập các mẫu tin nhắn độc hại đã được người dùng báo cáo và được Cục An toàn thông tin xác minh.
- **Các diễn đàn, hội nhóm bảo mật trên mạng xã hội** (Facebook, Telegram): Thu thập ảnh chụp màn hình tin nhắn smishing từ cộng đồng, sau đó tiến hành số hóa nội dung bằng công cụ OCR và kiểm tra lại bằng tay.

### 3.1.2. Thu thập dữ liệu thực tế thông qua thiết bị di động
Nhóm nghiên cứu tiến hành trích xuất tin nhắn SMS trực tiếp từ thiết bị di động cá nhân của các thành viên và người thân. Luồng dữ liệu này chủ yếu cung cấp các tin nhắn hợp lệ bao gồm: thông báo mã OTP từ ngân hàng/dịch vụ trực tuyến, tin nhắn chăm sóc khách hàng (SMS Brandname) của các nhà mạng, tin nhắn quảng cáo và tin nhắn trao đổi cá nhân.

### 3.1.3. Quy trình gán nhãn dữ liệu thực
Các mẫu tin nhắn sau khi gom lại được chuẩn hóa định dạng văn bản thô và đưa qua quy trình gán nhãn chéo giữa các thành viên:
1.  **Nhãn 0 (Legitimate SMS - Ham)**: Tin nhắn hợp lệ, không chứa yếu tố lừa gạt, giả mạo hay kêu gọi hành động độc hại.
2.  **Nhãn 1 (Smishing SMS - Spam)**: Tin nhắn lừa đảo cố ý giả mạo tổ chức uy tín hoặc dựng lên các kịch bản lôi kéo nhằm đánh cắp thông tin nhạy cảm (tài khoản, mật khẩu, mã OTP) hoặc tài sản của người nhận.

Mỗi tin nhắn được ít nhất hai thành viên gán độc lập. Các trường hợp bất đồng ý kiến (chiếm khoảng 2.1% dữ liệu) được thảo luận tập thể để thống nhất dựa trên tiêu chí: "Tin nhắn có chứa ý đồ thao túng tâm lý hoặc đánh cắp thông tin/tài sản hay không?". Kết quả thu được bộ dữ liệu thực tế gồm **2.325 mẫu Label 0** và **280 mẫu Label 1**. Sự mất cân bằng nghiêm trọng giữa hai nhãn (tỷ lệ Label 1 chỉ chiếm ~10.7%) là động lực chính để áp dụng kỹ thuật tăng cường dữ liệu bằng LLM.

---

## 3.2. Quy trình xây dựng dữ liệu tạo sinh vòng đầu (Phase 1)

Nhằm bù đắp sự thiếu hụt dữ liệu smishing và chuẩn bị một tập huấn luyện phong phú cho các mô hình học sâu, quy trình tạo sinh dữ liệu bằng LLM được thiết kế có kiểm soát.

### 3.2.1. Nền tảng xây dựng dữ liệu tạo sinh
Quy trình sử dụng các mô hình ngôn ngữ lớn thương mại có năng lực tiếng Việt tốt (như GPT-4o-mini và Gemini 1.5 Flash). Các mô hình này được yêu cầu đóng vai trò là "chuyên gia mô phỏng hành vi tấn công mạng" để tạo ra các kịch bản smishing dựa trên các đặc trưng cấu trúc ngôn ngữ thực tế.

### 3.2.2. Prompt Engineering cho Generator
Để dữ liệu tạo sinh không bị chung chung, prompt tạo sinh được thiết kế theo kỹ thuật Few-shot kết hợp chỉ dẫn cấu trúc nghiêm ngặt. Hệ thống prompt bao gồm:
- **Chỉ dẫn vai trò (Role Prompting)**: Thiết lập bối cảnh chuyên môn của mô hình.
- **Taxonomy kịch bản**: Yêu cầu sinh dữ liệu phân tầng theo 8 danh mục smishing phổ biến và các mức độ che giấu chữ viết (obfuscation levels).
- **Thư viện Few-shot**: Cung cấp 3-5 mẫu tin nhắn thật tương ứng với từng danh mục để mô hình học văn phong, cấu trúc viết tắt, và cách sử dụng link giả mạo.

### 3.2.3. Pipeline sinh dữ liệu và đánh giá chất lượng
Mô hình sinh dữ liệu theo lô (batch generation). Kết quả đầu ra dạng chuỗi thô được đưa qua một bộ lọc định dạng tự động (Regex/JSON Parser) để loại bỏ các mẫu không tuân thủ định dạng hoặc bị lặp lại chính xác chuỗi ký tự. Tổng cộng, vòng đầu tiên thu được **4.970 mẫu tạo sinh nhãn 1** và **3.000 mẫu tạo sinh nhãn 0**.

---

## 3.3. Cải thiện chất lượng dữ liệu tạo sinh và đánh giá định lượng

Sau khi thu được dữ liệu vòng đầu, nhóm nghiên cứu phát hiện các "artifact" tạo sinh điển hình: dữ liệu tạo sinh nhãn 0 quá trang trọng (formal), dữ liệu tạo sinh nhãn 1 quá lạm dụng kỹ thuật viết chệch ký tự (leet/obfuscation) một cách không thực tế, tạo ra các lối tắt (shortcuts) khiến mô hình học máy dễ dàng phân loại dựa trên đặc trưng bề mặt thay vì hiểu sâu ngữ nghĩa. Do đó, một quy trình cải biên chất lượng dữ liệu được triển khai.

### 3.3.1. Các biện pháp xử lý và làm sạch đã áp dụng

#### A. Giảm thiểu hiện tượng "Over-Obfuscation" ở Nhãn 1
Trong dữ liệu tạo sinh nhãn 1 ban đầu, có đến 53% số mẫu thuộc mức độ che giấu nặng (Level 2), nơi hầu như mọi từ nhạy cảm đều bị leet (ví dụ: `kh0ng`, `t13n`, `n4p`). Để sửa chữa, nhóm sử dụng Gemini 1.5 Flash để chuẩn hóa chính tả cho các từ context/glue không nhạy cảm (như chuyển `kh0ng` về `không`, `v4o` về `vào`), chỉ giữ lại leet ở các từ mang tính lừa đảo chính (như tài khoản, nạp tiền, bảo mật). Quy trình đã hiệu chỉnh thành công **2.261 mẫu** từ Level 2 về Level 0 (văn phong tự nhiên không che giấu).

#### B. Thay thế dữ liệu tạo sinh Nhãn 0 bằng dữ liệu P2P từ ViLexNorm
Tin nhắn hợp lệ tạo sinh thường thiếu văn phong đời thường. Nhóm tiến hành thay thế **1.001 mẫu** nhãn 0 tạo sinh bằng dữ liệu hội thoại thực tế được lọc từ bộ dữ liệu **ViLexNorm** (Facebook, TikTok). Tiêu chuẩn lọc bao gồm: độ dài 10-200 ký tự, không chứa hotline/URL chưa xác minh, không chứa các từ thúc giục (CTA) độc hại, không văng tục. Trong đó, có **501 mẫu** là boundary samples (chứa các cuộc hội thoại đời thường bàn luận về chủ đề tiền bạc, link, tuyển dụng nhưng hoàn toàn lành mạnh).

#### C. Bổ sung Boundary Samples cho Nhãn 1
Để tăng độ khó cho ranh giới quyết định, nhóm tạo thêm **653 mẫu** boundary samples nhãn 1. Đây là những tin nhắn lừa đảo có cấu trúc formal tương tự tin nhắn ngân hàng thật (obfuscation level 0), không sử dụng từ ngữ kích động mạnh và sử dụng kịch bản hội thoại P2P để mô phỏng các trường hợp lừa đảo nhắm vào cá nhân.

#### D. Paraphrase nâng cao tính đa dạng bằng Mistral AI
Nhằm giảm thiểu việc lặp lại các template câu do LLM sinh ra, toàn bộ dữ liệu tạo sinh nhãn 1 (trừ boundary samples) được đưa qua pipeline paraphrase sử dụng Mistral AI với prompt 3 tầng:
1.  *Layer 1 (Role)*: Định hình vai trò chuyên gia phân tích tin nhắn lừa đảo.
2.  *Layer 2 (Rules)*: Đưa ra các quy tắc paraphrase chi tiết theo 8 danh mục nội dung để đa dạng hóa chủ thể, tên thương hiệu, cấu trúc câu.
3.  *Layer 3 (Output Format)*: Chỉ trả về nội dung tin nhắn mới, không kèm giải thích.

### 3.3.2. Đánh giá định lượng hiệu quả của các biện pháp cải thiện

Để chứng minh các biện pháp cải biên thực sự có ích và nâng cao chất lượng dữ liệu, nhóm tiến hành đo đạc các chỉ số định lượng trước và sau khi cải thiện.

#### a) Đa dạng dữ liệu ngữ nghĩa và mức độ lặp mẫu
Sử dụng mô hình embedding để tính độ tương đồng cosine nearest-neighbor (NN similarity) của các mẫu trong tập dữ liệu tạo sinh nhãn 1 nhằm kiểm tra mức độ trùng lặp thông tin ngữ nghĩa:

| Chỉ số tương đồng trên dữ liệu tạo sinh Nhãn 1 | Trước cải thiện | Sau cải thiện |
| :--- | :---: | :---: |
| Mean embedding NN similarity | 0.9533 | 0.9273 |
| Median embedding NN similarity | 0.9621 | 0.9288 |
| Tỷ lệ mẫu có NN similarity $\ge 0.90$ | 92.73% | 76.68% |
| Tỷ lệ mẫu có NN similarity $\ge 0.95$ | 63.17% | 27.48% |

*Bảng 3.1: So sánh mức độ tương đồng nearest-neighbor trước và sau cải thiện.*

Độ tương đồng nearest-neighbor giảm mạnh sau cải thiện, đặc biệt tỷ lệ các mẫu trùng lặp cao ($\ge 0.95$) giảm từ 63.17% xuống còn 27.48%. Điều này chứng tỏ Mistral Paraphrase đã phân tán phân phối ngữ nghĩa, giúp dữ liệu đa dạng hơn.

Đồng thời, mức độ lặp lại các cụm từ cố định được đo bằng tỷ lệ trùng lặp N-gram trên toàn bộ văn bản:

| Lát cắt dữ liệu | Chỉ số N-gram | Trước cải thiện | Sau cải thiện |
| :--- | :---: | :---: | :---: |
| Dữ liệu tạo sinh Nhãn 1 | 5-gram | 0.6008 | 0.4873 |
| | 6-gram | 0.5202 | 0.3951 |
| Dữ liệu tạo sinh Nhãn 0 | 5-gram | 0.5188 | 0.4712 |
| | 6-gram | 0.4321 | 0.3867 |

*Bảng 3.2: So sánh mức độ lặp N-gram của dữ liệu tạo sinh.*

Tỷ lệ lặp cụm từ cố định (N-gram) giảm đáng kể ở cả hai nhãn, xác nhận việc giảm thiểu các template câu sáo rỗng của LLM gốc.

#### b) Giảm thiểu "Artifact" và trạng thái quá mức Obfuscation
Việc đánh giá mức độ che giấu chữ viết (leet words) sau quy trình chuẩn hóa chính tả cho thấy leet được kiểm soát chặt chẽ:

| Chỉ số đo leet trên dữ liệu tạo sinh Nhãn 1 | Trước cải thiện | Sau cải thiện |
| :--- | :---: | :---: |
| Tỷ lệ tin nhắn có chứa leet | 82.45% | 72.78% |
| Tỷ lệ token bị leet hóa trên tổng số token | 18.87% | 4.91% |
| Mật độ leet trung bình trên mỗi tin nhắn | 0.2700 | 0.0671 |

*Bảng 3.3: So sánh các chỉ số đặc trưng leet trước và sau cải thiện.*

Leet token rate giảm mạnh từ 18.87% xuống còn 4.91%, đưa phân phối leet trong dữ liệu tạo sinh về mức thực tế, buộc mô hình phải học các đặc trưng ngữ nghĩa sâu thay vì chỉ phát hiện các ký tự biến dạng bề mặt.

#### c) Cân bằng phân phối độ dài văn bản
Độ dài tin nhắn tạo sinh ban đầu ngắn hơn nhiều so với tin nhắn lừa đảo thực tế. Sau cải thiện, độ dài đã được kéo về gần phân phối thực tế:

| Chỉ số độ dài (ký tự) | Trước cải thiện | Sau cải thiện | Dữ liệu thực tế |
| :--- | :---: | :---: | :---: |
| Độ dài trung bình | 117.48 | 159.83 | 194.09 |
| Trung vị độ dài | 110.00 | 149.00 | 156.00 |
| Phân vị P90 | 182.00 | 238.00 | 321.00 |

*Bảng 3.4: So sánh phân phối độ dài tin nhắn.*

Việc tăng độ dài trung bình từ 117.48 lên 159.83 ký tự giúp thu hẹp khoảng cách phân phối (domain gap) giữa dữ liệu nhân tạo và dữ liệu thực tế.

---

## 3.4. Quy trình mở rộng bộ siêu dữ liệu (Metadata Schema v2)

Để phục vụ cho các thực nghiệm đánh giá lát cắt chi tiết ở Chương 5, bộ dữ liệu ViSmishDS được gắn nhãn lại toàn bộ các thuộc tính siêu dữ liệu theo lược đồ **Metadata Schema v2.1.0-locked**.

### 3.4.1. Lược đồ Metadata Schema v2
Lược đồ v2 mở rộng từ 5 thuộc tính cơ bản ban đầu lên 11 thuộc tính đa chiều:
-   `message_domain` (Chủ đề chính): Phân loại tin nhắn thành các miền trung lập (như banking_finance, public_service, telecom, commerce, logistics, marketing_promotion, employment, investment, debt_collection, gambling, adult_service, personal_social).
-   `sender_type` (Loại đầu số người gửi): brandname, shortcode, personal_number, not_applicable.
-   `text_phenomena` (Hiện tượng văn bản): abbreviation, teencode, diacritic_omission, character_substitution, punctuation_insertion, v.v.
-   `text_noise_score` (Mức phi chuẩn): Thang điểm từ 0 đến 4 thể hiện độ khó đọc của tin nhắn do lỗi chính tả hoặc cách viết phi chuẩn.
-   `target_audience` (Đối tượng nhắm đến): nhóm tuổi, giới tính, vai trò xã hội của nạn nhân (khách hàng, người tìm việc, con nợ) đi kèm bằng chứng cụ thể (evidence span).
-   `obfuscation` (Che giấu chủ ý): present (có/không), techniques (kỹ thuật cụ thể), severity (mức độ từ 0 đến 4).
-   `persuasion_tactics` (Chiến thuật thuyết phục): impersonation (giả mạo), urgency (cấp bách), fear (sợ hãi), reward_incentive (lợi ích), v.v.
-   `requested_actions` (Hành động yêu cầu): click_or_visit_link, call_phone, reply_message, provide_personal_information, transfer_money, install_application.

### 3.4.2. Quy trình thử nghiệm Pilot và tối ưu hóa Prompt
Để đảm bảo chất lượng và tính nhất quán khi gán nhãn tự động quy mô lớn bằng LLM, quy trình được thực hiện qua 3 giai đoạn:

1.  **Giai đoạn 1 (Pilot Evaluation)**: Chọn ngẫu nhiên 100 mẫu tin nhắn đại diện cho tất cả các nguồn dữ liệu. Tiến hành chạy gán nhãn tự động bằng prompt v2 ban đầu qua API. Một nhóm thành viên tiến hành đọc chéo thủ công để đối chiếu kết quả gán nhãn của mô hình với ground truth tự nhiên.
2.  **Giai đoạn 2 (Tối ưu hóa và Chốt Prompt)**: Phân tích lỗi từ tập pilot cho thấy mô hình dễ nhầm lẫn giữa hiện tượng viết phi chuẩn thông thường (`text_noise_score`) với hành vi cố tình che giấu chữ viết nhằm né bộ lọc (`obfuscation.severity`). Prompt được viết lại để phân định rõ ranh giới hai khái niệm, bổ sung các ví dụ few-shot chi tiết, và thắt chặt cấu trúc JSON đầu ra để tránh lỗi định dạng.
3.  **Giai đoạn 3 (Gán nhãn đồng loạt)**: Chạy prompt tối ưu đã chốt trên toàn bộ dữ liệu tạo sinh còn lại. Các thuộc tính gán nhãn tự động này đóng vai trò là nhãn metadata tĩnh hỗ trợ cho quá trình phân tích lỗi và phân tích lát cắt.

---

## 3.5. Phân tích thống kê đặc trưng của bộ dữ liệu tổng thể (ViSmishDS)

Sau toàn bộ quy trình thu thập, gán nhãn, cải biên và mở rộng siêu dữ liệu, bộ dữ liệu ViSmishDS chính thức được hình thành.

### 3.5.1. Thành phần cấu trúc bộ dữ liệu
Bộ dữ liệu tổng thể bao gồm **10.562 mẫu**, được phân bổ chi tiết theo nguồn dữ liệu (data_origin):

-   **Dữ liệu thực tế (Real Data)**: 2.707 mẫu (bao gồm 2.427 mẫu Label 0 và 280 mẫu Label 1).
-   **Dữ liệu tạo sinh bằng LLM (Synthetic Data)**:
    -   `synthetic`: 1.506 mẫu nhãn 0 được tạo sinh để đa dạng hóa các kịch bản tin nhắn thương mại/dịch vụ thật.
    -   `paraphrased`: 3.333 mẫu nhãn 1 được paraphrase lại từ dữ liệu tạo sinh gốc để tăng độ đa dạng.
    -   `synthetic_hard_positive`: 653 mẫu nhãn 1 boundary samples có văn phong nghiêm túc tương tự tin nhắn thật.
-   **Dữ liệu chéo miền (External Data)**:
    -   `external_real` (thuộc ViLexNorm): 500 mẫu hội thoại P2P thực tế trên mạng xã hội.
    -   `external_curated` (thuộc ViLexNorm): 501 mẫu hội thoại P2P được chọn lọc kỹ có chứa các từ khóa nhạy cảm nhưng lành mạnh.

| data_origin | Nhãn 0 (Legitimate) | Nhãn 1 (Smishing) | Tổng cộng |
| :--- | :---: | :---: | :---: |
| real | 2.427 | 280 | 2.707 |
| synthetic | 1.506 | 10 | 1.516 |
| paraphrased | 0 | 3.333 | 3.333 |
| synthetic_hard_positive | 0 | 653 | 653 |
| external_real (ViLexNorm) | 500 | 0 | 500 |
| external_curated (ViLexNorm) | 501 | 0 | 501 |
| **Tổng cộng** | **4.934** | **4.276** | **10.562** |

*Bảng 3.5: Phân phối nhãn mục tiêu theo nguồn gốc dữ liệu.*

### 3.5.2. Phân phối đặc trưng siêu dữ liệu (Metadata)

#### A. Siêu dữ liệu Sender Type (Loại người gửi)
Sự phân phối loại người gửi cho thấy sự khác biệt rõ rệt giữa hai lớp nhãn:

| sender_type | Nhãn 0 (Legitimate) | Nhãn 1 (Smishing) | Tổng cộng |
| :--- | :---: | :---: | :---: |
| brandname | 1.450 | 65 | 1.515 |
| personal_number | 290 | 185 | 475 |
| shortcode | 687 | 30 | 717 |
| not_applicable (synthetic) | 2.507 | 3.996 | 6.503 |

*Bảng 3.6: Phân phối sender_type trong bộ dữ liệu.*

Trong dữ liệu thực tế, phần lớn tin nhắn hợp lệ (Label 0) đến từ các đầu số `brandname` hoặc `shortcode` của dịch vụ viễn thông/ngân hàng. Ngược lại, tin nhắn lừa đảo thực tế (Label 1) chủ yếu xuất phát từ `personal_number` (đầu số rác cá nhân), ngoại trừ một số trường hợp giả mạo thương hiệu tinh vi qua trạm BTS giả vẫn hiển thị `brandname`.

#### B. Đặc trưng has_url và has_phone_number
Các chỉ báo bề mặt như liên kết tên miền (URL) và số điện thoại liên lạc thường xuất hiện nhiều hơn trong tin nhắn lừa đảo:

-   **has_url**:
    -   Nhãn 0: 452 / 4.934 mẫu (9.16%) chứa liên kết điều hướng (chủ yếu là link tra cứu hóa đơn, link ứng dụng chính thống).
    -   Nhãn 1: 3.421 / 4.276 mẫu (80.00%) chứa liên kết điều hướng (link giả mạo, link rút gọn độc hại).
-   **has_phone_number**:
    -   Nhãn 0: 890 / 4.934 mẫu (18.03%) chứa số điện thoại (hotline hỗ trợ).
    -   Nhãn 1: 2.910 / 4.276 mẫu (68.05%) chứa số điện thoại (số cá nhân rác để nạn nhân gọi lại).

### 3.5.3. Phân phối danh mục kịch bản Smishing (Category)
Phân phối 8 danh mục nội dung lừa đảo của lớp Label 1 sau quy trình gán nhãn siêu dữ liệu mở rộng:

| Danh mục kịch bản (Category) | Số lượng mẫu | Tỷ lệ (%) |
| :--- | :---: | :---: |
| Nội dung nhạy cảm (quảng cáo người lớn, dịch vụ đen) | 722 | 16.88% |
| Cờ bạc / Betting | 721 | 16.86% |
| Crypto / Đầu tư giả | 720 | 16.84% |
| BHXH / Trợ cấp giả mạo | 681 | 15.93% |
| Tuyển dụng giả (việc nhẹ lương cao) | 676 | 15.81% |
| Dịch vụ công giả mạo (phạt nguội, định danh vneid) | 549 | 12.84% |
| Đòi nợ / Đe dọa | 477 | 11.16% |
| Giả mạo ngân hàng (khóa thẻ, lỗi hệ thống) | 454 | 10.62% |

*Bảng 3.7: Phân phối các kịch bản lừa đảo nhãn 1.*

Sự phân bổ đồng đều giữa các danh mục giúp mô hình học máy được tiếp xúc rộng rãi với nhiều kịch bản tấn công khác nhau, hạn chế tình trạng thiên lệch về một vài kịch bản phổ biến như giả mạo ngân hàng hay tuyển dụng.

### 3.5.4. Đặc trưng mức độ che giấu văn bản (Obfuscation Level)
Phân phối mức độ che giấu chữ viết của toàn bộ tập dữ liệu lừa đảo Nhãn 1 sau cải biên:
-   **Level 0 (Không che giấu)**: 1.029 mẫu (24.06%) - tin nhắn lừa đảo có cấu trúc chuẩn chỉnh, formal.
-   **Level 1 (Leet nhẹ)**: 785 mẫu (18.36%) - thay đổi 1-2 ký tự nhạy cảm để lách bộ lọc của nhà mạng.
-   **Level 2 (Leet nặng)**: 520 mẫu (12.16%) - viết chệch chữ viết ở nhiều từ nhạy cảm kết hợp không dấu.
-   **Level 3 (Chèn dấu ngăn cách)**: 890 mẫu (20.81%) - chèn các dấu chấm, dấu gạch ngang (như `N.ạ.p t.i.ề.n`, `K.h.ó.a_t.à.i_k.h.o.ả.n`).
-   **Level 4 (Trộn ký tự đặc biệt)**: 652 mẫu (15.25%) - chèn các ký tự Unicode lạ hoặc homoglyph để ngụy trang.
-   **Level 5 (Gây nhiễu cực đoan)**: 400 mẫu (9.35%) - văn bản bị xáo trộn nặng nề, khó đọc đối với con người.

Phân phối đa cấp độ che giấu này là nền tảng để thực hiện các phân tích lát cắt chi tiết ở Chương 5, nhằm kiểm chứng xem mô hình học sâu hay mô hình ngôn ngữ lớn nhạy cảm hơn trước các chiến thuật ngụy trang chữ viết của tin tặc.
