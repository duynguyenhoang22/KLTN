"""Select synthetic label-0 rows to remove before adding ViLexNorm rows."""

from pathlib import Path


IN_FILE = Path("data/final/vismishds_phase1_final.csv")
OUT_DIR = Path("data/interim/vilexnorm_integration")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Input dataset: {IN_FILE}")
    print(f"Output directory: {OUT_DIR}")
    print("Selection logic is intentionally not implemented yet.")


if __name__ == "__main__":
    main()
