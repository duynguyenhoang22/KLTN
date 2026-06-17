from __future__ import annotations

import re
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path("setup_results")
OUT_DIR = ROOT / "manual_error_analysis"

SETUP_DIRS = [
    ROOT / "setup_a_results",
    ROOT / "setup_b_results",
    ROOT / "setup_e_results",
    ROOT / "setup_g_results",
]

KEY_VARIANTS = {
    "A_real_only",
    "B1_class_weight_default",
    "B2_class_weight_threshold",
    "E4_all",
    "G0_E4_champion",
    "G2_external_curated",
}

URL_RE = re.compile(r"https?://|www\.|bit\.ly|tinyurl|t\.me|zalo\.me|facebook\.com|m\.me|\.com|\.vn|\.net", re.I)
PHONE_RE = re.compile(r"(?:\+?84|0|\(?0)\D{0,3}\d(?:\D{0,3}\d){7,10}")
MONEY_RE = re.compile(r"\b\d+[\.,]?\d*\s*(?:k|tr|tri[eệ]u|ng[aà]n|vnd|đ|dong)\b", re.I)
REWARD_RE = re.compile(r"ch[uú]c m[uư]ng|tr[uú]ng|qu[aà]|th[ưởư]ng|ưu đãi|khuy[eế]n m[aã]i|gi[aả]m|voucher|tặng|điểm", re.I)
RECRUIT_RE = re.compile(r"tuy[eể]n|vi[eệ]c l[aà]m|c[oộ]ng t[aá]c|thu nh[aậ]p|l[uư][ơo]ng|online|t[aạ]i nh[aà]|nh[aậ]p li[eệ]u|x[uử] l[yý] đơn", re.I)
OFFICIAL_RE = re.compile(r"bộ|cục|thuế|bhxh|công an|điện lực|ngân hàng|đại học|trường|fpt|viettel|vinaphone|mobifone|shopee|cskh|hotline", re.I)
OTP_RE = re.compile(r"\botp\b|m[aã]\s+(?:xac|x[aá]c|otp)|đăng nh[aậ]p|giao d[iị]ch", re.I)
OBF_RE = re.compile(r"[*_~`^|<>]|[a-zA-Z]*[01345789@$!][a-zA-Z]+|[a-zA-Z]+[01345789@$!][a-zA-Z]*")


def normalize_variant(df: pd.DataFrame) -> pd.Series:
    if "variant" in df.columns:
        variant = df["variant"].fillna("").astype(str)
    else:
        variant = pd.Series("", index=df.index)
    setup = df["setup"].fillna("").astype(str)
    return np.where(variant.str.len() > 0, variant, setup)


def read_error_files() -> pd.DataFrame:
    frames = []
    for setup_dir in SETUP_DIRS:
        for path in sorted(setup_dir.glob("*_errors.csv")):
            df = pd.read_csv(path)
            df["source_error_file"] = str(path)
            df["variant_key"] = normalize_variant(df)
            if "threshold" not in df.columns:
                df["threshold"] = np.nan
            frames.append(df)
    if not frames:
        raise FileNotFoundError("No *_errors.csv files found for A/B/E/G.")
    out = pd.concat(frames, ignore_index=True)
    out["seed"] = out["seed"].astype(int)
    out["true_label"] = out["true_label"].astype(int)
    out["pred_label"] = out["pred_label"].astype(int)
    if "sample_id" not in out.columns:
        out["sample_id"] = ""
    out["sample_id"] = out["sample_id"].fillna("").astype(str)
    out["content"] = out["content"].fillna("").astype(str)
    for col in ["category", "sender_type", "data_origin", "has_url", "has_phone_number", "obfuscation_level"]:
        if col not in out.columns:
            out[col] = ""
    content_hash = out["content"].map(lambda text: hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:12])
    out["case_id"] = np.where(out["sample_id"].str.len() > 0, out["sample_id"], "content_" + content_hash)
    return out


def reason_for_row(row: pd.Series) -> str:
    text = str(row.get("content", ""))
    cat = str(row.get("category", ""))
    sender = str(row.get("sender_type", ""))
    has_url_value = row.get("has_url", 0)
    has_phone_value = row.get("has_phone_number", 0)
    has_url = (not pd.isna(has_url_value) and int(has_url_value) == 1) or bool(URL_RE.search(text))
    has_phone = (not pd.isna(has_phone_value) and int(has_phone_value) == 1) or bool(PHONE_RE.search(text))
    is_fp = row.get("error_type") == "FP"

    if is_fp:
        if RECRUIT_RE.search(text):
            return "FP_legitimate_recruitment_like"
        if REWARD_RE.search(text):
            return "FP_legitimate_promotion_reward"
        if has_url and has_phone:
            return "FP_legitimate_url_and_phone"
        if has_url:
            return "FP_legitimate_with_url"
        if has_phone:
            return "FP_legitimate_with_phone"
        if OFFICIAL_RE.search(text) or sender == "brandname":
            return "FP_official_brandlike"
        if OTP_RE.search(text):
            return "FP_otp_transaction_like"
        return "FP_other_or_ambiguous"

    if OBF_RE.search(text):
        return "FN_obfuscation_or_leet"
    if REWARD_RE.search(text) and not has_url:
        return "FN_smishing_reward_without_url"
    if RECRUIT_RE.search(text) and ("FPT" in text or "fpt" in text):
        return "FN_smishing_recruitment_brandlike"
    if has_url and not has_phone:
        return "FN_smishing_with_url_only"
    if has_phone and not has_url:
        return "FN_smishing_with_phone_only"
    if len(text) < 90:
        return "FN_short_low_context"
    if OFFICIAL_RE.search(text) or sender == "brandname" or "giả" in cat.lower():
        return "FN_official_or_brandlike_smishing"
    return "FN_other_or_ambiguous"


def compact_content(text: str, limit: int = 260) -> str:
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def summarize_errors(errors: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary = (
        errors.groupby(["variant_key", "seed", "eval_subset", "error_type"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["variant_key", "seed", "eval_subset", "error_type"])
    )

    by_reason = (
        errors.groupby(["variant_key", "error_type", "suggested_reason"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["variant_key", "error_type", "n"], ascending=[True, True, False])
    )

    by_category = (
        errors.groupby(["variant_key", "error_type", "category"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["variant_key", "error_type", "n"], ascending=[True, True, False])
    )

    stable = (
        errors.groupby(["variant_key", "case_id", "error_type"], dropna=False)
        .agg(
            sample_id=("sample_id", "first"),
            seeds=("seed", lambda s: ",".join(map(str, sorted(set(s))))),
            n_seeds=("seed", "nunique"),
            eval_subset=("eval_subset", lambda s: ",".join(sorted(set(map(str, s))))),
            category=("category", "first"),
            sender_type=("sender_type", "first"),
            data_origin=("data_origin", "first"),
            suggested_reason=("suggested_reason", "first"),
            mean_prob_label1=("prob_label1", "mean"),
            content=("content", "first"),
        )
        .reset_index()
        .sort_values(["variant_key", "error_type", "n_seeds", "mean_prob_label1"], ascending=[True, True, False, False])
    )
    stable["content_short"] = stable["content"].map(compact_content)
    return summary, by_reason, by_category, stable


def representative_review(stable: pd.DataFrame) -> pd.DataFrame:
    keep = stable[stable["variant_key"].isin(KEY_VARIANTS)].copy()
    rows = []
    for (variant, etype), group in keep.groupby(["variant_key", "error_type"], dropna=False):
        ranked = group.sort_values(["n_seeds", "mean_prob_label1"], ascending=[False, etype == "FN"])
        rows.append(ranked.head(12))
    if not rows:
        return keep
    review = pd.concat(rows, ignore_index=True)
    review.insert(0, "manual_reason", "")
    review.insert(1, "manual_note", "")
    cols = [
        "manual_reason",
        "manual_note",
        "variant_key",
        "sample_id",
        "error_type",
        "n_seeds",
        "seeds",
        "eval_subset",
        "category",
        "sender_type",
        "data_origin",
        "suggested_reason",
        "mean_prob_label1",
        "content",
    ]
    return review[cols]


def pivot_counts(errors: pd.DataFrame) -> pd.DataFrame:
    piv = (
        errors[errors["variant_key"].isin(KEY_VARIANTS)]
        .pivot_table(
            index=["variant_key", "seed"],
            columns="error_type",
            values="sample_id",
            aggfunc="count",
            fill_value=0,
        )
        .reset_index()
    )
    for col in ["FP", "FN"]:
        if col not in piv.columns:
            piv[col] = 0
    piv["total_errors"] = piv["FP"] + piv["FN"]
    return piv.sort_values(["variant_key", "seed"])


def write_report(errors: pd.DataFrame, stable: pd.DataFrame, by_reason: pd.DataFrame, pivot: pd.DataFrame) -> None:
    lines = []
    lines.append("# Phân tích thủ công FP/FN cho Setup A/B/E/G\n")
    lines.append("## Phạm vi\n")
    lines.append(
        "Báo cáo này dùng các file `*_errors.csv` sinh từ prediction-level output của Setup A, B, E và G. "
        "Mục tiêu là giải thích pattern lỗi, không thay thế các chỉ số định lượng chính.\n"
    )
    lines.append("Các lỗi được gom theo `variant_key`, `seed`, `error_type`, metadata và một taxonomy nguyên nhân lỗi sơ bộ. "
                 "Cột `suggested_reason` là nhãn gợi ý bằng rule; khi đưa vào khóa luận có thể rà lại các dòng trong `manual_review_candidates.csv`.\n")

    lines.append("## Tổng quan lỗi ở các setup trọng tâm\n")
    lines.append(pivot.to_markdown(index=False))
    lines.append("")

    focus = by_reason[by_reason["variant_key"].isin(KEY_VARIANTS)].copy()
    lines.append("## Nhóm nguyên nhân lỗi nổi bật\n")
    for variant in ["A_real_only", "B1_class_weight_default", "B2_class_weight_threshold", "E4_all", "G0_E4_champion", "G2_external_curated"]:
        sub = focus[focus["variant_key"].eq(variant)]
        if sub.empty:
            continue
        lines.append(f"### {variant}")
        lines.append(sub.head(10).to_markdown(index=False))
        lines.append("")

    lines.append("## Nhận định chính\n")
    lines.append(
        "1. Trên Real Test, các setup A/B/E mắc rất ít lỗi tuyệt đối vì test set nhỏ; do đó phân tích lỗi nên xem như minh họa định tính cho trade-off precision/recall.\n"
    )
    lines.append(
        "2. Cặp A vs E4 phù hợp để phân tích tác động của synthetic Label 1 augmentation: E4 giữ số lỗi thấp, nhưng cần kiểm tra các FP xem mô hình có nhạy hơn với URL/khuyến mãi/brandname hay không.\n"
    )
    lines.append(
        "3. Cặp G0 vs G2 là bằng chứng định tính mạnh nhất: G0 tạo nhiều FP trên external Label 0, trong khi G2 loại bỏ lỗi external ở cả ba seed và chỉ còn lỗi trên real subset. Điều này ủng hộ luận điểm cần mở rộng miền Label 0 khi dùng synthetic Label 1 augmentation.\n"
    )
    lines.append(
        "4. Các lỗi FN ổn định qua nhiều seed thường là smishing có bề mặt giống tin hợp lệ: thiếu URL, dùng shortcode/brandname, văn phong khuyến mãi hoặc tuyển sinh hợp lệ. Đây là nhóm nên được mô tả trong phần hạn chế.\n"
    )

    lines.append("## File artefact\n")
    lines.append("- `all_errors_labeled.csv`: toàn bộ FP/FN đã gán `suggested_reason`.\n")
    lines.append("- `stable_error_cases.csv`: lỗi gộp theo mẫu và số seed mắc lỗi.\n")
    lines.append("- `manual_review_candidates.csv`: tập mẫu ưu tiên để rà thủ công và viết ví dụ trong khóa luận.\n")
    lines.append("- `error_summary_by_setup_seed.csv`, `error_summary_by_reason.csv`, `error_summary_by_category.csv`: các bảng tổng hợp.\n")

    (OUT_DIR / "fp_fn_manual_analysis_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    errors = read_error_files()
    errors["suggested_reason"] = errors.apply(reason_for_row, axis=1)

    summary, by_reason, by_category, stable = summarize_errors(errors)
    review = representative_review(stable)
    pivot = pivot_counts(errors)

    errors.to_csv(OUT_DIR / "all_errors_labeled.csv", index=False, encoding="utf-8-sig")
    summary.to_csv(OUT_DIR / "error_summary_by_setup_seed.csv", index=False, encoding="utf-8-sig")
    by_reason.to_csv(OUT_DIR / "error_summary_by_reason.csv", index=False, encoding="utf-8-sig")
    by_category.to_csv(OUT_DIR / "error_summary_by_category.csv", index=False, encoding="utf-8-sig")
    stable.to_csv(OUT_DIR / "stable_error_cases.csv", index=False, encoding="utf-8-sig")
    review.to_csv(OUT_DIR / "manual_review_candidates.csv", index=False, encoding="utf-8-sig")
    pivot.to_csv(OUT_DIR / "key_variant_error_counts.csv", index=False, encoding="utf-8-sig")
    write_report(errors, stable, by_reason, pivot)

    print(f"[OK] Wrote manual error analysis to {OUT_DIR}")
    print(pivot.to_string(index=False))


if __name__ == "__main__":
    main()
