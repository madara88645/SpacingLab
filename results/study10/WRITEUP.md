# Study 10: variable-gap replication did not establish a primary-score advantage

## Finding

The new three-seed replication was **mixed/inconclusive on the preregistered primary
measure**. Variable gaps improved its mean by 1.14 percentage points, but paired
sample SD was 2.77 points and one of the three differences was negative. Lower
answer NLL in all three seeds and higher terminal accuracy in all three are useful
secondary observations, not grounds to replace the primary endpoint after the fact.

## What was tested

Six fresh full-fine-tuning runs of GPT-2 124M on Apple Silicon. Seeds 3,4,5 each
had a fixed-gap arm [64,64,64,64] and a per-fact randomly permuted [32,32,64,128]
arm. Every fact had exactly five exposures, identical first/final exposure times,
and span 256. There were 200 synthetic facts and the same pinned WikiText filler
within each pair, followed by 1500 steps including 50 new facts. Each run had
2300 optimizer steps. The primary score is the unweighted average of exact-match
accuracy at seven interference checkpoints, not the final checkpoint or time AUC.

Study 9 was already known when this replication was selected. The six-run sample
size and seeds, unchanged protocol, metrics, traps and decision rule were committed
in a4b3079 before any new outcomes. Code was committed in ef1d996 and the frozen
model/data/source/software manifest in ea5ac56 before evaluation. No tuning or
optional extra runs took place. The three new pairs are analyzed separately, not
pooled with the preceding study.

## Results

All mean ± sample SD values describe three seed settings; ranges are min–max.
Accuracy is expressed in percentage points for differences.

| Primary score | Fixed | Variable | Variable minus fixed |
|---|---:|---:|---:|
| Seed 3 | 27.50% | 26.57% | -0.93 pp |
| Seed 4 | 27.50% | 27.57% | +0.07 pp |
| Seed 5 | 30.14% | 34.43% | +4.29 pp |
| Mean ± SD | 28.38% ± 1.53 pp | 29.52% ± 4.28 pp | +1.14 ± 2.77 pp |
| Range | 27.50–30.14% | 26.57–34.43% | -0.93 to +4.29 pp |

The registered heuristic requires all differences to have the same sign and mean
magnitude greater than sample SD for a consistent directional signal. It fails for
a positive primary effect. It is not a significance/equivalence test. The cautious
prediction of no consistent primary positive signal was not contradicted; this does
not establish the absence of an effect.

**Secondary NLL:** checkpoint-mean answer negative log likelihood, lower is better,
was 1.33402 ± 0.11821 [1.19803,1.41221] fixed versus 1.24063 ± 0.14777
[1.07000,1.32680] variable. Paired delta -0.09338 ± 0.03197
[-0.12803,-0.06502], with seed deltas -0.08710, -0.06502, -0.12803.
This suggests an answer-probability benefit in this protocol even though exact
output accuracy did not show a consistent primary improvement. NLL is not evidence
by itself that an internal representation survives or that fact-specific knowledge
rather than answer form caused the change. Foil discrimination did not consistently
improve: paired mean -0.01450 ± 0.15499 [-0.19336,+0.08041].

**Terminal accuracy:** 14.67% ± 4.19 pp [12.00–19.50%] fixed versus
19.17% ± 4.75 pp [14.50–24.00%] variable. Paired delta +4.50 ± 2.00 pp
[+2.50,+6.50]. Terminal NLL delta -0.17361 ± 0.07554 [-0.25939,-0.11705].
These are secondary endpoints; presenting the terminal +4.50 as the main result
would conceal the registered seven-checkpoint mean result.

## Guard quantities and limits

- Acquisition was not equal: last-exposure accuracy delta +1.00 ± 7.09 pp
  [-7.00,+6.50]; window-end delta +4.50 ± 5.20 pp [+1.50,+10.50]. An
  acquisition-independent forgetting-rate claim is not warranted. Similar means
  are not a formal acquisition-equivalence test.
- Each arm in every pair used 2300 steps, 2,208,000 filler tokens, 1000 target
  exposures and 200 interference exposures. Fact token counts and complete
  schedules/budgets matched within pairs as required.
- First/last times and gap multisets were verified per fact; middle positions,
  gap magnitudes and batch composition still differ. This does not isolate
  randomness alone.
- New-fact terminal accuracy delta -2.67 ± 7.02 pp [-10.00,+4.00] does not establish
  a reliable cost or no cost. Held-out filler loss delta -0.00081 ± 0.00072
  [-0.00133,+0.00002] is tiny; do not market it as an additional improvement.
- All steps were clipped in all six runs. Clipped coefficients and parameter
  displacements remain in REPORT.md; they do not establish equal per-fact Adam
  updates. Neither arm's primary checkpoints hit the predefined floor/ceiling.
- Pre-intervention losses differed by at most 0.0000138283 within pairs; pretrained
  held-out losses were identical. Exact CPU input provenance matched. Numerical
  MPS reproducibility is not guaranteed.
- One small pretrained model, synthetic facts, one data/optimizer protocol, and
  three new seed settings. No human-memory mechanism, personalization, PEFT/LoRA,
  general capability preservation, universal best gap, or erasure claim is tested.

## Relationship to Study 9 and next decision

Study 9 stays mixed/inconclusive: primary delta +4.24 ± 5.87 pp
[-2.00,+9.64]. Study 10's +1.14 ± 2.77 pp [-0.93,+4.29] does not reproduce a
clear primary advantage. Do not relabel either or pool for a significance claim.

A further study could prospectively test the secondary NLL/terminal signal with
new data and a fixed sample size, explicitly acknowledging why those endpoints
were selected. That narrow follow-up may be worth doing; more repetitions merely
to obtain a favorable primary label are not. No additional experiment has started.

All 66 metric-by-arm summary blocks were recomputed independently from six finite
raw logs; frozen source/model/data/software provenance matches the pre-evaluation
Git record. See AUDIT.md and the complete machine-readable summary.
