from __future__ import annotations

import json
from functools import lru_cache

from .paths import TAXONOMY_PATH


@lru_cache(maxsize=1)
def load_taxonomy() -> dict[str, object]:
    with TAXONOMY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def allowed(field: str) -> set[str]:
    values = load_taxonomy().get(field)
    if not isinstance(values, list):
        raise KeyError(f"Unknown taxonomy field: {field}")
    return {str(value) for value in values}
