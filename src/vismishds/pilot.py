from __future__ import annotations

import csv
import random
from collections import defaultdict
from pathlib import Path


ANNOTATION_COLUMNS = [
    "message_domain_v2",
    "target_age_groups",
    "target_gender",
    "target_occupations",
    "target_life_statuses",
    "target_evidence",
    "text_phenomena",
    "text_noise_score",
    "obfuscation_present",
    "obfuscation_techniques",
    "obfuscation_severity",
    "persuasion_tactics",
    "annotation_confidence",
    "annotator_id",
    "review_notes",
]


def create_pilot(
    source: Path,
    output: Path,
    size: int,
    seed: int,
) -> dict[str, int]:
    if size < 4:
        raise ValueError("Pilot size must be at least 4")

    strata: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            strata[(row["label"], row["data_origin"])].append(row)

    if not strata:
        raise ValueError("Reference dataset is empty")

    rng = random.Random(seed)
    base, remainder = divmod(size, len(strata))
    selected: list[dict[str, str]] = []
    counts: dict[str, int] = {}

    for index, key in enumerate(sorted(strata)):
        target = base + (1 if index < remainder else 0)
        available = strata[key]
        if target > len(available):
            raise ValueError(f"Not enough rows in stratum {key}: {len(available)}")
        sampled = rng.sample(available, target)
        selected.extend(sampled)
        counts[f"label={key[0]},origin={key[1]}"] = len(sampled)

    rng.shuffle(selected)
    output.parent.mkdir(parents=True, exist_ok=True)
    base_columns = [
        "sample_id",
        "content",
        "label",
        "data_origin",
        "source_dataset",
        "source_file",
        "source_row_id",
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base_columns + ANNOTATION_COLUMNS)
        writer.writeheader()
        for row in selected:
            writer.writerow({column: row.get(column, "") for column in base_columns})
    return counts
