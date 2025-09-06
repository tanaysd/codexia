from fastapi import APIRouter

from codexia_contracts.contracts import Claim, PlanResult, RecodingPlan

router = APIRouter()


@router.post("/plan", response_model=PlanResult)
def plan(claim: Claim) -> PlanResult:
    return RecodingPlan(claim_id=claim.claim_id, codes=[])
