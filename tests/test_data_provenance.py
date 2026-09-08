"""Regression tests: a seed alone does not identify a shuffled filler stream."""
import hashlib

import numpy as np
import pytest

from spacinglab import data


def snapshot(tmp_path, tokens):
    path = tmp_path / "tokens.npy"
    np.save(path, tokens)
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


def test_verified_snapshot_is_read_only_and_does_not_get_truncated(tmp_path):
    expected = np.arange(128, dtype=np.uint16)
    path, sha = snapshot(tmp_path, expected)
    actual = data.load_filler_snapshot(path, sha, required_tokens=64)
    np.testing.assert_array_equal(actual, expected)
    assert not actual.flags.writeable


def test_cache_extension_is_rejected_even_when_original_prefix_is_identical(tmp_path):
    path, sha = snapshot(tmp_path, np.arange(128, dtype=np.uint16))
    np.save(path, np.arange(256, dtype=np.uint16))
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        data.load_filler_snapshot(path, sha, required_tokens=64)


def test_insufficient_snapshot_is_rejected_without_growth(tmp_path):
    path, sha = snapshot(tmp_path, np.arange(64, dtype=np.uint16))
    with pytest.raises(ValueError, match="Insufficient"):
        data.load_filler_snapshot(path, sha, required_tokens=128)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha


@pytest.mark.parametrize("tokens", [np.zeros((2, 4), dtype=np.uint16), np.arange(8.0)])
def test_invalid_token_arrays_are_rejected(tmp_path, tokens):
    path, sha = snapshot(tmp_path, tokens)
    with pytest.raises(ValueError, match="one-dimensional integer"):
        data.load_filler_snapshot(path, sha, required_tokens=4)


def test_stream_provenance_identifies_data_without_consuming_it():
    tokens = np.arange(4096, dtype=np.uint16)
    a = data.FillerStream(tokens, seq_len=8, seed=0, n_holdout=20)
    b = data.FillerStream(tokens, seq_len=8, seed=0, n_holdout=20)
    assert a.provenance(n_train=200) == b.provenance(n_train=200)
    assert a.pos == b.pos == 0
    extended = data.FillerStream(np.arange(8192, dtype=np.uint16), 8, 0, 20)
    assert a.provenance(200)["train_sha256"] != extended.provenance(200)["train_sha256"]
    assert a.provenance(200)["heldout_sha256"] != extended.provenance(200)["heldout_sha256"]
    with pytest.raises(ValueError, match="Insufficient"):
        a.provenance(n_train=1000)


def test_independent_audit_matches_actual_stream_selection():
    from spacinglab.provenance_audit import fingerprint
    tokens = np.arange(4096, dtype=np.uint16)
    for seed in (0, 1, 2):
        # fingerprint uses 200 holdout chunks; provide enough unique chunk contents.
        longer = np.tile(tokens, 5)
        independent = fingerprint(longer, seed=seed, steps=3)
        actual = data.FillerStream(longer, seq_len=64, seed=seed).provenance(45)
        assert independent["heldout_sha256"] == actual["heldout_sha256"]
        assert independent["train_sha256"] == actual["train_sha256"]
