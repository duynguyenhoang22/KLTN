# Quy ước dữ liệu

- `sources/`: dữ liệu nhập bất biến. Không sửa nội dung tại đây.
- `reference/phase1/`: snapshot cũ duy nhất dùng để migration và truy vết.
- `annotations/`: batch và kết quả annotation đang làm; bị Git ignore.
- `processed/`: output trung gian tái tạo được; bị Git ignore.
- `releases/`: dataset đã đóng băng theo phiên bản; chỉ đưa vào Git/LFS sau khi
  có quyết định phát hành rõ ràng.

Không đặt script, notebook, báo cáo hoặc model trong `data/`.

Mọi bản release phải có:

- phiên bản schema và guideline;
- checksum nguồn;
- số lượng mẫu theo `label × data_origin`;
- tỷ lệ unknown và confidence thấp;
- kết quả inter-annotator agreement;
- changelog từ phiên bản trước.
