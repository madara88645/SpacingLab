# Study 13: deterioration-prioritized replay with equal distinct-fact coverage

10 September 2026. Completed finite, preregistered three-pair screen; no additional
training authorized or launched. All spreads below are sample standard deviations
across three seeds, not uncertainty intervals. Differences are priority minus uniform.

## Finding

With both policies replaying exactly 80 distinct previously learned facts once each,
deterioration-prioritized selection improved delayed all-fact exact-answer accuracy
by **4.50 percentage points, SD 2.21**, across three paired seeds. Individual effects
were **+6.60, +2.20, +4.70 points**. The prediction passes the preregistered positive
directional screen. This is limited evidence for this complete constrained policy,
not statistical significance, a universal improvement, or a biological mechanism.

## What was compared

GPT-2 124M was fully fine-tuned locally on synthetic facts mixed with a frozen
WikiText filler stream. Each seed learned 200 old facts with five exposures each,
at fixed 64-update gaps, in a common 800-update prefix. That gap was a reference,
not a claimed universal optimum. Both continuations restored the SAME model and
Adam optimizer moments, then received identical filler and 50 new facts over
1500 updates. No larger model, personal corpus, or PEFT was tested.

Only old facts answered correctly at the fork were eligible for replay. The pools
contained 145, 142, and 130 items, all above the precommitted minimum of 80.
Common accuracy was .69500 +/- .03969; common answer NLL .42359 +/- .06118.
NLL is the average negative log probability of the correct answer tokens; lower
means the model assigned the correct tokens greater probability.

Uniform drew 80 eligible facts without replacement before either continuation.
Four ordered blocks of 20 specified replay times AND full-input-length slots.
Priority filled those same slots with not-yet-replayed facts whose answer NLL
had deteriorated most since the fixed common reference. This measures accumulated
deterioration, not an instantaneous forgetting rate or just current difficulty.
Both arms had identical evaluation probes and exactly 80 distinct one-time replays,
at updates 101–120, 301–320, 601–620, and 901–920.

The primary is the equal-weight mean accuracy on ALL 200 old facts at updates
200, 400, 800, 1200, and 1500. It is not restricted to replayed or eligible items.
The final checkpoint is 580 training updates after the last old-fact replay.

## Primary result and decision

| Seed | Uniform accuracy (%) | Priority accuracy (%) | Difference (points) |
|---|---:|---:|---:|
| 12 | 43.70 | 50.30 | +6.60 |
| 13 | 43.80 | 46.00 | +2.20 |
| 14 | 36.40 | 41.10 | +4.70 |
| Mean +/- sample SD | 41.30 +/- 4.24 | 45.80 +/- 4.60 | +4.50 +/- 2.21 |

Paired range: +2.20 to +6.60 points. All effects are positive and the mean exceeds
the sample SD, satisfying the fixed screen. There is no p-value, confidence
interval, equivalence test, or claim of adequate power for small effects.
The independent experimental unit is a seed pair, not each question or checkpoint.

## Negatives and secondary checks

- Terminal accuracy alone was NOT consistently improved: differences +8.50,
  -0.50, +3.00 points; mean +3.67 +/- 4.54. Therefore “better in every test” would
  be wrong. The favorable primary is an average across five delayed checkpoints.
- Mean true-answer NLL improved by -.08687 +/- .03497, with all three negative
  differences. But incorrect same-template foil NLL also decreased by -.07128
  +/- .08567. Correct-versus-foil separation changed by +.01558 +/- .06966,
  with mixed signs. This does not establish content-specific representation
  preservation, and NLL alone cannot prove a memory was erased or retained.
- Initially incorrect-at-fork items had a descriptive accuracy difference of
  +.00537 +/- 1.60778 points: mixed, not evidence of a benefit. “Initially
  incorrect” does not mean “never learned.” Eligible-item accuracy improved
  by +6.47715 +/- 2.43060 points; it remains secondary, not the primary endpoint.
- Terminal new-fact accuracy differences were +2.00, -2.00, 0.00 points; mean
  0.00 +/- 2.00. Uniform was 97.33% +/- 3.06 points; priority 97.33% +/- 2.31.
  Near-ceiling learning and three seeds cannot establish absence of harm.
  New-fact NLL difference was -.00821 +/- .00630. Filler-loss difference was
  +.00034 +/- .00073, mixed. All outcomes, including these negatives, are retained.

## Guards and audit

Independent post-run reconstruction passed, without training or fresh model logits.
All 80 software tests passed again. The verification-before-completion skill guided
fresh checks of completion, raw aggregates and provenance before reporting success.

- Git records registration fbda2c9, tested implementation 80f6c88, frozen manifest
  a80bfda, then launch receipt b508f69. Frozen source, dependencies, model/tokenizer
  files and filler bytes match. Execution session 38078 exited 0 with STUDY13_DONE;
  three pair-completion markers and six child completion markers were verified.
- All three retained model/optimizer forks match branch-start fingerprints.
  There were zero pre-replay correctness disagreements at steps 50 and 100.
  Tiny MPS numerical drift existed: maximum item-NLL difference .0000176430.
  Shared initialization does not mean bit-identical subsequent arithmetic.
- All 11,400 logged update rows and 24 selection rounds were rebuilt. Each arm
  used 1500 continuation updates, 80 old replays, 200 new-fact exposures and
  1,440,000 filler input tokens. Per-update lengths, filler bytes and new items
  match. Distinct coverage was exactly 20,40,60,80; each old item was replayed
  zero or one time. Old replay token totals per pair were 1241,1247,1222.
- No zero-score fallback was used in any round. Bucket capacity was sufficient
  everywhere, but restricted choice: seed 13 had a sole candidate for the length-19
  first-round slot and length-11 second-round slot. Exact capacity tables are in
  audit.json. Length distributions match; template distributions and identities do
  not, intentionally. This tests the whole allocation policy, not an isolated score.
- Every replay update was gradient-clipped. The average clipping multiplier was
  .50400 +/- .00488 uniform versus .49443 +/- .00560 priority; difference
  -.00957 +/- .00108. Equal examples/steps do not imply equal gradients or equal
  effective optimization. Full gradient and coefficient guards are in AUDIT.md.
- No primary checkpoint hit the registered floor or ceiling. Runtime was about
  74.3 minutes summed over logged stages, excluding orchestration and audit.
  Continuation duration was 582.36 +/- 23.16 seconds uniform and 583.44 +/- 25.39
  seconds priority. Both arms paid the same probing cost; this does NOT measure
  production efficiency against a random-replay system that omits probes.

Old AND new exact-answer accuracy was reconstructed from saved generated strings;
NLL/foil aggregates from per-item arrays. This does not recompute logits. Filler
loss and parameter displacement remain logged measurements; final branch weights
were not retained. The common forks are retained locally, excluded from Git.

## What this changes, and the next question

The current advantage cannot be attributed to a larger COUNT of distinct replayed
facts: that count is exactly equal here. Study 12 suggested this possible explanation;
Study 13 finds a positive policy effect even under equal coverage. However BOTH
policies were changed to forbid revisits and seeds changed, so this does not
quantify what caused Study 12's effect. Do not pool these screens or compare their
means as if they were one controlled experiment. This is one small synthetic-fact
protocol, with no no-replay arm, original-revisit arm, unseen phrasing, personalization,
broader continual-learning benchmark, or biological mechanism test.

Further work seems worth discussing, not automatically executing. One focused
candidate is deterioration-priority versus CURRENT-difficulty priority, retaining
the same no-revisit/token budget. For example, distinguish “became harder since
learning” from “is hard right now.” This could test whether tracking change adds
value beyond a simpler hard-item rule. It requires a new explained design,
explicit user approval and prospective registration. No new experiment is started.

Evidence: [registration](../../docs/STUDY13_PREREGISTRATION.md), [all primary and
secondary metrics](REPORT.md), [audit and guard tables](AUDIT.md), [machine-readable
audit](audit.json), and seed_12/seed_13/seed_14 raw records. Earlier studies remain
separate. Local reporting only; no push, new agents or new image.
