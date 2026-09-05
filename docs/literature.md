# Literature notes (gathered 2026-09-05 by two Sonnet research agents; URLs verified by them, claims re-read by me)

## Is the exact manipulation already in the literature?
Not that we could find. Nothing located varies only the **step gap between repeated
exposures of the same fact** inside one fine-tuning run with total exposures, steps,
tokens and time-since-last-exposure held fixed. Closest work:

- **Chang et al. 2024**, *How Do LLMs Acquire Factual Knowledge During Pretraining?*
  (NeurIPS 2024) — https://arxiv.org/abs/2406.11813. Injects fictional facts into live
  pretraining checkpoints. Duplicated injection gives higher initial memorisation but is
  offset by faster forgetting than paraphrased injection; larger batches slow forgetting.
  Does not vary the gap between duplicates as an independent variable (from abstract and
  secondary sources; full methods not checked).
- **Allen-Zhu & Li 2023/24**, *Physics of LMs 3.1* — https://arxiv.org/abs/2309.14316.
  Knowledge becomes extractable only with paraphrase augmentation; verbatim repeats can
  leave it stored but unusable. Diversity axis, not timing axis.
- **arXiv:2507.14198**, *On the Retention of Edited Knowledge in Fine-tuned LMs* —
  edited/injected facts forget faster under later fine-tuning than pretrained facts;
  ~3 paraphrases close most of the gap. Paraphrase count, not spacing.
- **Hernandez et al. 2022** (https://arxiv.org/abs/2205.10487) and **Muennighoff et al.
  2023** (https://arxiv.org/abs/2305.16264): corpus-level repetition / epochs; repeats are
  spread by construction.
- Spaced-repetition *scheduling* for ML (which example to replay when): Amiri et al. 2017
  https://aclanthology.org/D17-1255/; Kang et al. CVPR 2025 https://arxiv.org/abs/2503.18371;
  MSSR https://arxiv.org/abs/2603.09892; FOREVER https://arxiv.org/abs/2601.03938. None
  isolate gap length for one item.
- Mechanism side (why consecutive identical steps might be fragile): no direct paper.
  Adjacent: *The Order Is The Message* https://arxiv.org/abs/2603.25047 (ordering acts
  through Hessian–gradient coupling between consecutive steps); Charton & Kempe 2024
  https://arxiv.org/abs/2410.07041 (repeating a subset, interspersed, speeds learning).

## The human spacing effect, stated carefully
- Canonical synthesis: **Cepeda, Pashler, Vul, Wixted & Rohrer 2006**, Psych. Bulletin,
  839 effect sizes — https://augmentingcognition.com/assets/Cepeda2006.pdf. Spaced beats
  massed on delayed tests; the best inter-study interval grows with the retention interval.
- **Lag effect / optimal gap:** Cepeda et al. 2008, *A temporal ridgeline of optimal
  retention* — https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf.
  Inverted U: more spacing helps, then hurts. Optimal gap ≈ 20–40 % of the retention
  interval for a 1-week test, ≈ 5–10 % for a 1-year test.
- **Expanding vs equal intervals:** roughly a wash for long-term retention (Karpicke &
  Roediger 2007; Kang et al. 2014). Pop-science claims that expanding schedules are
  superior are not supported by the primary literature.
- **Massed better at very short delays?** Described in secondary sources, not uniformly
  confirmed in meta-analyses; hedge.
- **Mechanism theories:** encoding variability; study-phase retrieval / reminding (best
  direct support); deficient processing; consolidation between exposures (cellular level,
  Smolen, Zhang & Byrne 2016 https://arxiv.org/abs/1606.08370). Reviews favour a mix.
- **Spacing in artificial networks (recent):** Sun et al. 2025, spacing in knowledge
  distillation, flatter minima — https://arxiv.org/abs/2502.06192; *Spacing effect
  improves generalization in biological and artificial systems*, Patterns 2026 /
  bioRxiv 2025.12.18.695340 — spacing applied at dropout / weight-averaging /
  distillation levels. These are about generalisation, not retention of injected facts.

## What this means for SpacingLab's claim
The narrow claim ("for fact injection by fine-tuning, consecutive repeats of the same
sequence produce a memory that decays within tens of steps, while the same repeats
spread 64 steps apart survive") appears not to have been measured before. The
practical corollary — keep repeats/paraphrases of one fact far apart in the shuffle —
is consistent with Chang et al.'s duplicated-vs-paraphrased finding but was not their
manipulation. Our mechanism story is our own hypothesis; Study 2a tests one piece.
