# server/config.py
import os
from pydantic import BaseModel, Field, ConfigDict

class Settings(BaseModel):
    model_config = ConfigDict(extra="ignore")

    # provider selector
    provider: str = Field(default_factory=lambda: os.getenv("PROVIDER", "gemini"))

    # gemini
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite-preview"))
    gemini_timeout_sec: int = Field(default_factory=lambda: int(os.getenv("GEMINI_TIMEOUT_SEC", "60")))

    # api constraints
    max_file_mb: int = Field(default_factory=lambda: int(os.getenv("MAX_FILE_MB", "100")))

def load_settings() -> Settings:
    return Settings()