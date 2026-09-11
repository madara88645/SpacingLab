"""Post-run audit, not a new experiment. No model inference or training.

Reconstructs selection, schedules, filler bytes, raw aggregates and summary
independently of the Study 12 runner/analysis. Reuses only the frozen fact
generator and state serialization hash to check checkpoint identity.
Run: uv run --no-sync python results/study12/audit_results.py
"""
import hashlib
import json
import math
import statistics as st
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

import numpy as np
import torch
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from spacinglab.facts import make_facts
from spacinglab.study12_replay import fingerprint

OUT = ROOT / 'results/study12'
SEEDS = (9, 10, 11)
PRIMARY = (200, 400, 800, 1200, 1500)
EVALS = (50, 100, 200, 300, 400, 600, 800, 900, 1200, 1500)
ROUNDS = (100, 300, 600, 900)


def read(path):
    return json.loads(path.read_text())


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def close(a, b):
    assert math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-10), (a, b)


def desc(xs):
    return dict(values=list(xs), mean=st.mean(xs), sample_sd=st.stdev(xs), min=min(xs), max=max(xs))


def finite(obj):
    if isinstance(obj, float):
        assert math.isfinite(obj)
    elif isinstance(obj, dict):
        for value in obj.values():
            finite(value)
    elif isinstance(obj, list):
        for value in obj:
            finite(value)


def eval_audit(e, facts):
    c, n, f = e['per_fact_correct'], e['per_fact_nll'], e['per_fact_nll_foil']
    assert len(c) == len(n) == len(f) == len(facts)
    assert all(v in (0, 1) for v in c)
    assert all(v >= 0 for v in n + f)
    assert c == [int(g == fact['answer']) for g, fact in zip(e['per_fact_generated'], facts)]
    for key, v in [('acc', st.mean(c)), ('nll', st.mean(n)), ('nll_foil', st.mean(f)),
                   ('disc', st.mean([b-a for a,b in zip(n,f)])),
                   ('disc_frac', st.mean([int(b>a) for a,b in zip(n,f)]))]:
        close(e[key], v)


def main():
    m = read(OUT/'manifest.json')
    assert (OUT/'manifest.json').read_bytes() == git('show', '59cf386:results/study12/manifest.json')
    for path, digest in m['source_sha256'].items():
        assert sha(ROOT/path) == digest, path
        assert hashlib.sha256(git('show', f'd19c63f:{path}')).hexdigest() == digest, path
    assert git('show', 'dd3e56c:docs/STUDY12_PREREGISTRATION.md') == (ROOT/'docs/STUDY12_PREREGISTRATION.md').read_bytes()
    for earlier, later in [('dd3e56c','d19c63f'), ('d19c63f','59cf386'), ('59cf386','eb38dcc')]:
        subprocess.run(['git','merge-base','--is-ancestor',earlier,later],cwd=ROOT,check=True)
    assert sys.version == m['python']
    assert {p:version(p) for p in m['packages']} == m['packages']
    modelpath = Path(m['configs'][0]['model_name'])
    for name, digest in m['model_files_sha256'].items():
        assert sha(modelpath/name) == digest
    assert sha(ROOT/'data/wikitext103_tokens.npy') == m['filler_sha256']
    tok = AutoTokenizer.from_pretrained(str(modelpath), local_files_only=True)
    tokens = np.load(ROOT/'data/wikitext103_tokens.npy', allow_pickle=False)
    chunks = tokens[:len(tokens)//64*64].reshape(-1,64)
    assert m['primary_checkpoints'] == list(PRIMARY)
    assert m['eval_checkpoints'] == list(EVALS)
    assert m['replay_probe_steps'] == list(ROUNDS) and m['replay_quota_per_round'] == 20
    report = dict(status='PASS', audit_type='post-run verification, no inference/training', seeds={}, metrics={})
    allmetrics = defaultdict(dict)
    paired = {}
    for seed in SEEDS:
        folder = OUT/f'seed_{seed}'
        c = read(folder/'common.json'); finite(c)
        assert c['manifest_sha256'] == sha(OUT/'manifest.json')
        assert c['config'] == m['configs'][SEEDS.index(seed)]
        subprocess.run(['git','merge-base','--is-ancestor','59cf386',c['source_commit']],cwd=ROOT,check=True)
        for path,digest in m['source_sha256'].items():
            assert hashlib.sha256(git('show',f'{c["source_commit"]}:{path}')).hexdigest() == digest
        facts = [asdict(f) for f in make_facts(250,seed)]
        assert c['facts'] + c['int_facts'] == facts
        lengths = [1+len(tok(f['text'])['input_ids']) for f in facts]
        assert c['lengths'] + c['new_lengths'] == lengths and max(lengths) <= 64
        assert sha(folder/'fork.pt') == c['checkpoint_sha256']
        fork = torch.load(folder/'fork.pt',map_location='cpu',weights_only=True)
        assert fingerprint(fork) == c['fork_state_sha256']
        states = list(fork['optimizer']['state'].values())
        assert states and all(float(v['step']) == 800 for v in states)
        assert all('exp_avg' in v and 'exp_avg_sq' in v for v in states)
        assert any(torch.count_nonzero(v['exp_avg']).item() for v in states)
        for g in fork['optimizer']['param_groups']:
            assert g['lr']==1e-4 and tuple(g['betas'])==(.9,.999) and g['weight_decay']==0
        del fork, states
        last = np.random.default_rng(seed).integers(256,700,200).tolist()
        target = defaultdict(list)
        for i, end in enumerate(last):
            for j in range(5):
                target[str(end-64*j)].append(i)
        rng = np.random.default_rng(seed+10000)
        new = defaultdict(list)
        for i in range(50):
            for step in rng.choice(1500,4,replace=False).tolist():
                new[str(step)].append(i)
        assert c['last_exposure']==last and c['target_schedule']==dict(target)
        assert c['interference_schedule']==dict(new)
        order=np.random.default_rng(seed).permutation(len(chunks))
        filler=chunks[order[200:]]
        digest=lambda a:hashlib.sha256(np.asarray(a,dtype='<i8').tobytes()).hexdigest()
        provenance=dict(train_chunks=34500,heldout_chunks=200,seq_len=64,
                        train_sha256=digest(filler[:34500]),heldout_sha256=digest(chunks[order[:200]]))
        assert c['stream']==m['streams'][str(seed)]==provenance
        assert len(c['step_guards'])==800 and len(c['at_last_exposure'])==200
        assert [e['int_step'] for e in c['evals']]==[-800,-700,0]
        for e in c['evals']:
            eval_audit(e,facts[:200])
        ref=c['reference']; assert ref==c['evals'][-1]
        eligible=[i for i,v in enumerate(ref['per_fact_correct']) if v]
        never=[i for i in range(200) if i not in eligible]
        assert len(eligible)>=20
        plans=[]
        for r,p in enumerate(ROUNDS):
            ids=np.random.default_rng(seed+60000+r).choice(eligible,20,replace=False).tolist()
            plans.append(dict(probe_step=p,uniform_ids=ids,length_slots=[lengths[i] for i in ids]))
        assert c['replay_plan']==plans
        logs={a:read(folder/a/'log.json') for a in ('uniform','prioritized')}
        paired[seed]=logs
        sr=dict(eligible_count=len(eligible),common_accuracy=ref['acc'],common_nll=ref['nll'],
                last_exposure_accuracy=st.mean(v['correct'] for v in c['at_last_exposure']),
                prefix_wall_seconds=c['prefix_wall_seconds'],arms={},pre_replay_drift={})

        def steps_audit(gs, start, replay):
            for offset,g in enumerate(gs):
                step=start+offset
                assert g['step']==step
                assert g['old_ids']==(target.get(str(step-100),[]) if 100<=step<800 else [])
                assert g['new_ids']==(new.get(str(step-800),[]) if step>=800 else [])
                assert g['replay_ids']==replay.get(step-799,[])
                rows=[lengths[i] for i in g['old_ids']]+[lengths[200+i] for i in g['new_ids']]+[lengths[i] for i in g['replay_ids']]
                assert g['row_lengths']==rows and g['fact_tokens']==sum(rows)
                assert g['replay_tokens']==sum(lengths[i] for i in g['replay_ids'])
                assert g['filler_tokens']==960 and g['filler_sha256']==digest(filler[15*step:15*(step+1)])
                assert g['loss']>=0 and g['preclip_norm']>=0
                close(g['clip_scale'],min(1,1/(g['preclip_norm']+1e-6)))
                close(g['replay_coefficient'],len(g['replay_ids'])/(15+len(rows)))
                close(g['clipped_replay_coefficient'],g['clip_scale']*g['replay_coefficient'])

        steps_audit(c['step_guards'],0,{})
        for arm,log in logs.items():
            finite(log)
            assert log['seed']==seed and log['arm']==arm
            assert log['common_sha256']==sha(folder/'common.json')
            assert log['start_state_sha256']==c['fork_state_sha256']
            assert [e['int_step'] for e in log['evals']]==list(EVALS)
            assert len(log['selections'])==4 and len(log['step_guards'])==1500
            for e in log['evals']:
                eval_audit(e,facts[:200])
                close(e['eligible_acc'],st.mean(e['per_fact_correct'][i] for i in eligible))
                close(e['initially_unlearned_acc'],st.mean(e['per_fact_correct'][i] for i in never))
            replay={}
            for r,s in enumerate(log['selections']):
                p=ROUNDS[r]; assert s['probe_step']==p
                e=next(e for e in log['evals'] if e['int_step']==p)
                scores=[max(0,a-b) for a,b in zip(e['per_fact_nll'],ref['per_fact_nll'])]
                assert s['scores']==scores
                if arm=='uniform':
                    ids=plans[r]['uniform_ids']
                else:
                    tie=np.random.default_rng(seed+80000+r).random(200)
                    candidates=sorted(eligible,key=lambda i:(-scores[i],tie[i],i))
                    ids=[]
                    for length in plans[r]['length_slots']:
                        i=next(i for i in candidates if lengths[i]==length)
                        ids.append(i); candidates.remove(i)
                assert s['selected_ids']==ids and len(set(ids))==20
                assert all(i in eligible for i in ids)
                assert s['zero_score_slots']==sum(scores[i]==0 for i in ids)
                assert s['uniform_overlap']==len(set(ids)&set(plans[r]['uniform_ids']))
                for j,i in enumerate(ids,1):
                    replay[p+j]=[i]
            gs=log['step_guards'];steps_audit(gs,800,replay)
            counts=[sum(i in g['replay_ids'] for g in gs) for i in range(200)]
            assert sum(counts)==80 and max(counts)<=4 and all(counts[i]==0 for i in never)
            expected=dict(continuation_steps=1500,replay_exposures=80,replay_counts=counts,
                          **{k:sum(g[k] for g in gs) for k in ('replay_tokens','fact_tokens','filler_tokens')})
            for k,v in expected.items():
                assert log['guards'][k]==v
            es=[e for e in log['evals'] if e['int_step'] in PRIMARY]; end=es[-1]
            ms=dict(retention_accuracy=st.mean(st.mean(e['per_fact_correct']) for e in es),
                    retention_nll=st.mean(st.mean(e['per_fact_nll']) for e in es),
                    retention_discrimination=st.mean(st.mean(b-a for a,b in zip(e['per_fact_nll'],e['per_fact_nll_foil'])) for e in es),
                    terminal_accuracy=end['acc'],terminal_nll=end['nll'],
                    new_fact_accuracy=end['int_facts_acc'],new_fact_nll=end['int_facts_nll'],
                    filler_loss=end['holdout_loss'],floor_checkpoints=sum(e['acc']<=.02 for e in es),
                    ceiling_checkpoints=sum(e['acc']>=.98 for e in es))
            allmetrics[arm][seed]=ms
            replay_g=[g for g in gs if g['replay_ids']]
            ids=[i for s in log['selections'] for i in s['selected_ids']]
            sr['arms'][arm]=dict(**log['guards'],distinct_replayed=len(set(ids)),
                zero_score_slots=[s['zero_score_slots'] for s in log['selections']],
                uniform_overlap=[s['uniform_overlap'] for s in log['selections']],
                template_counts=[sum(facts[i]['idx']%5==t for i in ids) for t in range(5)],
                length_counts=dict(sorted(Counter(lengths[i] for i in ids).items())),
                replay_count_histogram=dict(sorted(Counter(counts).items())),
                replay_mean_deterioration=st.mean(s['scores'][i] for s in log['selections'] for i in s['selected_ids']),
                replay_gradient_mean=st.mean(g['preclip_norm'] for g in replay_g),
                replay_clip_scale_mean=st.mean(g['clip_scale'] for g in replay_g),
                replay_clipped_fraction=st.mean(int(g['clip_scale']<1) for g in replay_g),
                replay_coefficient_mean=st.mean(g['replay_coefficient'] for g in replay_g),
                clipped_replay_coefficient_mean=st.mean(g['clipped_replay_coefficient'] for g in replay_g),
                final_displacement=end['param_dist'],eligible_retention=st.mean(e['eligible_acc'] for e in es),
                initially_unlearned_retention=st.mean(e['initially_unlearned_acc'] for e in es),
                retention_foil_nll=st.mean(e['nll_foil'] for e in es))
        u,p=logs['uniform'],logs['prioritized']
        for a,b in zip(u['step_guards'],p['step_guards']):
            for key in ('step','filler_sha256','filler_tokens','new_ids','fact_tokens','replay_tokens','row_lengths'):
                assert a[key]==b[key]
        for step in (50,100):
            a=next(e for e in u['evals'] if e['int_step']==step)
            b=next(e for e in p['evals'] if e['int_step']==step)
            sr['pre_replay_drift'][step]=dict(accuracy=b['acc']-a['acc'],nll=b['nll']-a['nll'],
                max_per_fact_nll=max(abs(x-y) for x,y in zip(a['per_fact_nll'],b['per_fact_nll'])),
                correctness_disagreements=sum(x!=y for x,y in zip(a['per_fact_correct'],b['per_fact_correct'])))
        report['seeds'][seed]=sr
    summary=read(OUT/'summary.json')
    assert summary['complete_pairs']==3 and summary['complete_continuations']==6
    table=(OUT/'REPORT.md').read_text()
    for metric in allmetrics['uniform'][9]:
        a=[allmetrics['uniform'][s][metric] for s in SEEDS]
        b=[allmetrics['prioritized'][s][metric] for s in SEEDS]
        stats=dict(uniform=desc(a),prioritized=desc(b),prioritized_minus_uniform=desc([y-x for x,y in zip(a,b)]))
        report['metrics'][metric]=stats
        fmt=lambda v:f"{v['mean']:.5f} +/- {v['sample_sd']:.5f} [{v['min']:.5f}, {v['max']:.5f}]"
        assert f"| {metric} | {fmt(stats['uniform'])} | {fmt(stats['prioritized'])} | {fmt(stats['prioritized_minus_uniform'])} |" in table
        for arm,values in stats.items():
            for k,v in values.items():
                actual=summary['metrics'][metric][arm][k]
                if isinstance(v,list):
                    for x,y in zip(v,actual):close(x,y)
                else:close(v,actual)
    d=report['metrics']['retention_accuracy']['prioritized_minus_uniform']
    expected=('positive_directional_signal' if d['min']>0 and d['mean']>d['sample_sd'] else
              'negative_directional_signal' if d['max']<0 and abs(d['mean'])>d['sample_sd'] else 'mixed_or_inconclusive')
    assert summary['direction']==expected and summary['prediction_supported']==(expected=='positive_directional_signal')
    report['direction']=expected
    for s in SEEDS:
        a,b=allmetrics['uniform'][s]['retention_accuracy'],allmetrics['prioritized'][s]['retention_accuracy']
        assert f'| {s} | {a:.6f} | {b:.6f} | {b-a:+.6f} |' in table
    report['guard_summaries']={}
    keys=('distinct_replayed','replay_mean_deterioration','replay_gradient_mean','replay_clip_scale_mean',
          'replay_clipped_fraction','replay_coefficient_mean','clipped_replay_coefficient_mean',
          'final_displacement','eligible_retention','initially_unlearned_retention','retention_foil_nll','wall_seconds')
    for key in keys:
        a=[report['seeds'][s]['arms']['uniform'][key] for s in SEEDS]
        b=[report['seeds'][s]['arms']['prioritized'][key] for s in SEEDS]
        report['guard_summaries'][key]=dict(uniform=desc(a),prioritized=desc(b),prioritized_minus_uniform=desc([y-x for x,y in zip(a,b)]))
    report['common_summaries']={k:desc([report['seeds'][s][k] for s in SEEDS]) for k in
                              ('eligible_count','common_accuracy','common_nll','last_exposure_accuracy','prefix_wall_seconds')}
    report['limitations']=['No new model evaluation: NLL values verified by aggregation, not by recomputing logits.',
        'New-fact accuracy/NLL and filler loss are logged aggregates; per-item new-fact predictions were not retained.',
        'Saved fork and logged branch-state hashes verify common initialization; final branch weights were not saved.',
        'Read-only secondary guard summaries are post-run reporting, not new primary tests.']
    finite(report)
    (OUT/'audit.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    lines=['# Study 12 completion audit','',
        'PASS. Post-run verification only, not a new experiment or new registered hypothesis.',
        'Reproduce: `uv run --no-sync python results/study12/audit_results.py`.',
        'The frozen training/analysis source, tests, dependencies and manifest are unchanged.','',
        '## Checks','',
        '- Registration dd3e56c -> implementation d19c63f -> manifest 59cf386 -> launch record eb38dcc; Git ancestry and committed source bytes verified.',
        '- Every model/tokenizer file, dataset, dependency version, Python version and frozen source file matches the manifest.',
        '- Three saved model/optimizer forks hash to the recorded branch starts. Adam moments are populated, step counters are 800, and learning rate/betas/weight decay match.',
        '- Full acquisition and new-fact schedules rebuilt; every one of 11,400 logged update rows has the expected filler bytes, item IDs, token lengths, replay timing and loss/clipping coefficients.',
        '- All 24 replay selections independently rebuilt from the saved reference/current scores and length slots; eligibility, uniqueness, seeded ties and fallback counts match.',
        '- Old-fact accuracy reconstructed from saved generated answers; NLL and foil aggregates reconstructed from per-fact arrays. All 30 summary blocks and generated report table entries match.',
        '- No extra training, seed replacement, partial failed attempts or model inference was performed by this audit.','',
        '## Common acquisition','',
        'Values in seed order 9,10,11; every spread below is sample SD, not a confidence interval.','',
        '| Quantity | Seed values | Mean +/- SD [min,max] |','|---|---|---|']
    for k,v in report['common_summaries'].items():
        lines.append(f"| {k} | {v['values']} | {fmt(v)} |")
    lines+=['','## Paired secondary guard summaries','',
            'Means aggregate one value per seed; gradient/clipping quantities first average replay updates within each seed.',
            'These are descriptive checks, not additional primary hypothesis tests.','',
            '| Quantity | Uniform | Prioritized | Prioritized minus uniform |','|---|---|---|---|']
    for k,v in report['guard_summaries'].items():
        lines.append(f"| {k} | {fmt(v['uniform'])} | {fmt(v['prioritized'])} | {fmt(v['prioritized_minus_uniform'])} |")
    lines+=['','## Exact per-pair budgets and allocation','',
            'Each continuation has 1500 updates, 80 old replays, 200 new-fact exposures, and 1,440,000 filler input tokens.',
            'Paired lengths match at every update; padded row counts and replay loss coefficients therefore match too.',
            'Template order: capital, birthplace, river/lake, currency, founder. Histograms include all 200 old facts.','']
    for seed,s in report['seeds'].items():
        lines += [f'### Seed {seed}','',f"Pre-replay drift: `{json.dumps(s['pre_replay_drift'],sort_keys=True)}`",'']
        for arm,v in s['arms'].items():
            keys=('replay_tokens','fact_tokens','distinct_replayed','zero_score_slots','uniform_overlap','template_counts','length_counts','replay_count_histogram')
            lines += [f"{arm}: `{json.dumps({k:v[k] for k in keys},sort_keys=True)}`",'']
    lines+=['## Audit limits','']+['- '+v for v in report['limitations']]
    (OUT/'AUDIT.md').write_text('\n'.join(lines)+'\n')
    print('PASS: frozen provenance, checkpoint and optimizer, three paired schedules, 11400 steps, 24 selections, raw old-fact aggregates and 30 summary blocks')
    print(json.dumps({k:report[k] for k in ('direction','common_summaries','guard_summaries')},indent=2))


if __name__=='__main__':
    main()
