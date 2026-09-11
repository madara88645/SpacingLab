#!/bin/zsh
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
for s in 0 1 2; do
  d="results/study6/random_s${s}_lr0.0001_k5"; [ -f "$d/log.json" ] && continue; rm -rf "$d"
  echo "=== random seed=$s ==="
  uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 700 --k 5 --lr 1e-4 --condition random --seed $s --out results/study6 2>&1 | grep --line-buffered -E "^\[eval\]|^\[guard\]|Traceback|Error"
done
echo STUDY6_DONE
