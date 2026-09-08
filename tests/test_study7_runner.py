import copy
import importlib
import importlib.util

import pytest


def module():
    assert importlib.util.find_spec("spacinglab.study7") is not None, "Missing Study 7 runner"
    return importlib.import_module("spacinglab.study7")


def fake_log(condition):
    return {"config": {"condition": condition, "seed": 0, "t_pre": 1, "t_inj": 1, "t_int": 1},
            "provenance": {k: "same" for k in ("train_sha256", "heldout_sha256", "filler_file_sha256",
                             "model_revision", "packages")}, "facts": [{"id": 1}], "int_facts": [],
            "interference_schedule": {}, "step_guards": [{}, {}, {}],
            "guards": {k: 3 for k in ("optimizer_steps", "filler_tokens_seen", "fact_tokens_seen", "exposures", "int_exposures")}}


def test_direction_rule_uses_all_seeds_and_sd_and_reports_no_equivalence():
    m = module()
    assert m.direction([.1, .2, .15]) == "positive_directional_signal"
    assert m.direction([-.1, -.2, -.15]) == "negative_directional_signal"
    assert m.direction([-.01, .02, .03]) == "mixed_or_inconclusive"
    assert m.direction([0., 0., 0.]) == "mixed_or_inconclusive"


def test_describe_keeps_seed_values_and_sample_spread():
    s = module().describe([1., 2., 3.])
    assert s == {"values": [1., 2., 3.], "mean": 2., "sample_sd": 1., "min": 1., "max": 3.}


def test_pair_validation_rejects_changed_data_and_counts():
    m = module()
    a, b = fake_log("spaced"), fake_log("random")
    m.validate_pair(a, b)
    for category, key in [("provenance", "train_sha256"), ("guards", "optimizer_steps")]:
        changed = copy.deepcopy(b)
        changed[category][key] = "changed"
        with pytest.raises(ValueError, match="mismatch"):
            m.validate_pair(a, changed)


def test_file_manifest_changes_when_contents_change(tmp_path):
    m = module()
    p = tmp_path / "file"
    p.write_text("first")
    first = m.file_sha(p)
    p.write_text("second")
    assert first != m.file_sha(p)


def test_planned_runs_are_fresh_pinned_pairs():
    m = module()
    assert len(m.ORDER) == 6
    assert len(set(m.ORDER)) == 6
    for condition, seed in m.ORDER:
        c = m.config(condition, seed)
        assert c.t_inj == 700 and c.k == 5
        assert c.offline and c.collect_step_guards and c.filler_sha256 and c.model_revision
