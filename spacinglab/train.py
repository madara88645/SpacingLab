"""One run: pre-phase -> injection window (facts placed by schedule) -> interference.

Everything except the exposure placement is identical across conditions of a seed.
"""
from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from .data import FillerStream, build_filler_tokens
from .facts import Fact, make_facts
from .schedule import draw_last_exposures, exposure_count, gap_schedule, random_schedule

GAPS = {"massed": 1, "gap4": 4, "gap16": 16, "spaced": 64}
GAP_MAX = 64


@dataclass
class Config:
    condition: str            # massed | gap4 | gap16 | spaced | random (pilot only)
    seed: int
    lr: float = 1e-4
    k: int = 4                # exposures per fact
    n_facts: int = 100
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

    @torch.no_grad()
    def __call__(self, model) -> dict:
        model.eval()
        dev = self.device
        # teacher-forced answer NLL per fact
        logits = model(input_ids=self.tf_ids.to(dev)).logits[:, :-1].float()
        labels = self.tf_labels[:, 1:].to(dev)
        tok_loss = F.cross_entropy(
            logits.reshape(-1, logits.size(-1)), labels.reshape(-1), ignore_index=-100, reduction="none"
        ).view(labels.shape)
        mask = (labels != -100).float()
        nll = ((tok_loss * mask).sum(1) / mask.sum(1)).cpu().tolist()
        # greedy exact match
        out = model.generate(
            input_ids=self.gen_ids.to(dev), attention_mask=self.gen_mask.to(dev),
            max_new_tokens=self.max_ans, do_sample=False, pad_token_id=self.tok.eos_token_id,
        )
        gen = out[:, self.gen_ids.size(1):].cpu()
        correct = [gen[i, : len(a)].tolist() == a for i, a in enumerate(self.answer_ids)]
        model.train()
        return {
            "acc": float(np.mean(correct)),
            "nll": float(np.mean(nll)),
            "per_fact_correct": [int(c) for c in correct],
            "per_fact_nll": nll,
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
    return math.sqrt(sum(((p - q) ** 2).sum().item() for p, q in zip(model.parameters(), theta0)))


def run(cfg: Config, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(cfg.seed)
    dev = cfg.device
    tok = AutoTokenizer.from_pretrained(cfg.model_name)
    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name, resid_pdrop=0.0, embd_pdrop=0.0, attn_pdrop=0.0
    ).to(dev)
    model.train()
    theta0 = [p.detach().clone() for p in model.parameters()]

    facts = make_facts(cfg.n_facts, cfg.seed)
    evaluator = Evaluator(tok, facts, dev)

    total_steps = cfg.t_pre + cfg.t_inj + cfg.t_int
    n_filler = total_steps * cfg.filler_per_step
    tokens = build_filler_tokens(tok, n_tokens=(n_filler + 400) * cfg.seq_len)
    stream = FillerStream(tokens, cfg.seq_len, seed=cfg.seed)

    if cfg.condition == "random":
        sched = random_schedule(cfg.n_facts, cfg.k, cfg.t_inj, seed=cfg.seed)
        last = None
    else:
        last = draw_last_exposures(cfg.n_facts, cfg.k, GAP_MAX, cfg.t_inj, seed=cfg.seed)
        sched = gap_schedule(last, cfg.k, GAPS[cfg.condition])
    assert exposure_count(sched) == cfg.n_facts * cfg.k
    assert max(len(v) for v in sched.values()) <= cfg.max_facts_per_step

    eos = tok.eos_token_id
    fact_ids = [[eos] + tok(f.text)["input_ids"] for f in facts]
    assert max(len(x) for x in fact_ids) <= cfg.seq_len

    opt = torch.optim.AdamW(model.parameters(), lr=cfg.lr, betas=(0.9, 0.999), weight_decay=0.0)

    log: dict = {"config": asdict(cfg), "facts": [asdict(f) for f in facts],
                 "last_exposure": None if last is None else last.tolist(),
                 "evals": [], "train_loss": [], "guards": {}}

    def evaluate(phase: str, step: int, int_step: int | None = None):
        r = evaluator(model)
        r.update(phase=phase, step=step, int_step=int_step,
                 holdout_loss=holdout_loss(model, stream.holdout, dev),
                 param_dist=param_distance(model, theta0))
        log["evals"].append(r)
        print(f"[eval] {phase:>10} step={step:5d} acc={r['acc']:.3f} nll={r['nll']:.3f} "
              f"holdout={r['holdout_loss']:.3f} |dθ|={r['param_dist']:.2f}", flush=True)

    evaluate("pretrained", 0)
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
        if shown:
            fx = torch.full((len(shown), cfg.seq_len), eos, dtype=torch.long)
            fl = torch.full((len(shown), cfg.seq_len), -100, dtype=torch.long)
            for r, i in enumerate(shown):
                ids = fact_ids[i]
                fx[r, : len(ids)] = torch.tensor(ids)
                fl[r, : len(ids)] = torch.tensor(ids)
                fact_tokens_seen += len(ids)
            x = torch.cat([x, fx]); labels = torch.cat([labels, fl])
        filler_tokens_seen += cfg.filler_per_step * cfg.seq_len

        x, labels = x.to(dev), labels.to(dev)
        loss = per_sequence_mean_loss(model(input_ids=x).logits, labels)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); opt.zero_grad(set_to_none=True)
        if step % 25 == 0:
            log["train_loss"].append((step, loss.item()))
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

    log["guards"].update(
        optimizer_steps=total_steps, fact_tokens_seen=fact_tokens_seen,
        filler_tokens_seen=filler_tokens_seen, exposures=exposure_count(sched),
        param_dist_end=log["evals"][-1]["param_dist"], wall_seconds=time.time() - t0,
        max_facts_in_one_step=max(len(v) for v in sched.values()),
    )
    (out_dir / "log.json").write_text(json.dumps(log, indent=1))
    return log


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", required=True, choices=list(GAPS) + ["random"])
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--k", type=int, default=4)
    ap.add_argument("--t-inj", type=int, default=600)
    ap.add_argument("--t-int", type=int, default=1500)
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", default="results/runs")
    a = ap.parse_args()
    cfg = Config(condition=a.condition, seed=a.seed, lr=a.lr, k=a.k, t_inj=a.t_inj, t_int=a.t_int, tag=a.tag)
    if a.t_int < 1500:
        cfg.eval_int_steps = tuple(s for s in cfg.eval_int_steps if s <= a.t_int)
    name = f"{a.tag + '_' if a.tag else ''}{a.condition}_s{a.seed}_lr{a.lr:g}_k{a.k}"
    run(cfg, Path(a.out) / name)


if __name__ == "__main__":
    main()
