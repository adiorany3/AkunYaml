from __future__ import annotations

import base64
import concurrent.futures
import csv
import html
import io
import json
import os
import re
import socket
import ssl
import statistics
import time
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

import requests
import yaml


class _NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def dump_yaml_no_alias(data: dict[str, Any]) -> str:
    return yaml.dump(data, Dumper=_NoAliasDumper, allow_unicode=True, sort_keys=False, width=140)




def _enforce_no_selector_no_direct_config(config: dict[str, Any]) -> dict[str, Any]:
    """Force automatic proxy groups and prevent proxy-group DIRECT fallback.

    DIRECT is still allowed in LAN/private rules. This function only cleans
    proxy-groups so OpenClash reload cannot leave selectors on DIRECT.
    """
    if not isinstance(config, dict):
        return config
    groups = config.get("proxy-groups")
    if not isinstance(groups, list):
        return config

    proxy_names: list[str] = []
    for proxy in config.get("proxies", []) or []:
        if isinstance(proxy, dict) and proxy.get("name"):
            proxy_names.append(str(proxy["name"]))

    group_names = [str(g.get("name")) for g in groups if isinstance(g, dict) and g.get("name")]
    automatic_defaults = [
        "WARM-UP",
        "WARM-UP-CF",
        "AUTO-FAST",
        "STREAMING-FAST",
        "FALLBACK",
        "LOAD-BALANCE",
        "PING-CHECK",
    ]

    def dedupe(values: list[str]) -> list[str]:
        out: list[str] = []
        seen: set[str] = set()
        for value in values:
            if not value or value in seen:
                continue
            seen.add(value)
            out.append(value)
        return out

    def clean_refs(name: str, values: Any) -> list[str]:
        refs: list[str] = []
        for value in values or []:
            text = str(value).strip()
            if not text or text == "DIRECT" or text == name:
                continue
            refs.append(text)
        refs = dedupe(refs)
        if refs:
            return refs
        fallback_refs = [x for x in automatic_defaults if x in group_names and x != name]
        fallback_refs += [x for x in proxy_names if x != name]
        fallback_refs = dedupe(fallback_refs)
        return fallback_refs or ["REJECT"]

    for group in groups:
        if not isinstance(group, dict):
            continue
        name = str(group.get("name") or "")
        gtype = str(group.get("type") or "").lower()
        if gtype == "select":
            group["type"] = "fallback"
            group.setdefault("url", "https://www.gstatic.com/generate_204")
            group.setdefault("interval", 15 if name == "GLOBAL" else 30)
            group.setdefault("lazy", False)
            group.setdefault("timeout", 3000)
            group.setdefault("expected-status", "200/204/301/302")
            group.setdefault("max-failed-times", 2)
        if isinstance(group.get("proxies"), list):
            group["proxies"] = clean_refs(name, group.get("proxies"))
    return config

def _env_int_range(name: str, default: int, minimum: int, maximum: int) -> int:
    """Read integer env safely and clamp it for stable generated YAML."""
    raw = os.getenv(name, "").strip()
    try:
        value = int(raw) if raw else int(default)
    except ValueError:
        value = int(default)
    return max(minimum, min(maximum, value))


def _mihomo_keep_alive_config() -> dict[str, Any]:
    """Global TCP keep-alive tuning to reduce idle/hibernating proxy sessions."""
    return {
        "keep-alive-interval": _env_int_range("KEEP_ALIVE_INTERVAL", 15, 5, 120),
        "keep-alive-idle": _env_int_range("KEEP_ALIVE_IDLE", 600, 15, 3600),
        "disable-keep-alive": False,
    }


def _active_health_interval(interval: int) -> int:
    """Use a shorter active health-check interval without allowing extreme values."""
    return _env_int_range("WAKEUP_INTERVAL", max(20, min(int(interval), 30)), 15, 300)


def _delay_from_proxy_name(name: str) -> int:
    """Extract delay suffix from names like AKUN-001-...-86MS for smart ranking."""
    match = re.search(r"(\d+)MS\b", str(name).upper())
    return int(match.group(1)) if match else 999999


def _dedupe_names(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        item = str(value or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _rank_names_by_delay(names: list[str]) -> list[str]:
    clean_names = [str(n) for n in names if str(n) and str(n) != "DIRECT"]
    original_index = {name: idx for idx, name in enumerate(clean_names)}
    return sorted(clean_names, key=lambda n: (_delay_from_proxy_name(n), original_index[n]))


def _is_cloudflare_like(name: str) -> bool:
    upper = str(name or "").upper()
    return any(token in upper for token in ("CLOUDFLARE", "WORKER", "WORKERS", "CF-", "-CF", "DEV-"))


def _select_fast_pool_names(names: list[str]) -> list[str]:
    """Tier-2 pool: quick enough for AUTO-FAST, but not as aggressive as WARM-UP."""
    ranked = _rank_names_by_delay(names)
    if not ranked:
        return []
    limit = _env_int_range("FAST_NODE_LIMIT", 12, 5, 30)
    max_delay = _env_int_range("FAST_MAX_DELAY_MS", 700, 120, 3000)
    good = [name for name in ranked if _delay_from_proxy_name(name) <= max_delay]
    pool = good or ranked
    return pool[: min(limit, len(pool))]


def _select_warmup_names(names: list[str]) -> list[str]:
    """Tier-1 pool: small hot pool to keep daily nodes awake without overloading the router."""
    ranked = _rank_names_by_delay(names)
    if not ranked:
        return []
    limit = _env_int_range("WARMUP_NODE_LIMIT", 7, 3, 12)
    max_delay = _env_int_range("WARMUP_MAX_DELAY_MS", 180, 80, 1000)
    preferred = [name for name in ranked if _delay_from_proxy_name(name) <= max_delay]
    pool = preferred or ranked
    return pool[: min(limit, len(pool))]


def _select_cf_warmup_names(names: list[str]) -> list[str]:
    """Dedicated Cloudflare/Worker warm-up pool with its own health endpoint."""
    ranked = _rank_names_by_delay([name for name in names if _is_cloudflare_like(name)])
    if not ranked:
        return []
    limit = _env_int_range("CF_WARMUP_NODE_LIMIT", 5, 2, 12)
    max_delay = _env_int_range("CF_WARMUP_MAX_DELAY_MS", 350, 100, 2000)
    preferred = [name for name in ranked if _delay_from_proxy_name(name) <= max_delay]
    pool = preferred or ranked
    return pool[: min(limit, len(pool))]


def _select_streaming_names(names: list[str], warmup_names: list[str] | None = None, cf_names: list[str] | None = None) -> list[str]:
    """Streaming pool prioritizes Cloudflare/WS nodes, then the general warm pool."""
    limit = _env_int_range("STREAMING_NODE_LIMIT", 8, 3, 16)
    fast_names = _select_fast_pool_names(names)
    ordered = _dedupe_names((cf_names or []) + (warmup_names or []) + fast_names + _rank_names_by_delay(names))
    return ordered[: min(limit, len(ordered))]


def _fallback_order_names(names: list[str], warmup_names: list[str] | None = None, cf_names: list[str] | None = None) -> list[str]:
    """Fallback should try strict automatic nodes first; manual nodes are appended later by generate_yaml.py."""
    return _dedupe_names((warmup_names or []) + (cf_names or []) + _rank_names_by_delay(names))


SMART_FAKE_IP_FILTER = [
    "+.lan",
    "+.local",
    "localhost.ptlogin2.qq.com",
    "dns.msftncsi.com",
    "www.msftconnecttest.com",
    "connectivitycheck.gstatic.com",
    "connect.rom.miui.com",
    "time.*.com",
    "ntp.*.com",
    "+.pool.ntp.org",
    "router.asus.com",
    "tplinkwifi.net",
    "tendawifi.com",
    "+.bca.co.id",
    "+.bni.co.id",
    "+.bri.co.id",
    "+.mandiri.co.id",
]




# -----------------------------
# Manual unblock domain routing
# -----------------------------
def _strip_inline_comment(line: str) -> str:
    """Strip comments in simple txt lists without damaging URL fragments too much."""
    text = str(line or "").strip()
    if not text:
        return ""
    for marker in (" //", "\t//"):
        if marker in text:
            text = text.split(marker, 1)[0].strip()
    # Treat # as a comment when it starts a line or is preceded by whitespace.
    if text.startswith("#"):
        return ""
    match = re.search(r"\s+#", text)
    if match:
        text = text[: match.start()].strip()
    return text.strip()


def _domain_from_manual_line(line: str) -> tuple[str, str] | None:
    """Convert one manual_unblock_domains.txt line into a Clash rule tuple.

    Supported active line formats:
      example.com
      *.example.com
      +.example.com
      https://example.com/path
      DOMAIN,example.com
      DOMAIN-SUFFIX,example.com
      DOMAIN-KEYWORD,keyword
      GEOSITE,category
    The target policy is always injected later as MANUAL.
    """
    text = _strip_inline_comment(line)
    if not text:
        return None
    text = text.strip().strip('"\'')
    if not text:
        return None

    upper = text.upper()
    if "," in text:
        parts = [p.strip() for p in text.split(",") if p.strip()]
        if len(parts) >= 2:
            kind = parts[0].upper()
            value = parts[1].strip().strip('"\'')
            if kind in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "GEOSITE"} and value:
                return kind, value.lower() if kind != "DOMAIN-KEYWORD" else value

    # Remove URL scheme/path/query if a full URL is pasted.
    if "://" in text:
        parsed = urlparse(text)
        text = parsed.hostname or parsed.netloc or text
    else:
        text = text.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]

    text = text.strip().strip(".").lower()
    for prefix in ("+.", "*.", "."):
        if text.startswith(prefix):
            text = text[len(prefix):].strip(".")
            break
    if not text or " " in text or ":" in text:
        return None
    if "*" in text:
        return None
    if looks_like_ip(text):
        return "IP-CIDR", f"{text}/32"
    if re.fullmatch(r"[a-z0-9][a-z0-9.-]*\.[a-z]{2,}", text):
        return "DOMAIN-SUFFIX", text
    return None


def _read_manual_unblock_domains_file() -> list[str]:
    path = os.getenv("MANUAL_UNBLOCK_DOMAINS_FILE", "manual_unblock_domains.txt").strip() or "manual_unblock_domains.txt"
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return handle.readlines()
    except FileNotFoundError:
        return []
    except Exception:
        return []


def _manual_unblock_domain_rules(target: str = "MANUAL") -> list[str]:
    """Build high-priority rules so listed domains always use the MANUAL group."""
    target = str(target or "MANUAL").strip() or "MANUAL"
    rules: list[str] = []
    seen: set[str] = set()
    for raw_line in _read_manual_unblock_domains_file():
        item = _domain_from_manual_line(raw_line)
        if not item:
            continue
        kind, value = item
        if kind == "IP-CIDR":
            rule = f"IP-CIDR,{value},{target},no-resolve"
        else:
            rule = f"{kind},{value},{target}"
        if rule not in seen:
            seen.add(rule)
            rules.append(rule)
    return rules


def _inject_manual_unblock_rules(rules: list[str], target: str = "MANUAL") -> list[str]:
    """Insert manual-unblock rules after LAN/DIRECT rules and before reject/category rules."""
    manual_rules = _manual_unblock_domain_rules(target=target)
    if not manual_rules:
        return rules

    out: list[str] = []
    seen: set[str] = set()
    for rule in rules:
        if rule not in seen:
            seen.add(rule)
            out.append(rule)

    # Remove older generated manual rules if this function is called repeatedly.
    out = [r for r in out if r not in manual_rules]

    insert_at = 0
    for idx, rule in enumerate(out):
        text = str(rule)
        if (
            ",DIRECT" in text
            or text.startswith("GEOIP,LAN,")
            or text.startswith("IP-CIDR,127.")
            or text.startswith("IP-CIDR,10.")
            or text.startswith("IP-CIDR,172.16.")
            or text.startswith("IP-CIDR,192.168.")
            or text.startswith("IP-CIDR,169.254.")
        ):
            insert_at = idx + 1
            continue
        break
    return out[:insert_at] + manual_rules + out[insert_at:]

def _valid_mihomo_domain_wildcard(value: str) -> bool:
    """Validate wildcard syntax accepted by Mihomo domain matchers.

    Rules enforced here are intentionally conservative:
    - `+` is only allowed as the `+.` prefix.
    - `*` must occupy a complete DNS label, e.g. `time.*.com`.
    - partial wildcards such as `bank*`, `*bank`, or `foo+` are rejected.
    """
    text = str(value or "").strip()
    if not text or any(ch.isspace() for ch in text):
        return False
    if text.startswith("+."):
        text = text[2:]
        if not text:
            return False
    elif "+" in text:
        return False
    if text.startswith("."):
        text = text[1:]
        if not text:
            return False
    labels = text.split(".")
    if any(not label for label in labels):
        return False
    for label in labels:
        if "*" in label and label != "*":
            return False
    return True


def _dns_fake_ip_filter() -> list[str]:
    raw = SMART_FAKE_IP_FILTER + [
        x.strip() for x in os.getenv("EXTRA_FAKE_IP_FILTER", "").split(",") if x.strip()
    ]
    cleaned: list[str] = []
    for item in _dedupe_names(raw):
        if _valid_mihomo_domain_wildcard(item):
            cleaned.append(item)
        else:
            print(f"[WARN] Abaikan fake-ip-filter domain invalid untuk Mihomo: {item}")
    return cleaned

DEFAULT_LINKS = [
    "https://raw.githubusercontent.com/itsyebekhe/PSG/main/lite/subscriptions/xray/normal/mix",
    "https://raw.githubusercontent.com/arshiacomplus/v2rayExtractor/refs/heads/main/mix/sub.html",
    "https://raw.githubusercontent.com/Rayan-Config/C-Sub/refs/heads/main/configs/proxy.txt",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
    "https://raw.githubusercontent.com/Everyday-VPN/Everyday-VPN/main/subscription/main.txt",
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/config/refs/heads/main/xray_final.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/refs/heads/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/trojan.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vmess_configs.txt",
    "https://raw.githubusercontent.com/Argh94/Proxy-List/refs/heads/main/Trojan.txt",
    "http://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/refs/heads/main/subscriptions/v2ray/all_sub.txt",
    "https://raw.githubusercontent.com/MustafaBaqer/VestraNet-Nodes/refs/heads/main/subscriptions/mix-normal.txt",
    "http://raw.githubusercontent.com/V2RAYCONFIGSPOOL/V2RAY_SUB/refs/heads/main/v2ray_configs_no3.txt",
    "https://raw.githubusercontent.com/amir-reza-bijandi/v2ray-configs/refs/heads/main/configs.txt",
    "https://raw.githubusercontent.com/amirkma/proxykma/refs/heads/main/mix.txt",
    "https://raw.githubusercontent.com/cbusifabcap/daily_free_vpn/refs/heads/main/Z.txt",
    "https://raw.githubusercontent.com/iboxz/free-v2ray-collector/main/main/vmess.txt",
    "https://raw.githubusercontent.com/iboxz/free-v2ray-collector/main/main/vless.txt",
    "https://raw.githubusercontent.com/iboxz/free-v2ray-collector/main/main/trojan.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/v2rayNG-Config/refs/heads/main/server.txt",
    "https://raw.githubusercontent.com/MohammadBahemmat/V2ray-Collector/refs/heads/main/all_servers.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/26.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/25.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/24.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/23.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/22.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/21.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/20.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/19.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/18.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/17.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/16.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/15.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/14.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/13.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/12.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/11.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/10.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/9.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/8.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/7.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/6.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/5.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/4.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/3.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/2.txt",
    "https://raw.githubusercontent.com/nikita29a/FreeProxyList/refs/heads/main/mirror/1.txt",
    "https://raw.githubusercontent.com/sakha1370/OpenRay/refs/heads/main/output/kind/vmess.txt",
    "https://raw.githubusercontent.com/sakha1370/OpenRay/refs/heads/main/output/kind/vless.txt",
    "https://raw.githubusercontent.com/sakha1370/OpenRay/refs/heads/main/output/kind/trojan.txt",
]

TARGET_SERVER = "104.17.3.81"
ONLY_PORT = 443
USER_AGENT = "Mozilla/5.0 SumberYAML-OpenClash-BugCompat/3.0"
URI_RE = re.compile(r"(?:vless|vmess|trojan|ss)://[^\s<'\"`]+", re.IGNORECASE)
FAST_TEST_URL = "http://cp.cloudflare.com/generate_204"
ALT_TEST_URL = "https://www.gstatic.com/generate_204"
THIRD_TEST_URL = "https://www.google.com/generate_204"
FAST_TARGET_DELAY_MS = 123
DEFAULT_FILL_DELAY_MS = 400
HARD_MAX_DELAY_MS = 1500
MIN_OUTPUT_NODES = 20
DEFAULT_URLTEST_INTERVAL = 30
DEFAULT_TOLERANCE_MS = 40
DEFAULT_TCP_TIMEOUT = 1.5
DEFAULT_FETCH_TIMEOUT = 15
DEFAULT_HEALTH_TIMEOUT_MS = 5000
DEFAULT_RESERVE_POOL_NODES = 100
DEFAULT_FORCE_WS_ONLY = True

OPTIMIZATION_PRESETS: dict[str, dict[str, Any]] = {
    "Cepat": {
        "max_nodes": 20,
        "min_output_nodes": 15,
        "fill_delay_ms": 400,
        "attempts": 2,
        "require_successes": 1,
        "tcp_timeout": 1.5,
        "max_workers": 64,
        "fetch_timeout": 10,
        "urltest_interval": 60,
        "tolerance": 50,
        "require_original": False,
        "candidate_multiplier": 40,
        "candidate_min": 1000,
        "reserve_pool_nodes": 60,
        "max_jitter_ms": 200,
        "rule_mode": "Lite",
        "force_ws_only": True,
        "health_timeout_ms": 5000,
    },
    "Seimbang": {
        "max_nodes": 20,
        "min_output_nodes": 20,
        "fill_delay_ms": 800,
        "attempts": 3,
        "require_successes": 2,
        "tcp_timeout": 2.0,
        "max_workers": 64,
        "fetch_timeout": 15,
        "urltest_interval": 60,
        "tolerance": 50,
        "require_original": False,
        "candidate_multiplier": 80,
        "candidate_min": 2000,
        "reserve_pool_nodes": 100,
        "max_jitter_ms": 300,
        "rule_mode": "Lite",
        "force_ws_only": True,
        "health_timeout_ms": 5000,
    },
    "Kejar 20 Hidup": {
        "max_nodes": 20,
        "min_output_nodes": 20,
        "fill_delay_ms": 1200,
        "attempts": 4,
        "require_successes": 3,
        "tcp_timeout": 3.0,
        "max_workers": 80,
        "fetch_timeout": 20,
        "urltest_interval": 60,
        "tolerance": 80,
        "require_original": False,
        "candidate_multiplier": 120,
        "candidate_min": 3000,
        "reserve_pool_nodes": 160,
        "max_jitter_ms": 500,
        "rule_mode": "Lite",
        "force_ws_only": True,
        "health_timeout_ms": 6000,
    },
    "Ketat": {
        "max_nodes": 20,
        "min_output_nodes": 20,
        "fill_delay_ms": 1500,
        "attempts": 5,
        "require_successes": 4,
        "tcp_timeout": 3.0,
        "max_workers": 60,
        "fetch_timeout": 25,
        "urltest_interval": 90,
        "tolerance": 60,
        "require_original": True,
        "candidate_multiplier": 120,
        "candidate_min": 3000,
        "reserve_pool_nodes": 160,
        "max_jitter_ms": 500,
        "rule_mode": "Lengkap",
        "force_ws_only": True,
        "health_timeout_ms": 6000,
    },
}


@dataclass
class ProxyNode:
    name: str
    type: str
    original_server: str
    port: int
    raw: str
    clash: dict[str, Any]
    source: str = "manual"
    status: str = "pending"
    best_delay_ms: int | None = None
    avg_delay_ms: int | None = None
    jitter_ms: int | None = None
    success_count: int = 0
    attempts: int = 0
    score: int = 999999
    reason: str = ""
    original_best_delay_ms: int | None = None
    bug_best_delay_ms: int | None = None
    bug_avg_delay_ms: int | None = None
    bug_jitter_ms: int | None = None
    bug_success_count: int = 0
    original_success_count: int = 0
    bug_sni: str = ""
    ws_upgrade_ms: int | None = None
    ws_success_count: int = 0
    ws_status: str = ""
    original_provider: str = ""
    original_ip: str = ""
    tier: str = ""
    original_name: str = ""
    key: str = field(default="")


def b64decode_text(value: str) -> str | None:
    if not value:
        return None
    cleaned = re.sub(r"\s+", "", value.strip())
    if not cleaned:
        return None
    padding = "=" * (-len(cleaned) % 4)
    candidates = [cleaned + padding, cleaned.replace("-", "+").replace("_", "/") + padding]
    for candidate in candidates:
        try:
            data = base64.b64decode(candidate, validate=False)
            text = data.decode("utf-8", errors="ignore")
            if text and len(text.strip()) >= 4:
                return text
        except Exception:
            continue
    return None


def normalize_name(name: str | None, fallback: str) -> str:
    text = html.unescape(unquote(name or "")).strip()
    text = re.sub(r"[\x00-\x1f\x7f\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text[:70].strip(" -_|/")
    return text or fallback


def safe_proxy_name(value: str | None, fallback: str) -> str:
    """Return an OpenClash-safe proxy name.

    Public subscription names often contain emoji, quotes, slashes, hidden newline,
    YAML-reserved characters, or duplicate text. Some OpenClash builds reject those
    names. This function converts every proxy name to a short ASCII-only alias.
    """
    text = html.unescape(unquote(value or "")).strip()
    text = re.sub(r"[\x00-\x1f\x7f]+", "", text)
    text = re.sub(r"[^A-Za-z0-9_.-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-._")
    if not text:
        text = fallback
    text = text[:64].strip("-._") or fallback
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", text):
        text = fallback
    return text


def unique_names(nodes: list[ProxyNode], provider_names: bool = True) -> None:
    """Replace all proxy names with safe unique aliases.

    If provider_names is enabled, the alias uses provider/ASN information from
    the original server, not from the forced bug IP 104.17.3.81. This makes the
    output easier to read, for example AKUN-001-VULTR-VLESS-WS-18MS.
    """
    seen: set[str] = set()
    for i, node in enumerate(nodes, start=1):
        node.original_name = node.original_name or normalize_name(node.name, f"ORIGINAL-{i:03d}")
        delay = f"{int(node.best_delay_ms)}MS" if node.best_delay_ms is not None else "NA"
        proto = safe_proxy_name(node.type.upper(), "NODE")
        net = safe_proxy_name(node_network(node).upper(), "NET")
        provider = provider_label_from_original_server(node) if provider_names else ""
        if provider:
            base = safe_proxy_name(f"AKUN-{i:03d}-{provider}-{proto}-{net}-{delay}", f"AKUN-{i:03d}")
        else:
            base = safe_proxy_name(f"AKUN-{i:03d}-{proto}-{net}-{delay}", f"AKUN-{i:03d}")
        name = base
        counter = 2
        while name in seen:
            suffix = f"-{counter}"
            name = (base[: 64 - len(suffix)] + suffix).strip("-._")
            counter += 1
        seen.add(name)
        node.name = name
        node.clash["name"] = name


def first_query(params: dict[str, list[str]], *names: str, default: str = "") -> str:
    for name in names:
        if name in params and params[name]:
            return params[name][0]
    return default


def is_supported_network(network: str) -> bool:
    return (network or "tcp").lower() in {"tcp", "ws", "grpc", "h2", "http"}


def parse_vless(uri: str, source: str) -> ProxyNode | None:
    parsed = urlparse(uri)
    uuid = parsed.username or ""
    server = parsed.hostname or ""
    port = parsed.port or 0
    if not uuid or not server or port != ONLY_PORT:
        return None

    params = parse_qs(parsed.query)
    network = (first_query(params, "type", default="tcp") or "tcp").lower()
    if not is_supported_network(network):
        return None
    security = (first_query(params, "security", default="tls") or "tls").lower()
    sni = first_query(params, "sni", "servername", "peer", default="") or server
    host = first_query(params, "host", default="") or sni or server
    path = first_query(params, "path", default="/") or "/"
    flow = first_query(params, "flow", default="")
    fp = first_query(params, "fp", default="chrome") or "chrome"
    alpn = first_query(params, "alpn", default="")

    name = normalize_name(parsed.fragment, f"VLESS-{server}")
    clash: dict[str, Any] = {
        "name": name,
        "type": "vless",
        "server": TARGET_SERVER,
        "port": ONLY_PORT,
        "uuid": uuid,
        "udp": True,
        "tls": security in {"tls", "reality"} or port == 443,
        "servername": sni,
        "network": "http" if network == "h2" else network,
        "client-fingerprint": fp,
        "skip-cert-verify": True,
    }
    if flow:
        clash["flow"] = flow
    if alpn:
        clash["alpn"] = [x.strip() for x in alpn.split(",") if x.strip()]
    if network == "ws":
        clash["ws-opts"] = {"path": path, "headers": {"Host": host}}
    elif network == "grpc":
        service_name = first_query(params, "serviceName", "service-name", default="")
        clash["grpc-opts"] = {"grpc-service-name": service_name or "grpc"}
    elif network in {"h2", "http"}:
        clash["http-opts"] = {"method": "GET", "path": [path], "headers": {"Host": [host]}}
    if security == "reality":
        pbk = first_query(params, "pbk", "public-key", default="")
        sid = first_query(params, "sid", "short-id", default="")
        clash["reality-opts"] = {}
        if pbk:
            clash["reality-opts"]["public-key"] = pbk
        if sid:
            clash["reality-opts"]["short-id"] = sid

    key = f"vless|{uuid}|{server}|{port}|{network}|{path}|{host}"
    return ProxyNode(name, "vless", server, port, uri, clash, source=source, key=key)


def parse_trojan(uri: str, source: str) -> ProxyNode | None:
    parsed = urlparse(uri)
    password = parsed.username or ""
    server = parsed.hostname or ""
    port = parsed.port or 0
    if not password or not server or port != ONLY_PORT:
        return None

    params = parse_qs(parsed.query)
    network = (first_query(params, "type", default="tcp") or "tcp").lower()
    if not is_supported_network(network):
        return None
    sni = first_query(params, "sni", "peer", "servername", default="") or server
    host = first_query(params, "host", default="") or sni or server
    path = first_query(params, "path", default="/") or "/"
    alpn = first_query(params, "alpn", default="")

    name = normalize_name(parsed.fragment, f"TROJAN-{server}")
    clash: dict[str, Any] = {
        "name": name,
        "type": "trojan",
        "server": TARGET_SERVER,
        "port": ONLY_PORT,
        "password": unquote(password),
        "udp": True,
        "sni": sni,
        "skip-cert-verify": True,
        "network": "http" if network == "h2" else network,
    }
    if alpn:
        clash["alpn"] = [x.strip() for x in alpn.split(",") if x.strip()]
    if network == "ws":
        clash["ws-opts"] = {"path": path, "headers": {"Host": host}}
    elif network == "grpc":
        service_name = first_query(params, "serviceName", "service-name", default="")
        clash["grpc-opts"] = {"grpc-service-name": service_name or "grpc"}
    elif network in {"h2", "http"}:
        clash["http-opts"] = {"method": "GET", "path": [path], "headers": {"Host": [host]}}

    key = f"trojan|{password}|{server}|{port}|{network}|{path}|{host}"
    return ProxyNode(name, "trojan", server, port, uri, clash, source=source, key=key)


def parse_vmess(uri: str, source: str) -> ProxyNode | None:
    payload = uri.split("://", 1)[1].split("#", 1)[0]
    decoded = b64decode_text(payload)
    if not decoded:
        return None
    try:
        data = json.loads(decoded)
    except Exception:
        return None

    server = str(data.get("add") or data.get("server") or "").strip()
    try:
        port = int(data.get("port") or 0)
    except Exception:
        port = 0
    uuid = str(data.get("id") or "").strip()
    if not server or not uuid or port != ONLY_PORT:
        return None

    network = str(data.get("net") or "tcp").strip().lower() or "tcp"
    if not is_supported_network(network):
        return None
    tls_value = str(data.get("tls") or "tls").strip().lower()
    sni = str(data.get("sni") or data.get("servername") or data.get("serverName") or data.get("host") or server).strip()
    host = str(data.get("host") or sni or server).strip()
    path = str(data.get("path") or "/").strip() or "/"
    cipher = str(data.get("scy") or data.get("cipher") or "auto").strip() or "auto"
    fp = str(data.get("fp") or "chrome").strip() or "chrome"

    name = normalize_name(str(data.get("ps") or ""), f"VMESS-{server}")
    clash: dict[str, Any] = {
        "name": name,
        "type": "vmess",
        "server": TARGET_SERVER,
        "port": ONLY_PORT,
        "uuid": uuid,
        "alterId": int(data.get("aid") or 0),
        "cipher": cipher,
        "udp": True,
        "tls": tls_value in {"tls", "true", "1"} or port == 443,
        "servername": sni,
        "network": "http" if network == "h2" else network,
        "client-fingerprint": fp,
        "skip-cert-verify": True,
    }
    if network == "ws":
        clash["ws-opts"] = {"path": path, "headers": {"Host": host}}
    elif network == "grpc":
        clash["grpc-opts"] = {"grpc-service-name": path.strip("/") or "grpc"}
    elif network in {"h2", "http"}:
        clash["http-opts"] = {"method": "GET", "path": [path], "headers": {"Host": [host]}}

    key = f"vmess|{uuid}|{server}|{port}|{network}|{path}|{host}"
    return ProxyNode(name, "vmess", server, port, uri, clash, source=source, key=key)


def decode_ss_userinfo(userinfo: str) -> tuple[str, str] | None:
    userinfo = unquote(userinfo or "")
    decoded = b64decode_text(userinfo) or userinfo
    if ":" not in decoded:
        return None
    method, password = decoded.split(":", 1)
    method = method.strip()
    password = password.strip()
    if not method or not password:
        return None
    return method, password


def parse_ss(uri: str, source: str) -> ProxyNode | None:
    raw_without_scheme = uri.split("://", 1)[1]
    name = ""
    if "#" in raw_without_scheme:
        raw_without_scheme, name = raw_without_scheme.split("#", 1)
        name = unquote(name)
    raw_without_scheme = raw_without_scheme.split("?", 1)[0]

    method = password = server = ""
    port = 0

    if "@" in raw_without_scheme:
        userinfo, serverpart = raw_without_scheme.rsplit("@", 1)
        credentials = decode_ss_userinfo(userinfo)
        if not credentials:
            return None
        method, password = credentials
        parsed_server = urlparse("ss://" + serverpart)
        server = parsed_server.hostname or ""
        port = parsed_server.port or 0
    else:
        decoded = b64decode_text(raw_without_scheme)
        if not decoded or "@" not in decoded:
            return None
        userinfo, serverpart = decoded.rsplit("@", 1)
        credentials = decode_ss_userinfo(userinfo)
        if not credentials:
            return None
        method, password = credentials
        parsed_server = urlparse("ss://" + serverpart)
        server = parsed_server.hostname or ""
        port = parsed_server.port or 0

    if not server or port != ONLY_PORT:
        return None

    final_name = normalize_name(name, f"SS-{server}")
    clash: dict[str, Any] = {
        "name": final_name,
        "type": "ss",
        "server": TARGET_SERVER,
        "port": ONLY_PORT,
        "cipher": method,
        "password": password,
        "udp": True,
    }
    key = f"ss|{method}|{password}|{server}|{port}"
    return ProxyNode(final_name, "ss", server, port, uri, clash, source=source, key=key)


def parse_uri(uri: str, source: str) -> ProxyNode | None:
    uri = html.unescape(uri.strip()).strip("'\",[]()")
    if not uri or "://" not in uri:
        return None
    scheme = uri.split("://", 1)[0].lower()
    try:
        if scheme == "vless":
            return parse_vless(uri, source)
        if scheme == "trojan":
            return parse_trojan(uri, source)
        if scheme == "vmess":
            return parse_vmess(uri, source)
        if scheme == "ss":
            return parse_ss(uri, source)
    except Exception:
        return None
    return None


def extract_uris(text: str) -> list[str]:
    if not text:
        return []
    chunks: list[str] = []
    text = html.unescape(text)
    text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    chunks.append(text)
    decoded = b64decode_text(text)
    if decoded and decoded != text:
        chunks.append(html.unescape(decoded))
    found: list[str] = []
    for chunk in chunks:
        for match in URI_RE.findall(chunk):
            uri = match.strip().rstrip(",;)]}'\"")
            found.append(uri)
    unique: list[str] = []
    seen = set()
    for uri in found:
        if uri not in seen:
            seen.add(uri)
            unique.append(uri)
    return unique


def fetch_url(url: str, timeout: int) -> tuple[str, str, str]:
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        text = response.text or ""
        if not text.strip():
            return url, "", f"dead: HTTP {response.status_code}, kosong"
        return url, text, f"alive: HTTP {response.status_code}"
    except Exception as exc:
        return url, "", f"dead: {exc}"


def fetch_url_cached(url: str, timeout: int) -> tuple[str, str, str]:
    """Fetch subscription URL. The Streamlit app version may cache this; CLI mode keeps it direct."""
    return fetch_url(url, timeout)


def one_tcp_delay(host: str, port: int, timeout: float) -> int | None:
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return int((time.perf_counter() - start) * 1000)
    except Exception:
        return None


def stability_check(host: str, port: int, timeout: float, attempts: int) -> tuple[bool, dict[str, Any]]:
    delays: list[int] = []
    last_error = ""
    for _ in range(max(1, attempts)):
        start = time.perf_counter()
        try:
            with socket.create_connection((host, port), timeout=timeout):
                delays.append(int((time.perf_counter() - start) * 1000))
        except Exception as exc:
            last_error = str(exc)
        # small gap so a node with one lucky accept is less likely to pass every attempt instantly
        time.sleep(0.03)

    if not delays:
        return False, {
            "best_delay_ms": None,
            "avg_delay_ms": None,
            "jitter_ms": None,
            "success_count": 0,
            "attempts": attempts,
            "score": 999999,
            "reason": last_error or "timeout",
        }

    best = min(delays)
    avg = int(statistics.mean(delays))
    jitter = int(max(delays) - min(delays)) if len(delays) > 1 else 0
    # Score favors low latency, stable repeated success, and low jitter.
    score = best + int(jitter * 0.7) + int((attempts - len(delays)) * 120)
    return True, {
        "best_delay_ms": best,
        "avg_delay_ms": avg,
        "jitter_ms": jitter,
        "success_count": len(delays),
        "attempts": attempts,
        "score": score,
        "reason": "alive",
    }


def looks_like_ip(host: str) -> bool:
    try:
        socket.inet_aton(host)
        return True
    except Exception:
        return False


def node_sni_host(node: ProxyNode) -> str:
    clash = node.clash
    # VLESS/VMess commonly use servername; Trojan commonly uses sni.
    candidates: list[str] = []
    for key in ("servername", "sni"):
        value = str(clash.get(key) or "").strip()
        if value:
            candidates.append(value)
    ws_host = clash.get("ws-opts", {}).get("headers", {}).get("Host", "") if isinstance(clash.get("ws-opts"), dict) else ""
    if isinstance(ws_host, str) and ws_host.strip():
        candidates.append(ws_host.strip())
    http_host = clash.get("http-opts", {}).get("headers", {}).get("Host", []) if isinstance(clash.get("http-opts"), dict) else []
    if isinstance(http_host, list) and http_host:
        candidates.append(str(http_host[0]).strip())
    candidates.append(node.original_server)
    for candidate in candidates:
        candidate = candidate.strip().strip("[]")
        if candidate and not looks_like_ip(candidate):
            return candidate
    return node.original_server



def explicit_tls_name_from_raw(node: ProxyNode) -> str:
    """Return the explicit SNI/servername from the original URI, if present.

    This is stricter than node_sni_host(): it does NOT fall back to Host or
    original_server. For bug-server output, nodes without explicit SNI/servername
    often pass a simple TLS check but later timeout in OpenClash.
    """
    raw = str(node.raw or "").strip()
    scheme = raw.split("://", 1)[0].lower() if "://" in raw else str(node.type or "").lower()

    try:
        if scheme in {"vless", "trojan"}:
            params = parse_qs(urlparse(raw).query)
            for key in ("sni", "servername", "serverName", "peer"):
                value = first_query(params, key, default="").strip()
                if complete_value(value) and not looks_like_ip(value):
                    return value
        elif scheme == "vmess":
            payload = raw.split("://", 1)[1].split("#", 1)[0]
            decoded = b64decode_text(payload)
            if not decoded:
                return ""
            data = json.loads(decoded)
            for key in ("sni", "servername", "serverName"):
                value = str(data.get(key) or "").strip()
                if complete_value(value) and not looks_like_ip(value):
                    return value
    except Exception:
        return ""
    return ""

def node_network(node: ProxyNode) -> str:
    """Return the normalized transport network used by the proxy node."""
    if str(node.type or "").lower() == "ss":
        return "ss"
    network = str(node.clash.get("network") or "tcp").strip().lower()
    if network in {"h2", "http"}:
        return "http"
    return network or "tcp"


def protocol_priority_rank(node: ProxyNode) -> int:
    """Prefer protocols that usually work better with bug server + SNI/Host."""
    return {"vless": 0, "trojan": 1, "vmess": 2, "ss": 3}.get(str(node.type or "").lower(), 9)


def network_priority_rank(node: ProxyNode, prefer_ws: bool = True) -> int:
    """When prefer_ws is enabled, WebSocket nodes are tested and selected first."""
    if not prefer_ws:
        return 0
    return {"ws": 0, "grpc": 1, "http": 2, "tcp": 3, "ss": 4}.get(node_network(node), 9)


def node_sort_key(node: ProxyNode, prefer_ws: bool = True) -> tuple[int, int, int, int, int]:
    return (
        network_priority_rank(node, prefer_ws),
        protocol_priority_rank(node),
        int(node.score or 999999),
        int(node.best_delay_ms or 999999),
        int(node.jitter_ms or 999999),
    )


def domain_root(host: str) -> str:
    """Return a simple root domain used only for soft diversity scoring."""
    text = str(host or "").strip().lower().strip(".")
    if not text or looks_like_ip(text):
        return text
    parts = [p for p in text.split(".") if p]
    if len(parts) <= 2:
        return text
    # Keep common 2-level public suffixes together enough for our duplicate filter.
    if parts[-2] in {"co", "com", "net", "org", "ac", "sch", "web", "or"} and len(parts[-1]) == 2 and len(parts) >= 3:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


_PROVIDER_CACHE: dict[str, tuple[str, str]] = {}
_RDAP_CACHE: dict[str, str] = {}

PROVIDER_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("VULTR", ("VULTR", "CHOOPA", "CONSTANT COMPANY")),
    ("MELBICOM", ("MELBICOM",)),
    ("DIGITALOCEAN", ("DIGITALOCEAN", "DIGITAL OCEAN", "DO-")),
    ("OVH", ("OVH",)),
    ("ORACLE", ("ORACLE", "ORACLE-BMC")),
    ("AKAMAI", ("AKAMAI", "LINODE")),
    ("HETZNER", ("HETZNER",)),
    ("AMAZON", ("AMAZON", "AWS", "AMAZON.COM")),
    ("GOOGLE", ("GOOGLE",)),
    ("MICROSOFT", ("MICROSOFT", "AZURE")),
    ("ALIBABA", ("ALIBABA",)),
    ("TENCENT", ("TENCENT",)),
    ("CLOUDFLARE", ("CLOUDFLARE",)),
    ("LEASEWEB", ("LEASEWEB",)),
    ("CONTABO", ("CONTABO",)),
    ("HOSTINGER", ("HOSTINGER",)),
    ("IONOS", ("IONOS", "1&1")),
    ("NETCUP", ("NETCUP",)),
    ("SCALWAY", ("SCALWAY", "ONLINE S.A.S", "ONLINE SAS")),
    ("GCORE", ("GCORE",)),
    ("M247", ("M247",)),
    ("CDN77", ("CDN77", "DATACAMP")),
    ("NFORCE", ("NFORCE",)),
    ("RETN", ("RETN",)),
    ("COGENT", ("COGENT",)),
]

COMMON_DOMAIN_LABELS = {
    "www", "cdn", "sni", "edge", "node", "server", "proxy", "vpn", "joinproxyvpn", "join", "cloud", "worker", "workers",
    "ray", "rayan", "config", "telegram", "free", "mianfei", "cf", "vless", "vmess", "trojan", "ws", "sg", "us", "de",
    "uk", "nl", "fr", "jp", "id", "hk", "fi", "ru", "ir", "tr", "au", "ca", "eu",
}


def _extract_text_values(value: Any, limit: int = 6000) -> str:
    """Collect useful short strings from RDAP JSON without depending on schema details."""
    out: list[str] = []

    def walk(obj: Any) -> None:
        if sum(len(x) for x in out) > limit:
            return
        if isinstance(obj, str):
            text = obj.strip()
            if text and len(text) <= 200:
                out.append(text)
        elif isinstance(obj, dict):
            for key in ("name", "handle", "title", "description", "type", "country"):
                if key in obj:
                    walk(obj[key])
            # vcardArray usually contains organization / full-name records.
            if "vcardArray" in obj:
                walk(obj["vcardArray"])
            if "entities" in obj:
                walk(obj["entities"])
            if "remarks" in obj:
                walk(obj["remarks"])
            if "links" in obj:
                walk(obj["links"])
            if "notices" in obj:
                walk(obj["notices"])
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(value)
    return " ".join(out)


def _map_provider(text: str) -> str:
    upper = str(text or "").upper()
    for label, patterns in PROVIDER_PATTERNS:
        if any(pattern in upper for pattern in patterns):
            return label
    return ""


def _resolve_original_ip(host: str) -> str:
    host = str(host or "").strip().strip("[]")
    if not host:
        return ""
    if looks_like_ip(host):
        return host
    try:
        return socket.gethostbyname(host)
    except Exception:
        return ""


def _rdap_provider(ip: str) -> str:
    ip = str(ip or "").strip()
    if not ip:
        return ""
    if ip in _RDAP_CACHE:
        return _RDAP_CACHE[ip]
    provider = ""
    try:
        response = requests.get(
            f"https://rdap.org/ip/{ip}",
            timeout=5,
            headers={"User-Agent": USER_AGENT},
        )
        if response.ok:
            data = response.json()
            provider = _map_provider(_extract_text_values(data))
            if not provider:
                # Fallback to a short RDAP name/handle when it is already readable.
                candidate = str(data.get("name") or data.get("handle") or "").strip()
                candidate = re.sub(r"[^A-Za-z0-9]+", "-", candidate).strip("-").upper()
                if candidate and not re.fullmatch(r"NET-?\d+|IPV4|RIPE|APNIC|ARIN|LACNIC|AFRINIC", candidate):
                    provider = candidate[:24]
    except Exception:
        provider = ""
    _RDAP_CACHE[ip] = provider
    return provider


def _domain_provider_fallback(host: str) -> str:
    """Use original domain text only when RDAP/ASN provider cannot be detected."""
    root = domain_root(host)
    if not root or looks_like_ip(root):
        return "UNKNOWN"
    labels = [x for x in root.split(".") if x]
    if not labels:
        return "UNKNOWN"
    for label in labels:
        clean = re.sub(r"[^A-Za-z0-9]+", "", label).upper()
        if clean and clean.lower() not in COMMON_DOMAIN_LABELS and len(clean) >= 3:
            return clean[:18]
    clean = re.sub(r"[^A-Za-z0-9]+", "", labels[0]).upper()
    return clean[:18] if clean else "UNKNOWN"


def provider_label_from_original_server(node: ProxyNode) -> str:
    """Return provider/ASN label detected from node.original_server.

    The forced output server is always Cloudflare bug IP, so provider naming must
    be based on original_server. If original_server is a domain, it is resolved to
    an IP first, then RDAP is queried. If RDAP fails, the root domain is used as a
    readable fallback.
    """
    host = str(node.original_server or "").strip().strip("[]")
    if not host:
        node.original_provider = "UNKNOWN"
        return "UNKNOWN"
    if host in _PROVIDER_CACHE:
        provider, ip = _PROVIDER_CACHE[host]
        node.original_provider = provider
        node.original_ip = ip
        return provider
    ip = _resolve_original_ip(host)
    provider = _rdap_provider(ip) if ip else ""
    if not provider:
        provider = _map_provider(host) or _domain_provider_fallback(host)
    provider = safe_proxy_name(provider.upper(), "UNKNOWN")
    _PROVIDER_CACHE[host] = (provider, ip)
    node.original_provider = provider
    node.original_ip = ip
    return provider


def update_raw_uri_name(raw: str, new_name: str) -> str:
    """Return a shareable URI with its display name changed to new_name."""
    raw = str(raw or "").strip()
    name = quote(str(new_name or "").strip(), safe="")
    if not raw or "://" not in raw:
        return raw
    scheme = raw.split("://", 1)[0].lower()
    try:
        if scheme == "vmess":
            payload = raw.split("://", 1)[1].split("#", 1)[0]
            decoded = b64decode_text(payload)
            if not decoded:
                return raw
            data = json.loads(decoded)
            data["ps"] = new_name
            encoded = base64.b64encode(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode("ascii")
            return "vmess://" + encoded
        # vless/trojan/ss: replace fragment safely.
        body = raw.split("#", 1)[0]
        return body + "#" + name
    except Exception:
        body = raw.split("#", 1)[0]
        return body + "#" + name


def update_raw_uri_name_and_server(raw: str, new_name: str, target_server: str = TARGET_SERVER) -> str:
    """Return a shareable URI using the bug server plus updated display name.

    YAML output already forces ``server`` to TARGET_SERVER. This function makes
    ``akun.txt`` consistent with that YAML: vless/trojan/ss links use
    ``@104.17.3.81:443`` while keeping SNI/Host/path query parameters intact.
    VMess links update the JSON ``add``/``server`` and ``port`` fields, while
    keeping transport fields such as ``host`` and ``sni`` unchanged.
    """
    raw = str(raw or "").strip()
    name = quote(str(new_name or "").strip(), safe="")
    if not raw or "://" not in raw:
        return raw
    scheme = raw.split("://", 1)[0].lower()
    try:
        if scheme == "vmess":
            payload = raw.split("://", 1)[1].split("#", 1)[0]
            decoded = b64decode_text(payload)
            if not decoded:
                return update_raw_uri_name(raw, new_name)
            data = json.loads(decoded)
            data["ps"] = new_name
            data["add"] = str(target_server)
            if "server" in data:
                data["server"] = str(target_server)
            data["port"] = str(ONLY_PORT)
            encoded = base64.b64encode(json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode("ascii")
            return "vmess://" + encoded

        body = raw.split("#", 1)[0]
        rest = body.split("://", 1)[1]
        main, sep, query = rest.partition("?")
        if "@" not in main:
            # Some ss:// links are fully base64 encoded. Keep the server untouched
            # rather than corrupting the account, but still refresh the name.
            return body + "#" + name
        userinfo, _serverpart = main.rsplit("@", 1)
        new_body = f"{scheme}://{userinfo}@{target_server}:{ONLY_PORT}"
        if sep:
            new_body += "?" + query
        return new_body + "#" + name
    except Exception:
        return update_raw_uri_name(raw, new_name)


def build_akun_txt(nodes: list[ProxyNode]) -> str:
    """Build akun.txt from final nodes using bug server 104.17.3.81."""
    lines: list[str] = []
    for node in nodes:
        if str(node.type or "").lower() not in {"vless", "vmess", "trojan", "ss"}:
            continue
        uri = update_raw_uri_name_and_server(node.raw, node.clash.get("name") or node.name, TARGET_SERVER)
        if uri:
            lines.append(uri)
    return "\n".join(lines) + ("\n" if lines else "")


def node_identity_key(node: ProxyNode) -> tuple[str, str, str, str, str]:
    """Hard duplicate key: same protocol/account/host/path should appear only once."""
    clash = node.clash or {}
    credential = str(clash.get("uuid") or clash.get("password") or "").strip().lower()
    return (
        str(node.type or "").lower(),
        credential,
        node_network(node),
        ws_host_header(node).lower() if node_network(node) == "ws" else node_sni_host(node).lower(),
        ws_path(node) if node_network(node) == "ws" else str(node.original_server).lower(),
    )


def select_diverse_nodes(nodes: list[ProxyNode], limit: int, prefer_ws: bool = True) -> list[ProxyNode]:
    """Pick stable nodes while avoiding many copies of the same host/root domain.

    This is intentionally soft: it first takes one per exact identity, then limits
    root-domain concentration. If that makes the result too small, it fills from
    the remaining alive nodes so the app can still pursue the requested 20 output.
    """
    sorted_nodes = sorted(nodes, key=lambda n: node_sort_key(n, prefer_ws))
    selected: list[ProxyNode] = []
    seen_identity: set[tuple[str, str, str, str, str]] = set()
    root_counts: dict[str, int] = {}

    for node in sorted_nodes:
        ident = node_identity_key(node)
        if ident in seen_identity:
            continue
        root = domain_root(ws_host_header(node) if node_network(node) == "ws" else node_sni_host(node))
        # Keep some diversity, but allow up to 4 nodes per root because public CF
        # pools can legitimately host several working accounts on one root domain.
        if root and root_counts.get(root, 0) >= 4:
            continue
        selected.append(node)
        seen_identity.add(ident)
        if root:
            root_counts[root] = root_counts.get(root, 0) + 1
        if len(selected) >= limit:
            return selected

    # Fill if strict diversity was too limiting.
    selected_ids = {id(n) for n in selected}
    for node in sorted_nodes:
        if id(node) in selected_ids:
            continue
        ident = node_identity_key(node)
        if ident in seen_identity:
            continue
        selected.append(node)
        seen_identity.add(ident)
        if len(selected) >= limit:
            break
    return selected


def ws_path(node: ProxyNode) -> str:
    ws_opts = node.clash.get("ws-opts") if isinstance(node.clash, dict) else None
    path = ws_opts.get("path") if isinstance(ws_opts, dict) else "/"
    path = str(path or "/").strip() or "/"
    if not path.startswith("/"):
        path = "/" + path
    # Request-line must be ASCII. Keep existing percent escapes and common URL chars.
    return quote(path, safe="/%?&=:+,;@._~!$'()*-[]")


def ws_host_header(node: ProxyNode) -> str:
    ws_opts = node.clash.get("ws-opts") if isinstance(node.clash, dict) else None
    if isinstance(ws_opts, dict):
        headers = ws_opts.get("headers")
        if isinstance(headers, dict):
            host = headers.get("Host") or headers.get("host")
            if isinstance(host, str) and host.strip():
                return host.strip()
    return node_sni_host(node)


def is_placeholder_uuid(value: str | None) -> bool:
    uuid = str(value or "").strip().lower()
    compact = uuid.replace("-", "")
    placeholder_set = {
        "00000000-0000-0000-0000-000000000000",
        "ffffffff-ffff-ffff-ffff-ffffffffffff",
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        "aaaaaabb-4ddd-4eee-9fff-ffffffffffff",
    }
    if uuid in placeholder_set:
        return True
    if re.fullmatch(r"[0-9a-f]{32}", compact):
        # Reject obvious public-list dummy UUIDs made mostly from a/f/0/1.
        dominant = max(compact.count(ch) for ch in set(compact)) if compact else 0
        if dominant >= 20 and len(set(compact)) <= 5:
            return True
    return False


def harden_ws_node(node: ProxyNode) -> None:
    """Make WS output closer to what OpenClash/Mihomo expects."""
    if node_network(node) != "ws":
        return
    node.clash["alpn"] = ["http/1.1"]
    ws_opts = node.clash.setdefault("ws-opts", {})
    if not isinstance(ws_opts, dict):
        ws_opts = {}
        node.clash["ws-opts"] = ws_opts
    ws_opts["path"] = ws_path(node)
    headers = ws_opts.setdefault("headers", {})
    if not isinstance(headers, dict):
        headers = {}
        ws_opts["headers"] = headers
    headers["Host"] = str(headers.get("Host") or headers.get("host") or node_sni_host(node)).strip()


PLACEHOLDER_VALUES = {"", "-", "none", "null", "undefined", "nil", "nan"}


def complete_value(value: Any) -> bool:
    """True if a config value is meaningful enough to be written to YAML."""
    if value is None:
        return False
    if isinstance(value, str):
        text = html.unescape(unquote(value)).strip()
        return text.lower() not in PLACEHOLDER_VALUES
    if isinstance(value, (list, tuple, set)):
        return any(complete_value(item) for item in value)
    if isinstance(value, dict):
        return bool(value)
    return True


def get_nested(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def has_host_value(value: Any) -> bool:
    if isinstance(value, list):
        return any(complete_value(item) for item in value)
    return complete_value(value)


def validate_network_options(clash: dict[str, Any], missing: list[str]) -> None:
    network = str(clash.get("network") or "tcp").lower()
    if network == "ws":
        ws_opts = clash.get("ws-opts")
        if not isinstance(ws_opts, dict):
            missing.append("ws-opts")
            return
        if not complete_value(ws_opts.get("path")):
            missing.append("ws-opts.path")
        if not has_host_value(get_nested(ws_opts, "headers", "Host")):
            missing.append("ws-opts.headers.Host")
    elif network == "grpc":
        grpc_opts = clash.get("grpc-opts")
        if not isinstance(grpc_opts, dict):
            missing.append("grpc-opts")
            return
        if not complete_value(grpc_opts.get("grpc-service-name")):
            missing.append("grpc-opts.grpc-service-name")
    elif network == "http":
        http_opts = clash.get("http-opts")
        if not isinstance(http_opts, dict):
            missing.append("http-opts")
            return
        if not complete_value(http_opts.get("path")):
            missing.append("http-opts.path")
        if not has_host_value(get_nested(http_opts, "headers", "Host")):
            missing.append("http-opts.headers.Host")


def validate_complete_node(node: ProxyNode) -> tuple[bool, str]:
    """Reject incomplete public accounts before they are tested or written.

    Because the output server is forced to the Cloudflare bug IP, a usable account
    must have enough protocol information for OpenClash/Mihomo to build the real
    connection: credentials, TLS SNI/Host where applicable, network-specific
    options, and port 443.
    """
    clash = node.clash
    missing: list[str] = []

    if node.port != ONLY_PORT:
        missing.append("port 443")
    if not complete_value(node.original_server):
        missing.append("original_server")
    if not complete_value(clash.get("type")):
        missing.append("type")
    if not complete_value(clash.get("server")):
        missing.append("server")
    if not complete_value(clash.get("port")):
        missing.append("port")

    proto = str(clash.get("type") or node.type or "").lower()
    network = str(clash.get("network") or "tcp").lower()

    if proto in {"vless", "vmess", "trojan"}:
        explicit_sni = explicit_tls_name_from_raw(node)
        if explicit_sni:
            if proto in {"vless", "vmess"}:
                clash["servername"] = explicit_sni
            elif proto == "trojan":
                clash["sni"] = explicit_sni
            node.bug_sni = explicit_sni
        else:
            missing.append("explicit sni/servername")
        sni = node_sni_host(node)
        node.bug_sni = explicit_sni or sni
        if not complete_value(sni) or looks_like_ip(str(sni)):
            missing.append("SNI/Host domain")
        if network not in {"tcp", "ws", "grpc", "http"}:
            missing.append("network")
        validate_network_options(clash, missing)

    if proto == "vless":
        if not complete_value(clash.get("uuid")):
            missing.append("uuid")
        elif is_placeholder_uuid(str(clash.get("uuid"))):
            missing.append("uuid placeholder")
        if not complete_value(clash.get("servername")):
            missing.append("servername")
        if str(clash.get("tls", "")).lower() in {"false", "0", "none"}:
            missing.append("tls")
        if isinstance(clash.get("reality-opts"), dict):
            reality_opts = clash.get("reality-opts") or {}
            if not complete_value(reality_opts.get("public-key")):
                missing.append("reality-opts.public-key")
    elif proto == "vmess":
        if not complete_value(clash.get("uuid")):
            missing.append("uuid")
        elif is_placeholder_uuid(str(clash.get("uuid"))):
            missing.append("uuid placeholder")
        if not complete_value(clash.get("cipher")):
            missing.append("cipher")
        if not complete_value(clash.get("servername")):
            missing.append("servername")
        if str(clash.get("tls", "")).lower() in {"false", "0", "none"}:
            missing.append("tls")
        try:
            int(clash.get("alterId"))
        except Exception:
            missing.append("alterId")
    elif proto == "trojan":
        if not complete_value(clash.get("password")):
            missing.append("password")
        if not complete_value(clash.get("sni")):
            missing.append("sni")
    elif proto == "ss":
        if not complete_value(clash.get("cipher")):
            missing.append("cipher")
        if not complete_value(clash.get("password")):
            missing.append("password")
        # Plain Shadowsocks cannot carry SNI/Host when the server is replaced by
        # the bug IP. Keeping it would often create YAML that imports but cannot
        # connect through 104.17.3.81.
        if str(node.original_server).strip() != TARGET_SERVER:
            missing.append("ss tidak kompatibel dengan bug server tanpa SNI/Host")
    else:
        missing.append("protocol unsupported")

    if missing:
        unique_missing = []
        seen = set()
        for item in missing:
            if item not in seen:
                seen.add(item)
                unique_missing.append(item)
        return False, "incomplete: " + ", ".join(unique_missing[:10])
    return True, "complete"


def tls_bug_delay(node: ProxyNode, timeout: float, attempts: int) -> tuple[bool, dict[str, Any]]:
    """Measure whether TARGET_SERVER:443 can complete TLS with the node SNI/Host.

    This is the important check when the YAML output forces server to 104.17.3.81.
    It does not replace OpenClash url-test, but it prevents many accounts whose SNI/Host
    cannot work through the selected bug IP from entering the generated YAML.
    """
    sni = node_sni_host(node)
    node.bug_sni = sni
    delays: list[int] = []
    last_error = ""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    for _ in range(max(1, attempts)):
        start = time.perf_counter()
        try:
            raw = socket.create_connection((TARGET_SERVER, ONLY_PORT), timeout=timeout)
            raw.settimeout(timeout)
            with raw:
                with context.wrap_socket(raw, server_hostname=sni):
                    delays.append(int((time.perf_counter() - start) * 1000))
        except Exception as exc:
            last_error = str(exc)
        time.sleep(0.03)

    if not delays:
        return False, {
            "best_delay_ms": None,
            "avg_delay_ms": None,
            "jitter_ms": None,
            "success_count": 0,
            "attempts": attempts,
            "score": 999999,
            "reason": last_error or "bug tls timeout",
        }
    best = min(delays)
    avg = int(statistics.mean(delays))
    jitter = int(max(delays) - min(delays)) if len(delays) > 1 else 0
    score = best + int(jitter * 0.8) + int((attempts - len(delays)) * 160)
    return True, {
        "best_delay_ms": best,
        "avg_delay_ms": avg,
        "jitter_ms": jitter,
        "success_count": len(delays),
        "attempts": attempts,
        "score": score,
        "reason": "bug-tls-alive",
    }


def ws_upgrade_delay(node: ProxyNode, timeout: float, attempts: int) -> tuple[bool, dict[str, Any]]:
    """Check TLS + WebSocket Upgrade through the selected bug IP.

    A node can complete TLS with Cloudflare but still fail OpenClash health check
    if the WS path/Host is wrong. This check only accepts HTTP 101 Switching Protocols.
    """
    sni = node_sni_host(node)
    host = ws_host_header(node)
    path = ws_path(node)
    node.bug_sni = sni
    delays: list[int] = []
    status_codes: list[int] = []
    last_error = ""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    for _ in range(max(1, attempts)):
        start = time.perf_counter()
        try:
            raw = socket.create_connection((TARGET_SERVER, ONLY_PORT), timeout=timeout)
            raw.settimeout(timeout)
            with raw:
                with context.wrap_socket(raw, server_hostname=sni) as sock:
                    key = base64.b64encode(os.urandom(16)).decode("ascii")
                    request = (
                        f"GET {path} HTTP/1.1\r\n"
                        f"Host: {host}\r\n"
                        f"User-Agent: {USER_AGENT}\r\n"
                        "Connection: Upgrade\r\n"
                        "Upgrade: websocket\r\n"
                        "Sec-WebSocket-Version: 13\r\n"
                        f"Sec-WebSocket-Key: {key}\r\n"
                        "Pragma: no-cache\r\n"
                        "Cache-Control: no-cache\r\n"
                        "\r\n"
                    )
                    sock.sendall(request.encode("ascii", errors="ignore"))
                    response = sock.recv(512)
                    first_line = response.split(b"\r\n", 1)[0].decode("iso-8859-1", errors="ignore")
                    match = re.search(r"\s(\d{3})\s", first_line)
                    status = int(match.group(1)) if match else 0
                    status_codes.append(status)
                    if status == 101:
                        delays.append(int((time.perf_counter() - start) * 1000))
                    else:
                        last_error = first_line or f"HTTP {status}"
        except Exception as exc:
            last_error = str(exc)
        time.sleep(0.03)

    node.ws_success_count = len(delays)
    node.ws_upgrade_ms = min(delays) if delays else None
    node.ws_status = "101" if delays else (str(status_codes[-1]) if status_codes else str(last_error)[:80])

    if not delays:
        return False, {
            "best_delay_ms": None,
            "avg_delay_ms": None,
            "jitter_ms": None,
            "success_count": 0,
            "attempts": attempts,
            "score": 999999,
            "reason": f"ws upgrade gagal: {node.ws_status}",
        }

    best = min(delays)
    avg = int(statistics.mean(delays))
    jitter = int(max(delays) - min(delays)) if len(delays) > 1 else 0
    score = best + int(jitter * 0.9) + int((attempts - len(delays)) * 220)
    return True, {
        "best_delay_ms": best,
        "avg_delay_ms": avg,
        "jitter_ms": jitter,
        "success_count": len(delays),
        "attempts": attempts,
        "score": score,
        "reason": "bug-ws-101-alive",
    }


def check_node_bug_compat(node: ProxyNode, timeout: float, attempts: int, require_original: bool, require_ws_upgrade: bool = True) -> ProxyNode:
    harden_ws_node(node)
    if require_ws_upgrade and node_network(node) == "ws":
        bug_ok, bug_info = ws_upgrade_delay(node, timeout, attempts)
    else:
        bug_ok, bug_info = tls_bug_delay(node, timeout, attempts)

    # Optimasi penting: kalau original server tidak diwajibkan, jangan dites.
    # Seleksi YAML memang memakai delay ke bug server, jadi cek original hanya menambah waktu proses.
    if require_original:
        orig_ok, orig_info = stability_check(node.original_server, node.port, timeout, attempts)
    else:
        orig_ok = False
        orig_info = {
            "best_delay_ms": None,
            "success_count": 0,
            "reason": "original check skipped",
        }

    node.bug_best_delay_ms = bug_info["best_delay_ms"]
    node.bug_avg_delay_ms = bug_info["avg_delay_ms"]
    node.bug_jitter_ms = bug_info["jitter_ms"]
    node.bug_success_count = bug_info["success_count"]
    node.original_best_delay_ms = orig_info["best_delay_ms"]
    node.original_success_count = orig_info["success_count"]

    # Selection uses bug delay because output server is the bug IP.
    node.best_delay_ms = node.bug_best_delay_ms
    node.avg_delay_ms = node.bug_avg_delay_ms
    node.jitter_ms = node.bug_jitter_ms
    node.success_count = node.bug_success_count
    node.attempts = attempts
    node.score = bug_info["score"] + int((attempts - node.bug_success_count) * 200)

    if not bug_ok:
        node.status = "dead"
        node.reason = "bug server gagal: " + str(bug_info["reason"])[:120]
    elif require_original and not orig_ok:
        node.status = "dead"
        node.reason = "original server gagal: " + str(orig_info["reason"])[:120]
    else:
        node.status = "alive"
        node.reason = "bug server alive" + (" + original alive" if orig_ok else " + original skipped")
    return node


def build_openclash_yaml(nodes: list[ProxyNode], interval: int, tolerance: int, test_url: str, health_timeout: int = DEFAULT_HEALTH_TIMEOUT_MS, rule_mode: str = "Lengkap") -> str:
    names = [node.clash["name"] for node in nodes]
    direct_or_names = names or ["DIRECT"]
    warmup_names = _select_warmup_names(names)
    cf_warmup_names = _select_cf_warmup_names(names)
    fast_names = _select_fast_pool_names(names)
    streaming_names = _select_streaming_names(names, warmup_names, cf_warmup_names)
    fallback_names = _fallback_order_names(names, warmup_names, cf_warmup_names)
    warmup_or_direct = warmup_names or direct_or_names
    cf_or_warmup = cf_warmup_names or warmup_or_direct
    fast_or_direct = fast_names or direct_or_names
    streaming_or_direct = streaming_names or warmup_or_direct
    fallback_or_direct = fallback_names or direct_or_names
    active_interval = _active_health_interval(interval)
    warmup_interval = _env_int_range("WARMUP_INTERVAL", 15, 10, 120)
    cf_interval = _env_int_range("CF_WARMUP_INTERVAL", 20, 10, 120)
    fallback_interval = max(active_interval, _env_int_range("FALLBACK_INTERVAL", 60, 30, 600))
    balance_interval = max(fallback_interval, _env_int_range("BALANCE_INTERVAL", 90, 60, 600))
    base_timeout = int(health_timeout)
    warmup_timeout = _env_int_range("WARMUP_TIMEOUT_MS", min(3000, base_timeout), 1000, 10000)
    cf_timeout = _env_int_range("CF_WARMUP_TIMEOUT_MS", min(3000, base_timeout), 1000, 10000)
    fast_timeout = _env_int_range("FAST_HEALTH_TIMEOUT_MS", min(3000, base_timeout), 1000, 10000)
    cf_test_url = os.getenv("CF_TEST_URL", "https://cp.cloudflare.com").strip() or "https://cp.cloudflare.com"
    streaming_test_url = os.getenv("STREAMING_TEST_URL", cf_test_url).strip() or cf_test_url
    ping_check_url = os.getenv("PING_CHECK_URL", test_url).strip() or test_url
    ping_check_interval = _env_int_range("PING_CHECK_INTERVAL", 60, 45, 600)
    ping_check_timeout = _env_int_range("PING_CHECK_TIMEOUT_MS", max(5000, base_timeout), 2000, 15000)

    def selector(defaults: list[str] | None = None) -> list[str]:
        defaults = defaults or ["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"]
        return defaults + names

    domain_provider = {
        "type": "http",
        "interval": 86400,
        "behavior": "domain",
        "format": "mrs",
    }
    ip_provider = {
        "type": "http",
        "interval": 86400,
        "behavior": "ipcidr",
        "format": "mrs",
    }
    classical_provider = {
        "type": "http",
        "interval": 86400,
        "behavior": "classical",
        "format": "yaml",
    }
    text_domain_provider = {
        "type": "http",
        "interval": 43200,
        "behavior": "domain",
        "format": "text",
    }

    rule_providers: dict[str, Any] = {
        # Threat feed mini memblokir malware, phishing, scam, spam, dan C2
        # dengan footprint yang masih masuk akal untuk router.
        "threat-tif-mini": {
            **text_domain_provider,
            "path": "./rule_providers/threat-tif-mini.txt",
            "url": "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/wildcard/tif.mini-onlydomains.txt",
        },

        # Block iklan, tracking, privacy-leak, dan hijacking.
        "ads_domain": {
            **domain_provider,
            "path": "./rule_providers/ads_domain.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ads-all.mrs",
        },
        "ads_classical": {
            **classical_provider,
            "path": "./rule_providers/Advertising.yaml",
            "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Advertising/Advertising.yaml",
        },
        "privacy_classical": {
            **classical_provider,
            "path": "./rule_providers/Privacy.yaml",
            "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Privacy/Privacy.yaml",
        },
        "hijacking_classical": {
            **classical_provider,
            "path": "./rule_providers/Hijacking.yaml",
            "url": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Hijacking/Hijacking.yaml",
        },

        # YouTube dipisah agar bisa diberi jalur berbeda dari Google umum.
        "youtube_domain": {
            **domain_provider,
            "path": "./rule_providers/youtube.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.mrs",
        },
        "youtube_ip": {
            **ip_provider,
            "path": "./rule_providers/youtube_ip.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/google.mrs",
        },

        # Sosial media.
        "telegram_domain": {
            **domain_provider,
            "path": "./rule_providers/telegram.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/telegram.mrs",
        },
        "twitter_domain": {
            **domain_provider,
            "path": "./rule_providers/twitter.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitter.mrs",
        },
        "tiktok_domain": {
            **domain_provider,
            "path": "./rule_providers/tiktok.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/tiktok.mrs",
        },
        "facebook_domain": {
            **domain_provider,
            "path": "./rule_providers/facebook.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/facebook.mrs",
        },
        "telegram_ip": {
            **ip_provider,
            "path": "./rule_providers/telegram_ip.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/telegram.mrs",
        },
        "twitter_ip": {
            **ip_provider,
            "path": "./rule_providers/twitter_ip.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/twitter.mrs",
        },

        # Edukasi / research / developer learning.
        "scholar_domain": {
            **domain_provider,
            "path": "./rule_providers/scholar.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-scholar-!cn.mrs",
        },
        "github_domain": {
            **domain_provider,
            "path": "./rule_providers/github.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/github.mrs",
        },

        # Streaming selain YouTube.
        "netflix_domain": {
            **domain_provider,
            "path": "./rule_providers/netflix.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/netflix.mrs",
        },
        "spotify_domain": {
            **domain_provider,
            "path": "./rule_providers/spotify.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/spotify.mrs",
        },
        "biliintl_domain": {
            **domain_provider,
            "path": "./rule_providers/biliintl.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/biliintl.mrs",
        },
        "netflix_ip": {
            **ip_provider,
            "path": "./rule_providers/netflix_ip.mrs",
            "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/netflix.mrs",
        },
    }

    proxy_groups: list[dict[str, Any]] = [
        {
            "name": "GLOBAL",
            "type": "select",
            # WARM-UP dibuat paling depan supaya fresh import langsung memakai pool kecil yang sudah dipanaskan.
            "proxies": ["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK", "SOCIAL-MEDIA", "YOUTUBE", "EDUKASI", "STREAMING-FAST", "STREAMING", "CLEAN", "LOAD-BALANCE"] + names,
        },
        {
            "name": "PROXY",
            "type": "select",
            "proxies": ["GLOBAL", "WARM-UP", "WARM-UP-CF", "AUTO-FAST", "SOCIAL-MEDIA", "YOUTUBE", "EDUKASI", "STREAMING-FAST", "STREAMING", "CLEAN", "FALLBACK", "LOAD-BALANCE"] + names,
        },
        {
            "name": "SOCIAL-MEDIA",
            "type": "select",
            "proxies": selector(["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"]),
        },
        {
            "name": "YOUTUBE",
            "type": "select",
            "proxies": selector(["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"]),
        },
        {
            "name": "EDUKASI",
            "type": "select",
            "proxies": selector(["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"]),
        },
        {
            "name": "STREAMING",
            "type": "select",
            # STREAMING-FAST dibuat url-test khusus agar panel OpenClash punya delay hijau
            # sendiri, bukan hanya delay dari nested select group.
            "proxies": selector(["WARM-UP-CF", "STREAMING-FAST", "WARM-UP", "AUTO-FAST", "FALLBACK"]),
        },
        {
            "name": "PING-CHECK",
            "type": "url-test",
            # Probe semua akun agar panel OpenClash/Mihomo segera punya delay/ping.
            # Group ini bukan jalur utama; dipakai sebagai health probe pasca import/reload.
            "proxies": direct_or_names,
            "url": ping_check_url,
            "interval": ping_check_interval,
            "tolerance": max(tolerance, 100),
            "lazy": False,
            "timeout": ping_check_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "WARM-UP",
            "type": "url-test",
            "proxies": warmup_or_direct,
            "url": test_url,
            "interval": warmup_interval,
            "tolerance": min(tolerance, 30),
            "lazy": False,
            "timeout": warmup_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "WARM-UP-CF",
            "type": "url-test",
            "proxies": cf_or_warmup,
            "url": cf_test_url,
            "interval": cf_interval,
            "tolerance": min(tolerance, 30),
            "lazy": False,
            "timeout": cf_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "STREAMING-FAST",
            "type": "url-test",
            "proxies": streaming_or_direct,
            "url": streaming_test_url,
            "interval": active_interval,
            "tolerance": max(tolerance, 50),
            "lazy": False,
            "timeout": fast_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "CLEAN",
            "type": "select",
            "proxies": ["WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"],
        },
        {
            "name": "AUTO-FAST",
            "type": "url-test",
            "proxies": fast_or_direct,
            "url": test_url,
            "interval": active_interval,
            "tolerance": tolerance,
            "lazy": False,
            "timeout": fast_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "FALLBACK",
            "type": "fallback",
            "proxies": fallback_or_direct,
            "url": test_url,
            "interval": fallback_interval,
            "lazy": False,
            "timeout": health_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 3,
        },
        {
            "name": "LOAD-BALANCE",
            "type": "load-balance",
            "strategy": "sticky-sessions",
            "proxies": warmup_or_direct,
            "url": test_url,
            "interval": balance_interval,
            "lazy": False,
            "timeout": health_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 3,
        },
    ]

    rules = [
        # LAN/private harus direct sebelum ruleset lain.
        "DOMAIN-SUFFIX,local,DIRECT",
        "DOMAIN-SUFFIX,lan,DIRECT",
        "DOMAIN-SUFFIX,localhost,DIRECT",
        "IP-CIDR,127.0.0.0/8,DIRECT",
        "IP-CIDR,10.0.0.0/8,DIRECT",
        "IP-CIDR,172.16.0.0/12,DIRECT",
        "IP-CIDR,192.168.0.0/16,DIRECT",
        "IP-CIDR,169.254.0.0/16,DIRECT",
        "GEOIP,LAN,DIRECT,no-resolve",

        # Cegah malware/phishing lebih dulu, lalu iklan/tracker.
        "RULE-SET,threat-tif-mini,REJECT",
        "RULE-SET,ads_domain,REJECT",
        "RULE-SET,ads_classical,REJECT",
        "RULE-SET,privacy_classical,REJECT",
        "RULE-SET,hijacking_classical,REJECT",
        "DOMAIN-SUFFIX,doubleclick.net,REJECT",
        "DOMAIN-SUFFIX,googlesyndication.com,REJECT",
        "DOMAIN-SUFFIX,googleadservices.com,REJECT",
        "DOMAIN-SUFFIX,pagead2.googlesyndication.com,REJECT",

        # YouTube khusus, sebelum Google umum/edukasi.
        "RULE-SET,youtube_domain,YOUTUBE",
        "DOMAIN-SUFFIX,youtube.com,YOUTUBE",
        "DOMAIN-SUFFIX,youtu.be,YOUTUBE",
        "DOMAIN-SUFFIX,ytimg.com,YOUTUBE",
        "DOMAIN-SUFFIX,googlevideo.com,YOUTUBE",
        "DOMAIN-SUFFIX,youtubei.googleapis.com,YOUTUBE",

        # Sosial media.
        "RULE-SET,telegram_domain,SOCIAL-MEDIA",
        "RULE-SET,twitter_domain,SOCIAL-MEDIA",
        "RULE-SET,tiktok_domain,SOCIAL-MEDIA",
        "RULE-SET,facebook_domain,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,facebook.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,fbcdn.net,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,instagram.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,cdninstagram.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,threads.net,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,tiktok.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,tiktokcdn.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,twitter.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,x.com,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,t.me,SOCIAL-MEDIA",
        "DOMAIN-SUFFIX,telegram.org,SOCIAL-MEDIA",
        "GEOIP,telegram,SOCIAL-MEDIA,no-resolve",
        "GEOIP,twitter,SOCIAL-MEDIA,no-resolve",

        # Edukasi, riset, kuliah, dan developer learning.
        "RULE-SET,scholar_domain,EDUKASI",
        "RULE-SET,github_domain,EDUKASI",
        "DOMAIN-SUFFIX,edu,EDUKASI",
        "DOMAIN-SUFFIX,ac.id,EDUKASI",
        "DOMAIN-SUFFIX,scholar.google.com,EDUKASI",
        "DOMAIN-SUFFIX,coursera.org,EDUKASI",
        "DOMAIN-SUFFIX,edx.org,EDUKASI",
        "DOMAIN-SUFFIX,khanacademy.org,EDUKASI",
        "DOMAIN-SUFFIX,udemy.com,EDUKASI",
        "DOMAIN-SUFFIX,academia.edu,EDUKASI",
        "DOMAIN-SUFFIX,arxiv.org,EDUKASI",
        "DOMAIN-SUFFIX,github.com,EDUKASI",
        "DOMAIN-SUFFIX,githubusercontent.com,EDUKASI",

        # Streaming umum selain YouTube.
        "RULE-SET,netflix_domain,STREAMING",
        "RULE-SET,spotify_domain,STREAMING",
        "RULE-SET,biliintl_domain,STREAMING",
        "DOMAIN-SUFFIX,netflix.com,STREAMING",
        "DOMAIN-SUFFIX,nflxvideo.net,STREAMING",
        "DOMAIN-SUFFIX,disneyplus.com,STREAMING",
        "DOMAIN-SUFFIX,hotstar.com,STREAMING",
        "DOMAIN-SUFFIX,primevideo.com,STREAMING",
        "DOMAIN-SUFFIX,amazonvideo.com,STREAMING",
        "DOMAIN-SUFFIX,hulu.com,STREAMING",
        "DOMAIN-SUFFIX,hbomax.com,STREAMING",
        "DOMAIN-SUFFIX,max.com,STREAMING",
        "DOMAIN-SUFFIX,spotify.com,STREAMING",
        "DOMAIN-SUFFIX,twitch.tv,STREAMING",
        "DOMAIN-SUFFIX,viu.com,STREAMING",
        "DOMAIN-SUFFIX,wetv.vip,STREAMING",
        "GEOIP,netflix,STREAMING,no-resolve",

        # Sisanya ikut GLOBAL yang defaultnya langsung AUTO-FAST.
        "MATCH,GLOBAL",
    ]
    rules = _inject_manual_unblock_rules(rules, target="MANUAL")

    if rule_mode == "Lite":
        # Rule Lite lebih ringan untuk router/OpenClash kecil: provider lebih sedikit, import lebih cepat,
        # tetapi kategori utama tetap ada.
        rule_providers = {
            "ads_domain": {
                **domain_provider,
                "path": "./rule_providers/ads_domain.mrs",
                "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-ads-all.mrs",
            },
            "youtube_domain": {
                **domain_provider,
                "path": "./rule_providers/youtube.mrs",
                "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.mrs",
            },
        }
        rules = [
            "DOMAIN-SUFFIX,local,DIRECT",
            "DOMAIN-SUFFIX,lan,DIRECT",
            "DOMAIN-SUFFIX,localhost,DIRECT",
            "IP-CIDR,127.0.0.0/8,DIRECT",
            "IP-CIDR,10.0.0.0/8,DIRECT",
            "IP-CIDR,172.16.0.0/12,DIRECT",
            "IP-CIDR,192.168.0.0/16,DIRECT",
            "IP-CIDR,169.254.0.0/16,DIRECT",
            "GEOIP,LAN,DIRECT,no-resolve",
            "RULE-SET,ads_domain,REJECT",
            "DOMAIN-SUFFIX,doubleclick.net,REJECT",
            "DOMAIN-SUFFIX,googlesyndication.com,REJECT",
            "DOMAIN-SUFFIX,googleadservices.com,REJECT",
                        "RULE-SET,youtube_domain,YOUTUBE",
            "DOMAIN-SUFFIX,youtube.com,YOUTUBE",
            "DOMAIN-SUFFIX,youtu.be,YOUTUBE",
            "DOMAIN-SUFFIX,ytimg.com,YOUTUBE",
            "DOMAIN-SUFFIX,googlevideo.com,YOUTUBE",
            "DOMAIN-SUFFIX,facebook.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,fbcdn.net,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,instagram.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,cdninstagram.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,tiktok.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,tiktokcdn.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,twitter.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,x.com,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,t.me,SOCIAL-MEDIA",
            "DOMAIN-SUFFIX,telegram.org,SOCIAL-MEDIA",
            "MATCH,GLOBAL",
        ]
        rules = _inject_manual_unblock_rules(rules, target="MANUAL")

    config: dict[str, Any] = {
        "mixed-port": 7890,
        "redir-port": 7892,
        "tproxy-port": 7895,
        "allow-lan": True,
        "bind-address": "*",
        "lan-allowed-ips": ["127.0.0.0/8", "10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"],
        "mode": "rule",
        "log-level": "warning",
        "ipv6": False,
        "unified-delay": True,
        "tcp-concurrent": True,
        "find-process-mode": "off",
        **_mihomo_keep_alive_config(),
        "external-controller": os.getenv("MIHOMO_EXTERNAL_CONTROLLER", "127.0.0.1:9090"),
        "secret": os.getenv("MIHOMO_SECRET", "reyre"),
        "profile": {
            "store-selected": True,
            "store-fake-ip": True,
        },
        "sniffer": {
            "enable": True,
            "sniff": {
                "TLS": {"ports": [443, 8443]},
                "HTTP": {"ports": [80, "8080-8880"], "override-destination": True},
                "QUIC": {"ports": [443, 8443]},
            },
            "force-domain": ["+.v2ex.com"],
            "skip-domain": ["+.lan", "+.local"],
        },
        "dns": {
            "enable": True,
            "ipv6": False,
            "listen": "0.0.0.0:7874",
            "enhanced-mode": "fake-ip",
            "fake-ip-range": "198.18.0.1/16",
            "fake-ip-filter": _dns_fake_ip_filter(),
            "default-nameserver": ["1.1.1.1", "8.8.8.8"],
            "nameserver": ["https://1.1.1.1/dns-query", "https://dns.google/dns-query"],
            "fallback": ["tls://1.1.1.1", "tls://8.8.8.8"],
            "fallback-filter": {"geoip": True, "geoip-code": "ID", "ipcidr": ["240.0.0.0/4"]},
        },
        "proxies": [node.clash for node in nodes],
        "proxy-groups": proxy_groups,
        "rule-providers": rule_providers,
        "rules": rules,
    }

    config = _enforce_no_selector_no_direct_config(config)
    return dump_yaml_no_alias(config)


def build_openclash_android_yaml(
    nodes: list[ProxyNode],
    interval: int,
    tolerance: int,
    test_url: str,
    health_timeout: int = DEFAULT_HEALTH_TIMEOUT_MS,
) -> str:
    """Build a lightweight Clash/OpenClash-for-Android config without rule providers.

    This output is intended for Android clients that only need the active accounts.
    It deliberately omits rule-providers, custom category rules, redir-port, and
    tproxy-port. Traffic is handled in global mode and the user can select
    AUTO-FAST, FALLBACK, or a specific node in the client UI.
    """
    names = [node.clash["name"] for node in nodes]
    direct_or_names = names or ["DIRECT"]
    warmup_names = _select_warmup_names(names)
    cf_warmup_names = _select_cf_warmup_names(names)
    fast_names = _select_fast_pool_names(names)
    streaming_names = _select_streaming_names(names, warmup_names, cf_warmup_names)
    fallback_names = _fallback_order_names(names, warmup_names, cf_warmup_names)
    warmup_or_direct = warmup_names or direct_or_names
    cf_or_warmup = cf_warmup_names or warmup_or_direct
    fast_or_direct = fast_names or direct_or_names
    streaming_or_direct = streaming_names or warmup_or_direct
    fallback_or_direct = fallback_names or direct_or_names
    active_interval = _active_health_interval(interval)
    warmup_interval = _env_int_range("WARMUP_INTERVAL", 15, 10, 120)
    cf_interval = _env_int_range("CF_WARMUP_INTERVAL", 20, 10, 120)
    fallback_interval = max(active_interval, _env_int_range("FALLBACK_INTERVAL", 60, 30, 600))
    base_timeout = int(health_timeout)
    warmup_timeout = _env_int_range("WARMUP_TIMEOUT_MS", min(3000, base_timeout), 1000, 10000)
    cf_timeout = _env_int_range("CF_WARMUP_TIMEOUT_MS", min(3000, base_timeout), 1000, 10000)
    fast_timeout = _env_int_range("FAST_HEALTH_TIMEOUT_MS", min(3000, base_timeout), 1000, 10000)
    cf_test_url = os.getenv("CF_TEST_URL", "https://cp.cloudflare.com").strip() or "https://cp.cloudflare.com"
    streaming_test_url = os.getenv("STREAMING_TEST_URL", cf_test_url).strip() or cf_test_url
    ping_check_url = os.getenv("PING_CHECK_URL", test_url).strip() or test_url
    ping_check_interval = _env_int_range("PING_CHECK_INTERVAL", 60, 45, 600)
    ping_check_timeout = _env_int_range("PING_CHECK_TIMEOUT_MS", max(5000, base_timeout), 2000, 15000)

    proxy_groups: list[dict[str, Any]] = [
        {
            "name": "GLOBAL",
            "type": "select",
            "proxies": ["WARM-UP-CF", "STREAMING-FAST", "WARM-UP", "AUTO-FAST", "FALLBACK"] + names,
        },
        {
            "name": "PING-CHECK",
            "type": "url-test",
            # Probe semua akun agar panel OpenClash/Mihomo segera punya delay/ping.
            # Group ini bukan jalur utama; dipakai sebagai health probe pasca import/reload.
            "proxies": direct_or_names,
            "url": ping_check_url,
            "interval": ping_check_interval,
            "tolerance": max(tolerance, 100),
            "lazy": False,
            "timeout": ping_check_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "WARM-UP",
            "type": "url-test",
            "proxies": warmup_or_direct,
            "url": test_url,
            "interval": warmup_interval,
            "tolerance": min(tolerance, 30),
            "lazy": False,
            "timeout": warmup_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "WARM-UP-CF",
            "type": "url-test",
            "proxies": cf_or_warmup,
            "url": cf_test_url,
            "interval": cf_interval,
            "tolerance": min(tolerance, 30),
            "lazy": False,
            "timeout": cf_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "STREAMING-FAST",
            "type": "url-test",
            "proxies": streaming_or_direct,
            "url": streaming_test_url,
            "interval": active_interval,
            "tolerance": max(tolerance, 50),
            "lazy": False,
            "timeout": fast_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "AUTO-FAST",
            "type": "url-test",
            "proxies": fast_or_direct,
            "url": test_url,
            "interval": active_interval,
            "tolerance": tolerance,
            "lazy": False,
            "timeout": fast_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 2,
        },
        {
            "name": "FALLBACK",
            "type": "fallback",
            "proxies": fallback_or_direct,
            "url": test_url,
            "interval": fallback_interval,
            "lazy": False,
            "timeout": health_timeout,
            "expected-status": "200/204/301/302",
            "max-failed-times": 3,
        },
    ]

    config: dict[str, Any] = {
        "mixed-port": 7890,
        "allow-lan": False,
        "bind-address": "*",
        "mode": "global",
        "log-level": "warning",
        "ipv6": False,
        "unified-delay": True,
        "tcp-concurrent": True,
        **_mihomo_keep_alive_config(),
        "profile": {
            "store-selected": True,
            "store-fake-ip": True,
        },
        "sniffer": {
            "enable": True,
            "sniff": {
                "TLS": {"ports": [443, 8443]},
                "HTTP": {"ports": [80, "8080-8880"], "override-destination": True},
            },
            "skip-domain": ["+.lan", "+.local"],
        },
        "dns": {
            "enable": True,
            "ipv6": False,
            "enhanced-mode": "fake-ip",
            "fake-ip-range": "198.18.0.1/16",
            "fake-ip-filter": _dns_fake_ip_filter(),
            "default-nameserver": ["1.1.1.1", "8.8.8.8"],
            "nameserver": ["https://1.1.1.1/dns-query", "https://dns.google/dns-query"],
        },
        "proxies": [node.clash for node in nodes],
        "proxy-groups": proxy_groups,
    }
    config = _enforce_no_selector_no_direct_config(config)
    return dump_yaml_no_alias(config)


def build_csv(nodes: list[ProxyNode]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "name",
        "original_name",
        "type",
        "network",
        "original_server",
        "original_ip",
        "original_provider",
        "bug_sni",
        "output_server",
        "port",
        "status",
        "tier",
        "bug_best_delay_ms",
        "bug_avg_delay_ms",
        "bug_jitter_ms",
        "bug_success_count",
        "ws_upgrade_ms",
        "ws_success_count",
        "ws_status",
        "original_best_delay_ms",
        "original_success_count",
        "attempts",
        "score",
        "source",
        "reason",
    ])
    for node in nodes:
        writer.writerow([
            node.name,
            node.original_name,
            node.type,
            node_network(node),
            node.original_server,
            node.original_ip,
            node.original_provider,
            node.bug_sni,
            TARGET_SERVER,
            node.port,
            node.status,
            node.tier,
            node.bug_best_delay_ms if node.bug_best_delay_ms is not None else "",
            node.bug_avg_delay_ms if node.bug_avg_delay_ms is not None else "",
            node.bug_jitter_ms if node.bug_jitter_ms is not None else "",
            node.bug_success_count,
            node.ws_upgrade_ms if node.ws_upgrade_ms is not None else "",
            node.ws_success_count,
            node.ws_status,
            node.original_best_delay_ms if node.original_best_delay_ms is not None else "",
            node.original_success_count,
            node.attempts,
            node.score,
            node.source,
            node.reason,
        ])
    return buffer.getvalue()


def _node_passes_output_filters(node: ProxyNode, require_successes: int, max_jitter_ms: int) -> bool:
    return (
        node.status == "alive"
        and node.best_delay_ms is not None
        and node.success_count >= int(require_successes)
        and (int(max_jitter_ms) <= 0 or (node.jitter_ms is not None and node.jitter_ms <= int(max_jitter_ms)))
    )


def _finalize_selected_nodes(
    candidates: list[ProxyNode],
    max_nodes: int,
    fast_target_ms: int,
    fill_delay_ms: int,
    prefer_ws: bool,
) -> list[ProxyNode]:
    fast = [node for node in candidates if (node.best_delay_ms or 999999) <= int(fast_target_ms)]
    for node in fast:
        node.tier = node.tier or f"FAST ≤{fast_target_ms}ms"

    backup = [
        node for node in candidates
        if (node.best_delay_ms or 999999) > int(fast_target_ms)
        and (node.best_delay_ms or 999999) <= int(fill_delay_ms)
    ]
    for node in backup:
        node.tier = node.tier or f"BACKUP ≤{fill_delay_ms}ms"

    selected_pool = fast + backup
    if len(selected_pool) < int(max_nodes):
        existing = {id(n) for n in selected_pool}
        slow_fill = [
            n for n in sorted(candidates, key=lambda n: node_sort_key(n, bool(prefer_ws)))
            if id(n) not in existing
        ]
        for node in slow_fill:
            node.tier = node.tier or "STRICT-SLOW"
        selected_pool.extend(slow_fill)

    selected = select_diverse_nodes(selected_pool, int(max_nodes), bool(prefer_ws))
    selected.sort(key=lambda n: node_sort_key(n, bool(prefer_ws)))
    selected = selected[: int(max_nodes)]
    unique_names(selected)
    return selected


def process_sources(
    links_text: str,
    manual_text: str,
    fetch_timeout: int,
    tcp_timeout: float,
    max_workers: int,
    max_nodes: int,
    fast_target_ms: int,
    fill_delay_ms: int,
    min_output_nodes: int,
    attempts: int,
    require_successes: int,
    require_original: bool,
    candidate_multiplier: int = 30,
    candidate_min: int = 350,
    max_jitter_ms: int = 0,
    prefer_ws: bool = True,
    require_ws_upgrade: bool = True,
    force_ws_only: bool = DEFAULT_FORCE_WS_ONLY,
    reserve_pool_nodes: int = 10,
    early_stop_good_nodes: bool = True,
    test_batch_size: int = 0,
) -> tuple[list[ProxyNode], list[ProxyNode], list[tuple[str, str]], list[str]]:
    """Fetch public subscriptions, test only until enough good auto nodes are found.

    Manual nodes are intentionally handled by generate_yaml.py and should normally
    be passed as an empty manual_text here. This function is optimized for speed:
    it tests WS candidates in small batches and stops once max_nodes good nodes are
    available, instead of testing thousands of nodes until the GitHub Action times out.
    """
    fast_target_ms = min(int(fast_target_ms), FAST_TARGET_DELAY_MS)
    fill_delay_ms = min(max(int(fill_delay_ms), fast_target_ms), HARD_MAX_DELAY_MS)
    final_target = max(1, int(max_nodes))
    # Do not force a minimum of 20 anymore. The requested fast profile outputs 10.
    target = max(final_target, int(min_output_nodes), 1)

    links = [line.strip().strip(",'\"") for line in links_text.splitlines() if line.strip()]
    fetch_logs: list[tuple[str, str]] = []
    raw_uris: list[tuple[str, str]] = []

    if links:
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(int(max_workers), len(links))) as executor:
            futures = [executor.submit(fetch_url_cached, url, int(fetch_timeout)) for url in links]
            for future in concurrent.futures.as_completed(futures):
                url, text, status = future.result()
                fetch_logs.append((url, status))
                if text:
                    for uri in extract_uris(text):
                        raw_uris.append((uri, url))

    # This remains for backward compatibility, but the GitHub Action passes manual_text=""
    # so manual nodes stay outside strict filtering and outside the 10 auto-node quota.
    for uri in extract_uris(manual_text or ""):
        raw_uris.append((uri, "manual"))

    parsed: list[ProxyNode] = []
    seen_keys: set[str] = set()
    skipped: list[str] = []
    for uri, source in raw_uris:
        node = parse_uri(uri, source)
        if not node:
            skipped.append(uri[:140])
            continue
        harden_ws_node(node)
        is_complete, complete_reason = validate_complete_node(node)
        if not is_complete:
            node.status = "incomplete"
            node.reason = complete_reason
            node.score = 999999
            parsed.append(node)
            continue
        if node.key in seen_keys:
            continue
        seen_keys.add(node.key)
        parsed.append(node)

    if force_ws_only:
        for node in parsed:
            if node.status == "pending" and node_network(node) != "ws":
                node.status = "skipped"
                node.reason = "skipped: mode WS only"
                node.score = 999999

    # Small candidate pool, because we stop when enough good nodes are found.
    candidate_limit = max(target * int(candidate_multiplier), int(candidate_min), final_target * 20)
    parsed.sort(
        key=lambda n: (
            0 if n.status == "pending" else 1,
            network_priority_rank(n, bool(prefer_ws)),
            protocol_priority_rank(n),
        )
    )
    parsed = parsed[:candidate_limit]

    testable = [node for node in parsed if node.status == "pending"]
    good_candidates: list[ProxyNode] = []
    batch_size = int(test_batch_size) if int(test_batch_size or 0) > 0 else max(20, min(int(max_workers) * 2, 120))
    batch_size = max(1, batch_size)

    for start_index in range(0, len(testable), batch_size):
        batch = testable[start_index : start_index + batch_size]
        if not batch:
            break
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(int(max_workers), len(batch))) as executor:
            future_map = {
                executor.submit(check_node_bug_compat, node, float(tcp_timeout), int(attempts), bool(require_original), bool(require_ws_upgrade)): node
                for node in batch
            }
            for future in concurrent.futures.as_completed(future_map):
                node = future_map[future]
                try:
                    future.result()
                except Exception as exc:
                    node.status = "dead"
                    node.reason = "check error: " + str(exc)[:120]

        batch_good = [
            node for node in batch
            if _node_passes_output_filters(node, int(require_successes), int(max_jitter_ms))
        ]
        if batch_good:
            good_candidates = select_diverse_nodes(
                good_candidates + batch_good,
                max(final_target, int(reserve_pool_nodes), 1),
                bool(prefer_ws),
            )

        if bool(early_stop_good_nodes) and len(good_candidates) >= final_target:
            # Mark the rest as intentionally untested so the report explains why
            # generation finished quickly instead of testing all candidates.
            remaining = testable[start_index + batch_size :]
            for node in remaining:
                if node.status == "pending":
                    node.status = "skipped"
                    node.reason = "not tested: early stop after enough good nodes"
                    node.score = 999999
            break

    candidates = [
        node for node in parsed
        if _node_passes_output_filters(node, int(require_successes), int(max_jitter_ms))
    ]

    selected = _finalize_selected_nodes(
        candidates,
        max_nodes=final_target,
        fast_target_ms=fast_target_ms,
        fill_delay_ms=fill_delay_ms,
        prefer_ws=bool(prefer_ws),
    )
    return selected, parsed, fetch_logs, skipped

