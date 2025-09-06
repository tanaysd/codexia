from fastapi import APIRouter
from ..schemas import Claim, AssessmentResult

router = APIRouter(prefix="/v1", tags=["rcm"])


@router.post("/assess", response_model=AssessmentResult)
def assess(claim: Claim) -> AssessmentResult:
    # deterministic stub
    return AssessmentResult(
        risk=0.72,
        drivers=[{"line":0,"issue":"modifier_missing","why":"97012 + 97110 same DOS"}],
        evidence=[{"source":"UHC-LCD-123.md","clauseId":"UHC-LCD-123 §3b","passage":"...","effective":{"from":"2024-01-01"}}],
    )
