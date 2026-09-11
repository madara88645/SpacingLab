# Study 9 — variable gaps with identical first and last exposures

Registered before Study 9 model evaluation/training/outcomes. Studies 7 and 8 are
known. Study 8's primary paired difference was +0.01595 (sample SD 0.04427; range
-0.03214 to +0.05500), mixed/inconclusive. User now approved this particular control.
No personal messages, personal corpus, adapters or new model size are in scope.

## One question and prediction

At the same five exposures, mean gap, first exposure and final exposure, does a
random permutation of short/long intervals outperform uniform 64-step intervals?

Prediction: small/mixed effects, not a consistent positive directional signal under
the rule below. A consistent positive signal would contradict that prediction.
This tests a variable-gap **policy**, not randomness alone: gap magnitudes and ordering
both differ. It does not isolate acquisition-independent forgetting, a biological
mechanism, personalization, PEFT or a general optimal scheduling rule.

## Exactly six fresh runs and two policies

Seeds 0,1,2. Order: spaced0, variable_gaps0, variable_gaps1, spaced1, spaced2,
variable_gaps2. Fresh initialization in both arms; no historical comparator reuse.

Use GPT-2 full fine-tuning on MPS, offline cached revision
`607a30d783dfa663caf39e06633721c8d4cfcd7e`. Filler is the complete existing snapshot:
`data/wikitext103_tokens.npy`, SHA-256
`868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304`.
Same source/package/model/tokenizer/data manifest procedure as Study 8, frozen before
any evaluation and checked on each launch. New outputs only under `results/study9`.

200 synthetic facts, five identical exposures each. 100 pre-injection, 700 injection,
1500 interference steps. 15 filler chunks per step, length 64. Interference: 50 distinct
facts, four exposures each. AdamW lr 1e-4, betas (.9,.999), zero weight decay and
dropout, warmup 50, clip norm 1, existing per-sequence-mean loss. No tuning or pilots.

Draw p_i with existing `draw_last_exposures(200,5,64,700,seed)`.
- Spaced: gaps [64,64,64,64], first exposure p_i-256, last p_i.
- Variable gaps: for each fact, independently permute [32,32,64,128] with a NumPy
  generator seeded seed+40000. Start at p_i-256, then cumulatively add the four gaps.
  Each permutation has total span 256 and mean gap 64. Duplicate 32s mean there are
  twelve distinct orders; no outcome-based choice of order. Do not change these gaps.

Save actual target schedules. Validate exact per-fact first and last times across
arms, five distinct in-window exposures, and the exact registered gap multiset per
arm. Data/facts/interference/model/software/step/token budgets must match.

## Primary/secondary measures and decision

Primary: mean exact-match accuracy across interference checkpoints
50,100,200,400,800,1200,1500 (not time-integral AUC). Delta = variable_gaps minus spaced.
Report all three values, mean, sample SD (ddof=1), and min/max for each arm and delta.

Consistent positive direction: all three deltas >0 and mean > sample SD. Negative:
all three <0 and absolute mean > sample SD. Otherwise mixed/inconclusive. This is an
exploratory screening heuristic, not a significance or equivalence test. Three seeds
will not reliably resolve small differences. No post-hoc extra runs until p<.05.

Secondary: answer NLL averaged over those checkpoints, terminal accuracy/NLL and
foil discrimination. If mean NLL contradicts accuracy direction, label discordant
metrics and avoid calling it an unqualified improvement. Retain failed predictions.

## Traps and guard quantities

1. First/last timing and mean/span now match, but middle-time positions, variability
   and batch composition change. Do not infer a mechanism from a policy effect.
2. Accuracy/NLL at each fact's last exposure and window end measure acquisition.
   Unequal acquisition prevents a pure forgetting-rate claim; no correct-only filtering
   or normalization for the primary score.
3. Log full schedules, fact counts per step, preclip norm, actual clipping scale,
   nominal and clipped loss coefficients, model displacement and actual budgets.
   Coefficients do not measure per-fact Adam updates. Small differences are not proof
   of equal effective learning pressure.
4. Flag accuracy <=.02 and >=.98 at interference checkpoints, report NLL too.
   Neither zero accuracy nor NLL alone establishes erasure of a representation.
5. Report new-fact accuracy/NLL and held-out filler loss to expose tradeoffs.
6. Assert exact CPU input and timing hashes/arrays; report pre-injection numerical
   differences due to possible MPS nondeterminism. Do not pool older studies or treat
   seven checkpoints or 200 facts as independent model runs.

## Execution policy

Serial finite chain, six runs then automatic complete-case validation and analysis.
No new studies, personal-data collection, publication, remote or push. Unit tests
on artificial arrays are software tests, not experimental pilots. Preserve partial
attempts; no overwrite. Stop on user request, nonfinite values, provenance mismatch
or any timing/budget validation failure. Register repair before restarting affected
runs. After completion give a short English write-up and plain Turkish summary,
including negative outcomes and limitations, and commit locally.
