import json

import pytest

import ai_adblock_classifier as classifier


def payload(domain="ads.example"):
    return {"results": [{"domain": domain, "label": "review", "category": "unknown", "confidence": 0.0, "reason": "insufficient evidence"}]}


@pytest.mark.parametrize("wrapper", ["{}", "```json\n{}\n```", "{}\n\nAnalysis complete."])
def test_single_response_wrappers(wrapper):
    content = wrapper.format(json.dumps(payload()))
    assert len(classifier.parse_response(content, ["ads.example"])) == 1


@pytest.mark.parametrize("extra", ['\n{"results": []}', '\n[]', '\n```json\n{}\n```'])
def test_multiple_documents_rejected(extra):
    with pytest.raises(ValueError):
        classifier.parse_response(json.dumps(payload()) + extra, ["ads.example"])


def test_duplicate_json_keys_rejected():
    with pytest.raises(ValueError):
        classifier.parse_response('{"results": [], "results": []}', [])


def test_retry_invalid_batch(tmp_path, monkeypatch):
    (tmp_path / "adblock_ai_candidates.txt").write_text("ads.example\n")
    monkeypatch.setenv("AI_ADBLOCK_API_KEY", "test")
    calls = []

    def batch(*args):
        calls.append(1)
        if len(calls) == 1:
            raise ValueError("invalid JSON")
        return payload()["results"]

    monkeypatch.setattr(classifier, "_classify_batch", batch)
    result = classifier.classify_candidates(tmp_path, base_url="https://example.invalid", model="test", key_file=None, log=lambda *_: None)
    assert result["status"] == "updated"
    assert len(calls) == 2
    assert result["blocked"] == []


def test_persistent_bad_response_still_fails_open(tmp_path, monkeypatch):
    (tmp_path / "adblock_ai_candidates.txt").write_text("ads.example\n")
    monkeypatch.setenv("AI_ADBLOCK_API_KEY", "test")
    calls = []

    def batch(*args):
        calls.append(1)
        raise ValueError("ambiguous response")

    monkeypatch.setattr(classifier, "_classify_batch", batch)
    result = classifier.classify_candidates(tmp_path, base_url="https://example.invalid", model="test", key_file=None, log=lambda *_: None)
    assert result["status"] == "failed-open"
    assert len(calls) == 2
    assert not (tmp_path / ".runtime_cache/ai_adblock_blocklist.txt").exists()