from __future__ import annotations

import argparse
from pathlib import Path

import nbformat


def markdown_source(lines: list[str]) -> str:
    out: list[str] = []
    for line in lines:
        if line.startswith("# "):
            out.append(line[2:])
        elif line.startswith("#"):
            out.append(line[1:])
        else:
            out.append(line)
    return "".join(out).strip()


def convert_one(py_path: Path, ipynb_path: Path) -> None:
    lines = py_path.read_text(encoding="utf-8").splitlines(keepends=True)
    cells = []
    current_kind = "code"
    current: list[str] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        if current_kind == "markdown":
            cells.append(nbformat.v4.new_markdown_cell(markdown_source(current)))
        else:
            cells.append(nbformat.v4.new_code_cell("".join(current).strip()))
        current = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# %%"):
            flush()
            current_kind = "markdown" if "[markdown]" in stripped else "code"
            continue
        current.append(line)
    flush()

    nb = nbformat.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "pygments_lexer": "ipython3",
        },
    }
    nbformat.write(nb, ipynb_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    for py_path in args.paths:
        if py_path.suffix != ".py":
            raise ValueError(f"Expected .py path: {py_path}")
        ipynb_path = Path("notebooks") / (py_path.stem + ".ipynb")
        convert_one(py_path, ipynb_path)
        print(f"[WRITE] {ipynb_path}")


if __name__ == "__main__":
    main()
