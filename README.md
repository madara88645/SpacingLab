# SpacingLab

**How does the timing and selection of repeated facts affect what a small language model retains during fine-tuning?**

SpacingLab is a laptop-scale research project inspired by spacing and selective replay in memory research. It starts with consecutive versus spaced repetitions, then tests whether irregular intervals or replaying deteriorating facts help. The experiments use GPT-2 (124M), synthetic facts and a WikiText-103 background stream on Apple Silicon.

The project includes negative results, failed predictions and a withdrawn comparison. It does not establish a generally better training method or a biological memory mechanism.

[Türkçe özet](RAPOR_TR.md) · [Full research report](RESEARCH_REPORT.md) · [Publication and reproduction limits](PUBLICATION.md)

## Latest finding: choosing what to repeat

In Study 13, two continuations started from the same learned model and optimizer state. Both repeated **80 distinct learned facts exactly once**, at the same training slots and with matched token budgets. One selected facts randomly; the other selected facts whose correct-answer likelihood had deteriorated since learning.

Across three paired seeds, prioritized replay improved the primary delayed-accuracy measure by **4.50 percentage points, sample standard deviation 2.21 points**. Individual differences were **+6.60, +2.20 and +4.70 points**. Accuracy was averaged over five later checkpoints and all 200 original facts, not just the selected replay facts.

This is a positive **three-pair screening result**, not evidence of statistical significance or general superiority. The terminal-only result was mixed, and correct-versus-incorrect answer separation did not consistently improve. Equal coverage rules out a simple count advantage in this study; it does not isolate a neural memory mechanism or explain the earlier study causally.

[Study 13 interpretation](results/study13/WRITEUP.md) · [All metrics and seed spreads](results/study13/REPORT.md) · [Recorded audit](results/study13/AUDIT.md) · [Local preregistration record](docs/STUDY13_PREREGISTRATION.md)

## How the question developed

| Question | What the experiments support |
|---|---|
| Consecutive or spaced repetitions? | Spaced repetitions produced higher later exact-match accuracy in the tested setup, but initial learning also differed. The original equal-learning, slower-forgetting hypothesis was **not supported as written**. |
| Is ordinary shuffling sufficient? | A historical comparison reused a control with different background data. Its claim was **withdrawn** after a provenance audit. Later matched comparisons are reported separately. |
| Are irregular gaps better than fixed gaps? | Follow-up and replication results were mixed. Neither a universal best gap of 64 steps nor superiority of irregular spacing was established. |
| Repeat deteriorating facts or choose randomly? | Study 12 gave a positive small-screen result but covered different numbers of distinct facts. Study 13 matched that count and gave the positive primary result above, with important secondary limits. |

The [full report](RESEARCH_REPORT.md) retains the earlier studies, calibration failures, alternative explanations and corrections. The [data-provenance audit](docs/PROVENANCE_AUDIT_2026-09-08.md) explains the withdrawn comparison. Studies are not pooled into a single effect estimate.

## What is measured

- **Exact-match accuracy:** whether the generated answer is exactly correct.
- **Answer NLL:** how much probability the model assigns to the correct answer; lower is better. This can change even when the final answer is wrong.
- **Answer separation:** how the model distinguishes a correct answer from a deliberately wrong alternative. NLL alone does not establish fact-specific memory.
- **Controls:** initial learning, repeated-fact coverage, training steps and tokens, new-fact learning, background-text performance and seed-to-seed variation.

Loss of a correct answer is not proof that an internal representation has been erased. These experiments do not establish benefits for personal writing style, large models, general PEFT workflows or human learning.

## Explore the repository

| Location | Contents |
|---|---|
| `spacinglab/` | Training, scheduling, replay policies and analysis code |
| `tests/` | Software tests for schedules, paired controls and replay rules |
| `PREREGISTRATION.md`, `docs/STUDY*_PREREGISTRATION.md` | Local design records and amendments; timing limitations explained below |
| `results/` | Per-run measurements, reports, historical audits, pilots and failed attempts |
| `RESEARCH_REPORT.md` | Detailed English research narrative |
| `RAPOR_TR.md` | Short Turkish explanation of the latest result |

## Check the results without training

For the latest primary result, only Python's standard library is required:

```sh
uv run --no-project python scripts/check_public_results.py
```

This recomputes Study 13's paired accuracy differences from the six published continuation logs and checks them against the saved summary. It does **not** reproduce training or replace the historical audit.

For the existing software tests and Study 1 analysis:

```sh
uv sync --locked --group dev
uv run --no-sync pytest -q
uv run --no-sync python -m spacinglab.analyze
```

Installing the full environment includes PyTorch and may be substantial. No command above launches the pretrained-model experiments.

## Publication status and reproducibility

This repository is a **public snapshot**, not the original local Git history. Source code and numerical measurements are preserved; personal absolute paths are replaced with placeholders. Private operational notes, model checkpoints and the third-party dataset cache are omitted. See [PUBLICATION.md](PUBLICATION.md) and [EXPORT_MANIFEST.json](EXPORT_MANIFEST.json).

Historical audit statements describe checks performed on the original local files. Some historical hashes and commit references cannot be resolved against this redacted snapshot. The local preregistration records are **not independently timestamped public preregistrations**. Full training reproduction requires the exact original inputs and a deliberate new setup; recreating a dataset cache is not proof of matching it.

Research runs are complete and paused. A possible next question is whether deterioration-based selection beats selecting facts that are simply hardest now. That experiment has not been run.
