import pandas as pd
import requests
import json
import time
import emoji
import os
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

# ==================== CONFIG ====================
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY") or ""
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"      # hoặc "mistral-medium-latest" / "mistral-large-latest"

INPUT_FILE = "model\\base\\merged_dataset_label1_synthetic.csv"
OUTPUT_FILE = f"paraphrased_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
CHECKPOINT_FILE = "checkpoint.json"     

# Số lần paraphrase mỗi sample (tạo N bản biến thể)
NUM_PARAPHRASES_PER_SAMPLE = 1

# Rate limiting
REQUESTS_PER_MINUTE = 60   # tuỳ theo plan Mistral của bạn
DELAY_BETWEEN_REQUESTS = 60 / REQUESTS_PER_MINUTE  # seconds

# Xử lý lỗi
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ==================== PROMPT TEMPLATES ====================
# Mỗi category có prompt riêng để paraphrase đúng văn phong
CATEGORY_PROMPTS = {
    "Giả mạo ngân hàng": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn giả mạo ngân hàng sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa lừa đảo (tài khoản bị khóa/dừng, cần đăng nhập link giả)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: từ ngữ, cấu trúc câu, tên ngân hàng (nếu cần), format tin nhắn.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "Crypto / Đầu tư giả": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn lừa đảo đầu tư/crypto sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa lừa đảo (kiếm tiền dễ, cơ hội đầu tư ảo)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: từ ngữ, số tiền hứa hẹn, tên sàn/app, cách tiếp cận.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "Tuyển dụng giả": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn tuyển dụng giả sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa lừa đảo (việc nhẹ lương cao, làm tại nhà)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: tên công ty, mức lương, công việc mô tả, cách liên hệ.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "BHXH / Trợ cấp": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn giả mạo BHXH/trợ cấp sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa lừa đảo (nhận tiền hỗ trợ giả, quyết định giả)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: số quyết định, số tiền, link, cách diễn đạt.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "Dịch vụ công giả": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn giả mạo dịch vụ công (VNeID, CSGT...) sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa lừa đảo (tài khoản bị khóa, cần xác thực)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: tên dịch vụ, link, cách diễn đạt, mức độ khẩn cấp.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "Cờ bạc / Betting": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn quảng cáo cờ bạc/betting sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa spam (mời cá độ, đánh bạc online)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: tên nhà cái, tỉ lệ thưởng, cách liên hệ, slogan.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "Đòi nợ / Đe dọa": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn đòi nợ/đe dọa sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa đe dọa/gây áp lực
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: từ ngữ đe dọa, số tiền, thời hạn, cách liên hệ.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",

    "Nội dung nhạy cảm": """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn có nội dung nhạy cảm/dụ dỗ sau theo cách KHÁC, giữ nguyên:
- Ý nghĩa spam (tìm bạn bè, dịch vụ nhạy cảm)
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: cách mời gọi, địa điểm, cách liên hệ.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích.""",
}

DEFAULT_PROMPT = """Bạn là chuyên gia phân tích tin nhắn lừa đảo.
Hãy viết lại tin nhắn spam/lừa đảo sau theo cách KHÁC nhưng vẫn là spam, giữ nguyên:
- Ý nghĩa lừa đảo gốc
- Label spam (label=1)
- Ngôn ngữ tiếng Việt
Thay đổi: từ ngữ, cấu trúc câu, cách diễn đạt.
Chỉ trả về tin nhắn đã viết lại, KHÔNG giải thích."""


# ==================== CHECKPOINT ====================
def load_checkpoint():
    """Đọc tiến độ đã xử lý (để resume)"""
    if Path(CHECKPOINT_FILE).exists():
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"processed_ids": [], "results": []}


def save_checkpoint(checkpoint):
    """Lưu tiến độ"""
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


# ==================== MISTRAL API CALL ====================
def call_mistral_api(prompt: str, content: str, retry: int = 0) -> str | None:
    """
    Gọi Mistral API để paraphrase 1 tin nhắn
    Returns: chuỗi tin nhắn đã paraphrase, hoặc None nếu lỗi
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Tin nhắn gốc:\n{content}"}
        ],
        "temperature": 0.8,      # cao hơn = đa dạng hơn
        "max_tokens": 300,
        "top_p": 0.95,
    }

    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=payload, timeout=30)

        # Rate limit
        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 60))
            logger.warning(f"Rate limited. Đợi {wait}s...")
            time.sleep(wait)
            return call_mistral_api(prompt, content, retry)

        # Lỗi server
        if response.status_code >= 500:
            if retry < MAX_RETRIES:
                logger.warning(f"Server error {response.status_code}. Retry {retry+1}/{MAX_RETRIES}...")
                time.sleep(RETRY_DELAY * (retry + 1))
                return call_mistral_api(prompt, content, retry + 1)
            return None

        response.raise_for_status()
        data = response.json()
        result = data["choices"][0]["message"]["content"].strip()
        return emoji.replace_emoji(result, replace="")

    except requests.exceptions.Timeout:
        if retry < MAX_RETRIES:
            logger.warning(f"Timeout. Retry {retry+1}/{MAX_RETRIES}...")
            time.sleep(RETRY_DELAY)
            return call_mistral_api(prompt, content, retry + 1)
        return None

    except Exception as e:
        logger.error(f"API error: {e}")
        return None


# ==================== MAIN PIPELINE ====================
def run_pipeline(
    input_file: str = INPUT_FILE,
    output_file: str = OUTPUT_FILE,
    num_paraphrases: int = NUM_PARAPHRASES_PER_SAMPLE,
    sample_limit: int = None,   # None = xử lý toàn bộ; hoặc số lượng để test
    resume: bool = True,        # True = tiếp tục từ checkpoint
):
    if not MISTRAL_API_KEY:
        raise ValueError(
            "MISTRAL_API_KEY chưa được thiết lập. "
            "Thêm key vào file .env ở thư mục gốc project hoặc biến môi trường."
        )

    logger.info("=" * 60)
    logger.info("BẮT ĐẦU PIPELINE PARAPHRASE MISTRAL AI")
    logger.info(f"Model: {MISTRAL_MODEL}")
    logger.info(f"Input: {input_file}")
    logger.info(f"Output: {output_file}")
    logger.info(f"Số paraphrase/sample: {num_paraphrases}")
    logger.info("=" * 60)

    # Load dataset
    df = pd.read_csv(input_file)
    if sample_limit:
        df = df.head(sample_limit)
        logger.info(f"Chế độ test: chỉ xử lý {sample_limit} samples đầu")

    logger.info(f"Tổng số samples: {len(df)}")
    logger.info(f"Phân bố category:\n{df['category'].value_counts().to_string()}")

    # Load checkpoint (resume)
    checkpoint = load_checkpoint() if resume else {"processed_ids": [], "results": []}
    processed_ids = set(checkpoint["processed_ids"])
    results = checkpoint["results"]

    logger.info(f"Đã xử lý trước đó: {len(processed_ids)} samples")

    # Thống kê tiến độ
    total_to_process = len(df) - len(processed_ids)
    total_api_calls = total_to_process * num_paraphrases
    estimated_time = total_api_calls * DELAY_BETWEEN_REQUESTS / 60
    logger.info(f"Cần xử lý thêm: {total_to_process} samples ({total_api_calls} API calls)")
    logger.info(f"Ước tính thời gian: ~{estimated_time:.1f} phút")

    # ---- VÒNG LẶP CHÍNH ----
    processed_count = 0
    error_count = 0

    for idx, row in df.iterrows():
        sample_id = row["sample_id"]

        # Bỏ qua nếu đã xử lý
        if sample_id in processed_ids:
            continue

        category = row["category"]
        content = row["content"]
        prompt = CATEGORY_PROMPTS.get(category, DEFAULT_PROMPT)

        logger.info(f"[{idx+1}/{len(df)}] Xử lý: {sample_id} | {category}")

        # Tạo N paraphrase cho sample này
        for para_idx in range(num_paraphrases):
            time.sleep(DELAY_BETWEEN_REQUESTS)  # rate limiting

            paraphrased = call_mistral_api(prompt, content)

            if paraphrased:
                # Tạo row mới với dữ liệu paraphrase
                new_row = row.to_dict()
                new_row["sample_id"] = f"{sample_id}_para_{para_idx+1}"
                new_row["content"] = paraphrased
                new_row["data_origin"] = "paraphrased"
                new_row["source_row_id"] = sample_id  # trỏ về gốc
                results.append(new_row)
                logger.info(f"  ✓ Para {para_idx+1}: {paraphrased[:60]}...")
            else:
                error_count += 1
                logger.warning(f"  ✗ Lỗi para {para_idx+1} cho {sample_id}")

        # Đánh dấu đã xử lý và lưu checkpoint
        processed_ids.add(sample_id)
        checkpoint["processed_ids"] = list(processed_ids)
        checkpoint["results"] = results
        save_checkpoint(checkpoint)

        processed_count += 1

        # Lưu output mỗi 100 samples
        if processed_count % 100 == 0:
            _save_output(results, output_file)
            logger.info(f">>> Đã lưu intermediate output: {len(results)} paraphrases")

    # ---- LƯU KẾT QUẢ CUỐI ----
    _save_output(results, output_file)

    logger.info("=" * 60)
    logger.info("HOÀN THÀNH!")
    logger.info(f"Tổng paraphrase tạo được: {len(results)}")
    logger.info(f"Số lỗi: {error_count}")
    logger.info(f"Output: {output_file}")
    logger.info("=" * 60)

    return pd.DataFrame(results)


def _save_output(results: list, output_file: str):
    """Lưu kết quả ra CSV"""
    if results:
        df_out = pd.DataFrame(results)
        df_out.to_csv(output_file, index=False, encoding="utf-8-sig")


# ==================== ENTRY POINT ====================
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mistral Paraphrase Pipeline")
    parser.add_argument("--input", default=INPUT_FILE, help="File CSV đầu vào")
    parser.add_argument("--output", default=OUTPUT_FILE, help="File CSV đầu ra")
    parser.add_argument("--num-paraphrases", type=int, default=1, help="Số paraphrase/sample")
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn số samples (để test)")
    parser.add_argument("--no-resume", action="store_true", help="Bắt đầu lại từ đầu (xóa checkpoint)")
    parser.add_argument("--model", default=MISTRAL_MODEL, help="Mistral model")
    args = parser.parse_args([]) # Modified to pass an empty list

    MISTRAL_MODEL = args.model

    run_pipeline(
        input_file=args.input,
        output_file=args.output,
        num_paraphrases=args.num_paraphrases,
        sample_limit=args.limit,
        resume=not args.no_resume,
    )
