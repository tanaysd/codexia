from fastapi import APIRouter

from codexia_contracts.contracts import ActResult, BriefResult

router = APIRouter()


@router.post("/brief", response_model=BriefResult)
def brief(act: ActResult) -> BriefResult:
    return BriefResult(claim_id=act.claim_id, summary="")
