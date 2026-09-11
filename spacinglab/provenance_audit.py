"""Retrospective, CPU-only audit specified in docs/AUDIT_2026-09-08_PLAN.md."""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CACHE_PATH = "data/wikitext103_tokens.npy"
MAIN = ("runs", "contingency", "study2a", "study2b", "study2d", "study3", "study4", "study5", "study6")


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(x: np.ndarray) -> str:
    return hashlib.sha256(np.asarray(x, dtype="<i8").tobytes()).hexdigest()


def fingerprint(tokens: np.ndarray, seed: int, steps: int = 2300) -> dict:
    chunks = tokens[:len(tokens) // 64 * 64].reshape(-1, 64)
    order = np.random.default_rng(seed).permutation(len(chunks))
    if len(chunks) < 200 + steps * 15:
        return {"insufficient_chunks": True}
    train = chunks[order[200:200 + steps * 15]]
    return {"heldout_sha256": digest(chunks[order[:200]]),
            "train_sha256": digest(train), "first_batch_sha256": digest(train[:15])}


def load_run(study: str, condition: str, seed: int) -> tuple[Path, dict]:
    matches = []
    for path in (ROOT / "results" / study).glob("*/log.json"):
        log = json.loads(path.read_text())
        c = log["config"]
        if c["condition"] == condition and c["seed"] == seed and c["tag"] == "":
            matches.append((path, log))
    if len(matches) != 1:
        raise ValueError(f"Expected one run: {study}/{condition}/{seed}, found {len(matches)}")
    return matches[0]


def main() -> None:
    commits = git("log", "--reverse", "--format=%H", "--", CACHE_PATH).decode().splitlines()
    snapshots = []
    for commit in commits:
        raw = git("show", f"{commit}:{CACHE_PATH}")
        arr = np.load(io.BytesIO(raw), allow_pickle=False)
        snapshots.append({"commit": commit, "date": git("show", "-s", "--format=%aI", commit).decode().strip(),
                          "file_sha256": hashlib.sha256(raw).hexdigest(), "tokens": len(arr),
                          "fingerprints": {str(s): fingerprint(arr, s) for s in (0, 1, 2)}})
    pairs = []
    for seed in (0, 1, 2):
        pa, a = load_run("runs", "spaced", seed)
        pb, b = load_run("study6", "random", seed)
        def pre(l):
            return next(e for e in l["evals"] if e["phase"] == "pretrained")
        def prefix(l):
            return [item for item in l["train_loss"] if item[0] < l["config"]["t_pre"]]
        def scores(l):
            vals = [e["acc"] for e in l["evals"] if e["phase"] == "interference"]
            assert len(vals) == 7
            return float(np.mean(vals))
        pairs.append({"seed": seed, "spaced_path": str(pa.relative_to(ROOT)), "random_path": str(pb.relative_to(ROOT)),
                      "spaced_pretrained_holdout_loss": pre(a)["holdout_loss"],
                      "random_pretrained_holdout_loss": pre(b)["holdout_loss"],
                      "spaced_pre_injection_losses": prefix(a), "random_pre_injection_losses": prefix(b),
                      "pre_injection_losses_equal": prefix(a) == prefix(b),
                      "spaced_retention": scores(a), "random_retention": scores(b),
                      "paired_difference": scores(b) - scores(a)})
    inventory = {}
    for folder in sorted((ROOT / "results").iterdir()):
        if not folder.is_dir():
            continue
        logs = list(folder.glob("*/log.json"))
        if not logs and folder.name not in MAIN:
            continue
        inventory[folder.name] = {"log_count": len(logs), "is_main": folder.name in MAIN,
                                 "incomplete_directories": [p.name for p in sorted(folder.iterdir())
                                    if p.is_dir() and not (p / "log.json").exists()]}
    ds = np.array([p["paired_difference"] for p in pairs])
    result = {"plan": "docs/AUDIT_2026-09-08_PLAN.md", "audit_code_commit": git("rev-parse", "HEAD").decode().strip(),
              "snapshots": snapshots, "historical_pairs": pairs, "inventory": inventory,
              "main_log_count": sum(v["log_count"] for v in inventory.values() if v["is_main"]),
              "historical_random_minus_spaced": {"mean": float(ds.mean()), "sample_sd": float(ds.std(ddof=1)),
                                                  "min": float(ds.min()), "max": float(ds.max())}}
    out = ROOT / "results" / "provenance_audit_2026-09-08.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
