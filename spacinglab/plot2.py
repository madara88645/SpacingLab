"""Study 2 figure: one panel per sub-study, massed vs spaced accuracy curves, Study 1 as reference."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analyze import INT_STEPS, load_runs

XS = [0] + list(INT_STEPS)
COL = {"massed": "#3b82f6", "spaced": "#f59e0b"}


def curves(df, cond):
    sub = df[df.condition == cond]
    return np.array([[r["imm_acc"]] + r["curve_acc"] for _, r in sub.iterrows()]) if len(sub) else None


def panel(ax, df, title, ref=None):
    for c in ("massed", "spaced"):
        cv = curves(df, c)
        if cv is None:
            continue
        for row in cv:
            ax.plot(XS, row, color=COL[c], lw=0.8, alpha=0.35)
        ax.plot(XS, cv.mean(0), color=COL[c], lw=2, marker="o", ms=3.5, label=f"{c} (n={len(cv)})")
        if ref is not None and (rc := curves(ref, c)) is not None:
            ax.plot(XS, rc.mean(0), color=COL[c], lw=1.2, ls="--", alpha=0.7, label=f"{c}, Study 1")
    ax.set_title(title, fontsize=9)
    ax.set_xscale("symlog", linthresh=50)
    ax.set_xticks(XS); ax.set_xticklabels([str(x) for x in XS], fontsize=6, rotation=45); ax.minorticks_off()
    ax.set_ylim(-0.02, 0.8); ax.grid(alpha=0.2); ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=6, frameon=False)


def main(out: str = "results/study2.png") -> None:
    base = load_runs(Path("results/runs")); base = base[base.tag == ""]
    base3 = base[base.seed.isin([0, 1, 2])]
    panels = [
        ("results/study2a", "2a: Adam without momentum (beta1 = 0)"),
        ("results/study2b", "2b: LoRA rank 64, lr 1e-3 (floor: nothing survives interference)"),
        ("results/study2d", "2d: five different paraphrases instead of five copies"),
        ("results/contingency", "2c: massed with K = 10 and K = 20 exposures (seed 0)"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7.5), dpi=150)
    for ax, (root, title) in zip(axes.ravel(), panels):
        df = load_runs(Path(root)) if Path(root).exists() else None
        if df is None or df.empty:
            ax.set_title(title + " — no runs", fontsize=9); ax.axis("off"); continue
        if "contingency" in root:
            for (_, r), col in zip(df.sort_values("k").iterrows(), ("#7c3aed", "#0f766e")):
                ax.plot(XS, [r.imm_acc] + r.curve_acc, color=col, marker="o", ms=3.5, lw=2, label=f"massed K={r.k} (acc right after last exposure {r.acc_at_last:.2f})")
            sp = base[(base.condition == "spaced") & (base.seed == 0)].iloc[0]
            ax.plot(XS, [sp.imm_acc] + sp.curve_acc, color=COL["spaced"], ls="--", lw=1.2, label="spaced K=5, seed 0 (Study 1)")
            ax.set_title(title, fontsize=9); ax.set_xscale("symlog", linthresh=50)
            ax.set_xticks(XS); ax.set_xticklabels([str(x) for x in XS], fontsize=6, rotation=45); ax.minorticks_off()
            ax.set_ylim(-0.02, 0.8); ax.grid(alpha=0.2); ax.spines[["top", "right"]].set_visible(False); ax.legend(fontsize=6, frameon=False)
        else:
            panel(ax, df, title, ref=base3)
    for ax in axes[1]:
        ax.set_xlabel("interference steps after the injection window", fontsize=8)
    for ax in axes[:, 0]:
        ax.set_ylabel("exact-match accuracy, 200 facts", fontsize=8)
    fig.suptitle("Study 2: does the massed-vs-spaced gap survive changes to the optimiser, the adapter, the exposure count and the wording?", fontsize=9)
    fig.tight_layout()
    fig.savefig(out); print("wrote", out)


if __name__ == "__main__":
    main()
