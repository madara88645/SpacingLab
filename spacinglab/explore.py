"""Exploratory (not pre-registered) analyses, labelled as such in the write-up.

1. Within-window forgetting curve: at the immediate evaluation, each fact has waited
   (T_inj - p_i) steps since its last exposure. Survival vs that delay, per condition.
2. Encoding-matched survival: among facts whose NLL right after the last exposure was
   below a threshold (strongly encoded), fraction still correct at the immediate
   evaluation, per condition. Separates "weaker encoding" from "fragile encoding".
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

CONDS = ["massed", "gap4", "gap16", "spaced"]


def load(root: Path) -> pd.DataFrame:
    rows = []
    for p in sorted(root.glob("*/log.json")):
        log = json.loads(p.read_text())
        cfg = log["config"]
        if cfg["tag"] or "at_last_exposure" not in log:
            continue
        imm = next(e for e in log["evals"] if e["phase"] == "immediate")
        fin = log["evals"][-1]
        last = np.array(log["last_exposure"])
        for i in range(cfg["n_facts"]):
            al = log["at_last_exposure"][i]
            rows.append({
                "condition": cfg["condition"], "seed": cfg["seed"], "fact": i,
                "delay": cfg["t_inj"] - last[i],
                "enc_correct": al["correct"], "enc_nll": al["nll"],
                "imm_correct": imm["per_fact_correct"][i], "imm_nll": imm["per_fact_nll"][i],
                "final_correct": fin["per_fact_correct"][i], "final_nll": fin["per_fact_nll"][i],
            })
    return pd.DataFrame(rows)


def main(root: str = "results/runs") -> None:
    df = load(Path(root))
    conds = [c for c in CONDS if c in set(df.condition)]
    print("== 1. survival at the immediate eval vs steps since the fact's last exposure (all seeds pooled) ==")
    bins = [0, 50, 100, 200, 300, 450]
    df["delay_bin"] = pd.cut(df.delay, bins, right=False)
    tab = df.groupby(["delay_bin", "condition"], observed=True).imm_correct.mean().unstack()[conds]
    n = df.groupby(["delay_bin"], observed=True).size() // len(conds) if len(conds) else None
    print(tab.round(3).to_string())
    print("facts per bin per condition ≈", (df[df.condition == conds[0]].groupby("delay_bin", observed=True).size()).to_dict())

    print("\n== 2. encoding-matched survival: facts with NLL right after last exposure < threshold ==")
    for thr in [0.1, 0.3, 1.0]:
        line = f"enc_nll < {thr:<4}: "
        for c in conds:
            sub = df[(df.condition == c) & (df.enc_nll < thr)]
            line += f"{c}: n={len(sub):4d} imm={sub.imm_correct.mean():.3f} final={sub.final_correct.mean():.3f}   "
        print(line)

    print("\n== 3. encoding strength: NLL right after last exposure, quartiles per condition ==")
    print(df.groupby("condition").enc_nll.describe()[["mean", "25%", "50%", "75%"]].loc[conds].round(3).to_string())

    print("\n== 4. what massed facts say instead (immediate eval, seed 0, first 8 wrong) ==")
    p = next(iter(sorted(Path(root).glob("massed_s0_*/log.json"))), None)
    if p:
        log = json.loads(p.read_text())
        imm = next(e for e in log["evals"] if e["phase"] == "immediate")
        shown = 0
        for i, f in enumerate(log["facts"]):
            if not imm["per_fact_correct"][i]:
                print(f"  {f['prompt']!r:55} answer={f['answer']!r:14} model={imm['per_fact_generated'][i]!r}")
                shown += 1
                if shown == 8:
                    break


if __name__ == "__main__":
    main(*sys.argv[1:])
