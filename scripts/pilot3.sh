#!/bin/zsh
# Pilot 3: interference dose. k=5, lr=1e-4, full-length interference, set B size in {15, 50}.
set -e
cd "$(dirname "$0")/.."
for nb in 15 50; do
  echo "=== pilot3 k=5 lr=1e-4 n_int_facts=$nb ==="
  uv run python -m spacinglab.train --condition random --seed 100 --k 5 --lr 1e-4 \
    --n-int-facts $nb --tag pilot3 --out results/pilot 2>&1 | grep -E "^\[eval\]|Traceback|Error"
done
echo PILOT3_DONE
