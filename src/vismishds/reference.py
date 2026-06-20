from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


def audit_reference(path: Path) -> dict[str, object]:
    counts: Counter[tuple[str, str]] = Counter()
    obfuscation: Counter[tuple[str, str]] = Counter()
    categories: Counter[tuple[str, str]] = Counter()
    ids: set[str] = set()
    duplicates = 0
    rows = 0

    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        for row in reader:
            rows += 1
            sample_id = row.get("sample_id", "")
            if sample_id in ids:
                duplicates += 1
            ids.add(sample_id)
            label = row.get("label", "")
            origin = row.get("data_origin", "")
            counts[(label, origin)] += 1
            obfuscation[(label, row.get("obfuscation_level", ""))] += 1
            categories[(label, row.get("category", ""))] += 1

    return {
        "path": str(path),
        "rows": rows,
        "columns": columns,
        "duplicate_sample_ids": duplicates,
        "label_origin": counts,
        "obfuscation": obfuscation,
        "categories": categories,
    }
