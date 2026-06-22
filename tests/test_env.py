import os
from pathlib import Path

from vismishds.env import load_dotenv


def test_load_dotenv_supports_comments_quotes_and_export(
    tmp_path: Path,
    monkeypatch,
) -> None:
    path = tmp_path / ".env"
    path.write_text(
        "# comment\n"
        "MISTRAL_TEST_A=plain\n"
        "MISTRAL_TEST_B=\"quoted value\"\n"
        "export MISTRAL_TEST_C='exported'\n",
        encoding="utf-8",
    )
    for key in ("MISTRAL_TEST_A", "MISTRAL_TEST_B", "MISTRAL_TEST_C"):
        monkeypatch.delenv(key, raising=False)

    assert load_dotenv(path) == 3
    assert os.environ["MISTRAL_TEST_A"] == "plain"
    assert os.environ["MISTRAL_TEST_B"] == "quoted value"
    assert os.environ["MISTRAL_TEST_C"] == "exported"


def test_load_dotenv_does_not_override_existing_value(
    tmp_path: Path,
    monkeypatch,
) -> None:
    path = tmp_path / ".env"
    path.write_text("MISTRAL_TEST_KEEP=from_file\n", encoding="utf-8")
    monkeypatch.setenv("MISTRAL_TEST_KEEP", "from_process")

    assert load_dotenv(path) == 0
    assert os.environ["MISTRAL_TEST_KEEP"] == "from_process"
