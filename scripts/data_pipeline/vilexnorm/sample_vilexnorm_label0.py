"""Sample curated ViLexNorm label-0 rows for VISmishDS integration."""

from pathlib import Path


CURATED_DIR = Path("data/external/vilexnorm/curated")
OUT_FILE = Path("data/interim/vilexnorm_integration/label0_vilexnorm_replacement_pool.csv")


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Curated input directory: {CURATED_DIR}")
    print(f"Output file: {OUT_FILE}")
    print("Sampling logic is intentionally not implemented yet.")


if __name__ == "__main__":
    main()
