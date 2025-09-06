import time
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_body_size: int = int(1.5 * 1024 * 1024)):
        super().__init__(app)
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-Id") or str(uuid4())
        start = time.time()
        body = await request.body()
        if len(body) > self.max_body_size:
            return Response(status_code=413)
        request._body = body  # allow downstream to read again
        request.state.request_id = request_id
        response = await call_next(request)
        duration = int((time.time() - start) * 1000)
        response.headers.setdefault("X-Request-Id", request_id)
        response.headers.setdefault("X-Response-Time", str(duration))
        return response
