import importlib
import importlib.util

import numpy as np
import pytest
import torch


def module():
    assert importlib.util.find_spec('spacinglab.study12_replay') is not None, 'Missing replay policy'
    return importlib.import_module('spacinglab.study12_replay')


def test_uniform_plan_uses_only_common_learned_pool_and_exact_quota():
    m = module()
    correct = [1]*24 + [0]*6
    lengths = [10,11,12]*10
    p = m.make_plan(correct,lengths,9)
    assert [r['probe_step'] for r in p] == [100,300,600,900]
    assert p == m.make_plan(correct,lengths,9)
    for r in p:
        assert len(r['uniform_ids'])==len(set(r['uniform_ids']))==20
        assert all(correct[i] for i in r['uniform_ids'])
        assert r['length_slots']==[lengths[i] for i in r['uniform_ids']]
    with pytest.raises(ValueError,match='eligible'):
        m.make_plan([1]*19,[10]*19,9)


def test_priority_means_deterioration_not_current_difficulty_or_never_learned():
    m = module()
    correct, lengths = [1,1,0,1],[10]*4
    reference, current = [.1,4.,.1,.2],[1.,4.1,20.,.1]
    plan = m.make_plan(correct,lengths,9,quota=2)[0]
    r = m.select('prioritized',plan,correct,reference,current,lengths,9,0)
    assert set(r['selected_ids']) == {0,1}
    assert r['scores'] == pytest.approx([.9,.1,19.9,0.])
    assert 2 not in r['selected_ids']
    assert r['zero_score_slots']==0


def test_priority_exactly_matches_uniform_token_lengths_at_each_step():
    m = module()
    correct, lengths = [1]*30, [10,11,12]*10
    ref, now = [1.]*30, list(np.linspace(.1,3.,30))
    for idx,p in enumerate(m.make_plan(correct,lengths,10)):
        a=m.select('uniform',p,correct,ref,now,lengths,10,idx)
        b=m.select('prioritized',p,correct,ref,now,lengths,10,idx)
        assert [lengths[i] for i in a['selected_ids']] == [lengths[i] for i in b['selected_ids']]
        assert len(set(b['selected_ids']))==20
        assert a['selected_ids']==p['uniform_ids']
        assert b==m.select('prioritized',p,correct,ref,now,lengths,10,idx)


def test_zero_score_fallback_preserves_budget_and_never_selects_unlearned():
    m = module()
    correct,lengths=[1]*21+[0],[10]*22
    p=m.make_plan(correct,lengths,9)[0]
    r=m.select('prioritized',p,correct,[1.]*22,[.5]*22,lengths,9,0)
    assert r['zero_score_slots']==20 and len(set(r['selected_ids']))==20
    assert 21 not in r['selected_ids']
    with pytest.raises(ValueError,match='finite'):
        m.select('prioritized',p,correct,[1.]*22,[float('nan')]*22,lengths,9,0)
    with pytest.raises(ValueError,match='arm'):
        m.select('unregistered',p,correct,[1.]*22,[1.]*22,lengths,9,0)


@pytest.mark.parametrize('device',['cpu','mps'] if torch.backends.mps.is_available() else ['cpu'])
def test_restore_preserves_parameters_optimizer_moments_and_immutable_fork(device):
    m = module()
    torch.manual_seed(1)
    model=torch.nn.Linear(2,1).to(device)
    opt=torch.optim.AdamW(model.parameters(),lr=.01)
    x=torch.tensor([[1.,2.]],device=device)
    model(x).sum().backward(); opt.step(); opt.zero_grad()
    fork=m.capture(model,opt)
    original=m.fingerprint(fork)
    results=[]
    for _ in range(2):
        m.restore(model,opt,fork)
        assert m.fingerprint(m.capture(model,opt))==original
        model(x).sum().backward(); opt.step(); opt.zero_grad()
        results.append(m.fingerprint(m.capture(model,opt)))
        assert m.fingerprint(fork)==original
    assert results[0]==results[1] and results[0]!=original


def test_batch_counts_true_tokens_without_changing_filler():
    m = module()
    filler=torch.tensor([[1,2,3,4],[5,6,7,8]])
    ids,labels=m.batch(filler,[[9,10],[11,12,13]],0)
    assert torch.equal(ids[:2],filler) and torch.equal(labels[:2],filler)
    assert ids.tolist()==[[1,2,3,4],[5,6,7,8],[9,10,0,0],[11,12,13,0]]
    assert labels.tolist()[-2:]==[[9,10,-100,-100],[11,12,13,-100]]
    with pytest.raises(ValueError,match='length'):
        m.batch(filler,[[1]*5],0)
