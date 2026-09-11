# Study 12 results

Registered screen: **positive_directional_signal**.
Mean +/- sample SD [min,max], three paired seeds. No historical pooling.
All 200 old facts evaluated; shared acquisition and matched replay budgets.

| Metric | Uniform | Prioritized | Prioritized minus uniform |
|---|---|---|---|
| retention_accuracy | 0.43633 +/- 0.03585 [0.39500, 0.45900] | 0.46867 +/- 0.04607 [0.41900, 0.51000] | 0.03233 +/- 0.01620 [0.02200, 0.05100] |
| retention_nll | 0.92024 +/- 0.09456 [0.84115, 1.02497] | 0.85492 +/- 0.07954 [0.79037, 0.94377] | -0.06533 +/- 0.04882 [-0.10424, -0.01054] |
| retention_discrimination | 2.27341 +/- 0.16014 [2.09384, 2.40142] | 2.27462 +/- 0.15163 [2.10315, 2.39102] | 0.00121 +/- 0.06925 [-0.07174, 0.06605] |
| terminal_accuracy | 0.43000 +/- 0.03969 [0.38500, 0.46000] | 0.47000 +/- 0.03279 [0.44000, 0.50500] | 0.04000 +/- 0.03041 [0.00500, 0.06000] |
| terminal_nll | 0.89193 +/- 0.11845 [0.82231, 1.02869] | 0.80008 +/- 0.10986 [0.70397, 0.91984] | -0.09185 +/- 0.04026 [-0.12082, -0.04587] |
| new_fact_accuracy | 0.98000 +/- 0.02000 [0.96000, 1.00000] | 0.98667 +/- 0.02309 [0.96000, 1.00000] | 0.00667 +/- 0.03055 [-0.02000, 0.04000] |
| new_fact_nll | 0.03935 +/- 0.02405 [0.01559, 0.06368] | 0.04804 +/- 0.05001 [0.01776, 0.10577] | 0.00869 +/- 0.05533 [-0.04309, 0.06699] |
| filler_loss | 3.44970 +/- 0.02138 [3.42513, 3.46406] | 3.44987 +/- 0.02088 [3.42578, 3.46276] | 0.00017 +/- 0.00130 [-0.00130, 0.00116] |
| floor_checkpoints | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |
| ceiling_checkpoints | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] | 0.00000 +/- 0.00000 [0.00000, 0.00000] |

## Primary paired results

| Seed | Uniform | Prioritized | Difference |
|---|---|---|---|
| 9 | 0.395000 | 0.419000 | +0.024000 |
| 10 | 0.455000 | 0.477000 | +0.022000 |
| 11 | 0.459000 | 0.510000 | +0.051000 |

NLL/foil, acquisition, replay allocation, clipping and new-learning guards require completion audit.
No no-replay arm, unseen-fact generalization, representation-erasure or PEFT claim.
