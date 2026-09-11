# Study 12 completion audit

PASS. Post-run verification only, not a new experiment or new registered hypothesis.
Reproduce: `uv run --no-sync python results/study12/audit_results.py`.
The frozen training/analysis source, tests, dependencies and manifest are unchanged.

## Checks

- Registration dd3e56c -> implementation d19c63f -> manifest 59cf386 -> launch record eb38dcc; Git ancestry and committed source bytes verified.
- Every model/tokenizer file, dataset, dependency version, Python version and frozen source file matches the manifest.
- Three saved model/optimizer forks hash to the recorded branch starts. Adam moments are populated, step counters are 800, and learning rate/betas/weight decay match.
- Full acquisition and new-fact schedules rebuilt; every one of 11,400 logged update rows has the expected filler bytes, item IDs, token lengths, replay timing and loss/clipping coefficients.
- All 24 replay selections independently rebuilt from the saved reference/current scores and length slots; eligibility, uniqueness, seeded ties and fallback counts match.
- Old-fact accuracy reconstructed from saved generated answers; NLL and foil aggregates reconstructed from per-fact arrays. All 30 summary blocks and generated report table entries match.
- No extra training, seed replacement, partial failed attempts or model inference was performed by this audit.

## Common acquisition

Values in seed order 9,10,11; every spread below is sample SD, not a confidence interval.

| Quantity | Seed values | Mean +/- SD [min,max] |
|---|---|---|
| eligible_count | [123, 140, 139] | 134.00000 +/- 9.53939 [123.00000, 140.00000] |
| common_accuracy | [0.615, 0.7, 0.695] | 0.67000 +/- 0.04770 [0.61500, 0.70000] |
| common_nll | [0.5738494673872993, 0.33013267483191155, 0.38974085300578737] | 0.43124 +/- 0.12705 [0.33013, 0.57385] |
| last_exposure_accuracy | [0.745, 0.845, 0.915] | 0.83500 +/- 0.08544 [0.74500, 0.91500] |
| prefix_wall_seconds | [315.01715898513794, 347.57061886787415, 371.80186700820923] | 344.79655 +/- 28.49381 [315.01716, 371.80187] |

## Paired secondary guard summaries

Means aggregate one value per seed; gradient/clipping quantities first average replay updates within each seed.
These are descriptive checks, not additional primary hypothesis tests.

| Quantity | Uniform | Prioritized | Prioritized minus uniform |
|---|---|---|---|
| distinct_replayed | 65.00000 +/- 3.00000 [62.00000, 68.00000] | 74.33333 +/- 1.15470 [73.00000, 75.00000] | 9.33333 +/- 4.04145 [5.00000, 13.00000] |
| replay_mean_deterioration | 0.81449 +/- 0.09786 [0.71262, 0.90778] | 1.45684 +/- 0.06663 [1.40606, 1.53228] | 0.64235 +/- 0.04491 [0.60911, 0.69343] |
| replay_gradient_mean | 2.03395 +/- 0.07578 [1.96017, 2.11158] | 2.10415 +/- 0.04984 [2.06212, 2.15921] | 0.07020 +/- 0.02830 [0.04763, 0.10195] |
| replay_clip_scale_mean | 0.49958 +/- 0.01436 [0.48565, 0.51433] | 0.48384 +/- 0.00811 [0.47540, 0.49158] | -0.01574 +/- 0.00639 [-0.02275, -0.01025] |
| replay_clipped_fraction | 1.00000 +/- 0.00000 [1.00000, 1.00000] | 1.00000 +/- 0.00000 [1.00000, 1.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| replay_coefficient_mean | 0.06193 +/- 0.00016 [0.06176, 0.06209] | 0.06193 +/- 0.00016 [0.06176, 0.06209] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| clipped_replay_coefficient_mean | 0.03097 +/- 0.00083 [0.03013, 0.03178] | 0.02999 +/- 0.00045 [0.02950, 0.03038] | -0.00098 +/- 0.00039 [-0.00140, -0.00063] |
| final_displacement | 118.78956 +/- 0.30923 [118.46409, 119.07948] | 118.77105 +/- 0.31445 [118.42082, 119.02912] | -0.01851 +/- 0.04915 [-0.05036, 0.03809] |
| eligible_retention | 0.60171 +/- 0.01020 [0.59000, 0.60863] | 0.65564 +/- 0.02620 [0.63143, 0.68345] | 0.05393 +/- 0.01821 [0.04143, 0.07482] |
| initially_unlearned_retention | 0.10506 +/- 0.04293 [0.05714, 0.14000] | 0.09272 +/- 0.03982 [0.04675, 0.11667] | -0.01233 +/- 0.01017 [-0.02333, -0.00328] |
| retention_foil_nll | 3.19365 +/- 0.06583 [3.11881, 3.24257] | 3.12953 +/- 0.07232 [3.04692, 3.18139] | -0.06412 +/- 0.02305 [-0.08228, -0.03819] |
| wall_seconds | 637.76941 +/- 40.23076 [592.05156, 667.76434] | 668.84409 +/- 15.95477 [651.03257, 681.82625] | 31.07468 +/- 54.08243 [-16.73177, 89.77469] |

## Exact per-pair budgets and allocation

Each continuation has 1500 updates, 80 old replays, 200 new-fact exposures, and 1,440,000 filler input tokens.
Paired lengths match at every update; padded row counts and replay loss coefficients therefore match too.
Template order: capital, birthplace, river/lake, currency, founder. Histograms include all 200 old facts.

### Seed 9

Pre-replay drift: `{"50": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 2.4318695068359375e-05, "nll": -3.449898213769842e-07}, "100": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 2.2172927856445312e-05, "nll": 2.4501979352109515e-06}}`

uniform: `{"distinct_replayed": 62, "fact_tokens": 4282, "length_counts": {"12": 4, "13": 8, "14": 22, "15": 16, "16": 11, "17": 11, "18": 5, "19": 3}, "replay_count_histogram": {"0": 138, "1": 47, "2": 13, "3": 1, "4": 1}, "replay_tokens": 1210, "template_counts": [20, 13, 18, 13, 16], "uniform_overlap": [20, 20, 20, 20], "zero_score_slots": [0, 0, 2, 3]}`

prioritized: `{"distinct_replayed": 75, "fact_tokens": 4282, "length_counts": {"12": 4, "13": 8, "14": 22, "15": 16, "16": 11, "17": 11, "18": 5, "19": 3}, "replay_count_histogram": {"0": 125, "1": 70, "2": 5}, "replay_tokens": 1210, "template_counts": [18, 18, 17, 16, 11], "uniform_overlap": [4, 3, 4, 3], "zero_score_slots": [0, 0, 0, 0]}`

### Seed 10

Pre-replay drift: `{"50": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 9.655952453613281e-06, "nll": 4.759547300725586e-07}, "100": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 1.609325408935547e-05, "nll": -8.755736053966956e-07}}`

uniform: `{"distinct_replayed": 68, "fact_tokens": 4342, "length_counts": {"11": 1, "12": 5, "13": 5, "14": 19, "15": 21, "16": 14, "17": 8, "18": 2, "19": 3, "20": 2}, "replay_count_histogram": {"0": 132, "1": 56, "2": 12}, "replay_tokens": 1210, "template_counts": [22, 12, 16, 13, 17], "uniform_overlap": [20, 20, 20, 20], "zero_score_slots": [0, 0, 1, 0]}`

prioritized: `{"distinct_replayed": 73, "fact_tokens": 4342, "length_counts": {"11": 1, "12": 5, "13": 5, "14": 19, "15": 21, "16": 14, "17": 8, "18": 2, "19": 3, "20": 2}, "replay_count_histogram": {"0": 127, "1": 66, "2": 7}, "replay_tokens": 1210, "template_counts": [19, 13, 16, 15, 17], "uniform_overlap": [2, 4, 6, 4], "zero_score_slots": [0, 0, 0, 0]}`

### Seed 11

Pre-replay drift: `{"50": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 6.341934204101562e-05, "nll": -4.552453756190289e-06}, "100": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 2.1576881408691406e-05, "nll": 4.025548696606762e-07}}`

uniform: `{"distinct_replayed": 65, "fact_tokens": 4410, "length_counts": {"12": 3, "13": 5, "14": 21, "15": 14, "16": 20, "17": 9, "18": 6, "20": 2}, "replay_count_histogram": {"0": 135, "1": 52, "2": 11, "3": 2}, "replay_tokens": 1226, "template_counts": [17, 15, 24, 9, 15], "uniform_overlap": [20, 20, 20, 20], "zero_score_slots": [0, 0, 1, 1]}`

prioritized: `{"distinct_replayed": 75, "fact_tokens": 4410, "length_counts": {"12": 3, "13": 5, "14": 21, "15": 14, "16": 20, "17": 9, "18": 6, "20": 2}, "replay_count_histogram": {"0": 125, "1": 70, "2": 5}, "replay_tokens": 1226, "template_counts": [19, 17, 11, 20, 13], "uniform_overlap": [1, 3, 3, 2], "zero_score_slots": [0, 0, 0, 0]}`

## Audit limits

- No new model evaluation: NLL values verified by aggregation, not by recomputing logits.
- New-fact accuracy/NLL and filler loss are logged aggregates; per-item new-fact predictions were not retained.
- Saved fork and logged branch-state hashes verify common initialization; final branch weights were not saved.
- Read-only secondary guard summaries are post-run reporting, not new primary tests.
