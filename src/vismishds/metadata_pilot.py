from __future__ import annotations

import csv
import hashlib
import random
from collections import defaultdict
from pathlib import Path


HUMAN_METADATA_COLUMNS = [
    "message_domain",
    "text_phenomena",
    "text_noise_score",
    "target_age_groups",
    "target_gender",
    "target_roles",
    "target_evidence",
    "obfuscation_present",
    "obfuscation_techniques",
    "obfuscation_severity",
    "obfuscation_confidence",
    "persuasion_tactics",
    "requested_actions",
    "requested_action_evidence",
    "overall_confidence",
    "review_notes",
]

PILOT_BUCKETS = [
    "has_url",
    "no_url",
    "short",
    "long",
    "nonstandard",
]


def _stable_rank(sample_id: str, seed: int, bucket: str) -> str:
    return hashlib.sha256(
        f"{seed}|{bucket}|{sample_id}".encode("utf-8")
    ).hexdigest()


def _candidate_buckets(row: dict[str, str]) -> list[str]:
    content = row.get("content", "")
    buckets = ["has_url" if row.get("has_url") == "1" else "no_url"]
    if len(content) <= 80:
        buckets.append("short")
    if len(content) > 240:
        buckets.append("long")
    if row.get("obfuscation_level", "") not in {
        "", "NONE", "LEVEL 0 – Không obfuscation (formal)"
    }:
        buckets.append("nonstandard")
    return buckets


def select_metadata_pilot(
    source: Path,
    size: int = 100,
    seed: int = 20260622,
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    if size % 4:
        raise ValueError("metadata pilot size must be divisible by 4")

    strata: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    with source.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            row["_pilot_buckets"] = "|".join(_candidate_buckets(row))
            strata[(row["label"], row["data_origin"])].append(row)

    required_strata = {
        ("0", "real"),
        ("0", "synthetic"),
        ("1", "real"),
        ("1", "synthetic"),
    }
    if set(strata) != required_strata:
        missing = required_strata - set(strata)
        if missing:
            raise ValueError(f"missing pilot strata: {sorted(missing)}")

    per_stratum = size // 4
    selected: list[dict[str, str]] = []
    internal: list[dict[str, str]] = []
    counts: dict[str, int] = {}

    for stratum in sorted(required_strata):
        candidates = strata[stratum]
        chosen_ids: set[str] = set()
        chosen: list[dict[str, str]] = []
        bucket_quota = max(1, per_stratum // len(PILOT_BUCKETS))

        for bucket in PILOT_BUCKETS:
            available = [
                row for row in candidates
                if bucket in row["_pilot_buckets"].split("|")
                and row["sample_id"] not in chosen_ids
            ]
            available.sort(
                key=lambda row: _stable_rank(
                    row["sample_id"], seed, f"{stratum}-{bucket}"
                )
            )
            for row in available[:bucket_quota]:
                chosen.append(row)
                chosen_ids.add(row["sample_id"])

        if len(chosen) < per_stratum:
            remaining = [
                row for row in candidates if row["sample_id"] not in chosen_ids
            ]
            remaining.sort(
                key=lambda row: _stable_rank(
                    row["sample_id"], seed, f"{stratum}-fill"
                )
            )
            chosen.extend(remaining[: per_stratum - len(chosen)])

        if len(chosen) != per_stratum:
            raise ValueError(
                f"could not select {per_stratum} rows for stratum {stratum}"
            )

        counts[f"label={stratum[0]},origin={stratum[1]}"] = len(chosen)
        for row in chosen:
            selected.append({
                "sample_id": row["sample_id"],
                "content": row["content"],
            })
            internal.append({
                "sample_id": row["sample_id"],
                "label": row["label"],
                "data_origin": row["data_origin"],
                "has_url": row.get("has_url", ""),
                "content_length": str(len(row["content"])),
                "legacy_category": row.get("category", ""),
                "legacy_obfuscation_level": row.get("obfuscation_level", ""),
                "pilot_buckets": row["_pilot_buckets"],
            })
    return selected, internal, counts


def write_metadata_pilot(
    selected: list[dict[str, str]],
    internal: list[dict[str, str]],
    reviewer_outputs: dict[str, Path],
    manifest_output: Path,
    internal_output: Path,
    seed: int,
) -> None:
    manifest_output.parent.mkdir(parents=True, exist_ok=True)
    with manifest_output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sample_id"])
        writer.writeheader()
        writer.writerows({"sample_id": row["sample_id"]} for row in selected)

    internal_output.parent.mkdir(parents=True, exist_ok=True)
    with internal_output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(internal[0]))
        writer.writeheader()
        writer.writerows(internal)

    fields = ["item_order", "sample_id", "content", *HUMAN_METADATA_COLUMNS]
    for index, (reviewer, output) in enumerate(sorted(reviewer_outputs.items())):
        rows = [dict(row) for row in selected]
        random.Random(seed + index + 1).shuffle(rows)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            for item_order, row in enumerate(rows, start=1):
                writer.writerow({
                    "item_order": item_order,
                    "sample_id": row["sample_id"],
                    "content": row["content"],
                })


def read_manifest_ids(path: Path) -> list[str]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return [row["sample_id"] for row in csv.DictReader(handle)]
