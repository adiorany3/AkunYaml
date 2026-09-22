from pathlib import Path

import feed_guard


def test_feed_guard_rejects_html_and_keeps_last_known_good(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("FEED_REFRESH_TTL_SEC", "0")
    monkeypatch.setattr(feed_guard, "_feed_specs", lambda: [feed_guard.FeedSpec("test", "https://example.test", "domain", 2)])
    monkeypatch.setattr(feed_guard, "_fetch", lambda url, timeout=20: b"one.example\ntwo.example\n")
    first = feed_guard.refresh_security_feeds(tmp_path, log=lambda *_: None)
    assert first["test"]["status"] == "updated"
    good = tmp_path / ".feed_cache" / "last_good" / "test.txt"
    before = good.read_bytes()

    monkeypatch.setattr(feed_guard, "_fetch", lambda url, timeout=20: b"<!doctype html><html>access denied</html>")
    second = feed_guard.refresh_security_feeds(tmp_path, log=lambda *_: None)
    assert second["test"]["status"] == "last-known-good"
    assert good.read_bytes() == before
