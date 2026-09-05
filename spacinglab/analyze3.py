"""Study 3 analysis (Amendment 6): discrimination and savings, massed vs spaced, seeds 0-2."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .analyze import INT_STEPS


def load(root: Path) -> pd.DataFrame:
    rows = []
    for p in sorted(root.glob("*/log.json")):
        L = json.loads(p.read_text()); c = L["config"]
        ev = {(e["phase"], e.get("int_step")): e for e in L["evals"]}
        pre, imm = ev[("pretrained", None)], ev[("immediate", 0)]
        ints = [ev[("interference", s)] for s in INT_STEPS]
        end = ints[-1]
        r = L.get("relearn", {})
        rows.append({
            "condition": c["condition"], "seed": c["seed"],
            "disc_pretrained": pre["disc"], "disc_imm": imm["disc"], "disc_end": end["disc"],
            "disc_frac_end": end["disc_frac"],
            "nll_pretrained": pre["nll"], "nll_end": end["nll"], "nll_foil_end": end["nll_foil"],
            "acc_imm": imm["acc"], "acc_end": end["acc"],
            "retention_acc": float(np.mean([e["acc"] for e in ints])),
            "old_before": r["before_old"]["acc"], "old_after": r["after_old"]["acc"],
            "new_before": r["before_new"]["acc"], "new_after": r["after_new"]["acc"],
            "old_nll_after": r["after_old"]["nll"], "new_nll_after": r["after_new"]["nll"],
            "old_disc_after": r["after_old"]["disc"], "new_disc_after": r["after_new"]["disc"],
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["savings_acc"] = (df.old_after - df.old_before) - (df.new_after - df.new_before)
    df["old_gain"] = df.old_after - df.old_before
    df["new_gain"] = df.new_after - df.new_before
    return df


def main() -> None:
    pd.set_option("display.width", 220)
    df = load(Path("results/study3"))
    if df.empty:
        print("no Study 3 runs yet"); return
    cols = ["condition", "seed", "acc_imm", "acc_end", "retention_acc", "nll_pretrained", "nll_end", "nll_foil_end",
            "disc_pretrained", "disc_imm", "disc_end", "disc_frac_end"]
    print("== discrimination (NLL foil - NLL true; >0 = prefers this fact's answer) ==")
    print(df.sort_values(["seed", "condition"])[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    cols = ["condition", "seed", "old_before", "old_after", "old_gain", "new_before", "new_after", "new_gain",
            "savings_acc", "old_nll_after", "new_nll_after", "old_disc_after", "new_disc_after"]
    print("\n== savings: one re-exposure of every old fact vs one exposure of never-seen controls ==")
    print(df.sort_values(["seed", "condition"])[cols].to_string(index=False, float_format=lambda x: f"{x:.3f}"))

    m, s = df[df.condition == "massed"].sort_values("seed"), df[df.condition == "spaced"].sort_values("seed")
    print("\n== Amendment 6 decision ==")
    print(f"sanity: pretrained discrimination = {df.disc_pretrained.mean():+.3f} (must be ~0)")
    print("massed disc_end per seed:", " ".join(f"{x:+.2f}" for x in m.disc_end), "| spaced:", " ".join(f"{x:+.2f}" for x in s.disc_end))
    print("massed savings per seed:", " ".join(f"{x:+.3f}" for x in m.savings_acc), "| spaced:", " ".join(f"{x:+.3f}" for x in s.savings_acc))
    p1 = bool((m.disc_end > 0).all()) and bool((s.disc_end.values > m.disc_end.values).all())
    p2 = bool((m.savings_acc > 0.05).all())
    print(f"prediction 1 (massed disc>0 all seeds and spaced>massed): {p1}")
    print(f"prediction 2 (massed savings > 0.05 all seeds): {p2};  spaced savings > massed: {bool((s.savings_acc.values > m.savings_acc.values).all())}")
    if (m.disc_end > 0).all() and p2:
        print("-> massed memory is HIDDEN, NOT ERASED")
    elif (m.disc_end.abs() < 0.1).all() and (m.savings_acc.abs() < 0.05).all():
        print("-> massed memory is ERASED at every level we can see")
    else:
        print("-> PARTIAL: report both numbers as they are")
    fmt_drop = (df.nll_pretrained - df.nll_end)
    print(f"\nNLL drop from pretrained to end: massed {fmt_drop[df.condition=='massed'].mean():.2f}, of which discrimination accounts for "
          f"{m.disc_end.mean():.2f}; the rest ({fmt_drop[df.condition=='massed'].mean()-m.disc_end.mean():.2f}) also applies to the foil = format learning")


if __name__ == "__main__":
    main()
