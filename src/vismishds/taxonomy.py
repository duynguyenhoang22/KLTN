from __future__ import annotations

import json
from functools import lru_cache

from .paths import SCHEMA_PATH, TAXONOMY_PATH


@lru_cache(maxsize=1)
def load_taxonomy() -> dict[str, object]:
    with TAXONOMY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def allowed(field: str) -> set[str]:
    values = load_taxonomy().get(field)
    if not isinstance(values, list):
        raise KeyError(f"Unknown taxonomy field: {field}")
    return {str(value) for value in values}


def audit_taxonomy_schema_contract() -> list[str]:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        schema = json.load(handle)

    properties = schema["properties"]
    schema_values = {
        "data_origin": properties["data_origin"]["enum"],
        "message_domain": properties["message_domain"]["enum"],
        "sender_type": properties["sender_type"]["enum"],
        "text_phenomena": (
            properties["surface_features"]["properties"]["text_phenomena"]
            ["items"]["enum"]
        ),
        "target_age_group": (
            properties["target_audience"]["properties"]["age_groups"]
            ["items"]["enum"]
        ),
        "target_gender": (
            properties["target_audience"]["properties"]["gender"]["enum"]
        ),
        "target_roles": (
            properties["target_audience"]["properties"]["roles"]["items"]["enum"]
        ),
        "obfuscation_techniques": (
            properties["obfuscation"]["properties"]["techniques"]
            ["items"]["enum"]
        ),
        "persuasion_tactics": (
            properties["persuasion_tactics"]["items"]["enum"]
        ),
        "requested_actions": (
            properties["requested_actions"]["properties"]["types"]["items"]["enum"]
        ),
        "annotation_status": (
            properties["annotation"]["properties"]["status"]["enum"]
        ),
    }

    errors: list[str] = []
    taxonomy = load_taxonomy()
    for field, schema_enum in schema_values.items():
        taxonomy_values = taxonomy.get(field)
        if taxonomy_values != schema_enum:
            errors.append(
                f"{field}: taxonomy and schema enum differ "
                f"(taxonomy={taxonomy_values}, schema={schema_enum})"
            )

    forbidden_fragments = {"fake", "legitimate", "scam", "real"}
    exempt_fields = {"data_origin"}
    for field, values in taxonomy.items():
        if field in {"version", "scope_version", "status"} or field in exempt_fields:
            continue
        if not isinstance(values, list):
            continue
        for value in values:
            tokens = set(str(value).lower().replace("-", "_").split("_"))
            forbidden = tokens & forbidden_fragments
            if forbidden:
                errors.append(
                    f"{field}.{value}: label-revealing token(s) {sorted(forbidden)}"
                )
    return errors
