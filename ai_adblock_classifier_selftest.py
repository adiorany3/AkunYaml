#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from ai_adblock_classifier import classify_candidates, is_allowlisted, parse_response


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[OK] {message}")


def main() -> int:
    expected = ["ads.example", "api.example"]
    payload = {"results": [
        {"domain": "ads.example", "label": "block", "category": "advertising", "confidence": 0.99, "reason": "dedicated ad host"},
        {"domain": "api.example", "label": "allow", "category": "service", "confidence": 1.0, "reason": "service API"},
    ]}
    parsed = parse_response(json.dumps(payload), expected)
    check(parsed[0]["label"] == "block", "strict response parsed")

    malformed = json.dumps({"results": payload["results"][:1]})
    try:
        parse_response(malformed, expected)
    except ValueError:
        pass
    else:
        raise AssertionError("incomplete response accepted")
    check(True, "incomplete response rejected")
    check(is_allowlisted("telemetry.linkedin.com", {"linkedin.com"}), "parent allowlist protects subdomain")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        output = root / ".runtime_cache" / "ai_adblock_blocklist.txt"
        output.parent.mkdir()
        output.write_text("stale.example\n", encoding="utf-8")
        (root / "adblock_allowlist.txt").write_text("linkedin.com\n", encoding="utf-8")
        (root / "adblock_ai_candidates.txt").write_text("telemetry.linkedin.com\n", encoding="utf-8")
        result = classify_candidates(root, base_url="https://ai.tamandata.com/v1", model="tamandata", key_file=None, log=lambda *_: None)
        check(result["status"] == "skipped", "allowlist precedence skips API classification")
        check(not output.exists(), "skipped classification removes stale block rules")

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        output = root / ".runtime_cache" / "ai_adblock_blocklist.txt"
        output.parent.mkdir()
        output.write_text("stale.example\n", encoding="utf-8")
        (root / "adblock_allowlist.txt").write_text("", encoding="utf-8")
        (root / "adblock_ai_candidates.txt").write_text("ads.example\n", encoding="utf-8")
        result = classify_candidates(root, base_url="https://ai.tamandata.com/v1", model="tamandata", key_file=None, log=lambda *_: None)
        check(result["status"] == "skipped", "missing key skips classification")
        check(not output.exists(), "missing key removes stale block rules")

    print("[OK] AI adblock classifier self-test complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
