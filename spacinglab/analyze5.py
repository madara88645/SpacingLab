"""Study 5 analysis (Amendment 8): gap curve {1,16,64,128,256} in a 1400-step window."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from .analyze import load_runs

GAP = {"massed": 1, "gap16": 16, "spaced": 64, "gap128": 128, "gap256": 256}
SPREAD = 0.041


def main() -> None:
    df = load_runs(Path("results/study5"))
    if df.empty:
        print("no Study 5 runs yet"); return
    df["gap"] = df.condition.map(GAP)
    piv = df.pivot(index="seed", columns="gap", values="retention_acc").sort_index(axis=1)
    print("== retention score by gap (rows = seeds) ==")
    print(piv.to_string(float_format=lambda x: f"{x:.3f}"))
    print("\nmean:", "  ".join(f"gap{g}={piv[g].mean():.3f}" for g in piv.columns))
    for m in ("imm_acc", "final_acc", "acc_at_last"):
        if m in df.columns:
            pv = df.pivot(index="seed", columns="gap", values=m).sort_index(axis=1)
            print(f"{m:12s} mean:", "  ".join(f"gap{g}={pv[g].mean():.3f}" for g in pv.columns))
    full = piv.dropna()
    if len(full) == 0:
        return
    print("\n== Amendment 8 decision (paired per seed, spread 0.041) ==")
    if {1, 16, 64} <= set(full.columns):
        print("prediction 1 (1<16<64 every seed):", bool(((full[16] > full[1]) & (full[64] > full[16])).all()))
    if {64, 128} <= set(full.columns):
        d = full[128] - full[64]
        print("prediction 2 (128 > 64):", "  ".join(f"s{s}:{x:+.3f}" for s, x in d.items()), "->", "holds 3/3" if (d > SPREAD).all() else ("fails" if (d.abs() <= SPREAD).sum() >= 2 or (d < -SPREAD).all() else "partial"))
    if {64, 128, 256} <= set(full.columns):
        d2 = full[256] - full[128]; d1 = full[128] - full[64]
        print("prediction 3 (diminishing returns, (256-128) < (128-64) every seed):", bool((d2 < d1).all()))
        print("Δ(256-128):", "  ".join(f"s{s}:{x:+.3f}" for s, x in d2.items()))
        if (d2 > SPREAD).all():
            print("-> benefit KEEPS RISING through 256")
        elif (d2.abs() <= SPREAD).sum() >= 2:
            print("-> benefit SATURATES between 128 and 256")
        elif (d2 < -SPREAD).all():
            print("-> benefit DECLINES past 128 (inverted U)")
        else:
            print("-> mixed; report as is")
    m = df[df.condition == "massed"]
    if len(m):
        print(f"guard, prediction 4: massed immediate acc = {m.imm_acc.mean():.3f}, at-last = {m.acc_at_last.mean():.3f}")
    for seed, g in df.groupby("seed"):
        assert g.steps.nunique() == 1 and g.fact_tokens.nunique() == 1, seed
    print("guards: steps and fact tokens identical within seed")


if __name__ == "__main__":
    main()
