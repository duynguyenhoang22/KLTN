from vismishds.metadata_pipeline import (
    PreparedRecord,
    build_request_preview,
    validate_batch_response,
    sanitize_response_items,
)


def sample_record() -> PreparedRecord:
    return PreparedRecord(
        sample_id="x1",
        content="Vui long truy cap https://example.com",
        masked_content="Vui long truy cap https://example.com",
        label=1,
        data_origin="real",
        sender_type="personal_number",
        source_dataset="test",
        source_file="test.csv",
        source_row_id="1",
        masking={},
    )


def test_preview_contains_model_taxonomy_and_masked_content() -> None:
    preview = build_request_preview(
        [sample_record()],
        {
            "model": "mistral-small-2506",
            "prompt_version": "test",
        },
    )
    assert preview["model"] == "mistral-small-2506"
    assert preview["sample_ids"] == ["x1"]
    assert "https://example.com" in preview["user_prompt"]
    assert "ALLOWED_ENUMS" in preview["system_prompt"]


def test_response_validation_checks_ids() -> None:
    valid = {
        "items": [{
            "sample_id": "x1",
            "message_domain": "telecom",
            "surface_features": {
                "text_phenomena": ["none"],
                "text_noise_score": 0,
            },
            "target_audience": {
                "age_groups": ["general"],
                "gender": "all",
                "roles": ["general_public"],
                "evidence": [],
            },
            "obfuscation": {
                "present": False,
                "techniques": [],
                "severity": 0,
                "confidence": 0.9,
            },
            "persuasion_tactics": ["none"],
            "requested_actions": {
                "types": ["click_or_visit_link"],
                "evidence": ["truy cap"],
            },
            "field_confidence": {
                "message_domain": 0.9,
                "surface_features": 0.9,
                "target_audience": 0.8,
                "obfuscation": 0.7,
                "persuasion_tactics": 0.8,
                "requested_actions": 0.9,
            },
            "review_flags": [],
        }]
    }
    assert validate_batch_response(valid, ["x1"]) == []
    errors = validate_batch_response(valid, ["x2"])
    assert any("sample_id mismatch" in error for error in errors)


def test_sanitize_response_items() -> None:
    invalid = {
        "items": [{
            "sample_id": "x1",
            "message_domain": "invalid_domain",
            "surface_features": {
                "text_phenomena": ["invalid_pheno"],
                "text_noise_score": 10,
            },
            "target_audience": {
                "age_groups": ["adolescent"],  # specific, requires evidence
                "gender": "all",
                "roles": ["parent"],  # invalid role
                "evidence": [],
            },
            "obfuscation": {
                "present": True,
                "techniques": [],
                "severity": 0,
                "confidence": 1.5,
            },
            "persuasion_tactics": ["none", "urgency"],  # none must be exclusive
            "requested_actions": {
                "types": ["click_or_visit_link"],
                "evidence": [],  # specific, requires evidence
            },
            "field_confidence": {},
        }]
    }
    
    batch = [sample_record()]
    sanitize_response_items(invalid, batch)
    
    item = invalid["items"][0]
    assert item["message_domain"] == "other"
    assert item["surface_features"]["text_phenomena"] == ["none"]
    assert item["surface_features"]["text_noise_score"] == 0
    assert item["target_audience"]["roles"] == ["other"]
    assert len(item["target_audience"]["evidence"]) > 0
    assert item["obfuscation"]["present"] is False
    assert item["obfuscation"]["techniques"] == []
    assert item["obfuscation"]["severity"] == 0
    assert item["obfuscation"]["confidence"] == 0.5
    assert item["persuasion_tactics"] == ["urgency"]
    assert item["requested_actions"]["types"] == ["click_or_visit_link"]
    assert len(item["requested_actions"]["evidence"]) > 0
    assert "message_domain" in item["field_confidence"]

