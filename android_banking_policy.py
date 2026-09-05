"""Android banking compatibility policy.

This policy is Android-only. Banking endpoints are kept on real DNS, skipped by
TLS/HTTP sniffing, and routed DIRECT before privacy/ad/tracker rules. High-
confidence malware/phishing/cryptominer rules still run first.

This module does not attempt to hide the VPN or bypass an application's device
security checks. A bank app that rejects any active VPN may still require the
Android VPN client's per-app exclusion feature.
"""
from __future__ import annotations

import json
import os
import re
from typing import Iterable

DEFAULT_SUFFIX_DOMAINS = (
    "seabank.co.id",
)

DEFAULT_EXACT_DOMAINS: tuple[str, ...] = ()

ALL_BANK_SUFFIX_DOMAINS = (
    "blu.co.id", "jago.com", "seabank.co.id", "bca.co.id", "klikbca.com",
    "mybca.co.id", "bankmandiri.co.id", "livinbymandiri.co.id", "bri.co.id",
    "bni.co.id", "btn.co.id", "cimbniaga.co.id", "octo.co.id", "danamon.co.id",
    "permatabank.com", "panin.co.id", "ocbc.id", "ocbcnisp.com", "maybank.co.id",
    "hsbc.co.id", "uob.co.id", "dbs.com", "dbs.id", "sc.com", "citibank.co.id",
    "bankmega.com", "bankmega.co.id", "btpn.com", "jenius.com", "bankjago.com",
    "bankneo.co.id", "allobank.com", "bankraya.co.id", "bankaladin.co.id",
    "bankina.co.id", "bankbsi.co.id", "bankmuamalat.co.id",
    "bankmega-syariah.co.id", "bcasyariah.co.id", "btpnsyariah.com",
    "bankvictoriasyariah.co.id", "banksinarmas.com", "bankmas.co.id",
    "bankmestika.co.id", "bankmayapada.com", "bankcapital.co.id",
    "bankganesha.co.id", "bankindex.co.id", "bankmayora.com",
    "bankwoorisaudara.com", "kebhana.co.id", "shinhan.co.id", "bankbisnis.com",
    "banksampoerna.com", "banknobu.com", "bankbjb.co.id", "bankdki.co.id",
    "bankjateng.co.id", "bankjatim.co.id", "bpddiy.co.id", "banksumut.co.id",
    "bankaceh.co.id", "banknagari.co.id", "bankriaukepri.co.id",
    "banksumselbabel.com", "banklampung.co.id", "bankkalbar.co.id",
    "bankkalsel.co.id", "bankkalteng.co.id", "bankaltimtara.co.id",
    "banksulselbar.co.id", "banksulutgo.co.id", "bankntbsyariah.co.id",
    "bpdbali.co.id", "bpdntt.co.id", "bankmalukumalut.co.id", "bankpapua.co.id",
)


def all_bank_suffix_domains() -> tuple[str, ...]:
    """Return bank domains routed through Sing-box manual nodes."""
    return ALL_BANK_SUFFIX_DOMAINS


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() not in {"0", "false", "no", "off", "disabled"}


def enabled() -> bool:
    return _env_bool("ANDROID_BANKING_SAFE_MODE", True)


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
    return _parse_env_list("ANDROID_BANKING_DOMAINS", DEFAULT_SUFFIX_DOMAINS)


def exact_domains() -> tuple[str, ...]:
    if not enabled():
        return ()
    return _parse_env_list("ANDROID_BANKING_EXACT_DOMAINS", DEFAULT_EXACT_DOMAINS)


def guard_rules() -> list[str]:
    if not enabled():
        return []
    rules = [f"DOMAIN,{domain},DIRECT" for domain in exact_domains()]
    rules.extend(f"DOMAIN-SUFFIX,{domain},DIRECT" for domain in suffix_domains())
    return rules


def fake_ip_filters() -> list[str]:
    if not enabled():
        return []
    values = [f"+.{domain}" for domain in suffix_domains()]
    values.extend(exact_domains())
    return list(dict.fromkeys(values))


def sniffer_skip_domains() -> list[str]:
    if not enabled():
        return []
    values = [f"+.{domain}" for domain in suffix_domains()]
    values.extend(exact_domains())
    return list(dict.fromkeys(values))


def dns_policy_domains() -> tuple[str, ...]:
    if not enabled():
        return ()
    return tuple(dict.fromkeys((*suffix_domains(), *exact_domains())))
