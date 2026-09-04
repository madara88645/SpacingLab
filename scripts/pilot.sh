#!/bin/zsh
# Calibration pilot declared in PREREGISTRATION.md: random placement, seed 100,
# interference shortened to 400 steps, grid lr x K. Never compares gaps.
set -e
cd "$(dirname "$0")/.."
for k in 4 8; do
  for lr in 1e-4 3e-4; do
    echo "=== pilot k=$k lr=$lr ==="
    uv run python -m spacinglab.train --condition random --seed 100 --k $k --lr $lr \
      --t-int 400 --tag pilot --out results/pilot 2>&1 | grep -E "^\[eval\]|^step"
  done
done
echo PILOT_DONE
