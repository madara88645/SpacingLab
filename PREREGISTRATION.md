# Pre-registration: does spacing repetitions protect fine-tuned facts from later forgetting?

Written 2026-09-04, before any experiment number existed. Anything changed after the
first main run is recorded under "Amendments" with the reason and the date; the git
history is the timestamp.

## The phenomenon borrowed from human memory

The **spacing effect** (Ebbinghaus 1885; Cepeda et al. 2006 meta-analysis): the same
number of study repetitions produces better long-term retention when the repetitions
are spread out in time, with other material in between, than when they are massed
back-to-back. It is one of the most replicated findings in the learning literature.

## The one question

When a small pretrained language model is fine-tuned to absorb a set of new facts,
each shown K times, does **spreading a fact's K exposures apart** in training time
(other data in between) rather than **presenting them in consecutive steps** improve
how well the fact survives **subsequent fine-tuning on unrelated text**, when
everything else is held equal: total exposures, total gradient steps, total tokens,
the other data seen, and the time since the fact's last exposure?

## Prediction (committed now)

**H1 (spacing effect):** retention after the interference phase increases with the
spacing gap. Concretely, the retention score (defined below) at gap 64 is higher than
at gap 1, in every seed, by more than the seed-to-seed spread.

Supporting, not required: retention is monotone across gaps 1 < 4 < 16 < 64.

**Immediate learning is a guard, not a prediction.** My prior is that massed
exposures (4 consecutive Adam steps on the same sequence) memorise *at least as
strongly* immediately as spaced ones. If massed learns *less* immediately, the
retention difference is confounded by learning and the contingency below applies.

**What would kill H1:** retention(gap 64) − retention(gap 1) is inside the seed
spread or the replication-noise band, or is negative, in the primary metric.

## Design

### Model and training
- `gpt2` (124M parameters), full fine-tuning, fp32, Apple-Silicon MPS.
- Dropout set to 0 everywhere (removes a noise source and a hidden regulariser).
- AdamW, betas (0.9, 0.999), weight decay 0, gradient clipping at 1.0.
- Learning rate: linear warmup over the first 50 steps of the pre-phase, then constant
  for the rest of the run. The value is fixed by the pilot (below).
- Loss: each sequence in a batch contributes the mean cross-entropy over its label
  tokens; the batch loss is the mean over sequences ("one document, one vote"). This
  is declared because it gives a 13-token fact the same weight as a 64-token filler
  chunk; the alternative per-token weighting would make a single fact ~1% of a batch
  and would need far more exposures to learn.

### Data
- **Facts:** N = 100 synthetic paired-associate facts per seed. Each is one sentence
  from one of five templates (capital-of, born-in-town, river-flows-into-lake,
  currency-of, founder-of) with *invented* subject and answer names (random
  pronounceable syllable strings, capitalised, all unique within a seed). Invented
  names mean the pretrained model cannot know the answer: pre-injection accuracy must
  be 0 and is checked.
- **Filler / interference text:** WikiText-103 train, tokenised as one stream with
  `<|endoftext|>` between articles, cut into 64-token chunks, consumed in a fixed
  per-seed order. The injection phase and the interference phase draw from the same
  stream, so the interference text is *disjoint* from but *same-domain* as the filler.
  That is a scope limit, stated here.

### Phases of one run (all conditions identical except exposure placement)
1. **Pre-phase:** 100 steps of filler only (LR warmup happens here, so no fact is
   ever shown at a reduced learning rate).
2. **Injection window:** T_inj = 600 steps. Every step has 15 filler chunks; fact
   sequences are *added on top* of the filler at their exposure steps, so the filler
   consumed at every step is byte-identical across conditions.
3. **Interference phase:** 1500 steps of filler only.

### Conditions (the only manipulated variable)
For each fact i, a **last-exposure step** p_i is drawn uniformly from
[(K−1)·64, T_inj) once per seed and shared by all conditions. The fact's K exposure
steps are p_i − j·g for j = 0..K−1, where the gap g is the condition:

| condition | gap g (steps) | meaning |
|---|---|---|
| massed | 1 | K consecutive steps |
| gap4 | 4 | |
| gap16 | 16 | |
| spaced | 64 | span of (K−1)·64 steps |

Because p_i is shared, the time from a fact's *last* exposure to any evaluation point
is identical across conditions (this is the classic recency confound in human spacing
studies; it is removed here by construction). Total exposures (N·K), total steps,
total filler tokens and total fact tokens are equal by construction and are logged
and asserted.

### Measurement
For each fact, the prompt is the sentence with the answer removed (e.g. "The capital
of Zorbland is"), prefixed with `<|endoftext|>` as in training. Two measures:
- **exact-match accuracy**: greedy decoding of len(answer tokens) tokens equals the
  answer tokens. Averaged over the 100 facts.
- **answer NLL**: teacher-forced mean negative log-likelihood per answer token,
  averaged over facts (continuous, no ceiling).

Evaluation points: before injection (must be ≈0 accuracy), immediately after the
injection window ("immediate"), and at interference steps
{50, 100, 200, 400, 800, 1200, 1500}. Filler held-out loss (200 held-out chunks) is
measured at the same points to confirm the interference phase really trains.

- **Primary outcome:** *retention score* = mean exact-match accuracy over the seven
  interference checkpoints.
- **Secondary:** accuracy at step 1500; the NLL analogues of both; immediate accuracy.
- **Guards logged per run:** immediate accuracy and NLL; parameter displacement
  ‖θ − θ_pretrained‖ after injection and at the end; filler tokens and fact tokens
  seen; number of optimizer steps.

### Seeds and noise
- Seeds 0, 1, 2 (minimum three). A seed fixes the facts, p_i, and the filler order;
  all four conditions of a seed share them, so comparisons are paired within seed.
- One extra run: condition `spaced`, seed 0, repeated. Its difference from the
  original is the *replication-noise band* (MPS kernels are not bit-deterministic).
- Total: 4 × 3 + 1 = 13 runs.

### Decision rule (fixed now)
H1 is **supported** if all of:
1. retention(spaced) > retention(massed) in each of the 3 seeds;
2. the mean paired difference exceeds both the SD of that paired difference across
   seeds and the replication-noise band;
3. |immediate(spaced) − immediate(massed)| is smaller than the retention difference
   (otherwise "learned more" rather than "kept more" is the simpler story and the
   result is reported as confounded).

Otherwise H1 is **not supported**; the numbers are reported as they are.

### Named traps and how each is handled
| trap | handling |
|---|---|
| spaced simply *learns more* at injection time | immediate accuracy/NLL reported next to retention; rule 3; contingency below |
| more gradient steps / more tokens in one condition | equal by construction; asserted from logs |
| different filler seen | identical stream per seed; facts added on top, never displacing filler |
| recency: spaced facts were seen more recently | last-exposure step p_i shared across conditions |
| ceiling / floor | pilot targets immediate accuracy in [0.5, 0.95] and non-zero retention at 400 steps; both checked in the main runs |
| pretrained prior knows the answers | invented names; pre-injection accuracy asserted ≈ 0 |
| run-to-run nondeterminism read as an effect | replication run defines the noise band |
| the effect is about weight displacement, not spacing per se | ‖Δθ‖ logged and reported; a difference here is a mechanism note, not a rescue |
| accuracy hides graded knowledge | NLL reported alongside |

### Pilot (calibration only, before the main runs)
The pilot uses a **fifth placement, "random"** (each fact's K exposures at K
distinct uniformly random steps in the injection window), seed 100, interference
shortened to 400 steps, to choose the learning rate and K from the grid
lr ∈ {1e-4, 3e-4} × K ∈ {4, 8}. Selection criterion: smallest K such that some lr
gives immediate accuracy in [0.5, 0.95] and accuracy at interference step 400 ≥ 0.10;
ties broken toward the lower lr. The chosen values are recorded under Amendments
before the main runs start. The pilot never compares gaps, and its numbers are not
part of the result. If K = 8 is needed, the injection window becomes 800 steps so
that p_i has a range of at least 350 steps.

### Contingency (pre-declared)
If rule 3 fails because massed learns less immediately, one additional condition is
run: `massed_matched`, K increased until its immediate accuracy is within 0.05 of
`spaced` (same seeds). Its retention is compared to `spaced` under the same rules,
and reported explicitly as a post-hoc learning-matched control.

## Scope of any conclusion
One model (GPT-2 124M), one fact format (synthetic single-sentence paired associates),
one interference corpus (WikiText-103, same domain as filler), one optimiser
setting, exposures K fixed by the pilot. Nothing here speaks to larger models,
real-world facts, LoRA, or different interference domains.

## Amendments

### Amendment 1 (2026-09-04, after the pilot, before any main run): stronger interference
**What the pilot showed.** With same-domain WikiText as the only interference, almost
nothing was forgotten: at k=4/lr=1e-4 accuracy went 0.47 → 0.42 over 400 interference
steps; at k=8 it stayed at 0.97–0.99 at both learning rates. lr=3e-4 was rejected
independently: it made the held-out filler loss *worse* than lr=1e-4 (3.54 vs 3.44)
and moved the weights twice as far, i.e. it damages the model rather than tuning it.
The pilot also showed exact-match accuracy can rise briefly after the last exposure
while NLL rises monotonically; the primary metric stays accuracy as pre-registered, and
NLL is reported alongside in every table.

**Why that matters.** If the interference phase forgets nothing, the "retention score"
is just the immediate score measured seven more times, and spacing has nothing to
protect. The design would be unable to say anything about retention.

**Change.** The interference phase is now filler **plus 300 new facts** of the same
five templates with disjoint invented names ("set B"), each shown 4 times at random
steps of the interference phase. Set B and its placement are seeded and identical
across all conditions of a seed. This is the classic retroactive-interference layout
of human memory experiments (learn list A, then list B, test A). Set B accuracy is
logged at every checkpoint as a guard that the interference is really being learned.
Interference from a different text domain is left as future work.

**Second pilot.** lr fixed at 1e-4. K ∈ {4, 6} with the new interference, seed 100,
random placement, 400 interference steps. Selection: smallest K with immediate accuracy
in [0.5, 0.95] and accuracy at 400 steps ≥ 0.10 and at least 0.10 below immediate
(so that there is forgetting to protect). The chosen K is recorded in Amendment 2.
