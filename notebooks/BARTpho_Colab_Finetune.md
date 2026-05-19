# BARTpho Colab Fine-tuning Notes

Paste `notebooks/bartpho_normalization_colab.py` vào các cells trên Google Colab.

## Colab setup

1. Colab notebook `Fintuning BARTpho.ipynb`, T4 GPU runtime.
2. Up `data/normalization/phase2_full_normalization_content_only.csv` lên thư mục `/content` (cân nhắc up lên drive r mount).
3. Run all các cells.
4. BARTpho-word sử dụng hàm helper built-in `segment_vietnamese_text(text)` từ `py_vncorenlp`, theo gợi ý của tác giả BARTpho.
5. `RUN_VARIANTS = ["syllable"]` : theo âm tiết tiếng Việt (do bản chất đơn âm của các từ tiếng Việt, không như tiếng Anh). -> xử lý ở mức âm tiết.
6. `RUN_VARIANTS = ["word"]`: theo từ đã qua phân đoạn (học_sinh, hôm_nay). -> xử lý ở mức từ tiếng Việt, sau khi đã đc VnCoreNLP phân đoạn từ.

## Configuration

Đường dẫn:

```python
DATA_PATH = "/content/phase2_full_normalization_content_only.csv"
OUTPUT_ROOT = "/content/bartpho-normalization"
VNCORENLP_DIR = "/content/vncorenlp"
```

**Google Drive:**

```python
from google.colab import drive
drive.mount("/content/drive")

DATA_PATH = "/content/drive/MyDrive/path/to/phase2_full_normalization_content_only.csv"
OUTPUT_ROOT = "/content/drive/MyDrive/bartpho-normalization"
```

## Data handling

- Input column: `source_text`.
- Target column: `normalized_text`.
- CSV hiện tại có 6,402 rows (chưa bao gồm các data nhãn 1 có obf_level 0/1/2), không khuyết, không duplicate theo cặp source_text - normalized_text trước khi xử lý sâu hơn.\
- Sau khi qua chuẩn hoá dấu câu (theo lưu ý của tác giả), drop cặp dup nếu có.
- Tỉ lệ chia: 90% train, 5% validation, 5% test.
- Đầu ra `OUTPUT_ROOT` bao gồm:
  - `tone_normalized_full.csv`
  - `train.csv`
  - `validation.csv`
  - `test.csv`

## BARTpho-syllable

- Dùng `vinai/bartpho-syllable`.
- Chỉ áp chuẩn hoá dấu.
- Giữa khoảng trắng phân cách âm tiết trong tiếng Việt.

## BARTpho-word

- Dùng `vinai/bartpho-word`.
- Áp chuẩn hoá dấu trước.
- Sau đó dùng `py_vncorenlp.download_model(save_dir=VNCORENLP_DIR)` và `py_vncorenlp.VnCoreNLP(annotators=["wseg"], save_dir=VNCORENLP_DIR)` để phân đoạn từ tiếng Việt.
- Xoá gạch nối trả về khoảng trắng để output dễ đọc. 

## Suggested runs

Mặc định chạy BARTpho-syllable

```python
RUN_VARIANTS = ["syllable"]
```

Test nhanh:

```python
NUM_EPOCHS = 1
RUN_VARIANTS = ["syllable"]
```

Tăng epoch để học sâu hơn

```python
NUM_EPOCHS = 5
RUN_VARIANTS = ["syllable"]
```

Chạy BARTpho-word

```python
NUM_EPOCHS = 5
RUN_VARIANTS = ["word"]
```


