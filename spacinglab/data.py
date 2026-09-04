"""Filler text: WikiText-103 as one token stream, cut into fixed-length chunks."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import torch

CACHE = Path(__file__).resolve().parent.parent / "data"


def build_filler_tokens(tokenizer, n_tokens: int, cache_name: str = "wikitext103_tokens.npy") -> np.ndarray:
    """Tokenise WikiText-103 train (from the start) into a flat uint16 array, cached on disk."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / cache_name
    if path.exists():
        arr = np.load(path)
        if len(arr) >= n_tokens:
            return arr[:n_tokens]
    from datasets import load_dataset
    ds = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train")
    eos = tokenizer.eos_token_id
    out: list[int] = []
    doc: list[str] = []
    i = 0
    while len(out) < n_tokens and i < len(ds):
        line = ds[i]["text"]
        i += 1
        if line.startswith(" = ") and not line.startswith(" = = "):
            # new article: flush the previous one
            if doc:
                out.extend(tokenizer("".join(doc))["input_ids"])
                out.append(eos)
                doc = []
        elif line.strip():
            doc.append(line)
    if doc and len(out) < n_tokens:
        out.extend(tokenizer("".join(doc))["input_ids"])
        out.append(eos)
    arr = np.asarray(out[:n_tokens], dtype=np.uint16)
    np.save(path, arr)
    return arr


class FillerStream:
    """Fixed-order 64-token chunks. `seed` shuffles chunk order; `take(n)` consumes."""

    def __init__(self, tokens: np.ndarray, seq_len: int, seed: int, n_holdout: int = 200):
        n_chunks = len(tokens) // seq_len
        chunks = tokens[: n_chunks * seq_len].reshape(n_chunks, seq_len)
        order = np.random.default_rng(seed).permutation(n_chunks)
        self.holdout = torch.from_numpy(chunks[order[:n_holdout]].astype(np.int64))
        self.chunks = chunks[order[n_holdout:]]
        self.pos = 0

    def take(self, n: int) -> torch.Tensor:
        assert self.pos + n <= len(self.chunks), "filler stream exhausted"
        batch = self.chunks[self.pos : self.pos + n]
        self.pos += n
        return torch.from_numpy(batch.astype(np.int64))
