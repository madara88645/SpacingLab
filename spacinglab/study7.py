"""Frozen six-run execution and analysis; see docs/STUDY7_PREREGISTRATION.md."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

import numpy as np

from .data import FillerStream, load_filler_snapshot
from .train import Config, run

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/study7"
REVISION = "607a30d783dfa663caf39e06633721c8d4cfcd7e"
MODEL = Path.home() / ".cache/huggingface/hub/models--gpt2/snapshots" / REVISION
FILLER_SHA = "868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304"
ORDER = [("spaced", 0), ("random", 0), ("random", 1), ("spaced", 1), ("spaced", 2), ("random", 2)]


def config(condition: str, seed: int) -> Config:
    return Config(condition=condition, seed=seed, k=5, t_inj=700,
                  model_name=str(MODEL), model_revision=REVISION, offline=True,
                  filler_snapshot=str(ROOT / "data/wikitext103_tokens.npy"),
                  filler_sha256=FILLER_SHA, collect_step_guards=True, tag="study7")


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def freeze_manifest() -> dict:
    if not (MODEL / "model.safetensors").is_file():
        raise FileNotFoundError(f"Pinned model weights missing at {MODEL}")
    tokens = load_filler_snapshot(ROOT / "data/wikitext103_tokens.npy", FILLER_SHA, 2233600)
    paths = sorted((ROOT / "spacinglab").glob("*.py")) + [ROOT / "uv.lock", ROOT / "pyproject.toml",
             ROOT / "docs/STUDY7_PREREGISTRATION.md"]
    manifest = {"source_sha256": {str(p.relative_to(ROOT)): file_sha(p) for p in paths},
                "model_files_sha256": {p.name: file_sha(p) for p in sorted(MODEL.iterdir()) if p.is_file()},
                "filler_sha256": FILLER_SHA, "python": sys.version,
                "packages": {p: version(p) for p in ("torch", "transformers", "numpy", "datasets", "peft")},
                "order": [asdict(config(c, s)) for c, s in ORDER],
                "streams": {str(s): FillerStream(tokens, 64, s).provenance(34500) for s in (0, 1, 2)}}
    # Compare JSON-native values on both sides (checkpoint tuples serialize as lists).
    manifest = json.loads(json.dumps(manifest))
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "manifest.json"
    if path.exists():
        if json.loads(path.read_text()) != manifest:
            raise ValueError("Manifest mismatch: pinned inputs, code, or software changed; stop and amend")
    else:
        with path.open("x") as f:
            json.dump(manifest, f, indent=2)
    return manifest


def describe(values) -> dict:
    x = np.asarray(values, dtype=float)
    if len(x) != 3 or not np.isfinite(x).all():
        raise ValueError("Expected three finite seed-level values")
    return {"values": x.tolist(), "mean": float(x.mean()), "sample_sd": float(x.std(ddof=1)),
            "min": float(x.min()), "max": float(x.max())}


def direction(values) -> str:
    s = describe(values)
    if s["min"] > 0 and s["mean"] > s["sample_sd"]:
        return "positive_directional_signal"
    if s["max"] < 0 and abs(s["mean"]) > s["sample_sd"]:
        return "negative_directional_signal"
    return "mixed_or_inconclusive"


def validate_pair(a: dict, b: dict) -> None:
    ca, cb = dict(a["config"]), dict(b["config"])
    ca.pop("condition"); cb.pop("condition")
    if ca != cb:
        raise ValueError("Paired configuration mismatch")
    for key in ("train_sha256", "heldout_sha256", "filler_file_sha256", "model_revision", "packages"):
        if a["provenance"][key] != b["provenance"][key]:
            raise ValueError(f"Paired provenance mismatch: {key}")
    for key in ("facts", "int_facts", "interference_schedule"):
        if a[key] != b[key]:
            raise ValueError(f"Paired content mismatch: {key}")
    for key in ("optimizer_steps", "filler_tokens_seen", "fact_tokens_seen", "exposures", "int_exposures"):
        if a["guards"][key] != b["guards"][key]:
            raise ValueError(f"Paired budget mismatch: {key}")
    for log in (a, b):
        c = log["config"]
        if len(log["step_guards"]) != c["t_pre"] + c["t_inj"] + c["t_int"]:
            raise ValueError("Step diagnostic count mismatch")


def load_log(condition: str, seed: int) -> dict:
    p = OUT / f"{condition}_s{seed}" / "log.json"
    log = json.loads(p.read_text())
    if log["config"] != asdict(config(condition, seed)):
        # JSON turns the checkpoint tuple into a list.
        if log["config"] != json.loads(json.dumps(asdict(config(condition, seed)))):
            raise ValueError(f"Saved configuration mismatch: {p}")
    expected = json.loads((OUT / "manifest.json").read_text())["streams"][str(seed)]
    for key in ("train_sha256", "heldout_sha256"):
        if log["provenance"][key] != expected[key]:
            raise ValueError(f"Saved stream mismatch: {p}, {key}")
    return log


def metrics(log: dict) -> dict:
    es = [e for e in log["evals"] if e["phase"] == "interference"]
    if [e["int_step"] for e in es] != [50, 100, 200, 400, 800, 1200, 1500]:
        raise ValueError("Incomplete checkpoint sequence")
    imm = next(e for e in log["evals"] if e["phase"] == "immediate")
    steps, guards = log["step_guards"], log["guards"]
    return {"retention_accuracy": float(np.mean([e["acc"] for e in es])),
            "retention_nll": float(np.mean([e["nll"] for e in es])),
            "retention_discrimination": float(np.mean([e["disc"] for e in es])),
            "terminal_accuracy": es[-1]["acc"], "terminal_nll": es[-1]["nll"],
            "at_last_accuracy": guards["acc_at_last_exposure"], "at_last_nll": guards["nll_at_last_exposure"],
            "window_accuracy": imm["acc"], "window_nll": imm["nll"],
            "last_exposure_step": float(np.mean(log["last_exposure"])),
            "terminal_new_facts_accuracy": es[-1]["int_facts_acc"], "terminal_new_facts_nll": es[-1]["int_facts_nll"],
            "terminal_filler_loss": es[-1]["holdout_loss"], "parameter_displacement": es[-1]["param_dist"],
            "clip_fraction": float(np.mean([g["clip_scale"] < 1 for g in steps])),
            "mean_preclip_norm": float(np.mean([g["preclip_norm"] for g in steps])),
            "target_coefficient_per_exposure": sum(g["target_coefficient_sum"] for g in steps) / guards["exposures"],
            "clipped_target_coefficient_per_exposure": sum(g["clipped_target_coefficient_sum"] for g in steps) / guards["exposures"],
            "floor_checkpoints": sum(e["acc"] <= .02 for e in es),
            "ceiling_checkpoints": sum(e["acc"] >= .98 for e in es)}


def analyze() -> dict:
    logs = {(c, s): load_log(c, s) for c, s in ORDER}
    pre = []
    for s in (0, 1, 2):
        a, b = logs["spaced", s], logs["random", s]
        validate_pair(a, b)
        losses = [abs(x[1]-y[1]) for x, y in zip(a["train_loss"], b["train_loss"]) if x[0] < 100]
        pre.append({"seed": s, "max_pre_injection_training_loss_difference": max(losses),
                    "pretrained_holdout_difference": b["evals"][0]["holdout_loss"] - a["evals"][0]["holdout_loss"]})
    ms = {key: metrics(log) for key, log in logs.items()}
    summaries = {}
    for metric in ms["spaced", 0]:
        a = [ms["spaced", s][metric] for s in (0, 1, 2)]
        b = [ms["random", s][metric] for s in (0, 1, 2)]
        summaries[metric] = {"spaced": describe(a), "random": describe(b),
                             "random_minus_spaced": describe(np.array(b)-a)}
    d = summaries["retention_accuracy"]["random_minus_spaced"]["values"]
    nll_delta = summaries["retention_nll"]["random_minus_spaced"]["mean"]
    result = {"registration": "docs/STUDY7_PREREGISTRATION.md", "complete_runs": 6,
              "direction": direction(d), "metrics_discordant": bool(np.mean(d) * nll_delta > 0),
              "pre_intervention_guards": pre, "metrics": summaries,
              "interpretation": "Total placement-policy effect; three seeds do not establish significance or equivalence."}
    (OUT / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    def fmt(s):
        return f"{s['mean']:.5f} ± {s['sample_sd']:.5f} [{s['min']:.5f}, {s['max']:.5f}]"
    lines = ["# Study 7 results", "", "All six fresh runs; mean ± sample SD [min, max] across three seeds.", "",
             f"Registered rule: **{result['direction']}**; accuracy/NLL discordant: **{result['metrics_discordant']}**.", "",
             "These are total placement-policy effects, including recency and batch composition.",
             "They do not establish equivalence, a universal shuffle rule, or a brain-like mechanism.", "",
             "| Metric | Spaced | Random | Random minus spaced |", "|---|---|---|---|"]
    for metric, s in summaries.items():
        lines.append(f"| {metric} | {fmt(s['spaced'])} | {fmt(s['random'])} | {fmt(s['random_minus_spaced'])} |")
    lines += ["", "## Primary score by seed", "", "| Seed | Spaced | Random | Difference |", "|---|---|---|---|"]
    for s in (0, 1, 2):
        a, b = ms["spaced", s]["retention_accuracy"], ms["random", s]["retention_accuracy"]
        lines.append(f"| {s} | {a:.6f} | {b:.6f} | {b-a:+.6f} |")
    lines += ["", "Paired input/fact/budget checks passed. Pre-injection numerical differences:",
              "```json", json.dumps(pre, indent=2), "```", "",
              "Continuous metrics and floor/ceiling flags must be read together. Clipped coefficients",
              "are diagnostics, not per-fact gradient attribution. Acquisition differences prevent an",
              "equal-learning forgetting interpretation. Do not pool these with older studies."]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "metrics"}, indent=2), flush=True)
    print(json.dumps({k: summaries[k] for k in ("retention_accuracy", "retention_nll")}, indent=2), flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--one", nargs=2, metavar=("CONDITION", "SEED"))
    ap.add_argument("--analyze", action="store_true")
    args = ap.parse_args()
    if args.analyze:
        analyze()
        return
    freeze_manifest()
    if args.one:
        c, s = args.one[0], int(args.one[1])
        if (c, s) not in ORDER:
            raise ValueError("Unregistered run")
        run(config(c, s), OUT / f"{c}_s{s}")
        return
    if not args.run:
        print("STUDY7_PREFLIGHT_OK: immutable manifest recorded; no model evaluation", flush=True)
        return
    with (OUT / "runner.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for c, s in ORDER:
            folder = OUT / f"{c}_s{s}"
            if (folder / "log.json").exists():
                load_log(c, s)
                continue
            if folder.exists() and any(folder.iterdir()):
                raise RuntimeError(f"Incomplete attempt retained at {folder}; amend before restart")
            folder.mkdir(parents=True, exist_ok=True)
            print(f"START {c} seed={s}", flush=True)
            with (folder / "console.log").open("x") as output:
                subprocess.run([sys.executable, "-u", "-m", "spacinglab.study7", "--one", c, str(s)],
                               cwd=ROOT, stdout=output, stderr=subprocess.STDOUT, check=True,
                               env={**os.environ, "HF_HUB_OFFLINE": "1", "TOKENIZERS_PARALLELISM": "false"})
            load_log(c, s)
            other = "random" if c == "spaced" else "spaced"
            if (OUT / f"{other}_s{s}" / "log.json").exists():
                validate_pair(load_log("spaced", s), load_log("random", s))
            print(f"COMPLETE {c} seed={s}", flush=True)
        analyze()
        print("STUDY7_DONE", flush=True)


if __name__ == "__main__":
    main()
