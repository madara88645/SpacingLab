import importlib
import importlib.util
from dataclasses import asdict

import numpy as np
import pytest


def module():
    assert importlib.util.find_spec('spacinglab.study11') is not None, 'Missing replication runner'
    return importlib.import_module('spacinglab.study11')


def test_replication_has_exactly_six_new_seed_runs_and_unchanged_training():
    from spacinglab.study9 import config as original
    m = module()
    assert m.ORDER == [('spaced',6), ('variable_gaps',6), ('variable_gaps',7),
                       ('spaced',7), ('spaced',8), ('variable_gaps',8)]
    assert m.OUT.name == 'study11'
    for condition, seed in m.ORDER:
        current = asdict(m.config(condition, seed))
        previous = asdict(original(condition, seed))
        assert current.pop('tag') == 'study11'
        previous.pop('tag')
        assert current == previous


def test_replication_rejects_unregistered_seeds_and_conditions():
    m = module()
    for condition, seed in [('spaced',0), ('spaced',3), ('spaced',9), ('random',6)]:
        with pytest.raises(ValueError, match='Unregistered'):
            m.config(condition, seed)


def test_replication_preserves_three_seed_rule():
    m = module()
    assert m.direction([.1,.2,.15]) == 'positive_directional_signal'
    assert m.direction([-.1,-.2,-.15]) == 'negative_directional_signal'
    assert m.direction([.1,.05,-.02]) == 'mixed_or_inconclusive'
    with pytest.raises(ValueError):
        m.direction([.1]*6)


def test_new_seed_schedules_keep_exact_endpoints_and_gap_multisets():
    m = module()
    for seed in (6,7,8):
        last = m.draw_last_exposures(200,5,64,700,seed)
        regular = m.gap_schedule(last,5,64)
        varied = m.permuted_gap_schedule(last,5,seed+40000)
        for i in range(200):
            a = sorted(t for t,ids in regular.items() if i in ids)
            b = sorted(t for t,ids in varied.items() if i in ids)
            assert len(a) == len(b) == 5
            assert a[0] == b[0] == last[i]-256
            assert a[-1] == b[-1] == last[i]
            assert sorted(np.diff(b).tolist()) == [32,32,64,128]


def test_manifest_freezes_new_seeds_both_registrations_and_detects_drift(tmp_path, monkeypatch):
    import hashlib
    m = module()
    for folder in ('data','spacinglab','docs','model'):
        (tmp_path/folder).mkdir()
    data = tmp_path/'data/wikitext103_tokens.npy'
    np.save(data, np.zeros(2233600, dtype=np.uint16))
    for name in ('uv.lock','pyproject.toml','docs/STUDY9_PREREGISTRATION.md',
                 'docs/STUDY10_PREREGISTRATION.md','docs/STUDY11_PREREGISTRATION.md','model/model.safetensors'):
        (tmp_path/name).write_text('fixture')
    monkeypatch.setattr(m,'ROOT',tmp_path)
    monkeypatch.setattr(m,'OUT',tmp_path/'results')
    monkeypatch.setattr(m,'MODEL',tmp_path/'model')
    monkeypatch.setattr(m,'FILLER_SHA',hashlib.sha256(data.read_bytes()).hexdigest())
    first = m.freeze_manifest()
    assert set(first['streams']) == {'6','7','8'}
    assert 'docs/STUDY9_PREREGISTRATION.md' in first['source_sha256']
    assert 'docs/STUDY10_PREREGISTRATION.md' in first['source_sha256']
    assert 'docs/STUDY11_PREREGISTRATION.md' in first['source_sha256']
    assert m.freeze_manifest() == first
    (tmp_path/'docs/STUDY9_PREREGISTRATION.md').write_text('changed')
    with pytest.raises(ValueError,match='Manifest mismatch'):
        m.freeze_manifest()


def test_analysis_uses_new_three_seeds_without_old_results(tmp_path, monkeypatch):
    from test_study7_runner import fake_log
    m = module()
    logs = {}
    for condition,seed in m.ORDER:
        log = fake_log(condition)
        log['config'].update(seed=seed, n_facts=1,k=5,t_inj=300)
        log['step_guards'] = [dict(clip_scale=1.,preclip_norm=.5,
            target_coefficient_sum=.1,clipped_target_coefficient_sum=.1)]*302
        log['last_exposure'] = [256]
        ts = [0,64,128,192,256] if condition=='spaced' else [0,32,64,128,256]
        log['target_schedule'] = {str(t):[0] for t in ts}
        log['guards'].update(acc_at_last_exposure=.8,nll_at_last_exposure=.2)
        log['train_loss'] = [[0,1.]]
        acc = .2 if condition=='spaced' else .2+{6:.1,7:.05,8:-.02}[seed]
        log['evals'] = [dict(phase='immediate',acc=.8,nll=.2,holdout_loss=1.)]
        for step in (50,100,200,400,800,1200,1500):
            log['evals'].append(dict(phase='interference',int_step=step,acc=acc,
                nll=1.-acc,disc=.5,int_facts_acc=.9,int_facts_nll=.1,
                holdout_loss=1.,param_dist=1.))
        logs[condition,seed]=log
    monkeypatch.setattr(m,'OUT',tmp_path)
    monkeypatch.setattr(m,'load_log',lambda condition,seed: logs[condition,seed])
    result = m.analyze()
    assert result['complete_runs']==6
    assert [g['seed'] for g in result['pre_intervention_guards']] == [6,7,8]
    delta = result['metrics']['retention_accuracy']['variable_gaps_minus_spaced']
    assert delta['values'] == pytest.approx([.1,.05,-.02])
    assert result['direction'] == 'mixed_or_inconclusive'
    assert 'Studies 9 and 10 are not pooled' in (tmp_path/'REPORT.md').read_text()


def test_direction_gate_is_strict_and_never_claims_significance():
    m = module()
    assert m.direction([0., .01, .02]) == 'mixed_or_inconclusive'
    assert m.direction([.001, .001, .1]) == 'mixed_or_inconclusive'
    assert m.direction([.02, .03, .04]) == 'positive_directional_signal'
    with pytest.raises(ValueError):
        m.direction([.1, float('nan'), .2])
