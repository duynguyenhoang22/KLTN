from vismishds.taxonomy import audit_taxonomy_schema_contract


def test_taxonomy_and_schema_stay_synchronized() -> None:
    assert audit_taxonomy_schema_contract() == []
