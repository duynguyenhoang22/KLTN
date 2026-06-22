from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any

import httpx

from .metadata_contract import metadata_output_schema


@dataclass(frozen=True)
class MistralConfig:
    api_key: str
    base_url: str
    model: str
    temperature: float
    timeout_seconds: float
    max_retries: int
    minimum_request_interval_seconds: float


def config_from_environment(settings: dict[str, Any]) -> MistralConfig:
    api_key = os.getenv("MISTRAL_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is not configured")
    return MistralConfig(
        api_key=api_key,
        base_url=os.getenv(
            "MISTRAL_BASE_URL", str(settings["base_url"])
        ).rstrip("/"),
        model=os.getenv(
            "MISTRAL_METADATA_MODEL", str(settings["model"])
        ),
        temperature=float(settings["temperature"]),
        timeout_seconds=float(settings["request_timeout_seconds"]),
        max_retries=int(settings["max_retries"]),
        minimum_request_interval_seconds=float(
            settings["minimum_request_interval_seconds"]
        ),
    )


class MistralMetadataClient:
    def __init__(self, config: MistralConfig) -> None:
        self.config = config
        self._last_request_started = 0.0
        self._client = httpx.Client(
            base_url=config.base_url,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=config.timeout_seconds,
        )

    def close(self) -> None:
        self._client.close()

    def annotate(self, system_prompt: str, user_prompt: str) -> tuple[dict[str, Any], dict[str, Any]]:
        payload = {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
        }
        last_error: Exception | None = None
        for attempt in range(1, self.config.max_retries + 1):
            elapsed = time.monotonic() - self._last_request_started
            wait = self.config.minimum_request_interval_seconds - elapsed
            if wait > 0:
                time.sleep(wait)
            self._last_request_started = time.monotonic()
            try:
                response = self._client.post("/chat/completions", json=payload)
                response.raise_for_status()
                raw = response.json()
                content = raw["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                return parsed, raw
            except (httpx.HTTPError, KeyError, IndexError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt < self.config.max_retries:
                    time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(
            f"Mistral metadata request failed after "
            f"{self.config.max_retries} attempts"
        ) from last_error


def request_contract() -> dict[str, Any]:
    return metadata_output_schema()
