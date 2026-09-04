# Resume note (2026-09-04, session stopped mid-run)

Main chain `scripts/main_runs.sh` was interrupted. Finished runs are in
`results/runs/*/log.json` (each has a `guards` block). To finish: delete any run
directory *without* a log.json, then rerun `scripts/main_runs.sh` — it re-runs every
run in order; comment out finished ones in the script, or run the missing
condition/seed pairs by hand:

    uv run python -m spacinglab.train --condition <massed|gap4|gap16|spaced> --seed <s> \
      --k 5 --lr 1e-4 --n-int-facts 50 --n-facts 200 --t-inj 700 --out results/runs

Then: `uv run python -m spacinglab.analyze`, `uv run python -m spacinglab.explore`,
`uv run python -m spacinglab.plot`, fill README.md placeholders.

Seeds 0-2 so far: massed 0.02-0.03 immediate / 0.00 final; spaced 0.65-0.68 / 0.12-0.20.
