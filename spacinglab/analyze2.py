"""Study 2 analysis (Amendment 5): 2a beta1=0, 2b LoRA, 2c contingency, 2d paraphrase.

Every comparison is paired within seed against Study 1's massed/spaced run of the same
seed (results/runs). Decision rules are the ones written in Amendment 5.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze import load_runs

SEEDS = (0, 1, 2)


def fmt(x: float) -> str:
    return "nan" if x is None or np.isnan(x) else f"{x:.3f}"


def summary(df: pd.DataFrame, label: str) -> None:
    cols = ["condition", "seed", "imm_acc", "retention_acc", "final_acc", "retention_nll",
            "acc_at_last", "cond_retention", "dtheta_imm", "fact_tokens", "steps"]
    cols = [c for c in cols if c in df.columns]
    print(f"\n-- {label}: per run --")
    print(df.sort_values(["seed", "condition"])[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))


def paired(a: pd.DataFrame, b: pd.DataFrame, metric: str) -> tuple[np.ndarray, list[int]]:
    """a - b per common seed."""
    seeds = sorted(set(a.seed) & set(b.seed))
    d = np.array([float(a[a.seed == s][metric].iloc[0]) - float(b[b.seed == s][metric].iloc[0]) for s in seeds])
    return d, seeds


def report_delta(name: str, d: np.ndarray, seeds: list[int]) -> None:
    print(f"{name}: " + "  ".join(f"s{s}:{x:+.3f}" for s, x in zip(seeds, d))
          + f"  | mean {d.mean():+.3f}  SD {d.std(ddof=1) if len(d) > 1 else float('nan'):.3f}")


def study1_baseline(base: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, float, float]:
    m = base[(base.condition == "massed") & (base.tag == "")]
    s = base[(base.condition == "spaced") & (base.tag == "")]
    d, _ = paired(s, m, "retention_acc")
    rep = base[base.tag == "replicate"]
    noise = float("nan")
    if len(rep):
        s0 = s[s.seed == 0].retention_acc.iloc[0]
        noise = abs(float(rep.retention_acc.iloc[0]) - float(s0))
    return m, s, float(d.mean()), noise


def study2a(base, root: Path) -> None:
    df = load_runs(root)
    if df.empty:
        print("\n== 2a: no runs yet =="); return
    summary(df, "2a beta1=0")
    m0, s0, d1, _ = study1_baseline(base)
    m, s = df[df.condition == "massed"], df[df.condition == "spaced"]
    d, seeds = paired(s, m, "retention_acc")
    print(f"\n== 2a decision (Study 1 Δ = {d1:+.3f}) ==")
    report_delta("retention Δ(spaced-massed) at beta1=0", d, seeds)
    di, _ = paired(s, m, "imm_acc"); report_delta("immediate Δ at beta1=0", di, seeds)
    massed_imm = float(m.imm_acc.mean())
    print(f"massed immediate acc at beta1=0: {massed_imm:.3f} (Study 1: {m0.imm_acc.mean():.3f})")
    if d.mean() < 0.5 * d1 and massed_imm > 0.30:
        print("-> momentum is a MAJOR part of the mechanism (both criteria met)")
    elif d.mean() < 0.5 * d1 or massed_imm > 0.30:
        print("-> PARTIAL: one of the two criteria met")
    else:
        print("-> momentum is NOT the main mechanism")


def study2b(base, root: Path) -> None:
    df = load_runs(root)
    if df.empty:
        print("\n== 2b: no runs yet =="); return
    summary(df, f"2b LoRA (rank from config)")
    m, s = df[df.condition == "massed"], df[df.condition == "spaced"]
    d, seeds = paired(s, m, "retention_acc")
    _, _, _, noise = study1_baseline(base)
    print(f"\n== 2b decision (noise band from Study 1 replicate = {fmt(noise)}) ==")
    report_delta("retention Δ(spaced-massed) LoRA", d, seeds)
    di, _ = paired(s, m, "imm_acc"); report_delta("immediate Δ LoRA", di, seeds)
    r1 = bool((d > 0).all()); r2 = bool(d.mean() > d.std(ddof=1) and d.mean() > noise)
    r3 = bool(abs(di.mean()) < abs(d.mean()))
    print(f"rule1 every seed spaced>massed: {r1}   rule2 mean>SD and >noise: {r2}   rule3 |imm Δ|<|ret Δ| (reported only): {r3}")
    print("-> spacing effect REPLICATES under LoRA" if r1 and r2 else "-> spacing effect does NOT replicate under LoRA")


def study2c(base, root: Path) -> None:
    df = load_runs(root)
    if df.empty:
        print("\n== 2c: no runs yet =="); return
    summary(df, "2c contingency massed K=10/20 seed 0")
    _, s, _, _ = study1_baseline(base)
    sp = s[s.seed == 0].iloc[0]
    print(f"\n== 2c decision: spaced seed0 immediate={sp.imm_acc:.3f}, retention={sp.retention_acc:.3f} ==")
    for _, r in df.sort_values("k").iterrows():
        reached = abs(r.imm_acc - sp.imm_acc) <= 0.05
        print(f"massed K={r.k}: immediate {r.imm_acc:.3f}  retention {r.retention_acc:.3f}  acc_at_last {fmt(r.get('acc_at_last', float('nan')))}"
              f"  -> learning-matched: {'YES' if reached else 'no'}")


def study2d(base, root: Path) -> None:
    df = load_runs(root)
    if df.empty:
        print("\n== 2d: no runs yet =="); return
    summary(df, "2d paraphrase")
    m0, s0, _, noise = study1_baseline(base)
    d_ms, _ = paired(s0, m0, "retention_acc"); spread = float(d_ms.std(ddof=1))
    mp, sp = df[df.condition == "massed"], df[df.condition == "spaced"]
    print(f"\n== 2d decision (seed spread of Study 1 Δ = {spread:.3f}, noise band = {fmt(noise)}) ==")
    a, seeds = paired(mp, m0, "retention_acc"); report_delta("massed+para − massed", a, seeds)
    b, seeds = paired(mp, s0, "retention_acc"); report_delta("massed+para − spaced", b, seeds)
    c, seeds = paired(sp, s0, "retention_acc"); report_delta("spaced+para − spaced", c, seeds)
    for name, x, y in [("massed+para − massed (NLL, lower better)", mp, m0), ("spaced+para − spaced (NLL)", sp, s0)]:
        dn, sd = paired(x, y, "retention_nll"); report_delta(name, dn, sd)
    if len(a) and (a > spread).all():
        verdict = "diversity FULLY substitutes" if (b >= -spread).all() else "diversity PARTIALLY substitutes"
    else:
        verdict = "NO substitution (massed+para not reliably above massed)"
    print("->", verdict)
    if len(c):
        print("-> additive on top of spacing" if (c > spread).all() else "-> not additive on top of spacing (within spread)")
    if len(df):
        print(f"fact tokens: para {df.fact_tokens.mean():.0f} vs Study 1 {m0.fact_tokens.mean():.0f} ({(df.fact_tokens.mean()/m0.fact_tokens.mean()-1)*100:+.1f}%)")


def main() -> None:
    pd.set_option("display.width", 220)
    base = load_runs(Path("results/runs"))
    study2c(base, Path("results/contingency"))
    study2a(base, Path("results/study2a"))
    study2b(base, Path("results/study2b"))
    study2d(base, Path("results/study2d"))


if __name__ == "__main__":
    main()
