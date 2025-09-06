# CPT–ICD and modifier demo rules (synthetic, not clinical advice)
ICD10_REGEX = r"^[A-TV-Z][0-9][A-Z0-9](?:\.[A-Z0-9]{1,4})?$"  # allow letter-digit, dot variants
CPT_REGEX   = r"^[0-9]{5}[A-Z0-9]?$"                          # allow HCPCS letter suffix
MOD_REGEX   = r"^[A-Z0-9]{2}$"

# Known CPT pairs that often require -59 when same DOS unless documentation justifies separation
MODIFIER_59_REQUIRED_PAIRS = {
    # (primary, paired) order-insensitive check will be used
    ("97012", "97110"): {
        "policy_refs": ["UHC-LCD-123 §3b", "Kaiser-ACL-22 §1", "Cigna-MED-77 §2"],
        "why": "Traction (97012) with therapeutic exercise (97110) on same DOS may need -59.",
    }
}

# ICD specificity suggestions for M25.50 → site-specific M25.51x variants (demo mapping)
ICD_SPECIFICITY_SUGGESTIONS = {
    "M25.50": ["M25.512", "M25.511", "M25.519"]  # shoulder pain left/right/unspecified
}

# Site-of-service constraints (demo)
SITE_OF_SERVICE_RULES = {
    # POS 11 is physician office; require documentation rationale for certain imaging/bundles
    "11": {"notes_required_for": ["imaging_generic"], "policy_refs": ["BCBS-P123 §7"]}
}

# CPT-ICD incompatibility demo pairs
DX_CPT_INCOMPATIBLE_PAIRS = {
    ("97110", "Z00.00"): {
        "policy_refs": ["NCD-001 §1"],
        "why": "Therapeutic exercise not covered for general checkup.",
    }
}
