"""Finite common-fork replay experiment; see docs/STUDY12_PREREGISTRATION.md."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import statistics as st
import subprocess
import sys
import time
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .data import FillerStream, load_filler_snapshot, token_digest
from .facts import make_facts
from .schedule import draw_last_exposures, gap_schedule, random_schedule
from .train import Config, Evaluator, holdout_loss, param_distance, per_sequence_mean_loss
from .study12_replay import ROUNDS, batch, capture, fingerprint, make_plan, restore, select

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/study12'
SEEDS=(9,10,11)
PRIMARY=(200,400,800,1200,1500)
EVALS=(50,100,200,300,400,600,800,900,1200,1500)
REVISION='607a30d783dfa663caf39e06633721c8d4cfcd7e'
MODEL=Path.home()/'.cache/huggingface/hub/models--gpt2/snapshots'/REVISION
FILLER_SHA='868d9478038bd65a11f33b2f943178bf1a291c3d756041191faf542502b70304'


def arm_order(seed):
    if seed not in SEEDS:
        raise ValueError('Unregistered seed')
    return ('prioritized','uniform') if seed==10 else ('uniform','prioritized')


def config(seed):
    arm_order(seed)
    return Config(condition='spaced',seed=seed,k=5,t_inj=700,tag='study12',
                  model_name=str(MODEL),model_revision=REVISION,offline=True,
                  filler_snapshot=str(ROOT/'data/wikitext103_tokens.npy'),
                  filler_sha256=FILLER_SHA,collect_step_guards=True)


def file_sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def save_json(path,value,exclusive=False):
    if exclusive:
        with path.open('x') as f:
            json.dump(value,f,indent=2,allow_nan=False)
    else:
        tmp=path.with_suffix(path.suffix+'.tmp')
        tmp.write_text(json.dumps(value,indent=2,allow_nan=False))
        tmp.replace(path)


def freeze_manifest():
    if not (MODEL/'model.safetensors').is_file():
        raise FileNotFoundError('Pinned model is missing')
    tokens=load_filler_snapshot(ROOT/'data/wikitext103_tokens.npy',FILLER_SHA,2233600)
    files=(sorted((ROOT/'spacinglab').glob('*.py'))+sorted((ROOT/'tests').glob('test_study12*.py'))
           +[ROOT/'uv.lock',ROOT/'pyproject.toml',ROOT/'docs/STUDY12_PREREGISTRATION.md'])
    m=dict(source_sha256={str(p.relative_to(ROOT)):file_sha(p) for p in files},
           model_files_sha256={p.name:file_sha(p) for p in MODEL.iterdir() if p.is_file()},
           filler_sha256=FILLER_SHA,python=sys.version,
           packages={p:version(p) for p in ('torch','transformers','numpy','datasets','peft')},
           configs=[asdict(config(s)) for s in SEEDS],
           arm_order={str(s):arm_order(s) for s in SEEDS},primary_checkpoints=PRIMARY,
           eval_checkpoints=EVALS,replay_probe_steps=ROUNDS,replay_quota_per_round=20,
           streams={str(s):FillerStream(tokens,64,s).provenance(34500) for s in SEEDS})
    m=json.loads(json.dumps(m))
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/'manifest.json'
    if path.exists():
        if json.loads(path.read_text())!=m:
            raise ValueError('Manifest mismatch; stop before evaluation')
    else:
        save_json(path,m,exclusive=True)
    return m


def evaluate(model,old_eval,new_eval,stream,theta0,int_step):
    r=old_eval(model)
    n=new_eval(model)
    r.update(int_step=int_step,int_facts_acc=n['acc'],int_facts_nll=n['nll'],
             holdout_loss=holdout_loss(model,stream.holdout,'mps'),
             param_dist=param_distance(model,theta0))
    return r


def update(model,opt,stream,old_ids,new_ids,old,new,replay,step,eos):
    filler=stream.take(15)
    rows=[old_ids[i] for i in old]+[new_ids[i] for i in new]+[old_ids[i] for i in replay]
    x,labels=batch(filler,rows,eos)
    lr=1e-4*min(1.,(step+1)/50)
    for group in opt.param_groups:
        group['lr']=lr
    device=next(model.parameters()).device
    loss=per_sequence_mean_loss(model(input_ids=x.to(device)).logits,labels.to(device))
    if not torch.isfinite(loss):
        raise ValueError('Nonfinite training loss')
    loss.backward()
    norm=float(torch.nn.utils.clip_grad_norm_(model.parameters(),1.))
    if not np.isfinite(norm):
        raise ValueError('Nonfinite gradient norm')
    opt.step();opt.zero_grad(set_to_none=True)
    scale=min(1.,1./(norm+1e-6))
    return dict(step=step,loss=float(loss.detach()),old_ids=list(old),new_ids=list(new),
                replay_ids=list(replay),filler_sha256=token_digest(filler.numpy()),
                filler_tokens=960,fact_tokens=sum(map(len,rows)),
                replay_tokens=sum(len(old_ids[i]) for i in replay),row_lengths=[len(x) for x in rows],
                preclip_norm=norm,clip_scale=scale,replay_coefficient=len(replay)/(15+len(rows)),
                clipped_replay_coefficient=scale*len(replay)/(15+len(rows)))


def run_pair(seed):
    manifest=freeze_manifest()
    cfg=config(seed)
    folder=OUT/f'seed_{seed}'
    if any(p.name!='console.log' for p in folder.iterdir()):
        raise FileExistsError('Preserve incomplete/completed attempt; no overwrite')
    started=time.time()
    torch.manual_seed(seed)
    tokens=load_filler_snapshot(cfg.filler_snapshot,FILLER_SHA,2233600)
    tok=AutoTokenizer.from_pretrained(str(MODEL),local_files_only=True)
    model=AutoModelForCausalLM.from_pretrained(str(MODEL),local_files_only=True,
            resid_pdrop=0.,embd_pdrop=0.,attn_pdrop=0.).to('mps')
    model.train()
    theta0=[p.detach().clone() for p in model.parameters()]
    opt=torch.optim.AdamW(model.parameters(),lr=1e-4,betas=(.9,.999),weight_decay=0.)
    all_facts=make_facts(250,seed)
    facts,new_facts=all_facts[:200],all_facts[200:]
    old_ids=[[tok.eos_token_id]+tok(f.text)['input_ids'] for f in facts]
    new_ids=[[tok.eos_token_id]+tok(f.text)['input_ids'] for f in new_facts]
    lengths=list(map(len,old_ids))
    assert max(map(len,old_ids+new_ids))<=64
    old_eval,new_eval=Evaluator(tok,facts,'mps'),Evaluator(tok,new_facts,'mps')
    stream=FillerStream(tokens,64,seed)
    assert stream.provenance(34500)==manifest['streams'][str(seed)]
    last=draw_last_exposures(200,5,64,700,seed)
    schedule=gap_schedule(last,5,64)
    interference=random_schedule(50,4,1500,seed+10000)
    common=dict(config=asdict(cfg),facts=[asdict(f) for f in facts],
        int_facts=[asdict(f) for f in new_facts],target_schedule=schedule,
        interference_schedule=interference,last_exposure=last.tolist(),lengths=lengths,new_lengths=list(map(len,new_ids)),
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        manifest_sha256=file_sha(OUT/'manifest.json'),stream=stream.provenance(34500),
        step_guards=[],evals=[],at_last_exposure=[None]*200)
    common['evals'].append(evaluate(model,old_eval,new_eval,stream,theta0,-800))
    for step in range(800):
        shown=schedule.get(step-100,[]) if step>=100 else []
        common['step_guards'].append(update(model,opt,stream,old_ids,new_ids,shown,[],[],step,tok.eos_token_id))
        done=[i for i in shown if last[i]==step-100]
        if done:
            r=old_eval(model,done)
            for j,i in enumerate(done):
                common['at_last_exposure'][i]={'correct':r['per_fact_correct'][j],'nll':r['per_fact_nll'][j]}
        if step+1 in (100,800):
            common['evals'].append(evaluate(model,old_eval,new_eval,stream,theta0,step+1-800))
        if (step+1)%200==0:
            save_json(folder/'common_progress.json',common)
            print(f'PREFIX seed={seed} step={step+1}/800 elapsed={time.time()-started:.0f}s',flush=True)
    reference=common['evals'][-1]
    common['reference']=reference
    try:
        common['replay_plan']=make_plan(reference['per_fact_correct'],lengths,seed)
    except ValueError:
        save_json(folder/'calibration_failure.json',common,exclusive=True)
        raise
    fork=capture(model,opt)
    common['fork_state_sha256']=fingerprint(fork)
    torch.save(fork,folder/'fork.pt')
    common['checkpoint_sha256']=file_sha(folder/'fork.pt')
    common['prefix_wall_seconds']=time.time()-started
    save_json(folder/'common.json',common,exclusive=True)
    for arm in arm_order(seed):
        dest=folder/arm
        dest.mkdir()
        restore(model,opt,fork)
        torch.manual_seed(seed+50000)
        state_hash=fingerprint(capture(model,opt))
        if state_hash!=common['fork_state_sha256']:
            raise ValueError('Fork model/optimizer state mismatch')
        stream=FillerStream(tokens,64,seed);stream.pos=12000
        log=dict(arm=arm,seed=seed,common_sha256=file_sha(folder/'common.json'),
                 start_state_sha256=state_hash,evals=[],selections=[],step_guards=[],guards={})
        replay_schedule={}
        arm_start=time.time()
        print(f'START {arm} seed={seed} eligible={sum(reference["per_fact_correct"])}',flush=True)
        for j in range(1,1501):
            new=interference.get(j-1,[])
            replay=replay_schedule.get(j,[])
            log['step_guards'].append(update(model,opt,stream,old_ids,new_ids,[],new,replay,799+j,tok.eos_token_id))
            if j in EVALS:
                r=evaluate(model,old_eval,new_eval,stream,theta0,j)
                eligible=[i for i,c in enumerate(reference['per_fact_correct']) if c]
                never=[i for i,c in enumerate(reference['per_fact_correct']) if not c]
                r['eligible_acc']=float(np.mean([r['per_fact_correct'][i] for i in eligible]))
                r['initially_unlearned_acc']=(float(np.mean([r['per_fact_correct'][i] for i in never])) if never else None)
                log['evals'].append(r)
                if j in ROUNDS:
                    idx=ROUNDS.index(j)
                    selection=select(arm,common['replay_plan'][idx],reference['per_fact_correct'],
                        reference['per_fact_nll'],r['per_fact_nll'],lengths,seed,idx)
                    selection.update(probe_step=j)
                    log['selections'].append(selection)
                    for offset,i in enumerate(selection['selected_ids'],1):
                        replay_schedule[j+offset]=[i]
                save_json(dest/'progress.json',log)
                print(f'EVAL {arm} seed={seed} int_step={j} acc={r["acc"]:.3f} nll={r["nll"]:.3f}',flush=True)
            if j%200==0:
                print(f'PROGRESS {arm} seed={seed} step={j}/1500 elapsed={time.time()-arm_start:.0f}s',flush=True)
        gs=log['step_guards']
        log['guards']=dict(continuation_steps=len(gs),replay_exposures=sum(len(g['replay_ids']) for g in gs),
            replay_tokens=sum(g['replay_tokens'] for g in gs),fact_tokens=sum(g['fact_tokens'] for g in gs),
            filler_tokens=sum(g['filler_tokens'] for g in gs),wall_seconds=time.time()-arm_start,
            replay_counts=[sum(i in g['replay_ids'] for g in gs) for i in range(200)])
        save_json(dest/'log.json',log,exclusive=True)
        if fingerprint(fork)!=common['fork_state_sha256']:
            raise ValueError('One continuation mutated the shared fork')
        print(f'COMPLETE {arm} seed={seed}',flush=True)
    validate_pair(seed)


def validate_pair(seed):
    folder=OUT/f'seed_{seed}'
    common=json.loads((folder/'common.json').read_text())
    manifest=json.loads((OUT/'manifest.json').read_text())
    assert common['manifest_sha256']==file_sha(OUT/'manifest.json')
    assert common['config']==json.loads(json.dumps(asdict(config(seed))))
    assert common['stream']==manifest['streams'][str(seed)]
    assert common['checkpoint_sha256']==file_sha(folder/'fork.pt')
    ref=common['reference'];lengths=common['lengths']
    assert common['replay_plan']==make_plan(ref['per_fact_correct'],lengths,seed)
    assert len(common['step_guards'])==800
    last=draw_last_exposures(200,5,64,700,seed)
    expected_target=json.loads(json.dumps(gap_schedule(last,5,64)))
    expected_interference=json.loads(json.dumps(random_schedule(50,4,1500,seed+10000)))
    assert common['last_exposure']==last.tolist()
    assert common['target_schedule']==expected_target
    assert common['interference_schedule']==expected_interference
    for t,g in enumerate(common['step_guards']):
        assert g['step']==t and g['old_ids']==(expected_target.get(str(t-100),[]) if t>=100 else [])
    logs={a:json.loads((folder/a/'log.json').read_text()) for a in arm_order(seed)}
    for arm,log in logs.items():
        assert log['arm']==arm and log['seed']==seed
        assert log['common_sha256']==file_sha(folder/'common.json')
        assert log['start_state_sha256']==common['fork_state_sha256']
        assert [e['int_step'] for e in log['evals']]==list(EVALS)
        assert len(log['selections'])==4 and len(log['step_guards'])==1500
        assert log['guards']['replay_exposures']==80
        for e in log['evals']:
            assert len(e['per_fact_correct'])==200
            assert np.isclose(e['acc'],np.mean(e['per_fact_correct']))
        schedule={}
        for idx,s in enumerate(log['selections']):
            e=next(e for e in log['evals'] if e['int_step']==ROUNDS[idx])
            expected=select(arm,common['replay_plan'][idx],ref['per_fact_correct'],
                ref['per_fact_nll'],e['per_fact_nll'],lengths,seed,idx)
            expected['probe_step']=ROUNDS[idx]
            assert s==expected
            for offset,i in enumerate(s['selected_ids'],1):
                schedule[ROUNDS[idx]+offset]=[i]
        for j,g in enumerate(log['step_guards'],1):
            assert g['step']==799+j and not g['old_ids']
            assert g['replay_ids']==schedule.get(j,[])
            assert g['new_ids']==common['interference_schedule'].get(str(j-1),[])
            assert np.isfinite(g['loss']) and np.isfinite(g['preclip_norm'])
            expected_lengths=[common['new_lengths'][i] for i in g['new_ids']]+[lengths[i] for i in g['replay_ids']]
            assert g['row_lengths']==expected_lengths
            assert g['fact_tokens']==sum(expected_lengths)
            assert g['replay_tokens']==sum(lengths[i] for i in g['replay_ids'])
            assert g['filler_tokens']==960
        for name,key in [('fact_tokens','fact_tokens'),('replay_tokens','replay_tokens'),('filler_tokens','filler_tokens')]:
            assert log['guards'][name]==sum(g[key] for g in log['step_guards'])
    a,b=logs['uniform'],logs['prioritized']
    for ga,gb in zip(a['step_guards'],b['step_guards']):
        for k in ('step','new_ids','filler_sha256','filler_tokens','fact_tokens','replay_tokens','row_lengths'):
            assert ga[k]==gb[k],k
    for k in ('continuation_steps','replay_exposures','replay_tokens','fact_tokens','filler_tokens'):
        assert a['guards'][k]==b['guards'][k]
    return common,logs


def measures(log):
    if [e['int_step'] for e in log['evals']]!=list(EVALS):
        raise ValueError('Incomplete evaluations')
    es=[e for e in log['evals'] if e['int_step'] in PRIMARY]
    result={f'retention_{k}':float(np.mean([e[key] for e in es]))
            for k,key in [('accuracy','acc'),('nll','nll'),('discrimination','disc')]}
    last=es[-1]
    result.update(terminal_accuracy=last['acc'],terminal_nll=last['nll'],
                  new_fact_accuracy=last['int_facts_acc'],new_fact_nll=last['int_facts_nll'],
                  filler_loss=last['holdout_loss'],floor_checkpoints=sum(e['acc']<=.02 for e in es),
                  ceiling_checkpoints=sum(e['acc']>=.98 for e in es))
    return result


def describe(x):
    if len(x)!=3 or not np.isfinite(x).all():
        raise ValueError('Expected three finite seed values')
    return dict(values=list(x),mean=st.mean(x),sample_sd=st.stdev(x),min=min(x),max=max(x))


def direction(x):
    d=describe(x)
    if min(x)>0 and d['mean']>d['sample_sd']:
        return 'positive_directional_signal'
    if max(x)<0 and abs(d['mean'])>d['sample_sd']:
        return 'negative_directional_signal'
    return 'mixed_or_inconclusive'


def analyze():
    pairs={s:validate_pair(s) for s in SEEDS}
    ms={(arm,s):measures(pair[1][arm]) for s,pair in pairs.items() for arm in ('uniform','prioritized')}
    summary={}
    for metric in ms['uniform',9]:
        a=[ms['uniform',s][metric] for s in SEEDS]
        b=[ms['prioritized',s][metric] for s in SEEDS]
        summary[metric]=dict(uniform=describe(a),prioritized=describe(b),
                            prioritized_minus_uniform=describe([y-x for x,y in zip(a,b)]))
    d=summary['retention_accuracy']['prioritized_minus_uniform']['values']
    result=dict(registration='docs/STUDY12_PREREGISTRATION.md',complete_pairs=3,
        complete_continuations=6,direction=direction(d),
        prediction_supported=direction(d)=='positive_directional_signal',metrics=summary,
        interpretation='Budget-constrained selection screen, not significance, equivalence, or a biological mechanism.')
    save_json(OUT/'summary.json',result)
    lines=['# Study 12 results','',f'Registered screen: **{result["direction"]}**.',
           'Mean +/- sample SD [min,max], three paired seeds. No historical pooling.',
           'All 200 old facts evaluated; shared acquisition and matched replay budgets.','',
           '| Metric | Uniform | Prioritized | Prioritized minus uniform |','|---|---|---|---|']
    fmt=lambda v:f"{v['mean']:.5f} +/- {v['sample_sd']:.5f} [{v['min']:.5f}, {v['max']:.5f}]"
    for k,v in summary.items():
        lines.append(f"| {k} | {fmt(v['uniform'])} | {fmt(v['prioritized'])} | {fmt(v['prioritized_minus_uniform'])} |")
    lines+=['','## Primary paired results','','| Seed | Uniform | Prioritized | Difference |','|---|---|---|---|']
    for s in SEEDS:
        a,b=ms['uniform',s]['retention_accuracy'],ms['prioritized',s]['retention_accuracy']
        lines.append(f'| {s} | {a:.6f} | {b:.6f} | {b-a:+.6f} |')
    lines+=['','NLL/foil, acquisition, replay allocation, clipping and new-learning guards require completion audit.',
            'No no-replay arm, unseen-fact generalization, representation-erasure or PEFT claim.']
    (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--run',action='store_true');ap.add_argument('--pair',type=int)
    ap.add_argument('--analyze',action='store_true')
    args=ap.parse_args()
    if args.analyze:
        analyze();return
    freeze_manifest()
    if args.pair is not None:
        run_pair(args.pair);return
    if not args.run:
        print('STUDY12_PREFLIGHT_OK; no model evaluation',flush=True);return
    with (OUT/'runner.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        for seed in SEEDS:
            folder=OUT/f'seed_{seed}'
            if all((folder/a/'log.json').exists() for a in arm_order(seed)):
                validate_pair(seed);continue
            if folder.exists() and any(folder.iterdir()):
                raise RuntimeError(f'Incomplete attempt retained: {folder}; no automatic restart')
            folder.mkdir(parents=True,exist_ok=True)
            print(f'START_PAIR seed={seed}',flush=True)
            with (folder/'console.log').open('x') as output:
                subprocess.run([sys.executable,'-u','-m','spacinglab.study12','--pair',str(seed)],cwd=ROOT,
                    stdout=output,stderr=subprocess.STDOUT,check=True,
                    env={**os.environ,'HF_HUB_OFFLINE':'1','TOKENIZERS_PARALLELISM':'false'})
            validate_pair(seed)
            print(f'COMPLETE_PAIR seed={seed}',flush=True)
        analyze();print('STUDY12_DONE',flush=True)


if __name__=='__main__':
    main()
