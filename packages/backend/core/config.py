import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")

    MODEL_PROVIDER: str = "local"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_PATH: str = "./var/vector"
    AUDIT_PATH: str = "./var/audit"
    LOG_LEVEL: str = "INFO"
    RAG_TOPK_DEFAULT: int = 5
    RISK_WEIGHTS: dict = {
        "modifier_missing": 0.35,
        "dx_unspecific": 0.20,
        "doc_missing": 0.25,
        "dx_incompatibility": 0.30,
        "lines": 0.10,
    }

    def model_post_init(self, __context):
        os.makedirs(self.VECTOR_PATH, exist_ok=True)
        os.makedirs(self.AUDIT_PATH, exist_ok=True)
