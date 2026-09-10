# Execution and completion receipt

10 September 2026, local Study 13 only.

- Execution session 38078 returned exit code 0. Retained terminal output included
  COMPLETE_PAIR seed=12, COMPLETE_PAIR seed=13, COMPLETE_PAIR seed=14 and STUDY13_DONE.
- Child console logs each contain both expected COMPLETE arm markers in registered
  order. Process checks found the parent/child gone and no Study 13 training process.
- Independent audit command: `uv run --no-sync python results/study13/audit_results.py`.
  Exit 0, PASS; rerun after strengthening generated-answer length validation, PASS.
- Verification command: `uv run --no-sync pytest -q`.
  Exit 0: 80 passed in 2.95s. No pretrained-model training or inference in this audit.
- Frozen training source, tests, registration, manifest and dependencies unchanged.
  No new study, repeated attempt, extra seed, agent, image, remote or push.
- Three fork.pt files retained locally and excluded from Git. Runner locks and
  historical outputs untouched. Generated progress and completed raw logs preserved.
- English WRITEUP.md/AUDIT.md and Turkish RAPOR_TR.md prepared; completion heartbeat
  spacinglab-sonu-ve-infografik paused through the app. Next experiment is a proposal
  only and needs user understanding, explicit approval and prospective registration.

This receipt records observed tool outcomes; it is not an independently timestamped
external certificate. Raw log and immutable-source checks are reproducible via the audit.
