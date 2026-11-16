"""Tests for adblock_protection_audit: rule ordering, critical allowlist, and engine parity."""
import json
from pathlib import Path

import yaml

from adblock_protection_audit import (
    audit_feed_cache,
    audit_openclash,
    audit_singbox,
)


def test_audit_openclash_passes_current_outputs():
    for name in ("openclash_auto.yaml", "openclash_android.yaml", "openclash_lite.yaml", "openclash_fresh_pool.yaml"):
        path = Path(name)
        if path.exists():
            errors = audit_openclash(path)
            assert not errors, f"{name} audit failed: {errors}"


def test_audit_openclash_rejects_direct_mode(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump({
        "mode": "direct",
        "dns": {"enable": True},
        "rule-providers": {"ads_domain": {}, "tracker-domain": {}},
        "rules": ["RULE-SET,ads_domain,REJECT", "RULE-SET,tracker-domain,REJECT", "MATCH,GLOBAL"],
    }))
    assert any("mode harus rule" in err for err in audit_openclash(p))


def test_audit_openclash_rejects_critical_allowlist_domain_rejection(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text(yaml.safe_dump({
        "mode": "rule",
        "dns": {"enable": True},
        "rule-providers": {"ads_domain": {}, "tracker-domain": {}},
        "rules": [
            "DOMAIN,challenges.cloudflare.com,REJECT",
            "RULE-SET,ads_domain,REJECT",
            "RULE-SET,tracker-domain,REJECT",
            "MATCH,GLOBAL",
        ],
    }))
    assert any("domain allowlist kritis ditolak" in err for err in audit_openclash(p))


def test_audit_singbox_passes_current_output():
    p = Path("singbox_android.json")
    if p.exists():
        assert not audit_singbox(p)


def test_audit_singbox_rejects_missing_ads_reject(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({
        "dns": {"servers": [{"tag": "local"}]},
        "route": {
            "rule_set": [{"tag": "ads-domain"}, {"tag": "tracker-domain"}],
            "rules": [{"outbound": "direct"}],
            "final": "proxy",
        },
    }))
    assert any("reject" in err for err in audit_singbox(p))


def test_audit_feed_cache_passes_when_feeds_valid():
    p = Path(".feed_cache/metadata.json")
    if p.exists():
        assert not audit_feed_cache(p)
