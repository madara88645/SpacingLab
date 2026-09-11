#!/bin/zsh
# Pilot 2 (Amendment 1): interference = filler + 300 new facts. lr fixed at 1e-4. K in {4, 6}.
set -e
cd "$(dirname "$0")/.."
for k in 4 6; do
  echo "=== pilot2 k=$k lr=1e-4 ==="
  uv run python -m spacinglab.train --condition random --seed 100 --k $k --lr 1e-4 \
    --t-int 400 --tag pilot2 --out results/pilot 2>&1 | grep -E "^\[eval\]|Traceback|Error"
done
echo PILOT2_DONE
