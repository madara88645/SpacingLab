# Study 10 — fixed-size replication of the variable-gap comparison

Registered 9 September 2026 before any Study 10 model evaluation or training.
This is a follow-up chosen after seeing Study 9, not a retroactive extension of
its preregistration. Study 9 remains mixed/inconclusive: paired primary mean
+0.04238, sample SD 0.05866, range -0.02000 to +0.09643. All six original runs are
preserved in commit add1634. The user authorized three new matched pairs today.

## Question and prediction

Does the variable-gap policy show a consistent positive retention advantage on
three additional seed settings when first/last exposures and mean gap match?
Prediction remains cautious: no consistent positive signal under the screening
rule below. A consistent positive result will be reported as contradicting that
prediction. We will not relabel Study 9 as positive whatever happens here.

## Fixed sample, protocol and order

Exactly six fresh runs, seeds 3, 4, 5. Order: variable_gaps3, spaced3, spaced4,
variable_gaps4, variable_gaps5, spaced5. Reverse the alternating starting-arm
pattern of Study 9. No pilot, learning-rate tuning, optional stopping or extra
seeds based on intermediate outcomes. All runs start from the same pretrained
checkpoint, not from Study 9 checkpoints. Neither arm reuses a historical control.

The model, data, objective, optimizer, schedules, checkpoints and guards are
unchanged from docs/STUDY9_PREREGISTRATION.md, which is incorporated here in full.
GPT-2 124M full fine-tuning on local MPS; offline revision
607a30d783dfa663caf39e06633721c8d4cfcd7e. Filler snapshot SHA-256:
868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304.
200 synthetic facts, five exposures; 100 pre-injection, 700 injection and 1500
interference steps. 15 filler chunks of 64 tokens per step. 50 interference facts
with four exposures. AdamW lr 1e-4, betas (.9,.999), warmup 50, norm clipping 1,
zero dropout/weight decay, existing per-sequence-mean loss.

For each seed, draw last times with draw_last_exposures(200,5,64,700,seed).
Spaced uses [64,64,64,64]; variable_gaps independently permutes [32,32,64,128]
per fact using NumPy RNG seed+40000. Both start at last-256 and finish at last.
Each has five exposures, span 256 and average interval 64. Actual schedules must
match the construction, including the entire per-fact gap multiset and endpoints.

## Outcomes and analysis locked before running

Primary: unweighted mean exact-match accuracy at interference steps
50,100,200,400,800,1200,1500. Compute within-seed variable-minus-spaced differences.
Report every seed, mean, sample SD (ddof=1), min/max for each arm and difference.

Apply the same exploratory screening rule to NEW seeds 3-5 only:
all three differences positive and mean greater than sample SD => positive
directional signal; all negative and absolute mean greater than SD => negative
directional signal; otherwise mixed/inconclusive. Not a p-value, significance,
equivalence or power claim. Three new seeds may still leave substantial uncertainty.
Do not count facts or checkpoints as independent model runs.

Secondary: checkpoint-mean answer NLL, foil discrimination, terminal accuracy/NLL.
Flag opposing mean accuracy/NLL directions and avoid an unqualified improvement.
Report last-exposure and window-end acquisition, new-fact accuracy/NLL, filler
holdout loss, weight displacement, step/token/exposure budgets, preclip norm,
clipping fractions and nominal/clipped target coefficients. Keep floor <=.02 and
ceiling >=.98 flags. Coefficients are not per-fact Adam update attribution.

Primary conclusion uses the new three seeds alone; display Study 9 alongside it
without pooling for the decision. No combined-six significance test is planned.
Any later combined descriptive analysis must explicitly label that extension was
chosen after observing Study 9 and must not replace the separate results.

## Named traps and claims we will not make

- Unequal initial acquisition: an advantage may reflect better learning, not a
  lower forgetting rate after equal learning. Measure acquisition; do not normalize
  it away or filter the primary to facts correct initially.
- Gap magnitudes, middle positions, ordering and batch composition all change.
  Endpoints/span matching does not isolate randomness or a biological mechanism.
- New seeds also change synthetic facts, filler ordering and schedules together.
  This probes sensitivity to those choices, not a second model/dataset or factorial
  isolation of each source of variability. MPS may be numerically nondeterministic.
- Noisy observed improvement and post-result follow-up selection: retain Study 9,
  use the fixed new sample above, no result-dependent extension or hidden failures.
- Same model does not imply the same data/software: freeze model/tokenizer/data/
  source/environment hashes before evaluation and verify each launch. Log exact
  paired input streams, schedules and budgets plus pre-injection numerical drift.
- NLL and exact accuracy cannot establish whether a representation was erased.
  Neither personalization, LoRA/PEFT, general skills nor a universal best gap is tested.

## Execution and audit

New outputs only in results/study10. Freeze a new manifest including both Study 9
and Study 10 registrations; never rewrite old manifests. Preserve the training
and scheduling code. An isolated runner may reuse the tested Study 9 structure
with only seed/order/tag/output/registration changes. Test using synthetic inputs
before any model evaluation. Commit registration, code, then manifest before run.

Finite serial chain: six runs, validated analysis, then stop. Preserve partial
attempts; do not overwrite or silently discard a failure. Stop for user request,
nonfinite output, provenance drift or validation failure. Document any repair and
restart before retrying; do not change protocol mid-chain. No remote compute,
publication, pushes, personal messages or extra experiments. No subagents needed;
if later used, all must explicitly be Sonnet. Report English evidence and a short,
student-level Turkish explanation, including failed predictions and uncertainty.
