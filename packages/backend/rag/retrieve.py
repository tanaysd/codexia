import os
import random
from typing import Dict, Any, Tuple, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
import hashlib

from .normalize import normalize_text
from .indexer import load_index
from .types import Retrieval, Passage


def _sort_key(p: Passage):
    return (p["source"], p["clause_id"])


def semantic_search(query: str, topk: int, vector_dir: str) -> Retrieval:
    index, meta = load_index(vector_dir)

    random.seed(13)
    np.random.seed(13)
    try:
        import torch
        torch.manual_seed(13)
    except Exception:
        pass

    norm_q = normalize_text(query)
    try:
        model = SentenceTransformer(meta["model"], local_files_only=True)
        q_emb = model.encode([norm_q], normalize_embeddings=True).astype("float32")
    except Exception:
        dim = meta["vector_dim"]
        q_emb = np.zeros((1, dim), dtype="float32")
        for word in norm_q.split():
            h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16) % dim
            q_emb[0, h] += 1.0
        q_emb = q_emb / (np.linalg.norm(q_emb) + 1e-10)

    k = max(topk, 1)
    D, I = index.search(q_emb, k)
    pairs = []
    for dist, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        passage = meta["passages"][idx]
        pairs.append((float(dist), passage))

    pairs.sort(key=lambda x: (x[0], _sort_key(x[1])))
    results = [p for _, p in pairs[:topk]]
    return Retrieval(query=query, topk=topk, results=results)


def query_policy_for_claim_context(claim: Dict[str, Any], topk: int, vector_dir: str) -> Retrieval:
    payer = claim.get("payer", {}).get("name", "")
    cpts = [line.get("cpt", "") for line in claim.get("lines", [])]
    mods = [m for line in claim.get("lines", []) for m in line.get("modifiers", []) if m]
    sos = claim.get("provider", {}).get("siteOfService") or claim.get("provider", {}).get("site_of_service")

    parts = []
    if payer:
        parts.append(payer)
    parts.extend(cpts)
    parts.extend(mods)
    if sos:
        parts.append(f"pos {sos}")
    query = " ".join(parts)
    return semantic_search(query, topk, vector_dir)


def top_citations_for_issue(issue: str, cpt_pair: Optional[Tuple[str, str]], payer: Optional[str], topk: int, vector_dir: str) -> list[Passage]:
    parts = [issue]
    if cpt_pair:
        parts.extend(list(cpt_pair))
    if payer:
        parts.append(payer)
    retrieval = semantic_search(" ".join(parts), topk, vector_dir)
    return retrieval["results"]
