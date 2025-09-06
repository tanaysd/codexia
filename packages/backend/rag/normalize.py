import re
from typing import List
from .types import Passage

ALLOWED_CHARS = re.compile(r"[^a-z0-9\s\-_/.:()§]")
SPACE_RE = re.compile(r"\s+")


def normalize_text(s: str) -> str:
    s = s.lower()
    s = ALLOWED_CHARS.sub(" ", s)
    s = SPACE_RE.sub(" ", s)
    return s.strip()


def extract_clauses(md: str, source: str) -> List[Passage]:
    lines = md.splitlines()
    passages: List[Passage] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("- clause_id:"):
            clause_id = line.split(":", 1)[1].strip()
            i += 1
            if i >= len(lines):
                break
            eff_line = lines[i].strip()
            m = re.match(r"- effective:\s*(\d{4}-\d{2}-\d{2})\s*→\s*(\d{4}-\d{2}-\d{2})?", eff_line)
            if not m:
                i += 1
                continue
            effective_from = m.group(1)
            effective_to = m.group(2) or None
            i += 1
            text_lines = []
            if i < len(lines) and lines[i].strip().startswith("Text:"):
                text_lines.append(lines[i].split("Text:", 1)[1].strip())
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("- clause_id:") and lines[i].strip() != "":
                    text_lines.append(lines[i].strip())
                    i += 1
            text = " ".join(text_lines).strip()
            passage_text = f"{clause_id} ({effective_from}→{effective_to or ''}) {text}".strip()
            passages.append(
                Passage(
                    text=passage_text,
                    source=source,
                    clause_id=clause_id,
                    effective_from=effective_from,
                    effective_to=effective_to,
                )
            )
        else:
            i += 1
    return passages
