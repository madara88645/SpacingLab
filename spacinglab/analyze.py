"""Apply the pre-registered analysis to results/runs/*/log.json.

Primary: retention score = mean exact-match accuracy over the 7 interference checkpoints.
Everything is paired within seed; spread is reported next to every mean.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

CONDS = ["massed", "gap4", "gap16", "spaced"]
INT_STEPS = (50, 100, 200, 400, 800, 1200, 1500)


def load_runs(root: Path) -> pd.DataFrame:
    rows = []
    for p in sorted(root.glob("*/log.json")):
        log = json.loads(p.read_text())
        cfg = log["config"]
        ev = {(e["phase"], e.get("int_step")): e for e in log["evals"]}
        imm = ev[("immediate", 0)]
        ints = [ev[("interference", s)] for s in INT_STEPS if ("interference", s) in ev]
        rows.append({
            "run": p.parent.name, "condition": cfg["condition"], "seed": cfg["seed"],
            "tag": cfg["tag"], "lr": cfg["lr"], "k": cfg["k"],
            "pre_acc": ev[("pre_injection", None)]["acc"],
            "imm_acc": imm["acc"], "imm_nll": imm["nll"],
            "retention_acc": float(np.mean([e["acc"] for e in ints])),
            "retention_nll": float(np.mean([e["nll"] for e in ints])),
            "final_acc": ints[-1]["acc"], "final_nll": ints[-1]["nll"],
            "holdout_imm": imm["holdout_loss"], "holdout_final": ints[-1]["holdout_loss"],
            "dtheta_imm": imm["param_dist"], "dtheta_end": ints[-1]["param_dist"],
            "fact_tokens": log["guards"]["fact_tokens_seen"],
            "filler_tokens": log["guards"]["filler_tokens_seen"],
            "steps": log["guards"]["optimizer_steps"],
            "curve_acc": [e["acc"] for e in ints], "curve_nll": [e["nll"] for e in ints],
            "b_acc_final": ints[-1].get("int_facts_acc"),
            **amendment4_fields(log, imm, ints),
        })
    return pd.DataFrame(rows)


def amendment4_fields(log: dict, imm: dict, ints: list[dict]) -> dict:
    """Encoding strength right after the last exposure, and retention conditional on it."""
    al = log.get("at_last_exposure")
    if not al:
        return {}
    enc = np.array([v["correct"] for v in al], dtype=bool)
    enc_nll = np.array([v["nll"] for v in al])
    out = {"acc_at_last": float(enc.mean()), "nll_at_last": float(enc_nll.mean()), "n_encoded": int(enc.sum())}
    def cond(e):
        c = np.array(e["per_fact_correct"], dtype=bool)
        return float(c[enc].mean()) if enc.any() else float("nan")
    out["cond_imm"] = cond(imm)
    out["cond_curve"] = [cond(e) for e in ints]
    out["cond_retention"] = float(np.mean(out["cond_curve"]))
    # NLL drift from at-last to immediate / mean over interference checkpoints
    out["dnll_imm"] = float(np.mean(np.array(imm["per_fact_nll"]) - enc_nll))
    out["dnll_retention"] = float(np.mean([np.mean(np.array(e["per_fact_nll"]) - enc_nll) for e in ints]))
    return out


def main(root: str = "results/runs") -> None:
    df = load_runs(Path(root))
    main_df = df[df.tag == ""].copy()
    rep = df[df.tag == "replicate"]
    pd.set_option("display.width", 200)
    cols = ["condition", "seed", "pre_acc", "imm_acc", "imm_nll", "retention_acc", "retention_nll",
            "final_acc", "dtheta_imm", "dtheta_end", "holdout_final", "fact_tokens", "filler_tokens", "steps"]
    print("== per run ==")
    print(main_df.sort_values(["seed", "condition"])[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    # guards: equal steps / tokens across conditions within a seed
    for seed, g in main_df.groupby("seed"):
        assert g.steps.nunique() == 1 and g.fact_tokens.nunique() == 1 and g.filler_tokens.nunique() == 1, seed
        assert (g.pre_acc == 0).all(), ("pre-injection accuracy not zero", seed)
    print("\nguards: steps, fact tokens, filler tokens identical within every seed; pre-injection acc = 0")

    print("\n== mean over seeds (min..max) ==")
    for metric in ["imm_acc", "retention_acc", "final_acc", "imm_nll", "retention_nll", "dtheta_imm"]:
        line = f"{metric:>14}: "
        for c in CONDS:
            v = main_df[main_df.condition == c][metric]
            line += f"{c}={v.mean():.3f} ({v.min():.3f}..{v.max():.3f})  "
        print(line)

    # paired differences spaced - massed per seed
    piv = main_df.pivot(index="seed", columns="condition", values="retention_acc")
    piv_imm = main_df.pivot(index="seed", columns="condition", values="imm_acc")
    d = piv["spaced"] - piv["massed"]
    d_imm = piv_imm["spaced"] - piv_imm["massed"]
    print("\n== paired spaced - massed, per seed ==")
    for s in piv.index:
        print(f"seed {s}: retention Δ={d[s]:+.3f}   immediate Δ={d_imm[s]:+.3f}")
    sd = d.std(ddof=1) if len(d) > 1 else float("nan")
    print(f"mean retention Δ = {d.mean():+.3f}, SD across seeds = {sd:.3f}")

    noise = float("nan")
    if len(rep):
        r = rep.iloc[0]
        orig = main_df[(main_df.condition == r.condition) & (main_df.seed == r.seed)].iloc[0]
        noise = abs(r.retention_acc - orig.retention_acc)
        print(f"replication noise band (|Δ retention| same seed/condition rerun): {noise:.3f} "
              f"(immediate |Δ| = {abs(r.imm_acc - orig.imm_acc):.3f})")

    # monotonicity across gaps (supporting)
    from scipy.stats import spearmanr  # noqa
    print("\n== monotonicity: Spearman(retention, log gap) per seed ==")
    gaps = np.log([1, 4, 16, 64])
    for s in piv.index:
        rho = spearmanr(gaps, piv.loc[s, CONDS].values).statistic
        print(f"seed {s}: rho={rho:+.2f}  retention by gap = " + " ".join(f"{piv.loc[s, c]:.3f}" for c in CONDS))

    if "acc_at_last" in main_df:
        print("\n== Amendment 4: encoding right after the last exposure, and conditional retention ==")
        for metric in ["acc_at_last", "nll_at_last", "cond_imm", "cond_retention", "dnll_imm", "dnll_retention"]:
            line = f"{metric:>15}: "
            for c in CONDS:
                v = main_df[main_df.condition == c][metric]
                if len(v):
                    line += f"{c}={v.mean():.3f} ({v.min():.3f}..{v.max():.3f})  "
            print(line)
        pc = main_df.pivot(index="seed", columns="condition", values="cond_retention")
        pe = main_df.pivot(index="seed", columns="condition", values="acc_at_last")
        print("paired spaced - massed per seed: conditional retention / encoding")
        for s_ in pc.index:
            print(f"  seed {s_}: cond Δ={pc.loc[s_, 'spaced'] - pc.loc[s_, 'massed']:+.3f}   "
                  f"encoding Δ={pe.loc[s_, 'spaced'] - pe.loc[s_, 'massed']:+.3f}")

    print("\n== pre-registered decision rule ==")
    r1 = bool((d > 0).all())
    r2 = bool(d.mean() > sd and (np.isnan(noise) or d.mean() > noise))
    r3 = bool(abs(d_imm.mean()) < abs(d.mean()))
    print(f"rule 1 (every seed spaced > massed): {r1}")
    print(f"rule 2 (mean Δ > seed SD and > noise band): {r2}")
    print(f"rule 3 (|immediate Δ| < |retention Δ|): {r3}   (immediate Δ mean = {d_imm.mean():+.3f})")
    print("H1 SUPPORTED" if r1 and r2 and r3 else "H1 NOT SUPPORTED")


if __name__ == "__main__":
    main(*sys.argv[1:])
