#!/bin/zsh
# Study 2d (paraphrase). Waits for study2_runs.sh to finish.
set -e
cd "$(dirname "$0")/.."
while ! grep -q STUDY2_DONE results/study2.log 2>/dev/null; do sleep 30; done
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|Traceback|Error"'
tr() { uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 700 --k 5 --lr 1e-4 "$@" 2>&1 | eval $F; }
for s in 0 1 2; do for c in massed spaced; do echo "=== $c seed=$s paraphrase ==="; tr --condition $c --seed $s --paraphrase --out results/study2d; done; done
echo STUDY2D_DONE
