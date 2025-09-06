import logging
import re
from datetime import datetime
from pythonjsonlogger import jsonlogger
from .config import Settings

EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
NPI_RE = re.compile(r"\b\d{10}\b")


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[redacted-email]", text)
    text = NPI_RE.sub("[redacted-npi]", text)
    return text


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("ts", datetime.utcnow().isoformat() + "Z")
        log_record.setdefault("level", record.levelname)
        if "message" in log_record:
            log_record["msg"] = redact(log_record.pop("message"))
        for field in ["path", "method", "status", "dur_ms", "req_id"]:
            log_record.setdefault(field, None)


def configure() -> None:
    settings = Settings()
    handler = logging.StreamHandler()
    formatter = CustomJsonFormatter()
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, settings.LOG_LEVEL, "INFO"))
