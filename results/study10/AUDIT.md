# Completion audit — 9 September 2026

Audit performed after all six runs finished and before creating the infographic.
No training processes remained. This is post-run verification, not preregistration.

- freeze_manifest() reproduced the existing manifest and its contents exactly
  matched git show ea5ac56:results/study10/manifest.json. No historical manifest
  was replaced. Current source, model files, filler, packages and input streams
  passed the frozen checks.
- All six logs loaded via registered config and exact-schedule validation, using
  seeds 3,4,5 only. Paired fact/interference content, CPU streams, package fields,
  first/last exposure times, gap multisets and budgets passed.
- Independently traversed raw logs for finite floating-point values.
- All runs had 2300 optimizer steps/step guards, 2,208,000 filler tokens,
  1000 target exposures and 200 interference exposures. Full target schedule
  count checked independently.
- Recomputed 22 measures for each run directly from raw evals, schedules and
  guards without calling the runner's metrics() or analyze(). Used Python
  statistics.mean/stdev and direct sums, then checked all 66 metric-by-arm
  blocks, including individual values, means, sample SDs, min and max, against
  summary.json with 1e-10 absolute/relative tolerance.
- The three independently recomputed primary differences in percentage points:
  -0.9285714285714286, +0.07142857142857784, +4.285714285714287.
- NLL differences: -0.08710236955533879, -0.06501746636083627,
  -0.12802659180281406. Primary remains mixed_or_inconclusive.
- No pooling, refitting, outcome-dependent run addition or changed threshold.

Raw log SHA-256:

| Run | SHA-256 |
|---|---|
| spaced_s3 | f92aea0c67b82f1d96f17480b65d5d1db9861a310fcd32bed21b34a3de6aee1b |
| variable_gaps_s3 | cf70586073d7e4ab028539df0a8c0a3443ca1e02d39ee24fd8798d0a4b7c9ac5 |
| spaced_s4 | 96507b7ed84747bd3a62f16bec1461ba92b6b722ae8a291e9330a673d626cc26 |
| variable_gaps_s4 | 3a73077cb6e05b9b5bfe7fb17f7220afcf724ace9c4601e8f80c9e68d6886c1e |
| spaced_s5 | 0f7b6853977fe2d706455062854b8bd495b6679feeb9eb02271b4436c500bd12 |
| variable_gaps_s5 | 8b5c131a907b7bc749c16ec8c75c51e62f41ac1e8922fe08e24ba6d67e68c0f7 |
