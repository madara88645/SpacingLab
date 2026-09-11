# Study 13 completion audit

PASS. Post-run verification only, not a new experiment or new registered hypothesis.
Reproduce: `uv run --no-sync python results/study13/audit_results.py`.
The frozen training/analysis source, tests, dependencies and manifest are unchanged.

## Checks

- Registration fbda2c9 -> implementation 80f6c88 -> manifest a80bfda -> launch record b508f69; Git ancestry and committed source bytes verified.
- Every model/tokenizer file, dataset, dependency version, Python version and frozen source file matches the manifest.
- Three saved model/optimizer forks hash to the recorded branch starts. Adam moments are populated, step counters are 800, and learning rate/betas/weight decay match.
- Full acquisition and new-fact schedules rebuilt; every one of 11,400 logged update rows has the expected filler bytes, item IDs, token lengths, replay timing and loss/clipping coefficients.
- All 24 replay selections independently rebuilt from the saved reference/current scores and length slots; global 80-item sample, used-ID exclusions, exact length capacity, cumulative coverage 20/40/60/80, seeded ties and fallback counts match.
- Old AND new fact accuracy reconstructed from saved generated answers; NLL and foil aggregates reconstructed from per-fact arrays. All 30 summary blocks and generated report table entries match.
- No extra training, seed replacement, partial failed attempts or model inference was performed by this audit.

## Common acquisition

Values in seed order 12,13,14; every spread below is sample SD, not a confidence interval.

| Quantity | Seed values | Mean +/- SD [min,max] |
|---|---|---|
| eligible_count | [145, 142, 130] | 139.00000 +/- 7.93725 [130.00000, 145.00000] |
| common_accuracy | [0.725, 0.71, 0.65] | 0.69500 +/- 0.03969 [0.65000, 0.72500] |
| common_nll | [0.3720593328152609, 0.4075137389980955, 0.49120566998063625] | 0.42359 +/- 0.06118 [0.37206, 0.49121] |
| last_exposure_accuracy | [0.81, 0.835, 0.74] | 0.79500 +/- 0.04924 [0.74000, 0.83500] |
| prefix_wall_seconds | [326.7286419868469, 315.4326910972595, 319.6271710395813] | 320.59617 +/- 5.70998 [315.43269, 326.72864] |

## Paired secondary guard summaries

Means aggregate one value per seed; gradient/clipping quantities first average replay updates within each seed.
These are descriptive checks, not additional primary hypothesis tests.

| Quantity | Uniform | Prioritized | Prioritized minus uniform |
|---|---|---|---|
| distinct_replayed | 80.00000 +/- 0.00000 [80.00000, 80.00000] | 80.00000 +/- 0.00000 [80.00000, 80.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| replay_mean_deterioration | 0.95523 +/- 0.07547 [0.87643, 1.02685] | 1.40773 +/- 0.11668 [1.27307, 1.47873] | 0.45250 +/- 0.05616 [0.39664, 0.50896] |
| replay_gradient_mean | 2.00036 +/- 0.02506 [1.97183, 2.01884] | 2.04098 +/- 0.02978 [2.00662, 2.05944] | 0.04062 +/- 0.00748 [0.03479, 0.04905] |
| replay_clip_scale_mean | 0.50400 +/- 0.00488 [0.50114, 0.50963] | 0.49443 +/- 0.00560 [0.49034, 0.50081] | -0.00957 +/- 0.00108 [-0.01081, -0.00882] |
| replay_clipped_fraction | 1.00000 +/- 0.00000 [1.00000, 1.00000] | 1.00000 +/- 0.00000 [1.00000, 1.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| replay_coefficient_mean | 0.06200 +/- 0.00008 [0.06191, 0.06205] | 0.06200 +/- 0.00008 [0.06191, 0.06205] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| clipped_replay_coefficient_mean | 0.03127 +/- 0.00032 [0.03106, 0.03164] | 0.03068 +/- 0.00036 [0.03045, 0.03109] | -0.00060 +/- 0.00006 [-0.00067, -0.00055] |
| final_displacement | 118.34190 +/- 0.26984 [118.10478, 118.63552] | 118.32264 +/- 0.27595 [118.08918, 118.62718] | -0.01926 +/- 0.01314 [-0.03384, -0.00835] |
| eligible_retention | 0.56417 +/- 0.02545 [0.53692, 0.58732] | 0.62895 +/- 0.02326 [0.60769, 0.65379] | 0.06477 +/- 0.02431 [0.03803, 0.08552] |
| initially_unlearned_retention | 0.06873 +/- 0.02424 [0.04286, 0.09091] | 0.06878 +/- 0.03211 [0.04571, 0.10545] | 0.00005 +/- 0.01608 [-0.01724, 0.01455] |
| retention_foil_nll | 3.25170 +/- 0.02919 [3.21909, 3.27540] | 3.18042 +/- 0.08484 [3.09063, 3.25924] | -0.07128 +/- 0.08567 [-0.16998, -0.01616] |
| wall_seconds | 582.35647 +/- 23.15602 [555.77986, 598.18719] | 583.43877 +/- 25.38799 [554.70397, 602.83443] | 1.08231 +/- 3.11011 [-1.07588, 4.64725] |

## Exact per-pair budgets and allocation

Each continuation has 1500 updates, 80 old replays, 200 new-fact exposures, and 1,440,000 filler input tokens.
Paired lengths match at every update; padded row counts and replay loss coefficients therefore match too.
Template order: capital, birthplace, river/lake, currency, founder. Histograms include all 200 old facts.

### Seed 12

Pre-replay drift: `{"50": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 1.7642974853515625e-05, "nll": 2.7149915693414073e-07}, "100": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 1.5676021575927734e-05, "nll": 1.4486908912481056e-06}}`

uniform: `{"distinct_replayed": 80, "fact_tokens": 4353, "length_counts": {"12": 4, "13": 9, "14": 12, "15": 16, "16": 15, "17": 13, "18": 6, "19": 1, "20": 4}, "replay_count_histogram": {"0": 120, "1": 80}, "replay_tokens": 1241, "template_counts": [21, 12, 18, 14, 15], "uniform_overlap": [20, 20, 20, 20], "zero_score_slots": [0, 0, 0, 0]}`

prioritized: `{"distinct_replayed": 80, "fact_tokens": 4353, "length_counts": {"12": 4, "13": 9, "14": 12, "15": 16, "16": 15, "17": 13, "18": 6, "19": 1, "20": 4}, "replay_count_histogram": {"0": 120, "1": 80}, "replay_tokens": 1241, "template_counts": [19, 15, 16, 14, 16], "uniform_overlap": [2, 3, 3, 4], "zero_score_slots": [0, 0, 0, 0]}`

### Seed 13

Pre-replay drift: `{"50": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 8.821487426757812e-06, "nll": 1.22435390947917e-06}, "100": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 8.404254913330078e-06, "nll": -4.225224257137228e-07}}`

uniform: `{"distinct_replayed": 80, "fact_tokens": 4359, "length_counts": {"11": 1, "12": 3, "13": 6, "14": 9, "15": 19, "16": 16, "17": 20, "18": 2, "19": 1, "20": 3}, "replay_count_histogram": {"0": 120, "1": 80}, "replay_tokens": 1247, "template_counts": [14, 17, 20, 18, 11], "uniform_overlap": [20, 20, 20, 20], "zero_score_slots": [0, 0, 0, 0]}`

prioritized: `{"distinct_replayed": 80, "fact_tokens": 4359, "length_counts": {"11": 1, "12": 3, "13": 6, "14": 9, "15": 19, "16": 16, "17": 20, "18": 2, "19": 1, "20": 3}, "replay_count_histogram": {"0": 120, "1": 80}, "replay_tokens": 1247, "template_counts": [15, 17, 17, 19, 12], "uniform_overlap": [4, 8, 3, 5], "zero_score_slots": [0, 0, 0, 0]}`

### Seed 14

Pre-replay drift: `{"50": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 1.1920928955078125e-05, "nll": -3.434903919075083e-07}, "100": {"accuracy": 0.0, "correctness_disagreements": 0, "max_per_fact_nll": 1.0251998901367188e-05, "nll": 9.419396518328682e-08}}`

uniform: `{"distinct_replayed": 80, "fact_tokens": 4394, "length_counts": {"12": 2, "13": 16, "14": 14, "15": 12, "16": 12, "17": 14, "18": 7, "19": 2, "20": 1}, "replay_count_histogram": {"0": 120, "1": 80}, "replay_tokens": 1222, "template_counts": [14, 18, 17, 15, 16], "uniform_overlap": [20, 20, 20, 20], "zero_score_slots": [0, 0, 0, 0]}`

prioritized: `{"distinct_replayed": 80, "fact_tokens": 4394, "length_counts": {"12": 2, "13": 16, "14": 14, "15": 12, "16": 12, "17": 14, "18": 7, "19": 2, "20": 1}, "replay_count_histogram": {"0": 120, "1": 80}, "replay_tokens": 1222, "template_counts": [20, 19, 16, 14, 11], "uniform_overlap": [4, 5, 5, 4], "zero_score_slots": [0, 0, 0, 0]}`

## Audit limits

- No new model evaluation: NLL values verified by aggregation, not by recomputing logits.
- Old AND new generated-answer correctness and per-item NLL/foil aggregates verified; filler loss is logged only, not freshly evaluated.
- Saved fork and logged branch-state hashes verify common initialization; final branch weights were not saved.
- Read-only secondary guard summaries are post-run reporting, not new primary tests.
