# Resume SpacingLab — Study 8 active (2026-09-08)

## Current state

Study 7 finished: all six raw logs, progress logs, console logs and the paired summary
were committed in `4f84b3a`. Data/model/source and paired guards were verified before
the user's status answer. Retention random-minus-spaced was +0.09286 (sample SD
0.04586; range +0.06357 to +0.14571), with NLL in the same direction. This was a
placement-policy result, not a last-exposure-recency-controlled result.

The user then explicitly authorized the last-exposure control. **Study 8 is running.**
Do not launch a duplicate. Registered design: `docs/STUDY8_PREREGISTRATION.md`,
commit `7547cf8`; implementation `2aeb80b`; pre-evaluation manifest `fafbd6b`.
29 tests passed, two successive preflights passed, and first pretrained evaluation
plus optimizer step 0 were observed. No Study 8 outcome yet.

Command: `uv run --frozen python -u -m spacinglab.study8 --run`.
Exec session 59926; initial parent PID 22035, worker PID 22037 (verify live).
Order: spaced0, random_matched0, random_matched1, spaced1, spaced2, random_matched2.
Estimated whole chain roughly 1.5–2 hours, uncertain. Serial MPS; no remote compute.

## What the new control does

Both arms freshly trained. Same data/model/software, same per-seed facts, same final
exposure of **every fact**, not just the same mean date. Spaced has fixed gap 64.
Random matched samples four distinct earlier times from [0,p_i), then includes p_i.
Seed for earlier times = seed+30000. Number of exposures = five in both arms.

Actual target schedules are logged and checked against their registered construction.
Complete schedule and final-time equality are checked before a pair is accepted.
First-time/span metrics, acquisition, NLL, clipping, batch-weight and new-learning
guards remain in the analysis. Earlier exposure history still differs: if the effect
vanishes that does not prove recency mediated all of Study 7. If it persists, this
comparison excludes a last-exposure-recency-only explanation. See registration for
the directional rule and prediction; do not introduce a new threshold.

## How to inspect and finish

Look at `results/study8/<condition>_s<seed>/console.log` and `progress.json`.
Only `log.json` means a completed run. After six validated logs the chain automatically
creates `results/study8/summary.json` and `REPORT.md`, then prints `STUDY8_DONE`.
No recurring monitor/notification automation exists; the finite process runs and analyzes.

On completion: verify all six logs, exact schedule/last-time matching, paired data/
model/budgets and the generated numbers; inspect NLL/acquisition/new-learning tradeoffs;
update English and short Turkish reports, then commit all evidence locally. Do not
claim an outcome from one seed. A status-only question permits inspection/reporting;
do not infer authority for extra studies.

On a stop request, check live PIDs and terminate only this chain and its worker;
preserve partial attempts. On interruption, completed runs can be skipped after checks;
an incomplete nonempty attempt must be retained and a restart documented before retry.
The chain refuses silent overwrites. Do not change source/lock/registration/model/data
during execution: manifests reject drift.

## Reproducibility and earlier caveats

Current immutable filler SHA-256:
`868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304`.
GPT-2 revision: `607a30d783dfa663caf39e06633721c8d4cfcd7e`.
Full file hashes/software versions are in each study's manifest.

Shared training source changed for Study 8. To exactly rerun Study 7 from its pinned
manifest, use its historical source commit in a separate authorized checkout; do not
replace its old manifest with the new source hashes. Historical `--analyze` reads
stored logs, but compare calculations to frozen source before making reproducibility claims.

Read `docs/PROVENANCE_AUDIT_2026-09-08.md` for the old mutable-cache failure. Study 6b's
unmatched-data recommendation remains withdrawn; Study 7 is separate fresh evidence.
Study 3 did not establish erasure, unusable representations, or a unique 90%-format
decomposition. Preserve failed predictions and three-seed uncertainty.

`uv run --frozen pytest -q` runs software tests (no model training).
Never touch ForgetLab. No remote/push/publication without user approval. If subagents
are needed, every one must explicitly use Sonnet. None used in these continuations.
Explain results with short student-level examples; no unexplained jargon.
