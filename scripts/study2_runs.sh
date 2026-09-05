#!/bin/zsh
# Study 2 (Amendment 5). Waits for any running training to finish first.
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
NB=50; NA=200; TINJ=700
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|^\[lora\]|Traceback|Error"'
tr() { uv run python -m spacinglab.train --n-int-facts $NB --n-facts $NA --t-inj $TINJ "$@" 2>&1 | eval $F; }

echo "##### 2c contingency: massed K=10,20 seed 0 (p_i drawn as for K=5)"
for K in 10 20; do echo "=== massed_matched seed=0 K=$K ==="; tr --condition massed --seed 0 --k $K --k-last 5 --lr 1e-4 --out results/contingency --tag matchedK$K; done

echo "##### 2a momentum ablation: beta1=0"
for s in 0 1 2; do for c in massed spaced; do echo "=== $c seed=$s beta1=0 ==="; tr --condition $c --seed $s --k 5 --lr 1e-4 --beta1 0.0 --out results/study2a; done; done

echo "##### 2b LoRA pilot (calibration only)"
for lr in 3e-4 1e-3; do echo "=== lora pilot lr=$lr ==="; tr --condition random --seed 100 --k 5 --lr $lr --lora-r 16 --t-int 400 --out results/pilot_lora --tag pilot; done
LR=$(uv run python - <<'PY'
import json,glob
best=None; cands=[]
for p in glob.glob("results/pilot_lora/*/log.json"):
    L=json.load(open(p)); lr=L["config"]["lr"]
    imm=[e for e in L["evals"] if e["phase"]=="immediate"][0]["acc"]
    a400=[e for e in L["evals"] if e.get("int_step")==400][0]["acc"]
    cands.append((lr,imm,a400))
ok=[c for c in cands if 0.5<=c[1]<=0.95 and c[2]>=0.10]
pick=min(ok)[0] if ok else min(cands,key=lambda c:abs(c[1]-0.7))[0]
print(f"{pick:g}")
import sys; print("pilot_lora:",cands,"->",pick,file=sys.stderr)
PY
)
echo "LORA_LR_SELECTED=$LR"
echo "##### 2b LoRA main: massed vs spaced, seeds 0-2, lr=$LR"
for s in 0 1 2; do for c in massed spaced; do echo "=== $c seed=$s lora16 lr=$LR ==="; tr --condition $c --seed $s --k 5 --lr $LR --lora-r 16 --out results/study2b; done; done
echo STUDY2_DONE
