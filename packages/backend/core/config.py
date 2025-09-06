import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")

    MODEL_PROVIDER: str = "local"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VECTOR_PATH: str = "./var/vector"
    AUDIT_PATH: str = "./var/audit"
    MAX_PAYLOAD_BYTES: int = 1_500_000
    RATE_LIMIT_RPS: float = 5.0
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    ENABLE_HSTS: bool = False
    LOG_LEVEL: str = "INFO"
    METRICS_NAMESPACE: str = "codexia"
    RAG_TOPK_DEFAULT: int = 5
    W_DELTA: float = 0.5
    W_FEAS: float = 0.25
    W_URG: float = 0.15
    W_FIT: float = 0.10
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

    @property
    def allowed_origins(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]
