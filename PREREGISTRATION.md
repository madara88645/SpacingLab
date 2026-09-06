# Pre-registration: does spacing repetitions protect fine-tuned facts from later forgetting?

Written 2026-09-04, before any experiment number existed. Anything changed after the
first main run is recorded under "Amendments" with the reason and the date; the git
history is the timestamp.

## The phenomenon borrowed from human memory

The **spacing effect** (Ebbinghaus 1885; Cepeda et al. 2006 meta-analysis): the same
number of study repetitions produces better long-term retention when the repetitions
are spread out in time, with other material in between, than when they are massed
back-to-back. It is one of the most replicated findings in the learning literature.

## The one question

When a small pretrained language model is fine-tuned to absorb a set of new facts,
each shown K times, does **spreading a fact's K exposures apart** in training time
(other data in between) rather than **presenting them in consecutive steps** improve
how well the fact survives **subsequent fine-tuning on unrelated text**, when
everything else is held equal: total exposures, total gradient steps, total tokens,
the other data seen, and the time since the fact's last exposure?

## Prediction (committed now)

**H1 (spacing effect):** retention after the interference phase increases with the
spacing gap. Concretely, the retention score (defined below) at gap 64 is higher than
at gap 1, in every seed, by more than the seed-to-seed spread.

Supporting, not required: retention is monotone across gaps 1 < 4 < 16 < 64.

**Immediate learning is a guard, not a prediction.** My prior is that massed
exposures (4 consecutive Adam steps on the same sequence) memorise *at least as
strongly* immediately as spaced ones. If massed learns *less* immediately, the
retention difference is confounded by learning and the contingency below applies.

**What would kill H1:** retention(gap 64) − retention(gap 1) is inside the seed
spread or the replication-noise band, or is negative, in the primary metric.

## Design

### Model and training
- `gpt2` (124M parameters), full fine-tuning, fp32, Apple-Silicon MPS.
- Dropout set to 0 everywhere (removes a noise source and a hidden regulariser).
- AdamW, betas (0.9, 0.999), weight decay 0, gradient clipping at 1.0.
- Learning rate: linear warmup over the first 50 steps of the pre-phase, then constant
  for the rest of the run. The value is fixed by the pilot (below).
- Loss: each sequence in a batch contributes the mean cross-entropy over its label
  tokens; the batch loss is the mean over sequences ("one document, one vote"). This
  is declared because it gives a 13-token fact the same weight as a 64-token filler
  chunk; the alternative per-token weighting would make a single fact ~1% of a batch
  and would need far more exposures to learn.

### Data
- **Facts:** N = 100 synthetic paired-associate facts per seed. Each is one sentence
  from one of five templates (capital-of, born-in-town, river-flows-into-lake,
  currency-of, founder-of) with *invented* subject and answer names (random
  pronounceable syllable strings, capitalised, all unique within a seed). Invented
  names mean the pretrained model cannot know the answer: pre-injection accuracy must
  be 0 and is checked.
- **Filler / interference text:** WikiText-103 train, tokenised as one stream with
  `<|endoftext|>` between articles, cut into 64-token chunks, consumed in a fixed
  per-seed order. The injection phase and the interference phase draw from the same
  stream, so the interference text is *disjoint* from but *same-domain* as the filler.
  That is a scope limit, stated here.

### Phases of one run (all conditions identical except exposure placement)
1. **Pre-phase:** 100 steps of filler only (LR warmup happens here, so no fact is
   ever shown at a reduced learning rate).
2. **Injection window:** T_inj = 600 steps. Every step has 15 filler chunks; fact
   sequences are *added on top* of the filler at their exposure steps, so the filler
   consumed at every step is byte-identical across conditions.
3. **Interference phase:** 1500 steps of filler only.

### Conditions (the only manipulated variable)
For each fact i, a **last-exposure step** p_i is drawn uniformly from
[(K−1)·64, T_inj) once per seed and shared by all conditions. The fact's K exposure
steps are p_i − j·g for j = 0..K−1, where the gap g is the condition:

| condition | gap g (steps) | meaning |
|---|---|---|
| massed | 1 | K consecutive steps |
| gap4 | 4 | |
| gap16 | 16 | |
| spaced | 64 | span of (K−1)·64 steps |

Because p_i is shared, the time from a fact's *last* exposure to any evaluation point
is identical across conditions (this is the classic recency confound in human spacing
studies; it is removed here by construction). Total exposures (N·K), total steps,
total filler tokens and total fact tokens are equal by construction and are logged
and asserted.

### Measurement
For each fact, the prompt is the sentence with the answer removed (e.g. "The capital
of Zorbland is"), prefixed with `<|endoftext|>` as in training. Two measures:
- **exact-match accuracy**: greedy decoding of len(answer tokens) tokens equals the
  answer tokens. Averaged over the 100 facts.
- **answer NLL**: teacher-forced mean negative log-likelihood per answer token,
  averaged over facts (continuous, no ceiling).

Evaluation points: before injection (must be ≈0 accuracy), immediately after the
injection window ("immediate"), and at interference steps
{50, 100, 200, 400, 800, 1200, 1500}. Filler held-out loss (200 held-out chunks) is
measured at the same points to confirm the interference phase really trains.

- **Primary outcome:** *retention score* = mean exact-match accuracy over the seven
  interference checkpoints.
- **Secondary:** accuracy at step 1500; the NLL analogues of both; immediate accuracy.
- **Guards logged per run:** immediate accuracy and NLL; parameter displacement
  ‖θ − θ_pretrained‖ after injection and at the end; filler tokens and fact tokens
  seen; number of optimizer steps.

### Seeds and noise
- Seeds 0, 1, 2 (minimum three). A seed fixes the facts, p_i, and the filler order;
  all four conditions of a seed share them, so comparisons are paired within seed.
- One extra run: condition `spaced`, seed 0, repeated. Its difference from the
  original is the *replication-noise band* (MPS kernels are not bit-deterministic).
- Total: 4 × 3 + 1 = 13 runs.

### Decision rule (fixed now)
H1 is **supported** if all of:
1. retention(spaced) > retention(massed) in each of the 3 seeds;
2. the mean paired difference exceeds both the SD of that paired difference across
   seeds and the replication-noise band;
3. |immediate(spaced) − immediate(massed)| is smaller than the retention difference
   (otherwise "learned more" rather than "kept more" is the simpler story and the
   result is reported as confounded).

Otherwise H1 is **not supported**; the numbers are reported as they are.

### Named traps and how each is handled
| trap | handling |
|---|---|
| spaced simply *learns more* at injection time | immediate accuracy/NLL reported next to retention; rule 3; contingency below |
| more gradient steps / more tokens in one condition | equal by construction; asserted from logs |
| different filler seen | identical stream per seed; facts added on top, never displacing filler |
| recency: spaced facts were seen more recently | last-exposure step p_i shared across conditions |
| ceiling / floor | pilot targets immediate accuracy in [0.5, 0.95] and non-zero retention at 400 steps; both checked in the main runs |
| pretrained prior knows the answers | invented names; pre-injection accuracy asserted ≈ 0 |
| run-to-run nondeterminism read as an effect | replication run defines the noise band |
| the effect is about weight displacement, not spacing per se | ‖Δθ‖ logged and reported; a difference here is a mechanism note, not a rescue |
| accuracy hides graded knowledge | NLL reported alongside |

### Pilot (calibration only, before the main runs)
The pilot uses a **fifth placement, "random"** (each fact's K exposures at K
distinct uniformly random steps in the injection window), seed 100, interference
shortened to 400 steps, to choose the learning rate and K from the grid
lr ∈ {1e-4, 3e-4} × K ∈ {4, 8}. Selection criterion: smallest K such that some lr
gives immediate accuracy in [0.5, 0.95] and accuracy at interference step 400 ≥ 0.10;
ties broken toward the lower lr. The chosen values are recorded under Amendments
before the main runs start. The pilot never compares gaps, and its numbers are not
part of the result. If K = 8 is needed, the injection window becomes 800 steps so
that p_i has a range of at least 350 steps.

### Contingency (pre-declared)
If rule 3 fails because massed learns less immediately, one additional condition is
run: `massed_matched`, K increased until its immediate accuracy is within 0.05 of
`spaced` (same seeds). Its retention is compared to `spaced` under the same rules,
and reported explicitly as a post-hoc learning-matched control.

## Scope of any conclusion
One model (GPT-2 124M), one fact format (synthetic single-sentence paired associates),
one interference corpus (WikiText-103, same domain as filler), one optimiser
setting, exposures K fixed by the pilot. Nothing here speaks to larger models,
real-world facts, LoRA, or different interference domains.

## Amendments

### Amendment 1 (2026-09-04, after the pilot, before any main run): stronger interference
**What the pilot showed.** With same-domain WikiText as the only interference, almost
nothing was forgotten: at k=4/lr=1e-4 accuracy went 0.47 → 0.42 over 400 interference
steps; at k=8 it stayed at 0.97–0.99 at both learning rates. lr=3e-4 was rejected
independently: it made the held-out filler loss *worse* than lr=1e-4 (3.54 vs 3.44)
and moved the weights twice as far, i.e. it damages the model rather than tuning it.
The pilot also showed exact-match accuracy can rise briefly after the last exposure
while NLL rises monotonically; the primary metric stays accuracy as pre-registered, and
NLL is reported alongside in every table.

**Why that matters.** If the interference phase forgets nothing, the "retention score"
is just the immediate score measured seven more times, and spacing has nothing to
protect. The design would be unable to say anything about retention.

**Change.** The interference phase is now filler **plus 300 new facts** of the same
five templates with disjoint invented names ("set B"), each shown 4 times at random
steps of the interference phase. Set B and its placement are seeded and identical
across all conditions of a seed. This is the classic retroactive-interference layout
of human memory experiments (learn list A, then list B, test A). Set B accuracy is
logged at every checkpoint as a guard that the interference is really being learned.
Interference from a different text domain is left as future work.

**Second pilot.** lr fixed at 1e-4. K ∈ {4, 6} with the new interference, seed 100,
random placement, 400 interference steps. Selection: smallest K with immediate accuracy
in [0.5, 0.95] and accuracy at 400 steps ≥ 0.10 and at least 0.10 below immediate
(so that there is forgetting to protect). The chosen K is recorded in Amendment 2.

### Amendment 2 (2026-09-04, after pilots 2 and 3, before any main run): frozen values
**Pilot 2 (300 interference facts).** Far too strong: set-A accuracy fell from 0.43
(k=4) and 0.91 (k=6) to ≤ 0.04 within 50 interference steps, before set B itself
was learned at all. Floor.

**Pilot 3 (k=5, 15 vs 50 interference facts, full 1500-step interference).**
15 facts: immediate 0.77 → final 0.43 (final/immediate = 0.56, fails the "≤ 0.5" rule
narrowly). 50 facts: immediate 0.67 → final 0.18 (0.27; accuracy at 200 steps 0.25 =
0.37 × immediate, passes). **Chosen: k = 5, lr = 1e-4, 50 interference facts × 4
exposures.**

**Noise floor discovered.** The two pilot-3 runs have byte-identical pre-phase and
injection phases (the dose only differs afterwards), yet reached immediate accuracy
0.77 vs 0.67 and NLL 0.25 vs 0.38. MPS kernels are not deterministic and the
divergence compounds over 700 steps. A 0.10 accuracy difference can therefore arise
from nothing. Two responses, both decided before the main runs:
1. **N = 200 facts** instead of 100 (per-fact sampling noise of the accuracy estimate
   halves in variance). The immediate-accuracy band [0.5, 0.95] will be checked in
   the main runs rather than re-piloted; a violation is reported as a calibration
   failure, not repaired after the fact.
2. **Five seeds (0–4) for the core massed-vs-spaced comparison.** gap4 and gap16 keep
   three seeds (0–2) as the supporting dose-response. The replicate (spaced, seed 0)
   stays. Total 17 runs. The decision rule is unchanged and is applied to the five
   core seeds.

**Housekeeping.** Run directories now include N and the interference size (the two
pilot-3 logs overwrote each other; their printed evaluations are in
`results/pilot3.log`). The filler chunk order is pinned to the cached token file so it
no longer depends on how many tokens a run requests.

### Amendment 3 (2026-09-04, main launch failed before producing any number)
With k = 5 the spaced span is (k−1)·64 = 256 steps, leaving p_i a range of only 344
steps inside a 600-step window; the schedule builder's own assertion (range ≥ 350)
stopped every run at start-up. The pilots used random placement, which has no such
check. **Injection window T_inj = 700** (p_i range 444). This adds 100 filler-only
steps early in the window for all conditions equally; the pilot calibration is
assumed to carry over, and the immediate-accuracy band is checked in the main runs
as stated in Amendment 2. No main-run number existed when this was changed.

### Amendment 4 (2026-09-04, after one aborted main run; additive measurement only)
**What was seen.** The first main run (massed, seed 0) reached immediate accuracy
0.02 / NLL 5.0 at the end of the injection window, against 0.67–0.77 for random
placement in the pilots. The run was discarded (kept under `results/aborted/`), and
nothing else from it is used. A 20-fact smoke test of the new measurement showed
massed facts at 0.47 accuracy *right after their fifth exposure* and 0.025 at the end
of the window.

**Why the pre-registered guard is not enough.** "Immediate" accuracy is measured at a
fixed step, up to 444 steps after a fact's last exposure, and the window itself
contains dense interference (the other 199 facts). So a low immediate score can mean
*never encoded* (a learning difference: rule 3 rightly flags it) or *encoded and lost
inside the window* (which is the phenomenon under test). The original design cannot
tell these apart.

**Added measurement.** Right after the optimizer step at each fact's last exposure
p_i, that fact alone is evaluated (accuracy + NLL + generated answer). Per run this
gives `acc_at_last_exposure` — the encoding strength before any further delay. It adds
~20 s per run and changes no training computation.

**Pre-declared analysis using it.**
- The pre-registered rules 1–3 are still applied exactly as written and reported first.
- Encoding guard: acc_at_last per condition. If massed is far below spaced here, part
  of the effect is a *learning* difference and is labelled so.
- Conditional retention: among facts correct right after their last exposure, the
  fraction still correct at each checkpoint (immediate and the seven interference
  points), per condition and seed. **H1 predicts spaced > massed here too.** If
  conditional retention is equal and only acc_at_last differs, the honest summary is
  "spacing makes each exposure teach more, not remember longer".
- The same in NLL: change in NLL from at-last to each checkpoint.

No condition, hyperparameter or decision rule changed. Runs restart from scratch.

### Amendment 5 (2026-09-05, after all 17 Study 1 runs; Study 2 pre-registration)
**Status of Study 1 at the time of writing.** All 17 runs are in. Rules 1 and 2 hold
(spaced > massed retention in every seed; mean Δ = +0.285, seed SD 0.041). Rule 3
fails: the immediate difference (+0.62) is larger than the retention difference, so
H1 as pre-registered is **not supported**. Amendment 4's encoding measurement shows
massed facts *are* encoded right after their fifth exposure (acc 0.43 vs spaced 0.81)
and are gone within ~50 steps. The pre-declared contingency (`massed_matched`,
K raised) is running on seed 0 with K ∈ {10, 20} as a bounded probe (two runs).

Study 2 asks two questions about that finding, and each is committed here before any
of its numbers exist. Nothing in Study 1's analysis changes.

**2a. Is Adam's momentum the mechanism?** The obvious boring story: five identical
consecutive gradients pump the first-moment estimate, so massed exposures overshoot
along one direction and the filler pulls them back. Test: massed vs spaced, seeds
0–2, identical to Study 1 except `beta1 = 0` (no first moment; second-moment scaling
kept). Six runs.
- *Prediction (committed):* the massed penalty **persists**. Under Adam, identical
  consecutive gradients give the same normalised step whether or not momentum is on;
  momentum only carries a decaying fraction of the fact gradient into the next few
  filler steps. I expect retention Δ(spaced − massed) at beta1=0 to stay above the
  seed spread and above half of Study 1's Δ.
- *Decision rule:* momentum is called a **major part of the mechanism** if mean
  Δ(beta1=0) < 0.5 × Δ(Study 1) **and** massed immediate accuracy rises above 0.30.
  Otherwise momentum is **not the main mechanism**. Anything in between is reported
  as partial.
- *Traps:* beta1=0 changes the effective optimiser for both conditions, so absolute
  levels may shift; only the paired difference is read. Same steps/tokens guards.

**2b. Does it hold under LoRA?** Most practical fine-tuning is parameter-efficient.
Test: massed vs spaced, seeds 0–2, LoRA rank 16 (alpha 32, on c_attn, c_proj, c_fc;
2.36M trainable params), full model frozen otherwise. Six runs.
- *Pilot first (calibration only):* random placement, seed 100, K=5, interference 400
  steps, lr ∈ {3e-4, 1e-3}. Selection rule as in the original pilot: lowest lr with
  immediate accuracy in [0.5, 0.95] and accuracy at step 400 ≥ 0.10; if none
  qualifies, the lr whose immediate accuracy is closest to 0.7. The chosen lr is
  recorded below before the six runs start. Pilot numbers are not results.
- *Prediction (committed):* same direction — spaced > massed retention in every seed
  by more than the seed spread. I am unsure of the size; low-rank updates may make
  massed encoding even more fragile (fewer directions to spread over) or less (a
  smaller update cannot overshoot as far). No prediction on magnitude.
- *Decision rule:* rules 1–2 of the original decision rule, applied to the LoRA
  pair. Rule 3 is reported but, given Study 1, not used to gate the conclusion; the
  Amendment 4 encoding guard and conditional retention are reported alongside.

**2c. Contingency runs (already running, declared here for completeness).**
massed, seed 0, K ∈ {10, 20}. *Prediction:* massed immediate accuracy stays below
0.30 even at K=20, i.e. a learning-matched massed control is not reachable by adding
consecutive exposures. If it *is* reached (immediate within 0.05 of spaced's 0.66),
its retention is compared to spaced as the contingency says. Note K changes fact
tokens seen, so this control is a post-hoc probe, not a matched comparison.

Scope of Study 2: same model, facts, filler, interference and window as Study 1.

**2d. Does diversity substitute for spacing? (added 2026-09-05, before any 2d number)**
Human "encoding variability" accounts say part of the spacing benefit comes from each
repetition arriving in a different context. The model analogue is paraphrase: the five
exposures are five *different* sentences stating the same fact (variant 0 is the
canonical sentence, the one used at evaluation; variants 1–4 are answer-final
rewrites; exposure j in time uses variant j, so the canonical form is seen first and
only once). Two conditions, seeds 0–2, six runs: `massed+para` and `spaced+para`,
compared with Study 1's `massed` and `spaced` of the same seed (same p_i, same filler).
- *Prediction (committed):* `massed+para` retention > `massed` in every seed (diversity
  helps even when consecutive), but `massed+para` < `spaced` (temporal spacing does
  something diversity does not). For `spaced+para` vs `spaced` I predict a small gain
  or none; the eval-form handicap (canonical seen once instead of five times) works
  against it.
- *Decision rule:* "diversity partially substitutes" if massed+para − massed > seed
  spread in every seed and massed+para < spaced − spread; "fully substitutes" if
  massed+para ≥ spaced − spread; "no substitution" otherwise. Additivity: spaced+para
  − spaced > spread in every seed.
- *Traps:* paraphrases have slightly different token counts (fact tokens seen differs
  by a few percent; logged). The evaluation prompt is the canonical form, so any
  paraphrase condition is handicapped on exact match; NLL reported alongside. This is a
  confound *against* the prediction, not for it.

**Amendment 5b (2026-09-05, during the LoRA pilot, before any 2b main run).** The two
pre-declared pilot learning rates both floor: lr 3e-4 gives immediate accuracy 0.025,
lr 1e-3 gives 0.085 (random placement, seed 100). Neither meets the [0.5, 0.95] target,
and running the main LoRA comparison there would be a floor effect. The pilot grid is
extended upward to {3e-3, 1e-2}; the selection rule is unchanged (lowest lr with
immediate in [0.5, 0.95] and acc@400 ≥ 0.10, else closest to 0.7). Nothing else changes.

**Amendment 5c (2026-09-05, still before any 2b main run).** The extended grid also
floors: lr 3e-3 gives immediate 0.11 with held-out loss starting to degrade (3.87 vs
3.60), and 0.00 at interference step 400; lr 1e-2 result pending. Rank 16 appears to be
the limit, not the learning rate. One more pilot is added: rank 64 (alpha 128) at
lr 1e-3. Selection then runs over all LoRA pilots (lr and rank), same rule. If nothing
reaches immediate ≥ 0.5, the main 2b runs still go ahead at the pilot closest to 0.7 and
2b is reported as a **floor-effect comparison**: only the ordering massed vs spaced can
be read, not the size.

### Amendment 6 (2026-09-05, Study 3: is the massed memory erased or hidden? Written before any Study 3 number)
**Why.** Study 1 and 2 read exact-match accuracy first and NLL second. Two objections
(raised by an outside reader) are fair: (i) massed's NLL at the end (4.3–5.2) is far below
the pretrained 8.7, so *something* was retained, but part of that is the model learning
the *format* ("the answer is an invented name"), which NLL on the true answer cannot
separate from knowledge of *this* answer; (ii) a memory can be gone at the output and
still present inside the weights ("representational" rather than output forgetting). The
human-memory literature's classic test for (ii) is Ebbinghaus's **savings**: relearning
is faster than first learning if a trace remains.

**Two added measurements, no change to training before the end of interference.**
- *Discrimination* at every evaluation: NLL(foil answer) − NLL(true answer), where the
  foil is the answer of another fact with the same template (a derangement within
  template groups, fixed per seed). Both are invented names of the same style, so the
  format contribution cancels. >0 means the model prefers *this* fact's answer.
  Sanity: pretrained discrimination must be ≈ 0.
- *Savings* after the last interference evaluation: 10 extra steps in which every one of
  the 200 old facts and every one of 200 **never-seen control facts** (same generator,
  same templates) is shown exactly once (20 + 20 per step on top of filler), then both
  sets are evaluated. Savings = (after − before) for old facts, compared with the same
  for controls, which start at 0.

**Runs.** massed and spaced, seeds 0–2, otherwise identical to Study 1 (6 runs). Every
Study 1 metric is recomputed on these runs, which also acts as a second replication.

**Predictions (committed).**
1. Discrimination at the end of interference: massed > 0 in every seed (a trace exists
   at the representation level even where exact match is 0), and spaced > massed in
   every seed.
2. Savings in accuracy after one re-exposure: massed old facts > control facts by more
   than the seed spread in every seed (the memory is hidden, not erased). Spaced's
   savings are larger than massed's in absolute accuracy.
3. Discrimination and NLL move together; if discrimination is ≈ 0 while NLL is well below
   pretrained, the NLL drop was format, and I will say so.

**Decision rule.** "Hidden, not erased" for massed if *both* (1) massed discrimination
> 0 in 3/3 seeds and (2) massed savings − control savings > 0.05 accuracy in 3/3 seeds.
"Erased at every level we can see" if discrimination is within ±0.1 of 0 and savings are
within 0.05 of control. Anything else is reported as partial.

**Traps.** The relearning step uses the same lr and optimizer state as the end of
interference for both old and control facts, so neither set is favoured. Control facts
never appeared anywhere before; the "old" set's answers were foils for each other, which
applies equally to spaced. Discrimination uses teacher forcing; a foil that happens to
be a substring-prefix match could inflate it, but all names are ≥ 5 characters and unique.

### Amendment 7 (2026-09-05, Study 4: the fair paraphrase probe; written before any Study 4 number)
**Why.** Study 2d probed every condition with the canonical sentence, which the copy
conditions saw five times and the paraphrase conditions once. That confound alone could
produce 2d's result. Study 4 adds a probe through a **sixth wording per template that no
condition ever saw** (`facts.HELDOUT`), evaluated at every checkpoint next to the canonical
probe. Training is unchanged. Four conditions × seeds 0–2 = 12 runs: massed, spaced,
massed+para, spaced+para. The canonical-probe numbers of these runs should reproduce
Study 1 / 2d within the noise band (a third replication for free).

**Predictions (committed).**
1. On the unseen wording, every condition scores lower than on its canonical probe.
2. spaced+para > spaced on the unseen wording, in every seed, by more than the Study 1
   seed spread (0.041): five wordings teach the *fact*, five copies teach the *sentence*.
3. massed+para stays ≈ 0 on the unseen wording (nothing to generalise from).
4. Discrimination on the unseen wording follows the same ordering as accuracy.

**Decision rule.** "Diversity buys generalisation" if (2) holds in 3/3 seeds. "Diversity
does not help even when probed fairly" if spaced+para ≤ spaced + spread on the unseen
wording in ≥ 2 seeds. Otherwise partial. Prediction 3 is a guard, not a gate.

**Traps.** The sixth wording is longer and less template-like than the five training
wordings; that lowers absolute numbers for everyone but not the paired comparison. Noise
band and guards as before.

### Amendment 8 (2026-09-05, Study 5: where does the benefit stop? Written before any Study 5 number)
**Why.** Studies 1–4 tested gaps up to 64 inside a 700-step window. The human lag-effect
literature (Cepeda et al. 2008) finds an inverted U: more spacing helps, then hurts, and
the optimum shifts with the retention interval. Whether gap 64 is on the rising limb or
past the peak is unknown.

**Design.** Injection window **1,400 steps** (so that four gaps of 256 plus a 350-step
range for the last-exposure draw fit), everything else as Study 1: 200 facts, K = 5,
lr 1e-4, 100 pre-steps, 1,500 interference steps with 50 new facts. Conditions: gap
∈ {1, 16, 64, 128, 256}, seeds 0–2, **15 runs**, seed-major order so each seed yields a
full curve. Gap 4 is dropped (Study 1: indistinguishable from gap 1). Because the window
doubled, exposure density halves and *all* gaps are re-run in the new window; Study 1
numbers are not compared across windows.

**Predictions (committed).**
1. Ordering 1 < 16 < 64 in every seed, as before.
2. retention(128) > retention(64) in every seed (still on the rising limb at 64).
3. Diminishing returns: retention(256) − retention(128) < retention(128) − retention(64),
   in every seed. No prediction on the sign of the 256 − 128 difference.
4. Guard: massed still decays to ≈ 0 by the end of the window; if the longer window
   changes that, it is reported as a window effect.

**Decision rule.** With Δ = retention(256) − retention(128), paired per seed and the
Study 1 spread (0.041): "keeps rising" if Δ > spread in 3/3; "saturates" if |Δ| ≤ spread
in ≥ 2 seeds; "declines" if Δ < −spread in 3/3. Prediction 2 is read the same way.

**Traps.** The largest gaps place a fact's first exposure up to 1,024 steps before its
last, i.e. early in the window when fewer other facts are being trained: an exposure
then may be "cleaner". This is inherent to gap manipulation and was also true in Study 1
(gap 64 vs 1). It is noted, not controlled. Guards as before.
