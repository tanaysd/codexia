from typing import TypedDict, List, Optional

class Passage(TypedDict):
    text: str
    source: str           # filename
    clause_id: str        # e.g., "UHC-LCD-123 §3b"
    effective_from: str   # YYYY-MM-DD
    effective_to: Optional[str]  # None or YYYY-MM-DD

class Retrieval(TypedDict):
    query: str
    topk: int
    results: List[Passage]
