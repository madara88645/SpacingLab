# Resume SpacingLab — Study 11 finite chain launched (2026-09-10)

## Current authorization and boundary

Mehmet explicitly said "tamam artık başlatabilirsin" after approving THREE fresh
fixed-versus-variable comparisons, six training runs, not the rejected 12-pair plan.
Read docs/STUDY11_PREREGISTRATION.md and its incorporated Study 9 protocol first.
Seeds 6,7,8 only; output results/study11; branch study11-small-retest. Order:
spaced6, variable_gaps6, variable_gaps7, spaced7, spaced8, variable_gaps8.

The user requires very short student-level Turkish explanations, time to understand
the experiment, and explicit approval before any NEW study. Do not turn completion
into automatic extra gap runs, selective replay, subagents or infographic production.
Luna's read-only idea scout is completed, reviewed and closed. Selective replay is
only a possible next proposal and must separate never-learned from deteriorating facts.

## Launch evidence and resume procedure

Registration committed 1aac057, runner/tests 8c8eb15, immutable manifest 90eda1f,
all BEFORE Study 11 model evaluation. Baseline 39 tests; extended suite 46 passed.
All source files from Study 10's manifest, model/tokenizer file hashes, filler hash,
package versions and Python version matched that historical record. Shared training
and schedule code is unchanged. Study 11 has its own manifest; never rewrite old ones.

Started `uv run --no-sync python -u -m spacinglab.study11 --run` from this repository
in execution session 62040. This id is a launch receipt, not proof it is still live.
Launch check observed parent PID 5388, child PID 5389 and advancing first-run output
through step 200. Recheck these rather than assuming the old PIDs remain valid.
Check process state and results/study11/*/console.log plus completed log.json files.
The parent owns runner.lock; never launch a duplicate chain. Completed runs are
validated and skipped on an authorized restart. Partial attempts are retained and
must NOT be overwritten or restarted without documenting the failure and asking.
Laptop sleep can suspend progress; a terminated partial run is not checkpoint-resumable.

The chain analyzes all six outcomes and exits. Only then apply the registered
three-seed screening rule. Positive direction is not significance or definitive
superiority, particularly after two mixed earlier screens. No outcome-based extra
runs or pooled decision with Studies 9/10. Preserve every outcome and guard, including
acquisition, new-fact learning, NLL and foil discrimination. No NLL-only memory claim.

Reused existing heartbeat spacinglab-sonu-ve-infografik with a Study 11-only prompt,
ACTIVE every 20 minutes, quiet on normal progress, completion/failure only. Its old
display name still mentions infographic; that task is completed and its current
prompt explicitly forbids generating another or starting new training. Pause it
after results delivery or a genuine failure requiring user action.

At completion audit the raw files, schedules, budgets and frozen provenance; update
English evidence and a concise Turkish report with all paired deltas and mean plus
seed spread; commit locally and stop. No push, remote compute or personal data.
Never touch ForgetLab. Report a failure once and pause monitoring, not automatic repair.

## Historical Study 10 snapshot (not current execution status)

The sections below preserve the 9 September handoff. Their statements about no
active training or a pending Luna agent describe that earlier date, not Study 11.

## Latest user-authorized continuation

The user asked to continue and explicitly requested ONE gpt-5.6-luna research
subagent. This overrides the historical Sonnet rule for that specific agent only.
Spawned read-only sidecar Ampere, id 01a0859e-7576-7422-8f06-2029f6ae09fa, model
gpt-5.6-luna, reasoning high, no inherited history. Its scope: three alternative
memory-inspired interventions with primary sources, matched controls and failure
criteria. No file edits, training, publication or descendants. Review its source
claims before adopting suggestions and close the agent when done.

Main agent separately inspected existing true-versus-foil NLL, without retraining.
Post-hoc analysis description committed afb7252; checked results committed 293360f.
See results/study10/NLL_SPECIFICITY.md. Incorrect same-template answers also show
lower mean NLL; separation delta -.01450 ± .15499 is not a consistent benefit.
This clarifies an already-reported guard, not independent new evidence. Do not
promote NLL-only improvement to factual memory improvement or conclude all gain
is format. No new training launched; next experiment choice awaits research review.

## Completion

Six Study 10 runs on seeds 3,4,5 completed normally; no training process remains.
Independent raw-log audit checked all 66 metric-by-arm summary blocks, every full
registered schedule/endpoints, paired content/budgets, finite values and frozen
data/model/source/software manifest against the pre-evaluation Git record.
39 tests passed again. Results plus WRITEUP.md/AUDIT.md committed in 7f3c12b.

Primary variable-minus-fixed delta +0.01143, sample SD 0.02767,
range -0.00929 to +0.04286 => mixed/inconclusive, not superiority or equivalence.
Primary fixed .28381 ± .01526, variable .29524 ± .04277.
Secondary checkpoint-mean NLL delta -.09338 ± .03197, all three negative.
Secondary terminal accuracy delta +.04500 ± .02000, all three positive.
Do not substitute those secondary endpoints for the preregistered primary.

Last-exposure acquisition delta +.01000 ± .07089; window delta +.04500 ± .05196.
No equal-learning forgetting-rate claim. New-fact accuracy delta -.02667 ± .07024;
no demonstrated absence of tradeoffs. Read full REPORT.md/WRITEUP.md.
Study 9 stays separate and inconclusive; no pooling and no extra runs started.

## Audit trail

Study 10 registration a4b3079, runner/tests ef1d996, manifest ea5ac56.
Prior Study 9 evidence add1634. Never regenerate historical manifests merely to
match later source changes. Training and scheduling code were not changed.
All original/raw results preserved. No push/publication or personal data accessed.
Never touch ForgetLab. Historical rule: subagents must be explicitly Sonnet.
The latest user-authorized one-agent Luna exception is documented above.

## Completed visual delivery

User-requested imagegen infographic generated, corrected and inspected. First draft
had four teal markers and was rejected. The corrected five-marker diagram, gap
labels, all result values and limitations were visually checked against source.
Final file: results/study10/infographic-tr.png, SHA-256
b9fa875dd37727e488e981c6d70e37810af2c54e36b42f41cd7725ff2d77b415.
Timeline geometry is schematic; numerical labels give exact step gaps.
Original generation and targeted edit prompts plus QA notes are preserved as
INFOGRAPHIC_PROMPT.md and INFOGRAPHIC_EDIT_PROMPT.md in results/study10.
Imagegen skill and both prompting references were used; no CLI/API fallback.
English write-up, README and short Turkish RAPOR_TR.md updated with verified results.

Heartbeat spacinglab-sonu-ve-infografik was PAUSED via the app after artifacts were
ready, to prevent duplicate notifications. No active training or new experiment.
A sensible proposed next step is prospective validation of secondary NLL/terminal
signals on new data, not more runs until a favorable primary label appears.
This is a proposal only; further training requires authorization and preregistration.
