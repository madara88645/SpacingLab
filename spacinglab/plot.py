"""Retention curves for the write-up: mean over seeds per condition, seeds as thin lines.

Palette validated with the dataviz checks (light surface); series are also
direct-labeled so identity is never color-alone; a table view lives in results/.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analyze import CONDS, INT_STEPS, load_runs

COLORS = {"massed": "#2a78d6", "gap4": "#eb6834", "gap16": "#1baf7a", "spaced": "#eda100"}
LABEL = {"massed": "massed (gap 1)", "gap4": "gap 4", "gap16": "gap 16", "spaced": "spaced (gap 64)"}


def main(root: str = "results/runs", out: str = "results/retention.png") -> None:
    df = load_runs(Path(root))
    df = df[df.tag == ""]
    xs = [0] + list(INT_STEPS)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
    for ax, key, imm_key, ylabel in [
        (axes[0], "curve_acc", "imm_acc", "exact-match accuracy on the 200 injected facts"),
        (axes[1], "curve_nll", "imm_nll", "answer NLL per token (lower = better remembered)"),
    ]:
        for c in CONDS:
            sub = df[df.condition == c]
            if not len(sub):
                continue
            curves = np.array([[r[imm_key]] + r[key] for _, r in sub.iterrows()])
            for cv in curves:
                ax.plot(xs, cv, color=COLORS[c], lw=0.8, alpha=0.35)
            m = curves.mean(0)
            ax.plot(xs, m, color=COLORS[c], lw=2, marker="o", ms=4, label=f"{LABEL[c]} (n={len(sub)})")
            ax.annotate(LABEL[c], (xs[-1], m[-1]), xytext=(4, 0), textcoords="offset points",
                        fontsize=7, color="#52514e", va="center")
        ax.set_xlabel("interference steps after the injection window")
        ax.set_ylabel(ylabel, fontsize=8)
        ax.set_xscale("symlog", linthresh=50)
        ax.set_xticks(xs); ax.set_xticklabels([str(x) for x in xs], fontsize=7)
        ax.grid(alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
        ax.legend(fontsize=7, frameon=False)
    fig.suptitle("Spacing the 5 exposures of each fact: retention under new-fact interference "
                 "(thin = single seed, thick = mean)", fontsize=9)
    fig.tight_layout()
    Path(out).parent.mkdir(exist_ok=True)
    fig.savefig(out)
    print("wrote", out)


if __name__ == "__main__":
    main(*sys.argv[1:])
