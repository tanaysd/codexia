import os
import json
import glob
import random
from typing import Tuple

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from .normalize import extract_clauses
from .types import Passage

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _gather_passages(policies_dir: str) -> list[Passage]:
    passages: list[Passage] = []
    for path in sorted(glob.glob(os.path.join(policies_dir, "*.md"))):
        with open(path, "r", encoding="utf-8") as f:
            md = f.read()
        passages.extend(extract_clauses(md, os.path.basename(path)))
    return passages


def build_index(policies_dir: str, vector_dir: str, rebuild: bool = False):
    os.makedirs(vector_dir, exist_ok=True)
    index_path = os.path.join(vector_dir, "index.faiss")
    meta_path = os.path.join(vector_dir, "meta.json")

    if (
        not rebuild
        and os.path.exists(index_path)
        and os.path.exists(meta_path)
    ):
        latest_src = max(
            os.path.getmtime(p)
            for p in glob.glob(os.path.join(policies_dir, "*.md"))
        )
        if os.path.getmtime(meta_path) >= latest_src:
            return load_index(vector_dir)

    random.seed(13)
    np.random.seed(13)
    try:
        import torch
        torch.manual_seed(13)
    except Exception:
        pass

    passages = _gather_passages(policies_dir)
    texts = [p["text"] for p in passages]

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    embeddings = embeddings.astype("float32")
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    meta = {"vector_dim": dim, "model": MODEL_NAME, "passages": passages}
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return index, meta


def load_index(vector_dir: str):
    index_path = os.path.join(vector_dir, "index.faiss")
    meta_path = os.path.join(vector_dir, "meta.json")
    if not (os.path.exists(index_path) and os.path.exists(meta_path)):
        raise FileNotFoundError("Vector index not found; build it first")
    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta
