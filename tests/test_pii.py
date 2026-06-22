from vismishds.pii import mask_pii


def test_mask_pii_masks_phone_and_email_but_preserves_url() -> None:
    result = mask_pii(
        "Lien he 0987654321, email test@example.com, vao https://example.com"
    )
    assert "<PHONE_1>" in result.text
    assert "<EMAIL_1>" in result.text
    assert "https://example.com" in result.text
