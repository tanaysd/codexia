try:
    # canonical (when packages/contracts-py lands)
    from codexia_contracts.contracts import (
        Claim, AssessmentResult, PlanResult, ActResult, BriefResult
    )
except Exception:
    # fallback stubs (strict enough for tests)
    from pydantic import BaseModel, Field, ConfigDict
    from typing import List, Optional, Literal

    class Evidence(BaseModel):
        source: str
        clauseId: str
        passage: str
        effective: dict

    class Driver(BaseModel):
        line: int
        issue: Literal["modifier_missing","dx_incompatibility","ncd_exclusion","sos_restriction","doc_missing","other"]
        why: str

    class ClaimLine(BaseModel):
        cpt: str
        dx: List[str]
        modifiers: List[str] = Field(default_factory=list)
        units: int
        charge: float

    class Payer(BaseModel):
        name: str
        planId: Optional[str] = None
        state: Optional[str] = None

    class Patient(BaseModel):
        dob: str
        age: int
        sex: str

    class Provider(BaseModel):
        npi: str
        siteOfService: Optional[str] = None

    class Claim(BaseModel):
        model_config = ConfigDict(extra="ignore")
        claimId: str
        payer: Payer
        patient: Patient
        provider: Provider
        lines: List[ClaimLine]
        attachments: Optional[List[dict]] = None
        history: Optional[List[dict]] = None
        notes: Optional[List[str]] = None

    class AssessmentResult(BaseModel):
        model_config = ConfigDict(extra="ignore")
        risk: float = Field(ge=0.0, le=1.0)
        drivers: List[Driver] = Field(default_factory=list)
        evidence: List[Evidence] = Field(default_factory=list)

    class RecodingAction(BaseModel):
        line: int
        addModifier: Optional[str] = None
        replaceDx: Optional[dict] = None
        cite: Optional[str] = None

    class RecodingPlan(BaseModel):
        type: Literal["recoding"]
        actions: List[RecodingAction]
        rationale: str

    class AppealAction(BaseModel):
        level: Literal["L1","L2"]
        reason: str
        cites: List[str] = Field(default_factory=list)

    class AppealPlan(BaseModel):
        type: Literal["appeal"]
        actions: List[AppealAction]
        rationale: str

    class PlanResult(BaseModel):
        plans: List[RecodingPlan | AppealPlan] = Field(default_factory=list)

    class ActResult(BaseModel):
        artifactType: Literal["corrected_claim","appeal_letter"]
        payload: dict

    class BriefItem(BaseModel):
        claimId: str
        score: float
        expDeltaUsd: float
        why: List[str]
        etaMin: int
        deadline: Optional[str] = None

    class BriefResult(BaseModel):
        highlights: List[str] = Field(default_factory=list)
        queue: List[BriefItem] = Field(default_factory=list)
