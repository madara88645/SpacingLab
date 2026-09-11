"""One run: pre-phase -> injection window (facts placed by schedule) -> interference.

Matched comparisons require the same immutable filler snapshot, not just a seed.
"""
from __future__ import annotations

import json
import math
import subprocess
import time
import warnings
from importlib.metadata import version
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from .data import FillerStream, build_filler_tokens, load_filler_snapshot, token_digest
from .facts import TEMPLATES, Fact, heldout_fact, make_facts, paraphrases
from .schedule import draw_last_exposures, exposure_count, gap_schedule, random_schedule, matched_random_schedule, permuted_gap_schedule

GAPS = {"massed": 1, "gap4": 4, "gap16": 16, "spaced": 64, "gap128": 128, "gap256": 256}
GAP_MAX = 64


@dataclass
class Config:
    condition: str            # massed | gap4 | gap16 | spaced | random (pilot only)
    seed: int
    lr: float = 1e-4
    k: int = 5                # exposures per fact
    n_facts: int = 200
    model_name: str = "gpt2"
    seq_len: int = 64
    filler_per_step: int = 15
    t_pre: int = 100
    t_inj: int = 600
    t_int: int = 1500
    warmup: int = 50
    eval_int_steps: tuple[int, ...] = (50, 100, 200, 400, 800, 1200, 1500)
    device: str = "mps"
    tag: str = ""             # free label, e.g. "pilot" or "replicate"
    max_facts_per_step: int = 64
    # interference phase content (Amendment 1): filler plus a new set of facts
    n_int_facts: int = 50
    k_int: int = 4
    # Study 2 (Amendment 5) knobs; defaults reproduce Study 1 exactly
    beta1: float = 0.9        # Adam first-moment coefficient; 0.0 removes momentum
    lora_r: int = 0           # 0 = full fine-tuning; >0 = LoRA with this rank
    k_last: int = 0           # k used to draw the last-exposure steps p_i; 0 = same as k
    paraphrase: bool = False  # Study 2d: exposure j of a fact uses paraphrase variant j % 5
    heldout_probe: bool = False  # Study 4: also probe every fact through an unseen sixth wording
    gap_max: int = GAP_MAX    # Study 5: largest gap the shared last-exposure draw must accommodate
    relearn: bool = False     # Study 3: after interference, 1 exposure of every old fact + 1 of each new control fact
    relearn_steps: int = 10
    filler_snapshot: str = ""  # new comparisons must supply a snapshot AND its file hash
    filler_sha256: str = ""
    model_revision: str = ""
    offline: bool = False
    collect_step_guards: bool = False


def schedule_last_exposures(sched: dict, n_facts: int) -> np.ndarray:
    last = np.full(n_facts, -1, dtype=int)
    for step, ids in sched.items():
        for i in ids:
            last[i] = max(last[i], step)
    if np.any(last < 0):
        raise ValueError("Schedule missing a target fact")
    return last


def training_step_guard(step: int, filler: int, targets: int, interference: int, norm: float) -> dict:
    if not math.isfinite(norm):
        raise ValueError(f"Nonfinite pre-clipping norm at step {step}")
    coefficient = targets / (filler + targets + interference)
    scale = min(1.0, 1.0 / (norm + 1e-6))
    return {"step": step, "targets": targets, "interference": interference,
            "preclip_norm": norm, "clip_scale": scale,
            "target_coefficient_sum": coefficient,
            "clipped_target_coefficient_sum": coefficient * scale}


def per_sequence_mean_loss(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    """Mean CE over each sequence's label tokens, then mean over sequences."""
    shift_logits = logits[:, :-1].float()
    shift_labels = labels[:, 1:]
    tok_loss = F.cross_entropy(
        shift_logits.reshape(-1, shift_logits.size(-1)), shift_labels.reshape(-1),
        ignore_index=-100, reduction="none",
    ).view(shift_labels.shape)
    mask = (shift_labels != -100).float()
    seq_loss = (tok_loss * mask).sum(1) / mask.sum(1).clamp(min=1)
    return seq_loss.mean()


class Evaluator:
    def __init__(self, tok, facts: list[Fact], device: str):
        self.tok, self.facts, self.device = tok, facts, device
        eos = tok.eos_token_id
        self.prompt_ids, self.answer_ids = [], []
        for f in facts:
            p = [eos] + tok(f.prompt)["input_ids"]
            a = tok(f.answer)["input_ids"]
            full = [eos] + tok(f.text)["input_ids"]
            dot = tok(".")["input_ids"]
            assert full == p + a + dot, (f.text, p, a, dot, full)
            self.prompt_ids.append(p)
            self.answer_ids.append(a)
        self.max_ans = max(len(a) for a in self.answer_ids)
        # Study 3: foil answer = the answer of the next fact with the same template (a
        # derangement within template groups), so foil and true answer share format.
        n_t = len(TEMPLATES)
        groups: dict[int, list[int]] = {}
        for i, f in enumerate(facts):
            groups.setdefault(f.idx % n_t, []).append(i)
        self.foil_of = list(range(len(facts)))
        for g in groups.values():
            if len(g) > 1:
                for k, i in enumerate(g):
                    self.foil_of[i] = g[(k + 1) % len(g)]
        self.foil_ids = [self.answer_ids[self.foil_of[i]] for i in range(len(facts))]
        # left-padded prompt batch for generation
        maxp = max(len(p) for p in self.prompt_ids)
        self.gen_ids = torch.full((len(facts), maxp), eos, dtype=torch.long)
        self.gen_mask = torch.zeros((len(facts), maxp), dtype=torch.long)
        for i, p in enumerate(self.prompt_ids):
            self.gen_ids[i, maxp - len(p):] = torch.tensor(p)
            self.gen_mask[i, maxp - len(p):] = 1
        # right-padded prompt+answer batch for teacher forcing, labels only on answer
        maxl = max(len(p) + len(a) for p, a in zip(self.prompt_ids, self.answer_ids))
        self.tf_ids = torch.full((len(facts), maxl), eos, dtype=torch.long)
        self.tf_labels = torch.full((len(facts), maxl), -100, dtype=torch.long)
        for i, (p, a) in enumerate(zip(self.prompt_ids, self.answer_ids)):
            self.tf_ids[i, : len(p) + len(a)] = torch.tensor(p + a)
            self.tf_labels[i, len(p) : len(p) + len(a)] = torch.tensor(a)
        maxf = max(len(p) + len(a) for p, a in zip(self.prompt_ids, self.foil_ids))
        self.foil_tf_ids = torch.full((len(facts), maxf), eos, dtype=torch.long)
        self.foil_tf_labels = torch.full((len(facts), maxf), -100, dtype=torch.long)
        for i, (p, a) in enumerate(zip(self.prompt_ids, self.foil_ids)):
            self.foil_tf_ids[i, : len(p) + len(a)] = torch.tensor(p + a)
            self.foil_tf_labels[i, len(p) : len(p) + len(a)] = torch.tensor(a)

    def _nll(self, model, ids, labels):
        logits = model(input_ids=ids.to(self.device)).logits[:, :-1].float()
        labels = labels[:, 1:].to(self.device)
        tok_loss = F.cross_entropy(
            logits.reshape(-1, logits.size(-1)), labels.reshape(-1), ignore_index=-100, reduction="none"
        ).view(labels.shape)
        mask = (labels != -100).float()
        return ((tok_loss * mask).sum(1) / mask.sum(1)).cpu().tolist()

    @torch.no_grad()
    def __call__(self, model, idxs: list[int] | None = None) -> dict:
        """Evaluate all facts, or only the facts in `idxs` (used right after a fact's last exposure)."""
        model.eval()
        dev = self.device
        sel = slice(None) if idxs is None else torch.tensor(idxs)
        tf_ids, tf_labels = self.tf_ids[sel], self.tf_labels[sel]
        gen_ids, gen_mask = self.gen_ids[sel], self.gen_mask[sel]
        answer_ids = self.answer_ids if idxs is None else [self.answer_ids[i] for i in idxs]
        # teacher-forced answer NLL per fact, and the same for the foil answer
        nll = self._nll(model, tf_ids, tf_labels)
        nll_foil = self._nll(model, self.foil_tf_ids[sel], self.foil_tf_labels[sel])
        disc = [b - a for a, b in zip(nll, nll_foil)]   # >0: true answer more likely than foil
        # greedy exact match
        out = model.generate(
            input_ids=gen_ids.to(dev), attention_mask=gen_mask.to(dev),
            max_new_tokens=self.max_ans, do_sample=False, pad_token_id=self.tok.eos_token_id,
        )
        gen = out[:, gen_ids.size(1):].cpu()
        correct = [gen[i, : len(a)].tolist() == a for i, a in enumerate(answer_ids)]
        generated = [self.tok.decode(gen[i, : len(a)]) for i, a in enumerate(answer_ids)]
        model.train()
        return {
            "acc": float(np.mean(correct)),
            "nll": float(np.mean(nll)),
            "nll_foil": float(np.mean(nll_foil)),
            "disc": float(np.mean(disc)),
            "disc_frac": float(np.mean([d > 0 for d in disc])),
            "per_fact_correct": [int(c) for c in correct],
            "per_fact_nll": nll,
            "per_fact_nll_foil": nll_foil,
            "per_fact_generated": generated,
        }


@torch.no_grad()
def holdout_loss(model, holdout: torch.Tensor, device: str, bs: int = 50) -> float:
    model.eval()
    losses = []
    for i in range(0, len(holdout), bs):
        x = holdout[i : i + bs].to(device)
        losses.append(per_sequence_mean_loss(model(input_ids=x).logits, x).item())
    model.train()
    return float(np.mean(losses))


@torch.no_grad()
def param_distance(model, theta0: list[torch.Tensor]) -> float:
    params = [p for p in model.parameters() if p.requires_grad]
    return math.sqrt(sum(((p - q) ** 2).sum().item() for p, q in zip(params, theta0)))


def relearn(cfg, model, opt, stream, tok, old_eval, ctrl_facts, dev, log) -> None:
    """Study 3 savings test. One exposure of every old fact and of every never-seen control
    fact, interleaved over `relearn_steps` steps on top of filler; evaluate both sets
    before and after. Training computation before this point is untouched."""
    ctrl_eval = Evaluator(tok, ctrl_facts, dev)
    eos = tok.eos_token_id
    old_ids = [[eos] + tok(f.text)["input_ids"] for f in old_eval.facts]
    new_ids = [[eos] + tok(f.text)["input_ids"] for f in ctrl_facts]
    rng = np.random.default_rng(cfg.seed + 20_000)
    order_old, order_new = rng.permutation(len(old_ids)), rng.permutation(len(new_ids))
    per = math.ceil(len(old_ids) / cfg.relearn_steps)
    before_old, before_new = old_eval(model), ctrl_eval(model)
    for k in range(cfg.relearn_steps):
        x = stream.take(cfg.filler_per_step)
        labels = x.clone()
        rows = [old_ids[i] for i in order_old[k * per:(k + 1) * per]] + [new_ids[i] for i in order_new[k * per:(k + 1) * per]]
        fx = torch.full((len(rows), cfg.seq_len), eos, dtype=torch.long)
        fl = torch.full((len(rows), cfg.seq_len), -100, dtype=torch.long)
        for r, ids in enumerate(rows):
            fx[r, : len(ids)] = torch.tensor(ids); fl[r, : len(ids)] = torch.tensor(ids)
        x, labels = torch.cat([x, fx]).to(dev), torch.cat([labels, fl]).to(dev)
        loss = per_sequence_mean_loss(model(input_ids=x).logits, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); opt.zero_grad(set_to_none=True)
    after_old, after_new = old_eval(model), ctrl_eval(model)
    strip = lambda r: {k: v for k, v in r.items() if not k.startswith("per_fact")}
    log["relearn"] = {"before_old": strip(before_old), "before_new": strip(before_new),
                      "after_old": strip(after_old), "after_new": strip(after_new),
                      "per_fact_after_old": after_old["per_fact_correct"],
                      "per_fact_after_new": after_new["per_fact_correct"],
                      "steps": cfg.relearn_steps, "exposures_per_fact": 1}
    print(f"[relearn] old: acc {before_old['acc']:.3f}->{after_old['acc']:.3f} nll {before_old['nll']:.2f}->{after_old['nll']:.2f} disc {before_old['disc']:.2f}->{after_old['disc']:.2f}"
          f" | new: acc {before_new['acc']:.3f}->{after_new['acc']:.3f} nll {before_new['nll']:.2f}->{after_new['nll']:.2f} disc {before_new['disc']:.2f}->{after_new['disc']:.2f}", flush=True)


def run(cfg: Config, out_dir: Path) -> dict:
    if (out_dir / "log.json").exists():
        raise FileExistsError(f"Refusing to overwrite completed run: {out_dir}")
    if bool(cfg.filler_snapshot) != bool(cfg.filler_sha256):
        raise ValueError("filler_snapshot and filler_sha256 must be supplied together")
    total_steps = cfg.t_pre + cfg.t_inj + cfg.t_int
    n_filler = total_steps * cfg.filler_per_step
    required_tokens = (n_filler + 400) * cfg.seq_len
    tokens = None
    if cfg.filler_snapshot:
        tokens = load_filler_snapshot(cfg.filler_snapshot, cfg.filler_sha256, required_tokens)
    else:
        warnings.warn("Unpinned legacy filler cache: not suitable for matched cross-run claims", stacklevel=2)
    out_dir.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(cfg.seed)
    dev = cfg.device
    load_kwargs = {"local_files_only": cfg.offline}
    if cfg.model_revision:
        load_kwargs["revision"] = cfg.model_revision
    tok = AutoTokenizer.from_pretrained(cfg.model_name, **load_kwargs)
    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name, resid_pdrop=0.0, embd_pdrop=0.0, attn_pdrop=0.0, **load_kwargs
    ).to(dev)
    if cfg.lora_r > 0:
        from peft import LoraConfig, get_peft_model
        model = get_peft_model(model, LoraConfig(
            r=cfg.lora_r, lora_alpha=2 * cfg.lora_r, lora_dropout=0.0, bias="none",
            target_modules=["c_attn", "c_proj", "c_fc"], fan_in_fan_out=True, task_type="CAUSAL_LM",
        ))
        n_tr = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"[lora] rank={cfg.lora_r} trainable params={n_tr:,}", flush=True)
    model.train()
    theta0 = [p.detach().clone() for p in model.parameters() if p.requires_grad]

    n_ctrl = cfg.n_facts if cfg.relearn else 0
    all_facts = make_facts(cfg.n_facts + cfg.n_int_facts + n_ctrl, cfg.seed)
    facts, int_facts = all_facts[: cfg.n_facts], all_facts[cfg.n_facts : cfg.n_facts + cfg.n_int_facts]
    ctrl_facts = all_facts[cfg.n_facts + cfg.n_int_facts :]
    evaluator = Evaluator(tok, facts, dev)
    int_evaluator = Evaluator(tok, int_facts, dev) if int_facts else None
    heldout_evaluator = Evaluator(tok, [heldout_fact(f) for f in facts], dev) if cfg.heldout_probe else None

    if tokens is None:
        tokens = build_filler_tokens(tok, n_tokens=required_tokens)
    stream = FillerStream(tokens, cfg.seq_len, seed=cfg.seed)
    provenance = stream.provenance(n_filler)
    provenance.update(snapshot_pinned=bool(cfg.filler_snapshot),
                      filler_file_sha256=cfg.filler_sha256 or None,
                      filler_tokens=len(tokens), filler_tokens_sha256=token_digest(tokens),
                      model_revision=getattr(model.config, "_commit_hash", None),
                      packages={p: version(p) for p in ("torch", "transformers", "numpy")})
    root = Path(__file__).resolve().parents[1]
    try:
        provenance["code_commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        provenance["tracked_code_dirty"] = bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=no", "--", "spacinglab", "uv.lock", "pyproject.toml"],
            cwd=root, text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        provenance["code_commit"] = None

    if cfg.condition == "random":
        sched = random_schedule(cfg.n_facts, cfg.k, cfg.t_inj, seed=cfg.seed)
        last = schedule_last_exposures(sched, cfg.n_facts) if cfg.collect_step_guards else None
    else:
        last = draw_last_exposures(cfg.n_facts, cfg.k_last or cfg.k, cfg.gap_max, cfg.t_inj, seed=cfg.seed)
        if cfg.condition == "random_matched":
            sched = matched_random_schedule(last, cfg.k, seed=cfg.seed + 30000)
        elif cfg.condition == "variable_gaps":
            sched = permuted_gap_schedule(last, cfg.k, seed=cfg.seed + 40000)
        else:
            sched = gap_schedule(last, cfg.k, GAPS[cfg.condition])
    assert exposure_count(sched) == cfg.n_facts * cfg.k
    assert max(len(v) for v in sched.values()) <= cfg.max_facts_per_step
    # interference facts: random placement over the interference phase, identical across
    # conditions of a seed (own rng stream so it never depends on the condition)
    int_sched = random_schedule(cfg.n_int_facts, cfg.k_int, cfg.t_int, seed=cfg.seed + 10_000) if int_facts else {}

    eos = tok.eos_token_id
    fact_ids = [[eos] + tok(f.text)["input_ids"] for f in facts]
    para_ids = [[[eos] + tok(t)["input_ids"] for t in paraphrases(f)] for f in facts] if cfg.paraphrase else None
    n_shown = [0] * len(facts)
    int_fact_ids = [[eos] + tok(f.text)["input_ids"] for f in int_facts]
    assert max(len(x) for x in fact_ids + int_fact_ids) <= cfg.seq_len

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=cfg.lr,
                            betas=(cfg.beta1, 0.999), weight_decay=0.0)

    log: dict = {"config": asdict(cfg), "provenance": provenance, "facts": [asdict(f) for f in facts],
                 "int_facts": [asdict(f) for f in int_facts],
                 "last_exposure": None if last is None else last.tolist(),
                 "evals": [], "train_loss": [], "guards": {}, "step_guards": [],
                 "interference_schedule": int_sched, "target_schedule": sched}

    def evaluate(phase: str, step: int, int_step: int | None = None):
        r = evaluator(model)
        if int_evaluator is not None:
            ri = int_evaluator(model)
            r.update(int_facts_acc=ri["acc"], int_facts_nll=ri["nll"])
        if heldout_evaluator is not None:
            rh = heldout_evaluator(model)
            r.update(heldout_acc=rh["acc"], heldout_nll=rh["nll"], heldout_disc=rh["disc"],
                     heldout_per_fact_correct=rh["per_fact_correct"], heldout_per_fact_nll=rh["per_fact_nll"])
        r.update(phase=phase, step=step, int_step=int_step,
                 holdout_loss=holdout_loss(model, stream.holdout, dev),
                 param_dist=param_distance(model, theta0))
        log["evals"].append(r)
        if cfg.collect_step_guards:
            partial = out_dir / "progress.json.tmp"
            partial.write_text(json.dumps(log, indent=1))
            partial.replace(out_dir / "progress.json")
        print(f"[eval] {phase:>10} step={step:5d} acc={r['acc']:.3f} nll={r['nll']:.3f} disc={r['disc']:.2f} "
              f"holdout={r['holdout_loss']:.3f} |dθ|={r['param_dist']:.2f}"
              + (f" B_acc={r['int_facts_acc']:.3f}" if int_evaluator else "")
              + (f" H_acc={r['heldout_acc']:.3f} H_nll={r['heldout_nll']:.2f} H_disc={r['heldout_disc']:.2f}" if heldout_evaluator else ""), flush=True)

    evaluate("pretrained", 0)
    at_last: dict[int, dict] = {}
    fact_tokens_seen = filler_tokens_seen = 0
    t0 = time.time()
    for step in range(total_steps):
        # learning rate: linear warmup inside the pre-phase, then constant
        lr = cfg.lr * min(1.0, (step + 1) / cfg.warmup)
        for g in opt.param_groups:
            g["lr"] = lr

        x = stream.take(cfg.filler_per_step)
        labels = x.clone()
        inj_step = step - cfg.t_pre
        shown = sched.get(inj_step, []) if 0 <= inj_step < cfg.t_inj else []
        int_step_now = step - cfg.t_pre - cfg.t_inj
        shown_int = int_sched.get(int_step_now, []) if int_step_now >= 0 else []
        if para_ids is None:
            rows = [fact_ids[i] for i in shown]
        else:
            rows = [para_ids[i][n_shown[i] % len(para_ids[i])] for i in shown]
            for i in shown:
                n_shown[i] += 1
        rows += [int_fact_ids[i] for i in shown_int]
        if rows:
            fx = torch.full((len(rows), cfg.seq_len), eos, dtype=torch.long)
            fl = torch.full((len(rows), cfg.seq_len), -100, dtype=torch.long)
            for r, ids in enumerate(rows):
                fx[r, : len(ids)] = torch.tensor(ids)
                fl[r, : len(ids)] = torch.tensor(ids)
                fact_tokens_seen += len(ids)
            x = torch.cat([x, fx]); labels = torch.cat([labels, fl])
        filler_tokens_seen += cfg.filler_per_step * cfg.seq_len

        x, labels = x.to(dev), labels.to(dev)
        loss = per_sequence_mean_loss(model(input_ids=x).logits, labels)
        if cfg.collect_step_guards and not torch.isfinite(loss).item():
            raise ValueError(f"Nonfinite loss at step {step}")
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        if cfg.collect_step_guards:
            log["step_guards"].append(training_step_guard(
                step, cfg.filler_per_step, len(shown), len(shown_int), float(norm)))
        opt.step(); opt.zero_grad(set_to_none=True)
        if step % 25 == 0:
            log["train_loss"].append((step, loss.item()))
        # Amendment 4: encoding strength right after each fact's last exposure
        if last is not None and 0 <= inj_step < cfg.t_inj:
            done = [i for i in shown if last[i] == inj_step]
            if done:
                r = evaluator(model, done)
                for j, i in enumerate(done):
                    at_last[i] = {"correct": r["per_fact_correct"][j], "nll": r["per_fact_nll"][j],
                                  "generated": r["per_fact_generated"][j]}
        if step % 200 == 0:
            print(f"step {step:5d}/{total_steps} loss={loss.item():.3f} lr={lr:.1e} "
                  f"facts_in_batch={len(shown)} {time.time()-t0:.0f}s", flush=True)

        if step + 1 == cfg.t_pre:
            evaluate("pre_injection", step + 1)
        elif step + 1 == cfg.t_pre + cfg.t_inj:
            evaluate("immediate", step + 1, int_step=0)
            log["guards"]["param_dist_immediate"] = log["evals"][-1]["param_dist"]
        elif step + 1 > cfg.t_pre + cfg.t_inj:
            int_step = step + 1 - cfg.t_pre - cfg.t_inj
            if int_step in cfg.eval_int_steps:
                evaluate("interference", step + 1, int_step=int_step)

    if cfg.relearn:
        relearn(cfg, model, opt, stream, tok, evaluator, ctrl_facts, dev, log)

    log["guards"].update(
        optimizer_steps=total_steps, fact_tokens_seen=fact_tokens_seen,
        int_exposures=exposure_count(int_sched),
        filler_tokens_seen=filler_tokens_seen, exposures=exposure_count(sched),
        param_dist_end=log["evals"][-1]["param_dist"], wall_seconds=time.time() - t0,
        max_facts_in_one_step=max(len(v) for v in sched.values()),
    )
    if at_last:
        log["at_last_exposure"] = [at_last[i] for i in range(cfg.n_facts)]
        log["guards"]["acc_at_last_exposure"] = float(np.mean([v["correct"] for v in at_last.values()]))
        log["guards"]["nll_at_last_exposure"] = float(np.mean([v["nll"] for v in at_last.values()]))
        print(f"[guard] acc right after last exposure = {log['guards']['acc_at_last_exposure']:.3f} "
              f"nll = {log['guards']['nll_at_last_exposure']:.3f}", flush=True)
    (out_dir / "log.json").write_text(json.dumps(log, indent=1))
    return log


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=list(GAPS) + ["random", "random_matched", "variable_gaps"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--t-inj", type=int, default=600)
    ap.add_argument("--t-int", type=int, default=1500)
    ap.add_argument("--tag", default="")
    ap.add_argument("--n-int-facts", type=int, default=50)
    ap.add_argument("--n-facts", type=int, default=200)
    ap.add_argument("--out", default="results/runs")
    ap.add_argument("--beta1", type=float, default=0.9)
    ap.add_argument("--lora-r", type=int, default=0)
    ap.add_argument("--k-last", type=int, default=0, help="draw p_i as if k were this (contingency runs)")
    ap.add_argument("--paraphrase", action="store_true")
    ap.add_argument("--relearn", action="store_true")
    ap.add_argument("--heldout-probe", action="store_true")
    ap.add_argument("--gap-max", type=int, default=GAP_MAX)
    ap.add_argument("--filler-snapshot", default="")
    ap.add_argument("--filler-sha256", default="")
    a = ap.parse_args()
    cfg = Config(condition=a.condition, seed=a.seed, lr=a.lr, k=a.k, t_inj=a.t_inj, t_int=a.t_int,
                 tag=a.tag, n_int_facts=a.n_int_facts, n_facts=a.n_facts, beta1=a.beta1, lora_r=a.lora_r, k_last=a.k_last, paraphrase=a.paraphrase, relearn=a.relearn, heldout_probe=a.heldout_probe, gap_max=a.gap_max,
                 filler_snapshot=a.filler_snapshot, filler_sha256=a.filler_sha256)
    if a.t_int < 1500:
        cfg.eval_int_steps = tuple(s for s in cfg.eval_int_steps if s <= a.t_int)
    name = f"{a.tag + '_' if a.tag else ''}{a.condition}_s{a.seed}_lr{a.lr:g}_k{a.k}"
    if a.beta1 != 0.9:
        name += f"_b1{a.beta1:g}"
    if a.lora_r > 0:
        name += f"_lora{a.lora_r}"
    if a.paraphrase:
        name += "_para"
    if a.relearn:
        name += "_relearn"
    if a.heldout_probe:
        name += "_hp"
    if a.gap_max != GAP_MAX or a.t_inj != 700:
        name += f"_w{a.t_inj}g{a.gap_max}"
    run(cfg, Path(a.out) / name)


if __name__ == "__main__":
    main()
