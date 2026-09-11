# Provenance audit: the random baseline was not a matched-data comparison

## Finding

The previous claim that ordinary random placement suffices in place of regular
spacing is **not established by Study 6b**. A mutable filler cache changes both the
training and held-out chunks even with the same seed. Historical runs also disagree
before any synthetic fact is injected. This is a failed matching assumption, not
evidence that random placement is worse.

This retrospective audit was registered in commit `a687a64` before its measurements;
its analysis code was committed as `52bf07a` before execution. It used CPU integer
arrays and existing logs, with **no new model training or tuning**. Plan:
[AUDIT_2026-09-08_PLAN.md](AUDIT_2026-09-08_PLAN.md). Machine-readable evidence:
[audit JSON](../results/provenance_audit_2026-09-08.json).

## What was tested

`build_filler_tokens` returned the entire cache, and `FillerStream` permuted every
64-token chunk. A seed reproduces a permutation only for the same input length and
contents. Growing the cache changes the permutation domain.

Git contains five cache revisions, of 198,400; 1,081,600; 2,137,600; 2,233,600;
and 2,905,600 tokens. The last two are sufficient for the common 2,300-step budget:

| Snapshot commit | Tokens | File SHA-256 |
|---|---:|---|
| `6f5408717fd94bfad70f888983cb2a11dce6ba32` | 2,233,600 | `3478801556e3609a7df7516cf843a1744587ed598c3688ce42710d5b2f6c916f` |
| `88e52ca8cf3a49ebc014b04f51e1fd99a7974e5b` | 2,905,600 | `868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304` |

For **each of seeds 0, 1, and 2**, these two snapshots produce different training,
held-out, and first-batch hashes. Integer hashes have no MPS numerical noise.
The earlier insufficient revisions are reported, not treated as completed controls.

## Historical check before the intervention

| Seed | Study 1 spaced: pretrained held-out loss | Study 6 random: pretrained held-out loss | Spaced: step-0 training loss | Random: step-0 training loss |
|---|---:|---:|---:|---:|
| 0 | 4.391357 | 4.441446 | 4.561933 | 4.384546 |
| 1 | 4.414058 | 4.467714 | 4.607787 | 4.298433 |
| 2 | 4.385477 | 4.447793 | 4.190226 | 4.218331 |

All three pre-injection training-loss prefixes differ. The intervention has not
started at these checkpoints, so its fact placement cannot explain those differences.
Together with the deterministic reconstruction and Git chronology, this supports
a historical data mismatch. However, old logs lack input hashes and complete model/
environment provenance: **we cannot prove exactly which bytes each old process read,
or exclude additional software differences**.

## What happens to the old result?

The old retention differences (random minus spaced) are +0.087857, +0.026429,
and +0.070000: mean **+0.061429**, sample SD **0.031599**, range **+0.026429 to +0.087857**.
They remain recorded measurements, but are a cross-stream descriptive comparison,
not an isolated placement effect. Their size does not repair this design problem.
The audit does not estimate how much of the difference is due to the changed data.

This does **not** retroactively invalidate all within-study massed/spaced findings.
It does require separate provenance checks for any claim that pools studies or reuses
an old control. Nor does it rescue the original H1: unequal acquisition and the
pre-registered calibration failure remain limitations.

## Other interpretation corrections

- One re-exposure with near-zero exact-match accuracy in both old and new facts is
  an insensitive savings test. It does not prove that relearning cannot use a trace.
  Several re-exposure budgets and continuous metrics would be needed.
- True-versus-foil NLL measures a relative preference under a chosen foil. It does
  not identify a unique numerical decomposition into format and factual knowledge;
  the old "90% format" statement is withdrawn.
- The reported loss-weight difference being below an arbitrary 5% threshold does not
  establish equivalence or bound its causal contribution. Extra-exposure controls
  do not supply that bound. Historical clipping statistics are missing.
- One repeat run's 0.014 score difference is one observed difference, not a calibrated
  noise distribution, significance cutoff, or equivalence margin for other studies.

## Inventory and fix

There are **73 complete main-run logs** (including one repeated run and two single-seed
contingency runs) and **12 preserved pilot logs**. These are not 73 independent
replications. Older overwritten pilots are not counted as preserved logs. The audited
main-study directories contain no incomplete run directories.

New training can use `--filler-snapshot` plus `--filler-sha256`. The loader verifies
the exact bytes before model loading, never grows/truncates the snapshot, and rejects
insufficient data. Logs record canonical training/held-out hashes, source hash,
package versions, resolved model revision, and code commit. A completed `log.json`
cannot be overwritten. Legacy calls remain available with an explicit warning;
they are **not** suitable for new matched comparisons.

Regression tests first failed, then passed after implementation. This prevents the
observed data failure mode; it does not retrospectively fill missing provenance or
prove every training variable is identical.

## Next decision

Before new mechanism claims or publication, rerun **both** random and regular-spacing
conditions freshly, in pairs for seeds 0–2, against one frozen input/model/software
snapshot. Do not compare three new random runs with the old spaced control again.
Estimate the total placement-policy effect, including recency and batch composition;
do not relabel it pure consolidation or equal-acquisition retention. Register metrics
and guards first, including NLL, last-exposure learning and clipping. Three seeds can
screen direction, not establish equivalence. If ambiguous, say so before extending.
