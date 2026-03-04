# server/providers/gemini.py
import base64
import requests
from typing import Any, Dict

from ..config import Settings
from .base import BaseProvider

class GeminiProvider(BaseProvider):
    def __init__(self, settings: Settings):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.settings = settings
        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{settings.gemini_model}:generateContent?key={settings.gemini_api_key}"
        )

    def generate(self, *, file_bytes: bytes, mime_type: str, prompt: str) -> str:
        encoded = base64.b64encode(file_bytes).decode("utf-8")

        payload: Dict[str, Any] = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime_type, "data": encoded}},
                ]
            }]
        }

        r = requests.post(self.url, json=payload, timeout=self.settings.gemini_timeout_sec)
        r.raise_for_status()
        data = r.json()

        candidates = data.get("candidates", [])
        if not candidates:
            raise ValueError(f"Gemini returned no candidates: {data}")

        parts = candidates[0].get("content", {}).get("parts", [])
        if not parts or "text" not in parts[0]:
            raise ValueError(f"Gemini returned unexpected shape: {data}")

        return parts[0]["text"]