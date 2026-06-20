from vismishds.validation import validate_record


def valid_record() -> dict[str, object]:
    return {
        "sample_id": "v2_000001",
        "content": "Thông báo thử nghiệm.",
        "label": 0,
        "data_origin": "real",
        "source": {
            "dataset": "real_label_0",
            "file": "dataset_label_0.csv",
            "record_id": "1",
        },
        "message_domain": "telecom",
        "sender_type": "brandname",
        "surface_features": {
            "has_url": False,
            "has_phone_number": False,
            "text_phenomena": [],
            "text_noise_score": 0,
        },
        "target_audience": {
            "age_groups": ["general"],
            "gender": "all",
            "occupations": [],
            "life_statuses": [],
            "evidence": [],
        },
        "obfuscation": {
            "present": False,
            "techniques": [],
            "severity": 0,
            "confidence": 1.0,
        },
        "persuasion_tactics": [],
        "annotation": {
            "status": "human_reviewed",
            "annotators": ["ann01"],
            "confidence": 0.95,
            "guideline_version": "2.0.0-draft",
            "notes": None,
        },
    }


def test_valid_record_has_no_errors() -> None:
    assert validate_record(valid_record()) == []


def test_obfuscation_invariant() -> None:
    record = valid_record()
    record["obfuscation"]["severity"] = 2
    assert "obfuscation severity must be 0 when present is false" in validate_record(record)


def test_label_and_taxonomy_are_checked() -> None:
    record = valid_record()
    record["label"] = 3
    record["message_domain"] = "fake_bank"
    errors = validate_record(record)
    assert "label must be 0 or 1" in errors
    assert "invalid message_domain: fake_bank" in errors
