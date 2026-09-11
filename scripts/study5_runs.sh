#!/bin/zsh
# Study 5 (Amendment 8): gap curve up to 256 in a 1400-step window. Resumable: skips finished runs.
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|Traceback|Error"'
for s in 0 1 2; do for c in massed spaced gap128 gap256 gap16; do
  d="results/study5/${c}_s${s}_lr0.0001_k5_w1400g256"
  if [ -f "$d/log.json" ]; then echo "=== $c seed=$s (done, skipped) ==="; continue; fi
  rm -rf "$d"; echo "=== $c seed=$s w1400 ==="
  uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 1400 --gap-max 256 --k 5 --lr 1e-4 \
    --condition $c --seed $s --out results/study5 2>&1 | eval $F
done; done
echo STUDY5_DONE
