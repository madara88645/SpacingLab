# Study 7 — fresh matched-data random versus regular placement

Registered 2026-09-08, before any Study 7 model evaluation or training. Previous
studies and the provenance audit are known; this is not a blind discovery claim.
The previous random-baseline comparison cannot isolate placement because its old
control likely used a different filler stream. No historical control will be reused.

## Question, prediction, scope

With a fixed model, fixed filler/held-out data and equal exposures/optimizer steps,
does independent uniform random placement of five fact exposures produce higher
later exact-match accuracy than a regular 64-step spacing policy?

Prediction: mean random-minus-spaced retention is nonnegative. The earlier positive
comparison motivates this prediction but does not support it causally. Negative,
mixed and inconclusive outcomes will be reported without changing this question.

The estimand is the **total placement-policy effect**: recency, varying intervals and
batch composition are included. This is not an equal-acquisition forgetting test,
not a pure spacing mechanism, not an actual epoch-wise shuffled corpus, and not a
biological consolidation claim.

## Fixed six runs

- Seeds 0, 1, 2; `spaced` and `random`, each freshly initialized. Order:
  spaced0, random0, random1, spaced1, spaced2, random2. Serial laptop MPS runs.
- GPT-2, full fine-tuning; cached revision
  `607a30d783dfa663caf39e06633721c8d4cfcd7e`, offline loading. No adapters.
- Token file `data/wikitext103_tokens.npy`, complete snapshot, SHA-256
  `868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304`.
  Same per-seed training/held-out chunk hashes must match across conditions.
- 200 synthetic facts, five identical exposures each; 100 pre-injection steps,
  700 injection steps, 1,500 interference steps. 15 filler sequences per step,
  sequence length 64. Interference adds 50 distinct facts, four exposures each.
- AdamW lr 1e-4, betas (.9,.999), weight decay zero, warmup 50, dropout zero,
  global gradient clipping at 1, and the existing per-sequence-mean loss unchanged.
- Regular placement uses the existing `draw_last_exposures` with gap_max=64 and
  k=5. Random placement uses five distinct uniform steps per fact. Actual last
  exposures will now be probed in **both** conditions. Do not match them post hoc.
- Store exact model/tokenizer file hashes, source and lockfile hashes, installed
  package versions and run configuration in a manifest before the first evaluation.
  Reject drift when resuming. Do not upgrade dependencies during the study.

## Measures and decision rule

Primary: each run's arithmetic mean exact-match accuracy at interference steps
50,100,200,400,800,1200,1500. This is a seven-checkpoint score, not a time-integral AUC.
For each seed report paired delta random minus spaced. Always print all seed values,
mean, sample SD (ddof=1) and min/max together for scores and deltas.

Secondary: arithmetic mean answer NLL at the same checkpoints (lower is better),
terminal accuracy/NLL, and true-versus-foil discrimination. NLL is teacher-forced
mean answer-token negative log likelihood, not a direct representation measurement.

A consistent positive directional signal requires all three accuracy deltas >0 and
their mean greater than their sample SD; a negative signal uses all deltas <0 with
absolute mean greater than sample SD. Otherwise label the accuracy evidence mixed/
inconclusive. Even a directional signal is not a significance or equivalence claim.
If mean NLL moves against the accuracy direction, label the metrics discordant and
do not call the result an unqualified improvement. A zero/small difference does not
prove that shuffling suffices. No reuse of the old 0.041/0.014 thresholds.

## Named traps and guards

1. **Different data or starting state:** compare full train/held-out/model/tokenizer/
   source/package fingerprints, facts, interference schedules, counts and pre-injection
   logs within each seed. Hash/config mismatch invalidates a pair and stops the chain.
   Floating-point logs may differ on MPS despite identical integer data; report maximum
   pre-injection loss differences rather than equating any rounding noise to data drift.
2. **Different acquisition:** record accuracy and NLL right after each fact's final
   exposure and at window end. Do not normalize outcome by acquisition or select only
   correctly encoded items for the primary analysis. Acquisition differences limit any
   forgetting-rate interpretation, even if outcome improves.
3. **Recency/batch composition:** record every last-exposure step, per-step fact counts
   and the nominal per-fact sequence-loss coefficient 1/(15+n). These are mediators
   of the policy, not eliminated confounds. No claim that a small coefficient difference
   proves equal learning pressure.
4. **Clipping:** log pre-clipping total gradient norm and applied scale each step,
   finite-value checks, and coefficient times clipping scale for target exposures.
   These are diagnostics, not per-fact gradient attribution or Adam update magnitude.
5. **Floor/ceiling:** flag checkpoint accuracy <=.02 or >=.98 in either condition;
   these operational flags are not chance levels. Inspect NLL alongside them. No erasure
   claim from zero exact match; no similarity claim from a saturated probe.
6. **New-learning tradeoff:** report interference-fact accuracy/NLL, held-out filler loss,
   parameter displacement and actual steps/tokens. Higher old-fact scores purchased by
   lower new-fact scores are a tradeoff, not a free improvement.
7. **Small n and nondeterminism:** three seeds only, paired seed spread, no p-value or
   equivalence test, no extra seeds selected after seeing a favorable partial result.

## Execution and stopping

Run only these six configurations. Save each completed log separately; never overwrite
old results. Save diagnostic progress at evaluation checkpoints; an interrupted run
without a final log is not a complete result and must be retained as an abandoned
attempt before a fresh restart. No hyperparameter pilots or tuning on Study 7 outcomes.
Unit tests with synthetic arrays/gradients are software tests, not experimental pilots.

Stop on user request, nonfinite loss/gradients, missing pinned inputs, source drift,
or a provenance mismatch. Preserve failure evidence; repair with a dated amendment
before restarting affected runs. Inspect and report partial results only as partial.
After six runs, analyze all six, update English/Turkish reports, and commit locally.
No new studies, remote creation, publishing, or pushing as part of this study.

## Amendment 7.1 — preflight serialization repair, 2026-09-08

The first chain launch stopped in manifest validation **before loading/evaluating any
model or starting a training run**. The in-memory checkpoint tuple was compared to
its JSON list representation, falsely reporting drift. A regression test reproduced
this; canonical JSON normalization repairs the comparison while still rejecting
changed model bytes. Preserve the initial manifest as `manifest.preflight-rejected.json`,
then freeze a corrected manifest including this code/registration update before any
evaluation. No data/model settings, prediction, metrics, order or decision rule change.
