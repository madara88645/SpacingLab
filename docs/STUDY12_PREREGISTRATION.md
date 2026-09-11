# Study 12 — deterioration-prioritized versus uniform replay

Registered 10 September 2026 BEFORE any Study 12 model evaluation, pilot or training.
Mehmet explicitly authorized this A/B experiment after discussing selection of
previously learned but deteriorating facts, equal replay budgets, and evaluating
ALL old facts. This is a new intervention, not another variable-gap experiment.
No subagents, private messages, remote compute, tuning or additional study is authorized.

## Question, prediction and fixed scope

Does replay prioritized by deterioration preserve more old facts than uniform
replay, with common acquisition and matched update, token and probing budgets?
Prediction: a positive directional primary signal for prioritized replay, as defined
below. A mixed or negative result does not support the prediction; retain it fully.
Studies 9–11 are known and inconclusive for variable gaps. They are not controls
for this study, and will not be pooled with it. There is established selective-replay
prior art, e.g. Aljundi et al., MIR (NeurIPS 2019):
https://papers.nips.cc/paper/2019/hash/15825aee15eb335cc13f9b559f166ee8-Abstract.html
MIR predicts damage from a future update. Here we measure accumulated deterioration
from a stored acquisition reference; this is NOT MIR, human retrieval practice,
a new general replay algorithm, or proof of biological consolidation.

Exactly three new paired seeds: 9,10,11. For each seed train ONE common acquisition
prefix, save model and optimizer states, then fork two independent continuations.
Arm order: uniform then prioritized for seed 9; prioritized then uniform for 10;
uniform then prioritized for 11. Run serially on local MPS. Stop after all three
pairs and automatic analysis, regardless of observed direction. No early stopping
for a positive pattern, extra seeds, or switching primary to a favorable secondary.

## Common acquisition and frozen inputs

GPT-2 124M full fine-tuning, existing tokenizer/model revision
607a30d783dfa663caf39e06633721c8d4cfcd7e, existing immutable filler snapshot
data/wikitext103_tokens.npy, SHA-256
868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304.
Use the existing synthetic generator to draw 250 facts: first 200 old, last 50 new.
Five identical exposures per old fact, fixed gaps [64,64,64,64], first/last times
drawn by draw_last_exposures(200,5,64,700,seed). This schedule is a held-constant
reference, not a claim that 64 is universally optimal.

Common prefix: 100 filler-only steps then 700 acquisition steps. Each step contains
15 filler chunks of 64 tokens plus scheduled facts. Continue each arm for 1500
interference steps with the same filler stream and 50 new facts, four exposures
each, random_schedule(50,4,1500,seed+10000). Each complete arm represents 2300
optimizer steps; the shared 800-step prefix is computed once per seed for efficiency.
AdamW lr 1e-4, betas (.9,.999), zero weight decay/dropout, warmup first 50 global
steps, gradient clipping 1, existing per-sequence mean loss. No optimizer reset
at the fork: restore both parameters and moments. Reset Torch RNG to seed+50000
for each arm; persist common checkpoints locally and verify state fingerprints.
Filler position at the fork is 12000 chunks and is restored for both arms.

## Operational definition of learned and deteriorating

At the common step-800 evaluation, record correctness and per-answer-token NLL for
ALL 200 old facts. The fixed eligible pool for BOTH arms consists only of facts
answered exactly correctly here. This is a behavior-based proxy for acquisition,
not proof of a representation. If fewer than 20 are eligible, record calibration
failure, preserve the attempt and stop; do not tune, replace the seed or silently
change the quota. Never select an initially unlearned fact in either arm.

At interference steps 100,300,600,900, evaluate ALL old facts in both arms without
gradients. For eligible fact i, score_i = max(0, current_NLL_i - reference_NLL_i).
Larger positive score means the previously correct answer has become less probable.
This ranks deterioration, not simply current error or the currently hardest fact.
NLL is normalized per answer token and may reflect format rather than factual
content; retain foil discrimination and exact accuracy as separate guards.
The reference stays fixed at the COMMON fork, not updated after a replay.

## Replay selection with exact paired budgets

Four rounds, 20 distinct eligible facts per round: 80 additional exposures per arm.
An item may appear in multiple rounds, at most once in each (maximum four total).
For round r=0,1,2,3 draw 20 uniform eligible indices without replacement using
NumPy RNG seed+60000+r. This is the uniform arm's selection, and its ordered list
of FULL input lengths (EOS plus full fact sentence) defines paired token quotas.
These lists are fixed at the common fork, before either continuation or its probes.

For the prioritized arm, within each full-input-length bucket rank eligible facts
by decreasing score; break ties using a separate RNG seed+80000+r. Take the same
number per length bucket as the preselected uniform list, and place them into the
same ordered length slots. This matches actual replay input tokens at EACH step,
not just exposure count or padding. It is budget-constrained priority, not globally
unconstrained top-20. Zero deterioration scores are tied; if there are too few
positive-score candidates, remaining slots are randomly tie-broken zero scores.
Log this fallback count, all scores, selections, per-fact replay counts, length and
template distributions, and overlap with the uniform plan. Never adapt quotas to
outcomes or silently skip a scheduled replay.

After each probe, replay one selected old fact per step during interference
updates 101–120,301–320,601–620,901–920 (1-based completed-update convention).
Append it to the SAME filler/new-fact batch; do not displace filler or new examples.
Both arms have exactly the same row counts, real input-token lengths, base data,
optimizer steps and replay times. Per-fact repeats may differ by design; targeted
allocation is the treatment, not a claim of an acquisition-independent mechanism.

## Outcomes fixed before execution

Primary: mean exact-match accuracy over ALL 200 old facts at interference steps
200,400,800,1200,1500, equally weighted. All are after the first replay round;
this new primary is chosen before Study 12, not a reanalysis of Studies 9–11.
Report each seed, mean, sample SD (ddof=1), min/max for arms and prioritized-minus-
uniform differences. Do not filter the primary to eligible or replayed facts.

Screening rule: all three paired differences >0 AND mean > sample SD yields a
positive directional signal. All <0 AND absolute mean > SD yields a negative
directional signal. Otherwise mixed/inconclusive. This is not a p-value,
significance, equivalence or adequate-power claim. Three pairs cannot resolve
small effects reliably. A positive result supports a larger future test only.

Secondary: primary-checkpoint mean true NLL and foil discrimination, terminal
accuracy/NLL, eligible-pool and initially-unlearned-pool accuracies (descriptive).
Also probe at steps 50,100,300,600,900. All old-fact probes, including selection
probes, are identical in number and timing across arms. The registered evaluation
set is the union [50,100,200,300,400,600,800,900,1200,1500]. At every evaluation
also measure new-fact accuracy/NLL and held-out filler loss. No immediate-post-
replay checkpoint is a primary endpoint. Last replay ends at 920; terminal testing
at 1500 has 580 intervening updates without old replay in both arms.

## Named traps, guards and limits

- Common-prefix checkpoint and optimizer fingerprints must match before either
  branch updates. Record identical initial acquisition; no separate pretraining
  per arm that could confound initial learning. Track MPS pre-first-replay drift.
- Equal update/token/probe budgets must be verified from actual step-level logs,
  not inferred from configuration. Log gradients, clipping, replay coefficients,
  time and displacement. Equal counts do not imply identical gradients or moments.
- Feedback uses canonical labels and the same old facts as the canonical test.
  This is maintenance of known training facts, not unseen-fact generalization.
  The policy is allowed to use labels; neither arm sees future probes or new labels.
- Regression to the mean can make selected noisy probes rebound; judge ALL facts
  at delayed checkpoints, not improvement on the selected subset immediately after
  replay. Secondary NLL alone must not replace exact-match primary.
- Report single-foil limitations, new-learning tradeoffs, and primary floor <=.02
  or ceiling >=.98. Never infer erasure or a brain mechanism from accuracy/NLL.
- Repeated hard-example rehearsal, length-bucket constraints, overconfidence in
  prior answers and sequence-format learning remain alternative interpretations.
  A win establishes only this complete selection policy under this budget.
- No no-replay arm: the test estimates selection benefit GIVEN replay, not whether
  replay itself beats no replay. No PEFT, personalization or broader skills claim.

## Execution record

Commit registration, then tested implementation, then immutable manifest before
model evaluation. New modules and outputs only under spacinglab/study12*.py,
tests/test_study12*.py and results/study12; leave historical training and manifests
unchanged. Freeze source/model/tokenizer/data/software and schedules/input digests.
Unit tests with synthetic arrays/toy tensors are not model pilots. Preserve all
attempts/checkpoints; no overwrite. Halt on nonfinite values, insufficient eligible
pool, provenance drift, mismatch or user stop. No automatic restart after failure.
After six continuations, audit all three pairs, report English evidence and a short
Turkish explanation, pause monitoring, and await explicit user approval for new work.
