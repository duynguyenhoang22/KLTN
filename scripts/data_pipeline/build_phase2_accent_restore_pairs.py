"""
Build Phase 2 accent-restoration pairs from the Phase 1 final dataset.

The output is a raw Seq2Seq pair dataset for Vietnamese accent restoration:
`source_text` is the accent-stripped SMS content and `target_text` is the
original accented SMS content. This script does not create train/dev/test
splits and does not perform leet/noise normalization.

Outputs:
    data/normalization/phase2_accent_restore_pairs.csv
    data/reports/phase2_accent_restore_pairs_report.md

Run from repository root:
    python scripts/data_pipeline/build_phase2_accent_restore_pairs.py
"""

from __future__ import annotations

from pathlib import Path
import re
import unicodedata

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
FINAL_DATASET_PATH = DATA_DIR / "final" / "vismishds_phase1_final.csv"
NORMALIZATION_DIR = DATA_DIR / "normalization"
REPORT_DIR = DATA_DIR / "reports"
OUTPUT_PATH = NORMALIZATION_DIR / "phase2_accent_restore_pairs.csv"
REPORT_PATH = REPORT_DIR / "phase2_accent_restore_pairs_report.md"
EXPECTED_PAIR_COUNT = 2440
TASK_TYPE = "accent_restore"

VIETNAMESE_ACCENT_RE = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡ"
    r"ùúụủũưừứựửữỳýỵỷỹđ"
    r"ÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ"
    r"ÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]"
)

OUTPUT_COLUMNS = [
    "pair_id",
    "source_text",
    "target_text",
    "task_type",
    "label",
    "category",
    "has_url",
    "has_phone_number",
    "sender_type",
    "obfuscation_level",
    "data_origin",
    "source_sample_id",
    "source_dataset",
    "source_row_id",
]

METADATA_COLUMNS = [
    "label",
    "category",
    "has_url",
    "has_phone_number",
    "sender_type",
    "obfuscation_level",
    "data_origin",
    "source_sample_id",
    "source_dataset",
    "source_row_id",
]


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig")


def has_vietnamese_accent(text: object) -> bool:
    return bool(VIETNAMESE_ACCENT_RE.search("" if pd.isna(text) else str(text)))


def strip_vietnamese_accents(text: str) -> str:
    value = str(text).replace("đ", "d").replace("Đ", "D")
    decomposed = unicodedata.normalize("NFD", value)
    stripped = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    return unicodedata.normalize("NFC", stripped)


def md_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    return df.to_markdown(index=False)


def validate_source_schema(df: pd.DataFrame) -> None:
    required = {
        "sample_id",
        "content",
        "label",
        "has_url",
        "has_phone_number",
        "sender_type",
        "category",
        "obfuscation_level",
        "data_origin",
        "source_dataset",
        "source_row_id",
    }
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{rel_path(FINAL_DATASET_PATH)} is missing columns: {', '.join(missing)}")


def build_pairs(phase1: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    validate_source_schema(phase1)

    accented = phase1.loc[phase1["content"].map(has_vietnamese_accent)].copy()
    pairs = pd.DataFrame(
        {
            "source_text": accented["content"].astype(str).str.strip().map(strip_vietnamese_accents),
            "target_text": accented["content"].astype(str).str.strip(),
            "task_type": TASK_TYPE,
            "label": pd.to_numeric(accented["label"], errors="raise").astype(int),
            "category": accented["category"].astype(str).str.strip(),
            "has_url": pd.to_numeric(accented["has_url"], errors="raise").astype(int),
            "has_phone_number": pd.to_numeric(accented["has_phone_number"], errors="raise").astype(int),
            "sender_type": accented["sender_type"].astype(str).str.strip(),
            "obfuscation_level": accented["obfuscation_level"].astype(str).str.strip(),
            "data_origin": accented["data_origin"].astype(str).str.strip(),
            "source_sample_id": accented["sample_id"].astype(str).str.strip(),
            "source_dataset": accented["source_dataset"].astype(str).str.strip(),
            "source_row_id": pd.to_numeric(accented["source_row_id"], errors="raise").astype(int),
        }
    )

    invalid = (
        pairs["source_text"].eq("")
        | pairs["target_text"].eq("")
        | pairs["source_text"].eq(pairs["target_text"])
    )
    skipped_rows = int(invalid.sum())
    pairs = pairs.loc[~invalid].copy()
    pairs.insert(0, "pair_id", [f"accent_restore_{idx:05d}" for idx in range(1, len(pairs) + 1)])
    return pairs[OUTPUT_COLUMNS], skipped_rows


def validate_output(df: pd.DataFrame) -> None:
    if list(df.columns) != OUTPUT_COLUMNS:
        raise ValueError("Output columns do not match the required order.")
    if len(df) != EXPECTED_PAIR_COUNT:
        raise ValueError(f"Expected {EXPECTED_PAIR_COUNT} pairs, found {len(df)}.")
    if not df["pair_id"].is_unique:
        raise ValueError("pair_id values are not unique.")
    if df[["source_text", "target_text"]].isna().any().any():
        raise ValueError("source_text or target_text contains null values.")
    if not df["target_text"].map(has_vietnamese_accent).all():
        raise ValueError("At least one target_text does not contain Vietnamese accents.")
    if df["source_text"].map(has_vietnamese_accent).any():
        raise ValueError("At least one source_text still contains Vietnamese accents.")
    if df["source_text"].eq(df["target_text"]).any():
        raise ValueError("At least one row has identical source_text and target_text.")
    if df[METADATA_COLUMNS].isna().any().any():
        raise ValueError("At least one metadata column contains null values.")
    for column in ["label", "has_url", "has_phone_number"]:
        if not df[column].isin([0, 1]).all():
            raise ValueError(f"{column} contains values outside 0/1.")
    if not df["task_type"].eq(TASK_TYPE).all():
        raise ValueError(f"task_type must always be {TASK_TYPE}.")


def build_report(phase1: pd.DataFrame, pairs: pd.DataFrame, selected_rows: int, skipped_rows: int) -> str:
    lines: list[str] = []
    lines.append("# Phase 2 Accent Restoration Pair Report\n\n")
    lines.append("Generated by `scripts/data_pipeline/build_phase2_accent_restore_pairs.py`.\n\n")
    lines.append("## Output\n\n")
    lines.append(f"- Input file: `{rel_path(FINAL_DATASET_PATH)}`\n")
    lines.append(f"- Output file: `{rel_path(OUTPUT_PATH)}`\n")
    lines.append(f"- Total phase-1 rows: {len(phase1)}\n")
    lines.append(f"- Accented rows selected: {selected_rows}\n")
    lines.append(f"- Final pair count: {len(pairs)}\n")
    lines.append(f"- Skipped rows after selection: {skipped_rows}\n\n")

    lines.append("## Pair Counts by Label\n\n")
    lines.append(md_table(pairs.groupby("label").size().reset_index(name="rows")))
    lines.append("\n\n")

    lines.append("## Pair Counts by Data Origin\n\n")
    lines.append(md_table(pairs.groupby("data_origin").size().reset_index(name="rows")))
    lines.append("\n\n")

    lines.append("## Pair Counts by Source Dataset\n\n")
    source_counts = pairs.groupby("source_dataset").size().reset_index(name="rows")
    lines.append(md_table(source_counts.sort_values("rows", ascending=False)))
    lines.append("\n\n")

    lines.append("## Pair Counts by Obfuscation Level\n\n")
    level_counts = pairs.groupby("obfuscation_level").size().reset_index(name="rows")
    lines.append(md_table(level_counts.sort_values("rows", ascending=False)))
    lines.append("\n\n")

    lines.append("## Note\n\n")
    lines.append(
        "This dataset is for accent restoration only. It does not perform full SMS "
        "normalization, leet repair, punctuation cleanup, or casing correction.\n"
    )
    return "".join(lines)


def main() -> None:
    NORMALIZATION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase1 = read_csv(FINAL_DATASET_PATH)
    selected_rows = int(phase1["content"].map(has_vietnamese_accent).sum())
    pairs, skipped_rows = build_pairs(phase1)
    if selected_rows != EXPECTED_PAIR_COUNT:
        raise ValueError(f"Expected {EXPECTED_PAIR_COUNT} accented source rows, found {selected_rows}.")
    if skipped_rows:
        raise ValueError(f"Expected 0 skipped rows after selection, found {skipped_rows}.")

    pairs.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    if not OUTPUT_PATH.exists():
        raise FileNotFoundError(f"Output file was not written: {OUTPUT_PATH}")

    reloaded = read_csv(OUTPUT_PATH)
    validate_output(reloaded)
    REPORT_PATH.write_text(build_report(phase1, pairs, selected_rows, skipped_rows), encoding="utf-8")

    print(f"Wrote pairs: {OUTPUT_PATH}")
    print(f"Wrote report: {REPORT_PATH}")
    print(f"Rows: {len(pairs)}")
    print(f"Skipped rows: {skipped_rows}")


if __name__ == "__main__":
    main()
