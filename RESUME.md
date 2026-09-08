# Resume SpacingLab — 2026-09-08

Read `docs/DURUM_2026-09-08_TR.md` and `docs/PROVENANCE_AUDIT_2026-09-08.md` first.
The linked ChatGPT conversation `6a9e6d1b-ab3c-83eb-9471-d0759ddfee81` was read; its
external review is already stored under `docs/`.

## Completed in the Codex continuation

- Registered CPU provenance audit before measuring (`a687a64`), then committed its
  analysis code before execution (`52bf07a`). JSON results are under `results/`.
- Reproduced changed training and held-out streams when the token cache grows.
  Historical Study 1 spaced vs Study 6 random logs differ before injection.
- Withdrew the isolated "ordinary shuffling suffices" interpretation. The historical
  numbers stay intact. No estimate of the data confound's causal size was made.
- Added opt-in immutable snapshot validation, stream/provenance logging, and rejection
  of attempts to overwrite a completed log. Old scripts warn but remain unpinned.
- Corrected erasure/savings/format-decomposition and loss-weight equivalence claims.
  Archived the old Turkish report; current root report reflects these corrections.
- No new model training, subagents, remote creation or publication in this continuation.

## Study 7 — registered and running, 2026-09-08

The user authorized continuation. Registration: `docs/STUDY7_PREREGISTRATION.md`,
initial commit `e5c93b0`. Instrumentation is implemented and 25 tests pass. A preflight
tuple/list serialization bug stopped the first launch before model loading; Amendment
7.1 records its regression fix. Initial and corrected manifests are both retained.

The corrected chain started successfully, observed GPT-2 pretrained evaluation and
optimizer step 0. At this handoff it is still running, not a completed result.
Exec session 70798; initial parent/worker PIDs 6934/6935 (verify live before using).
Command: `uv run --frozen python -u -m spacinglab.study7 --run`.
It runs spaced0, random0, random1, spaced1, spaced2, random2 serially, then creates
`results/study7/summary.json` and `results/study7/REPORT.md` automatically.

Read each run's `console.log` and `progress.json` for progress. Only `log.json` means
a completed run; only `STUDY7_DONE` plus six validated logs means chain success.
Do not start a duplicate. Runner lock prevents two ordinary chain launches. Check
processes before stopping or resuming. If interrupted, preserve the incomplete attempt
and amend before restarting it; completed runs can be skipped after manifest checks.

Next action: wait for the existing chain, inspect every paired guard and the auto-
generated report, update the Turkish conclusion, and commit all results. Do not
claim an outcome from the first seed, or reuse old controls. No automatic notification
or recurring monitor has been created; the finite chain itself performs the runs and
analysis. No extra experiments are authorized by its implementation.

### Design context

Fresh random vs spaced pairs, seeds 0–2, both conditions trained under one frozen
data/model/software snapshot. Do not reuse old spaced controls. The design was registered
before new model measurements. It includes exact-match accuracy, NLL, acquisition
at last exposure, last-exposure timing, effective loss coefficients and pre-clipping
gradient norms. Random-condition last-exposure probing is now enabled.

The estimand should be the total placement-policy effect, not pure consolidation:
random differs in recency and batch composition. Three seeds cannot establish
equivalence. Do not reuse the old 0.041 cutoff as if statistically calibrated.

Current tracked filler file: `data/wikitext103_tokens.npy`, expected file SHA-256
`868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304`.
New runs must supply `--filler-snapshot` AND `--filler-sha256`, pin model/software
versions, verify paired stream hashes, and use the dedicated `results/study7` directory.
Use the registered chain command above, not the legacy training scripts.

Previous random runs took 14.2–14.7 minutes each, excluding some setup overhead.
Budget roughly 1.5–2 hours for six runs, with uncertainty for extra probes. Do not
restart all 73 historical runs. Preserve results; stop immediately if asked to close.

## Local verification

`uv run pytest -q`

`uv run python -m spacinglab.provenance_audit` reconstructs the audit from Git and
stored logs; it overwrites only the audit JSON with the current execution commit.
Do not run it merely to erase the original audit execution provenance.

Use only Sonnet if subagents are needed. Do not touch ForgetLab. No remote or push
without the user's approval. Explain findings in short, plain Turkish.
