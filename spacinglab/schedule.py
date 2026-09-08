"""Exposure schedules: which fact is shown at which training step.

A schedule is a dict step -> list of fact indices shown at that step (on top of the
filler). The last-exposure step p_i of each fact is drawn once per seed and shared by
all gap conditions, so the time since a fact's last exposure is identical across
conditions (this removes the recency confound).
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np


def draw_last_exposures(n_facts: int, k: int, gap_max: int, t_inj: int, seed: int) -> np.ndarray:
    """p_i ~ Uniform[(k-1)*gap_max, t_inj) so that every gap <= gap_max fits."""
    lo = (k - 1) * gap_max
    assert t_inj - lo >= 350, "injection window too narrow for the range of p_i"
    rng = np.random.default_rng(seed)
    return rng.integers(lo, t_inj, size=n_facts)


def gap_schedule(last: np.ndarray, k: int, gap: int) -> dict[int, list[int]]:
    """Fact i is shown at steps last[i] - j*gap for j = 0..k-1."""
    sched: dict[int, list[int]] = defaultdict(list)
    for i, p in enumerate(last.tolist()):
        for j in range(k):
            step = p - j * gap
            assert step >= 0
            sched[step].append(i)
    return dict(sched)


def random_schedule(n_facts: int, k: int, t_inj: int, seed: int) -> dict[int, list[int]]:
    """Pilot-only placement: k distinct uniformly random steps per fact."""
    rng = np.random.default_rng(seed)
    sched: dict[int, list[int]] = defaultdict(list)
    for i in range(n_facts):
        for step in rng.choice(t_inj, size=k, replace=False).tolist():
            sched[step].append(i)
    return dict(sched)


def exposure_count(sched: dict[int, list[int]]) -> int:
    return sum(len(v) for v in sched.values())


def matched_random_schedule(last: np.ndarray, k: int, seed: int) -> dict[int, list[int]]:
    """Uniform earlier exposures conditional on each item's prescribed final step."""
    if k < 1 or any(p < k - 1 for p in last):
        raise ValueError("Not enough distinct steps before the prescribed last exposure")
    rng = np.random.default_rng(seed)
    sched: dict[int, list[int]] = defaultdict(list)
    for i, p in enumerate(last.tolist()):
        earlier = rng.choice(p, size=k - 1, replace=False).tolist()
        for step in earlier + [p]:
            sched[step].append(i)
    return dict(sched)


def permuted_gap_schedule(last: np.ndarray, k: int, seed: int) -> dict[int, list[int]]:
    """Five exposures with permuted gaps 32,32,64,128; both endpoints fixed."""
    if k != 5 or any(p < 256 for p in last):
        raise ValueError("Variable-gap policy requires five exposures and a 256-step span")
    rng = np.random.default_rng(seed)
    sched: dict[int, list[int]] = defaultdict(list)
    for i, p in enumerate(last.tolist()):
        step = p - 256
        sched[step].append(i)
        for gap in rng.permutation([32, 32, 64, 128]):
            step += int(gap)
            sched[step].append(i)
    return dict(sched)
