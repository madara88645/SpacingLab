"""Study 13 policy: exact paired coverage, no revisits across replay rounds."""
from collections import Counter

import numpy as np

from .study12_replay import ROUNDS, select as within_round_select


def make_plan(correct, lengths, seed, quota=20):
    if len(correct)!=len(lengths) or any(n<1 for n in lengths) or quota<1:
        raise ValueError('Invalid lengths or quota')
    eligible=np.flatnonzero(np.asarray(correct)==1)
    if len(eligible)<len(ROUNDS)*quota:
        raise ValueError('Insufficient eligible learned facts; calibration failure')
    chosen=np.random.default_rng(seed+60000).choice(eligible,len(ROUNDS)*quota,replace=False).tolist()
    return [dict(probe_step=step,uniform_ids=chosen[r*quota:(r+1)*quota],
                 length_slots=[lengths[i] for i in chosen[r*quota:(r+1)*quota]])
            for r,step in enumerate(ROUNDS)]


def select(arm,plan,correct,reference_nll,current_nll,lengths,seed,round_index,used_ids):
    history=list(used_ids)
    used=set(history)
    if (round_index not in range(len(ROUNDS)) or plan['probe_step']!=ROUNDS[round_index]
            or len(history)!=len(used) or len(used)!=round_index*len(plan['uniform_ids'])
            or any(i<0 or i>=len(correct) or correct[i]!=1 for i in used)):
        raise ValueError('Invalid no-revisit history')
    available=[int(c==1 and i not in used) for i,c in enumerate(correct)]
    capacity=Counter(lengths[i] for i,c in enumerate(available) if c)
    if any(capacity[n]<count for n,count in Counter(plan['length_slots']).items()):
        raise ValueError('Insufficient length-bucket capacity; preserve attempt')
    result=within_round_select(arm,plan,available,reference_nll,current_nll,lengths,seed,round_index)
    chosen=set(result['selected_ids'])
    if chosen & used:
        raise ValueError('Repeated replay item')
    result.update(used_before_ids=sorted(used),distinct_after=len(used|chosen))
    return result
