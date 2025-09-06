from __future__ import annotations

import re
from typing import Pattern

ID_RE: Pattern[str] = re.compile(r"^[A-Za-z0-9_-]+$")
NPI_RE: Pattern[str] = re.compile(r"^\d{10}$")
CPT_RE: Pattern[str] = re.compile(r"^\d{5}$")
ICD10_RE: Pattern[str] = re.compile(r"^[A-TV-Z][0-9][0-9A-TV-Z](?:\.[0-9A-TV-Z]{1,4})?$")
MODIFIER_RE: Pattern[str] = re.compile(r"^[A-Z0-9]{2}$")
STATE_RE: Pattern[str] = re.compile(
    r"^(?:A[KLRZ]|C[AOT]|D[EC]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[EHDAINSOTP]|N[HCJMVY]|O[HKR]|P[AR]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$"
)


def _check(value: str, regex: Pattern[str], message: str) -> str:
    if not regex.fullmatch(value):
        raise ValueError(message)
    return value


def check_id(value: str) -> str:
    return _check(value, ID_RE, "invalid id")


def check_npi(value: str) -> str:
    return _check(value, NPI_RE, "invalid npi")


def check_cpt(value: str) -> str:
    return _check(value, CPT_RE, "invalid cpt")


def check_icd10(value: str) -> str:
    return _check(value, ICD10_RE, "invalid icd10")


def check_modifier(value: str) -> str:
    return _check(value, MODIFIER_RE, "invalid modifier")


def check_state(value: str) -> str:
    return _check(value, STATE_RE, "invalid state")
