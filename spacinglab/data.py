"""Filler text: WikiText-103 as one token stream, cut into fixed-length chunks."""
from __future__ import annotations

import hashlib
import io
from pathlib import Path

import numpy as np
import torch

CACHE = Path(__file__).resolve().parent.parent / "data"


def load_filler_snapshot(path: Path | str, expected_sha256: str, required_tokens: int) -> np.ndarray:
    """Load exactly the registered bytes; never grow, download, or truncate them."""
    raw = Path(path).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_sha256:
        raise ValueError(f"Filler SHA-256 mismatch: expected {expected_sha256}, got {actual}")
    tokens = np.load(io.BytesIO(raw), allow_pickle=False)
    if tokens.ndim != 1 or not np.issubdtype(tokens.dtype, np.integer):
        raise ValueError("Filler snapshot must be a one-dimensional integer array")
    if len(tokens) < required_tokens:
        raise ValueError(f"Insufficient filler snapshot: {len(tokens)} < {required_tokens} tokens")
    tokens.flags.writeable = False
    return tokens


def token_digest(tokens: np.ndarray) -> str:
    """Canonical integer-array hash, independent of platform endianness/dtype."""
    return hashlib.sha256(np.asarray(tokens, dtype="<i8").tobytes()).hexdigest()


def build_filler_tokens(tokenizer, n_tokens: int, cache_name: str = "wikitext103_tokens.npy") -> np.ndarray:
    """Legacy mutable cache. New comparisons must use load_filler_snapshot instead."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / cache_name
    if path.exists():
        arr = np.load(path)
        if len(arr) >= n_tokens:
            # Legacy behavior preserved for old scripts, NOT stable across cache growth.
            # See docs/PROVENANCE_AUDIT_2026-09-08.md.
            return arr
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

    def provenance(self, n_train: int) -> dict:
        """Fingerprint the planned stream from its start, without consuming it."""
        if n_train < 0 or n_train > len(self.chunks):
            raise ValueError("Insufficient training chunks for requested provenance")
        return {"train_chunks": n_train, "heldout_chunks": len(self.holdout),
                "seq_len": self.chunks.shape[1],
                "train_sha256": token_digest(self.chunks[:n_train]),
                "heldout_sha256": token_digest(self.holdout.numpy())}

    def take(self, n: int) -> torch.Tensor:
        assert self.pos + n <= len(self.chunks), "filler stream exhausted"
        batch = self.chunks[self.pos : self.pos + n]
        self.pos += n
        return torch.from_numpy(batch.astype(np.int64))
