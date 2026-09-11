# Study 8 results

All six fresh runs; mean ± sample SD [min, max] across three seeds.

Registered rule: **mixed_or_inconclusive**; accuracy/NLL discordant: **False**.

These are total placement-policy effects, with last-exposure times matched; earlier history and batch composition still differ.
They do not establish equivalence, a universal shuffle rule, or a brain-like mechanism.

| Metric | Spaced | Random matched | Random matched minus spaced |
|---|---|---|---|
| first_exposure_step | 229.63833 ± 6.89699 [222.22500, 235.86500] | 97.80000 ± 5.78934 [91.20000, 102.02000] | -131.83833 ± 3.51137 [-135.68500, -128.80500] |
| exposure_span | 256.00000 ± 0.00000 [256.00000, 256.00000] | 387.83833 ± 3.51137 [384.80500, 391.68500] | 131.83833 ± 3.51137 [128.80500, 135.68500] |
| retention_accuracy | 0.28071 ± 0.08340 [0.19429, 0.36071] | 0.29667 ± 0.04185 [0.24929, 0.32857] | 0.01595 ± 0.04427 [-0.03214, 0.05500] |
| retention_nll | 1.28467 ± 0.12591 [1.17532, 1.42233] | 1.23084 ± 0.05427 [1.17010, 1.27455] | -0.05382 ± 0.08139 [-0.14778, -0.00522] |
| retention_discrimination | 1.78341 ± 0.21680 [1.54099, 1.95873] | 1.68740 ± 0.07386 [1.60282, 1.73913] | -0.09601 ± 0.14380 [-0.21960, 0.06183] |
| terminal_accuracy | 0.16333 ± 0.07638 [0.08000, 0.23000] | 0.16833 ± 0.04041 [0.12500, 0.20500] | 0.00500 ± 0.03606 [-0.02500, 0.04500] |
| terminal_nll | 1.42089 ± 0.18417 [1.30575, 1.63330] | 1.29503 ± 0.06620 [1.24762, 1.37067] | -0.12586 ± 0.22908 [-0.38568, 0.04705] |
| at_last_accuracy | 0.80667 ± 0.06807 [0.73000, 0.86000] | 0.69833 ± 0.04752 [0.65000, 0.74500] | -0.10833 ± 0.09224 [-0.21000, -0.03000] |
| at_last_nll | 0.27519 ± 0.06854 [0.22268, 0.35272] | 0.37035 ± 0.05081 [0.33076, 0.42765] | 0.09516 ± 0.10330 [-0.00008, 0.20497] |
| window_accuracy | 0.65333 ± 0.08963 [0.55000, 0.71000] | 0.66000 ± 0.03606 [0.62000, 0.69000] | 0.00667 ± 0.11930 [-0.09000, 0.14000] |
| window_nll | 0.48869 ± 0.11287 [0.41603, 0.61872] | 0.41067 ± 0.03463 [0.37520, 0.44440] | -0.07802 ± 0.14357 [-0.24353, 0.01307] |
| last_exposure_step | 485.63833 ± 6.89699 [478.22500, 491.86500] | 485.63833 ± 6.89699 [478.22500, 491.86500] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| terminal_new_facts_accuracy | 0.92000 ± 0.04000 [0.88000, 0.96000] | 0.96000 ± 0.02000 [0.94000, 0.98000] | 0.04000 ± 0.03464 [0.02000, 0.08000] |
| terminal_new_facts_nll | 0.07617 ± 0.03708 [0.03336, 0.09802] | 0.06711 ± 0.00530 [0.06129, 0.07166] | -0.00906 ± 0.03848 [-0.03585, 0.03504] |
| terminal_filler_loss | 3.42909 ± 0.03135 [3.39424, 3.45499] | 3.42868 ± 0.03191 [3.39342, 3.45558] | -0.00041 ± 0.00087 [-0.00100, 0.00059] |
| parameter_displacement | 119.28562 ± 0.35697 [118.99439, 119.68385] | 119.68026 ± 0.31656 [119.40419, 120.02577] | 0.39463 ± 0.04700 [0.34192, 0.43219] |
| clip_fraction | 1.00000 ± 0.00000 [1.00000, 1.00000] | 1.00000 ± 0.00000 [1.00000, 1.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| mean_preclip_norm | 2.28375 ± 0.01295 [2.26980, 2.29540] | 2.28498 ± 0.01467 [2.26908, 2.29798] | 0.00123 ± 0.00173 [-0.00072, 0.00258] |
| target_coefficient_per_exposure | 0.05683 ± 0.00041 [0.05640, 0.05722] | 0.05713 ± 0.00021 [0.05697, 0.05737] | 0.00030 ± 0.00030 [0.00010, 0.00064] |
| clipped_target_coefficient_per_exposure | 0.02309 ± 0.00070 [0.02241, 0.02380] | 0.02208 ± 0.00045 [0.02165, 0.02255] | -0.00101 ± 0.00025 [-0.00126, -0.00077] |
| floor_checkpoints | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |
| ceiling_checkpoints | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] | 0.00000 ± 0.00000 [0.00000, 0.00000] |

Prediction status: **consistent_but_not_proof_of_recency**.
If the advantage persists, last-exposure recency alone cannot explain this comparison.
If it disappears, this does not prove that recency caused the whole Study 7 effect:
the earlier exposure history also changed. No equivalence conclusion follows.

## Primary score by seed

| Seed | Spaced | Random matched | Difference |
|---|---|---|---|
| 0 | 0.360714 | 0.328571 | -0.032143 |
| 1 | 0.287143 | 0.312143 | +0.025000 |
| 2 | 0.194286 | 0.249286 | +0.055000 |

Paired input/fact/budget checks passed. Pre-injection numerical differences:
```json
[
  {
    "seed": 0,
    "max_pre_injection_training_loss_difference": 7.152557373046875e-07,
    "pretrained_holdout_difference": 0.0
  },
  {
    "seed": 1,
    "max_pre_injection_training_loss_difference": 5.4836273193359375e-06,
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
