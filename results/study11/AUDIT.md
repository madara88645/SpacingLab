# Independent completion audit — 10 September 2026

All six authorized runs finished. Execution session 62040 exited with code 0,
six COMPLETE markers and STUDY11_DONE. No Study 11 training process remained.
No restart, extra seed, additional model evaluation or parameter change was made.

Post-run verification script: audit_results.py. It does not call the runner's
metrics(), analyze() or direction(), and does not instantiate a language model.
It uses the frozen tokenizer only to independently count actual input tokens.
This is verification of recorded results, not a preregistered new experiment.

Verified with 1e-10 absolute/relative numerical tolerance where appropriate:

- The immutable manifest equals its pre-evaluation Git record in 90eda1f; the
  registration equals its initial commit 1aac057. Every frozen source hash matches
  current files and pre-evaluation code commit 8c8eb15. Model/tokenizer file hashes,
  the filler snapshot, Python and package versions match the frozen values.
- Both source commits recorded by runs, 90eda1f and 775c78e, contain exactly the
  registered source bytes. The latter only added the launch handoff after the
  first run began. All runs report tracked_code_dirty=false; no silent code drift.
- Independently reconstructed all seed-specific 64-token chunk permutations,
  training/held-out input hashes and full filler-token digest. No mutable cache use.
- Independently regenerated every target schedule from the registered random draw
  and gap construction, all first/last times, and all interference schedules.
  Each old fact has exactly five exposures over 256 steps, with correct gap values.
- Checked 2300 consecutive step guards and 92 sampled training losses per run.
  Every step's old/new fact count and nominal/clipped coefficient agrees with the
  actual schedule and clipping rule. Floating-point values in all raw logs are finite.
- Every run has 2,208,000 filler input tokens, 1000 old-fact and 200 new-fact
  exposures. True old+new fact input-token budgets independently retokenized:
  seed 6: 18,431; seed 7: 18,735; seed 8: 18,500. Each paired arm matches exactly.
- Recomputed each of the ten evaluations from all 200 per-fact correctness/NLL
  entries and foil scores, plus at-last-exposure guards. Seven interference
  checkpoints and global step numbers match the registration.
- Recomputed all 22 metrics per run using direct sums and Python statistics,
  checked all 66 metric-by-arm summary blocks (values, mean, sample SD, min/max),
  and checked every numeric metric table row in REPORT.md against summary.json.
- Independently verified all pre-intervention diagnostics and the decision rule.
  Primary deltas are -0.0464285714, -0.0100000000, -0.0014285714. Their absolute
  mean 0.0192857143 is below sample SD 0.0238938981: mixed_or_inconclusive.
- Full software suite: 46 passed. Audit status: PASS. No pooled test or fitted
  post-hoc threshold. New-fact outcomes and internal representations cannot be
  re-evaluated from absent model checkpoints; this audit validates stored evidence.

The recorded guards include wall_seconds: six training loops took 822.9 to 868.9
seconds each, about 84.6 minutes in total, excluding startup/parent audit overhead.
Contrary to the earlier idea scout's timing caveat, timing is available in these
JSON guards; no timing estimate needs to be inferred from optimizer step counts.

## Raw log SHA-256

| Run | SHA-256 |
|---|---|
| spaced_s6 | eba43ea31525a8cbb33c1ab96aec14b668b865a305a7bd9697837447fb8a84e3 |
| variable_gaps_s6 | f1fc32edf5dc754cd4f751799d3c0e6e3cfa3d03456b11948468f0ec397d3085 |
| variable_gaps_s7 | 4e01637faf90cecaaf7966f2068b255addb8b5e836d78dc6859549c9ff27f65d |
| spaced_s7 | e8ca506ff48c8bcde265a514a6ed52fa39c47ee4c1b5899c2b7c0687e07f29f7 |
| spaced_s8 | d966980b478f169b95b31d8c0d02423e9e63522abcde7670c1fdb11cca0b0028 |
| variable_gaps_s8 | 3d7282aa90164a6de9d84a72167fb6262d2d31c52964891f5ce29a4b345f8bf0 |
