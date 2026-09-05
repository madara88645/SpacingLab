# SpacingLab: does spacing repetitions protect fine-tuned facts?

**Question.** When a small language model is fine-tuned to absorb new facts, each shown
five times, does *spreading* the five exposures apart in training (other data in
between) protect the fact against later forgetting, compared with showing them in
five consecutive steps — everything else equal?

This borrows the **spacing effect** from human memory research, one of its most
replicated findings: the same number of study repetitions gives better long-term
retention when they are spread out than when they are massed.

**Answer (GPT-2 124M, synthetic facts, one protocol):** the pre-registered hypothesis was **not supported as written**, but the data show something sharper. Five consecutive exposures of a fact leave a memory that is real right after the fifth exposure (43 % exact-match) and gone within about 50 training steps; the same five exposures spread 64 steps apart are at 65 % when the injection window ends and still at 14 % after 1,500 steps of unrelated fine-tuning. The gap in between is graded (1 < 4 < 16 < 64 steps). The effect is therefore mostly about *how long the memory lasts inside the window*, not about how much is retained after equal encoding, which is what H1 assumed it could measure.

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


## Study 1: the pre-registered comparison

![retention curves](results/retention.png)

*Left: exact-match accuracy on the 200 injected facts at the end of the injection window
(step 0) and at the seven interference checkpoints. Right: answer NLL (lower = better
remembered). Thin lines are single seeds, thick lines the mean.*

### Numbers (mean over seeds, min..max in brackets)

| condition (gap) | seeds | immediate acc | retention score | acc at step 1500 | acc right after last exposure |
|---|---|---|---|---|---|
| massed (1)  | 5 | 0.03 (0.02..0.04) | 0.001 (0.000..0.001) | 0.00 | 0.43 (0.26..0.64) |
| gap 4       | 3 | 0.08 (0.06..0.09) | 0.023 (0.008..0.038) | 0.01 | 0.94 (0.92..0.95) |
| gap 16      | 3 | 0.35 (0.33..0.38) | 0.124 (0.111..0.144) | 0.05 (0.04..0.08) | 0.96 (0.94..0.99) |
| spaced (64) | 5 | 0.65 (0.62..0.68) | 0.285 (0.241..0.351) | 0.14 (0.10..0.20) | 0.81 (0.78..0.85) |

*Retention score* = mean exact-match accuracy over the seven interference checkpoints
(the pre-registered primary outcome). Paired spaced − massed retention difference:
+0.29, seed-to-seed SD 0.04, positive in every one of the five seeds (range
+0.24..+0.35). Replication-noise band (same run twice, MPS nondeterminism): __NOISE__.
Retention is monotone in the gap in every seed where all four gaps were run.

**Guards.** Within a seed, every condition took the same 2,300 optimizer steps, saw the
same 2,208,000 filler tokens and the same 18.5–18.9k fact tokens; pre-injection
accuracy was exactly 0 in all 17 runs; weight displacement after the window was
79.5–81.1 in every condition (no condition "moved more"); held-out filler loss at the
end was 3.37–3.45 everywhere, so the interference phase trained equally.

### The pre-registered decision rule, applied

| rule | result |
|---|---|
| 1. spaced > massed retention in every seed | **yes** (5/5) |
| 2. mean Δ exceeds seed SD and noise band | **yes** (0.29 vs 0.04 and __NOISE__) |
| 3. immediate difference smaller than retention difference | **no** (+0.62 vs +0.29) |

So **H1 is not supported as pre-registered.** Rule 3 was written to catch the boring
explanation "spaced simply learned more". It fired. Reporting that first is the point of
writing the rule down beforehand.

### What rule 3 actually caught (Amendment 4, measurement added before the main runs)

The pre-registered "immediate" probe sits at a fixed step, up to 444 steps after a
fact's last exposure, inside a window that is itself dense with interference (the other
199 facts). A low immediate score can therefore mean *never encoded* or *encoded and lost
inside the window*. Amendment 4 added a probe of each fact right after the optimizer step
of its own last exposure. That probe separates the two:

- massed facts **are** encoded: 43 % exact-match right after the fifth consecutive step
  (NLL 1.1), against 81 % for spaced and 94–96 % for gaps 4 and 16;
- and they **do not last**: among facts correct at that moment, 6 % are still correct at
  the end of the window for massed vs 77 % for spaced (conditional retention over the
  interference checkpoints: 0.002 vs 0.33).

Exploratory, pooled over seeds: split facts by how long they waited between their last
exposure and the end-of-window probe. Massed facts that waited under 50 steps survive at
24 %; over 50 steps, 0 %. Spaced facts survive at 100 %, 99 %, 92 %, 63 % and 20 % for
waits of 0–50, 50–100, 100–200, 200–300 and 300–450 steps. Restricting to *strongly*
encoded facts (NLL < 0.1 right after the last exposure) changes nothing for massed:
9.5 % survive to the end of the window, against 93 % for spaced.

What the massed model says instead is telling: it produces invented-looking names of the
right kind ("Zusvrox", "Prairhenv") but not the associated one. It learned the *format*
of the facts and lost the *item*.

**Honest summary of Study 1.** The pre-registered framing ("equal encoding, then who
keeps more") could not be tested, because consecutive exposures never produce a memory
that survives to the first probe. The finding that replaced it is stronger and simpler:
the *same* five gradient steps on the *same* sequence produce a durable memory when
spread out and a memory with a half-life of tens of steps when consecutive, with total
steps, tokens, filler, and time-since-last-exposure held fixed. gap 4 is almost as bad as
gap 1; gap 16 is half-way; gap 64 is the best we tested (we did not test larger gaps,
so we do not know where the benefit stops).

__STUDY2__

## What this does not show

One model (GPT-2 124M), one fact format (single-sentence synthetic paired associates),
one filler and interference corpus (WikiText-103), one learning rate, K = 5, gaps up to
64 steps of a 700-step window. Nothing here speaks to larger models, real-world facts,
or other interference domains. The mechanism story (why consecutive identical steps leave
a fragile trace) is a hypothesis; Study 2a tests one piece of it and no more.

Prior work (see [docs/literature.md](docs/literature.md)) has studied duplication vs
paraphrase and corpus-level repetition, and Chang et al. (2024) report that duplicated
injections forget faster than paraphrased ones; we found no earlier measurement that
varies only the gap between repeats of one fact with everything else matched.


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
