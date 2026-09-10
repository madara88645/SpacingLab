# Study 13 implementation and verification record

Registration fbda2c9 precedes every Study 13 model evaluation. The user approved
equal distinct-fact coverage as well as equal replay budgets. Implementation uses
80 distinct previously learned facts replayed once in BOTH arms; no-revisit is
limited to interference replay and does not alter five-exposure acquisition.

Design/planning and test-first skills were used locally. No agents or extra
experiments. Keep the research checkout and local branch; no merge, remote or
worktree cleanup is requested. Existing lock files are retained untouched.

New selector spacinglab/study13_replay.py generates one 80-item uniform sample,
then ranks deterioration among not-yet-used eligible facts within paired length
slots. It reuses the frozen Study 12 within-round score/tie implementation.
History validation prevents cross-round revisits. Sufficient bucket capacity
follows from the globally without-replacement uniform plan and matched preceding
bucket counts. Tests include all-zero scores and one rare-length eligible fact.

New runner spacinglab/study13.py is isolated from historical runners. The reviewed
diff changes only identifiers/seeds, no-revisit state/validation, coverage metadata
and retention of already-computed new-fact details. Model updates, common-fork
restoration, optimizer, stream and evaluation timings are unchanged. New raw
new_fact_evaluation dictionaries add no probe calls or training.

Verification before real-model measurements:

- Historical baseline: 60 tests passed.
- New policy suite: 10 tests failed with missing-policy assertions, then 10 passed.
- New runner suite: 9 tests failed with missing-runner assertions, plus the new
  logging test failed before the runner existed; all 10 subsequently passed.
- Full suite: 80 tests passed, including CPU/MPS toy optimizer-fork checks.
- Synthetic full three-pair fixtures verify summary calculation, exclusive
  completed logs, malformed coverage/history rejection and inflated-budget rejection.
- git diff --check passed. Every historical source/test/dependency/registration
  digest from the Study 12 manifest still matches. No new pretrained-model inference
  was used to tune the policy, select seeds or choose thresholds.

Commands (existing uv environment, no dependency updates):

```
uv run --no-sync pytest -q
uv run --no-sync python -m spacinglab.study13
uv run --no-sync python -u -m spacinglab.study13 --run
```

The middle command freezes and checks provenance only. Commit implementation,
then run preflight and commit results/study13/manifest.json BEFORE --run.
The runner is finite: exactly seeds 12,13,14, one common prefix and two arms each.
An incomplete attempt, fewer than 80 eligible facts, nonfinite result or invariant
failure halts the chain. Preserve it; do not overwrite, tune or automatically retry.

Completion audit must verify exact cumulative coverage 20,40,60,80, all per-fact
replay counts in {0,1}, per-step length/token matching, state/provenance identities,
selection reconstruction with historical used-ID exclusions, old AND new per-item
metrics, primary all-fact delayed scores and registered secondary guards. Retain
mixed/negative outcomes. No pooled result or causal-mediation claim about Study 12.
No new experiment without Mehmet's understanding and explicit approval.
