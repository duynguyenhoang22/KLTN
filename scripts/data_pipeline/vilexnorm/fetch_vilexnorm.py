"""Fetch ViLexNorm raw files.

This is a pipeline placeholder. Keep raw ViLexNorm files under
data/external/vilexnorm/raw/ and do not modify them in later steps.
"""

from pathlib import Path


RAW_DIR = Path("data/external/vilexnorm/raw")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Raw ViLexNorm directory: {RAW_DIR}")
    print("Download/fetch logic is intentionally not implemented yet.")


if __name__ == "__main__":
    main()
