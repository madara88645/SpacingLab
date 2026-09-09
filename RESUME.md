# Resume SpacingLab — Study 10 active (2026-09-09)

## Completed evidence

Study 9 six logs, registered schedules, paired budgets and model/data/source/software
manifest independently checked, and all results committed in add1634 before adding
new source. Primary variable-minus-spaced mean +0.04238, sample SD 0.05866, seed range
-0.02000 to +0.09643: mixed/inconclusive. NLL delta -0.07530, SD 0.08324.
At-last acquisition delta +0.04167, SD 0.02021: not equal-learning forgetting.
See results/study9/REPORT.md. Study 8 remains inconclusive, not superseded or pooled.

## New authorized fixed-size replication

User explicitly authorized continuation this morning after discussing three new
pairs. Study 10 is exactly six fresh runs on seeds 3,4,5; same model/training/data/
gap policies as Study 9, new seeds only. First/last exposures match for each fact,
five exposures, span 256. Fixed [64,64,64,64] vs per-fact permutation [32,32,64,128].
New-three-seed analysis stands alone; no hidden pooling or optional extra runs.

Registration: docs/STUDY10_PREREGISTRATION.md, commit a4b3079.
Implementation/tests: ef1d996. Pre-evaluation manifest: ea5ac56.
39 software tests passed; two successive preflights passed before evaluation.
No training/scheduling source modified; isolated runner preserves prior protocols.

## Live finite chain

Command: uv run --frozen python -u -m spacinglab.study10 --run
Exec session 99315. Initial uv PID 5531, parent 5544, worker 5545 (verify live).
Order: variable_gaps3, spaced3, spaced4, variable_gaps4, variable_gaps5, spaced5.
First worker reached pretrained evaluation and optimizer step 0. No outcome yet.
Serial local MPS; estimated total 1.5–2 hours. Do not launch duplicate processes.

Inspect results/study10/<condition>_s<seed>/console.log and progress.json.
A validated log.json marks a complete run. After six, the runner automatically
writes summary.json/REPORT.md and prints STUDY10_DONE, then exits.
On completion independently check full schedules, pinned provenance, budgets and
all calculations, acquisition/NLL/new-task/floor/ceiling/clipping guards. Update
reports and commit evidence locally. Do not read partial seeds as a full result.

## Requested follow-up and infographic

Mehmet explicitly asked to use the imagegen skill AFTER results to deliver one
Turkish visual diagram/infographic alongside a simple explanation.
A thread heartbeat was created: spacinglab-sonu-ve-infografik, every 20 minutes.
Stay quiet while progress is normal. On completion verify results, finish reports,
read imagegen skill and required prompting references, use built-in image generation,
inspect exact labels/numbers, save final image plus prompt to this repo and display
inline. Show schedules and all three paired results, sample variability and caveats.
Do not imply that SD is CI, that facts are independent model runs, or that improved
acquisition proves reduced forgetting. No personal data or LoRA claims.
Pause the heartbeat after delivery or after reporting a blocker once.
Never report an image as delivered before the tool succeeds and it is inspected.

## Safety / reproducibility

Do not change source, uv.lock, model/data or registrations during the active chain.
Status docs are safe to update. Old manifests must not be regenerated to match new
source additions; reproduce historical studies using historical commits.
Use uv; no remote compute, push/publication, or personal messages. Never touch
ForgetLab. All subagents must be Sonnet; none spawned.

On stop: resolve live chain and worker PIDs and terminate only those. Preserve partial
attempts. Completed validated runs can be skipped; nonempty incomplete runs are
refused. Document repair/restart before retry. No silent overwrites or further
experiments. If failure/stall, report and ask before restart.

Read docs/PROVENANCE_AUDIT_2026-09-08.md for the historical mutable-data error.
Study 6b's unmatched-data recommendation remains withdrawn. Study 8 did not prove
recency explains all of Study 7. No representation-erasure or biological claims.
Give short finding-first student-level Turkish reports, including negative findings.
