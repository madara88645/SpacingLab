# SpacingLab: does spacing repetitions protect fine-tuned facts?

**Question.** When a small language model is fine-tuned to absorb new facts, each shown
five times, does *spreading* the five exposures apart in training (other data in
between) protect the fact against later forgetting, compared with showing them in
five consecutive steps — everything else equal?

This borrows the **spacing effect** from human memory research, one of its most
replicated findings: the same number of study repetitions gives better long-term
retention when they are spread out than when they are massed.

**Answer (GPT-2 124M, synthetic facts, one protocol):** __RESULT_ONE_LINE__

The design, prediction, decision rule and named traps were committed before any
number existed ([PREREGISTRATION.md](PREREGISTRATION.md)); the four amendments made
during calibration are recorded there with the pilot numbers that forced them.

## Setup in one paragraph

GPT-2 (124M), full fine-tuning on Apple-Silicon MPS, AdamW lr 1e-4, dropout off.
200 synthetic paired-associate facts per seed ("The capital of Sheipiakvuk is
Prothkunshend.") with invented names, so the pretrained model scores exactly 0 on
them. Each fact is shown 5 times inside a 700-step "injection window" on top of a
fixed WikiText-103 filler stream (15 chunks of 64 tokens per step). The only thing
that differs between conditions is the *gap* between a fact's five exposures:
1 step (massed), 4, 16, or 64 steps (spaced). Each fact's **last** exposure step is
drawn once per seed and shared by all conditions, so time-since-last-exposure is
identical across conditions. After the window come 1500 steps of interference:
filler plus 50 *new* facts of the same kind (the classic learn-A-then-B paradigm).
Retention is measured as exact-match accuracy (and answer NLL) at 7 checkpoints.
Five seeds for massed vs spaced, three for the intermediate gaps, one replicate run
for the noise band. 17 runs, ~9 minutes each.

__RESULTS__

## How to reproduce

```bash
uv sync
uv run pytest
scripts/main_runs.sh            # 17 runs, ~2.7 h on an M-series laptop
uv run python -m spacinglab.analyze   # pre-registered analysis
uv run python -m spacinglab.explore   # exploratory analyses
uv run python -m spacinglab.plot      # results/retention.png
```

Pilot logs: `results/pilot*.log`. Main-run logs (per-fact evaluations, generated
answers, guards): `results/runs/*/log.json`.
