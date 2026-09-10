import importlib
import importlib.util

import numpy as np
import pytest


def module():
    assert importlib.util.find_spec('spacinglab.study13_replay') is not None, 'Missing no-revisit policy'
    return importlib.import_module('spacinglab.study13_replay')


def test_uniform_plan_has_exactly_80_globally_distinct_learned_facts():
    m=module(); correct,lengths=[1]*100+[0]*20,[10,11,12]*40
    plans=m.make_plan(correct,lengths,12)
    ids=[i for p in plans for i in p['uniform_ids']]
    assert len(ids)==len(set(ids))==80 and all(correct[i] for i in ids)
    expected=np.random.default_rng(60012).choice(range(100),80,replace=False).tolist()
    assert ids==expected and plans==m.make_plan(correct,lengths,12)
    assert [p['probe_step'] for p in plans]==[100,300,600,900]
    for p in plans:
        assert len(p['uniform_ids'])==20
        assert p['length_slots']==[lengths[i] for i in p['uniform_ids']]
    with pytest.raises(ValueError,match='eligible'):
        m.make_plan([1]*79,[10]*79,12)


@pytest.mark.parametrize('seed',range(12,18))
def test_priority_and_uniform_match_unique_counts_and_length_slots_each_round(seed):
    m=module(); correct,lengths=[1]*100+[0]*20,[10,11,12]*40
    used={a:set() for a in ('uniform','prioritized')}
    ref=[.1]*120; now=np.linspace(.1,5.,120).tolist()
    for r,p in enumerate(m.make_plan(correct,lengths,seed)):
        chosen={}
        for arm in used:
            s=m.select(arm,p,correct,ref,now,lengths,seed,r,used[arm])
            assert s==m.select(arm,p,correct,ref,now,lengths,seed,r,used[arm])
            assert s['used_before_ids']==sorted(used[arm])
            assert not set(s['selected_ids']) & used[arm]
            assert len(set(s['selected_ids']))==20 and all(correct[i] for i in s['selected_ids'])
            used[arm].update(s['selected_ids'])
            assert s['distinct_after']==len(used[arm])==20*(r+1)
            chosen[arm]=[lengths[i] for i in s['selected_ids']]
        assert chosen['uniform']==chosen['prioritized']==p['length_slots']


def test_no_revisit_priority_is_deterioration_not_absolute_error():
    m=module();correct=[1]*8+[0]; lengths=[10]*9
    p=dict(probe_step=300,uniform_ids=[2,3],length_slots=[10,10])
    ref=[.1,.1,4.,.1,1.,1.,1.,1.,.1]
    now=[30.,20.,4.1,2.,1.,1.,1.,1.,50.]
    s=m.select('prioritized',p,correct,ref,now,lengths,12,1,{0,1})
    assert s['selected_ids']==[3,2] and s['distinct_after']==4
    assert s['scores']==pytest.approx([29.9,19.9,.1,1.9,0,0,0,0,49.9])


def test_zero_scores_and_rare_length_buckets_still_finish_with_80_distinct():
    m=module();correct=[1]*80;lengths=[10]*79+[20]
    used=set()
    for r,p in enumerate(m.make_plan(correct,lengths,12)):
        s=m.select('prioritized',p,correct,[1.]*80,[.5]*80,lengths,12,r,used)
        assert s['zero_score_slots']==20
        used.update(s['selected_ids'])
    assert used==set(range(80))


def test_reject_bad_history_nonfinite_scores_and_infeasible_slots():
    m=module(); correct,lengths=[1]*100,[10]*100
    plans=m.make_plan(correct,lengths,12)
    used=set(plans[0]['uniform_ids'])
    with pytest.raises(ValueError,match='history'):
        m.select('uniform',plans[1],correct,[1.]*100,[2.]*100,lengths,12,1,set())
    with pytest.raises(ValueError):
        m.select('uniform',plans[1],correct,[1.]*100,[2.]*100,lengths,12,1,set(plans[1]['uniform_ids']))
    with pytest.raises(ValueError,match='finite'):
        m.select('prioritized',plans[0],correct,[1.]*100,[float('nan')]*100,lengths,12,0,set())
    bad=dict(plans[1],length_slots=[99]*20)
    with pytest.raises(ValueError,match='capacity'):
        m.select('prioritized',bad,correct,[1.]*100,[2.]*100,lengths,12,1,used)
