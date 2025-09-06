from fastapi import APIRouter
from pydantic import BaseModel

from ..schemas import Claim, AssessmentResult, PlanResult
from ..agents.planner_agent import make_plan
from ..core.config import Settings

router = APIRouter(prefix="/v1", tags=["rcm"])


class PlanRequest(BaseModel):
    claim: Claim
    assessment: AssessmentResult


@router.post("/plan", response_model=PlanResult)
def plan(body: PlanRequest) -> PlanResult:
    vec_dir = Settings().VECTOR_PATH
    out = make_plan(
        body.claim.model_dump(by_alias=True),
        body.assessment.model_dump(by_alias=True),
        vec_dir,
        topk=5,
    )
    return PlanResult(**out)
