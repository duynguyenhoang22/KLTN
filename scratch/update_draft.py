from pathlib import Path

def main():
    draft_path = Path("thesis/drafts/CHAPTER_5_DRAFT.md")
    if not draft_path.exists():
        print(f"Error: {draft_path} does not exist!")
        return

    content = draft_path.read_text(encoding="utf-8")

    # Replacement 1: Length table
    target_1 = """> **GHI CHÚ BẢNG 5.x — Hiệu năng theo độ dài trên dev**
>
> Nên trình bày ba nhóm đủ số mẫu Label 1: 81–160, 161–240 và trên 240 ký tự. Mỗi hàng ghi `n`, F1 Label 1, Recall Label 1, FP và FN. Nhóm ≤80 chỉ ghi phân phối 138 Label 0 và 2 Label 1, không dùng để so sánh mô hình.
>
> Nguồn dữ liệu: [rq2_slice_metrics_dev.csv](C:\\KLTN\\KLTN\\scripts\\RQ2_RQ3\\rq2_slice_metrics_dev.csv)."""

    rep_1 = """Bảng 5.x trình bày hiệu năng chi tiết của các mô hình theo nhóm độ dài tin nhắn trên tập dev.

**Bảng 5.x: Hiệu năng phân loại theo nhóm độ dài tin nhắn trên tập dev**

| Nhóm độ dài (ký tự) | Số mẫu (n) | Nhãn 1 (n1) | Mô hình | F1 Label 1 | Recall Label 1 | FP | FN |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **81–160** | 146 | 17 | CafeBERT | 0,9091 | 0,8824 | 1 | 2 |
| | | | DistilBERT multilingual | 0,9444 | 1,0000 | 2 | 0 |
| | | | TextCNN | 0,8387 | 0,7647 | 1 | 4 |
| | | | TextCNN distilled | 0,8125 | 0,7647 | 2 | 4 |
| **161–240** | 82 | 8 | CafeBERT | 0,9333 | 0,8750 | 0 | 1 |
| | | | DistilBERT multilingual | 0,8889 | 1,0000 | 2 | 0 |
| | | | TextCNN | 0,8571 | 0,7500 | 0 | 2 |
| | | | TextCNN distilled | 0,9333 | 0,8750 | 0 | 1 |
| **>240** | 167 | 10 | CafeBERT | 0,8421 | 0,8000 | 1 | 2 |
| | | | DistilBERT multilingual | 0,7619 | 0,8000 | 3 | 2 |
| | | | TextCNN | 0,8571 | 0,9000 | 2 | 1 |
| | | | TextCNN distilled | 0,8182 | 0,9000 | 3 | 1 |

*Ghi chú: Nhóm tin nhắn ngắn \\(\\le 80\\) ký tự chỉ chứa 2 mẫu Label 1 và 138 mẫu Label 0 nên không được đưa vào bảng so sánh trực tiếp để tránh thiên lệch thống kê.*"""

    # Replacement 2: Slices summary table
    target_2 = """> **GHI CHÚ BẢNG 5.x — Tóm tắt các lát cắt có ý nghĩa**
>
> Có thể dùng một bảng ngắn thay vì trình bày toàn bộ CSV:
>
> | Lát cắt | Phát hiện chính |
> |---|---|
> | Độ dài >240 | CafeBERT và DistilBERT suy giảm F1 L1; TextCNN ổn định hơn |
> | Có/không URL | Smishing không có URL khó hơn rõ đối với TextCNN |
> | Sender type | `personal_number` là nhóm khó hơn đối với hai TextCNN |
> | Data origin | FP trên external thấp; lỗi chủ yếu nằm ở dữ liệu real |"""

    rep_2 = """**Bảng 5.x: Tóm tắt hiệu năng các mô hình trên một số lát cắt dữ liệu tiêu biểu**

| Lát cắt | Phân phối mẫu (n0/n1) | Phát hiện chính |
| :--- | :---: | :--- |
| **Có URL** | 168 / 29 | Tín hiệu mạnh hỗ trợ phát hiện smishing. Recall đạt mức rất cao (DistilBERT: 100%, TextCNN distilled: 89,66%, CafeBERT & TextCNN: 86,21%). Kiểm soát FP cực tốt (CafeBERT: 0, TextCNN: 1). |
| **Không URL** | 330 / 8 | Là nhóm khó đối với mô hình ký tự. Recall của TextCNN & TextCNN distilled giảm mạnh còn 62,5%, DistilBERT giảm còn 75%, riêng CafeBERT duy trì ổn định ở 87,5%. |
| **Brandname** | 260 / 14 | Recall đạt mức cao (DistilBERT: 100%, TextCNN distilled: 92,86%, CafeBERT & TextCNN: 85,71%). |
| **Personal Number** | 16 / 23 | Là nhóm khó đối với mô hình ký tự (TextCNN & TextCNN distilled: Recall chỉ đạt 78,26%). CafeBERT và DistilBERT xử lý tốt hơn với Recall lần lượt là 86,96% và 91,30%. |
| **Nguồn dữ liệu** | 348 / 37 (Real)<br>150 / 0 (External) | Lỗi chủ yếu tập trung ở dữ liệu Real. Các mô hình kiểm soát FP trên dữ liệu hội thoại đời thường và bài viết mạng xã hội (tập External) cực tốt (tổng cộng chỉ có 1 FP với DistilBERT, và 2 FP với mỗi mô hình TextCNN). |"""

    # Replacement 3: Error overview table
    target_3 = """> **GHI CHÚ BẢNG 5.x — Tổng quan lỗi trên dev**
>
> | Mô hình | FP | FN | Tổng lỗi | Lỗi confidence ≥0,9 |
> |---|---:|---:|---:|---:|
> | CafeBERT | 2 | 5 | 7 | 5 |
> | DistilBERT multilingual | 7 | 2 | 9 | 8 |
> | TextCNN | 4 | 7 | 11 | 7 |
> | TextCNN distilled | 6 | 6 | 12 | 5 |
>
> Nguồn: [rq3_error_overview_dev.csv](C:\\KLTN\\KLTN\\scripts\\RQ2_RQ3\\rq3_error_overview_dev.csv)."""

    rep_3 = """**Bảng 5.x: Thống kê số lượng lỗi phân loại trên tập dev**

| Mô hình | False Positive (FP) | False Negative (FN) | Tổng số lỗi | Lỗi có độ tin cậy \\(\\ge 0,9\\) |
| :--- | :---: | :---: | :---: | :---: |
| **CafeBERT** | 2 | 5 | 7 | 5 |
| **DistilBERT multilingual** | 7 | 2 | 9 | 8 |
| **TextCNN** | 4 | 7 | 11 | 7 |
| **TextCNN distilled** | 6 | 6 | 12 | 5 |"""

    # Replacement 4: Representative errors table
    target_4 = """> **GHI CHÚ BẢNG 5.x — Ví dụ lỗi tiêu biểu**
>
> Chọn khoảng 4–6 mẫu từ [rq3_representative_errors_dev.csv](C:\\KLTN\\KLTN\\scripts\\RQ2_RQ3\\rq3_representative_errors_dev.csv), gồm:
>
> - Một FN mà cả bốn mô hình cùng mắc.
> - Một FN dạng cảnh báo ngân hàng/OTP giống tin hợp lệ.
> - Một FP tuyển sinh hoặc hội thảo có URL.
> - Một FP external có ngôn ngữ đời thường hoặc phi chuẩn.
>
> Nội dung nên được rút gọn và ẩn thông tin cá nhân nếu cần; ghi thêm số mô hình mắc lỗi và confidence."""

    rep_4 = """**Bảng 5.x: Danh sách các lỗi tiêu biểu của mô hình trên tập dev**

| ID | Nhãn thực | Dự đoán (Độ tin cậy) | Lĩnh vực (Domain) | Nội dung tin nhắn (Rút gọn) | Đặc điểm và Nguyên nhân lỗi |
| :--- | :---: | :--- | :---: | :--- | :--- |
| **ViSmish_07960** | 1 | **Tất cả**: 0 (\\(>0,96\\)) | Động đòi nợ | Nhan thay co hanh vi LOI DUNG TIN NHIEM, CHIEM DOAT TAI SAN. yc tt gap truoc 13g 16/2/2025... LH 0867256447 de giai quyet. | Tin nhắn Smishing đòi nợ dùng ngôn ngữ hành chính/pháp lý tự nhiên, không chứa liên kết URL, khiến toàn bộ các mô hình nhầm với tin nhắn hợp lệ. |
| **ViSmish_04995** | 1 | **CafeBERT**: 0 (0,9994)<br>**DistilBERT**: 1 (0,9956)<br>**TextCNN**: 0 (0,9991)<br>**TextCNN distilled**: 0 (0,9778) | Tài chính | ACB CANH BAO SMS LUA DAO: Hien co thu doan SMS GIA MAO dau so ACB moi KH dang nhap link gia, cung cap USER, MAT KHAU, OTP... | Tin nhắn cảnh báo lừa đảo chứa các từ khóa nhạy cảm và URL giả mạo. Chỉ DistilBERT bắt được, các mô hình khác nhầm với tin nhắn cảnh báo bảo mật hợp lệ. |
| **ViSmish_07545** | 0 | **CafeBERT**: 0 (0,7409)<br>**DistilBERT**: 1 (0,9995)<br>**TextCNN**: 1 (0,9536)<br>**TextCNN distilled**: 1 (0,9348) | Tuyển dụng | [ĐẠI HỌC NGOẠI THƯƠNG] CHÚC MỪNG EM ĐÃ ĐỦ ĐIỀU KIỆN TRÚNG TUYỂN... Để lại email để nhận hướng dẫn... SĐT/ZALO: 0906... | Tin nhắn tuyển sinh hợp lệ chứa cấu trúc thông báo trúng tuyển kèm đường dẫn đăng ký và thông tin liên hệ, khiến DistilBERT và TextCNN bị đánh lừa. |
| **ViSmish_08060** | 0 | **CafeBERT**: 0 (0,9998)<br>**DistilBERT**: 0 (0,9992)<br>**TextCNN**: 1 (0,8945)<br>**TextCNN distilled**: 1 (0,7560) | Cá nhân | t cx muốn nuôi capybara!!!!! | Tin nhắn hội thoại cá nhân phi chuẩn (teencode, dấu chấm than kéo dài) bị các mô hình ký tự (TextCNN) cảnh báo sai do nhạy cảm quá mức với ký tự phi chuẩn ngoài ngữ cảnh. |"""

    replacements = [
        (target_1, rep_1, "Length table"),
        (target_2, rep_2, "Slices summary table"),
        (target_3, rep_3, "Error overview table"),
        (target_4, rep_4, "Representative errors table")
    ]

    updated = content
    for target, replacement, name in replacements:
        # Normalize line endings to avoid matching issues
        target_norm = target.replace("\r\n", "\n")
        updated_norm = updated.replace("\r\n", "\n")
        
        if target_norm in updated_norm:
            updated = updated_norm.replace(target_norm, replacement)
            print(f"Successfully replaced {name} placeholder.")
        else:
            # Let's try flexible whitespace matching if literal matching fails
            print(f"Warning: Literal match failed for {name}. Checking why...")
            # We can print parts of draft to inspect
            # For debugging, print target start
            start_snippet = target_norm[:50]
            print(f"Target start snippet: '{start_snippet}'")
            if start_snippet in updated_norm:
                print("Start snippet found, but whole block has difference.")
            else:
                print("Start snippet NOT found in draft.")
            return

    draft_path.write_text(updated, encoding="utf-8")
    print("Draft updated successfully!")

if __name__ == "__main__":
    main()
