from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_provider: str = "local"
    vector_path: str = "./var/vector"
    audit_path: str = "./var/audit"
    log_level: str = "INFO"


settings = Settings()
