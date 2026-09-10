# Resume SpacingLab — Study 12 running (2026-09-10)

## Current Study 12 launch record — supersedes historical status below

Mehmet understood the A/B selection contrast and explicitly authorized starting:
"aynen doğru başlayabiliriz". Exactly three pairs, seeds 9,10,11, compare uniform
replay with deterioration-prioritized replay, not another gap experiment.
Read docs/STUDY12_PREREGISTRATION.md completely and STUDY12_IMPLEMENTATION.md.
Branch: study12-deterioration-replay. Registration dd3e56c, implementation d19c63f,
immutable input/source manifest 59cf386, all committed before model evaluation.
All 60 tests passed before launch. Historical shared training source, frozen model,
tokenizer, dataset and software matched Study 11; no package updates.

Started `uv run --no-sync python -u -m spacinglab.study12 --run`, session 39563.
Launch verification observed parent PID 10400 and seed-9 child 10403, with prefix
progress at step 400/800 after 153 seconds. These are historical launch receipts,
not proof of future liveness. Check processes and results/study12/seed_*/console.log,
common_progress.json, common.json and each uniform/prioritized log.json.
The parent owns runner.lock and runs the finite three-pair chain serially, then
analyzes and exits. Never launch duplicates or restart partial pairs automatically.

Each seed has one common 800-step acquisition prefix and identical model AND
optimizer-state forks for two 1500-step continuations. Each arm receives 80 old-fact
replays in four rounds, with matched per-step input lengths and the same selection
probes. Only commonly learned facts are eligible; fewer than 20 causes explicit
calibration failure and a halt. All 200 old facts remain in the primary evaluation.
Selection uses deterioration since the common reference, not current difficulty.
Full checkpoint fork.pt is retained locally and ignored by Git. Frozen experiment
source, tests, dependencies, registration and manifests must not change mid-run.

The existing spacinglab-sonu-ve-infografik heartbeat is retargeted to Study 12,
ACTIVE every 20 minutes, quiet except completion/failure/required decisions.
Its historical name does not authorize another image. At completion independently
audit all paired raw metrics, common states, selection reconstruction, actual token
budgets, provenance and registered guards. Primary is all-fact mean accuracy at
interference steps 200,400,800,1200,1500. Report all three paired differences with
mean and sample SD; the screening rule is not significance or equivalence evidence.
Document negatives and secondary measures without replacing the primary endpoint.
Write English evidence under results/study12 and a very short Turkish RAPOR_TR.md;
update this record, commit locally and pause the heartbeat. No remote or push.

On failure preserve partial files, pause the heartbeat, explain once and ask before
repair or restart. Laptop sleep alone is not failure. No extra seeds, studies,
subagents, infographic or ForgetLab access. User requires simple Turkish and must
understand and explicitly authorize ANY new experiment. Do not quiz or pressure him.

## Historical Study 11 completion record

## Current completion status — read before the historical launch record

All six runs (seeds 6,7,8) finished normally. Session 62040 exited 0 with six
COMPLETE markers and STUDY11_DONE. No training process remains. No extra training,
new study, model evaluation or subagent was started. Completion heartbeat
spacinglab-sonu-ve-infografik has been PAUSED to prevent duplicate follow-ups.

Independent results/study11/audit_results.py checks frozen inputs/source/software,
Git chronology, every full schedule and step guard, actual token budgets, all raw
per-fact aggregates, 66 summary blocks and report table values. PASS; 46 tests pass.
See results/study11/AUDIT.md and WRITEUP.md; current student-level report RAPOR_TR.md.
Audit code is post-run verification, not a new preregistered experiment.

Primary variable-minus-fixed differences: -4.64286, -1.00000, -0.14286 percentage
points. Mean -1.92857, sample SD 2.38939; the mean magnitude is below SD. Therefore
the registered outcome is mixed_or_inconclusive, NOT a robust negative signal or
equivalence. Fixed accuracy .29190 +/- .02489; variable .27262 +/- .01358.
Window-end acquisition favors variable by .04833 +/- .03403, but later primary
does not: no equal-learning forgetting-rate claim. NLL delta +.00941 +/- .08282
is mixed; Study 10's favorable NLL direction did not recur consistently. Foil
separation delta +.05443 +/- .03272 is secondary, not a replacement primary.
New-fact accuracy delta -.02667 +/- .03055; no demonstrated absence of tradeoffs.

Keep Studies 9 and 10 separate, both previously mixed; no pooled significance
claim, extra seeds or outcome-selected change of endpoint. This third block was
selected after the first two; acknowledge that selection. The agreed positive
continuation screen failed. Recommend parking the gap question and explaining
selective replay only if the user wants to consider it, never automatically.

User boundary remains: short plain Turkish, ensure the proposed experiment is
understood and get explicit approval BEFORE any new training. The research idea
and results are not a test of the user's worth or competence. No quizzes or pressure
are needed in the completion notification. Keep the local branch as-is, no push,
merge, cleanup, personal data access, or ForgetLab changes.

## Historical launch record (superseded by the completion status above)

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
