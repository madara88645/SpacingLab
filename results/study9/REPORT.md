# Study 9 results

All six fresh runs; mean ± sample SD [min, max] across three seeds.

Registered rule: **mixed_or_inconclusive**; accuracy/NLL discordant: **False**.

These are total placement-policy effects, with first/last times and mean gap matched; middle exposures and batch composition still differ.
They do not establish equivalence, a universal shuffle rule, or a brain-like mechanism.

| Metric | Spaced | Variable gaps | Variable gaps minus spaced |
|---|---|---|---|
| first_exposure_step | 229.63833 ± 6.89699 [222.22500, 235.86500] | 229.63833 ± 6.89699 [222.22500, 235.86500] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| exposure_span | 256.00000 ± 0.00000 [256.00000, 256.00000] | 256.00000 ± 0.00000 [256.00000, 256.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| retention_accuracy | 0.28667 ± 0.03967 [0.25214, 0.33000] | 0.32905 ± 0.09714 [0.23214, 0.42643] | 0.04238 ± 0.05866 [-0.02000, 0.09643] |
| retention_nll | 1.27738 ± 0.05201 [1.22036, 1.32219] | 1.20209 ± 0.13448 [1.06249, 1.33079] | -0.07530 ± 0.08324 [-0.15787, 0.00859] |
| retention_discrimination | 1.75125 ± 0.16547 [1.64515, 1.94191] | 1.84618 ± 0.18474 [1.69637, 2.05260] | 0.09493 ± 0.05896 [0.02969, 0.14441] |
| terminal_accuracy | 0.16167 ± 0.05132 [0.10500, 0.20500] | 0.17667 ± 0.08893 [0.08000, 0.25500] | 0.01500 ± 0.05679 [-0.02500, 0.08000] |
| terminal_nll | 1.36667 ± 0.09965 [1.25600, 1.44929] | 1.41985 ± 0.21909 [1.22547, 1.65725] | 0.05318 ± 0.19749 [-0.16924, 0.20796] |
| at_last_accuracy | 0.80667 ± 0.06110 [0.74000, 0.86000] | 0.84833 ± 0.04252 [0.80500, 0.89000] | 0.04167 ± 0.02021 [0.03000, 0.06500] |
| at_last_nll | 0.27394 ± 0.05935 [0.22167, 0.33845] | 0.23944 ± 0.05391 [0.20701, 0.30167] | -0.03449 ± 0.02142 [-0.05468, -0.01203] |
| window_accuracy | 0.66833 ± 0.07687 [0.58000, 0.72000] | 0.69167 ± 0.09088 [0.59000, 0.76500] | 0.02333 ± 0.01893 [0.01000, 0.04500] |
| window_nll | 0.44646 ± 0.11435 [0.37976, 0.57850] | 0.37802 ± 0.08278 [0.30466, 0.46777] | -0.06844 ± 0.04682 [-0.11073, -0.01812] |
| last_exposure_step | 485.63833 ± 6.89699 [478.22500, 491.86500] | 485.63833 ± 6.89699 [478.22500, 491.86500] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| terminal_new_facts_accuracy | 0.96667 ± 0.04163 [0.92000, 1.00000] | 0.92667 ± 0.03055 [0.90000, 0.96000] | -0.04000 ± 0.05292 [-0.10000, 0.00000] |
| terminal_new_facts_nll | 0.06848 ± 0.02766 [0.03772, 0.09133] | 0.07286 ± 0.02112 [0.05964, 0.09721] | 0.00438 ± 0.02944 [-0.02961, 0.02192] |
| terminal_filler_loss | 3.42833 ± 0.03093 [3.39407, 3.45421] | 3.42764 ± 0.03127 [3.39285, 3.45340] | -0.00069 ± 0.00060 [-0.00121, -0.00004] |
| parameter_displacement | 119.34054 ± 0.35508 [119.03605, 119.73058] | 119.23220 ± 0.40211 [118.87351, 119.66689] | -0.10834 ± 0.05011 [-0.16254, -0.06369] |
| clip_fraction | 1.00000 ± 0.00000 [1.00000, 1.00000] | 1.00000 ± 0.00000 [1.00000, 1.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| mean_preclip_norm | 2.28114 ± 0.01510 [2.26538, 2.29549] | 2.30016 ± 0.01893 [2.28524, 2.32145] | 0.01902 ± 0.03216 [-0.00171, 0.05607] |
| target_coefficient_per_exposure | 0.05683 ± 0.00041 [0.05640, 0.05722] | 0.05703 ± 0.00035 [0.05664, 0.05732] | 0.00020 ± 0.00009 [0.00010, 0.00027] |
| clipped_target_coefficient_per_exposure | 0.02325 ± 0.00066 [0.02259, 0.02392] | 0.02334 ± 0.00059 [0.02270, 0.02385] | 0.00009 ± 0.00016 [-0.00007, 0.00024] |
| floor_checkpoints | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| ceiling_checkpoints | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |

Prediction status: **no_consistent_positive_signal_as_predicted**.
This compares constant gaps to a shuffled short/long gap multiset at the same endpoints.
Gap magnitudes and ordering both change; this does not isolate randomness alone.
Small or mixed results do not establish equivalence; personalization/PEFT remain untested.

## Primary score by seed

| Seed | Spaced | Variable gaps | Difference |
|---|---|---|---|
| 0 | 0.330000 | 0.426429 | +0.096429 |
| 1 | 0.277857 | 0.328571 | +0.050714 |
| 2 | 0.252143 | 0.232143 | -0.020000 |

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
    "max_pre_injection_training_loss_difference": 2.86102294921875e-06,
    "pretrained_holdout_difference": 0.0
  },
  {
    "seed": 2,
    "max_pre_injection_training_loss_difference": 4.76837158203125e-07,
    "pretrained_holdout_difference": 0.0
  }
]
```

Continuous metrics and floor/ceiling flags must be read together. Clipped coefficients
are diagnostics, not per-fact gradient attribution. Acquisition differences prevent an
equal-learning forgetting interpretation. Do not pool these with older studies.
