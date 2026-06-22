from __future__ import annotations

import os
from pathlib import Path

from .paths import PROJECT_ROOT


def load_dotenv(
    path: Path | None = None,
    *,
    override: bool = False,
) -> int:
    """Load simple KEY=VALUE pairs from .env into the current process."""
    env_path = path or (PROJECT_ROOT / ".env")
    if not env_path.exists():
        return 0

    loaded = 0
    with env_path.open(encoding="utf-8-sig") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].lstrip()
            if "=" not in line:
                raise ValueError(
                    f"{env_path}:{line_number}: expected KEY=VALUE"
                )

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if not key or not key.replace("_", "a").isalnum() or key[0].isdigit():
                raise ValueError(
                    f"{env_path}:{line_number}: invalid environment variable name"
                )
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]

            if override or key not in os.environ:
                os.environ[key] = value
                loaded += 1
    return loaded
