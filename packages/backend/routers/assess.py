from fastapi import APIRouter

from ..schemas import Claim, AssessmentResult
from ..agents.assessor_agent import assess_claim
from ..core.config import Settings

router = APIRouter(prefix="/v1", tags=["rcm"])


@router.post("/assess", response_model=AssessmentResult)
def assess(claim: Claim) -> AssessmentResult:
    vec_dir = Settings().VECTOR_PATH
    out = assess_claim(claim.model_dump(by_alias=True), vec_dir, topk=5)
    return AssessmentResult(**out)
