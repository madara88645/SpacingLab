import numpy as np
from spacinglab.schedule import draw_last_exposures, gap_schedule, exposure_count, random_schedule
from spacinglab.facts import make_facts


def test_gap_schedule_matches_last_exposure_and_count():
    last = draw_last_exposures(100, 4, 64, 600, seed=0)
    assert last.min() >= 192 and last.max() < 600
    for gap in (1, 4, 16, 64):
        s = gap_schedule(last, 4, gap)
        assert exposure_count(s) == 400
        # every fact's max step equals its shared last-exposure step
        seen = {}
        for step, ids in s.items():
            for i in ids:
                seen.setdefault(i, []).append(step)
        for i, steps in seen.items():
            assert max(steps) == last[i]
            assert sorted(steps) == [last[i] - j * gap for j in range(3, -1, -1)]


def test_conditions_share_last_exposure():
    a = draw_last_exposures(100, 4, 64, 600, seed=1)
    b = draw_last_exposures(100, 4, 64, 600, seed=1)
    assert np.array_equal(a, b)


def test_random_schedule_count():
    s = random_schedule(100, 4, 600, seed=100)
    assert exposure_count(s) == 400


def test_facts_unique_and_seeded():
    f0, f0b, f1 = make_facts(100, 0), make_facts(100, 0), make_facts(100, 1)
    assert [f.text for f in f0] == [f.text for f in f0b]
    assert [f.text for f in f0] != [f.text for f in f1]
    names = [f.answer for f in f0] + [f.prompt for f in f0]
    assert len(set(names)) == len(names)
