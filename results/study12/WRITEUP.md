# Study 12: selecting deteriorating facts helped in this small replay screen

10 September 2026. Three preregistered paired seeds, all completed and audited.

## Finding

Under equal replay budgets and identical learned model/optimizer starts,
deterioration-prioritized replay improved mean old-fact exact-answer accuracy by
**3.23 percentage points, sample SD 1.62**, relative to uniform replay. The paired
differences were +2.40, +2.20 and +5.10 points. This meets the preregistered positive
directional screen; it is **not a statistical-significance or general-superiority
claim**. Three pairs are a small screen, not a powered confirmatory experiment.

The primary averages five delayed tests on all 200 old facts, not just selected
items or the immediately post-replay score. Uniform: **43.63% +/- 3.59 points**;
prioritized: **46.87% +/- 4.61 points** (mean +/- sample SD across seeds).

| Seed | Uniform | Prioritized | Difference, percentage points |
|---|---:|---:|---:|
| 9 | 39.50% | 41.90% | +2.40 |
| 10 | 45.50% | 47.70% | +2.20 |
| 11 | 45.90% | 51.00% | +5.10 |

Prediction: positive primary directional signal. Outcome: supported **at the
registered screening level only**. The rule requires all three differences to be
positive and their mean to exceed their sample SD. It does not compute a p-value
or confidence interval. No earlier studies were pooled and no seeds added.

## What was held constant, and what changed?

One GPT-2 124M model, full fine-tuning on synthetic sentence facts and a frozen
WikiText filler stream, local Apple Silicon/MPS. Each seed used one common
800-update acquisition prefix: five exposures per old fact, gap 64, held constant
as a reference rather than asserted optimal. Its model **and AdamW optimizer
moments** were saved and restored into both 1500-update continuations. The same
50 new facts received four exposures per continuation.

Only old facts answered correctly at the common fork could be selected: 123,140,139
eligible facts (mean 134, SD 9.54). Common accuracy was 67.00% +/- 4.77 points and
common answer NLL 0.43124 +/- 0.12705, identical between arms within each seed.
All 200 old facts remained in the primary denominator.

At updates 100,300,600,900 both arms received identical no-gradient tests. Priority
used `max(0, current answer NLL - common answer NLL)`: an answer becoming less
probable since the common reference, not simply the currently hardest question.
The reference remained fixed: accumulated deterioration, not instantaneous
forgetting speed. Uniform selection ignored scores. Probes did not teach the model.

Each arm replayed 20 distinct eligible facts per round, 80 exposures in total.
Uniform draws defined full-input-length slots; priority ranked within those length
buckets. One item was appended per update at 101–120,301–320,601–620,901–920.
Filler and new facts were not displaced. Actual paired input lengths, padded row
counts, update counts and probes match at every step. Replay tokens by seed were
1210,1210,1226 in **both** arms. Each continuation had 1,440,000 filler tokens.

Primary checkpoints were 200,400,800,1200,1500 with equal weights. The last test
followed 580 updates without old-fact replay. Choices were recorded before evaluation.

## Guard quantities and alternative explanations

Differences below are prioritized minus uniform, mean +/- sample SD across three
pairs. Full arm spreads, values and ranges are in [REPORT.md](REPORT.md) and
[AUDIT.md](AUDIT.md); machine-readable guard summaries are in audit.json.

- **Initialization:** saved checkpoint/state hashes match both branch starts,
  including populated optimizer moments at step 800. Before first replay, accuracy
  and per-fact correctness match exactly at updates 50 and 100. Tiny MPS numerical
  differences remain: maximum absolute per-fact NLL difference across these probes
  is 0.00006342. We do not claim bit-identical continuations.
- **Terminal accuracy:** difference +4.00 +/- 3.04 points; individual differences
  +5.50,+0.50,+6.00. The middle-seed difference is not strong standalone evidence.
  Uniform 43.00% +/- 3.97 points; priority 47.00% +/- 3.28.
- **NLL is not a representation assay:** true-answer checkpoint-mean NLL changes
  by -0.06533 +/- 0.04882, but incorrect same-template foil NLL also changes by
  -0.06412 +/- 0.02305. True-versus-foil separation changes by only +0.00121 +/-
  0.06925, a mixed result. NLL does not independently establish improved factual
  separation, erased/restored representations, or a mechanism. This qualification
  does not remove the measured exact-answer accuracy effect.
- **Coverage is a live explanation:** priority replayed 75,73,75 distinct facts
  versus uniform's 62,68,65. Means are 74.33 +/- 1.15 versus 65.00 +/- 3.00;
  paired difference +9.33 +/- 4.04 facts. This identifies the whole policy, not a
  benefit of deterioration scores independent of avoiding repeated visits to the
  same items. No coverage-matched arm was tested.
- **Allocation changed:** priority used no zero-score fallback slots; uniform
  selected 5,1,2 zero-score items across its four rounds. Full overlaps, template,
  length and per-item repeat distributions are retained in the audit. Templates
  were not separately matched; length constraints affect who receives replay.
- **Updates differ in magnitude:** every replay-containing batch was clipped.
  Replay-batch preclip gradient norms averaged 2.03395 +/- 0.07578 for uniform
  versus 2.10415 +/- 0.04984 for priority. Clip scales were 0.49958 +/- 0.01436
  versus 0.48384 +/- 0.00811. Equal tokens do not mean equal gradients, optimizer
  trajectories or effective update magnitudes.
- **Unselected old subgroup:** among facts incorrect at the common fork,
  checkpoint-mean accuracy was 10.51% +/- 4.29 points for uniform versus 9.27% +/-
  3.98 for priority; difference -1.23 +/- 1.02 points. This subgroup was ineligible
  in both arms. This is descriptive, not a separate primary test, and cautions
  against claiming every subgroup benefits. Incorrect at the fork does not prove
  a fact was never learned earlier.
- **New learning/background language:** terminal new-fact accuracy difference
  +0.67 +/- 3.06 points and NLL difference +0.00869 +/- 0.05533 are mixed.
  New-fact accuracy is near ceiling (96–100% across arms/seeds), so it cannot
  establish no learning cost. Held-out filler loss difference +0.00017 +/- 0.00130
  and parameter displacement difference -0.01851 +/- 0.04915 are also mixed,
  not equivalence evidence. No primary old-accuracy checkpoint hits the registered
  floor <=2% or ceiling >=98%.
- **Runtime:** prefixes averaged 344.80 +/- 28.49 seconds. Continuations averaged
  637.77 +/- 40.23 seconds for uniform versus 668.84 +/- 15.95 for priority;
  paired difference +31.07 +/- 54.08 seconds, mixed. Summed recorded stages took
  82.6 minutes, excluding some orchestration overhead. Both arms were probed equally;
  a deployed uniform policy could omit selection probes. Equal deployment cost
  was not established.

## Scope and next test

This modest result says that a fixed replay budget was more effective under this
complete selection policy than independent uniform round draws. It does not
establish benefits for PEFT, personal writing style, larger models, unseen phrasing
or broad skills. Canonical training facts and labels supplied feedback and tests.
There was no no-replay arm, so replay versus no replay was not estimated. Neither
biological consolidation nor a general solution to catastrophic forgetting follows.

Continuing is worthwhile **with a diversity/coverage-matched random control**:
random replay that also limits revisits and covers a comparable number of distinct
facts. Pre-register its matching rule before running. This would address whether
deterioration scores add value beyond wider coverage; simply adding seeds here
would improve precision but not resolve that explanation. This is a proposal, not
a launched study. No further experiment until Mehmet understands and approves it.

## Reproducibility

Registration dd3e56c; tested implementation d19c63f; manifest 59cf386; launch receipt
eb38dcc. Finite process exit 0, STUDY12_DONE. Independent post-run audit reconstructed
11,400 update rows, 24 selections, old per-fact aggregates and all 30 main summary
blocks; 60 software tests passed again. See [AUDIT.md](AUDIT.md) for limits: no
fresh logits or unlogged per-new-fact outputs were recovered. Original logs, local
forks, preregistration and frozen source are preserved. No new training was started.
