# Study 12 implementation record

The user approved the selective-replay A/B experiment after explaining the
contrast. Registration dd3e56c predates every Study 12 model evaluation or training.
Only three pairs (seeds 9,10,11) are authorized; no pilots or extra arms.

The old training modules are unchanged. New isolated modules:

- spacinglab/study12_replay.py: learned-pool construction, matched input-length
  quotas, deterioration scores, seeded ties, immutable model/optimizer forks,
  and masked batch assembly.
- spacinglab/study12.py: one acquisition prefix per seed, serial forked
  continuations, full logs/provenance, finite runner, paired validation and analysis.
- tests/test_study12*.py: synthetic fixtures and toy tensor models only, not
  research pilots. Tests were run failing before implementation, then passing.

Tests exercise never-learned exclusion, current-difficulty versus deterioration,
zero-score fallback, exact per-step length matching, fork immutability, optimizer
moment restoration on CPU and MPS, batch masking, true token counts, manifest
drift, delayed all-fact primary scoring, exclusive final logs, paired validation
and complete three-pair analysis. An integration fixture caught a NumPy integer
serialization bug in the zero-score count before model training; it was corrected.

Commands, using the existing environment without dependency updates:

```
uv run --no-sync pytest -q
uv run --no-sync python -m spacinglab.study12
uv run --no-sync python -u -m spacinglab.study12 --run
```

The first runner command freezes provenance without model evaluation. Commit the
implementation before preflight, then commit results/study12/manifest.json before
--run. Do not modify frozen source or software while the chain is active.

Parent process holds a lock and launches one seed pair at a time. Each seed has
a retained local fork.pt (not committed to Git), common.json, console.log and two
arm logs. Model and optimizer fingerprints must exactly match at the fork. Failure
preserves the incomplete folder and halts the chain; no automatic overwrite/retry.
Final guards and raw selection probes enable independent audit after completion.
No remote, push, private data or further study is authorized.
