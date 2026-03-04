# server/providers/__init__.py
from ..config import Settings
from .base import BaseProvider
from .gemini import GeminiProvider

def get_provider(settings: Settings) -> BaseProvider:
    name = (settings.provider or "").lower()
    if name == "gemini":
        return GeminiProvider(settings)
    raise ValueError(f"Unknown provider: {settings.provider}")