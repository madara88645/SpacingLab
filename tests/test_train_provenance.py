"""Fail closed before loading a model or overwriting an existing experiment."""
import pytest
import numpy as np

from spacinglab import train


def forbid_model_loading(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Model loading happened before input validation")
    monkeypatch.setattr(train.AutoTokenizer, "from_pretrained", forbidden)


def test_existing_result_cannot_be_overwritten(tmp_path, monkeypatch):
    forbid_model_loading(monkeypatch)
    (tmp_path / "log.json").write_text("original")
    with pytest.raises(FileExistsError):
        train.run(train.Config(condition="spaced", seed=0), tmp_path)
    assert (tmp_path / "log.json").read_text() == "original"


@pytest.mark.parametrize("field,value", [("filler_snapshot", "missing.npy"),
                                          ("filler_sha256", "0" * 64)])
def test_incomplete_snapshot_configuration_fails_before_model_load(tmp_path, monkeypatch, field, value):
    forbid_model_loading(monkeypatch)
    cfg = train.Config(condition="spaced", seed=0)
    setattr(cfg, field, value)
    with pytest.raises(ValueError, match="together"):
        train.run(cfg, tmp_path)


def test_changed_snapshot_is_rejected_before_model_load(tmp_path, monkeypatch):
    forbid_model_loading(monkeypatch)
    path = tmp_path / "changed.npy"
    np.save(path, np.arange(128, dtype=np.uint16))
    cfg = train.Config(condition="spaced", seed=0,
                       filler_snapshot=str(path), filler_sha256="0" * 64)
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        train.run(cfg, tmp_path / "run")
    assert not (tmp_path / "run").exists()
