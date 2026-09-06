"""Study 4 analysis (Amendment 7): canonical vs held-out-wording probe, four conditions, seeds 0-2."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze import INT_STEPS

SPREAD = 0.041  # Study 1 seed SD of the spaced-massed retention difference


def load(root: Path) -> pd.DataFrame:
    rows = []
    for p in sorted(root.glob("*/log.json")):
        L = json.loads(p.read_text()); c = L["config"]
        ev = {(e["phase"], e.get("int_step")): e for e in L["evals"]}
        imm = ev[("immediate", 0)]; ints = [ev[("interference", s)] for s in INT_STEPS]
        cond = c["condition"] + ("+para" if c["paraphrase"] else "")
        rows.append({
            "cond": cond, "seed": c["seed"],
            "canon_imm": imm["acc"], "canon_ret": float(np.mean([e["acc"] for e in ints])), "canon_end": ints[-1]["acc"],
            "held_imm": imm["heldout_acc"], "held_ret": float(np.mean([e["heldout_acc"] for e in ints])), "held_end": ints[-1]["heldout_acc"],
            "held_nll_ret": float(np.mean([e["heldout_nll"] for e in ints])),
            "held_disc_ret": float(np.mean([e["heldout_disc"] for e in ints])),
            "canon_disc_ret": float(np.mean([e["disc"] for e in ints])),
        })
    return pd.DataFrame(rows)


def pair(df, a, b, m):
    seeds = sorted(set(df[df.cond == a].seed) & set(df[df.cond == b].seed))
    d = np.array([float(df[(df.cond == a) & (df.seed == s)][m].iloc[0]) - float(df[(df.cond == b) & (df.seed == s)][m].iloc[0]) for s in seeds])
    return d, seeds


def rep(name, d, seeds):
    print(f"{name}: " + "  ".join(f"s{s}:{x:+.3f}" for s, x in zip(seeds, d)) + (f"  | mean {d.mean():+.3f}" if len(d) else ""))


def main() -> None:
    pd.set_option("display.width", 220)
    df = load(Path("results/study4"))
    if df.empty:
        print("no Study 4 runs yet"); return
    print("== per run: canonical probe vs held-out (unseen sixth wording) probe ==")
    print(df.sort_values(["seed", "cond"]).to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\n== mean by condition ==")
    print(df.groupby("cond")[["canon_imm", "canon_ret", "held_imm", "held_ret", "held_disc_ret", "canon_disc_ret"]].mean().to_string(float_format=lambda x: f"{x:.3f}"))
    print("\n== Amendment 7 decision (paired within seed; spread = 0.041) ==")
    for m, label in [("held_ret", "held-out retention"), ("held_imm", "held-out immediate"), ("held_disc_ret", "held-out discrimination")]:
        d, s = pair(df, "spaced+para", "spaced", m); rep(f"spaced+para − spaced ({label})", d, s)
    d, s = pair(df, "massed+para", "massed", "held_ret"); rep("massed+para − massed (held-out retention)", d, s)
    d2, s2 = pair(df, "spaced+para", "spaced", "held_ret")
    if len(d2) == 3:
        if (d2 > SPREAD).all():
            print("-> diversity BUYS GENERALISATION (prediction 2 holds 3/3)")
        elif (d2 <= SPREAD).sum() >= 2:
            print("-> diversity DOES NOT HELP even when probed fairly")
        else:
            print("-> PARTIAL")
    mp = df[df.cond == "massed+para"]
    if len(mp):
        print(f"guard, prediction 3: massed+para held-out retention = {mp.held_ret.mean():.3f}")
    print("prediction 1 (every condition lower on unseen wording than canonical):",
          bool((df.held_ret <= df.canon_ret + 1e-9).all()))
    # replication check against Study 1 / 2d canonical numbers
    print("\ncanonical-probe replication (this study vs earlier runs):")
    from .analyze import load_runs
    for cond, root in [("massed", "results/runs"), ("spaced", "results/runs"), ("massed+para", "results/study2d"), ("spaced+para", "results/study2d")]:
        old = load_runs(Path(root)); old = old[(old.tag == "") & (old.condition == cond.split("+")[0]) & (old.seed.isin([0, 1, 2]))]
        new = df[df.cond == cond]
        if len(new) and len(old):
            print(f"  {cond:12s} retention now {new.canon_ret.mean():.3f} vs before {old.retention_acc.mean():.3f}")


if __name__ == "__main__":
    main()
