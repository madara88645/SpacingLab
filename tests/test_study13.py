import importlib
import importlib.util
import json

import numpy as np
import pytest


def module():
    assert importlib.util.find_spec('spacinglab.study13') is not None, 'Missing paired replay runner'
    return importlib.import_module('spacinglab.study13')


def test_registered_sample_order_and_only_delayed_primary_checkpoints():
    m=module()
    assert m.SEEDS==(12,13,14)
    assert m.arm_order(12)==('uniform','prioritized')
    assert m.arm_order(13)==('prioritized','uniform')
    assert m.arm_order(14)==('uniform','prioritized')
    assert m.PRIMARY==(200,400,800,1200,1500)
    assert m.EVALS==(50,100,200,300,400,600,800,900,1200,1500)
    c=m.config(12)
    assert c.condition=='spaced' and c.k==5 and c.t_inj==700 and c.t_int==1500
    assert c.tag=='study13' and c.lora_r==0 and c.offline
    with pytest.raises(ValueError):
        m.config(8)


def test_primary_includes_all_old_facts_and_excludes_selection_probes():
    m=module()
    es=[]
    for t in m.EVALS:
        c=[1]*40+[0]*160 if t in m.PRIMARY else [1]*200
        es.append(dict(int_step=t,acc=np.mean(c),nll=1.,disc=.5,
                       per_fact_correct=c,int_facts_acc=.8,int_facts_nll=.2,holdout_loss=3.))
    v=m.measures({'evals':es})
    assert v['retention_accuracy']==pytest.approx(.2)
    assert v['terminal_accuracy']==pytest.approx(.2)
    assert m.direction([.1,.05,-.01])=='mixed_or_inconclusive'
    assert m.direction([.1,.12,.11])=='positive_directional_signal'
    assert m.direction([-.1,-.12,-.11])=='negative_directional_signal'
    with pytest.raises(ValueError):
        m.measures({'evals':es[:-1]})


def test_manifest_freezes_source_and_detects_drift_without_model_evaluation(tmp_path,monkeypatch):
    import hashlib
    m=module()
    for p in ('data','spacinglab','tests','docs','model'):
        (tmp_path/p).mkdir()
    data=tmp_path/'data/wikitext103_tokens.npy'
    np.save(data,np.zeros(2233600,dtype=np.uint16))
    for f in ('spacinglab/study13.py','tests/test_study13.py','uv.lock','pyproject.toml',
              'docs/STUDY13_PREREGISTRATION.md','model/model.safetensors'):
        (tmp_path/f).write_text('fixture')
    monkeypatch.setattr(m,'ROOT',tmp_path)
    monkeypatch.setattr(m,'OUT',tmp_path/'results/study13')
    monkeypatch.setattr(m,'MODEL',tmp_path/'model')
    monkeypatch.setattr(m,'FILLER_SHA',hashlib.sha256(data.read_bytes()).hexdigest())
    a=m.freeze_manifest()
    assert set(a['streams'])=={'12','13','14'}
    assert a['primary_checkpoints']==list(m.PRIMARY)
    assert a['distinct_replay_quota']==80 and a['max_replays_per_fact']==1
    assert 'tests/test_study13.py' in a['source_sha256']
    assert m.freeze_manifest()==a
    (tmp_path/'spacinglab/study13.py').write_text('drift')
    with pytest.raises(ValueError,match='Manifest mismatch'):
        m.freeze_manifest()


def test_completed_outputs_are_exclusive_and_progress_is_replaceable(tmp_path):
    m=module()
    p=tmp_path/'log.json'
    m.save_json(p,{'done':1},exclusive=True)
    with pytest.raises(FileExistsError):
        m.save_json(p,{'done':2},exclusive=True)
    assert json.loads(p.read_text())=={'done':1}
    p=tmp_path/'progress.json'
    m.save_json(p,{'step':1});m.save_json(p,{'step':2})
    assert json.loads(p.read_text())=={'step':2}


def test_real_toy_update_preserves_filler_and_measures_replay_tokens():
    import torch
    from types import SimpleNamespace
    from spacinglab.data import FillerStream
    m=module()
    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.embed=torch.nn.Embedding(32,8)
            self.head=torch.nn.Linear(8,32)
        def forward(self,input_ids):
            return SimpleNamespace(logits=self.head(self.embed(input_ids)))
    torch.manual_seed(2)
    model=Toy()
    opt=torch.optim.AdamW(model.parameters(),lr=1e-4,weight_decay=0.)
    before=m.fingerprint(m.capture(model,opt))
    stream=FillerStream(np.zeros(64*20,dtype=np.uint16),64,9,n_holdout=1)
    g=m.update(model,opt,stream,[[0,1],[0,2,3,4]],[[0,5,6]],[],[0],[1],800,0)
    assert g['filler_tokens']==960 and stream.pos==15
    assert g['replay_tokens']==4 and g['fact_tokens']==7
    assert g['row_lengths']==[3,4] and g['replay_ids']==[1]
    assert g['replay_coefficient']==pytest.approx(1/17)
    assert m.fingerprint(m.capture(model,opt))!=before


def synthetic_pair(m,root,seed):
    from dataclasses import asdict
    folder=root/f'seed_{seed}'
    folder.mkdir()
    (folder/'fork.pt').write_bytes(b'synthetic unit-test checkpoint, not model weights')
    last=m.draw_last_exposures(200,5,64,700,seed)
    target=m.gap_schedule(last,5,64)
    interference=m.random_schedule(50,4,1500,seed+10000)
    ref=dict(per_fact_correct=[1]*200,per_fact_nll=[.1]*200)
    lengths=[10]*200
    plan=m.make_plan(ref['per_fact_correct'],lengths,seed)
    common=dict(config=json.loads(json.dumps(asdict(m.config(seed)))),
        stream={},manifest_sha256=m.file_sha(root/'manifest.json'),
        checkpoint_sha256=m.file_sha(folder/'fork.pt'),fork_state_sha256='toy-fork',
        reference=ref,lengths=lengths,new_lengths=[12]*50,replay_plan=plan,
        target_schedule=target,last_exposure=last.tolist(),interference_schedule=interference,
        step_guards=[dict(step=t,old_ids=target.get(t-100,[]) if t>=100 else []) for t in range(800)])
    m.save_json(folder/'common.json',common)
    for arm in m.arm_order(seed):
        (folder/arm).mkdir()
        es=[dict(int_step=t,acc=.3,nll=1.,disc=.2,per_fact_correct=[1]*60+[0]*140,
                 per_fact_nll=[i/200+1 for i in range(200)],int_facts_acc=.8,
                 int_facts_nll=.2,holdout_loss=3.) for t in m.EVALS]
        selections=[];schedule={};used=set()
        for idx,step in enumerate(m.ROUNDS):
            e=next(e for e in es if e['int_step']==step)
            r=m.select(arm,plan[idx],ref['per_fact_correct'],ref['per_fact_nll'],
                       e['per_fact_nll'],lengths,seed,idx,used)
            r['probe_step']=step;selections.append(r);used.update(r['selected_ids'])
            schedule.update({step+o:[i] for o,i in enumerate(r['selected_ids'],1)})
        gs=[]
        for j in range(1,1501):
            new=interference.get(j-1,[]);replay=schedule.get(j,[])
            rows=[12]*len(new)+[10]*len(replay)
            gs.append(dict(step=799+j,old_ids=[],new_ids=new,replay_ids=replay,
                filler_sha256='synthetic',filler_tokens=960,fact_tokens=sum(rows),
                replay_tokens=10*len(replay),row_lengths=rows,loss=1.,preclip_norm=1.5))
        log=dict(arm=arm,seed=seed,common_sha256=m.file_sha(folder/'common.json'),
                 start_state_sha256='toy-fork',evals=es,selections=selections,step_guards=gs,
                 guards=dict(continuation_steps=1500,replay_exposures=80,replay_tokens=800,
                             fact_tokens=sum(g['fact_tokens'] for g in gs),filler_tokens=1500*960,
                             distinct_replayed=len(used),cumulative_distinct=[r['distinct_after'] for r in selections],
                             replay_counts=[sum(i in g['replay_ids'] for g in gs) for i in range(200)]))
        m.save_json(folder/arm/'log.json',log)
    return folder


def test_pair_validation_rejects_identically_inflated_token_budgets(tmp_path,monkeypatch):
    m=module();monkeypatch.setattr(m,'OUT',tmp_path)
    m.save_json(tmp_path/'manifest.json',{'streams':{'12':{}}})
    folder=synthetic_pair(m,tmp_path,12)
    m.validate_pair(12)
    for arm in m.arm_order(12):
        path=folder/arm/'log.json'
        x=json.loads(path.read_text());x['step_guards'][0]['fact_tokens']+=1
        m.save_json(path,x)
    with pytest.raises(AssertionError):
        m.validate_pair(12)


def test_three_pair_analysis_is_finite_and_does_not_pool_history(tmp_path,monkeypatch):
    m=module();monkeypatch.setattr(m,'OUT',tmp_path)
    m.save_json(tmp_path/'manifest.json',{'streams':{str(s):{} for s in m.SEEDS}})
    for seed in m.SEEDS:
        synthetic_pair(m,tmp_path,seed)
    result=m.analyze()
    assert result['complete_pairs']==3 and result['complete_continuations']==6
    assert result['direction']=='mixed_or_inconclusive'
    assert result['metrics']['retention_accuracy']['uniform']['mean']==pytest.approx(.3)
    assert result['metrics']['retention_accuracy']['prioritized_minus_uniform']['values']==[0.,0.,0.]
    assert 'No historical pooling' in (tmp_path/'REPORT.md').read_text()

def test_pair_validator_rejects_false_coverage_counter(tmp_path,monkeypatch):
    m=module();monkeypatch.setattr(m,'OUT',tmp_path)
    m.save_json(tmp_path/'manifest.json',{'streams':{'12':{}}})
    folder=synthetic_pair(m,tmp_path,12)
    m.validate_pair(12)
    path=folder/'uniform/log.json'
    x=json.loads(path.read_text());x['guards']['distinct_replayed']=79
    m.save_json(path,x)
    with pytest.raises(AssertionError):
        m.validate_pair(12)


def test_pair_validator_rejects_missing_used_history(tmp_path,monkeypatch):
    m=module();monkeypatch.setattr(m,'OUT',tmp_path)
    m.save_json(tmp_path/'manifest.json',{'streams':{'12':{}}})
    folder=synthetic_pair(m,tmp_path,12)
    path=folder/'prioritized/log.json'
    x=json.loads(path.read_text());x['selections'][1]['used_before_ids']=[]
    m.save_json(path,x)
    with pytest.raises(AssertionError):
        m.validate_pair(12)


def test_evaluate_retains_already_computed_new_fact_details(monkeypatch):
    from types import SimpleNamespace
    m=module()
    # No model inference: isolate logging from expensive, already-tested probes.
    calls=[]
    old={'acc':.5,'nll':1.}
    new={'acc':.25,'nll':2.,'per_fact_correct':[1,0,0,0],'per_fact_nll':[.2,2.,2.8,3.]}
    def old_probe(model):
        calls.append('old');return dict(old)
    def new_probe(model):
        calls.append('new');return dict(new)
    monkeypatch.setattr(m,'holdout_loss',lambda *args:3.)
    monkeypatch.setattr(m,'param_distance',lambda *args:4.)
    r=m.evaluate(object(),old_probe,new_probe,SimpleNamespace(holdout=None),[],100)
    assert calls==['old','new']
    assert r['new_fact_evaluation']==new
    assert r['int_facts_acc']==new['acc'] and r['int_facts_nll']==new['nll']
