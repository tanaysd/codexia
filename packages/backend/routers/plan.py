from fastapi import APIRouter
from pydantic import BaseModel
from ..schemas import Claim, AssessmentResult, PlanResult

router = APIRouter(prefix="/v1", tags=["rcm"])


class PlanRequest(BaseModel):
    claim: Claim
    assessment: AssessmentResult


@router.post("/plan", response_model=PlanResult)
def plan(body: PlanRequest) -> PlanResult:
    return PlanResult(plans=[
        {"type":"recoding","actions":[{"line":0,"addModifier":"59","cite":"UHC-LCD-123 §3b"}],"rationale":"Distinct procedural service"},
        {"type":"appeal","actions":[{"level":"L1","reason":"medical_necessity","cites":["CMS-NCD-456 §2"]}],"rationale":"Policy ambiguity"}
    ])
