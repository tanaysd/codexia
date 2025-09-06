from fastapi import APIRouter, Query
from ..schemas import BriefResult

router = APIRouter(prefix="/v1", tags=["rcm"])


@router.get("/brief", response_model=BriefResult)
def brief(user_id: str = Query(...), date: str = Query(...)) -> BriefResult:
    return BriefResult(
        highlights=["UHC-LCD-123 updated on 2025-08-01"],
        queue=[
            {"claimId":"CLM-1001","score":0.91,"expDeltaUsd":126.0,"why":["modifier"],"etaMin":2},
            {"claimId":"CLM-1002","score":0.86,"expDeltaUsd":410.0,"why":["NCD"],"etaMin":6,"deadline":"2025-09-12"},
        ],
    )
