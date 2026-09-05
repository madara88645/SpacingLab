#!/bin/zsh
# 2b LoRA: extended pilot (Amendment 5b) then main runs. Waits for running training.
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|^\[lora\]|Traceback|Error"'
tr() { uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 700 "$@" 2>&1 | eval $F; }
echo "##### 2b LoRA pilot, extended grid (Amendment 5b)"
for lr in 3e-3 1e-2; do echo "=== lora pilot lr=$lr ==="; tr --condition random --seed 100 --k 5 --lr $lr --lora-r 16 --t-int 400 --out results/pilot_lora --tag pilot; done
LR=$(uv run python - <<'PY'
import json,glob,sys
cands=[]
for p in glob.glob("results/pilot_lora/*/log.json"):
    L=json.load(open(p)); lr=L["config"]["lr"]
    imm=[e for e in L["evals"] if e["phase"]=="immediate"][0]["acc"]
    a400=[e for e in L["evals"] if e.get("int_step")==400][0]["acc"]
    cands.append((lr,imm,a400))
ok=[c for c in cands if 0.5<=c[1]<=0.95 and c[2]>=0.10]
pick=min(ok)[0] if ok else min(cands,key=lambda c:abs(c[1]-0.7))[0]
print(f"{pick:g}"); print("pilot_lora:",sorted(cands),"->",pick,file=sys.stderr)
PY
)
echo "LORA_LR_SELECTED=$LR"
echo "##### 2b LoRA main: massed vs spaced, seeds 0-2, lr=$LR"
for s in 0 1 2; do for c in massed spaced; do echo "=== $c seed=$s lora16 lr=$LR ==="; tr --condition $c --seed $s --k 5 --lr $LR --lora-r 16 --out results/study2b; done; done
echo STUDY2_DONE
