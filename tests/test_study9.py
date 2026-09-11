import copy
import importlib
import importlib.util

import numpy as np
import pytest

from spacinglab import schedule


def module():
    assert importlib.util.find_spec("spacinglab.study9") is not None, "Missing Study 9 runner"
    return importlib.import_module("spacinglab.study9")


def test_variable_gaps_have_registered_multiset_and_identical_endpoints():
    assert hasattr(schedule, "permuted_gap_schedule"), "Missing variable-gap scheduling"
    for seed in (0, 1, 2):
        last = schedule.draw_last_exposures(200, 5, 64, 700, seed)
        sched = schedule.permuted_gap_schedule(last, 5, seed+40000)
        assert schedule.exposure_count(sched) == 1000
        orders = set()
        for i, p in enumerate(last):
            ts = sorted(t for t, ids in sched.items() if i in ids)
            assert len(ts) == len(set(ts)) == 5
            assert ts[0] == p-256 and ts[-1] == p
            gaps = np.diff(ts).tolist()
            assert sorted(gaps) == [32, 32, 64, 128]
            orders.add(tuple(gaps))
        assert len(orders) > 1
        assert sched == schedule.permuted_gap_schedule(last, 5, seed+40000)


def test_variable_gap_rejects_wrong_budget():
    assert hasattr(schedule, "permuted_gap_schedule")
    for last, k in [(np.array([200]), 5), (np.array([300]), 4)]:
        with pytest.raises(ValueError):
            schedule.permuted_gap_schedule(last, k, 0)


def test_study9_is_six_fresh_pinned_runs():
    m = module()
    assert len(m.ORDER) == len(set(m.ORDER)) == 6
    assert {c for c,s in m.ORDER} == {"spaced", "variable_gaps"}
    assert m.OUT.name == "study9"
    for c,s in m.ORDER:
        cfg = m.config(c,s)
        assert cfg.tag == "study9" and cfg.offline and cfg.collect_step_guards


def test_pair_validator_checks_first_time_and_gap_multiset():
    m = module()
    from test_study7_runner import fake_log
    a,b = fake_log("spaced"), fake_log("variable_gaps")
    for log in (a,b):
        log["config"].update(n_facts=1,k=5,t_inj=300)
        log["step_guards"] = [{}]*302
        log["last_exposure"] = [256]
    a["target_schedule"] = {str(t):[0] for t in [0,64,128,192,256]}
    b["target_schedule"] = {str(t):[0] for t in [0,32,64,128,256]}
    m.validate_pair(a,b)
    for ts in ([1,32,64,128,256], [0,31,64,128,256]):
        bad = copy.deepcopy(b)
        bad["target_schedule"] = {str(t):[0] for t in ts}
        with pytest.raises(ValueError, match="first-exposure|gap multiset"):
            m.validate_pair(a,bad)
