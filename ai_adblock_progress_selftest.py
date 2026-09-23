#!/usr/bin/env python3
"""Run directly; no network or persistent output."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ai_adblock_classifier import classify_candidates


def main():
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "adblock_ai_candidates.txt").write_text("one.example\ntwo.example\n")
        logs = []

        def respond(base_url, model, key, domains, timeout):
            return [{"domain": domain, "label": "review", "category": "unknown",
                     "confidence": 0.0, "reason": "test"} for domain in domains]

        with patch("ai_adblock_classifier._read_api_key", return_value="test"), patch(
            "ai_adblock_classifier._classify_batch", side_effect=respond
        ):
            result = classify_candidates(root, base_url="https://example.invalid", model="test",
                                         key_file=None, batch_size=1, log=logs.append)
        assert result["status"] == "updated"
        assert any("batch 2/2" in line for line in logs)
        assert any("2/2 (100%)" in line for line in logs)
        assert "selesai" in logs[-1]
        assert (root / ".runtime_cache/ai_adblock_report.json").exists()
        logs.clear()
        with patch("ai_adblock_classifier._read_api_key", return_value="test"), patch(
            "ai_adblock_classifier._classify_batch", side_effect=ValueError("test failure")
        ):
            result = classify_candidates(root, base_url="https://example.invalid", model="test",
                                         key_file=None, batch_size=1, log=logs.append)
        assert result["status"] == "failed-open"
        assert "fail-open setelah 0/2" in logs[-1]
        assert not any("selesai" in line for line in logs)
    print("OK: progress, completion, failure logs")


if __name__ == "__main__":
    main()
