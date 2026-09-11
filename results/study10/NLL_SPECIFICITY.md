# Post-hoc true-versus-foil NLL check

9 September 2026. Analysis description committed in afb7252 before computing the
additional foil summaries. This is a post-hoc clarification, NOT preregistered new
evidence: true NLL and discrimination were already reported and algebraically
determine foil NLL. All values were recomputed from per-fact logs, no new training.

## Result

The observed decrease in true-answer NLL does not identify a fact-specific benefit.
Incorrect same-template answers also received lower NLL on average (two of three
seeds), and true-versus-foil separation did not consistently improve. This was
already visible in the reported discrimination guard; the table makes it explicit.

Mean ± sample SD [min,max], across seeds 3,4,5:

| Measure | Fixed | Variable | Variable minus fixed |
|---|---|---|---|
| True-answer NLL (lower better) | 1.33402 ± 0.11821 [1.19803,1.41221] | 1.24063 ± 0.14777 [1.07000,1.32680] | -0.09338 ± 0.03197 [-0.12803,-0.06502] |
| Incorrect-answer NLL | 3.13244 ± 0.03299 [3.11302,3.17052] | 3.02455 ± 0.11926 [2.89006,3.11744] | -0.10789 ± 0.15170 [-0.28046,+0.00442] |
| Separation, foil minus true (higher better) | 1.79842 ± 0.10328 [1.72121,1.91574] | 1.78392 ± 0.21567 [1.56496,1.99615] | -0.01450 ± 0.15499 [-0.19336,+0.08041] |

| Seed | True-NLL delta | Foil-NLL delta | Separation delta |
|---|---:|---:|---:|
| 3 | -0.08710 | -0.28046 | -0.19336 |
| 4 | -0.06502 | +0.00442 | +0.06944 |
| 5 | -0.12803 | -0.04762 | +0.08041 |

## Interpretation and explicit correction

The user-facing description of an "encouraging probability signal" must not be
read as evidence of stronger factual memory. Both candidate answer scores can
improve together. True NLL improved in all three runs, but the contrast with an
incorrect answer does not show a consistent benefit. This does not prove the gain
is entirely format learning, assign a format percentage, prove no effect, or imply
erasure. The exact-match primary remains mixed/inconclusive and unchanged.

These NLLs average teacher-forced log losses per answer token and then per fact;
they are not directly normalized probabilities over complete candidate answers.
One cyclic same-template foil per fact is a limited control; answer token lengths
can differ. We should not launch another true-NLL-only replication without a
prospectively chosen specificity check (e.g. multiple length-matched foils and a
subject-swap control). This would require fresh model evaluations and a new plan,
not a claim made by the present logs.

## Verification and background

All 200 per-fact true/foil entries were used at each of the seven registered
checkpoints for each run. Their means and differences matched stored nll,
nll_foil and disc aggregates, and original summary values, within 1e-10.
No fact filtering, new significance threshold, pooling or model fitting occurred.

Relevant analogy only: [Zhao et al., ICML 2021](https://proceedings.mlr.press/v139/zhao21c.html)
shows answer biases and contextual calibration in few-shot prompting. It motivates
checking answer propensity but does not establish the cause of this fine-tuning result.
