# Study 11 — finite three-pair continuation screen

Registered 10 September 2026 before any Study 11 model evaluation or training.
The user explicitly authorized starting this smaller experiment after rejecting
the proposed 12-pair plan. Authorization is exactly three new comparisons, six
training runs; it is not permission to continue automatically or launch adaptive
replay. The user requires a short, understandable explanation and explicit consent
before any subsequent experiment.

## Question, history and prediction

Does the variable-gap policy show a consistent positive retention direction on
three additional seed settings relative to constant gaps with matched endpoints?
This is a resource-limited research-direction screen, NOT a definitive superiority
test. Study 9 and Study 10 are already known, both mixed/inconclusive. Their paired
primary means and sample SDs were +0.04238 +/- 0.05866 and +0.01143 +/- 0.02767.
This follow-up was selected after those outcomes. All earlier outcomes remain in
the record; a positive third screen cannot retroactively make them positive.

Prediction: mixed/inconclusive rather than a positive directional signal. A
positive signal contradicts that prediction and must be reported as such.

## Exactly six runs, unchanged experiment

Use fresh seeds 6, 7, 8. Fixed order: spaced6, variable_gaps6, variable_gaps7,
spaced7, spaced8, variable_gaps8. Each starts from the same pretrained checkpoint;
no trained checkpoint or historical comparator is reused.

The complete training, scheduling, evaluation and guard protocol in
docs/STUDY9_PREREGISTRATION.md is incorporated unchanged. Read it before execution.
GPT-2 124M full fine-tuning, offline model revision
607a30d783dfa663caf39e06633721c8d4cfcd7e, Apple Silicon MPS. Frozen filler file
data/wikitext103_tokens.npy, SHA-256
868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304.
200 synthetic old facts, five exposures each; 100 pre-injection, 700 injection and
1500 interference steps. 50 interference facts, four exposures each. Fifteen
64-token filler chunks per step. AdamW lr 1e-4, betas (.9,.999), warmup 50,
clipping 1, zero dropout/weight decay, existing per-sequence-mean training loss.

For each seed, draw last exposures with draw_last_exposures(200,5,64,700,seed).
Fixed gaps are [64,64,64,64]. Variable gaps independently permute [32,32,64,128]
per fact using seed+40000. Both start at last-256, finish at last, have five
exposures, span 256 and mean interval 64. Middle positions and batch composition
are intentionally different. This does not isolate randomness from gap magnitudes.

## Locked metrics and decision rule

Primary is the unweighted mean exact-match accuracy across interference checkpoints
50,100,200,400,800,1200,1500, not terminal accuracy or a time-integrated curve.
Within each seed compute variable minus fixed. Report all three seed values,
mean, sample SD (ddof=1), min and max for each arm and paired difference.

- All three differences strictly positive AND their mean exceeds sample SD:
  positive_directional_signal; discuss whether a larger validation is worthwhile.
- All three strictly negative AND absolute mean exceeds sample SD:
  negative_directional_signal; no support for continuing this superiority claim.
- Otherwise: mixed_or_inconclusive; recommend parking the gap question and
  explaining an alternative selective-replay plan to the user.

All six runs finish before the decision. Never extend this block based on results,
stop early on a favorable result, or suppress an unfavorable seed. The above rule
is a screening heuristic, not a p-value, significance, equivalence or power claim.
No pooling with Studies 9/10 for a decision or combined significance test. Repeated
post-result screens can select chance positives; any favorable outcome remains a
new direction signal in the context of the two mixed earlier blocks, not proof.
Any future study requires a separate explanation, user approval and preregistration.

Secondary: checkpoint-mean answer NLL, foil discrimination, terminal accuracy/NLL.
Report opposing mean accuracy/NLL directions as discordance, never replace the
primary with a better secondary outcome. Lower true NLL alone is not stronger
fact-specific memory: Study 10's foil check is known. Keep the existing foil guard;
do not add new probes or claim to resolve its single-foil limitation here.

## Traps and guards

- Acquisition may differ. Report last-exposure and window-end accuracy/NLL; no
  equal-learning forgetting claim, correct-only primary or after-the-fact matching.
- Verify paired steps, true token budgets, exposure counts, content, first/last
  timing and complete per-fact gap multisets; log actual schedules and step guards.
- Flag checkpoint accuracy <=.02 or >=.98. Report new-fact performance, held-out
  filler loss, weight displacement, clipping and nominal/clipped loss coefficients.
  These coefficients are not per-fact Adam update attribution.
- Seeds change fact draws, filler order and schedules together. Three seeds do not
  separate these influences. MPS is potentially numerically nondeterministic; report
  pre-injection differences. Do not treat 200 facts or seven checkpoints as 1400
  independent model runs. No biological mechanism or representation-erasure claim.
- Same small model, synthetic fact generator and protocol only. No general best gap,
  personalization, PEFT, real-world conversational alignment or no-cost claim.

## Execution, provenance and stopping

New files only in results/study11 plus its runner, tests and documentation. Preserve
all historical results/manifests and training/scheduling/evaluation implementation.
Commit this registration first; then runner/tests; then an immutable manifest before
any model evaluation. Freeze data, model/tokenizer, source and software versions;
verify each launch. Synthetic unit tests and file hashing are not experimental pilots.

Run serially in the existing local SpacingLab repository; no subagents, remote compute,
personal data, publication or push. Stop on user request, nonfinite output, provenance
drift or validation failure. Preserve partial attempts without overwrite; document
repair before a restart. Existing whole-run files permit skipping validated completed
runs, not checkpoint-resuming an interrupted training run.

The finite chain runs analysis after all six runs and exits. Audit outputs, report
English evidence and a brief Turkish finding with uncertainty, commit locally, and
stop for the user's decision. Do not start Luna's proposal automatically.
