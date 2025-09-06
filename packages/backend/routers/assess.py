from fastapi import APIRouter

from codexia_contracts.contracts import Claim, AssessmentResult

router = APIRouter()


@router.post("/assess", response_model=AssessmentResult)
def assess(claim: Claim) -> AssessmentResult:
    return AssessmentResult(claim_id=claim.claim_id, risk=0.5, drivers=[], evidence=[])
