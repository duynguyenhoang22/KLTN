"""
Validate ViSmishDS synthetic SMS datasets before they are merged into the
final training corpus.

The script is intentionally rule-based and reproducible. It does not try to
prove that synthetic text is "good" with one score; instead, it checks several
quality layers that are useful for thesis reporting:

1. Hard schema/metadata validation:
   - required columns
   - empty content
   - invalid label/sender values
   - duplicate content
   - `has_url` and `has_phone_number` consistency
2. Real-vs-synthetic distribution comparison:
   - message length
   - URL/contact-number rate
   - accent usage
   - digit and special-character density
   - sender/category/domain distributions
3. Diversity and realism diagnostics:
   - repeated n-grams
   - near-duplicate pairs
   - a real-vs-synthetic classifier

Metadata definitions used here:
    has_url:
        1 when the message contains a URL/domain-like link target, including
        bare domains such as `momo.vn` or Zalo/Telegram links. Numeric values
        such as prices and dates are excluded.

    has_phone_number:
        1 when the message contains a contactable number: mobile number,
        hotline, service shortcode, SMS opt-out shortcode, or Zalo number.
        IDs such as CCCD/CMND, account numbers, tracking/order IDs, refs, and
        OTPs are excluded.

Outputs:
    data/reports/synthetic_validation_report.md

Run from repository root:
    python scripts/data_pipeline/validate_synthetic.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
GROUND_TRUTH_DIR = DATA_DIR / "ground_truth"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
REPORT_DIR = DATA_DIR / "reports"
REPORT_PATH = REPORT_DIR / "synthetic_validation_report.md"

REAL_LABEL0 = GROUND_TRUTH_DIR / "dataset_label_0_with_categories.csv"
REAL_LABEL1 = GROUND_TRUTH_DIR / "dataset_label_1_with_categories.csv"
SYN_LABEL0 = SYNTHETIC_DIR / "synthetic_label_0.csv"
SYN_LABEL1 = SYNTHETIC_DIR / "synthetic_label_1.csv"

URL_TLDS = (
    "vn|com|net|org|me|ly|top|vip|icu|cc|club|life|xyz|xin|us|link|app|site|online|"
    "info|io|co|gov|edu|tech|bet|fun|live|click|store|shop"
)
EXPLICIT_URL_RE = re.compile(
    rf"(?i)(?:https?://|www\.)\S+|\b[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)*"
    rf"\.(?:{URL_TLDS})/[^\s]+"
)
BARE_DOMAIN_RE = re.compile(
    rf"(?i)\b[a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)*\.(?:{URL_TLDS})\b"
)
PHONE_RE = re.compile(
    r"(?ix)"
    r"(?<![A-Za-z0-9])(?:\+?84|0)(?:[\s.-]?\d){8,10}(?![A-Za-z0-9])"
    r"|(?<![A-Za-z0-9])(?:1800|1900)(?:[\s.-]?\d){4,6}(?![A-Za-z0-9])"
    r"|zalo\.me/(?:g/)?(?:\+?84|0)?\d{8,11}\b"
)
SHORT_CONTACT_RE = re.compile(
    r"(?ix)"
    r"\b(?:lh|lien\s*he|li[eê]n\s*h[eệ]|hotline|tong\s*dai|t[oổ]ng\s*[dđ][aà]i|"
    r"call|zalo|sdt|s[đd]t|dt|[đd]t)"
    r"\s*(?:[:.\-]|\s)?\s*(?:\w+\s+){0,3}(\d{3,11})\b"
    r"|\b(?:soan|so[aạ]n|tc|huy|kt|dk)\b(?:\s+\w+){0,4}\s+g[uử]i\s+(\d{3,6})\b"
)
CONTACT_OVERRIDE_RE = re.compile(
    r"(?i)\b(lh|lien\s*he|li[eê]n\s*h[eệ]|sdt|s[đd]t|dt|[đd]t|hotline|zalo)\b"
)
EXCLUDE_PHONE_CONTEXT_RE = re.compile(
    r"(?i)\b("
    r"cccd|cmnd|cmt|can\s*cuoc|c[aă]n\s*c[uư][oơ]c|"
    r"stk|tk|tai\s*khoan|t[aà]i\s*kho[aả]n|"
    r"ma\s*don|m[aã]\s*[dđ][oơ]n|don\s*hang|[dđ][oơ]n\s*h[aà]ng|"
    r"tracking|van\s*don|v[aậ]n\s*[dđ][oơ]n|ref|mgd|ma\s*gd|otp"
    r")\b"
)
DOMAIN_RE = re.compile(
    rf"(?i)(?:https?://)?(?:www\.)?\b([a-z0-9][a-z0-9-]*(?:\.[a-z0-9][a-z0-9-]*)*"
    rf"\.(?:{URL_TLDS}))"
)
VIETNAMESE_ACCENT_RE = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡ"
    r"ùúụủũưừứựửữỳýỵỷỹđ"
    r"ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ"
    r"ÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]"
)
SPECIAL_RE = re.compile(r"[^A-Za-zÀ-ỹ0-9\s]")
DIGIT_RE = re.compile(r"\d")

VALID_SENDER_TYPES = {"brandname", "shortcode", "personal_number"}


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    path: Path
    expected_label: int
    is_synthetic: bool


DATASETS = [
    DatasetSpec("real_label_0", REAL_LABEL0, 0, False),
    DatasetSpec("real_label_1", REAL_LABEL1, 1, False),
    DatasetSpec("synthetic_label_0", SYN_LABEL0, 0, True),
    DatasetSpec("synthetic_label_1", SYN_LABEL1, 1, True),
]


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def as_int_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value).strip().lower())


def has_url(text: str) -> bool:
    value = str(text)
    if EXPLICIT_URL_RE.search(value):
        return True
    return bool(BARE_DOMAIN_RE.search(value))


def normalize_contact_context(text: str) -> str:
    value = str(text).lower()
    value = re.sub(r"[_~^*!;:|<>{}\[\](),\"']", " ", value)
    return value.translate(str.maketrans({"4": "a", "@": "a", "1": "i", "0": "o", "3": "e"}))


def has_phone(text: str) -> bool:
    value = str(text)
    for match in PHONE_RE.finditer(value):
        start = max(0, match.start() - 28)
        end = min(len(value), match.end() + 12)
        context = value[start:end]
        context_norm = normalize_contact_context(context)
        if (
            not EXCLUDE_PHONE_CONTEXT_RE.search(context)
            or CONTACT_OVERRIDE_RE.search(context)
            or CONTACT_OVERRIDE_RE.search(context_norm)
        ):
            return True

    for match in SHORT_CONTACT_RE.finditer(value):
        number = match.group(1) or match.group(2)
        if number and 3 <= len(number) <= 6:
            return True
        if number and len(number) >= 8 and CONTACT_OVERRIDE_RE.search(match.group(0)):
            return True
    return False


def has_accent(text: str) -> bool:
    return bool(VIETNAMESE_ACCENT_RE.search(text))


def extract_domains(texts: Iterable[str]) -> pd.Series:
    domains: list[str] = []
    for text in texts:
        domains.extend(match.group(1).lower().rstrip(".,);]") for match in DOMAIN_RE.finditer(str(text)))
    return pd.Series(domains, dtype="string")


def describe_binary(series: pd.Series) -> str:
    if len(series) == 0:
        return "0.00%"
    return f"{series.mean() * 100:.2f}%"


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows._"
    shown = df if max_rows is None else df.head(max_rows)
    return shown.to_markdown(index=False)


def value_counts_table(series: pd.Series, name: str, top_n: int = 20) -> pd.DataFrame:
    if series.empty:
        return pd.DataFrame(columns=[name, "count", "percent"])
    counts = series.fillna("<missing>").replace("", "<empty>").value_counts(dropna=False).head(top_n)
    total = len(series)
    return pd.DataFrame(
        {
            name: counts.index.astype(str),
            "count": counts.values,
            "percent": [f"{count / total * 100:.2f}%" for count in counts.values],
        }
    )


def collect_validation(df: pd.DataFrame, spec: DatasetSpec) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict[str, object]] = []
    invalid_rows: list[dict[str, object]] = []
    required = ["content", "label", "has_url", "has_phone_number", "sender_type"]

    for column in required:
        missing = column not in df.columns
        rows.append(
            {
                "dataset": spec.name,
                "check": f"required column: {column}",
                "failures": int(missing),
                "rate": "100.00%" if missing else "0.00%",
            }
        )

    if any(column not in df.columns for column in required):
        return pd.DataFrame(rows), pd.DataFrame(invalid_rows)

    work = df.copy()
    work["content_norm"] = work["content"].map(normalize_text)
    work["label_int"] = as_int_series(work["label"])
    work["has_url_int"] = as_int_series(work["has_url"])
    work["has_phone_int"] = as_int_series(work["has_phone_number"])
    work["actual_has_url"] = work["content"].astype(str).map(has_url).astype(int)
    work["actual_has_phone"] = work["content"].astype(str).map(has_phone).astype(int)
    work["content_length"] = work["content"].astype(str).str.len()

    checks = {
        "empty content": work["content_norm"].eq(""),
        f"label != {spec.expected_label}": work["label_int"].ne(spec.expected_label),
        "invalid has_url": ~work["has_url_int"].isin([0, 1]),
        "invalid has_phone_number": ~work["has_phone_int"].isin([0, 1]),
        "invalid sender_type": ~work["sender_type"].isin(VALID_SENDER_TYPES),
        "has_url mismatch": work["has_url_int"].ne(work["actual_has_url"]),
        "has_phone_number mismatch": work["has_phone_int"].ne(work["actual_has_phone"]),
        "content length < 10": work["content_length"].lt(10),
        "content length > 500": work["content_length"].gt(500),
        "exact duplicate content": work.duplicated("content_norm", keep=False),
    }

    for check, mask in checks.items():
        failures = int(mask.sum())
        rows.append(
            {
                "dataset": spec.name,
                "check": check,
                "failures": failures,
                "rate": f"{failures / len(work) * 100:.2f}%" if len(work) else "0.00%",
            }
        )
        if failures:
            sample = work.loc[mask, ["content", "label", "has_url", "has_phone_number", "sender_type"]].head(10)
            for idx, row in sample.iterrows():
                invalid_rows.append(
                    {
                        "dataset": spec.name,
                        "check": check,
                        "row_index": idx,
                        "content": str(row["content"])[:180],
                    }
                )

    if spec.name == "synthetic_label_0":
        category_missing = "category" not in df.columns
        rows.append(
            {
                "dataset": spec.name,
                "check": "category column present",
                "failures": int(category_missing),
                "rate": "100.00%" if category_missing else "0.00%",
            }
        )
    if spec.name == "synthetic_label_1":
        category_missing = not ({"category", "category_label", "smishing_type"} & set(df.columns))
        rows.append(
            {
                "dataset": spec.name,
                "check": "smishing category metadata present",
                "failures": int(category_missing),
                "rate": "100.00%" if category_missing else "0.00%",
            }
        )

    return pd.DataFrame(rows), pd.DataFrame(invalid_rows)


def profile_dataset(df: pd.DataFrame, spec: DatasetSpec) -> dict[str, object]:
    content = df["content"].fillna("").astype(str)
    lengths = content.str.len()
    has_url_actual = content.map(has_url)
    has_phone_actual = content.map(has_phone)
    special_counts = content.map(lambda text: len(SPECIAL_RE.findall(text)))
    digit_counts = content.map(lambda text: len(DIGIT_RE.findall(text)))

    return {
        "dataset": spec.name,
        "rows": len(df),
        "avg_length": round(float(lengths.mean()), 2),
        "median_length": round(float(lengths.median()), 2),
        "p95_length": round(float(lengths.quantile(0.95)), 2),
        "actual_url_rate": describe_binary(has_url_actual),
        "actual_phone_rate": describe_binary(has_phone_actual),
        "accented_rate": describe_binary(content.map(has_accent)),
        "avg_digits": round(float(digit_counts.mean()), 2),
        "avg_special_chars": round(float(special_counts.mean()), 2),
        "unique_content_rate": f"{content.map(normalize_text).nunique() / len(df) * 100:.2f}%" if len(df) else "0.00%",
    }


def compare_profiles(real_df: pd.DataFrame, syn_df: pd.DataFrame, label: int) -> pd.DataFrame:
    real_content = real_df["content"].fillna("").astype(str)
    syn_content = syn_df["content"].fillna("").astype(str)

    def numeric_features(content: pd.Series) -> dict[str, float]:
        lengths = content.str.len()
        return {
            "avg_length": float(lengths.mean()),
            "median_length": float(lengths.median()),
            "url_rate": float(content.map(has_url).mean()),
            "phone_rate": float(content.map(has_phone).mean()),
            "accented_rate": float(content.map(has_accent).mean()),
            "avg_digits": float(content.map(lambda text: len(DIGIT_RE.findall(text))).mean()),
            "avg_special_chars": float(content.map(lambda text: len(SPECIAL_RE.findall(text))).mean()),
        }

    real = numeric_features(real_content)
    syn = numeric_features(syn_content)
    rows = []
    for metric in real:
        rows.append(
            {
                "label": label,
                "metric": metric,
                "real": round(real[metric], 4),
                "synthetic": round(syn[metric], 4),
                "absolute_gap": round(abs(real[metric] - syn[metric]), 4),
            }
        )
    return pd.DataFrame(rows)


def top_ngrams(texts: pd.Series, ngram_range: tuple[int, int] = (3, 5), top_n: int = 20) -> pd.DataFrame:
    vectorizer = TfidfVectorizer(
        analyzer="word",
        ngram_range=ngram_range,
        lowercase=True,
        token_pattern=r"(?u)\b\w+\b",
        use_idf=False,
        norm=None,
        min_df=2,
    )
    try:
        matrix = vectorizer.fit_transform(texts.fillna("").astype(str))
    except ValueError:
        return pd.DataFrame(columns=["phrase", "count"])
    counts = np.asarray(matrix.sum(axis=0)).ravel()
    features = np.array(vectorizer.get_feature_names_out())
    order = counts.argsort()[::-1][:top_n]
    return pd.DataFrame({"phrase": features[order], "count": counts[order].astype(int)})


def near_duplicate_summary(df: pd.DataFrame, sample_size: int = 1500, threshold: float = 0.9) -> dict[str, object]:
    texts = df["content"].fillna("").astype(str).map(normalize_text)
    if len(texts) < 2:
        return {"sample_size": len(texts), "pairs_over_threshold": 0, "max_similarity": 0.0}

    sampled = texts.sample(n=min(sample_size, len(texts)), random_state=42)
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2)
    matrix = vectorizer.fit_transform(sampled)
    sim = cosine_similarity(matrix)
    upper = sim[np.triu_indices_from(sim, k=1)]
    pairs_over = int((upper >= threshold).sum())
    max_sim = float(upper.max()) if upper.size else 0.0
    return {
        "sample_size": len(sampled),
        "pairs_over_threshold": pairs_over,
        "max_similarity": round(max_sim, 4),
        "threshold": threshold,
    }


def real_vs_synthetic_classifier(real_df: pd.DataFrame, syn_df: pd.DataFrame, label: int) -> dict[str, object]:
    min_rows = min(len(real_df), len(syn_df))
    if min_rows < 20:
        return {"label": label, "status": "not enough rows"}

    real_sample = real_df.sample(n=min_rows, random_state=42)
    syn_sample = syn_df.sample(n=min_rows, random_state=42)
    x = pd.concat([real_sample["content"], syn_sample["content"]], ignore_index=True).fillna("").astype(str)
    y = np.array([1] * min_rows + [0] * min_rows)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )
    model = make_pipeline(
        TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2),
        LogisticRegression(max_iter=1000, class_weight="balanced"),
    )
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    prob = model.predict_proba(x_test)[:, 1]
    return {
        "label": label,
        "status": "ok",
        "balanced_rows_per_class": min_rows,
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4),
        "interpretation": "higher means synthetic is easier to distinguish from real",
    }


def report_section(title: str) -> str:
    return f"\n## {title}\n\n"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    frames = {spec.name: read_csv(spec.path) for spec in DATASETS}

    validation_tables = []
    invalid_samples = []
    profiles = []
    for spec in DATASETS:
        df = frames[spec.name]
        checks, samples = collect_validation(df, spec)
        validation_tables.append(checks)
        invalid_samples.append(samples)
        profiles.append(profile_dataset(df, spec))

    validation = pd.concat(validation_tables, ignore_index=True)
    invalid = pd.concat(invalid_samples, ignore_index=True) if invalid_samples else pd.DataFrame()
    profile = pd.DataFrame(profiles)

    comparisons = pd.concat(
        [
            compare_profiles(frames["real_label_0"], frames["synthetic_label_0"], 0),
            compare_profiles(frames["real_label_1"], frames["synthetic_label_1"], 1),
        ],
        ignore_index=True,
    )

    near_dupes = pd.DataFrame(
        [
            {"dataset": name, **near_duplicate_summary(df)}
            for name, df in frames.items()
            if name.startswith("synthetic")
        ]
    )

    classifiers = pd.DataFrame(
        [
            real_vs_synthetic_classifier(frames["real_label_0"], frames["synthetic_label_0"], 0),
            real_vs_synthetic_classifier(frames["real_label_1"], frames["synthetic_label_1"], 1),
        ]
    )

    lines: list[str] = []
    lines.append("# Synthetic Dataset Validation Report\n\n")
    lines.append("Generated by `scripts/data_pipeline/validate_synthetic.py`.\n")
    lines.append(report_section("1. Dataset Inventory"))
    inventory = pd.DataFrame(
        {
            "dataset": [spec.name for spec in DATASETS],
            "path": [str(spec.path.relative_to(ROOT)) for spec in DATASETS],
            "rows": [len(frames[spec.name]) for spec in DATASETS],
            "columns": [", ".join(frames[spec.name].columns) for spec in DATASETS],
        }
    )
    lines.append(md_table(inventory))

    lines.append(report_section("2. Hard Validation Checks"))
    lines.append(md_table(validation))
    lines.append("\n\nRows with non-zero failures should be reviewed before merging final data.\n")

    lines.append(report_section("3. Invalid Row Samples"))
    lines.append(md_table(invalid, max_rows=80))

    lines.append(report_section("4. Basic Text Profiles"))
    lines.append(md_table(profile))

    lines.append(report_section("5. Real vs Synthetic Distribution Gaps"))
    lines.append(md_table(comparisons))

    lines.append(report_section("6. Sender Type Distribution"))
    for name, df in frames.items():
        lines.append(f"### {name}\n\n")
        lines.append(md_table(value_counts_table(df.get("sender_type", pd.Series(dtype=str)), "sender_type")))
        lines.append("\n\n")

    lines.append(report_section("7. Category Distribution"))
    category_columns = {
        "real_label_0": "category_label",
        "real_label_1": "smishing_type",
        "synthetic_label_0": "category",
        "synthetic_label_1": "category",
    }
    for name, df in frames.items():
        column = category_columns[name]
        lines.append(f"### {name}\n\n")
        if column in df.columns:
            lines.append(md_table(value_counts_table(df[column], column)))
        else:
            lines.append(f"_Missing `{column}` column._")
        lines.append("\n\n")

    lines.append(report_section("8. Top Repeated Phrases in Synthetic Data"))
    for name in ["synthetic_label_0", "synthetic_label_1"]:
        lines.append(f"### {name}\n\n")
        lines.append(md_table(top_ngrams(frames[name]["content"], top_n=20)))
        lines.append("\n\n")

    lines.append(report_section("9. Top URL Domains"))
    for name, df in frames.items():
        domains = extract_domains(df["content"].fillna("").astype(str))
        lines.append(f"### {name}\n\n")
        lines.append(md_table(value_counts_table(domains, "domain", top_n=20)))
        lines.append("\n\n")

    lines.append(report_section("10. Near-Duplicate Summary"))
    lines.append(md_table(near_dupes))

    lines.append(report_section("11. Real-vs-Synthetic Classifier"))
    lines.append(md_table(classifiers))
    lines.append(
        "\n\nInterpretation: this classifier tries to distinguish real SMS from synthetic SMS "
        "within the same label. Scores close to 0.50 mean synthetic data is hard to separate "
        "from real data. Very high scores mean synthetic data has visible artifacts or a shifted distribution.\n"
    )

    lines.append(report_section("12. Recommended Quality Gates"))
    lines.append(
        "- Fix all schema issues and metadata mismatches before building the final merged dataset.\n"
        "- Keep exact duplicate rate at 0% inside each split.\n"
        "- Review near-duplicate clusters when cosine similarity is above 0.90.\n"
        "- Keep final test data real-only; synthetic data should be used for training/augmentation only.\n"
        "- Add `smishing_type` to synthetic label-1 generation so attack-type coverage can be measured.\n"
    )

    REPORT_PATH.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
