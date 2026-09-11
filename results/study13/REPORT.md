# Study 13 results

Registered screen: **positive_directional_signal**.
Mean +/- sample SD [min,max], three paired seeds. No historical pooling.
All 200 old facts evaluated; shared acquisition, matched token budgets and 80 distinct facts replayed once per arm.

| Metric | Uniform | Prioritized | Prioritized minus uniform |
|---|---|---|---|
| retention_accuracy | 0.41300 +/- 0.04244 [0.36400, 0.43800] | 0.45800 +/- 0.04603 [0.41100, 0.50300] | 0.04500 +/- 0.02207 [0.02200, 0.06600] |
| retention_nll | 0.98912 +/- 0.14690 [0.90325, 1.15875] | 0.90225 +/- 0.14043 [0.78930, 1.05948] | -0.08687 +/- 0.03497 [-0.11395, -0.04739] |
| retention_discrimination | 2.26258 +/- 0.12824 [2.11665, 2.35736] | 2.27816 +/- 0.06977 [2.19976, 2.33340] | 0.01558 +/- 0.06966 [-0.05603, 0.08310] |
| terminal_accuracy | 0.42167 +/- 0.03055 [0.39500, 0.45500] | 0.45833 +/- 0.01893 [0.44500, 0.48000] | 0.03667 +/- 0.04537 [-0.00500, 0.08500] |
| terminal_nll | 0.96252 +/- 0.07568 [0.89918, 1.04633] | 0.82588 +/- 0.03962 [0.79676, 0.87100] | -0.13665 +/- 0.03666 [-0.17533, -0.10241] |
| new_fact_accuracy | 0.97333 +/- 0.03055 [0.94000, 1.00000] | 0.97333 +/- 0.02309 [0.96000, 1.00000] | 0.00000 +/- 0.02000 [-0.02000, 0.02000] |
| new_fact_nll | 0.04443 +/- 0.01298 [0.02983, 0.05468] | 0.03621 +/- 0.01784 [0.01809, 0.05374] | -0.00821 +/- 0.00630 [-0.01196, -0.00094] |
| filler_loss | 3.43347 +/- 0.01348 [3.41806, 3.44310] | 3.43381 +/- 0.01285 [3.41919, 3.44330] | 0.00034 +/- 0.00073 [-0.00031, 0.00113] |
| floor_checkpoints | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| ceiling_checkpoints | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |

## Primary paired results

| Seed | Uniform | Prioritized | Difference |
|---|---|---|---|
| 12 | 0.437000 | 0.503000 | +0.066000 |
| 13 | 0.438000 | 0.460000 | +0.022000 |
| 14 | 0.364000 | 0.411000 | +0.047000 |

NLL/foil, acquisition, replay allocation, clipping and new-learning guards require completion audit.
No no-replay arm, unseen-fact generalization, representation-erasure or PEFT claim.
