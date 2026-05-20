"""Build the ViLexNorm-augmented VISmishDS candidate dataset."""

from pathlib import Path


BASE_DATASET = Path("data/final/vismishds_phase1_final.csv")
REPLACEMENT_POOL = Path("data/interim/vilexnorm_integration/label0_vilexnorm_replacement_pool.csv")
OUT_FILE = Path("data/final/vismishds_phase1_vilexnorm_augmented.csv")


def main() -> None:
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Base dataset: {BASE_DATASET}")
    print(f"Replacement pool: {REPLACEMENT_POOL}")
    print(f"Output dataset: {OUT_FILE}")
    print("Build logic is intentionally not implemented yet.")


if __name__ == "__main__":
    main()
