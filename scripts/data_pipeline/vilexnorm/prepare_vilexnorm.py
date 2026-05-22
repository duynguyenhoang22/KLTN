"""Prepare ViLexNorm raw splits into a single processed file.

This step is intentionally narrow: it only converts ViLexNorm raw split files
into one normalized CSV with provenance columns. Filtering, sampling and
deduplication against ViSmishDS are handled by later pipeline steps.
"""

import csv
from collections import Counter

from pathlib import Path


RAW_DIR = Path("data/external/vilexnorm/raw")
OUT_FILE = Path("data/external/vilexnorm/processed/vilexnorm_all.csv")
SOURCE_DATASET = "vilexnorm"
SPLIT_FILES = {
    "train": "train.csv",
    "dev": "dev.csv",
    "test": "test.csv",
}
OUTPUT_FIELDS = [
    "source_dataset",
    "source_file",
    "source_row_id",
    "split",
    "original",
    "normalized",
]


def _read_split(split: str, file_name: str) -> list[dict[str, str]]:
    path = RAW_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"Missing raw ViLexNorm split: {path}")

    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"Raw split has no header: {path}")

        required = {"original", "normalized"}
        missing = required.difference(reader.fieldnames)
        if missing:
            missing_cols = ", ".join(sorted(missing))
            raise ValueError(f"{path} is missing required columns: {missing_cols}")

        index_col = "" if "" in reader.fieldnames else None
        for row_number, raw_row in enumerate(reader):
            original = (raw_row.get("original") or "").strip()
            normalized = (raw_row.get("normalized") or "").strip()
            if not original and not normalized:
                continue

            source_row_id = (raw_row.get(index_col) or "").strip() if index_col else ""
            if not source_row_id:
                source_row_id = str(row_number)

            rows.append(
                {
                    "source_dataset": SOURCE_DATASET,
                    "source_file": str(path.as_posix()),
                    "source_row_id": source_row_id,
                    "split": split,
                    "original": original,
                    "normalized": normalized,
                }
            )

    return rows


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, str]] = []
    split_counts: Counter[str] = Counter()
    for split, file_name in SPLIT_FILES.items():
        split_rows = _read_split(split, file_name)
        all_rows.extend(split_rows)
        split_counts[split] = len(split_rows)

    with OUT_FILE.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    original_counts = Counter(row["original"] for row in all_rows)
    duplicate_originals = sum(1 for count in original_counts.values() if count > 1)

    print(f"Input directory: {RAW_DIR}")
    print(f"Output file: {OUT_FILE}")
    print(f"Rows written: {len(all_rows)}")
    for split in SPLIT_FILES:
        print(f"- {split}: {split_counts[split]}")
    print(f"Duplicate original texts retained for later review: {duplicate_originals}")


if __name__ == "__main__":
    main()
