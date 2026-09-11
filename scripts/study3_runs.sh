#!/bin/zsh
# Study 3 (Amendment 6): discrimination + savings. massed/spaced × seeds 0-2.
set -e
cd "$(dirname "$0")/.."
while pgrep -f "spacinglab.train" >/dev/null; do sleep 20; done
F='grep --line-buffered -E "^\[eval\]|^\[guard\]|^\[relearn\]|Traceback|Error"'
tr() { uv run python -m spacinglab.train --n-int-facts 50 --n-facts 200 --t-inj 700 --k 5 --lr 1e-4 --relearn "$@" 2>&1 | eval $F; }
for s in 0 1 2; do for c in massed spaced; do echo "=== $c seed=$s relearn ==="; tr --condition $c --seed $s --out results/study3; done; done
echo STUDY3_DONE
