# Study 11: no positive variable-gap signal in the finite continuation screen

10 September 2026. All six authorized runs completed normally; no additional
training was launched. This report applies the rule registered in 1aac057, before
training, rather than changing the endpoint after viewing the outcomes.

## Finding

Variable gaps did not outperform fixed gaps on the registered primary outcome in
any of the three new paired comparisons. The mean difference was **-1.929 +/- 2.389
percentage points** (mean +/- sample SD, range -4.643 to -0.143). Because the mean
magnitude was smaller than the seed SD, even the registered negative-direction
screen did not pass. The registered result is **mixed/inconclusive**, not proof of
inferiority, equality or equivalence.

| Fresh seed | Fixed accuracy (%) | Variable accuracy (%) | Variable minus fixed (pp) |
|---|---:|---:|---:|
| 6 | 31.857 | 27.214 | -4.643 |
| 7 | 26.929 | 25.929 | -1.000 |
| 8 | 28.786 | 28.643 | -0.143 |

Fixed primary accuracy was 29.190 +/- 2.489%; variable was 27.262 +/- 1.358%
(SDs expressed in percentage points). The score averages seven registered
interference checkpoints equally. It is not terminal accuracy, an integrated
forgetting curve, or 1400 independent observations.

## What was held fixed

GPT-2 124M, frozen WikiText filler and synthetic-fact protocol, five identical
exposures per old fact, 200 old facts, 50 new interference facts, and 2300 training
steps per run. First and last exposures match exactly. Fixed gaps are
[64,64,64,64]; the alternative permutes [32,32,64,128] separately per fact.
The span and average gap match, but middle positions and batch composition differ.
Each seed has two fresh runs, not a reused historical control. Model, tokenizer,
source, software, streams and real input budgets passed the audit.

## Guards and findings that must not be hidden

All differences below are variable minus fixed, mean +/- sample SD over three
paired seeds; full arm-level numbers and ranges are in REPORT.md.

- Window-end accuracy favored variable gaps: **+4.833 +/- 3.403 pp**, range
  +1.000 to +7.500. At-last-exposure accuracy differed by +4.167 +/- 4.537 pp,
  range 0.000 to +9.000. Thus there is no demonstrated equal-acquisition starting
  point. Better early recall did not turn into a positive primary result in this
  block; this does not isolate a causal forgetting-rate mechanism.
- Checkpoint-mean answer NLL differed by **+0.00941 +/- 0.08282**, with individual
  changes +0.08840, -0.07678, +0.01661. Lower is better. The uniformly favorable
  NLL direction from Study 10 did **not** recur here. Its earlier probability-score
  signal must not be described as reliably replicated or as stronger factual memory.
- Foil discrimination, the separation between a correct and a same-template wrong
  answer, increased by **+0.05443 +/- 0.03272**, range +0.03256 to +0.09205.
  This secondary positive signal is preserved, but cannot replace the primary
  or establish hidden representations were retained. Only one foil per fact was used.
- Terminal accuracy differed by **-0.500 +/- 1.803 pp**, range -2.000 to +1.500.
  Study 10's favorable terminal pattern did not consistently recur either.
- New-fact terminal accuracy differed by **-2.667 +/- 3.055 pp**, range -6.000
  to 0.000. This does not establish a robust cost, but rules out claiming a
  demonstrated absence of tradeoffs. Held-out filler loss differed by
  -0.00062 +/- 0.00108, range -0.00171 to +0.00046.
- No primary checkpoint reached the registered <=2% floor or >=98% ceiling.
  All training steps were clipped in both arms. Clipped target coefficient per
  exposure differed by +0.00021 +/- 0.00016; coefficients are not Adam-update
  attribution and do not demonstrate equal effective learning pressure.
- Pre-injection loss differences were nonzero, with maxima 7.15e-7, 7.15e-6 and
  0.0015869 for seeds 6,7,8 respectively. Exact paired CPU inputs matched; MPS
  numerical behavior is not guaranteed identical. No threshold was invented to
  discard a seed after seeing its result.

## Relationship to prior work and next decision

Study 9: +4.238 +/- 5.866 pp, range -2.000 to +9.643; mixed/inconclusive.
Study 10: +1.143 +/- 2.767 pp, range -0.929 to +4.286; mixed/inconclusive.
Study 11: -1.929 +/- 2.389 pp, range -4.643 to -0.143; mixed/inconclusive.
These blocks are displayed separately, not pooled for a significance claim.
Study 11 was selected after observing the first two. Repeated continuation screens
can favor chance positives; that limitation would also apply to a favorable result.

The preregistered cautious prediction was not contradicted. The positive condition
for considering a larger gap replication was not met. Following the user's finite
budget decision, recommend parking this gap comparison and explaining selective
replay as a possible next question: at the same total replay budget, is selecting
previously learned but deteriorating facts better than random selection?
This is a proposal, not authorization to start. Never-learned difficulty must be
separated from deterioration. No new study or extra seed has been launched.

Scope remains one small model, a synthetic generator and this training protocol.
This does not establish a universal best gap, brain-like consolidation,
personalization benefits, PEFT transfer, or representation erasure.

## Evidence and reproducibility

- [Full numerical report](REPORT.md) and [raw summary](summary.json).
- [Independent completion audit](AUDIT.md); 46 software tests passed.
- `uv run --no-sync python results/study11/audit_results.py` verifies the stored
  evidence without model evaluation or training. The audit script was written
  after outcomes existed; it checks existing measurements, not a new hypothesis.
- Registration 1aac057; runner/tests 8c8eb15; manifest 90eda1f; verified launch
  handoff 775c78e. All files and six original outcomes are retained locally.
