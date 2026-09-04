#!/bin/zsh
# Main pre-registered runs: 4 gap conditions x 3 seeds + 1 replicate (spaced, seed 0).
# K, lr and interference dose come from the pilot amendments (see PREREGISTRATION.md).
set -e
cd "$(dirname "$0")/.."
K=${K:-5}; LR=${LR:-1e-4}; NB=${NB:-15}
for seed in 0 1 2; do
  for cond in massed gap4 gap16 spaced; do
    echo "=== $cond seed=$seed ==="
    uv run python -m spacinglab.train --condition $cond --seed $seed --k $K --lr $LR \
      --n-int-facts $NB --out results/runs 2>&1 | grep -E "^\[eval\]|Traceback|Error"
  done
done
echo "=== replicate spaced seed=0 ==="
uv run python -m spacinglab.train --condition spaced --seed 0 --k $K --lr $LR \
  --n-int-facts $NB --tag replicate --out results/runs 2>&1 | grep -E "^\[eval\]|Traceback|Error"
echo MAIN_DONE
