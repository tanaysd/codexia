import logging
import re
import time
from datetime import datetime
from pythonjsonlogger import jsonlogger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .config import Settings
from .metrics import record_request

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
NPI_RE = re.compile(r"(?<!\d)\d{10}(?!\d)")


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = NPI_RE.sub("[REDACTED_NPI]", text)
    return text


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record.setdefault("ts", datetime.utcnow().isoformat() + "Z")
        log_record.setdefault("level", record.levelname)
        if "message" in log_record:
            log_record["msg"] = redact(log_record.pop("message"))
        for field in [
            "path",
            "method",
            "status",
            "dur_ms",
            "bytes_in",
            "bytes_out",
            "req_id",
            "client_ip",
        ]:
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


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger("codexia")

    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        request._body = body
        start = time.monotonic()
        response = await call_next(request)
        dur_ms = int((time.monotonic() - start) * 1000)
        request_id = getattr(request.state, "request_id", "")
        bytes_in = getattr(request.state, "bytes_in", len(body))
        msg = body.decode("utf-8", errors="ignore") if body else ""
        bytes_out = len(getattr(response, "body", b""))
        client_ip = request.client.host if request.client else ""
        self.logger.info(
            msg,
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "dur_ms": dur_ms,
                "bytes_in": bytes_in,
                "bytes_out": bytes_out,
                "req_id": request_id,
                "client_ip": client_ip,
            },
        )
        record_request(request.method, request.url.path, response.status_code, dur_ms / 1000.0)
        return response
