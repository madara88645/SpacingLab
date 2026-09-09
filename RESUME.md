# Resume SpacingLab — Study 10 and infographic completed (2026-09-09)

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
