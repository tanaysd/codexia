import time
from math import ceil
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .config import Settings
from .metrics import inc_rate_limited


class TokenBucket:
    def __init__(self, rate: float):
        self.rate = rate
        self.capacity = ceil(3 * rate)
        self.tokens = {}

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        tokens, last = self.tokens.get(key, (self.capacity, now))
        tokens = min(self.capacity, tokens + (now - last) * self.rate)
        if tokens < 1:
            self.tokens[key] = (tokens, now)
            return False
        self.tokens[key] = (tokens - 1, now)
        return True


class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        settings = Settings()
        self.max_body_size = settings.MAX_PAYLOAD_BYTES
        self.enable_hsts = settings.ENABLE_HSTS
        self.bucket = TokenBucket(settings.RATE_LIMIT_RPS)

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        body = await request.body()
        if len(body) > self.max_body_size:
            request.state.request_id = request_id
            request.state.bytes_in = len(body)
            return Response(status_code=413)
        request._body = body
        request.state.request_id = request_id
        request.state.bytes_in = len(body)
        client_ip = request.client.host if request.client else "unknown"
        if not self.bucket.allow(client_ip):
            inc_rate_limited(request.url.path)
            headers = {"Retry-After": "1", "X-Request-Id": request_id}
            return Response(status_code=429, headers=headers)
        response = await call_next(request)
        response.headers.setdefault("X-Request-Id", request_id)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault("Cache-Control", "no-store")
        if self.enable_hsts:
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )
        return response


def cors_config() -> dict:
    s = Settings()
    return {
        "allow_origins": s.allowed_origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
