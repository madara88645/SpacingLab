import numpy as np
import pytest
import torch

from spacinglab import train
from spacinglab.schedule import random_schedule


def test_random_last_exposure_probe_uses_actual_last_occurrence():
    assert hasattr(train, "schedule_last_exposures"), "Missing actual-last-exposure guard"
    sched = random_schedule(8, 5, 30, seed=2)
    last = train.schedule_last_exposures(sched, 8)
    for i in range(8):
        assert last[i] == max(t for t, shown in sched.items() if i in shown)
    with pytest.raises(ValueError, match="missing"):
        train.schedule_last_exposures({0: [0]}, 2)


def test_clipping_diagnostic_matches_pytorch_applied_scale():
    assert hasattr(train, "training_step_guard"), "Missing clipping/weight diagnostic"
    p = torch.nn.Parameter(torch.zeros(2))
    p.grad = torch.tensor([3.0, 4.0])
    norm = torch.nn.utils.clip_grad_norm_([p], 1.0)
    g = train.training_step_guard(7, 15, 2, 0, float(norm))
    assert g["preclip_norm"] == 5.0
    assert g["clip_scale"] == pytest.approx(1 / (5 + 1e-6))
    assert g["target_coefficient_sum"] == pytest.approx(2 / 17)
    assert g["clipped_target_coefficient_sum"] == pytest.approx(2 / 17 * g["clip_scale"])
    np.testing.assert_allclose(p.grad.numpy(), np.array([3., 4.]) * g["clip_scale"], rtol=1e-6)


def test_no_clip_and_nonfinite_guard():
    assert hasattr(train, "training_step_guard"), "Missing finite-value guard"
    g = train.training_step_guard(0, 15, 0, 1, .5)
    assert g["clip_scale"] == 1
    assert g["target_coefficient_sum"] == 0
    with pytest.raises(ValueError, match="Nonfinite"):
        train.training_step_guard(0, 15, 1, 0, float("nan"))


def test_config_supports_pinned_offline_model_and_opt_in_diagnostics():
    fields = train.Config.__dataclass_fields__
    assert {"model_revision", "offline", "collect_step_guards"} <= fields.keys()
