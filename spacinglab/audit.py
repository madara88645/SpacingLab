"""Study 6a: effective-weight audit from reconstructed schedules (no training).

Per-step loss is a mean over sequences (15 filler + n facts), so each fact exposure in
a step carries weight 1/(15+n). Reconstruct every Study 1 / Study 5 schedule from seed +
condition and compare the distribution of n and of the per-exposure weight.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .schedule import draw_last_exposures, gap_schedule, random_schedule

FILLER = 15


def audit(cond_gaps: dict[str, int], t_inj: int, gap_max: int, seeds=(0, 1, 2, 3, 4), k=5, n_facts=200):
    rows = []
    for seed in seeds:
        last = draw_last_exposures(n_facts, k, gap_max, t_inj, seed=seed)
        scheds = {c: gap_schedule(last, k, g) for c, g in cond_gaps.items()}
        scheds["random"] = random_schedule(n_facts, k, t_inj, seed=seed)
        for c, sched in scheds.items():
            n = np.zeros(t_inj, dtype=int)
            for step, facts in sched.items():
                n[step] = len(facts)
            w = 1.0 / (FILLER + n)                      # weight of one fact sequence in that step's loss
            exp_w = np.repeat(w, n)                     # one entry per exposure
            rows.append({
                "condition": c, "seed": seed, "steps_with_facts": int((n > 0).sum()),
                "mean_facts_per_step": n.mean(), "max_facts_per_step": int(n.max()),
                "mean_facts_when_present": n[n > 0].mean(),
                "mean_weight_per_exposure": exp_w.mean(), "min_weight": exp_w.min(),
                "total_fact_weight": exp_w.sum(),
            })
    return pd.DataFrame(rows)


def main() -> None:
    pd.set_option("display.width", 200)
    for label, gaps, t_inj, gmax, seeds in [
        ("Study 1 window (700 steps, gap_max 64)", {"massed": 1, "gap4": 4, "gap16": 16, "spaced": 64}, 700, 64, (0, 1, 2, 3, 4)),
        ("Study 5 window (1400 steps, gap_max 256)", {"massed": 1, "gap16": 16, "spaced": 64, "gap128": 128, "gap256": 256}, 1400, 256, (0, 1, 2)),
    ]:
        df = audit(gaps, t_inj, gmax, seeds)
        print(f"== {label} ==")
        g = df.groupby("condition").agg(
            steps_with_facts=("steps_with_facts", "mean"), mean_facts_per_step=("mean_facts_per_step", "mean"),
            max_facts_per_step=("max_facts_per_step", "max"), mean_facts_when_present=("mean_facts_when_present", "mean"),
            mean_weight_per_exposure=("mean_weight_per_exposure", "mean"), min_weight=("min_weight", "min"),
            total_fact_weight=("total_fact_weight", "mean"),
        )
        print(g.to_string(float_format=lambda x: f"{x:.4f}"))
        m, s = g.loc["massed", "mean_weight_per_exposure"], g.loc["spaced", "mean_weight_per_exposure"]
        print(f"massed vs spaced mean per-exposure weight: {m:.4f} vs {s:.4f} ({(m/s-1)*100:+.1f} %); "
              f"total fact weight {g.loc['massed','total_fact_weight']:.2f} vs {g.loc['spaced','total_fact_weight']:.2f}\n")


if __name__ == "__main__":
    main()
