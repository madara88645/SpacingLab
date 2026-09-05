#!/bin/zsh
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|^\[lora\]|Traceback|Error"'
tr() { uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 700 "$@" 2>&1 | eval $F; }
echo "##### 2b LoRA pilot, rank 64 (Amendment 5c)"
echo "=== lora pilot r=64 lr=1e-3 ==="; tr --condition random --seed 100 --k 5 --lr 1e-3 --lora-r 64 --t-int 400 --out results/pilot_lora --tag pilot
SEL=$(uv run python - <<'PY'
import json,glob,sys
cands=[]
for p in glob.glob("results/pilot_lora/*/log.json"):
    L=json.load(open(p)); c=L["config"]
    imm=[e for e in L["evals"] if e["phase"]=="immediate"][0]["acc"]
    a400=[e for e in L["evals"] if e.get("int_step")==400][0]["acc"]
    cands.append((c["lr"],c["lora_r"],imm,a400))
ok=[c for c in cands if 0.5<=c[2]<=0.95 and c[3]>=0.10]
pick=min(ok)[:2] if ok else min(cands,key=lambda c:abs(c[2]-0.7))[:2]
print(f"{pick[0]:g} {pick[1]}"); print("pilot_lora:",sorted(cands),"->",pick,file=sys.stderr)
PY
)
LR=${SEL% *}; R=${SEL#* }
echo "LORA_LR_SELECTED=$LR LORA_R_SELECTED=$R"
echo "##### 2b LoRA main: massed vs spaced, seeds 0-2, lr=$LR r=$R"
for s in 0 1 2; do for c in massed spaced; do echo "=== $c seed=$s lora$R lr=$LR ==="; tr --condition $c --seed $s --k 5 --lr $LR --lora-r $R --out results/study2b; done; done
echo STUDY2_DONE
