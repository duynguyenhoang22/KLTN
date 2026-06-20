from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from .taxonomy import allowed


REQUIRED_FIELDS = {
    "sample_id",
    "content",
    "label",
    "data_origin",
    "source",
    "message_domain",
    "sender_type",
    "surface_features",
    "target_audience",
    "obfuscation",
    "persuasion_tactics",
    "annotation",
}


def _unknown(values: Iterable[str], taxonomy_field: str) -> set[str]:
    return set(values) - allowed(taxonomy_field)


def validate_record(record: dict[str, object]) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        errors.append(f"missing fields: {sorted(missing)}")
        return errors

    if record["label"] not in {0, 1}:
        errors.append("label must be 0 or 1")
    if not str(record["sample_id"]).strip():
        errors.append("sample_id must not be empty")
    if not str(record["content"]).strip():
        errors.append("content must not be empty")

    for field in ("data_origin", "message_domain", "sender_type"):
        if record[field] not in allowed(field):
            errors.append(f"invalid {field}: {record[field]}")

    surface = record["surface_features"]
    if not isinstance(surface, dict):
        errors.append("surface_features must be an object")
    else:
        unknown = _unknown(surface.get("text_phenomena", []), "text_phenomena")
        if unknown:
            errors.append(f"invalid text_phenomena: {sorted(unknown)}")
        score = surface.get("text_noise_score")
        if not isinstance(score, int) or not 0 <= score <= 4:
            errors.append("text_noise_score must be an integer from 0 to 4")

    obfuscation = record["obfuscation"]
    if not isinstance(obfuscation, dict):
        errors.append("obfuscation must be an object")
    else:
        unknown = _unknown(
            obfuscation.get("techniques", []), "obfuscation_techniques"
        )
        if unknown:
            errors.append(f"invalid obfuscation techniques: {sorted(unknown)}")
        severity = obfuscation.get("severity")
        if not isinstance(severity, int) or not 0 <= severity <= 4:
            errors.append("obfuscation severity must be an integer from 0 to 4")
        if obfuscation.get("present") is False and severity != 0:
            errors.append("obfuscation severity must be 0 when present is false")

    unknown_tactics = _unknown(
        record["persuasion_tactics"], "persuasion_tactics"
    )
    if unknown_tactics:
        errors.append(f"invalid persuasion tactics: {sorted(unknown_tactics)}")

    annotation = record["annotation"]
    if not isinstance(annotation, dict):
        errors.append("annotation must be an object")
    elif annotation.get("status") not in allowed("annotation_status"):
        errors.append(f"invalid annotation status: {annotation.get('status')}")

    return errors


def validate_jsonl(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    rows = 0
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            rows += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
                continue
            if not isinstance(record, dict):
                errors.append(f"line {line_number}: record must be an object")
                continue
            sample_id = str(record.get("sample_id", ""))
            if sample_id in seen_ids:
                errors.append(f"line {line_number}: duplicate sample_id {sample_id}")
            seen_ids.add(sample_id)
            errors.extend(
                f"line {line_number}: {error}" for error in validate_record(record)
            )
    return rows, errors
