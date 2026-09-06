#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory

from ai_adblock_classifier import refresh_streaming_candidates


with TemporaryDirectory() as tmp:
    root = Path(tmp)
    feed = root / ".feed_cache" / "last_good"
    feed.mkdir(parents=True)
    (root / "adblock_allowlist.txt").write_text("netflix.com\n", encoding="utf-8")
    (feed / "hagezi-pro-plus-mini.txt").write_text(
        "ads.spotify.com\nopen.spotify.com\nlogs.netflix.com\nanalytics.example.com\n",
        encoding="utf-8",
    )
    (feed / "popup-ads.txt").write_text("pixel.spotify.com\n", encoding="utf-8")
    found = refresh_streaming_candidates(root, log=lambda _: None)
    assert found == ["ads.spotify.com", "pixel.spotify.com"], found
    assert (root / ".runtime_cache" / "ai_adblock_candidates.txt").exists()

print("OK")
