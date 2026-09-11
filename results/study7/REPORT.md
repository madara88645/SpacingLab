# Study 7 results

All six fresh runs; mean ± sample SD [min, max] across three seeds.

Registered rule: **positive_directional_signal**; accuracy/NLL discordant: **False**.

These are total placement-policy effects, including recency and batch composition.
They do not establish equivalence, a universal shuffle rule, or a brain-like mechanism.

| Metric | Spaced | Random | Random minus spaced |
|---|---|---|---|
| retention_accuracy | 0.27310 ± 0.08331 [0.20429, 0.36571] | 0.36595 ± 0.05705 [0.31857, 0.42929] | 0.09286 ± 0.04586 [0.06357, 0.14571] |
| retention_nll | 1.27838 ± 0.10928 [1.15808, 1.37150] | 1.09644 ± 0.11760 [0.96694, 1.19655] | -0.18193 ± 0.06878 [-0.24565, -0.10901] |
| retention_discrimination | 1.81531 ± 0.17540 [1.63256, 1.98229] | 1.80295 ± 0.10561 [1.68375, 1.88484] | -0.01236 ± 0.19220 [-0.14732, 0.20770] |
| terminal_accuracy | 0.15000 ± 0.07000 [0.08000, 0.22000] | 0.23000 ± 0.05220 [0.17000, 0.26500] | 0.08000 ± 0.04093 [0.03500, 0.11500] |
| terminal_nll | 1.38666 ± 0.10563 [1.27116, 1.47833] | 1.13185 ± 0.11778 [1.01634, 1.25178] | -0.25482 ± 0.02826 [-0.28308, -0.22655] |
| at_last_accuracy | 0.80667 ± 0.08977 [0.70500, 0.87500] | 0.76667 ± 0.02843 [0.73500, 0.79000] | -0.04000 ± 0.09579 [-0.10500, 0.07000] |
| at_last_nll | 0.27314 ± 0.08617 [0.20845, 0.37096] | 0.30802 ± 0.02550 [0.28243, 0.33344] | 0.03487 ± 0.10692 [-0.08853, 0.09972] |
| window_accuracy | 0.66667 ± 0.11015 [0.54000, 0.74000] | 0.77833 ± 0.02021 [0.75500, 0.79000] | 0.11167 ± 0.12292 [0.01500, 0.25000] |
| window_nll | 0.46432 ± 0.15494 [0.34906, 0.64045] | 0.25310 ± 0.04808 [0.20960, 0.30474] | -0.21122 ± 0.17622 [-0.39548, -0.04433] |
| last_exposure_step | 485.63833 ± 6.89699 [478.22500, 491.86500] | 581.28333 ± 3.18652 [577.78500, 584.02000] | 95.64500 ± 9.05010 [85.92000, 103.82000] |
| terminal_new_facts_accuracy | 0.95333 ± 0.03055 [0.92000, 0.98000] | 0.94000 ± 0.04000 [0.90000, 0.98000] | -0.01333 ± 0.01155 [-0.02000, 0.00000] |
| terminal_new_facts_nll | 0.06412 ± 0.03358 [0.02551, 0.08641] | 0.06079 ± 0.02825 [0.02869, 0.08186] | -0.00333 ± 0.00599 [-0.00862, 0.00318] |
| terminal_filler_loss | 3.42883 ± 0.03022 [3.39562, 3.45473] | 3.42862 ± 0.02990 [3.39539, 3.45335] | -0.00021 ± 0.00117 [-0.00137, 0.00097] |
| parameter_displacement | 119.30047 ± 0.33355 [119.04987, 119.67906] | 119.44972 ± 0.39126 [119.20334, 119.90086] | 0.14925 ± 0.07474 [0.07249, 0.22180] |
| clip_fraction | 1.00000 ± 0.00000 [1.00000, 1.00000] | 1.00000 ± 0.00000 [1.00000, 1.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| mean_preclip_norm | 2.28901 ± 0.01733 [2.27027, 2.30447] | 2.29434 ± 0.01602 [2.28011, 2.31170] | 0.00533 ± 0.01680 [-0.01327, 0.01940] |
| target_coefficient_per_exposure | 0.05683 ± 0.00041 [0.05640, 0.05722] | 0.05761 ± 0.00014 [0.05751, 0.05777] | 0.00078 ± 0.00033 [0.00055, 0.00116] |
| clipped_target_coefficient_per_exposure | 0.02313 ± 0.00077 [0.02231, 0.02382] | 0.02279 ± 0.00043 [0.02231, 0.02315] | -0.00035 ± 0.00082 [-0.00096, 0.00059] |
| floor_checkpoints | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| ceiling_checkpoints | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |

## Primary score by seed

| Seed | Spaced | Random | Difference |
|---|---|---|---|
| 0 | 0.365714 | 0.429286 | +0.063571 |
| 1 | 0.249286 | 0.318571 | +0.069286 |
| 2 | 0.204286 | 0.350000 | +0.145714 |

Paired input/fact/budget checks passed. Pre-injection numerical differences:
```json
[
  {
    "seed": 0,
    "max_pre_injection_training_loss_difference": 4.76837158203125e-07,
    "pretrained_holdout_difference": 0.0
  },
  {
    "seed": 1,
    "max_pre_injection_training_loss_difference": 1.1682510375976562e-05,
    "pretrained_holdout_difference": 0.0
  },
  {
    "seed": 2,
    "max_pre_injection_training_loss_difference": 2.384185791015625e-07,
    "pretrained_holdout_difference": 0.0
  }
]
```

Continuous metrics and floor/ceiling flags must be read together. Clipped coefficients
are diagnostics, not per-fact gradient attribution. Acquisition differences prevent an
equal-learning forgetting interpretation. Do not pool these with older studies.
