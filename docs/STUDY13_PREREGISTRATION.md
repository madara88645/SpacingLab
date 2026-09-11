# Study 13 — deterioration versus random replay with equal distinct-fact coverage

Registered 10 September 2026 BEFORE Study 13 model inference, calibration or training.
Mehmet approved the proposed coverage-matched A/B comparison with "evet" after
the plain-language explanation. Exactly three pairs are authorized; no extra
seeds, tuning, pilots, agents, remote compute, images or private data.

## Question and prediction

When BOTH policies replay exactly 80 distinct previously learned facts once each,
does accumulated-deterioration priority outperform uniform selection?
Directional prediction: positive primary screen for priority. Mixed or negative
outcomes fail this prediction and will be reported in full.

Study 12 is known and informed this question: wider coverage could explain its
positive policy effect. This is a prospective, coverage-constrained comparison,
NOT an unchanged replication of Study 12 and NOT causal mediation of that effect.
Both arms now prohibit repeat visits during the interference stage. A null result
does not prove that coverage caused Study 12's result. Do not pool the studies.

## Common protocol and fresh paired seeds

Use precisely seeds 12,13,14. Arm order: uniform then prioritized for 12;
prioritized then uniform for 13; uniform then prioritized for 14. Three common
acquisition prefixes, six continuations; serial local Apple Silicon/MPS.
Stop after those pairs and analysis regardless of direction.

GPT-2 124M full fine-tuning; local model/tokenizer revision
607a30d783dfa663caf39e06633721c8d4cfcd7e. Frozen filler snapshot
data/wikitext103_tokens.npy, SHA-256
868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304.
Existing make_facts(250,seed): first 200 old facts, last 50 new. One common prefix
per seed: 100 filler updates, then 700 old-acquisition updates. Each old fact has
five identical exposures spaced by 64, with last exposure drawn by the unchanged
draw_last_exposures(200,5,64,700,seed). This is a fixed reference, not an optimum claim.

Fork the common model AND optimizer states at update 800; verify fingerprints
and retain the checkpoint. Reset Torch RNG to seed+50000 before each arm.
Restore the same filler position (12000 chunks). Each arm then receives 1500
interference updates, 15 filler chunks of 64 tokens each, and four exposures per
new fact from random_schedule(50,4,1500,seed+10000). Same immutable base stream.
AdamW lr 1e-4, betas (.9,.999), zero weight decay/dropout, first-50-global-update
warmup, clipping norm 1, existing per-sequence mean loss. No optimizer reset.

## Equal coverage and matched input tokens

At the common fork, exact-answer-correct old facts are the fixed eligible pool
for BOTH arms. Store their common per-answer-token NLL as a fixed reference.
If fewer than 80 facts qualify, preserve calibration failure and stop the chain.
No quota relaxation, seed replacement or post-result tuning.

Draw an ordered sample of 80 eligible indices without replacement using
np.random.default_rng(seed+60000).choice(eligible,80,replace=False). Partition into
four consecutive blocks of 20, at probes 100,300,600,900. These are the uniform
arm's selections, fixed BEFORE either continuation. Their ordered full-input
lengths (EOS plus complete fact sentence) define paired length slots per round.

At each probe, evaluate all old facts identically in both arms without gradients.
Priority score_i = max(0,current_answer_NLL_i-common_reference_NLL_i). The common
reference never changes. Among eligible facts NOT replayed in any earlier round
of THIS arm, rank by decreasing score within each full-input-length bucket. Ties
use one length-200 random vector from np.random.default_rng(seed+80000+round_index),
then fact index. Fill the uniform plan's length slots in their recorded order.
Zero scores fill remaining slots if necessary; record every fallback.

Each prior round removes exactly the same count per length bucket in both arms.
Therefore sufficient candidates remain for the next predetermined bucket quota;
if an implementation finds otherwise, it must halt, not repeat an item or change
length slots. Total selected identities differ by design; coverage COUNT matches.

Replay one selected fact per update at 101–120,301–320,601–620,901–920, appended
to the same filler/new-fact batch. Do not displace other examples or add updates.
Each arm covers 20,40,60,80 distinct facts after the four rounds, exactly 80
additional exposures, and per-fact replay count 0 or 1. This no-revisit rule only
applies to interference replay, NOT the five common acquisition exposures.
Actual per-update input lengths, row counts, replay timings and probes must match.

## Fixed outcomes and decision

Primary: equal-weight mean exact-answer accuracy over ALL 200 old facts at
interference updates 200,400,800,1200,1500. All are delayed after first replay;
the terminal test is 580 updates after last replay. Never replace all-fact primary
with selected/eligible subset scores, NLL, or immediate-post-replay improvement.

For each arm and paired priority-minus-uniform difference, report three values,
mean, sample SD (ddof=1) and min/max. Positive directional screen requires all
three differences >0 AND mean > sample SD. Negative screen requires all <0 AND
absolute mean > SD. Otherwise mixed/inconclusive. This is not statistical
significance, a confidence interval, equivalence, or adequate power for small effects.

Secondary: primary-checkpoint mean true NLL and foil discrimination; terminal
old accuracy/NLL; descriptive eligible and initially-incorrect subgroup accuracy.
Evaluation union: 50,100,200,300,400,600,800,900,1200,1500. Both arms get every
probe, including selection probes. Log new-fact accuracy/NLL, held-out filler loss
and parameter displacement at each probe. Retain the already-computed full
new-fact evaluation dictionaries to enable aggregate checks without extra inference.

## Traps and required guards

- Initial learning: shared learned model AND optimizer hashes, common correctness
  and NLL; pre-first-replay drift at 50/100. Tiny MPS arithmetic differences may
  occur and must be reported, not described as bit-identical trajectories.
- Extra training/coverage/recency: actual step-level token and identity logs;
  cumulative distinct counts, exact no-revisit invariants, exposure counts, full
  schedules and paired tokens. Log scores, selected IDs, previous used IDs, fallback,
  uniform overlap, length/template distributions, gradient/clipping coefficients,
  wall time and displacement. Equal budgets do not imply identical gradients.
- Difficulty/format: use deterioration from fixed reference, not current NLL alone.
  Single-foil discrimination is limited. NLL cannot establish representation loss
  or prove content-specific memory by itself.
- Regression to the mean: judge all facts at delayed tests, not only chosen items.
- New-learning tradeoffs: retain new-fact and filler metrics even if unfavorable;
  report saturation, primary old-accuracy floor <=.02 or ceiling >=.98. Ceiling
  on new learning cannot prove no harm. Initially incorrect is not never learned.
- Length buckets can restrict candidate choice, especially late in the stream;
  score exhaustion/forced zero scores must be visible. Template distribution and
  WHICH facts receive replay remain unconstrained parts of the policy.
- A winner supports this complete budget/coverage-constrained policy only. A null
  or negative does not retrospectively identify the cause of Study 12's benefit.
  No no-replay arm, original-revisit-policy arm, unseen-fact/phrasing evaluation,
  PEFT, personalization, biological mechanism or broader model claim.

## Execution and stop boundary

Commit this registration, then tested isolated implementation, then immutable
manifest BEFORE any Study 13 model evaluation. Use uv without dependency updates.
New modules spacinglab/study13*.py and tests/test_study13*.py; results/study13.
Leave all historical training, tests, manifests and results unchanged.
Halt on nonfinite results, calibration failure, fork/budget/coverage/provenance
mismatch, incomplete attempt or user stop. Preserve all files; no automatic
restart or overwrite. At completion independently audit all pairs, deliver an
English write-up and short Turkish explanation, pause monitoring and wait for
understanding and explicit permission before proposing execution of any new study.
