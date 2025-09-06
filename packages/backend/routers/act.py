from fastapi import APIRouter

from codexia_contracts.contracts import PlanResult, ActResult

router = APIRouter()


@router.post("/act", response_model=ActResult)
def act(plan: PlanResult) -> ActResult:
    return ActResult(claim_id=plan.claim_id, actions=[])
