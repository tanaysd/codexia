from fastapi import APIRouter
from pydantic import BaseModel
from ..core.audit import audit_write
from ..schemas import Claim, PlanResult, ActResult

router = APIRouter(prefix="/v1", tags=["rcm"])


class ActRequest(BaseModel):
    claim: Claim
    plan: PlanResult


@router.post("/act", response_model=ActResult)
def act(body: ActRequest) -> ActResult:
    # For demo: if first plan is recoding, echo corrected JSON; else return letter md
    if body.plan.plans and body.plan.plans[0].type == "recoding":
        corrected = body.claim.model_dump() if hasattr(body.claim, "model_dump") else body.claim.__dict__
        # apply the modifier (demo-safe)
        corrected["lines"][0]["modifiers"] = ["59"]
        artifact = {"artifactType":"corrected_claim","payload":corrected}
    else:
        artifact = {"artifactType":"appeal_letter","payload":{"markdown":"# Appeal\n...","cites":["CMS-NCD-456 §2"]}}
    audit_write(kind="act", payload=artifact)
    return ActResult(**artifact)
