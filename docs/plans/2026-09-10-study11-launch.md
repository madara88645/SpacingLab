# Study 11 launch implementation plan

> **For agentic workers:** Use executing-plans locally, without delegation. The user has approved only six runs in the existing repository; do not move the experiment or start another study.

**Goal:** Launch the preregistered finite three-pair screen and make completion safely reviewable.

**Architecture:** Add an isolated Study 11 runner by mechanically adapting Study 10's tested runner; leave historical runners and shared training code unchanged. Keep new outputs under results/study11.

**Tech Stack:** Existing uv environment, Python, pytest, PyTorch MPS, local Git.

## Execution checklist

- [x] Read Study 9/10 protocols and current state; verify no training process and baseline tests (39 passed).
- [x] Keep existing checkout/data paths; use local branch study11-small-retest, no worktree relocation or remote operations.
- [ ] Commit docs/STUDY11_PREREGISTRATION.md before model evaluation or training.
- [ ] Create tests/test_study11.py from the Study 10 tests, replacing seeds 3/4/5 with 6/7/8, alternating order, output tag and required registration paths. Verify tests fail because spacinglab.study11 is absent.
- [ ] Create spacinglab/study11.py from Study 10 using precisely the registered seed/order/tag changes; include all three registrations in its immutable manifest. Preserve metrics, guards and three-seed rule. Test configuration against Study 9 except the tag, reject old seeds, and verify schedule endpoints and manifest drift detection.
- [ ] Run `uv run --no-sync pytest -q` and `git diff --check`; commit runner/tests.
- [ ] Compare shared source, package and model hashes against Study 10's frozen record without rewriting it. Run `uv run --no-sync python -m spacinglab.study11` to freeze inputs without evaluating the model; commit results/study11/manifest.json.
- [ ] Run `uv run --no-sync python -u -m spacinglab.study11 --run` once. Verify a live child and advancing first-run log before claiming training started.
- [ ] Update RESUME.md with the authorized scope and resume/stop instructions; arrange quiet completion checking without duplicate training launches.
- [ ] At completion: verify all six raw logs against registration/manifest, report mean plus seed spread and all previous blocks separately, commit evidence, then stop. Subsequent training requires user approval.
