from __future__ import annotations

from datetime import datetime, date

from .contracts import (
    Attachment,
    Claim,
    ClaimLine,
    HistoryEvent,
    Patient,
    Payer,
    Provider,
)

CASE_MOD59_PY = Claim(
    claim_id="CLM-1001",
    payer=Payer(name="UnitedHealthcare", plan_id="UHC-GOLD-CA", state="CA"),
    patient=Patient(dob=date(1962, 5, 14), age=63, sex="F"),
    provider=Provider(npi="1093817465", site_of_service="11"),
    lines=[
        ClaimLine(cpt="97012", dx=["M25.50"], modifiers=[""], units=1, charge=180.00),
        ClaimLine(cpt="97110", dx=["M25.50"], modifiers=[""], units=1, charge=190.00),
    ],
    attachments=[Attachment(type="progress_note", id="doc_123")],
    history=[HistoryEvent(ts=datetime.fromisoformat("2025-09-05T10:00:00+00:00"), event="created")],
    notes=[
        "Therapeutic exercise same session; distinct procedural service not indicated in line 1."
    ],
)


def case_mod59_wire() -> str:
    return CASE_MOD59_PY.model_dump_json(by_alias=True)
