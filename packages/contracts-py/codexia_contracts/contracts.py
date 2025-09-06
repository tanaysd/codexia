from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional, Annotated, Union, Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator

from .validators import (
    check_id,
    check_npi,
    check_cpt,
    check_icd10,
    check_modifier,
    check_state,
)


class _Base(BaseModel):
    model_config = ConfigDict(populate_by_name=True, frozen=True, str_strip_whitespace=True)


class Payer(_Base):
    name: str
    plan_id: str = Field(alias="planId")
    state: str

    _val_id = field_validator("plan_id", mode="before")(check_id)
    _val_state = field_validator("state", mode="before")(check_state)


class Patient(_Base):
    dob: date
    age: int
    sex: Literal["M", "F"]


class Provider(_Base):
    npi: str
    site_of_service: str = Field(alias="siteOfService")

    _val_npi = field_validator("npi", mode="before")(check_npi)


class ClaimLine(_Base):
    cpt: str
    dx: List[str]
    modifiers: List[str]
    units: int
    charge: float

    _val_cpt = field_validator("cpt", mode="before")(check_cpt)
    _val_dx = field_validator("dx", each_item=True, mode="before")(check_icd10)
    _val_mod = field_validator("modifiers", each_item=True, mode="before")(check_modifier)


class Attachment(_Base):
    type: str
    id: str

    _val_id = field_validator("id", mode="before")(check_id)


class HistoryEvent(_Base):
    ts: datetime
    event: str


class Claim(_Base):
    claim_id: str = Field(alias="claimId")
    payer: Payer
    patient: Patient
    provider: Provider
    lines: List[ClaimLine]
    attachments: List[Attachment] = Field(default_factory=list)
    history: List[HistoryEvent] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)

    _val_claim_id = field_validator("claim_id", mode="before")(check_id)


class AssessmentResult(_Base):
    claim_id: str = Field(alias="claimId")
    risk: float = 0.0
    drivers: List[str] = Field(default_factory=list)
    evidence: List[str] = Field(default_factory=list)

    _val_claim_id = field_validator("claim_id", mode="before")(check_id)

    @field_validator("risk")
    @classmethod
    def _check_risk(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError("risk must be between 0 and 1")
        return v


class RecodingPlan(_Base):
    claim_id: str = Field(alias="claimId")
    plan_type: Literal["recoding"] = Field(alias="planType", default="recoding")
    codes: List[str] = Field(default_factory=list)

    _val_claim_id = field_validator("claim_id", mode="before")(check_id)


class AppealPlan(_Base):
    claim_id: str = Field(alias="claimId")
    plan_type: Literal["appeal"] = Field(alias="planType", default="appeal")
    rationale: str

    _val_claim_id = field_validator("claim_id", mode="before")(check_id)


PlanResult = Annotated[Union[RecodingPlan, AppealPlan], Field(discriminator="plan_type")]


class ActResult(_Base):
    claim_id: str = Field(alias="claimId")
    actions: List[str] = Field(default_factory=list)

    _val_claim_id = field_validator("claim_id", mode="before")(check_id)


class BriefResult(_Base):
    claim_id: str = Field(alias="claimId")
    summary: str

    _val_claim_id = field_validator("claim_id", mode="before")(check_id)
