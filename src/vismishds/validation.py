from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from .taxonomy import allowed, load_taxonomy


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
    "requested_actions",
    "annotation",
}


def _unknown(values: Iterable[str], taxonomy_field: str) -> set[str]:
    return set(values) - allowed(taxonomy_field)


def _check_exclusive_sentinels(
    values: Iterable[str],
    field: str,
    sentinels: set[str],
) -> list[str]:
    selected = set(values)
    active = selected & sentinels
    if active and len(selected) > 1:
        return [
            f"{field} sentinel values {sorted(active)} must not be combined "
            "with other values"
        ]
    if len(active) > 1:
        return [f"{field} must not contain multiple sentinel values"]
    return []


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

    data_origin = record["data_origin"]
    sender_type = record["sender_type"]
    if data_origin == "real" and sender_type == "not_applicable":
        errors.append(
            "real records require a human-verified sender_type"
        )
    if data_origin != "real" and sender_type != "not_applicable":
        errors.append(
            "non-real records must use sender_type=not_applicable"
        )

    surface = record["surface_features"]
    if not isinstance(surface, dict):
        errors.append("surface_features must be an object")
    else:
        phenomena = surface.get("text_phenomena", [])
        unknown = _unknown(phenomena, "text_phenomena")
        if unknown:
            errors.append(f"invalid text_phenomena: {sorted(unknown)}")
        if not phenomena:
            errors.append("text_phenomena must contain at least one value (use 'none' if empty)")
        else:
            errors.extend(
                _check_exclusive_sentinels(
                    phenomena,
                    "text phenomena",
                    {"none"},
                )
            )
        score = surface.get("text_noise_score")
        if not isinstance(score, int) or not 0 <= score <= 4:
            errors.append("text_noise_score must be an integer from 0 to 4")

    target = record["target_audience"]
    if not isinstance(target, dict):
        errors.append("target_audience must be an object")
    else:
        age_groups = target.get("age_groups", [])
        roles = target.get("roles", [])
        gender = target.get("gender")
        unknown_age = _unknown(age_groups, "target_age_group")
        unknown_roles = _unknown(roles, "target_roles")
        if unknown_age:
            errors.append(f"invalid target age groups: {sorted(unknown_age)}")
        if gender not in allowed("target_gender"):
            errors.append(f"invalid target gender: {gender}")
        if unknown_roles:
            errors.append(f"invalid target roles: {sorted(unknown_roles)}")
        errors.extend(
            _check_exclusive_sentinels(
                age_groups,
                "target age_groups",
                {"general", "unknown", "not_applicable"},
            )
        )
        errors.extend(
            _check_exclusive_sentinels(
                roles,
                "target roles",
                {"general_public", "unknown", "not_applicable"},
            )
        )
        specific_age = set(age_groups) - {"general", "unknown", "not_applicable"}
        specific_roles = set(roles) - {
            "general_public", "unknown", "not_applicable"
        }
        specific_gender = gender not in {"all", "unknown"}
        if (specific_age or specific_roles or specific_gender) and not target.get(
            "evidence", []
        ):
            errors.append(
                "specific target audience values require at least one evidence span"
            )

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
        present = obfuscation.get("present")
        techniques = obfuscation.get("techniques", [])
        if present is False:
            if severity != 0:
                errors.append("obfuscation severity must be 0 when present is false")
            if techniques:
                errors.append(
                    "obfuscation techniques must be empty when present is false"
                )
        if present is True:
            if severity == 0:
                errors.append(
                    "obfuscation severity must be greater than 0 when present is true"
                )
            if not techniques:
                errors.append(
                    "obfuscation techniques must not be empty when present is true"
                )

    tactics = record["persuasion_tactics"]
    unknown_tactics = _unknown(tactics, "persuasion_tactics")
    if unknown_tactics:
        errors.append(f"invalid persuasion tactics: {sorted(unknown_tactics)}")
    if not tactics:
        errors.append("persuasion_tactics must contain at least one value (use 'none' if empty)")
    else:
        errors.extend(
            _check_exclusive_sentinels(
                tactics,
                "persuasion tactics",
                {"none"},
            )
        )

    requested = record["requested_actions"]
    if not isinstance(requested, dict):
        errors.append("requested_actions must be an object")
    else:
        action_types = requested.get("types", [])
        unknown_actions = _unknown(action_types, "requested_actions")
        if unknown_actions:
            errors.append(f"invalid requested actions: {sorted(unknown_actions)}")
        errors.extend(
            _check_exclusive_sentinels(
                action_types, "requested action types", {"none", "unclear"}
            )
        )
        actionable = set(action_types) - {"none", "unclear"}
        if actionable and not requested.get("evidence", []):
            errors.append(
                "actionable requested actions require at least one evidence span"
            )

    annotation = record["annotation"]
    if not isinstance(annotation, dict):
        errors.append("annotation must be an object")
    elif annotation.get("status") not in allowed("annotation_status"):
        errors.append(f"invalid annotation status: {annotation.get('status')}")
    elif annotation.get("taxonomy_version") != load_taxonomy()["version"]:
        errors.append(
            "annotation taxonomy_version must match the active taxonomy version"
        )

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
