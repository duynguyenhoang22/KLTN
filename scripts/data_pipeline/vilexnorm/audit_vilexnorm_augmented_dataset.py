"""Audit the ViLexNorm-augmented VISmishDS candidate dataset."""

from pathlib import Path


IN_FILE = Path("data/final/vismishds_phase1_vilexnorm_augmented.csv")
OUT_REPORT = Path("data/external/vilexnorm/docs/ViSmishDS_ViLexNorm_Integration_Report.md")


def main() -> None:
    print(f"Input dataset: {IN_FILE}")
    print(f"Report target: {OUT_REPORT}")
    print("Audit logic is intentionally not implemented yet.")


if __name__ == "__main__":
    main()
