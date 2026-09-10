"""Pure budget-matched replay policy and fork/batch helpers for Study 12."""
import copy
import hashlib

import numpy as np
import torch

ROUNDS = (100, 300, 600, 900)


def make_plan(correct, lengths, seed, quota=20):
    if len(correct)!=len(lengths) or any(n<1 for n in lengths):
        raise ValueError("Invalid lengths")
    eligible = np.flatnonzero(np.asarray(correct)==1)
    if len(eligible)<quota:
        raise ValueError("Insufficient eligible learned facts; calibration failure")
    result=[]
    for r,step in enumerate(ROUNDS):
        ids=np.random.default_rng(seed+60000+r).choice(eligible,quota,replace=False).tolist()
        result.append(dict(probe_step=step,uniform_ids=ids,length_slots=[lengths[i] for i in ids]))
    return result


def select(arm, plan, correct, reference_nll, current_nll, lengths, seed, round_index):
    if arm not in ("uniform","prioritized"):
        raise ValueError("Unregistered arm")
    ref,now=np.asarray(reference_nll,float),np.asarray(current_nll,float)
    if (ref.shape!=now.shape or ref.ndim!=1 or len(ref)!=len(correct)
            or len(lengths)!=len(correct) or not np.isfinite(ref).all() or not np.isfinite(now).all()):
        raise ValueError("Expected matching finite per-fact scores")
    scores=np.maximum(0.,now-ref)
    eligible=[i for i,c in enumerate(correct) if c==1]
    if arm=="uniform":
        selected=list(plan["uniform_ids"])
    else:
        tie=np.random.default_rng(seed+80000+round_index).random(len(correct))
        buckets={n:sorted([i for i in eligible if lengths[i]==n],key=lambda i:(-scores[i],tie[i],i))
                 for n in set(plan["length_slots"])}
        selected=[buckets[n].pop(0) for n in plan["length_slots"]]
    if len(set(selected))!=len(plan["uniform_ids"]) or any(i not in eligible for i in selected):
        raise ValueError("Invalid replay selection")
    if [lengths[i] for i in selected]!=plan["length_slots"]:
        raise ValueError("Replay token budget mismatch")
    return dict(selected_ids=selected,scores=scores.tolist(),
                zero_score_slots=int(sum(scores[i]==0 for i in selected)),
                uniform_overlap=len(set(selected)&set(plan["uniform_ids"])))


def _cpu(obj):
    if torch.is_tensor(obj):
        return obj.detach().cpu().clone()
    if isinstance(obj,dict):
        return {k:_cpu(v) for k,v in obj.items()}
    if isinstance(obj,list):
        return [_cpu(v) for v in obj]
    if isinstance(obj,tuple):
        return tuple(_cpu(v) for v in obj)
    return copy.deepcopy(obj)


def capture(model, optimizer):
    return dict(model=_cpu(model.state_dict()),optimizer=_cpu(optimizer.state_dict()))


def restore(model, optimizer, fork):
    model.load_state_dict(fork["model"])
    # load_state_dict may alias CPU tensors: never let one arm mutate the fork.
    optimizer.load_state_dict(copy.deepcopy(fork["optimizer"]))
    optimizer.zero_grad(set_to_none=True)


def fingerprint(obj):
    h=hashlib.sha256()
    def add(x):
        if torch.is_tensor(x):
            a=x.detach().cpu().contiguous()
            h.update(str((a.dtype,tuple(a.shape))).encode())
            h.update(a.reshape(-1).view(torch.uint8).numpy().tobytes())
        elif isinstance(x,dict):
            for k in sorted(x,key=lambda v:(type(v).__name__,str(v))):
                add(k); add(x[k])
        elif isinstance(x,(list,tuple)):
            h.update(type(x).__name__.encode())
            for v in x:
                add(v)
        else:
            h.update((type(x).__name__+":"+repr(x)+";").encode())
    add(obj)
    return h.hexdigest()


def batch(filler, rows, eos):
    if not rows:
        return filler,filler.clone()
    if any(len(ids)>filler.shape[1] or len(ids)<2 for ids in rows):
        raise ValueError("Invalid fact input length")
    fx=torch.full((len(rows),filler.shape[1]),eos,dtype=torch.long)
    labels=torch.full_like(fx,-100)
    for i,ids in enumerate(rows):
        fx[i,:len(ids)]=torch.tensor(ids)
        labels[i,:len(ids)]=torch.tensor(ids)
    return torch.cat([filler,fx]),torch.cat([filler,labels])
