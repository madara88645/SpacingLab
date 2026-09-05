#!/bin/zsh
# Pre-declared contingency (PREREGISTRATION.md "Contingency"): rule 3 failed because
# massed learned less immediately. Bounded probe on seed 0: massed with K=10 and K=20.
# Waits for finish_runs.sh to end so MPS is not shared.
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
LR=1e-4; NB=50; NA=200; TINJ=700
for K in 10 20; do
  echo "=== massed_matched seed=0 K=$K ==="
  uv run python -m spacinglab.train --condition massed --seed 0 --k $K --lr $LR \
    --n-int-facts $NB --n-facts $NA --t-inj $TINJ --out results/contingency --tag matchedK$K 2>&1 \
    | grep --line-buffered -E "^\[eval\]|^\[guard\]|Traceback|Error"
done
echo CONTINGENCY_DONE
