"""Android marketplace-live compatibility policy.

This policy is intentionally Android-only.  It protects first-party marketplace
and live-media endpoints from broad ad/tracker filters without weakening the
high-confidence malware/phishing/cryptominer layer.
"""
from __future__ import annotations

import json
import os
import re
from typing import Iterable

DEFAULT_SUFFIX_DOMAINS = (
    # Shopee / Shopee Live.
    "shopee.co.id",
    "shopee.com",
    "shopee.sg",
    "shopeemobile.com",
    "shopeeusercontent.com",
    "susercontent.com",
    "shp.ee",
    # Tokopedia.
    "tokopedia.com",
    "tokopedia.net",
    # Lazada / live-media CDN.
    "lazada.co.id",
    "lazada.com",
    "lzd.co",
    "lazcdn.com",
    "slatic.net",
    # Other large Indonesian marketplaces.
    "blibli.com",
    "bukalapak.com",
    # TikTok Shop / Live media.  Deliberately do NOT whitelist the whole
    # tiktok.com suffix so explicit advertising hosts can remain blocked.
    "tiktokv.com",
    "tiktokcdn.com",
    "ibytedtos.com",
    "byteimg.com",
)

DEFAULT_EXACT_DOMAINS = (
    # This host was previously classified with advertising endpoints even though
    # it can be required by TikTok Shop/business session flows.
    "business-api.tiktok.com",
    # Keep this exact rather than whitelisting *.byteoversea.com, which would be
    # unnecessarily broad.  Some TikTok app flows wait on this endpoint.
    "log.byteoversea.com",
)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off", "disabled"}


def enabled() -> bool:
    return _env_bool("ANDROID_MARKETPLACE_LIVE_COMPAT", True)


def route_policy() -> str:
    value = (os.getenv("ANDROID_MARKETPLACE_LIVE_POLICY", "GLOBAL").strip() or "GLOBAL")
    # Avoid accidental REJECT/PASS-like values from a typo.  DIRECT remains an
    # explicit opt-in, while GLOBAL is the compatibility default.
    if value.upper() in {"REJECT", "REJECT-DROP", "PASS", "COMPATIBLE"}:
        return "GLOBAL"
    return value


def _normalize_domain(value: str) -> str | None:
    domain = str(value or "").strip().lower().rstrip(".")
    domain = re.sub(r"^https?://", "", domain).split("/", 1)[0]
    if domain.startswith("+.") or domain.startswith("*."):
        domain = domain[2:]
    if not domain or ".." in domain:
        return None
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", domain):
        return None
    if "." not in domain:
        return None
    return domain


def _parse_env_list(name: str, defaults: Iterable[str]) -> tuple[str, ...]:
    raw = os.getenv(name, "").strip()
    values: list[str]
    if not raw:
        values = list(defaults)
    else:
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = None
        if isinstance(parsed, list):
            values = [str(item) for item in parsed]
        else:
            values = re.split(r"[,\n;]+", raw)

    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        domain = _normalize_domain(value)
        if not domain or domain in seen:
            continue
        seen.add(domain)
        result.append(domain)
    return tuple(result)


def suffix_domains() -> tuple[str, ...]:
    if not enabled():
        return ()
    return _parse_env_list("ANDROID_MARKETPLACE_LIVE_DOMAINS", DEFAULT_SUFFIX_DOMAINS)


def exact_domains() -> tuple[str, ...]:
    if not enabled():
        return ()
    return _parse_env_list("ANDROID_MARKETPLACE_LIVE_EXACT_DOMAINS", DEFAULT_EXACT_DOMAINS)


def guard_rules(policy: str | None = None) -> list[str]:
    if not enabled():
        return []
    target = policy or route_policy()
    rules = [f"DOMAIN,{domain},{target}" for domain in exact_domains()]
    rules.extend(f"DOMAIN-SUFFIX,{domain},{target}" for domain in suffix_domains())
    return rules


def fake_ip_filters() -> list[str]:
    if not enabled():
        return []
    values = [f"+.{domain}" for domain in suffix_domains()]
    values.extend(exact_domains())
    return list(dict.fromkeys(values))


def sniffer_skip_domains() -> list[str]:
    # Suffix form is supported by Mihomo skip-domain.  Exact entries are kept as
    # exact hostnames so the list stays conservative.
    if not enabled():
        return []
    values = [f"+.{domain}" for domain in suffix_domains()]
    values.extend(exact_domains())
    return list(dict.fromkeys(values))


def dns_policy_domains() -> tuple[str, ...]:
    if not enabled():
        return ()
    # Exact domains do not need dedicated entries when already under one of the
    # suffix domains.  Return both forms for deterministic config generation.
    return tuple(dict.fromkeys((*suffix_domains(), *exact_domains())))
