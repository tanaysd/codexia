import os
import time
import json
from fastapi import APIRouter, Response, status
from ..core.config import Settings

router = APIRouter(tags=["ops"])
_START = time.time()
settings = Settings()


@router.get("/healthz")
def healthz():
    uptime = time.time() - _START
    return {
        "status": "ok",
        "gitSha": os.getenv("GIT_SHA", "unknown"),
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "uptime_s": uptime,
    }


@router.get("/readyz")
def readyz():
    errors = []
    if settings.VECTOR_PATH and not os.path.isdir(settings.VECTOR_PATH):
        errors.append("vector path missing")
    if not os.access(settings.AUDIT_PATH, os.W_OK):
        errors.append("audit path not writable")
    ready = not errors
    status_code = status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE
    body = {"ready": ready}
    if errors:
        body["errors"] = errors
    return Response(status_code=status_code, media_type="application/json", content=json.dumps(body))
