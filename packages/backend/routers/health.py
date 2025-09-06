from fastapi import APIRouter
import os

router = APIRouter(tags=["ops"])


@router.get("/healthz")
def healthz():
    return {"status": "ok", "gitSha": os.getenv("GIT_SHA", "unknown")}
