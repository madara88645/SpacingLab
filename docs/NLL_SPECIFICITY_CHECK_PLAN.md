# Post-hoc specificity check — 9 September 2026

This is a transparent analysis of existing Study 10 logs, not a new preregistered
experiment. The true-answer NLL and discrimination summaries are already known;
therefore the derived foil result is not an independent discovery. Commit this
description before computing the additional foil summaries. No model is trained.

Question: did variable gaps improve true-answer NLL selectively, or also improve
the score of an incorrect same-template answer?

The existing Evaluator assigns a cyclically shifted answer within each template
group as the foil. It logs per-token teacher-forced NLL on answer tokens, averaged
per fact, and discrimination = foil NLL minus true NLL. Higher discrimination is
better separation. These are not normalized full-answer sequence probabilities:
answer lengths and teacher forcing prevent that literal interpretation.

Use only Study 10 seeds 3,4,5, all 200 facts and the seven registered interference
checkpoints. Recompute per-fact then checkpoint means for true NLL, foil NLL and
their difference; validate against logged aggregates and existing summaries.
For each arm and paired variable-minus-fixed difference, report all three values,
mean, sample SD and range. No p-value, new threshold, correct-only subset, pooling,
regeneration or hidden metric selection. Exact-match primary remains inconclusive.

Interpretation rule: if both true and foil NLL improve but discrimination does not
consistently improve, true-answer NLL alone does not identify a fact-specific
retention benefit. This does NOT prove all improvement is format, does not provide
a percentage decomposition, and does not establish representation erasure or an
absence of knowledge. One foil per fact and unequal answer token lengths are
limitations. A future confirmatory experiment would need fresh data and a stronger
matched control with a prespecified primary endpoint.

Background only: Zhao et al., ICML 2021, Calibrate Before Use, documents answer
bias and content-free calibration in few-shot prompting. It motivates separating
answer propensity from task evidence, but is not evidence that our fine-tuning
effect has the same cause: https://proceedings.mlr.press/v139/zhao21c.html
