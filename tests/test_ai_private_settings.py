import json

import pytest

from ai_adblock_classifier import _read_ai_settings, _read_api_key


@pytest.mark.parametrize("private_model,expected_model", [("selected-model", "selected-model"), ("", "test")])
def test_classifier_uses_private_endpoint(tmp_path, monkeypatch, private_model, expected_model):
    import ai_adblock_classifier as classifier

    path = tmp_path / "ai.key"
    path.write_text(json.dumps({"api_key": "private-key", "base_url": "https://private.example/v1", "model": private_model}))
    path.chmod(0o600)
    (tmp_path / "adblock_ai_candidates.txt").write_text("ads.example.org\n")
    monkeypatch.delenv("AI_ADBLOCK_API_KEY", raising=False)
    calls = []

    def fake_batch(base_url, model, api_key, domains, timeout):
        calls.append((base_url, api_key, model))
        return [{"domain": d, "label": "review", "category": "unknown", "confidence": 0.0, "reason": "test"} for d in domains]

    monkeypatch.setattr(classifier, "_classify_batch", fake_batch)
    classifier.classify_candidates(tmp_path, base_url="https://old.example/v1", model="test", key_file=path, log=lambda message: None)
    assert calls == [("https://private.example/v1", "private-key", expected_model)]


def test_json_settings(tmp_path, monkeypatch):
    monkeypatch.delenv("AI_ADBLOCK_API_KEY", raising=False)
    path = tmp_path / "ai.key"
    path.write_text(json.dumps({"api_key": "test-key", "base_url": "https://example.com/v1"}))
    path.chmod(0o600)
    assert _read_api_key(path) == "test-key"
    assert _read_ai_settings(path)["base_url"] == "https://example.com/v1"


def test_legacy_and_environment(tmp_path, monkeypatch):
    path = tmp_path / "ai.key"
    path.write_text("legacy-key\n")
    path.chmod(0o600)
    monkeypatch.delenv("AI_ADBLOCK_API_KEY", raising=False)
    assert _read_api_key(path) == "legacy-key"
    monkeypatch.setenv("AI_ADBLOCK_API_KEY", "override")
    assert _read_api_key(path) == "override"


def test_invalid_json_redacted(tmp_path):
    path = tmp_path / "ai.key"
    path.write_text('{"secret-value"')
    path.chmod(0o600)
    with pytest.raises(ValueError) as exc:
        _read_ai_settings(path)
    assert "secret-value" not in str(exc.value)


def test_permissions(tmp_path):
    path = tmp_path / "ai.key"
    path.write_text("key")
    path.chmod(0o644)
    with pytest.raises(PermissionError):
        _read_ai_settings(path)