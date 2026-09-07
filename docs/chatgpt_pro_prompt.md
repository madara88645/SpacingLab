# Prompt for ChatGPT Pro (deep reasoning). Paste everything below the line.

---

You are acting as a senior reviewer and research advisor for a small, finished-for-now
machine-learning research project. I want a rigorous, sceptical, comprehensive assessment
plus a concrete plan, and then an infographic that explains the whole thing to a
first-year student. Take your time; reason at length before answering. Do not flatter
me. If something is weak, say so and say why.

## Who I am and how to write for me

I am Mehmet, a first-year AI & Data Science student (Bournemouth University). I follow
reasoning well but lose the thread when findings arrive as dense prose. Rules for every
part of your answer:
- Write the report in **Turkish**, plain language. Every technical term is explained
  in the same sentence the first time it appears (e.g. "NLL, yani modelin doğru cevaba
  ne kadar şaşırdığını ölçen sayı").
- Lead every section with the conclusion in one sentence, then the reasoning.
- Short paragraphs, tables where numbers are compared, no unexplained jargon.
- Where you are unsure, say "emin değilim" and say what would settle it.
- I do not want a "scientific breakthrough" narrative. I want to know exactly what this
  project has established, what it has not, and what the most valuable next step is.

## The project: SpacingLab

**Niche.** Memory-consolidation phenomena from human learning (spacing effect, lag
effect, savings, encoding variability) applied to how a small language model retains and
loses injected facts during fine-tuning.

**The one question.** When a small pretrained language model is fine-tuned to absorb
new facts, each shown K = 5 times, does spreading a fact's five exposures apart in
training time (other data in between) rather than presenting them in consecutive steps
improve how well the fact survives subsequent fine-tuning on unrelated text, with
everything else held equal: total exposures, total gradient steps, total tokens, the
other data seen, and the time since the fact's last exposure?

**Setup (identical across all conditions of a seed).**
- Model: GPT-2 124M, full fine-tuning, AdamW lr 1e-4, betas (0.9, 0.999), no weight
  decay, dropout off, grad-clip 1.0, on an Apple-Silicon laptop (MPS).
- Facts: 200 synthetic single-sentence paired associates with invented names from five
  templates ("The capital of Sheipiakvuk is Prothkunshend."), so the pretrained model
  scores exactly 0. Each seed draws its own facts.
- Every optimizer step trains on 15 chunks of 64 tokens of WikiText-103 filler; on
  steps where a fact is scheduled, its sentence is added to that step's batch.
- Phases: 100 warm-up steps of filler only → 700-step "injection window" in which each
  fact is shown 5 times → 1,500 steps of interference: filler plus 50 *new* facts of
  the same kind (classic learn-A-then-B).
- The only manipulated variable: the **gap** between a fact's five exposures: 1 step
  (massed), 4, 16, 64 (spaced). Each fact's **last** exposure step is drawn once per
  seed and shared by all conditions, so time-since-last-exposure is identical.
- Measures: exact-match accuracy (greedy decode of the answer) and answer NLL, at the
  end of the window ("immediate") and at interference steps 50, 100, 200, 400, 800,
  1200, 1500. Primary outcome: **retention score** = mean accuracy over those seven
  checkpoints. Added later: accuracy right after each fact's own last exposure;
  discrimination = NLL(foil answer) − NLL(true answer) with a same-template foil;
  a held-out sixth wording probe; a savings (relearning) test.
- Seeds: 5 for massed vs spaced, 3 for everything else; one replicate run for the
  nondeterminism noise band (0.014 in retention). Guards logged: steps, fact tokens,
  filler tokens, pre-injection accuracy (always 0), weight displacement, held-out
  filler loss.
- **Pre-registration.** Design, metrics, predictions, decision rules and named traps
  were committed to git before any number existed; eight dated amendments record every
  change and the pilot numbers that forced it. Every study below was predicted in
  writing before its runs.

**Study 1 (17 runs).** Retention score, mean (min..max over seeds):
massed 0.001 (0.000..0.001); gap 4 0.023; gap 16 0.124; spaced/gap 64 0.285
(0.241..0.351). Paired spaced − massed = +0.29, seed SD 0.04, positive in 5/5 seeds,
monotone in gap in every seed. End-of-window accuracy: massed 0.03, gap 4 0.08, gap 16
0.35, spaced 0.65. Accuracy after 1,500 interference steps: 0.00 / 0.01 / 0.05 / 0.14.
BUT the pre-registered decision rule had a third clause, "the immediate difference must
be smaller than the retention difference" (to catch "spaced simply learned more"). It
fired (+0.62 vs +0.29), so **H1 as pre-registered is not supported**, and three of four
conditions violate the pre-declared calibration band [0.5, 0.95] for immediate accuracy;
this is reported as a calibration failure, nothing was re-tuned. The probe added before
the main runs (accuracy right after each fact's own last exposure) shows massed facts
*are* encoded (0.43 right after the fifth consecutive step; spaced 0.81; gaps 4 and 16
0.94–0.96) and are gone within ~50 steps: of massed facts correct at that moment, 6 %
are still correct at the end of the window vs 77 % for spaced. Restricting to strongly
encoded facts (NLL < 0.1) changes nothing: 9.5 % survive vs 93 %. The massed model
produces invented-looking names of the right kind but not the associated one: it learned
the format and lost the item.

**Study 2 (20 runs + 5 pilots), four pre-registered follow-ups.**
- 2c: massed with K = 10 and 20 exposures (seed 0): 0.99 right after the last exposure,
  0.025 / 0.06 at the end of the window. More consecutive repeats do not help.
- 2a: Adam with beta1 = 0 (no momentum), 3 seeds: spaced − massed retention +0.30
  (+0.33, +0.28, +0.30), unchanged from Study 1. Momentum is not the mechanism; it only
  weakened massed *encoding* (massed now encodes 0.95–0.98 at last exposure and still
  ends the window at 0.06–0.08).
- 2b: LoRA. Calibration failed: rank 16/64, lr 3e-4..1e-2, best immediate 0.245 with
  random placement. At rank 64 / lr 1e-3: end-of-window 0.31 (spaced) vs 0.015 (massed)
  in every seed, but both reach 0.00 by interference step 800–1500. Ordering replicates;
  retention comparison is a floor effect and no size is read.
- 2d: five paraphrases instead of five copies. Prediction ("diversity partially
  substitutes for spacing") failed: massed+para − massed = +0.002; spaced+para − spaced
  = −0.20 on the canonical probe. Confounded by the probe (see Study 4).

**Study 3 (6 runs): erased or hidden?** Discrimination (foil-based, format cancels;
pretrained model scores +0.05) after 1,500 interference steps: massed +0.24..+0.46,
spaced +2.06..+2.60. Of massed's 3.5-nat NLL drop from pretrained, 3.15 nats also apply
to the foil, i.e. **90 % of massed's NLL improvement is format learning, not
knowledge**. Savings (Ebbinghaus): one re-exposure of every old fact plus one exposure
of 200 never-seen controls; massed old facts 0 → 0 accuracy in all 3 seeds (controls
0 → 0); spaced +0.105, +0.240, +0.200. Verdict per pre-declared rule: partial; a small
item-specific residue exists but relearning cannot use it.

**Study 4 (12 runs): the fair paraphrase probe.** Every condition also probed through an
unseen sixth wording. Retention on the unseen wording: spaced (copies) 0.060, spaced+para
0.108; on the canonical wording 0.306 vs 0.092. End-of-window: copies 0.667 canonical /
0.275 unseen (40-point drop); paraphrases 0.348 / 0.365 (no drop). spaced+para − spaced
on unseen-wording retention: +0.056, +0.043, +0.044 vs a 0.041 threshold: rule passes
by a hair; wider margins at end-of-window (+0.055, +0.080, +0.135) and in discrimination
(+0.27, +0.18, +0.18). Corrected reading of 2d: copies buy the trained sentence,
paraphrases buy the fact; neither rescues consecutive exposures. The canonical numbers of
these 12 runs replicate Studies 1 and 2d to within 0.01.

**Study 5 (15 runs): where does the benefit stop?** Window doubled to 1,400 steps, gaps
{1, 16, 64, 128, 256}, all re-run. Retention by seed (gap 1 / 16 / 64 / 128 / 256):
seed 0: 0.004 / 0.171 / 0.366 / 0.280 / 0.296; seed 1: 0.000 / 0.108 / 0.194 / 0.274 /
0.222; seed 2: 0.002 / (pending) / 0.224 / 0.161 / (pending). Prediction "128 > 64"
failed (below in 2 of 3 seeds). Plateau from 64; seed-to-seed wobble at the plateau
(0.19–0.37 for gap 64 alone) exceeds gap-to-gap differences. Encoding right after the
last exposure weakens at large gaps (0.84 → 0.61 → 0.58 in seed 0), the shape of the
human lag effect.

**Literature position (two research agents, URLs checked).** No prior work found that
varies only the step gap between repeats of one fact with everything else matched.
Closest: Chang et al. 2024 (NeurIPS) find duplicated injections forget faster than
paraphrased ones, without manipulating the gap; Allen-Zhu & Li (Physics of LMs 3.1) on
paraphrase augmentation for extractability; arXiv:2507.14198 on retention of edited
knowledge; corpus-level repetition work (Hernandez 2022, Muennighoff 2023); recent
"spacing in ANNs" papers about generalisation (Sun et al. 2025 arXiv:2502.06192; a
Patterns 2026 paper). Human side: Cepeda et al. 2006 meta-analysis; Cepeda et al. 2008
ridgeline (optimal gap ≈ 5–40 % of retention interval, inverted U); expanding vs equal
intervals roughly a wash (Karpicke & Roediger 2007; Kang et al. 2014).

**Scope, stated honestly.** One model (GPT-2 124M), one fact format, one filler and
interference corpus (WikiText-103), one lr, K = 5, two window lengths, one interference
length. The mechanism of the massed decay is unknown: not momentum, not lack of
encoding, not recoverable by one re-exposure. Two candidate mechanisms not yet tested:
(a) sharpness — five identical consecutive steps land in a narrow region that the next
filler steps leave; (b) the other 199 facts' updates overwrite it (testable by injecting
a fact alone / at 10× lower density).

**Constraints for any next step.** Apple-Silicon laptop, 24 GB, no GPU cluster; one
run of the current protocol ≈ 9–12 minutes; a 3-seed, 2-condition experiment ≈ 1 hour.
The repo is private, uses uv, has 70 runs logged with per-fact evaluations.

## What I want from you

Produce, in this order, in Turkish (except code/identifiers):

1. **Tek paragraf özet** (5–6 cümle): bu proje ne buldu, ne bulmadı.
2. **Sert bir hakem değerlendirmesi.** What would a NeurIPS/ICLR reviewer or a careful
   cognitive scientist attack first? List the five most damaging objections, each with
   (i) why it matters, (ii) whether the existing data already answer it, (iii) if not,
   the cheapest experiment that would. Include alternative explanations for the massed
   decay that I have not listed.
3. **Yenilik değerlendirmesi.** What here is genuinely new relative to the literature you
   know (cite; say when you are unsure a paper exists), what is a rediscovery, and what
   is merely consistent with known results. Be specific about Chang et al. 2024 and
   about the "spacing in neural networks" line.
4. **Mekanizma.** Give your best two or three mechanistic hypotheses for why five
   consecutive identical gradient steps produce a trace that decays within ~50 steps
   while the same five steps 64 apart do not, given that momentum is ruled out and
   encoding is strong. For each, a concrete measurement on this setup (loss-landscape
   sharpness along the update direction, gradient alignment between the fact update and
   subsequent filler updates, per-layer displacement, etc.) with an estimate of how
   many runs it costs on this laptop.
5. **Sıradaki adımlar, önceliklendirilmiş.** A ranked list of 5–8 next experiments with,
   for each: the question, the pre-registrable prediction, the decision rule, the run
   count and laptop hours, and what result would make me stop. Mark which ones would
   change the practical recommendation ("keep repeats ≥ 16, ideally 64 steps apart") and
   which are only scientifically interesting.
6. **Pratik değer.** For whom is this useful today (people injecting knowledge by
   fine-tuning, continual-learning practitioners, data-pipeline authors), what concrete
   recommendation is defensible now, and what would need to be true (model scale, real
   facts, LoRA calibration) before it is defensible more broadly.
7. **Yayın / paylaşım potansiyeli.** Is this a workshop paper, a blog post, a negative-
   results venue entry, or nothing yet? Name venues. State what is missing for each.
   Be blunt.
8. **Benim için öğrenme haritası.** The five concepts I most need to understand deeply
   to own this project (e.g. Adam's update rule, sharpness/flat minima, catastrophic
   interference, the spacing/lag literature), each with a one-paragraph plain
   explanation and one exercise I can do on this laptop.
9. **İnfografik.** Generate an image: a single-page infographic in Turkish, clean and
   simple, for a first-year student. It must contain: (a) the setup as a timeline
   (ısınma → öğretme penceresi → unutturma), (b) the core result as one chart (retention
   vs gap: 0.001, 0.023, 0.124, 0.285 for gaps 1/4/16/64, plateau at 128/256), (c) the
   "öğrendi ama 50 adımda sildi" point (0.43 right after the last exposure → 0.03 at
   the window end, vs 0.81 → 0.65 for spaced), (d) a four-row "what did NOT rescue
   massed" strip (daha çok tekrar / momentum kapalı / LoRA / farklı cümleler), (e) the
   Study 4 trade ("kopya cümleyi öğretir, farklı cümle bilgiyi öğretir"), (f) one line
   of practical advice. Also output the infographic's full text content as a list so I
   can check it against the numbers above. No invented numbers: use only those given.

Before answering, list any numbers or claims in my description that look internally
inconsistent to you, and ask nothing: make your best reading explicit and proceed.
