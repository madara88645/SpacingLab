# Resume SpacingLab — Study 10 and infographic completed (2026-09-09)

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
Never touch ForgetLab. Any subagent must be explicitly Sonnet; none spawned.

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
