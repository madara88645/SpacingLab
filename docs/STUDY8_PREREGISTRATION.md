# Study 8 — match each fact's last exposure

Registered before any Study 8 model evaluation, training or outcome. Study 7 outcomes
are known: random-minus-spaced primary score +0.09286, sample SD 0.04586, seed range
0.06357–0.14571. This motivated the control; no blind-discovery claim.

## Question and prediction

When the last exposure of **each fact** is held identical, does random placement of
its preceding four exposures still outperform regular 64-step spacing?

Prediction: the positive advantage will attenuate, and the registered consistent-
positive directional criterion below will not be met. A persistent positive signal
would contradict that prediction and exclude a *last-exposure-recency-only*
explanation for this new comparison. A mixed/negative result would be compatible with
recency contributing to Study 7, but would **not prove recency caused all its advantage**.
Conditioning random placement also changes earlier exposure history. Do not treat
cross-study delta subtraction as a mediation estimate or proof of equivalence.

## Exactly six fresh runs

Seeds 0,1,2; conditions `spaced` and `random_matched`. Order: spaced0, random_matched0,
random_matched1, spaced1, spaced2, random_matched2. Do not reuse Study 7 controls.

All six use the same GPT-2 cached revision
`607a30d783dfa663caf39e06633721c8d4cfcd7e`, full fine-tuning on MPS, offline loading;
the same entire filler snapshot, SHA-256
`868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304`;
200 facts × 5 identical exposures; 100 pre-injection, 700 injection, 1500 interference
steps; 15 filler chunks of length 64 per step; 50 interference facts × 4 exposures;
AdamW lr 1e-4, betas (.9,.999), zero weight decay/dropout, warmup 50, global clipping
at 1, and existing per-sequence-mean loss. No learning-rate/seed/model tuning.

For each seed draw `p_i` with the existing `draw_last_exposures(200,5,64,700,seed)`.
- Spaced: `p_i-256, p_i-192, p_i-128, p_i-64, p_i`.
- Random matched: sample four distinct integers uniformly without replacement from
  `[0,p_i)`, using a separate NumPy generator seeded `seed+30000`, then add `p_i`.
  This is random placement conditional on the prescribed last exposure, not ordinary
  corpus shuffling. Do not also force the first exposure or total span to match.

Store complete target schedules, actual last-exposure vectors, first-exposure and
exposure-span diagnostics. Assert five distinct exposures per fact, exact last-time
matching, in-window times, and identical data/model/software/facts/budgets across pairs.
Freeze source/model/tokenizer/package/data fingerprints in a new manifest before the
first model evaluation. Do not change source files while the chain runs.

## Measures and decision rule

Primary: mean exact-match accuracy across interference checkpoints
50,100,200,400,800,1200,1500. Secondary: mean answer NLL on these checkpoints,
terminal accuracy/NLL, discrimination against the existing foil. Report every seed,
mean, sample SD (ddof=1) and range for both conditions and paired differences.

Delta means random_matched minus spaced. Consistent positive signal: all three
accuracy deltas >0 and mean > sample SD. Consistent negative: all three <0 and absolute
mean > sample SD. Otherwise mixed/inconclusive. This heuristic is not a significance
test or equivalence test. If mean NLL moves against accuracy, label discordant metrics
and do not call the outcome an unqualified improvement. Retain failed predictions.
Study 7 vs Study 8 effect-size comparison is descriptive only, not a second primary test.

## Guards and remaining alternative explanations

- Hashes, facts, interference schedules, budgets and exact last-exposure vectors must
  match. A mismatch stops the chain and invalidates the comparison until documented.
  Check actual saved target schedules, not just the scheduling configuration.
- Acquisition at each fact's final exposure and window end: accuracy and NLL. Unequal
  acquisition prevents equal-learning forgetting claims; no outcome normalization or
  post-hoc correct-item filtering in the primary analysis.
- First-exposure times, spans, interval variability and per-step batch composition
  differ. Their effects remain part of this policy comparison; only the last-time
  explanation is controlled. A benefit is not a biological mechanism finding.
- Log preclip norms, applied clip scale, nominal per-exposure loss coefficients and
  clipped coefficients. These are not per-fact gradient attribution/Adam update sizes.
- Flag target accuracy <=.02 or >=.98 at interference checkpoints. NLL is continuous
  but not an internal representation measurement. No erasure claim from zero accuracy.
- Report new-fact performance, held-out filler loss, displacement and actual steps/
  tokens. A new-learning cost must be disclosed, not called a free benefit.
- MPS numerical nondeterminism: report pre-injection numerical differences; CPU token
  hashes and saved schedule comparisons are exact. Three seeds give directional
  evidence, not generality. Do not reuse the old 0.041/0.014 cutoffs.

## Execution and failure policy

Serial local runs only, finite chain ending after six validated logs and automatic
analysis. Save progress and completed logs. Never overwrite earlier studies or a
completed attempt. On interruption keep partial attempts; amend before a fresh restart.
Stop on user request, nonfinite values, provenance drift or matching failures. No
pilots, extra seeds, model scaling, public upload or push in this study. Register any
necessary repair before restarting affected runs. Synthetic unit tests are software
tests, not experimental pilots. After completion report positive and negative results
in English and short, example-based Turkish, and commit locally.
