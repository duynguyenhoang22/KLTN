from __future__ import annotations

import csv
from pathlib import Path

from .taxonomy import load_taxonomy


REVIEW_FIELDS = [
    "message_domain",
    "sender_type",
    "text_phenomena",
    "obfuscation_techniques",
    "persuasion_tactics",
    "requested_actions",
    "target_age_group",
    "target_gender",
    "target_roles",
]

DECISION_COLUMNS = [
    "decision",
    "proposed_value_or_target",
    "comment",
]


def write_taxonomy_review_sheet(output: Path, reviewer_id: str) -> int:
    taxonomy = load_taxonomy()
    existing: dict[tuple[str, str], dict[str, str]] = {}
    if output.exists():
        with output.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                existing[(row.get("field", ""), row.get("value", ""))] = row

    rows: list[dict[str, str]] = []
    item = 0
    for field in REVIEW_FIELDS:
        for value in taxonomy[field]:
            item += 1
            previous = existing.get((field, str(value)), {})
            rows.append({
                "item_order": str(item),
                "reviewer_id": reviewer_id,
                "taxonomy_version": str(taxonomy["version"]),
                "field": field,
                "value": str(value),
                "decision": previous.get("decision", ""),
                "proposed_value_or_target": previous.get(
                    "proposed_value_or_target", ""
                ),
                "comment": previous.get("comment", ""),
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "item_order",
        "reviewer_id",
        "taxonomy_version",
        "field",
        "value",
        *DECISION_COLUMNS,
    ]
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)
