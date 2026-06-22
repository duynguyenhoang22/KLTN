from __future__ import annotations

from typing import Any

from .taxonomy import load_taxonomy


def metadata_output_schema() -> dict[str, Any]:
    taxonomy = load_taxonomy()

    def enum_array(field: str, minimum: int = 0) -> dict[str, Any]:
        return {
            "type": "array",
            "items": {"type": "string", "enum": taxonomy[field]},
            "uniqueItems": True,
            "minItems": minimum,
        }

    confidence = {"type": "number", "minimum": 0, "maximum": 1}
    evidence = {
        "type": "array",
        "items": {"type": "string"},
        "uniqueItems": True,
    }
    item = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "sample_id",
            "message_domain",
            "surface_features",
            "target_audience",
            "obfuscation",
            "persuasion_tactics",
            "requested_actions",
            "field_confidence",
            "review_flags",
        ],
        "properties": {
            "sample_id": {"type": "string"},
            "message_domain": {
                "type": "string",
                "enum": taxonomy["message_domain"],
            },
            "surface_features": {
                "type": "object",
                "additionalProperties": False,
                "required": ["text_phenomena", "text_noise_score"],
                "properties": {
                    "text_phenomena": enum_array("text_phenomena", 1),
                    "text_noise_score": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 4,
                    },
                },
            },
            "target_audience": {
                "type": "object",
                "additionalProperties": False,
                "required": ["age_groups", "gender", "roles", "evidence"],
                "properties": {
                    "age_groups": enum_array("target_age_group", 1),
                    "gender": {
                        "type": "string",
                        "enum": taxonomy["target_gender"],
                    },
                    "roles": enum_array("target_roles", 1),
                    "evidence": evidence,
                },
            },
            "obfuscation": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "present", "techniques", "severity", "confidence"
                ],
                "properties": {
                    "present": {"type": "boolean"},
                    "techniques": enum_array("obfuscation_techniques"),
                    "severity": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 4,
                    },
                    "confidence": confidence,
                },
            },
            "persuasion_tactics": enum_array("persuasion_tactics", 1),
            "requested_actions": {
                "type": "object",
                "additionalProperties": False,
                "required": ["types", "evidence"],
                "properties": {
                    "types": enum_array("requested_actions", 1),
                    "evidence": evidence,
                },
            },
            "field_confidence": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "message_domain", "surface_features", "target_audience",
                    "obfuscation", "persuasion_tactics", "requested_actions"
                ],
                "properties": {
                    "message_domain": confidence,
                    "surface_features": confidence,
                    "target_audience": confidence,
                    "obfuscation": confidence,
                    "persuasion_tactics": confidence,
                    "requested_actions": confidence,
                },
            },
            "review_flags": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "low_confidence",
                        "ambiguous_domain",
                        "target_inference_risk",
                        "obfuscation_intent_uncertain",
                        "unreadable_content",
                        "taxonomy_gap",
                    ],
                },
                "uniqueItems": True,
            },
        },
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["items"],
        "properties": {
            "items": {
                "type": "array",
                "items": item,
                "minItems": 1,
            }
        },
    }


def validate_metadata_item(item: dict[str, Any]) -> list[str]:
    taxonomy = load_taxonomy()
    errors: list[str] = []

    def enum_values(field: str, values: list[str]) -> None:
        unknown = set(values) - set(taxonomy[field])
        if unknown:
            errors.append(f"{field}: invalid values {sorted(unknown)}")

    if item.get("message_domain") not in taxonomy["message_domain"]:
        errors.append(f"message_domain: invalid value {item.get('message_domain')!r}")

    surface = item.get("surface_features")
    if not isinstance(surface, dict):
        errors.append("surface_features must be an object")
    else:
        pheno = surface.get("text_phenomena", [])
        enum_values("text_phenomena", pheno)
        if "none" in pheno and len(pheno) > 1:
            errors.append("text phenomena sentinel 'none' must be exclusive")
        score = surface.get("text_noise_score")
        if not isinstance(score, int) or not 0 <= score <= 4:
            errors.append("text_noise_score must be an integer from 0 to 4")

    target = item.get("target_audience")
    if not isinstance(target, dict):
        errors.append("target_audience must be an object")
    else:
        ages = target.get("age_groups", [])
        roles = target.get("roles", [])
        gender = target.get("gender")
        enum_values("target_age_group", ages)
        enum_values("target_roles", roles)
        if gender not in taxonomy["target_gender"]:
            errors.append(f"target_gender: invalid value {gender!r}")
        if len(set(ages) & {"general", "unknown", "not_applicable"}) and len(ages) > 1:
            errors.append("target age sentinel must be exclusive")
        if len(set(roles) & {"general_public", "unknown", "not_applicable"}) and len(roles) > 1:
            errors.append("target role sentinel must be exclusive")
        specific = (
            set(ages) - {"general", "unknown", "not_applicable"}
            or set(roles) - {"general_public", "unknown", "not_applicable"}
            or gender not in {"all", "unknown", "not_applicable"}
        )
        if specific and not target.get("evidence", []):
            errors.append("specific target audience requires evidence")

    obfuscation = item.get("obfuscation")
    if not isinstance(obfuscation, dict):
        errors.append("obfuscation must be an object")
    else:
        techniques = obfuscation.get("techniques", [])
        enum_values("obfuscation_techniques", techniques)
        present = obfuscation.get("present")
        severity = obfuscation.get("severity")
        confidence = obfuscation.get("confidence")
        if present is False and (techniques or severity != 0):
            errors.append(
                "obfuscation false requires empty techniques and severity 0"
            )
        if present is True and (not techniques or not isinstance(severity, int) or severity < 1):
            errors.append(
                "obfuscation true requires techniques and severity greater than 0"
            )
        if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
            errors.append("obfuscation confidence must be from 0 to 1")

    tactics = item.get("persuasion_tactics", [])
    enum_values("persuasion_tactics", tactics)
    if "none" in tactics and len(tactics) > 1:
        errors.append("persuasion tactics sentinel 'none' must be exclusive")

    requested = item.get("requested_actions")
    if not isinstance(requested, dict):
        errors.append("requested_actions must be an object")
    else:
        actions = requested.get("types", [])
        enum_values("requested_actions", actions)
        if set(actions) & {"none", "unclear"} and len(actions) > 1:
            errors.append("requested action sentinel must be exclusive")
        if set(actions) - {"none", "unclear"} and not requested.get("evidence", []):
            errors.append("specific requested action requires evidence")

    confidences = item.get("field_confidence")
    required_confidences = {
        "message_domain", "surface_features", "target_audience",
        "obfuscation", "persuasion_tactics", "requested_actions",
    }
    if not isinstance(confidences, dict):
        errors.append("field_confidence must be an object")
    else:
        if set(confidences) != required_confidences:
            errors.append("field_confidence keys do not match required fields")
        for field, value in confidences.items():
            if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                errors.append(f"field_confidence.{field} must be from 0 to 1")

    return errors
