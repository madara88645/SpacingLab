#!/bin/zsh
# Main pre-registered runs (Amendment 2): core comparison massed vs spaced on seeds 0-4,
# gap4/gap16 on seeds 0-2, one replicate (spaced, seed 0). Core comparison runs first.
set -e
cd "$(dirname "$0")/.."
K=5; LR=1e-4; NB=50; NA=200
run() { echo "=== $1 seed=$2 $3 ==="; uv run python -m spacinglab.train --condition $1 --seed $2 --k $K --lr $LR \
  --n-int-facts $NB --n-facts $NA --out results/runs ${3:+--tag $3} 2>&1 | grep --line-buffered -E "^\[eval\]|Traceback|Error"; }
for seed in 0 1 2 3 4; do run massed $seed; run spaced $seed; done
for seed in 0 1 2; do run gap4 $seed; run gap16 $seed; done
run spaced 0 replicate
echo MAIN_DONE
