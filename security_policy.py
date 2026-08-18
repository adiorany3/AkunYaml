"""Shared security/adblock policy for every ConvertYAML output.

This module is the single source of truth for remote security provider metadata
and the order of provider-backed REJECT rules.  Platform-specific inline rules
remain in the generator because they are not remote feeds.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

DEFAULT_PROVIDER_INTERVAL = 43200


def _http_domain(path: str, url: str, *, fmt: str = "text", interval: int = DEFAULT_PROVIDER_INTERVAL) -> dict[str, Any]:
    item: dict[str, Any] = {
        "type": "http",
        "behavior": "domain",
        "path": path,
        "url": url,
        "interval": int(interval),
    }
    if fmt:
        item["format"] = fmt
    return item


def _http_classical(path: str, url: str, *, interval: int = DEFAULT_PROVIDER_INTERVAL) -> dict[str, Any]:
    return {
        "type": "http",
        "behavior": "classical",
        "path": path,
        "url": url,
        "interval": int(interval),
    }


def _http_ipcidr(path: str, url: str, *, fmt: str = "text", interval: int = DEFAULT_PROVIDER_INTERVAL) -> dict[str, Any]:
    item: dict[str, Any] = {
        "type": "http",
        "behavior": "ipcidr",
        "path": path,
        "url": url,
        "interval": int(interval),
    }
    if fmt:
        item["format"] = fmt
    return item


# Router/OpenClash provider catalog.
ROUTER_BASE_PROVIDERS: dict[str, dict[str, Any]] = {
    "ads_indonesia": _http_domain(
        "./rule_providers/ads_indonesia.txt",
        "https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt",
    ),
    "ads_domain": _http_domain(
        "./rule_providers/ads_domain.mrs",
        "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ads-all.mrs",
        fmt="mrs",
    ),
    "tracker-domain": _http_domain(
        "./rule_providers/tracker.mrs",
        "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/tracker.mrs",
        fmt="mrs",
    ),
    "threat-tif-mini": _http_domain(
        "./rule_providers/threat-tif-mini.txt",
        "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/tif.mini-onlydomains.txt",
    ),
}

ROUTER_STRICT_PROVIDERS: dict[str, dict[str, Any]] = {
    "hagezi-pro-mini": _http_domain(
        "./rule_providers/hagezi-pro-mini.txt",
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro.mini-onlydomains.txt",
    ),
    "popup-ads": _http_domain(
        "./rule_providers/popup-ads.txt",
        "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/popupads-onlydomains.txt",
    ),
}

ROUTER_THREAT_SAFE_PROVIDERS: dict[str, dict[str, Any]] = {
    "threat-malware": _http_domain(
        "./rule_providers/threat-malware.txt",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/malware.txt",
    ),
    "threat-phishing": _http_domain(
        "./rule_providers/threat-phishing.txt",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/phishing.txt",
    ),
    "threat-cryptominers": _http_domain(
        "./rule_providers/threat-cryptominers.txt",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/cryptominers.txt",
    ),
    "threat-fake-scam": _http_domain(
        "./rule_providers/threat-fake-scam.txt",
        "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/fake-onlydomains.txt",
    ),
}

ROUTER_THREAT_IP_PROVIDERS: dict[str, dict[str, Any]] = {
    "threat-tif-ip": _http_ipcidr(
        "./rule_providers/threat-tif-ip.txt",
        "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/ips/tif.txt",
    ),
}

# Android keeps YAML-only remote providers for older bundled cores.  ABPindo is
# generated locally as a YAML snapshot by feed_guard.py because the upstream DNS
# feed is plain text.
ANDROID_BASE_PROVIDERS: dict[str, dict[str, Any]] = {
    "ads_indonesia": {
        "type": "file",
        "behavior": "domain",
        "path": "./rule_providers/ads_indonesia_android.yaml",
    },
    "ads_domain": _http_domain(
        "./rule_providers/ads_domain.yaml",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/category-ads-all.yaml",
        fmt="",
    ),
    "tracker-domain": _http_classical(
        "./rule_providers/tracker.yaml",
        "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/classical/tracker.yaml",
    ),
    "threat-malware": _http_domain(
        "./rule_providers/malware.yaml",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/malware.yaml",
        fmt="",
    ),
    "threat-phishing": _http_domain(
        "./rule_providers/phishing.yaml",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/phishing.yaml",
        fmt="",
    ),
    "threat-cryptominers": _http_domain(
        "./rule_providers/cryptominers.yaml",
        "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/cryptominers.yaml",
        fmt="",
    ),
}

ANDROID_STRICT_PROVIDERS: dict[str, dict[str, Any]] = {
    "privacy-extra": _http_classical(
        "./rule_providers/privacy-extra.yaml",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Privacy/Privacy.yaml",
    ),
}


def _with_interval(catalog: dict[str, dict[str, Any]], interval: int) -> dict[str, dict[str, Any]]:
    result = deepcopy(catalog)
    for provider in result.values():
        if provider.get("type") == "http":
            provider["interval"] = int(interval)
    return result


def provider_catalog(
    *,
    platform: str,
    profile: str,
    lite: bool = False,
    indonesia_ads: bool = True,
    threat_ip: bool = True,
    interval: int = DEFAULT_PROVIDER_INTERVAL,
    android_snapshot_exists: bool = True,
) -> dict[str, dict[str, Any]]:
    """Return the complete provider catalog required by the selected profile."""
    profile = (profile or "balanced").strip().lower()
    platform = platform.strip().lower()
    if profile == "off":
        return {}

    if platform == "android":
        out = _with_interval(ANDROID_BASE_PROVIDERS, interval)
        if not indonesia_ads or not android_snapshot_exists:
            out.pop("ads_indonesia", None)
        if profile in {"strict", "child-safe", "app-safe", "threat-safe"}:
            out.update(_with_interval(ANDROID_STRICT_PROVIDERS, interval))
        return out

    out = _with_interval(ROUTER_BASE_PROVIDERS, interval)
    if not indonesia_ads:
        out.pop("ads_indonesia", None)
    if profile in {"strict", "child-safe", "app-safe", "threat-safe"} and not lite:
        out.update(_with_interval(ROUTER_STRICT_PROVIDERS, interval))
    if profile == "threat-safe":
        out.update(_with_interval(ROUTER_THREAT_SAFE_PROVIDERS, interval))
        if threat_ip and not lite:
            out.update(_with_interval(ROUTER_THREAT_IP_PROVIDERS, interval))
    return out


def provider_reject_rules(
    *,
    platform: str,
    profile: str,
    lite: bool = False,
    indonesia_ads: bool = True,
    threat_ip: bool = True,
    android_snapshot_exists: bool = True,
) -> list[str]:
    """Return provider-backed REJECT rules in deterministic precision order."""
    profile = (profile or "balanced").strip().lower()
    platform = platform.strip().lower()
    if profile == "off":
        return []

    rules: list[str] = []
    if platform == "android":
        rules.extend([
            "RULE-SET,threat-malware,REJECT",
            "RULE-SET,threat-phishing,REJECT",
            "RULE-SET,threat-cryptominers,REJECT",
        ])
        if profile in {"strict", "child-safe", "app-safe", "threat-safe"}:
            rules.append("RULE-SET,privacy-extra,REJECT")
        if indonesia_ads and android_snapshot_exists:
            rules.append("RULE-SET,ads_indonesia,REJECT")
        rules.extend([
            "RULE-SET,ads_domain,REJECT",
            "RULE-SET,tracker-domain,REJECT",
        ])
        return rules

    if profile == "threat-safe":
        rules.extend([
            "RULE-SET,threat-malware,REJECT",
            "RULE-SET,threat-phishing,REJECT",
            "RULE-SET,threat-cryptominers,REJECT",
            "RULE-SET,threat-fake-scam,REJECT",
            "RULE-SET,threat-tif-mini,REJECT",
        ])
    else:
        rules.append("RULE-SET,threat-tif-mini,REJECT")

    if profile in {"strict", "child-safe", "app-safe", "threat-safe"} and not lite:
        rules.extend([
            "RULE-SET,hagezi-pro-mini,REJECT",
            "RULE-SET,popup-ads,REJECT",
        ])
    if profile == "threat-safe" and threat_ip and not lite:
        rules.append("RULE-SET,threat-tif-ip,REJECT,no-resolve")
    if indonesia_ads:
        rules.append("RULE-SET,ads_indonesia,REJECT")
    rules.extend([
        "RULE-SET,ads_domain,REJECT",
        "RULE-SET,tracker-domain,REJECT",
    ])
    return rules


def managed_provider_names() -> set[str]:
    names: set[str] = set()
    for catalog in (
        ROUTER_BASE_PROVIDERS,
        ROUTER_STRICT_PROVIDERS,
        ROUTER_THREAT_SAFE_PROVIDERS,
        ROUTER_THREAT_IP_PROVIDERS,
        ANDROID_BASE_PROVIDERS,
        ANDROID_STRICT_PROVIDERS,
    ):
        names.update(catalog)
    return names
