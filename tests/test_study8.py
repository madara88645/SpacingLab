import copy
import importlib
import importlib.util

import numpy as np
import pytest

from spacinglab import schedule
from spacinglab.train import schedule_last_exposures


def module():
    assert importlib.util.find_spec("spacinglab.study8") is not None, "Missing Study 8 runner"
    return importlib.import_module("spacinglab.study8")


def test_matched_random_preserves_exact_last_times_and_five_distinct_exposures():
    assert hasattr(schedule, "matched_random_schedule"), "Missing last-matched placement"
    for seed in (0, 1, 2):
        last = schedule.draw_last_exposures(200, 5, 64, 700, seed)
        sched = schedule.matched_random_schedule(last, 5, seed + 30000)
        np.testing.assert_array_equal(last, schedule_last_exposures(sched, 200))
        assert schedule.exposure_count(sched) == 1000
        for i in range(200):
            times = [t for t, ids in sched.items() if i in ids]
            assert len(times) == len(set(times)) == 5
            assert min(times) >= 0 and max(times) < 700
        assert sched == schedule.matched_random_schedule(last, 5, seed + 30000)
        assert sched != schedule.gap_schedule(last, 5, 64)


def test_invalid_matched_window_is_rejected():
    assert hasattr(schedule, "matched_random_schedule")
    with pytest.raises(ValueError):
        schedule.matched_random_schedule(np.array([2]), 5, 0)


def test_study8_planned_runs_are_fresh_and_named_correctly():
    m = module()
    assert len(m.ORDER) == len(set(m.ORDER)) == 6
    assert set(c for c, s in m.ORDER) == {"spaced", "random_matched"}
    for c, s in m.ORDER:
        cfg = m.config(c, s)
        assert cfg.tag == "study8" and cfg.t_inj == 700 and cfg.k == 5
        assert cfg.offline and cfg.collect_step_guards
    assert m.OUT.name == "study8"


def test_pair_validation_rejects_actual_exposure_mismatch():
    m = module()
    from test_study7_runner import fake_log
    a, b = fake_log("spaced"), fake_log("random_matched")
    a["config"].update(n_facts=1, k=5, t_inj=300)
    b["config"].update(n_facts=1, k=5, t_inj=300)
    a["step_guards"] = b["step_guards"] = [{}] * 302
    a["last_exposure"] = b["last_exposure"] = [256]
    a["target_schedule"] = {str(t): [0] for t in [0, 64, 128, 192, 256]}
    b["target_schedule"] = {str(t): [0] for t in [1, 45, 80, 220, 256]}
    m.validate_pair(a, b)
    bad = copy.deepcopy(b)
    bad["last_exposure"] = [255]
    with pytest.raises(ValueError, match="last-exposure"):
        m.validate_pair(a, bad)
    bad = copy.deepcopy(b)
    bad["target_schedule"].pop("256")
    with pytest.raises(ValueError, match="exposure"):
        m.validate_pair(a, bad)
