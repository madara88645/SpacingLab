# Resume SpacingLab — Study 9 active (2026-09-08)

## Current state

Study 8 is complete. Six raw runs and paired analysis committed in cbae065.
With every fact's final exposure matched, random-minus-spaced primary accuracy was
+0.01595 (sample SD 0.04427; seed range -0.03214 to +0.05500). Registered outcome:
mixed_or_inconclusive. NLL difference -0.05382 (SD 0.08139). No equivalence or
superiority claim; acquisition and earlier exposure histories still differed.
See results/study8/REPORT.md. Study 7 results remain separate (commit 4f84b3a).

User approved Study 9: fixed [64,64,64,64] versus independently permuted
[32,32,64,128]. Both first and final exposure times, five exposures and total
256-step span match exactly for every fact. This is not a personalization study.

Registration committed before outcomes: 9522b38, docs/STUDY9_PREREGISTRATION.md.
Implementation/tests: 8ac84d7. Frozen pre-evaluation manifest: 574ee26.
33 software tests and two preflights passed before launch. No subagents used.

## Active finite chain

Command: uv run --frozen python -u -m spacinglab.study9 --run
Exec session: 45803 (verify live; do not launch a duplicate).
Order: spaced0, variable_gaps0, variable_gaps1, spaced1, spaced2, variable_gaps2.
First worker reached optimizer step 400/2300; no completed Study 9 outcome yet.
Serial local MPS, estimated entire chain 1.5–2 hours; laptop must stay awake.
No recurring monitor/notification automation is configured.

Inspect results/study9/<condition>_s<seed>/console.log and progress.json.
Only a validated log.json means a completed run. After six valid runs, the chain
writes summary.json and REPORT.md and prints STUDY9_DONE.

On completion: independently verify six logs, exact full schedules/endpoints,
data/model/budgets, acquisition/NLL/new-learning guards and summary calculations.
Apply the preregistered directional heuristic (not a significance test); report
means with sample SD and ranges. Update English/Turkish reports and commit locally.
Do not launch extra studies without user authorization.

On a stop request: resolve live chain and child PIDs and stop only those processes.
Preserve partial attempts. Runner skips validated completed runs but rejects
incomplete nonempty attempts; document restart before retry. Do not silently overwrite.

## Reproducibility and scope

Do not edit spacinglab source, uv.lock, registration, model or cached data during
this chain. Manifests reject drift. Status docs can be updated.
Shared source changed for Study 9: reproduce prior studies with historical source;
never regenerate historical manifests to make current source appear matched.

Read docs/PROVENANCE_AUDIT_2026-09-08.md for the old mutable-cache failure.
Study 6b's unmatched-data recommendation remains withdrawn. Study 8 did not prove
that recency explains all of Study 7. Study 3 did not establish representation
erasure or a unique 90%-format decomposition. Keep all negatives and limitations.

No personal messages accessed. User asked whether style examples mixed with other
personal data could improve personalization/retention; discussed conceptually only.
No personal-data training or inference is authorized by this Study 9 launch.

Never touch ForgetLab. Use uv. No remote/push/publication without approval.
All subagents must explicitly use Sonnet; none used. Explain results in short,
student-level Turkish. Software checks: uv run --frozen pytest -q.
