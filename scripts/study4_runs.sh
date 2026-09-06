#!/bin/zsh
# Study 4 (Amendment 7): held-out wording probe. Per seed: massed+para, spaced+para, spaced, massed.
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|Traceback|Error"'
tr() { uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 700 --k 5 --lr 1e-4 --heldout-probe "$@" 2>&1 | eval $F; }
for s in 0 1 2; do
  echo "=== massed seed=$s para hp ==="; tr --condition massed --seed $s --paraphrase --out results/study4
  echo "=== spaced seed=$s para hp ==="; tr --condition spaced --seed $s --paraphrase --out results/study4
  echo "=== spaced seed=$s hp ===";      tr --condition spaced --seed $s --out results/study4
  echo "=== massed seed=$s hp ===";      tr --condition massed --seed $s --out results/study4
done
echo STUDY4_DONE
