#!/bin/zsh
# Finish the two runs interrupted on 2026-09-04.
set -e
cd "$(dirname "$0")/.."
K=5; LR=1e-4; NB=50; NA=200; TINJ=700
run() { echo "=== $1 seed=$2 $3 ==="; uv run python -m spacinglab.train --condition $1 --seed $2 --k $K --lr $LR \
  --n-int-facts $NB --n-facts $NA --t-inj $TINJ --out results/runs ${3:+--tag $3} 2>&1 | grep --line-buffered -E "^\[eval\]|^\[guard\]|Traceback|Error"; }
run gap16 2
run spaced 0 replicate
echo FINISH_DONE
