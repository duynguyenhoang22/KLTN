"""Filter ViLexNorm rows into clean, hard-negative and rejected candidates."""

from pathlib import Path


IN_FILE = Path("data/external/vilexnorm/processed/vilexnorm_all.csv")
OUT_DIR = Path("data/external/vilexnorm/processed")
RULES_DOC = Path("data/external/vilexnorm/docs/ViSmishDS_ViLexNorm_Filtering_Rules.md")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Input file: {IN_FILE}")
    print(f"Rules: {RULES_DOC}")
    print("Filtering logic is intentionally not implemented yet.")


if __name__ == "__main__":
    main()
