# Study 13 Coverage-Matched Replay Implementation Plan

> **For agentic workers:** Use executing-plans locally; no delegation is required or authorized for this bounded continuation. Steps use checkboxes.

**Goal:** Implement the approved comparison with exactly 80 distinct replayed facts per arm.

**Architecture:** Keep every historical module unchanged. Add an isolated replay
selector and finite Study 13 runner following the verified Study 12 orchestration.
Reuse frozen batch/state helpers, not historical results. Match length slots and
cumulative unique-item counts; maintain a separate used-ID set in each arm.

**Tech Stack:** Existing uv environment, Python, NumPy, PyTorch/MPS, Transformers, pytest.

## Approved design and scope review

- [x] Read current results and protocol; no active training and only old lock files untracked.
- [x] No visualization is necessary for this two-arm comparison.
- [x] User approved the explained equal-coverage A/B test; use the existing local
  research repository and preserve the branch, no remote, merge or cleanup.
- [x] Considered exact yoking of past repeat patterns, fresh random no-revisit
  control alone, and no-revisit in BOTH arms. Use the last: fixed prospective
  coverage, no dependence on future outcomes, readily checked at every round.
  It changes both policies and cannot identify causal mediation of Study 12.
- [x] Exact quotas, eligible threshold, fixed seeds, zero-score fallback and stop
  rule are in docs/STUDY13_PREREGISTRATION.md; no unresolved design placeholders.

## Task 1 — Register the experiment

- [x] Commit docs/STUDY13_PREREGISTRATION.md and this plan before producing Study 13 model measurements.

## Task 2 — Pure no-revisit selection (tests first)

Files: tests/test_study13_replay.py; spacinglab/study13_replay.py.

- [x] Write failing assertions for global uniqueness, eligibility, token-slot
  matching across all rounds, deterministic ties, insufficient learned pool and
  blocked repeated selections. Core fixture:

```python
correct, lengths = [1]*100+[0]*20, [10,11,12]*40
plans = make_plan(correct, lengths, 12)
ids = [i for p in plans for i in p['uniform_ids']]
assert len(ids) == len(set(ids)) == 80
```

- [x] Run `uv run --no-sync pytest -q tests/test_study13_replay.py`; expect missing-policy assertions before implementation.
- [x] Implement make_plan using one `choice(eligible,4*quota,replace=False)` from
  RNG seed+60000 and partition into four blocks. `select(..., used_ids)` validates
  history, removes used IDs before ranking, and delegates unchanged score/tie/
  per-step-length logic to the frozen Study 12 selector. Return used-before IDs
  for audit. Reject duplicate/replayed/unknown history and capacity failures.
- [x] Run the policy tests again; require all passing before the runner.

## Task 3 — Finite runner and integration fixtures (tests first)

Files: tests/test_study13.py; spacinglab/study13.py; .gitignore.

- [x] Adapt the existing synthetic fixture tests to seeds 12,13,14, new output,
  immutable manifest coverage fields and cumulative used-ID history. Add mutation
  tests for coverage counters, no-revisit history and fresh raw new-fact retention.
- [x] Run `uv run --no-sync pytest -q tests/test_study13.py`; expect missing-runner assertions.
- [x] Isolate the existing runner with all Study 12 labels changed to Study 13,
  SEEDS=(12,13,14), middle arm-order seed 13, and SEEDS[0] analysis lookup.
  Import new make_plan/select and existing batch/capture/fingerprint/restore.
  At branch start use `used_ids=set()`; pass it into select, then update it after
  each round. Save distinct_replayed, cumulative counts and per-fact counts.
  Validation reconstructs the used set, verifies saved counts and max count 1.
  Freeze `distinct_replay_quota=80`, `max_replays_per_fact=1`, and new test hashes.
  In evaluate, save the already-computed new-fact evaluation as `new_fact_evaluation`.
- [x] Ignore only results/study13/seed_*/fork.pt. Do not ignore raw results.
- [x] Run all tests, `git diff --check`, and compare the runner diff against Study
  12 for unintended training changes. Confirm new tests catch wrong coverage.
- [ ] Commit tested implementation and verification record.

## Task 4 — Freeze, launch and hand off

- [ ] `uv run --no-sync python -m spacinglab.study13` freezes provenance without
  model evaluation. Verify historical source/model/data/software hashes against
  Study 12's immutable manifest. Commit the new manifest before `--run`.
- [ ] `uv run --no-sync python -u -m spacinglab.study13 --run` starts exactly three
  pairs. Verify process plus advancing prefix log; do not interpret early results.
- [ ] Update RESUME.md and the existing paused heartbeat to this Study 13-only
  scope: quiet normal progress, no duplicate training/restart/extra seeds, audit
  all outcomes at completion then pause. Keep local branch and all files intact.
- [ ] Tell Mehmet briefly that it started, explain fixed 80-distinct-item fairness,
  and give a qualified runtime estimate. No new study is authorized after this one.
