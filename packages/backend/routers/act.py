from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List

from ..schemas import Claim, PlanResult, ActResult, AssessmentResult
from ..agents.actor_agent import act_on_plan
from ..core.audit import audit_write

router = APIRouter(prefix="/v1", tags=["rcm"])


class ActRequest(BaseModel):
    claim: Claim
    plan: PlanResult
    assessment: AssessmentResult | None = None


@router.post("/act", response_model=ActResult)
def act(body: ActRequest) -> ActResult:
    claim_dict = (
        body.claim.model_dump(by_alias=True) if hasattr(body.claim, "model_dump") else body.claim
    )
    plan_dict = (
        body.plan.model_dump(by_alias=True) if hasattr(body.plan, "model_dump") else body.plan
    )
    evidence: List[Dict[str, Any]] = []
    if body.assessment is not None:
        asmt = (
            body.assessment.model_dump(by_alias=True)
            if hasattr(body.assessment, "model_dump")
            else body.assessment
        )
        for e in asmt.get("evidence", []):
            passage = {
                "text": e.get("passage", ""),
                "clause_id": e.get("clause_id") or e.get("clauseId"),
                "source": e.get("source"),
            }
            evidence.append(passage)
    artifact = act_on_plan(claim_dict, plan_dict, evidence=evidence)

    audit_write(
        "act",
        {
            "artifactType": artifact["artifactType"],
            "meta": artifact.get("meta"),
        },
    )

    return ActResult(**{k: v for k, v in artifact.items() if k in ("artifactType", "payload")})
