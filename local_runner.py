#!/usr/bin/env python3
"""
ConvertYAML Local Runner v2.0

Final consolidated runner:
- no GitHub Actions dependency;
- verified TLS with retry + curl fallback;
- Mihomo/sing-box bootstrap;
- upstream compatibility patches;
- YAML sanitation;
- ad/tracker/malware protection;
- YouTube playback guard + browser filter;
- Mihomo validation with clear output.
"""

from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import gzip
import ipaddress
import json
import os
import platform
import re
import shutil
import ssl
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Iterable


from manual_routing_provider import compress_manual_routing
from mrs_compile import apply_compiled_mrs, load_compiled_report
from semantic_rule_audit import remove_safe_shadowed_domains

from openclash_target import (
    DEFAULT_ROUTER_CORE,
    MIHOMO_TARGET_LABEL,
    MIHOMO_TARGET_REVISION,
    OPENCLASH_TARGET_VERSION,
    assert_target_mihomo,
    is_target_mihomo_version,
    mihomo_version_text,
    validate_yaml_file,
)

APP_VERSION = "4.8-precision-optimization"
GITHUB_API = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"

CORE_REPO = "adiorany3/ConvertYAML"
MIHOMO_REPO = "MetaCubeX/mihomo"
SINGBOX_REPO = "SagerNet/sing-box"

REFERENCE_PROFILE_URL = (
    "https://raw.githubusercontent.com/adiorany3/ConvertYAML/"
    "refs/heads/main/openclash_auto.yaml"
)
REFERENCE_PROFILE_CACHE = ".reference/openclash_auto.reference.yaml"

CORE_FILES = ("generate_yaml.py", "sumberyaml_core.py", "security_policy.py", "android_marketplace_policy.py", "android_banking_policy.py", "feed_guard.py", "ai_adblock_classifier.py", "manual_routing_provider.py", "mrs_compile.py", "semantic_rule_audit.py", "requirements.txt", "openclash_target.py")
OUTPUT_YAMLS = (
    "openclash_auto.yaml",
    "openclash_android.yaml",
    "openclash_lite.yaml",
    "openclash_fresh_pool.yaml",
)

DEFAULT_ENV = {
    "MAX_NODES": "20",
    "MIN_OUTPUT_NODES": "10",
    "URLTEST_POOL_NODES": "60",
    "NEKOBOX_POOL_NODES": "30",
    "FRESH_POOL_NODES": "30",
    "REQUIRE_URL_TEST": "true",
    "REQUIRE_NEKOBOX_TEST": "false",
    "OPENCLASH_TARGET_VERSION": OPENCLASH_TARGET_VERSION,
    "MIHOMO_TARGET_REVISION": MIHOMO_TARGET_REVISION,
    "REQUIRE_EXACT_MIHOMO_CORE": "true",
    "FINAL_TARGET_VALIDATION": "true",
    "REQUIRE_OPENCLASH_COMPAT": "true",
    "OPENCLASH_COMPAT_TIMEOUT_SEC": "6",
    "OPENCLASH_COMPAT_WORKERS": "6",
    "OPENCLASH_COMPAT_POOL_MULTIPLIER": "4",
    "URL_TEST_URL": "https://www.gstatic.com/generate_204",
    "NEKOBOX_TEST_URL": "https://www.gstatic.com/generate_204",
    "TEST_URL": "https://www.gstatic.com/generate_204",
    "AI_TEST_URL": "https://chatgpt.com/favicon.ico",
    "AI_OPENAI_TEST_URL": "https://chatgpt.com/favicon.ico",
    "AI_CLAUDE_TEST_URL": "https://claude.ai/favicon.ico",
    "AI_GEMINI_TEST_URL": "https://gemini.google.com/favicon.ico",
    "AI_OTHER_TEST_URL": "https://www.gstatic.com/generate_204",
    "AI_HEALTH_INTERVAL": "180",
    "AI_HEALTH_TIMEOUT_MS": "5000",
    "AI_STABLE_NODE_LIMIT": "8",
    "AI_BACKUP_NODE_LIMIT": "8",
    "AI_STABLE_MAX_DELAY_MS": "250",
    "AI_BACKUP_MAX_DELAY_MS": "700",
    "URL_TEST_TIMEOUT_MS": "5000",
    "NEKOBOX_TEST_TIMEOUT_MS": "7000",
    "FORCE_WS_ONLY": "true",
    "REQUIRE_WS_UPGRADE": "true",
    "PREFER_WS": "true",
    "CANDIDATE_MULTIPLIER": "50",
    "CANDIDATE_MIN": "250",
    "ADAPTIVE_CANDIDATES": "true",
    "CANDIDATE_INITIAL": "250",
    "CANDIDATE_MAX": "2000",
    "RESERVE_POOL_NODES": "120",
    "ATTEMPTS": "3",
    "REQUIRE_SUCCESSES": "2",
    "REQUIRE_ORIGINAL": "true",
    "TCP_TIMEOUT": "3.0",
    "FETCH_TIMEOUT": "12",
    "MAX_WORKERS": "64",
    "HEALTH_TIMEOUT_MS": "6000",
    "RULE_MODE": "Lite",
    "REFERENCE_PROFILE_MODE": "local-pinned",
    "REFERENCE_PROFILE_FILE": "reference_profile_v047156.yaml",
    "REFERENCE_PROFILE_URL": REFERENCE_PROFILE_URL,
    "ADBLOCK_PROFILE": "balanced",
    "ADBLOCK_PROVIDER_INTERVAL": "43200",
    "INDONESIA_ADBLOCK": "true",
    "THREAT_IP_BLOCKING": "true",
    "SECURITY_FEED_GUARD": "true",
    "REFRESH_SECURITY_FEEDS": "true",
    "FEED_REFRESH_TTL_SEC": "43200",
    "FEED_MAX_DROP_RATIO": "0.65",
    "FEED_MAX_GROWTH_RATIO": "4.0",
    "AI_ADBLOCK_ENABLED": "false",
    "AI_ADBLOCK_BASE_URL": "https://ai.tamandata.com/v1",
    "AI_ADBLOCK_MODEL": "tamandata",
    "AI_ADBLOCK_API_KEY_FILE": ".secrets/ai_adblock.key",
    "AI_ADBLOCK_BATCH_SIZE": "25",
    "AI_ADBLOCK_MIN_CONFIDENCE": "0.98",
    "AI_ADBLOCK_TIMEOUT_SEC": "30",
    "MANUAL_ROUTING_COMPRESS": "true",
    "MANUAL_ROUTING_COMPRESS_THRESHOLD": "40",
    "MRS_COMPILE": "auto",
    "SEMANTIC_RULE_OPTIMIZE": "router",
    # Multi-host failover. Only configure hosts/IPs you own or are authorized to use.
    "BUG_SERVERS": "[\"104.17.3.81\"]",
    "BUG_MODE": "fallback",
    "BUG_HEALTH_CHECK": "true",
    "BUG_HEALTH_ATTEMPTS": "1",
    "BUG_MAX_VARIANTS_PER_NODE": "3",
    "BUG_TOTAL_VARIANTS_CAP": "24",
    "BUG_MIN_BASE_NODES": "8",
    "ANDROID_MULTI_HOST_MODE": "primary-cold-fallback",
    "ANDROID_FALLBACK_HOST_LIMIT": "3",
    "ANDROID_FALLBACK_TOTAL_CAP": "24",
    "ANDROID_FALLBACK_INTERVAL": "300",
    "ANDROID_FALLBACK_LAZY": "true",
    "ANDROID_GLOBAL_FALLBACK_INTERVAL": "180",
    "ANDROID_GLOBAL_FALLBACK_LAZY": "true",
    "GLOBAL_HEALTH_INTERVAL": "180",
    "GENERIC_FALLBACK_INTERVAL": "180",
    "GENERIC_HEALTH_TIMEOUT_MS": "5000",
    "GENERIC_MAX_FAILED_TIMES": "3",
    "ANDROID_AUTO_FAST_LAZY": "true",
    # Android-only marketplace/live compatibility. High-confidence threat rules
    # still run first; this guard only bypasses privacy/ad/tracker blocking.
    "ANDROID_MARKETPLACE_LIVE_COMPAT": "true",
    "ANDROID_MARKETPLACE_LIVE_POLICY": "GLOBAL",
    "ANDROID_MARKETPLACE_LIVE_DOMAINS": "",
    "ANDROID_MARKETPLACE_LIVE_EXACT_DOMAINS": "",
    # Android Banking Safe Mode. Domain traffic is DIRECT + real DNS + no sniffer.
    # This does not hide the VPN from bank-app device security checks.
    "ANDROID_BANKING_SAFE_MODE": "true",
    "ANDROID_BANKING_DOMAINS": "[\"seabank.co.id\"]",
    "ANDROID_BANKING_EXACT_DOMAINS": "[]",
    "SUBSCRIPTION_CACHE": "true",
    "SUBSCRIPTION_CACHE_TTL_SEC": "1800",
    "SUBSCRIPTION_CACHE_STALE_IF_ERROR": "true",
    "SUBSCRIPTION_CACHE_DIR": ".runtime_cache/subscriptions",
    "PROVIDER_CACHE": "true",
    "PROVIDER_CACHE_TTL_SEC": "1209600",
    "PROVIDER_CACHE_FILE": ".runtime_cache/provider_cache.json",
    "WARMUP_NODE_LIMIT": "4",
    "WARMUP_INTERVAL": "60",
    "WARMUP_LAZY": "true",
    "CF_WARMUP_NODE_LIMIT": "4",
    "CF_WARMUP_INTERVAL": "90",
    "CF_WARMUP_LAZY": "true",
    "FAST_NODE_LIMIT": "6",
    "WAKEUP_INTERVAL": "60",
    "AUTO_FAST_LAZY": "true",
    "STREAMING_NODE_LIMIT": "5",
    "STREAMING_HEALTH_LAZY": "true",
    "PING_CHECK_INTERVAL": "180",
    "PING_CHECK_LAZY": "true",
    "FALLBACK_INTERVAL": "120",
    "FALLBACK_LAZY": "true",
    "BALANCE_INTERVAL": "180",
    "LOAD_BALANCE_LAZY": "true",
    "LOAD_BALANCE_STRATEGY": "sticky-sessions",
    "LOAD_BALANCE_NODE_LIMIT": "4",
    "KEEP_ALIVE_INTERVAL": "15",
    "KEEP_ALIVE_IDLE": "30",
    "AI_SERVICE_NODE_LIMIT": "8",
    "THREAT_SAFE_FAMILY_DNS": "true",
    # OpenWrt router adblock tier. Enhanced adds a compact HaGeZi Pro++ Mini
    # layer plus focused popup/redirect blocking. Android is not affected.
    "OPENWRT_ADBLOCK_LEVEL": "enhanced",
    # Lite stays conservative by default for low-RAM routers. Set enhanced only
    # when the router has enough memory for the additional text provider.
    "OPENWRT_LITE_ADBLOCK_LEVEL": "compact",
    # OpenWrt-only category protection for gambling destinations frequently
    # reached from sponsored ads. Android is intentionally unchanged.
    "OPENWRT_GAMBLING_BLOCK": "true",
    "OPENWRT_LITE_GAMBLING_BLOCK": "true",
    # DNS-level ad blocking remains off by default to reduce false positives.
    "ADBLOCK_DNS_MODE": "off",
    # v3 lean mode prefers compact MRS providers + high-confidence local rules
    # over overlapping popup/benchmark/streaming provider stacks.
    "ADBLOCK_DEDUP_MODE": "lean",
    "YOUTUBE_ADBLOCK_MODE": "enhanced",
    # Router-only extra exact ad endpoints. This never blocks googlevideo.com
    # or static.doubleclick.net and does not alter Android output.
    "YOUTUBE_ROUTER_EXTRA_ADS": "true",
    "YOUTUBE_TEST_URL": "https://www.gstatic.com/generate_204",
    "YOUTUBE_HEALTH_INTERVAL": "120",
    "YOUTUBE_HEALTH_TIMEOUT_MS": "3000",
    "YOUTUBE_BROWSER_FILTER_FILE": "youtube_browser_filters.txt",
    "SUBSCRIPTION_LINKS_FILE": "subscription_links.txt",
    "MANUAL_NODES_FILE": "manual_nodes.txt",
    "OUTPUT_YAML": "openclash_auto.yaml",
    "OUTPUT_ANDROID_YAML": "openclash_android.yaml",
    "OUTPUT_SINGBOX_ANDROID": "singbox_android.json",
    "OUTPUT_LITE_YAML": "openclash_lite.yaml",
    "OUTPUT_FRESH_YAML": "openclash_fresh_pool.yaml",
    "OUTPUT_CSV": "openclash_auto_report.csv",
    "OUTPUT_AKUN": "akun.txt",
    "OUTPUT_MANUAL_AKUN": "akun_manual.txt",
    "OUTPUT_URLTEST_REPORT": "urltest_report.csv",
    "OUTPUT_NEKOBOX_REPORT": "nekobox_test_report.csv",
    "OUTPUT_OPENCLASH_COMPAT_REPORT": "openclash_compat_report.csv",
    "OUTPUT_NODE_QUALITY_REPORT": "node_quality_report.md",
    "OUTPUT_STAMP": "last_update.txt",
}

from security_policy import (
    ANDROID_BASE_PROVIDERS as ANDROID_SECURITY_PROVIDERS,
    ANDROID_STRICT_PROVIDERS as ANDROID_STRICT_SECURITY_PROVIDERS,
    ROUTER_BASE_PROVIDERS as SECURITY_PROVIDERS,
    ROUTER_STRICT_PROVIDERS as ROUTER_STRICT_SECURITY_PROVIDERS,
    ROUTER_THREAT_SAFE_PROVIDERS as ROUTER_THREAT_SAFE_SECURITY_PROVIDERS,
    ROUTER_THREAT_IP_PROVIDERS as ROUTER_THREAT_IP_PROVIDER,
    managed_provider_names,
    provider_catalog as shared_provider_catalog,
    provider_reject_rules as shared_provider_reject_rules,
)
from android_marketplace_policy import (
    enabled as android_marketplace_live_enabled,
    route_policy as android_marketplace_live_policy,
    guard_rules as android_marketplace_live_guard_rules,
    fake_ip_filters as android_marketplace_live_fake_ip_filters,
    sniffer_skip_domains as android_marketplace_live_sniffer_skip_domains,
    dns_policy_domains as android_marketplace_live_dns_policy_domains,
)
from android_banking_policy import (
    enabled as android_banking_enabled,
    guard_rules as android_banking_guard_rules,
    fake_ip_filters as android_banking_fake_ip_filters,
    sniffer_skip_domains as android_banking_sniffer_skip_domains,
    dns_policy_domains as android_banking_dns_policy_domains,
)

# Child-safe profile uses a family DNS resolver that blocks ads, trackers,
# malware, adult content, and gambling categories.  Keep proxy-server DNS
# separate so proxy hostnames can still resolve even if a family category
# classifies a proxy endpoint unexpectedly.
CHILD_SAFE_DNS = (
    "https://family.dns.bebasid.com/dns-query",
    "tls://family.dns.bebasid.com:853",
)

# Small benchmark-coverage list. It is refreshed at generation time and stored
# inline so Mihomo does not need another runtime HTTP provider. One compatibility
# host is intentionally excluded to preserve YouTube playback reliability.
TURTLECUTE_HOST_URL = "https://raw.githubusercontent.com/Turtlecute33/adblocktest/master/src/d3host.txt"
TURTLECUTE_SNAPSHOT_FILE = "turtlecute_d3host.txt"
TURTLECUTE_EXCLUDE = {"static.doubleclick.net"}

# Conservative streaming-ad layer. Exact hosts only. Never block whole
# spotifycdn.com/fwmrm.net/akamaized.net suffixes because those namespaces can
# also carry playback, licensing, artwork, or app control traffic.
# Spotify-specific ad/measurement endpoints are also treated as exact hosts to
# avoid broad blocking of the service's normal media, auth, and player traffic.
STREAMING_SAFE_AD_DOMAINS = (
    "video-akpcw.spotifycdn.com",
    "805ba.v.fwmrm.net",
    "tvm-mtv-freewheel.akamaized.net",
    "adeventtracker.spotify.com",
    "ads.spotify.com",
    "ads-fa.spotify.com",
    "ads-ak.spotify.com",
    "adserver.spotify.com",
    "adstudio.spotify.com",
    "ad-analytics.spotify.com",
    "aet.spotify.com",
    "analytics.spotify.com",
    "bloodhound.spotify.com",
    "crashdump.spotify.com",
    "pixel.spotify.com",
    "pixel-static.spotify.com",
    "pixels.spotify.com",
)

# Small local fallback for intrusive popunders and mobile/game ad SDKs.
# These are advertising namespaces, not game/CDN namespaces. Keeping them inline
# avoids another HTTP provider and limits rule-evaluation overhead.
POPUNDER_AD_SUFFIXES = (
    "popads.net",
    "popcash.net",
    "propellerads.com",
    "adsterra.com",
    "onclickalgo.com",
    "onclickperformance.com",
    "hilltopads.net",
    "richads.com",
    "clickadu.com",
    "adcash.com",
)

MOBILE_GAME_AD_SUFFIXES = (
    "applovin.com",
    "applvn.com",
    "unityads.unity3d.com",
    "supersonicads.com",
    "ironsrc.com",
    "vungle.com",
    "vunglecloud.com",
    "chartboost.com",
    "inmobi.com",
    "adcolony.com",
    "mintegral.com",
    "mtgglobals.com",
    "rayjump.com",
    "pangle.io",
    "pangleglobal.com",
    "tapjoy.com",
    "tapjoyads.com",
    "startappservice.com",
    "startapp.com",
    "fyber.com",
    "inner-active.mobi",
)

INTRUSIVE_AD_SUFFIXES = tuple(dict.fromkeys(POPUNDER_AD_SUFFIXES + MOBILE_GAME_AD_SUFFIXES))

# v3.4 App-Safe layer. Curated to target advertising namespaces used by
# Android apps, OEM recommendation systems, Windows/macOS app surfaces, and
# common mobile ad SDKs. Keep login, update, push, media, and general CDN
# namespaces out of this list to reduce breakage.
APP_SDK_AD_SUFFIXES = (
    "smaato.com",
    "smaato.net",
    "ogury.com",
    "ogury.co",
    "pubnative.net",
    "hyprmx.com",
    "mobilefuse.com",
    "amazon-adsystem.com",
    "mopub.com",
    "adjoe.io",
)

ANDROID_OEM_APP_AD_DOMAINS = (
    # Xiaomi / MIUI advertising and recommendation endpoints.
    "adv.sec.intl.miui.com",
    "adv.l7.34.sec.miui.com",
    "adv.sec.miui.com",
    "ad.miui.com",
    "api.ads.xiaomi.com",
    "ad.eu.xiaomi.com",
    "ad.quickapp.hybrid.xiaomi.com",
    "ad.india.xiaomi.com",
    "ad.intl.xiaomi.com",
    "xadx.file.market.xiaomi.com",
    "wtradv.market.xiaomi.com",
    "ad.cdn.pandora.xiaomi.com",
    # OPPO / Realme / HeyTap advertising endpoints.
    "ads.heytapmobi.com",
    "ads.heytapmobile.com",
    "ads-bdapi-my.heytapmobile.com",
    "ads-bdapi-ph.heytapmobile.com",
    "ads-bdapi-th.heytapmobile.com",
    "ads-bdapi-vn.heytapmobile.com",
    "ad-growth-in.heytapmobile.com",
    "ad-growth-ru.heytapmobile.com",
    "ad-growth-sg.heytapmobile.com",
    "adx-ads-fr.heytapmobile.com",
    "adx-ads-ru.heytapmobile.com",
    "bdapi-ads-sg.heytapmobile.com",
    "cldata-ads-fr.heytapmobile.com",
    "cldata-ads-ru.heytapmobile.com",
    "sms-ads-in.heytapmobile.com",
    "sms-ads-ru.heytapmobile.com",
    "stgdata-ads-fr.heytapmobile.com",
    "ads.oppomobile.com",
    "adsfs.oppomobile.com",
)

DESKTOP_APP_AD_DOMAINS = (
    # Microsoft / Windows / Office / MSN advertising endpoints.
    "ads.bing.com",
    "adserver.bing.com",
    "outlookads.live.com",
    "ads.microsoft.com",
    "adsdk.microsoft.com",
    "advertising.microsoft.com",
    "bingads.microsoft.com",
    "msadsscale.microsoft.com",
    "ads.eu.msn.com",
    "rmads.eu.msn.com",
    "ads.jp.msn.com",
    "advertising.jp.msn.com",
    "ad.msn.com",
    "adevents.msn.com",
    "ads.msn.com",
    "ads1.msn.com",
    "mobileads.msn.com",
    "rads.msn.com",
    "rmads.msn.com",
    "srtb.msn.com",
    "prod.editor.ads.trafficmanager.net",
    "ads-msn-com-profile.trafficmanager.net",
    "adsdk.trafficmanager.net",
    "dsp-ad-cache-tm.trafficmanager.net",
    "ssp-prod-eastus-nonmutt.trafficmanager.net",
    "msads.net",
    # Apple/macOS app advertising endpoints only, not general Apple services.
    "advertising.apple.com",
    "advp.apple.com",
    "api-adservices.apple.com",
    "iad.apple.com",
    "iadcontent.apple.com",
    "iadmoo.apple.com",
    "iadsdk.apple.com",
    "iadworkbench.apple.com",
    "searchads.apple.com",
)

APP_SAFE_EXACT_DOMAINS = tuple(dict.fromkeys(ANDROID_OEM_APP_AD_DOMAINS + DESKTOP_APP_AD_DOMAINS))
APP_SAFE_SUFFIXES = tuple(dict.fromkeys(APP_SDK_AD_SUFFIXES))

# V380 Pro uses av380.net for cloud traffic. Reject only known ad/telemetry
# hosts first, then bypass broad third-party blocklists for remaining service
# traffic. LAN camera/NVR access is already covered by LAN_DIRECT_RULES.
V380_AD_RULES = (
    "DOMAIN,adstatistics.av380.net,REJECT",
    "DOMAIN,logs.av380.net,REJECT",
    "DOMAIN,ad.av380.net,REJECT",
    "DOMAIN,ads.av380.net,REJECT",
    "DOMAIN,advert.av380.net,REJECT",
    "DOMAIN,advertising.av380.net,REJECT",
    "DOMAIN,promotion.av380.net,REJECT",
    "DOMAIN,promotions.av380.net,REJECT",
    "DOMAIN,app-ad.av380.net,REJECT",
)
V380_SERVICE_RULES = (
    "DOMAIN-SUFFIX,av380.net,DIRECT",
)

# Exact CCTV ad/telemetry hosts observed in local threat feed. Never block
# vendor suffixes: those suffixes also carry login, push, camera, playback.
CHINA_CCTV_AD_DOMAINS = (
    "veepai-device-log.eye4.cn",
    "eulog.ezvizlife.com",
    "log.ezvizlife.com",
    "salog.ezvizlife.com",
    "sgplog.ezvizlife.com",
    "uslog.ezvizlife.com",
    "rum-apis.reolink.com",
    "sentry.tuyaus.com",
    # iCSee/XMEye promotion endpoint.
    "promotion-en.xmeye.net",
)
CHINA_CCTV_AD_RULES = tuple(f"DOMAIN,{domain},REJECT" for domain in CHINA_CCTV_AD_DOMAINS)


def load_turtlecute_domains(workdir: Path) -> list[str]:
    snapshot = workdir / TURTLECUTE_SNAPSHOT_FILE
    # Refresh only when explicitly requested by the updater. A short, single
    # request avoids delaying normal generation when GitHub/DNS is unavailable.
    if os.environ.get("REFRESH_TURTLECUTE", "false").strip().lower() in {"1", "true", "yes", "on"}:
        try:
            req = urllib.request.Request(TURTLECUTE_HOST_URL, headers=_headers(False))
            with urllib.request.urlopen(req, timeout=8, context=_ssl_context()) as response:
                data = response.read()
            if data:
                snapshot.write_bytes(data)
                log("Turtlecute snapshot diperbarui")
        except Exception as exc:
            log(f"Turtlecute refresh gagal, pakai snapshot lokal: {exc}")
    if not snapshot.exists():
        return []
    domains: list[str] = []
    for raw in snapshot.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[0] in {"0.0.0.0", "127.0.0.1"}:
            domain = parts[1].strip().lower().rstrip(".")
            if domain and domain not in TURTLECUTE_EXCLUDE and domain not in domains:
                domains.append(domain)
    return domains

LAN_DIRECT_RULES = (
    "DOMAIN-SUFFIX,local,DIRECT",
    "DOMAIN-SUFFIX,lan,DIRECT",
    "DOMAIN-SUFFIX,localhost,DIRECT",
    "IP-CIDR,127.0.0.0/8,DIRECT,no-resolve",
    "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve",
    "IP-CIDR,172.16.0.0/12,DIRECT,no-resolve",
    "IP-CIDR,192.168.0.0/16,DIRECT,no-resolve",
    "IP-CIDR,169.254.0.0/16,DIRECT,no-resolve",
    "GEOIP,LAN,DIRECT,no-resolve",
)

# Broad keyword rules can block legitimate sites such as analytics dashboards,
# tracker documentation, or applications with those words in a hostname.
OVERBROAD_AD_KEYWORD_RULES = {
    "DOMAIN-KEYWORD,adservice,REJECT",
    "DOMAIN-KEYWORD,analytics,REJECT",
    "DOMAIN-KEYWORD,tracker,REJECT",
}

AI_PROXY_EXACT_DOMAINS = (
    "gemini.google.com",
    "aistudio.google.com",
    "ai.google.dev",
    "generativelanguage.googleapis.com",
    "aiplatform.googleapis.com",
    "copilot.microsoft.com",
    "copilot.cloud.microsoft",
    "sydney.bing.com",
    "api.githubcopilot.com",
    "copilot-proxy.githubusercontent.com",
)

AI_PROXY_DOMAIN_SUFFIXES = (
    "chatgpt.com",
    "openai.com",
    "oaistatic.com",
    "oaiusercontent.com",
    "sora.com",
    "claude.ai",
    "anthropic.com",
    "perplexity.ai",
    "grok.com",
    "x.ai",
    "poe.com",
    "deepseek.com",
    "mistral.ai",
    "meta.ai",
    "qwen.ai",
    "kimi.com",
    "cohere.com",
    "githubcopilot.com",
)

def ai_proxy_rules(target: str = "AI") -> list[str]:
    rules = [f"DOMAIN,{domain},{target}" for domain in AI_PROXY_EXACT_DOMAINS]
    rules.extend(f"DOMAIN-SUFFIX,{domain},{target}" for domain in AI_PROXY_DOMAIN_SUFFIXES)
    return rules


YOUTUBE_PLAYBACK_DOMAINS = (
    "youtube.com",
    "youtu.be",
    "youtube-nocookie.com",
    "googlevideo.com",
    "ytimg.com",
    "youtubei.googleapis.com",
    "youtube.googleapis.com",
    "ggpht.com",
)

# Compatibility endpoints that must stay reachable before broad ad/tracker
# providers. static.doubleclick.net can be required by YouTube's playback
# validation, while jnn-pa.googleapis.com is used by some live playback flows.
# Keep these as exact DOMAIN guards. Never allow the whole doubleclick.net tree.
YOUTUBE_COMPAT_DOMAINS = (
    "static.doubleclick.net",
    "jnn-pa.googleapis.com",
)

# Enhanced mode blocks ad/measurement endpoints that are separable from
# YouTube's primary media delivery. Never add googlevideo.com here. Avoid a
# broad doubleclick.net suffix reject because static.doubleclick.net can be
# required for playback validation.
YOUTUBE_NETWORK_AD_RULES = (
    "DOMAIN,googleads.g.doubleclick.net,REJECT",
    "DOMAIN,ad.doubleclick.net,REJECT",
    "DOMAIN,pubads.g.doubleclick.net,REJECT",
    "DOMAIN,securepubads.g.doubleclick.net,REJECT",
    "DOMAIN,pagead2.googlesyndication.com,REJECT",
    "DOMAIN,tpc.googlesyndication.com,REJECT",
    "DOMAIN,www.googleadservices.com,REJECT",
    "DOMAIN,imasdk.googleapis.com,REJECT",
    "DOMAIN,ads.youtube.com,REJECT",
    "DOMAIN-SUFFIX,2mdn.net,REJECT",
    "DOMAIN-SUFFIX,googlesyndication.com,REJECT",
    "DOMAIN-SUFFIX,googleadservices.com,REJECT",
    # Current Google Ads catalog endpoints; keep media/CDN hosts untouched.
    "DOMAIN,adtrafficquality.google,REJECT",
    "DOMAIN-SUFFIX,googleadapis.com,REJECT",
    "DOMAIN,mobileads.google.com,REJECT",
    "DOMAIN,pagead.l.google.com,REJECT",
)

# Router-only exact ad/measurement endpoints. These are intentionally not
# suffix rules because parts of doubleclick.net are used by YouTube playback.
# Keep Android conservative and preserve static.doubleclick.net.
YOUTUBE_ROUTER_EXTRA_AD_RULES = (
    "DOMAIN,adservice.google.com,REJECT",
    "DOMAIN,pagead2.googleadservices.com,REJECT",
    "DOMAIN,afs.googlesyndication.com,REJECT",
    "DOMAIN,stats.g.doubleclick.net,REJECT",
    "DOMAIN,m.doubleclick.net,REJECT",
    "DOMAIN,mediavisor.doubleclick.net,REJECT",
)

YOUTUBE_BROWSER_FILTERS_SAFE = """\
! ConvertYAML Local Runner v2.0
! Cosmetic YouTube filters. Do not block googlevideo.com.
youtube.com##ytd-display-ad-renderer
youtube.com##ytd-ad-slot-renderer
youtube.com##ytd-promoted-video-renderer
youtube.com##ytd-promoted-sparkles-web-renderer
youtube.com##ytd-in-feed-ad-layout-renderer
youtube.com##ytd-banner-promo-renderer
youtube.com##ytd-companion-slot-renderer
youtube.com##ytd-action-companion-ad-renderer
youtube.com##ytd-ad-engagement-panel-renderer
youtube.com##ytd-player-legacy-desktop-watch-ads-renderer
youtube.com##ytd-promoted-sparkles-text-search-renderer
youtube.com##.ytp-ad-module
youtube.com##.video-ads
youtube.com##.ytp-ad-overlay-container
youtube.com##.ytp-ad-player-overlay
youtube.com##.ytp-ad-text-overlay
youtube.com##.ytp-ad-image-overlay
youtube.com##.ytp-ad-progress-list
youtube.com##ytd-rich-item-renderer:has(ytd-ad-slot-renderer)
youtube.com##ytd-search ytd-ad-slot-renderer
youtube.com##ytd-watch-next-secondary-results-renderer ytd-ad-slot-renderer
youtube.com##ytm-ad-slot-renderer
youtube.com##ytm-promoted-video-renderer
youtube.com##ytm-rich-item-renderer:has(ytm-ad-slot-renderer)
youtube.com##ytm-promoted-sparkles-web-renderer
"""

YOUTUBE_BROWSER_FILTERS_ENHANCED = """\
! Additional endpoints separated from the main media CDN.
! static.doubleclick.net is intentionally NOT blocked because some YouTube
! playback validation depends on /instream/ad_status.js.
||googleads.g.doubleclick.net^$domain=youtube.com
||ad.doubleclick.net^$domain=youtube.com
||pubads.g.doubleclick.net^$domain=youtube.com
||securepubads.g.doubleclick.net^$domain=youtube.com
||pagead2.googlesyndication.com^$domain=youtube.com
||tpc.googlesyndication.com^$domain=youtube.com
||www.googleadservices.com^$domain=youtube.com
||adservice.google.com^$domain=youtube.com
||pagead2.googleadservices.com^$domain=youtube.com
||afs.googlesyndication.com^$domain=youtube.com
||stats.g.doubleclick.net^$domain=youtube.com
||m.doubleclick.net^$domain=youtube.com
||mediavisor.doubleclick.net^$domain=youtube.com
||adtrafficquality.google^$domain=youtube.com
||googleadapis.com^$domain=youtube.com
||mobileads.google.com^$domain=youtube.com
||pagead.l.google.com^$domain=youtube.com
||ads.youtube.com^$domain=youtube.com
||youtube.com/api/stats/ads^$xhr,domain=youtube.com
||youtube.com/pagead/*$xhr,domain=youtube.com
||youtube.com/pagead/parallelad^$xhr,domain=youtube.com
||youtube.com/ptracking^$xhr,domain=youtube.com

! Conservative in-page pruning for browser blockers that support uBO scriptlets.
youtube.com##+js(set-constant, ytInitialPlayerResponse.adPlacements, undefined)
youtube.com##+js(set-constant, ytInitialPlayerResponse.adSlots, undefined)
youtube.com##+js(set-constant, ytInitialPlayerResponse.playerAds, undefined)
"""


def log(message: str) -> None:
    print(f"[LOCAL] {message}", flush=True)


_YAML_TX_CACHE: dict[Path, dict[str, Any]] = {}
_YAML_TX_DIRTY: set[Path] = set()
_YAML_TX_STATS: dict[Path, dict[str, int]] = {}


def _yaml_key(path: Path) -> Path:
    try:
        return path.expanduser().resolve()
    except Exception:
        return path


def _yaml_load_config(path: Path) -> dict[str, Any]:
    """Load YAML once inside a transaction, otherwise behave like safe_load."""
    import yaml

    key = _yaml_key(path)
    if key in _YAML_TX_CACHE:
        return _YAML_TX_CACHE[key]
    obj = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(obj, dict):
        raise RuntimeError(f"{path.name}: root YAML bukan mapping")
    stats = _YAML_TX_STATS.setdefault(key, {"loads": 0, "writes": 0})
    stats["loads"] += 1
    return obj


def _yaml_store_config(path: Path, config: dict[str, Any]) -> None:
    """Queue one final YAML serialization when a transaction is active."""
    import yaml

    key = _yaml_key(path)
    if key in _YAML_TX_CACHE:
        _YAML_TX_CACHE[key] = config
        _YAML_TX_DIRTY.add(key)
        return
    path.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=160),
        encoding="utf-8",
    )
    stats = _YAML_TX_STATS.setdefault(key, {"loads": 0, "writes": 0})
    stats["writes"] += 1


@contextmanager
def yaml_edit_transaction(path: Path):
    """One file parse + one final serialization for the whole optimization pass."""
    import yaml

    key = _yaml_key(path)
    if key in _YAML_TX_CACHE:
        yield _YAML_TX_CACHE[key]
        return
    obj = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(obj, dict):
        raise RuntimeError(f"{path.name}: root YAML bukan mapping")
    _YAML_TX_CACHE[key] = obj
    _YAML_TX_STATS[key] = {"loads": 1, "writes": 0}
    try:
        yield obj
        if key in _YAML_TX_DIRTY:
            path.write_text(
                yaml.safe_dump(_YAML_TX_CACHE[key], allow_unicode=True, sort_keys=False, width=160),
                encoding="utf-8",
            )
            _YAML_TX_STATS[key]["writes"] += 1
    finally:
        _YAML_TX_CACHE.pop(key, None)
        _YAML_TX_DIRTY.discard(key)


def yaml_transaction_stats(path: Path) -> dict[str, int]:
    return dict(_YAML_TX_STATS.get(_yaml_key(path), {"loads": 0, "writes": 0}))


def _headers(json_api: bool = False) -> dict[str, str]:
    headers = {"User-Agent": f"ConvertYAML-Local-Runner/{APP_VERSION}"}
    if json_api:
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = GITHUB_API_VERSION
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _ssl_context() -> ssl.SSLContext:
    context = ssl.create_default_context()
    try:
        import certifi  # type: ignore
        cafile = certifi.where()
        if cafile and Path(cafile).exists():
            context.load_verify_locations(cafile=cafile)
    except Exception:
        pass
    return context


def _curl_available() -> bool:
    return shutil.which("curl") is not None


def _curl_base() -> list[str]:
    args = [
        "curl", "--fail", "--location", "--silent", "--show-error",
        "--retry", "4", "--retry-delay", "2", "--retry-max-time", "90",
        "--connect-timeout", "20", "--max-time", "180", "--http1.1",
        "-A", f"ConvertYAML-Local-Runner/{APP_VERSION}",
    ]
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        args += ["-H", f"Authorization: Bearer {token}"]
    return args


def request_json(url: str) -> dict:
    errors: list[str] = []
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url, headers=_headers(True))
            with urllib.request.urlopen(req, timeout=45, context=_ssl_context()) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            errors.append(f"urllib #{attempt}: {exc}")
            if attempt < 3:
                log(f"GitHub API via Python gagal, retry {attempt}/3")
                time.sleep(attempt * 2)

    if _curl_available():
        log("Fallback ke curl sistem dengan TLS verification aktif")
        cmd = _curl_base() + [
            "-H", "Accept: application/vnd.github+json",
            "-H", f"X-GitHub-Api-Version: {GITHUB_API_VERSION}",
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return json.loads(result.stdout)
        errors.append("curl: " + (result.stderr.strip() or str(result.returncode)))

    raise RuntimeError(
        "Gagal mengakses GitHub API.\n"
        + "\n".join(f"  - {item}" for item in errors)
        + "\nTes manual: curl -I https://api.github.com"
    )


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    for attempt in range(1, 4):
        part = destination.with_suffix(destination.suffix + ".part")
        part.unlink(missing_ok=True)
        try:
            req = urllib.request.Request(url, headers=_headers(False))
            with urllib.request.urlopen(req, timeout=120, context=_ssl_context()) as response, part.open("wb") as out:
                shutil.copyfileobj(response, out)
            if not part.exists() or part.stat().st_size == 0:
                raise RuntimeError("hasil download kosong")
            part.replace(destination)
            return
        except Exception as exc:
            part.unlink(missing_ok=True)
            errors.append(f"urllib #{attempt}: {exc}")
            if attempt < 3:
                log(f"Download via Python gagal, retry {attempt}/3")
                time.sleep(attempt * 2)

    if _curl_available():
        log("Fallback download ke curl sistem")
        part = destination.with_suffix(destination.suffix + ".part")
        part.unlink(missing_ok=True)
        result = subprocess.run(
            _curl_base() + ["--output", str(part), url],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and part.exists() and part.stat().st_size > 0:
            part.replace(destination)
            return
        part.unlink(missing_ok=True)
        errors.append("curl: " + (result.stderr.strip() or str(result.returncode)))

    raise RuntimeError(f"Gagal mengunduh {url}\n" + "\n".join(errors))


def raw_github_url(repo: str, filename: str, branch: str = "main") -> str:
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{filename}"


def ensure_core_files(workdir: Path, refresh: bool) -> None:
    """Verify the target-pinned source package without overwriting it from another repo."""
    missing = [name for name in CORE_FILES if not (workdir / name).is_file()]
    if missing:
        raise RuntimeError(
            "Paket target tidak lengkap. File hilang: " + ", ".join(missing)
        )
    if refresh:
        log(
            "--refresh-core diabaikan untuk source target-pinned. "
            "generate_yaml.py dan sumberyaml_core.py tidak boleh ditimpa remote karena "
            f"paket ini dikunci ke OpenClash {OPENCLASH_TARGET_VERSION} / {MIHOMO_TARGET_LABEL}."
        )
    else:
        log("Source target-pinned lengkap")

def ensure_input_files(workdir: Path) -> None:
    defaults = {
        "subscription_links.txt": "# Tambahkan subscription publik/milik Anda. Satu URL per baris.\n",
        "manual_nodes.txt": "# Node manual opsional. Satu URI per baris.\n",
        "adblock_allowlist.txt": "# Domain yang tidak boleh diblokir. Satu domain per baris.\n",
    }
    for name, body in defaults.items():
        path = workdir / name
        if not path.exists():
            path.write_text(body, encoding="utf-8")


def install_dependencies() -> None:
    try:
        import requests  # noqa: F401
        import yaml  # noqa: F401
        import certifi  # noqa: F401
        return
    except Exception:
        pass
    log("Memasang requests, PyYAML, certifi")
    subprocess.run(
        [
            sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
            "requests>=2.31", "PyYAML>=6.0", "certifi>=2024.2.2",
        ],
        check=True,
    )


def normalized_platform() -> tuple[str, str]:
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system not in {"windows", "linux", "darwin"}:
        raise RuntimeError(f"OS belum didukung: {platform.system()}")
    if machine in {"x86_64", "amd64", "x64"}:
        arch = "amd64"
    elif machine in {"arm64", "aarch64"}:
        arch = "arm64"
    else:
        raise RuntimeError(f"Arsitektur belum didukung: {platform.machine()}")
    return system, arch


def executable_name(name: str) -> str:
    return name + (".exe" if platform.system().lower() == "windows" else "")


def make_executable(path: Path) -> None:
    if platform.system().lower() != "windows":
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def select_mihomo_asset(assets: list[dict], os_name: str, arch: str) -> dict:
    prefix = f"mihomo-{os_name}-{arch}"
    candidates: list[tuple[int, int, dict]] = []
    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if not name.startswith(prefix) or "debug" in name:
            continue
        if not (name.endswith(".gz") or name.endswith(".zip")):
            continue
        score = 0
        if "compatible" in name:
            score += 20
        if "-v1-" in name or "-v2-" in name or "-v3-" in name:
            score += 10
        candidates.append((score, len(name), asset))
    if not candidates:
        raise RuntimeError(f"Asset Mihomo tidak ditemukan untuk {os_name}/{arch}")
    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][2]


def select_singbox_asset(assets: list[dict], os_name: str, arch: str) -> dict:
    needle = f"-{os_name}-{arch}"
    candidates = []
    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if name.startswith("sing-box-") and needle in name and (name.endswith(".tar.gz") or name.endswith(".zip")):
            candidates.append(asset)
    if not candidates:
        raise RuntimeError(f"Asset sing-box tidak ditemukan untuk {os_name}/{arch}")
    return sorted(candidates, key=lambda asset: len(str(asset.get("name", ""))))[0]


def extract_binary(archive: Path, binary_name: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if archive.name.endswith(".tar.gz"):
        with tarfile.open(archive, "r:gz") as tf:
            members = [m for m in tf.getmembers() if m.isfile() and Path(m.name).name.lower() == binary_name.lower()]
            if not members:
                raise RuntimeError(f"{binary_name} tidak ada dalam {archive.name}")
            src = tf.extractfile(members[0])
            if src is None:
                raise RuntimeError("Gagal extract")
            with output.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    elif archive.name.endswith(".zip"):
        with zipfile.ZipFile(archive) as zf:
            names = [name for name in zf.namelist() if Path(name).name.lower() == binary_name.lower()]
            if not names:
                raise RuntimeError(f"{binary_name} tidak ada dalam {archive.name}")
            with zf.open(names[0]) as src, output.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    elif archive.name.endswith(".gz"):
        with gzip.open(archive, "rb") as src, output.open("wb") as dst:
            shutil.copyfileobj(src, dst)
    else:
        raise RuntimeError(f"Archive tidak didukung: {archive.name}")
    make_executable(output)


def ensure_binary(workdir: Path, repo: str, program: str, selector, refresh: bool) -> Path:
    bin_dir = workdir / ".local_bin"
    bin_dir.mkdir(exist_ok=True)
    exe = executable_name(program)
    local = bin_dir / exe

    if local.exists() and not refresh:
        log(f"{program} lokal: {local}")
        return local

    if not refresh:
        system_binary = shutil.which(exe) or shutil.which(program)
        if system_binary:
            path = Path(system_binary).resolve()
            log(f"{program} dari PATH: {path}")
            return path

    os_name, arch = normalized_platform()
    log(f"Mencari {program} terbaru untuk {os_name}/{arch}")
    release = request_json(f"{GITHUB_API}/repos/{repo}/releases/latest")
    asset = selector(release.get("assets") or [], os_name, arch)

    with tempfile.TemporaryDirectory(prefix=f"{program}-") as temp_dir:
        archive = Path(temp_dir) / str(asset["name"])
        download(str(asset["browser_download_url"]), archive)
        extract_binary(archive, exe, local)
    return local


def _core_version_or_error(path: Path) -> tuple[str, str | None]:
    try:
        return mihomo_version_text(path), None
    except Exception as exc:
        return "", str(exc)


def select_target_mihomo(args, workdir: Path, config: dict[str, str]) -> Path:
    """Prefer the exact target core and never silently validate with a different Mihomo."""
    candidates: list[Path] = []
    if getattr(args, "mihomo_path", None):
        candidates.append(Path(args.mihomo_path).expanduser())
    configured = os.environ.get("MIHOMO_PATH", "").strip() or str(config.get("MIHOMO_PATH", "")).strip()
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.append(Path(DEFAULT_ROUTER_CORE))
    candidates.append(workdir / ".local_bin" / executable_name("mihomo"))
    for name in ("mihomo", "clash-meta", "clash_meta"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))

    seen: set[str] = set()
    mismatches: list[str] = []
    for candidate in candidates:
        key = str(candidate)
        if key in seen or not candidate.is_file():
            continue
        seen.add(key)
        version, error = _core_version_or_error(candidate)
        if error:
            mismatches.append(f"{candidate}: {error}")
            continue
        if is_target_mihomo_version(version):
            path = candidate.resolve()
            log(f"Mihomo exact target: {path}")
            log(f"Versi: {version}")
            return path
        mismatches.append(f"{candidate}: {version}")

    allow_other = bool(getattr(args, "allow_non_target_core", False)) or str(
        config.get("REQUIRE_EXACT_MIHOMO_CORE", "true")
    ).strip().lower() in {"0", "false", "no", "off"}
    if allow_other:
        log("[WARN] Exact target tidak ditemukan; mode non-target diizinkan.")
        return ensure_binary(workdir, MIHOMO_REPO, "mihomo", select_mihomo_asset, args.refresh_binaries)

    details = "\n".join("  - " + item for item in mismatches) or "  - tidak ada kandidat core lokal"
    raise RuntimeError(
        "Mihomo exact target tidak ditemukan.\n"
        f"Target: OpenClash {OPENCLASH_TARGET_VERSION}, {MIHOMO_TARGET_LABEL}.\n"
        "Gunakan --mihomo-path /path/ke/core atau set MIHOMO_PATH.\n"
        f"Pada router OpenClash, lokasi normalnya {DEFAULT_ROUTER_CORE}.\n"
        "Kandidat yang diperiksa:\n" + details
    )


def load_config(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Config JSON harus object")
    normalized: dict[str, str] = {}
    for key, value in data.items():
        if isinstance(value, (list, dict)):
            normalized[str(key)] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        elif isinstance(value, bool):
            normalized[str(key)] = "true" if value else "false"
        else:
            normalized[str(key)] = str(value)
    return normalized


def patch_core_compatibility(workdir: Path) -> None:
    """The packaged generator is already target-patched. Never mutate it at runtime."""
    required = (workdir / "generate_yaml.py", workdir / "sumberyaml_core.py")
    missing = [path.name for path in required if not path.is_file()]
    if missing:
        raise RuntimeError("Source generator hilang: " + ", ".join(missing))
    log("Runtime source patch dinonaktifkan; menggunakan source target-pinned")

def build_environment(args, workdir: Path, mihomo: Path, singbox: Path | None) -> dict[str, str]:
    env = os.environ.copy()
    env.update(DEFAULT_ENV)
    env.update(load_config(args.config))
    env["MAX_NODES"] = str(args.max_nodes)
    env["MIN_OUTPUT_NODES"] = str(min(args.min_nodes, args.max_nodes))
    env["MIHOMO_PATH"] = str(mihomo.resolve())
    if getattr(args, "allow_non_target_core", False):
        env["REQUIRE_EXACT_MIHOMO_CORE"] = "false"
    if singbox is not None:
        env["SINGBOX_PATH"] = str(singbox.resolve())
    if args.no_nekobox:
        env["REQUIRE_NEKOBOX_TEST"] = "false"
    if args.no_ws_only:
        env["FORCE_WS_ONLY"] = "false"
    if args.candidate_min is not None:
        env["CANDIDATE_MIN"] = str(args.candidate_min)
    if args.urltest_pool is not None:
        env["URLTEST_POOL_NODES"] = str(args.urltest_pool)
    if args.nekobox_pool is not None:
        env["NEKOBOX_POOL_NODES"] = str(args.nekobox_pool)
    return env


def load_allowlist(workdir: Path) -> list[str]:
    path = workdir / "adblock_allowlist.txt"
    if not path.exists():
        return []
    domains = []
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        value = raw.strip().lower().rstrip(".")
        if not value or value.startswith("#"):
            continue
        value = re.sub(r"^https?://", "", value).split("/", 1)[0]
        if value.startswith("*.") or value.startswith("+."):
            value = value[2:]
        if re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", value) and "." in value and ".." not in value:
            domains.append(value)
    return sorted(set(domains))


def load_ai_adblock_domains(workdir: Path, allowlist: set[str]) -> list[str]:
    if os.environ.get("AI_ADBLOCK_ENABLED", "false").strip().lower() in {"0", "false", "no", "off"}:
        return []
    from ai_adblock_classifier import is_allowlisted, load_domains

    return [
        domain for domain in load_domains(workdir / ".runtime_cache" / "ai_adblock_blocklist.txt")
        if not is_allowlisted(domain, allowlist)
    ]

def _safe_provider_path(name: str, provider: dict) -> str:
    fmt = str(provider.get("format") or "yaml").lower()
    ext = ".mrs" if fmt == "mrs" else ".txt" if fmt == "text" else ".yaml"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "provider"
    return f"./ruleset/{slug}{ext}"


def _valid_policies(config: dict) -> set[str]:
    names = {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}
    for item in config.get("proxies", []) or []:
        if isinstance(item, dict) and item.get("name"):
            names.add(str(item["name"]))
    for item in config.get("proxy-groups", []) or []:
        if isinstance(item, dict) and item.get("name"):
            names.add(str(item["name"]))
    return names


def _default_route(config: dict) -> str:
    valid = _valid_policies(config)
    rules = config.get("rules") or []
    for raw in reversed(rules):
        parts = [part.strip() for part in str(raw).split(",")]
        if len(parts) >= 2 and parts[0].upper() in {"MATCH", "FINAL"} and parts[1] in valid:
            return parts[1]
    for name in ("GLOBAL", "PROXY", "Proxy", "AUTO", "Auto"):
        if name in valid:
            return name
    groups = [
        group.get("name") for group in config.get("proxy-groups", []) or []
        if isinstance(group, dict) and group.get("name")
    ]
    return str(groups[0]) if groups else "DIRECT"



def _strict_hostname_or_ip(value: str) -> tuple[bool, str]:
    """Strict public proxy hostname/IP validation for OpenClash output."""
    raw = str(value or "").strip()
    if not raw:
        return False, "empty"

    # Bracketed IPv6.
    ip_candidate = raw[1:-1] if raw.startswith("[") and raw.endswith("]") else raw
    try:
        ipaddress.ip_address(ip_candidate)
        return True, ip_candidate
    except ValueError:
        pass

    # Public proxy domains should be ASCII DNS names. Validate case-insensitively
    # but preserve the original spelling so validation itself does not rewrite
    # proxy transport metadata.
    original_name = raw.rstrip(".")
    name = original_name.lower()
    if len(name) > 253 or "." not in name:
        return False, "invalid hostname length/shape"
    labels = name.split(".")
    for label in labels:
        if not (1 <= len(label) <= 63):
            return False, "invalid label length"
        if label.startswith("-") or label.endswith("-"):
            return False, "label starts/ends with hyphen"
        if not re.fullmatch(r"[a-z0-9-]+", label):
            return False, "invalid hostname character"
    return True, original_name


def strict_proxy_domain_filter(config: dict, source_name: str = "") -> int:
    """
    Normalize and remove proxies with unsafe server/SNI/WS Host values.

    This filter is intentionally stricter than DNS itself because generated
    public subscription nodes should not contain whitespace, wildcard
    expressions, URL schemes, IDN text, or malformed labels in fields that
    Mihomo/OpenClash interpret as a host/domain.
    """
    proxies = config.get("proxies")
    if not isinstance(proxies, list):
        return 0

    kept = []
    removed_names = []

    for proxy in proxies:
        if not isinstance(proxy, dict):
            continue
        name = str(proxy.get("name") or "UNNAMED")
        bad_reason = None

        # server can be IP or hostname.
        if isinstance(proxy.get("server"), str):
            ok, normalized = _strict_hostname_or_ip(proxy["server"])
            if not ok:
                bad_reason = f"server: {normalized}"
            else:
                proxy["server"] = normalized

        # SNI/domain fields.
        for field in ("servername", "sni"):
            if bad_reason:
                break
            if isinstance(proxy.get(field), str) and proxy[field].strip():
                ok, normalized = _strict_hostname_or_ip(proxy[field])
                if not ok:
                    bad_reason = f"{field}: {normalized}"
                    break
                proxy[field] = normalized

        # WebSocket Host.
        if not bad_reason:
            ws = proxy.get("ws-opts")
            if isinstance(ws, dict):
                headers = ws.get("headers")
                if isinstance(headers, dict):
                    host_key = next(
                        (k for k in headers if str(k).lower() == "host"),
                        None,
                    )
                    if host_key is not None and isinstance(headers.get(host_key), str):
                        ok, normalized = _strict_hostname_or_ip(headers[host_key])
                        if not ok:
                            bad_reason = f"ws Host: {normalized}"
                        else:
                            headers[host_key] = normalized

        if bad_reason:
            removed_names.append(name)
            log(f"{source_name}: SKIP strict-domain {name}: {bad_reason}")
        else:
            kept.append(proxy)

    if removed_names:
        config["proxies"] = kept
        valid_proxy_names = {
            str(p.get("name"))
            for p in kept
            if isinstance(p, dict) and p.get("name")
        }
        group_names = {
            str(g.get("name"))
            for g in config.get("proxy-groups", []) or []
            if isinstance(g, dict) and g.get("name")
        }
        valid_refs = valid_proxy_names | group_names | {
            "DIRECT", "REJECT", "PASS", "COMPATIBLE"
        }

        fallback = next(iter(valid_proxy_names), "DIRECT")
        for group in config.get("proxy-groups", []) or []:
            if not isinstance(group, dict):
                continue
            refs = group.get("proxies")
            if isinstance(refs, list):
                group["proxies"] = [
                    str(ref) for ref in refs if str(ref) in valid_refs
                ]
                if not group["proxies"]:
                    group["proxies"] = [fallback]

    return len(removed_names)

def sanitize_yaml(path: Path) -> bool:
    import yaml

    if not path.exists():
        return False
    try:
        config = _yaml_load_config(path)
    except Exception as exc:
        raise RuntimeError(f"{path.name}: YAML tidak dapat diparse: {exc}") from exc

    changed = False
    removed_strict = strict_proxy_domain_filter(config, path.name)
    if removed_strict:
        changed = True

    if "global-client-fingerprint" in config:
        config.pop("global-client-fingerprint", None)
        log(f"{path.name}: hapus global-client-fingerprint")
        changed = True

    # Portable local output should not contain OpenClash runtime absolute UI paths.
    external_ui = config.get("external-ui")
    if isinstance(external_ui, str) and external_ui.startswith("/"):
        config.pop("external-ui", None)
        log(f"{path.name}: hapus external-ui absolut dari output portable")
        changed = True

    dns = config.get("dns")
    if isinstance(dns, dict):
        fake_filter = dns.get("fake-ip-filter")
        if isinstance(fake_filter, list):
            cleaned_filter = []
            for raw_domain in fake_filter:
                value = str(raw_domain or "").strip()
                check = value[2:] if value.startswith("+.") else (value[1:] if value.startswith(".") else value)
                valid = bool(value) and not any(ch.isspace() for ch in value)
                if "+" in value and not value.startswith("+."):
                    valid = False
                labels = check.split(".") if check else []
                if not labels or any(not label for label in labels):
                    valid = False
                if any("*" in label and label != "*" for label in labels):
                    valid = False
                if valid:
                    cleaned_filter.append(value)
                else:
                    log(f"{path.name}: hapus fake-ip-filter domain invalid: {value}")
                    changed = True
            if cleaned_filter != fake_filter:
                dns["fake-ip-filter"] = cleaned_filter

        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            # Remove only stale keys injected by older runner versions.
            if "geosite:category-ads-all,tracker" in policy:
                policy.pop("geosite:category-ads-all,tracker", None)
                changed = True
            for domain in YOUTUBE_PLAYBACK_DOMAINS:
                for key in (domain, f"+.{domain}"):
                    if key in policy:
                        policy.pop(key, None)
                        changed = True

    legacy_security_providers = {
        "security-tif-mini",
        "awavenue-ads",
    }
    providers0 = config.get("rule-providers")
    if isinstance(providers0, dict):
        for old_name in legacy_security_providers:
            if old_name in providers0:
                providers0.pop(old_name, None)
                log(f"{path.name}: hapus provider TXT lama {old_name}")
                changed = True

    providers = config.get("rule-providers")
    if providers is not None and not isinstance(providers, dict):
        config["rule-providers"] = {}
        providers = config["rule-providers"]
        changed = True

    if isinstance(providers, dict):
        for name, provider in list(providers.items()):
            if not isinstance(provider, dict):
                continue
            if str(provider.get("type") or "").lower() == "http":
                provider_path = str(provider.get("path") or "").strip()
                path_parts = Path(provider_path).parts if provider_path else ()
                if not provider_path or provider_path.startswith("/") or ".." in path_parts:
                    provider["path"] = _safe_provider_path(str(name), provider)
                    log(f"{path.name}: normalisasi path provider {name}")
                    changed = True
                if "interval" not in provider:
                    provider["interval"] = 43200
                    changed = True

    rules = config.get("rules")
    if not isinstance(rules, list):
        rules = []
        config["rules"] = rules
        changed = True

    known_providers = set((config.get("rule-providers") or {}).keys())
    cleaned_rules: list[str] = []
    seen_rules = set()
    for raw in rules:
        value = str(raw).strip()
        if not value:
            changed = True
            continue
        if re.match(
            r"(?i)^RULE-SET\s*,\s*(security-tif-mini|awavenue-ads)\s*,",
            value,
        ):
            log(f"{path.name}: hapus RULE-SET provider TXT lama")
            changed = True
            continue

        if re.match(r"(?i)^GEOSITE\s*,\s*tracker\s*,", value):
            log(f"{path.name}: hapus GEOSITE,tracker yang tidak portable")
            changed = True
            continue

        parts = [part.strip() for part in value.split(",")]
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET":
            provider_name = parts[1]
            if known_providers and provider_name not in known_providers:
                log(f"{path.name}: hapus RULE-SET tanpa provider: {provider_name}")
                changed = True
                continue

        if value not in seen_rules:
            cleaned_rules.append(value)
            seen_rules.add(value)
        else:
            changed = True
    config["rules"] = cleaned_rules

    proxies = [
        proxy for proxy in config.get("proxies", []) or []
        if isinstance(proxy, dict) and str(proxy.get("name") or "").strip()
    ]
    proxy_names = {str(proxy["name"]) for proxy in proxies}
    groups = [
        group for group in config.get("proxy-groups", []) or []
        if isinstance(group, dict) and str(group.get("name") or "").strip()
    ]
    group_names = {str(group["name"]) for group in groups}
    valid_refs = proxy_names | group_names | {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}
    fallback = sorted(proxy_names)[0] if proxy_names else "DIRECT"

    for group in groups:
        refs = group.get("proxies")
        if not isinstance(refs, list):
            continue
        new_refs = []
        seen = set()
        for ref in refs:
            name = str(ref)
            if name in valid_refs and name not in seen:
                new_refs.append(name)
                seen.add(name)
        if new_refs != refs:
            log(f"{path.name}: bersihkan referensi group {group.get('name')}")
            group["proxies"] = new_refs
            changed = True
        if not group.get("proxies"):
            group["proxies"] = [fallback]
            changed = True

    if "MANUAL" not in group_names:
        fixed_rules = []
        route = _default_route(config)
        for rule in config["rules"]:
            parts = [part.strip() for part in str(rule).split(",")]
            if len(parts) >= 2:
                idx = -2 if parts[-1] == "no-resolve" and len(parts) >= 3 else -1
                if parts[idx] == "MANUAL":
                    parts[idx] = route
                    changed = True
            fixed_rules.append(",".join(parts))
        config["rules"] = fixed_rules

    if changed:
        _yaml_store_config(path, config)
    return changed



def apply_reference_profile(
    path: Path,
    workdir: Path,
    reference_url: str = REFERENCE_PROFILE_URL,
) -> bool:
    """
    Use the working ConvertYAML openclash_auto.yaml as the routing baseline.

    Preserved from newly generated output:
      - proxies
      - proxy-groups
      - runtime/top-level settings

    Locked to known-good reference:
      - profile
      - sniffer
      - dns
      - rule-providers
      - rules
    """
    import yaml

    if not path.exists():
        return False

    generated = _yaml_load_config(path)

    mode = os.environ.get("REFERENCE_PROFILE_MODE", "local-pinned").strip().lower()
    local_name = os.environ.get("REFERENCE_PROFILE_FILE", "reference_profile_v047156.yaml").strip() or "reference_profile_v047156.yaml"
    local_path = workdir / local_name
    cache_path = workdir / REFERENCE_PROFILE_CACHE
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if mode == "local-pinned":
        if not local_path.is_file():
            raise RuntimeError(f"Reference profile lokal tidak ditemukan: {local_path}")
        reference_path = local_path
        log(f"Known-good reference lokal: {reference_path.name}")
    else:
        try:
            download(reference_url, cache_path)
            log("Known-good OpenClash reference diperbarui")
        except Exception as exc:
            if not cache_path.exists():
                raise RuntimeError(
                    f"Gagal mengambil known-good reference: {exc}"
                ) from exc
            log(f"Reference download gagal; menggunakan cache {cache_path}")
        reference_path = cache_path

    reference = yaml.safe_load(reference_path.read_text(encoding="utf-8")) or {}
    if not isinstance(reference, dict):
        raise RuntimeError("Known-good reference YAML invalid")

    merged = copy.deepcopy(generated)

    for key in ("profile", "sniffer", "dns", "rule-providers", "rules"):
        if key in reference:
            merged[key] = copy.deepcopy(reference[key])

    # Deprecated in current Mihomo.
    merged.pop("global-client-fingerprint", None)

    # Never re-introduce providers/rules that are absent from the proven file.
    providers = merged.get("rule-providers")
    if isinstance(providers, dict):
        for name in (
            "tracker-domain",
            "security-tif-mini",
            "popup-ads",
            "hagezi-pro-mini",
            "awavenue-ads",
        ):
            providers.pop(name, None)

    if isinstance(merged.get("rules"), list):
        cleaned = []
        for raw in merged["rules"]:
            rule = str(raw).strip()
            if re.match(
                r"(?i)^GEOSITE\s*,\s*(tracker|category-ads-all)\s*,",
                rule,
            ):
                continue
            if re.match(
                r"(?i)^RULE-SET\s*,\s*"
                r"(tracker-domain|security-tif-mini|popup-ads|hagezi-pro-mini|awavenue-ads)"
                r"\s*,",
                rule,
            ):
                continue
            cleaned.append(rule)
        merged["rules"] = cleaned

    _yaml_store_config(path, merged)
    return True

def apply_network_hardening(path: Path) -> bool:
    """Reduce exposed management surface while preserving LAN proxy access."""
    import yaml

    if not path.exists():
        return False
    config = _yaml_load_config(path)

    changed = False

    controller = config.get("external-controller")
    if isinstance(controller, str) and controller.strip():
        port = controller.rsplit(":", 1)[-1].strip()
        if port.isdigit():
            hardened = f"127.0.0.1:{port}"
            if controller != hardened:
                config["external-controller"] = hardened
                changed = True

    if config.get("allow-lan") is True:
        allowed = [
            "127.0.0.0/8",
            "10.0.0.0/8",
            "172.16.0.0/12",
            "192.168.0.0/16",
        ]
        if config.get("lan-allowed-ips") != allowed:
            config["lan-allowed-ips"] = allowed
            changed = True

    sniffer = config.get("sniffer")
    if isinstance(sniffer, dict) and sniffer.get("enable") is True:
        sniff = sniffer.get("sniff")
        android_output_name = os.environ.get("OUTPUT_ANDROID_YAML", "openclash_android.yaml").strip() or "openclash_android.yaml"
        is_android = path.name == Path(android_output_name).name
        if isinstance(sniff, dict):
            if is_android:
                # Clash Meta for Android builds with older embedded cores may reject
                # the QUIC sniffer with: "no find the sniffer QUIC". Keep HTTP/TLS
                # sniffing for domain rules, but never inject QUIC into Android output.
                if "QUIC" in sniff:
                    sniff.pop("QUIC", None)
                    changed = True
            elif "QUIC" not in sniff:
                sniff["QUIC"] = {"ports": [443, 8443]}
                changed = True

    if changed:
        _yaml_store_config(path, config)
    return changed

def apply_responsiveness(path: Path) -> bool:
    """Tune Mihomo/OpenClash for lower router overhead and faster steady-state response."""
    import yaml

    if not path.exists():
        return False

    def perf_int(name: str, default: int, minimum: int, maximum: int) -> int:
        try:
            value = int(str(os.environ.get(name, default)).strip())
        except (TypeError, ValueError):
            value = default
        return max(minimum, min(maximum, value))

    def perf_bool(name: str, default: bool) -> bool:
        raw = str(os.environ.get(name, "")).strip().lower()
        if not raw:
            return default
        return raw in {"1", "true", "yes", "y", "on", "aktif"}
    config = _yaml_load_config(path)

    android_output_name = os.environ.get("OUTPUT_ANDROID_YAML", "openclash_android.yaml").strip() or "openclash_android.yaml"
    is_android = path.name == Path(android_output_name).name

    before = copy.deepcopy(config)

    config["unified-delay"] = True
    config["tcp-concurrent"] = True
    config["find-process-mode"] = "off"
    config["disable-keep-alive"] = False
    config["keep-alive-interval"] = perf_int("KEEP_ALIVE_INTERVAL", 15, 5, 120)
    config["keep-alive-idle"] = perf_int("KEEP_ALIVE_IDLE", 30, 15, 3600)

    dns = config.get("dns")
    if isinstance(dns, dict) and dns.get("enable") is not False:
        dns["cache-algorithm"] = "arc"
        dns["prefer-h3"] = False
        dns["respect-rules"] = True
        dns["default-nameserver"] = [
            "https://1.1.1.1/dns-query",
            "https://9.9.9.9/dns-query",
        ]
        dns["use-hosts"] = True
        dns["use-system-hosts"] = False
        # Keep the primary family-safe resolver, but provide an independent
        # family-safe backup so ordinary DNS resolution does not become a
        # single point of failure. Blocking rules remain unchanged.
        dns["fallback"] = [
            "https://family.cloudflare-dns.com/dns-query",
            "tls://family.cloudflare-dns.com:853",
            "https://dns.quad9.net/dns-query",
            "tls://dns.quad9.net:853",
        ]
        # Mihomo races fallback resolvers and keeps fastest healthy result.
        dns["fallback-lazy-query"] = False
        dns["proxy-server-nameserver"] = [
            "https://1.1.1.1/dns-query",
            "https://dns.google/dns-query",
            "https://dns.quad9.net/dns-query",
            "https://9.9.9.9/dns-query",
            "https://94.140.14.14/dns-query",
        ]
        fake_filter = dns.setdefault("fake-ip-filter", [])
        if isinstance(fake_filter, list):
            for item in (
                "+.stun.*.*", "+.stun.*.*.*", "+.stun.*.*.*.*",
                "+.stun.*.*.*.*.*", "*.n.n.srv.nintendo.net",
                "xbox.*.*.microsoft.com", "*.*.xboxlive.com",
            ):
                if item not in fake_filter:
                    fake_filter.append(item)

    # Repair the social premium provider when the generated rules reference it.
    rules_now = [str(item) for item in config.get("rules", []) or []]
    if any(rule.startswith("RULE-SET,social-premium,") for rule in rules_now):
        providers = config.setdefault("rule-providers", {})
        if isinstance(providers, dict):
            providers.setdefault("social-premium", {
                "type": "file",
                "behavior": "classical",
                "path": "./rule_providers/social-premium.yaml",
            })

    # IP rules do not need a DNS lookup to decide private/LAN destinations.
    private_prefixes = (
        "IP-CIDR,127.0.0.0/8,DIRECT",
        "IP-CIDR,10.0.0.0/8,DIRECT",
        "IP-CIDR,172.16.0.0/12,DIRECT",
        "IP-CIDR,192.168.0.0/16,DIRECT",
        "IP-CIDR,169.254.0.0/16,DIRECT",
    )
    tuned_rules = []
    for item in config.get("rules", []) or []:
        rule = str(item)
        if rule in private_prefixes:
            rule += ",no-resolve"
        tuned_rules.append(rule)
    if tuned_rules:
        config["rules"] = tuned_rules

    groups = config.get("proxy-groups")
    if isinstance(groups, list):
        group_names = {str(g.get("name")) for g in groups if isinstance(g, dict) and g.get("name")}
        compact = {
            "GLOBAL": (["WARM-UP", "AUTO-FAST", "ANDROID-COLD-BACKUP"] if is_android else ["LOAD-BALANCE", "WARM-UP", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"]),
            "PROXY": (["GLOBAL", "WARM-UP", "AUTO-FAST", "FALLBACK"] if is_android else ["GLOBAL", "LOAD-BALANCE", "WARM-UP", "AUTO-FAST", "FALLBACK"]),
            "SOCIAL-MEDIA": ["WARM-UP", "AUTO-FAST", "FALLBACK"],
            "YOUTUBE": ["WARM-UP-CF", "STREAMING-FAST", "AUTO-FAST", "FALLBACK"],
            "EDUKASI": ["WARM-UP", "AUTO-FAST", "FALLBACK"],
            "STREAMING": ["STREAMING-FAST", "WARM-UP-CF", "AUTO-FAST", "FALLBACK"],
            "CLEAN": ["WARM-UP", "AUTO-FAST", "FALLBACK"],
        }
        for g in groups:
            if not isinstance(g, dict):
                continue
            name = str(g.get("name") or "")
            gtype = str(g.get("type") or "").lower()
            if name in compact:
                refs = [x for x in compact[name] if x in group_names and x != name]
                if refs:
                    g["proxies"] = refs
                if gtype == "fallback":
                    if is_android and name == "GLOBAL":
                        g["interval"] = perf_int("ANDROID_GLOBAL_FALLBACK_INTERVAL", 180, 60, 900)
                        g["lazy"] = perf_bool("ANDROID_GLOBAL_FALLBACK_LAZY", True)
                        g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
                        g["max-failed-times"] = perf_int("GENERIC_MAX_FAILED_TIMES", 3, 2, 6)
                    else:
                        g["interval"] = perf_int("GLOBAL_HEALTH_INTERVAL", 300, 60, 1200) if name == "GLOBAL" else perf_int("GENERIC_FALLBACK_INTERVAL", 300, 60, 1200)
                        g["lazy"] = True
                        g["timeout"] = perf_int("GENERIC_HEALTH_TIMEOUT_MS", 5000, 2500, 15000)
                        g["max-failed-times"] = perf_int("GENERIC_MAX_FAILED_TIMES", 3, 2, 6)
            elif name in {"AI", "AI-OPENAI", "AI-CLAUDE", "AI-GEMINI", "AI-OTHER", "AI-STABLE", "AI-BACKUP", "AI-MANUAL"}:
                ai_urls = {
                    "AI-OPENAI": os.environ.get("AI_OPENAI_TEST_URL", os.environ.get("AI_TEST_URL", "https://chatgpt.com/favicon.ico")),
                    "AI-CLAUDE": os.environ.get("AI_CLAUDE_TEST_URL", "https://claude.ai/favicon.ico"),
                    "AI-GEMINI": os.environ.get("AI_GEMINI_TEST_URL", "https://gemini.google.com/favicon.ico"),
                    "AI-OTHER": os.environ.get("AI_OTHER_TEST_URL", "https://www.gstatic.com/generate_204"),
                    "AI-STABLE": os.environ.get("AI_OTHER_TEST_URL", "https://www.gstatic.com/generate_204"),
                    "AI-BACKUP": os.environ.get("AI_OTHER_TEST_URL", "https://www.gstatic.com/generate_204"),
                    "AI-MANUAL": os.environ.get("AI_OTHER_TEST_URL", "https://www.gstatic.com/generate_204"),
                    "AI": os.environ.get("AI_OTHER_TEST_URL", "https://www.gstatic.com/generate_204"),
                }
                g["url"] = str(ai_urls.get(name) or "https://www.gstatic.com/generate_204").strip()
                base_ai_interval = max(60, min(int(os.environ.get("AI_HEALTH_INTERVAL", "300") or 300), 1800))
                g["interval"] = max(base_ai_interval, 600) if name == "AI-MANUAL" else base_ai_interval
                g["lazy"] = True
                g["timeout"] = max(2000, min(int(os.environ.get("AI_HEALTH_TIMEOUT_MS", "5000") or 5000), 15000))
                g["max-failed-times"] = perf_int("GENERIC_MAX_FAILED_TIMES", 3, 2, 6)
            elif name == "WARM-UP":
                if isinstance(g.get("proxies"), list):
                    g["proxies"] = g["proxies"][:perf_int("WARMUP_NODE_LIMIT", 4, 2, 12)]
                g["interval"] = perf_int("WARMUP_INTERVAL", 60, 10, 300)
                g["lazy"] = perf_bool("WARMUP_LAZY", False)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
                g["tolerance"] = max(int(g.get("tolerance") or 0), 150)
            elif name == "WARM-UP-CF":
                if isinstance(g.get("proxies"), list):
                    g["proxies"] = g["proxies"][:perf_int("CF_WARMUP_NODE_LIMIT", 4, 2, 12)]
                g["interval"] = perf_int("CF_WARMUP_INTERVAL", 120, 10, 600)
                g["lazy"] = perf_bool("CF_WARMUP_LAZY", True)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
                g["tolerance"] = max(int(g.get("tolerance") or 0), 150)
            elif name == "AUTO-FAST":
                if isinstance(g.get("proxies"), list):
                    g["proxies"] = g["proxies"][:perf_int("FAST_NODE_LIMIT", 8, 4, 30)]
                g["interval"] = perf_int("WAKEUP_INTERVAL", 90, 20, 300)
                g["lazy"] = perf_bool("ANDROID_AUTO_FAST_LAZY", True) if is_android else perf_bool("AUTO_FAST_LAZY", False)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
                g["tolerance"] = max(int(g.get("tolerance") or 0), 150)
            elif name == "STREAMING-FAST":
                if isinstance(g.get("proxies"), list):
                    g["proxies"] = g["proxies"][:perf_int("STREAMING_NODE_LIMIT", 6, 3, 16)]
                g["interval"] = perf_int("WAKEUP_INTERVAL", 90, 20, 300)
                g["lazy"] = perf_bool("STREAMING_HEALTH_LAZY", True)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
                g["tolerance"] = max(int(g.get("tolerance") or 0), 150)
            elif is_android and (name.startswith("ANDROID-BACKUP-H") or name == "ANDROID-COLD-BACKUP"):
                g["interval"] = perf_int("ANDROID_FALLBACK_INTERVAL", 300, 60, 1800)
                g["lazy"] = perf_bool("ANDROID_FALLBACK_LAZY", True)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
                g["max-failed-times"] = perf_int("GENERIC_MAX_FAILED_TIMES", 3, 2, 6)
            elif name == "PING-CHECK":
                g["interval"] = perf_int("PING_CHECK_INTERVAL", 300, 45, 1200)
                g["lazy"] = perf_bool("PING_CHECK_LAZY", True)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
            elif name == "FALLBACK":
                g["interval"] = perf_int("FALLBACK_INTERVAL", 180, 30, 900)
                g["lazy"] = perf_bool("FALLBACK_LAZY", True)
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)
            elif name == "LOAD-BALANCE":
                if isinstance(g.get("proxies"), list):
                    g["proxies"] = g["proxies"][:perf_int("LOAD_BALANCE_NODE_LIMIT", 4, 2, 8)]
                strategy = str(os.environ.get("LOAD_BALANCE_STRATEGY", "sticky-sessions")).strip().lower()
                g["strategy"] = strategy if strategy in {"consistent-hashing", "round-robin", "sticky-sessions"} else "sticky-sessions"
                g["interval"] = perf_int("BALANCE_INTERVAL", 300, 60, 1200)
                g["lazy"] = perf_bool("LOAD_BALANCE_LAZY", True)
            elif name == "MANUAL" and gtype in {"fallback", "url-test"}:
                g["interval"] = 300
                g["lazy"] = True
                g["timeout"] = max(int(g.get("timeout") or 5000), 5000)

    if config != before:
        _yaml_store_config(path, config)
        return True
    return False

def apply_security(path: Path, profile: str, workdir: Path, interval: int, dns_mode: str) -> bool:
    """Apply ad, tracker, and threat protection with per-client provider compatibility."""
    import yaml

    if not path.exists():
        return False
    config = _yaml_load_config(path)

    changed = False
    android_output_name = os.environ.get("OUTPUT_ANDROID_YAML", "openclash_android.yaml").strip() or "openclash_android.yaml"
    is_android = path.name == Path(android_output_name).name
    lite_output_name = os.environ.get("OUTPUT_LITE_YAML", "openclash_lite.yaml").strip() or "openclash_lite.yaml"
    is_lite = path.name == Path(lite_output_name).name
    dedup_mode = os.environ.get("ADBLOCK_DEDUP_MODE", "lean").strip().lower()
    lean_router = (not is_android) and dedup_mode in {"lean", "optimized", "v3"}
    indonesia_ads_enabled = os.environ.get("INDONESIA_ADBLOCK", "true").strip().lower() not in {"0", "false", "no", "off"}
    threat_ip_enabled = os.environ.get("THREAT_IP_BLOCKING", "true").strip().lower() not in {"0", "false", "no", "off"}
    router_adblock_level = os.environ.get("OPENWRT_ADBLOCK_LEVEL", "enhanced").strip().lower()
    lite_adblock_level = os.environ.get("OPENWRT_LITE_ADBLOCK_LEVEL", "standard").strip().lower()
    if router_adblock_level not in {"standard", "compact", "enhanced"}:
        router_adblock_level = "enhanced"
    if lite_adblock_level not in {"standard", "compact", "enhanced"}:
        lite_adblock_level = "compact"
    selected_router_adblock_level = lite_adblock_level if is_lite else router_adblock_level
    gambling_block = os.environ.get("OPENWRT_GAMBLING_BLOCK", "true").strip().lower() not in {"0", "false", "no", "off"}
    lite_gambling_block = os.environ.get("OPENWRT_LITE_GAMBLING_BLOCK", "true").strip().lower() not in {"0", "false", "no", "off"}
    selected_gambling_block = False if is_android else (lite_gambling_block if is_lite else gambling_block)
    android_snapshot = workdir / "rule_providers" / "ads_indonesia_android.yaml"
    provider_catalog = shared_provider_catalog(
        platform="android" if is_android else "router",
        profile=profile,
        lite=is_lite,
        indonesia_ads=indonesia_ads_enabled,
        threat_ip=threat_ip_enabled,
        interval=interval,
        android_snapshot_exists=android_snapshot.exists(),
        router_adblock_level=selected_router_adblock_level,
        gambling_block=selected_gambling_block,
    )

    # Lean router mode deliberately skips overlapping strict provider layers.
    if lean_router:
        provider_catalog.pop("hagezi-pro-mini", None)
        if selected_router_adblock_level == "standard":
            provider_catalog.pop("popup-ads", None)

    turtlecute_domains = (
        load_turtlecute_domains(workdir)
        if profile in {"child-safe", "app-safe", "threat-safe"} and not lean_router
        else []
    )
    if profile in {"child-safe", "app-safe", "threat-safe"} and turtlecute_domains and not is_android and not lean_router:
        provider_catalog["turtlecute-coverage"] = {
            "type": "inline",
            "behavior": "domain",
            "payload": turtlecute_domains,
        }
    if profile in {"child-safe", "app-safe", "threat-safe"} and not is_android and not lean_router:
        provider_catalog["streaming-ad-safe"] = {
            "type": "inline",
            "behavior": "domain",
            "payload": list(STREAMING_SAFE_AD_DOMAINS),
        }
    if profile in {"app-safe", "threat-safe"} and not is_android:
        app_payload = list(APP_SAFE_EXACT_DOMAINS) + [f".{domain}" for domain in APP_SAFE_SUFFIXES]
        provider_catalog["app-ad-safe"] = {
            "type": "inline",
            "behavior": "domain",
            "payload": app_payload,
        }

    providers = config.setdefault("rule-providers", {})
    if not isinstance(providers, dict):
        providers = {}
        config["rule-providers"] = providers
        changed = True

    # Remove providers from old/other platform profiles so Android never keeps
    # an MRS/text provider by accident, while router profiles keep their lean MRS set.
    obsolete = {
        "security-tif-mini", "popup-ads", "hagezi-pro-mini", "hagezi-pro-plus-mini", "gambling-mini", "awavenue-ads",
        "privacy-extra", "threat-tif-mini", "threat-malware", "threat-phishing", "threat-cryptominers",
        "turtlecute-coverage", "streaming-ad-safe", "app-ad-safe",
        "threat-fake-scam", "threat-tif-ip", "ads_indonesia",
    }
    obsolete -= set(provider_catalog)
    for name in obsolete:
        if name in providers:
            providers.pop(name, None)
            changed = True

    if profile != "off":
        for name, base_provider in provider_catalog.items():
            provider = dict(base_provider)
            if provider.get("type") == "http":
                provider["interval"] = interval
            if providers.get(name) != provider:
                providers[name] = provider
                changed = True
    elif is_android:
        # Even with blocking disabled, an Android profile must not retain stale
        # MRS/text security providers because some CMFA cores reject them while
        # parsing the whole configuration.
        for name in managed_provider_names():
            if name in providers:
                providers.pop(name, None)
                changed = True

    if is_android:
        # Last-resort compatibility guard for custom/legacy providers. Unknown
        # MRS providers are removed instead of leaving an Android-import failure.
        for name, provider in list(providers.items()):
            if not isinstance(provider, dict):
                continue
            fmt = str(provider.get("format") or "").lower()
            path_value = str(provider.get("path") or "").lower()
            url_value = str(provider.get("url") or "").lower()
            if (
                fmt == "mrs"
                or path_value.endswith(".mrs")
                or url_value.endswith(".mrs")
                or name == "chatgpt_voice"
            ):
                # Android compatibility profile is YAML-only. Voice routing is
                # still covered by the static OpenAI IP guards generated in v2.
                providers.pop(name, None)
                changed = True

    current_rules = [str(item) for item in config.get("rules", []) or []]
    managed_prefixes = (
        "RULE-SET,security-tif-mini,",
        "RULE-SET,popup-ads,",
        "RULE-SET,hagezi-pro-mini,",
        "RULE-SET,hagezi-pro-plus-mini,",
        "RULE-SET,gambling-mini,",
        "RULE-SET,privacy-extra,",
        "RULE-SET,tracker-domain,",
        "RULE-SET,threat-tif-mini,",
        "RULE-SET,threat-malware,",
        "RULE-SET,threat-phishing,",
        "RULE-SET,threat-cryptominers,",
        "RULE-SET,hagezi-pro-mini,",
        "RULE-SET,awavenue-ads,",
        "RULE-SET,turtlecute-coverage,",
        "RULE-SET,streaming-ad-safe,",
        "RULE-SET,app-ad-safe,",
        "RULE-SET,threat-fake-scam,",
        "RULE-SET,threat-tif-ip,",
        "RULE-SET,ads_indonesia,",
        "RULE-SET,ads_domain,",
        "RULE-SET,anti-ad,",
        "GEOSITE,category-ads-all,",
        "GEOSITE,tracker,",
    )
    intrusive_managed_rules = {f"DOMAIN-SUFFIX,{domain},REJECT" for domain in INTRUSIVE_AD_SUFFIXES}
    app_managed_rules = ({f"DOMAIN,{domain},REJECT" for domain in APP_SAFE_EXACT_DOMAINS} | {f"DOMAIN-SUFFIX,{domain},REJECT" for domain in APP_SAFE_SUFFIXES})
    v380_managed_rules = set(V380_AD_RULES + V380_SERVICE_RULES)
    china_cctv_managed_rules = set(CHINA_CCTV_AD_RULES)
    from ai_adblock_classifier import load_domains as load_ai_candidate_domains
    ai_adblock_managed_rules = {
        f"DOMAIN,{domain},REJECT"
        for candidate_path in (
            workdir / "adblock_ai_candidates.txt",
            workdir / ".runtime_cache" / "ai_adblock_candidates.txt",
        )
        for domain in load_ai_candidate_domains(candidate_path)
    }
    cleaned = [
        rule for rule in current_rules
        if not rule.startswith(managed_prefixes)
        and rule not in OVERBROAD_AD_KEYWORD_RULES
        and rule not in intrusive_managed_rules
        and rule not in app_managed_rules
        and rule not in v380_managed_rules
        and rule not in china_cctv_managed_rules
        and rule not in ai_adblock_managed_rules
    ]

    # Android uses rule mode so blocklists are evaluated.  Unmatched traffic still
    # goes to GLOBAL, preserving the previous global-routing behavior.
    if is_android:
        if config.get("mode") != "rule":
            config["mode"] = "rule"
            changed = True
        cleaned = [rule for rule in cleaned if not rule.startswith(("MATCH,", "FINAL,"))]

    # Keep local/private traffic and explicit user allowlist ahead of all blocklists.
    lan_rules = [rule for rule in cleaned if rule in LAN_DIRECT_RULES]
    cleaned = [rule for rule in cleaned if rule not in LAN_DIRECT_RULES]
    if is_android:
        # The lightweight Android generator originally had no rules at all. Add
        # standard private/LAN bypasses when converting it to rule mode.
        lan_rules = list(LAN_DIRECT_RULES)

    # Preserve AI routes ahead of broad ad/tracker/threat providers. Prefer the
    # service-specific v2 routes already produced by sumberyaml_core/reference
    # profile, and remove legacy rules that sent every AI service to one alias.
    ai_policy_names = {"AI", "AI-OPENAI", "AI-CLAUDE", "AI-GEMINI", "AI-OTHER", "AI-STABLE", "AI-BACKUP", "AI-MANUAL"}
    ai_provider_names = {"openai_domain", "ai_category", "chatgpt_voice"}

    def _rule_policy(rule: str) -> str:
        parts = [part.strip() for part in str(rule).split(",")]
        if len(parts) < 3:
            return ""
        return parts[-2] if parts[-1].lower() == "no-resolve" and len(parts) >= 4 else parts[-1]

    def _is_managed_ai_rule(rule: str) -> bool:
        parts = [part.strip() for part in str(rule).split(",")]
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET" and parts[1] in ai_provider_names:
            return True
        return _rule_policy(rule) in ai_policy_names

    existing_ai_rules = [rule for rule in cleaned if _is_managed_ai_rule(rule)]
    cleaned = [rule for rule in cleaned if not _is_managed_ai_rule(rule)]

    group_names = {
        str(group.get("name") or "")
        for group in (config.get("proxy-groups") or [])
        if isinstance(group, dict)
    }
    service_groups = {"AI-OPENAI", "AI-CLAUDE", "AI-GEMINI", "AI-OTHER"}
    has_v2_groups = service_groups.issubset(group_names)
    has_v2_rules = any(_rule_policy(rule) in service_groups for rule in existing_ai_rules)

    if has_v2_rules:
        # Drop old direct-to-`AI` rules while preserving service rules. Dynamic
        # provider rules are retained only when the provider survived the
        # platform compatibility pass (Android intentionally removes them).
        available_ai_providers = set((config.get("rule-providers") or {}).keys())
        ai_guard_rules = []
        for rule in existing_ai_rules:
            if _rule_policy(rule) == "AI":
                continue
            parts = [part.strip() for part in str(rule).split(",")]
            if len(parts) >= 3 and parts[0].upper() == "RULE-SET" and parts[1] not in available_ai_providers:
                continue
            ai_guard_rules.append(rule)
    elif has_v2_groups:
        try:
            from sumberyaml_core import _ai_proxy_rules as _core_ai_proxy_rules
            ai_guard_rules = list(_core_ai_proxy_rules())
        except Exception:
            # Compatibility fallback for a partially upgraded installation.
            ai_guard_rules = ai_proxy_rules("AI")
        provider_names = set((config.get("rule-providers") or {}).keys())
        if "openai_domain" in provider_names:
            ai_guard_rules.append("RULE-SET,openai_domain,AI-OPENAI")
        if "ai_category" in provider_names:
            ai_guard_rules.append("RULE-SET,ai_category,AI-OTHER")
        if "chatgpt_voice" in provider_names:
            ai_guard_rules.append("RULE-SET,chatgpt_voice,AI-OPENAI,no-resolve")
    else:
        ai_guard_rules = existing_ai_rules

    # Preserve YouTube guard order so compatibility exceptions and playback hosts
    # stay ahead of broad ad/tracker providers.
    youtube_ad_rules = [rule for rule in cleaned if rule in YOUTUBE_NETWORK_AD_RULES]
    playback_domains = set(YOUTUBE_PLAYBACK_DOMAINS)
    compat_domains = set(YOUTUBE_COMPAT_DOMAINS)
    youtube_compat_rules = []
    youtube_guard_rules = []
    remaining_rules = []
    for rule in cleaned:
        if rule in YOUTUBE_NETWORK_AD_RULES:
            continue
        parts = [part.strip() for part in rule.split(",")]
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET" and parts[1] == "youtube_domain":
            youtube_guard_rules.append(rule)
            continue
        if len(parts) >= 3 and parts[0].upper() in {"DOMAIN", "DOMAIN-SUFFIX"}:
            domain = parts[1].lower()
            if parts[0].upper() == "DOMAIN" and domain in compat_domains:
                youtube_compat_rules.append(rule)
                continue
            if domain in playback_domains:
                youtube_guard_rules.append(rule)
                continue
        remaining_rules.append(rule)
    cleaned = remaining_rules

    allowlist = set(load_allowlist(workdir))
    allow_rules = [f"DOMAIN-SUFFIX,{domain},DIRECT" for domain in sorted(allowlist)]
    ai_adblock_rules = [f"DOMAIN,{domain},REJECT" for domain in load_ai_adblock_domains(workdir, allowlist)]
    banking_rules: list[str] = []
    if is_android and android_banking_enabled():
        # Banking Safe Mode is deliberately conservative: DIRECT routing, real
        # DNS, no Fake-IP, and no TLS/HTTP destination sniff override.
        banking_rules = list(dict.fromkeys(android_banking_guard_rules()))
        managed_banking_rules = set(banking_rules)
        cleaned = [rule for rule in cleaned if rule not in managed_banking_rules]

        dns_cfg = config.get("dns") if isinstance(config.get("dns"), dict) else {}
        fake_filter = list(dns_cfg.get("fake-ip-filter") or [])
        dns_cfg["fake-ip-filter"] = list(dict.fromkeys(fake_filter + android_banking_fake_ip_filters()))
        normal_dns = ["https://1.1.1.1/dns-query", "https://dns.google/dns-query"]
        ns_policy = dns_cfg.setdefault("nameserver-policy", {})
        if isinstance(ns_policy, dict):
            for domain in android_banking_dns_policy_domains():
                ns_policy[f"+.{domain}"] = list(normal_dns)
        sniff_cfg = config.get("sniffer") if isinstance(config.get("sniffer"), dict) else {}
        skip_domain = list(sniff_cfg.get("skip-domain") or [])
        sniff_cfg["skip-domain"] = list(dict.fromkeys(skip_domain + android_banking_sniffer_skip_domains()))

    marketplace_rules: list[str] = []
    if is_android and android_marketplace_live_enabled():
        # Remove any copy generated by the core first, then insert the guard at
        # the precise boundary below: after high-confidence threat feeds but
        # before privacy/ad/tracker rules.
        marketplace_rules = list(dict.fromkeys(android_marketplace_live_guard_rules(android_marketplace_live_policy())))
        managed_marketplace_rules = set(marketplace_rules)
        cleaned = [rule for rule in cleaned if rule not in managed_marketplace_rules]

        dns_cfg = config.get("dns") if isinstance(config.get("dns"), dict) else {}
        fake_filter = list(dns_cfg.get("fake-ip-filter") or [])
        dns_cfg["fake-ip-filter"] = list(dict.fromkeys(fake_filter + android_marketplace_live_fake_ip_filters()))
        normal_dns = ["https://1.1.1.1/dns-query", "https://dns.google/dns-query"]
        ns_policy = dns_cfg.setdefault("nameserver-policy", {})
        if isinstance(ns_policy, dict):
            for domain in android_marketplace_live_dns_policy_domains():
                ns_policy[f"+.{domain}"] = list(normal_dns)
        sniff_cfg = config.get("sniffer") if isinstance(config.get("sniffer"), dict) else {}
        skip_domain = list(sniff_cfg.get("skip-domain") or [])
        sniff_cfg["skip-domain"] = list(dict.fromkeys(skip_domain + android_marketplace_live_sniffer_skip_domains()))

    security_rules = (
        lan_rules
        + ai_guard_rules
        + list(V380_AD_RULES)
        + list(V380_SERVICE_RULES)
        + list(CHINA_CCTV_AD_RULES)
        + list(allow_rules)
        + ai_adblock_rules
        + youtube_compat_rules
        + youtube_ad_rules
        + youtube_guard_rules
    )
    if profile != "off":
        provider_rules = shared_provider_reject_rules(
            platform="android" if is_android else "router",
            profile=profile,
            lite=is_lite,
            indonesia_ads="ads_indonesia" in provider_catalog,
            threat_ip="threat-tif-ip" in provider_catalog,
            android_snapshot_exists="ads_indonesia" in provider_catalog,
            router_adblock_level=selected_router_adblock_level,
            gambling_block=selected_gambling_block,
        )
        if lean_router:
            blocked_lean_prefixes = ["RULE-SET,hagezi-pro-mini,"]
            if selected_router_adblock_level == "standard":
                blocked_lean_prefixes.append("RULE-SET,popup-ads,")
            provider_rules = [
                rule for rule in provider_rules
                if not rule.startswith(tuple(blocked_lean_prefixes))
            ]

        # Keep high-confidence threat/privacy providers before local ad rules, then
        # regional/global ad providers last. This preserves the same ordering on
        # every generation path while still allowing platform-specific inline rules.
        ad_start = len(provider_rules)
        for idx, rule in enumerate(provider_rules):
            if rule.startswith(("RULE-SET,ads_indonesia,", "RULE-SET,ads_domain,", "RULE-SET,anti-ad,", "RULE-SET,tracker-domain,")):
                ad_start = idx
                break
        provider_before_ads = provider_rules[:ad_start]
        if is_android and marketplace_rules:
            critical_prefixes = (
                "RULE-SET,threat-malware,",
                "RULE-SET,threat-phishing,",
                "RULE-SET,threat-cryptominers,",
            )
            critical_rules = [rule for rule in provider_before_ads if rule.startswith(critical_prefixes)]
            noncritical_rules = [rule for rule in provider_before_ads if not rule.startswith(critical_prefixes)]
            security_rules.extend(critical_rules)
            security_rules.extend(banking_rules)
            security_rules.extend(marketplace_rules)
            security_rules.extend(noncritical_rules)
        elif is_android and banking_rules:
            critical_prefixes = (
                "RULE-SET,threat-malware,",
                "RULE-SET,threat-phishing,",
                "RULE-SET,threat-cryptominers,",
            )
            critical_rules = [rule for rule in provider_before_ads if rule.startswith(critical_prefixes)]
            noncritical_rules = [rule for rule in provider_before_ads if not rule.startswith(critical_prefixes)]
            security_rules.extend(critical_rules)
            security_rules.extend(banking_rules)
            security_rules.extend(noncritical_rules)
        else:
            security_rules.extend(provider_before_ads)

        if is_android:
            if profile in {"child-safe", "app-safe", "threat-safe"} and turtlecute_domains:
                security_rules.extend(f"DOMAIN,{domain},REJECT" for domain in turtlecute_domains)
            if profile in {"child-safe", "app-safe", "threat-safe"}:
                security_rules.extend(f"DOMAIN,{domain},REJECT" for domain in STREAMING_SAFE_AD_DOMAINS)
                security_rules.extend(f"DOMAIN-SUFFIX,{domain},REJECT" for domain in INTRUSIVE_AD_SUFFIXES)
            if profile in {"app-safe", "threat-safe"}:
                security_rules.extend(f"DOMAIN,{domain},REJECT" for domain in APP_SAFE_EXACT_DOMAINS)
                security_rules.extend(f"DOMAIN-SUFFIX,{domain},REJECT" for domain in APP_SAFE_SUFFIXES)
        else:
            if profile in {"child-safe", "app-safe", "threat-safe"} and turtlecute_domains and not lean_router:
                security_rules.append("RULE-SET,turtlecute-coverage,REJECT")
            if profile in {"child-safe", "app-safe", "threat-safe"}:
                if lean_router:
                    security_rules.extend(f"DOMAIN,{domain},REJECT" for domain in STREAMING_SAFE_AD_DOMAINS)
                else:
                    security_rules.append("RULE-SET,streaming-ad-safe,REJECT")
                security_rules.extend(f"DOMAIN-SUFFIX,{domain},REJECT" for domain in INTRUSIVE_AD_SUFFIXES)
            if profile in {"app-safe", "threat-safe"}:
                security_rules.append("RULE-SET,app-ad-safe,REJECT")

        security_rules.extend(provider_rules[ad_start:])
    elif is_android:
        security_rules.extend(banking_rules)
        security_rules.extend(marketplace_rules)

    # Preserve fixed-account Reddit/X routing even when a pinned reference
    # profile replaces generated rules before this final optimization pass.
    reddit_rules = [
        "DOMAIN-SUFFIX,reddit.com,REDDIT",
        "DOMAIN-SUFFIX,redditmedia.com,REDDIT",
        "DOMAIN-SUFFIX,redd.it,REDDIT",
        "DOMAIN,old.reddit.com,REDDIT",
        "DOMAIN-KEYWORD,reddit,REDDIT",
        "DOMAIN-SUFFIX,twitter.com,REDDIT",
        "DOMAIN-SUFFIX,x.com,REDDIT",
        "DOMAIN-SUFFIX,api.twitter.com,REDDIT",
        "DOMAIN-SUFFIX,api.x.com,REDDIT",
        "DOMAIN-SUFFIX,t.co,REDDIT",
    ]
    reddit_rule_set = set(reddit_rules)
    cleaned = [rule for rule in cleaned if rule not in reddit_rule_set]
    valid_policies = _valid_policies(config)
    routed_reddit_rules = reddit_rules if "REDDIT" in valid_policies else []

    new_rules = security_rules + routed_reddit_rules + cleaned
    if is_android:
        new_rules.append("MATCH,GLOBAL")

    # AI routing must remain ahead of broad threat/ad/tracker providers.
    # apply_security() historically prepended security rules, which could undo
    # the AI guard after every account refresh. Keep LAN/private first, then AI,
    # then the security/category rules.
    ai_policy_names = {"AI", "AI-OPENAI", "AI-CLAUDE", "AI-GEMINI", "AI-OTHER", "AI-STABLE", "AI-BACKUP", "AI-MANUAL"}
    ai_provider_prefixes = (
        "RULE-SET,openai_domain,",
        "RULE-SET,ai_category,",
        "RULE-SET,chatgpt_voice,",
    )

    def _is_lan_direct_rule(rule: str) -> bool:
        text = str(rule)
        return (
            text.startswith("DOMAIN-SUFFIX,local,DIRECT")
            or text.startswith("DOMAIN-SUFFIX,lan,DIRECT")
            or text.startswith("DOMAIN-SUFFIX,localhost,DIRECT")
            or text.startswith("IP-CIDR,127.0.0.0/8,DIRECT")
            or text.startswith("IP-CIDR,10.0.0.0/8,DIRECT")
            or text.startswith("IP-CIDR,172.16.0.0/12,DIRECT")
            or text.startswith("IP-CIDR,192.168.0.0/16,DIRECT")
            or text.startswith("IP-CIDR,169.254.0.0/16,DIRECT")
            or text.startswith("GEOIP,LAN,DIRECT")
        )

    def _is_ai_rule(rule: str) -> bool:
        text = str(rule)
        if text.startswith(ai_provider_prefixes):
            return True
        parts = [part.strip() for part in text.split(",")]
        if len(parts) < 3:
            return False
        policy_index = -2 if parts[-1] == "no-resolve" and len(parts) >= 4 else -1
        return parts[policy_index] in ai_policy_names

    lan_rules = [r for r in new_rules if _is_lan_direct_rule(r)]
    ai_rules = [r for r in new_rules if _is_ai_rule(r)]
    remaining_rules = [r for r in new_rules if not _is_lan_direct_rule(r) and not _is_ai_rule(r)]
    new_rules = lan_rules + ai_rules + remaining_rules

    # Deduplicate while preserving order.
    new_rules = list(dict.fromkeys(new_rules))
    if new_rules != current_rules:
        config["rules"] = new_rules
        changed = True

    # DNS-level blocking remains opt-in. Rule-based blocking is safer for
    # YouTube because video and ad traffic may share delivery infrastructure.
    dns = config.get("dns")
    if isinstance(dns, dict):
        policy = dns.get("nameserver-policy")
        if isinstance(policy, dict):
            for stale in ("geosite:category-ads-all,tracker", "geosite:tracker"):
                if stale in policy:
                    policy.pop(stale, None)
                    changed = True
            if dns_mode == "off" or profile == "off":
                if "geosite:category-ads-all" in policy:
                    policy.pop("geosite:category-ads-all", None)
                    changed = True
            elif dns_mode == "geosite":
                if policy.get("geosite:category-ads-all") != "rcode://success":
                    policy["geosite:category-ads-all"] = "rcode://success"
                    changed = True

        family_dns_enabled = profile == "child-safe" or (
            profile == "threat-safe"
            and str(os.environ.get("THREAT_SAFE_FAMILY_DNS", "true")).strip().lower() in {"1", "true", "yes", "y", "on", "aktif"}
        )
        if family_dns_enabled:
            family_dns = list(CHILD_SAFE_DNS)
            if dns.get("nameserver") != family_dns:
                dns["nameserver"] = family_dns
                changed = True
            # Keep fallback under the same category policy so blocked categories
            # cannot bypass the primary resolver.
            if "fallback" in dns and dns.get("fallback") != family_dns:
                dns["fallback"] = family_dns
                changed = True

    if changed:
        _yaml_store_config(path, config)
    return changed

def apply_youtube_guard(path: Path, mode: str) -> bool:
    """Protect YouTube playback and add conservative ad endpoint rules."""
    import yaml

    if not path.exists():
        return False
    config = _yaml_load_config(path)

    current = [str(item) for item in config.get("rules", []) or []]
    playback_domains = set(YOUTUBE_PLAYBACK_DOMAINS)
    compat_domains = set(YOUTUBE_COMPAT_DOMAINS)
    is_android_output = path.name.lower() == "openclash_android.yaml"
    managed_ad_rules = set(YOUTUBE_NETWORK_AD_RULES)
    if not is_android_output:
        managed_ad_rules.update(YOUTUBE_ROUTER_EXTRA_AD_RULES)

    cleaned = []
    for rule in current:
        parts = [part.strip() for part in rule.split(",")]
        # Remove managed guards/rules from previous runs so ordering stays deterministic.
        if len(parts) >= 3 and parts[0].upper() in {"DOMAIN", "DOMAIN-SUFFIX"}:
            domain = parts[1].lower()
            if domain in playback_domains:
                continue
            if parts[0].upper() == "DOMAIN" and domain in compat_domains:
                continue
        if rule in managed_ad_rules:
            continue
        if len(parts) >= 3 and parts[0].upper() == "RULE-SET" and parts[1] == "youtube_domain":
            continue
        # Remove the old over-broad YouTube-era doubleclick suffix reject.
        if rule == "DOMAIN-SUFFIX,doubleclick.net,REJECT":
            continue
        cleaned.append(rule)

    if mode == "off":
        new_rules = cleaned
    else:
        # Use a dedicated streaming route. Full profiles already have YOUTUBE,
        # while Lite/Android outputs may omit it to stay compact. Add a small
        # select group there so playback no longer gets shadowed by GLOBAL.
        structure_changed = False
        valid_policies = _valid_policies(config)
        if "YOUTUBE" not in valid_policies:
            groups = config.get("proxy-groups")
            if isinstance(groups, list):
                group_names = {
                    str(group.get("name") or "")
                    for group in groups
                    if isinstance(group, dict) and group.get("name")
                }
                candidates = [
                    name for name in ("STREAMING-FAST", "WARM-UP-CF", "WARM-UP", "AUTO-FAST", "FALLBACK", "GLOBAL")
                    if name in group_names
                ]
                if candidates:
                    groups.append({"name": "YOUTUBE", "type": "fallback", "proxies": candidates})
                    valid_policies.add("YOUTUBE")
                    structure_changed = True

        # Normalize the dedicated group for automatic failover and lower probe
        # overhead. 120 s is fast enough for streaming recovery without the
        # 60 s probe churn used by the older profile.
        groups = config.get("proxy-groups")
        if isinstance(groups, list) and "YOUTUBE" in valid_policies:
            for group in groups:
                if not isinstance(group, dict) or group.get("name") != "YOUTUBE":
                    continue
                desired = {
                    "type": "fallback",
                    "url": os.environ.get("YOUTUBE_TEST_URL", "https://www.gstatic.com/generate_204").strip() or "https://www.gstatic.com/generate_204",
                    "interval": max(60, min(int(os.environ.get("YOUTUBE_HEALTH_INTERVAL", "120") or 120), 1800)),
                    "lazy": True,
                    "timeout": max(1500, min(int(os.environ.get("YOUTUBE_HEALTH_TIMEOUT_MS", "3000") or 3000), 10000)),
                    "expected-status": "200/204/301/302",
                    "max-failed-times": 2,
                }
                for key, value in desired.items():
                    if group.get(key) != value:
                        group[key] = value
                        structure_changed = True
                break

        route = "YOUTUBE" if "YOUTUBE" in valid_policies else _default_route(config)
        compat_guard = [f"DOMAIN,{domain},{route}" for domain in YOUTUBE_COMPAT_DOMAINS]
        guard = []
        providers = config.setdefault("rule-providers", {})
        if isinstance(providers, dict):
            # Lite already supports MRS through its AI providers, so add the
            # compact YouTube MRS there too. Android's compatibility profile
            # intentionally has no MRS provider and remains on explicit guards.
            supports_mrs = any(
                isinstance(provider, dict) and str(provider.get("format") or "").lower() == "mrs"
                for provider in providers.values()
            )
            if route == "YOUTUBE" and "youtube_domain" not in providers and supports_mrs:
                providers["youtube_domain"] = {
                    "type": "http",
                    "behavior": "domain",
                    "format": "mrs",
                    "path": "./rule_providers/youtube.mrs",
                    "url": "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.mrs",
                    "interval": 43200,
                }
                structure_changed = True
            if "youtube_domain" in providers:
                guard.append(f"RULE-SET,youtube_domain,{route}")
        guard.extend(f"DOMAIN-SUFFIX,{domain},{route}" for domain in YOUTUBE_PLAYBACK_DOMAINS)
        ad_rules = list(YOUTUBE_NETWORK_AD_RULES) if mode == "enhanced" else []
        router_extra_enabled = str(os.environ.get("YOUTUBE_ROUTER_EXTRA_ADS", "true")).strip().lower() in {"1", "true", "yes", "y", "on", "aktif"}
        if mode == "enhanced" and router_extra_enabled and not is_android_output:
            ad_rules.extend(YOUTUBE_ROUTER_EXTRA_AD_RULES)

        # Keep LAN/user DIRECT exceptions and all AI routing guards ahead of
        # YouTube/ad rules. Otherwise this post-processing step could move a
        # REJECT rule in front of AI after every refresh.
        insert_at = 0
        ai_policies = {"AI", "AI-OPENAI", "AI-CLAUDE", "AI-GEMINI", "AI-OTHER", "AI-STABLE", "AI-BACKUP", "AI-MANUAL"}
        ai_providers = {"openai_domain", "ai_category", "chatgpt_voice"}
        for index, rule in enumerate(cleaned):
            parts = [part.strip() for part in rule.split(",")]
            policy = ""
            if len(parts) >= 3:
                policy = parts[-2] if parts[-1].lower() == "no-resolve" and len(parts) >= 4 else parts[-1]
            is_ai_provider = len(parts) >= 3 and parts[0].upper() == "RULE-SET" and parts[1] in ai_providers
            if policy.upper() == "DIRECT" or policy in ai_policies or is_ai_provider:
                insert_at = index + 1
                continue
            break

        # Exact compatibility exceptions first, then separable ad endpoints,
        # then primary playback guards before broad ad/tracker lists.
        new_rules = cleaned[:insert_at] + compat_guard + ad_rules + guard + cleaned[insert_at:]

    rules_changed = new_rules != current
    if rules_changed:
        config["rules"] = new_rules
    if rules_changed or (mode != "off" and locals().get("structure_changed", False)):
        _yaml_store_config(path, config)
        return True
    return False


def write_youtube_filters(workdir: Path, mode: str, filename: str) -> None:
    path = workdir / filename
    if mode == "off":
        path.unlink(missing_ok=True)
        return
    body = YOUTUBE_BROWSER_FILTERS_SAFE
    if mode == "enhanced":
        body += "\n" + YOUTUBE_BROWSER_FILTERS_ENHANCED
    body += """
! Keep the browser blocker's own filter lists enabled and updated.
! DNS/Mihomo alone cannot reliably distinguish every YouTube video ad from
! normal media when they share delivery infrastructure.
"""
    path.write_text(body, encoding="utf-8")


def optimize_outputs(
    workdir: Path,
    files: Iterable[str],
    profile: str,
    interval: int,
    dns_mode: str,
    youtube_mode: str,
    youtube_filter_file: str,
) -> None:
    """Single-pass post-processing for every generated YAML output.

    Each output is parsed once and serialized at most once. All existing
    hardening/adblock/YouTube transforms operate on the in-memory transaction.
    """
    reference_url = os.environ.get(
        "REFERENCE_PROFILE_URL",
        REFERENCE_PROFILE_URL,
    ).strip() or REFERENCE_PROFILE_URL

    compiled_mrs = load_compiled_report(workdir)
    compress_manual = str(os.environ.get("MANUAL_ROUTING_COMPRESS", "true")).strip().lower() not in {"0", "false", "no", "off"}
    try:
        manual_threshold = max(10, min(1000, int(str(os.environ.get("MANUAL_ROUTING_COMPRESS_THRESHOLD", "40")).strip())))
    except ValueError:
        manual_threshold = 40

    for filename in files:
        path = workdir / filename
        if not path.exists():
            continue

        with yaml_edit_transaction(path):
            sanitize_yaml(path)

            if filename == "openclash_auto.yaml":
                reference_mode = os.environ.get("REFERENCE_PROFILE_MODE", "local-pinned").strip().lower()
                if reference_mode not in {"off", "none", "generated"}:
                    apply_reference_profile(path, workdir, reference_url)
                    sanitize_yaml(path)
                    log(f"Reference profile diterapkan ({reference_mode}): {filename}")

            if apply_network_hardening(path):
                log(f"Network hardening diterapkan: {filename}")
            if apply_responsiveness(path):
                log(f"Responsiveness tuning diterapkan: {filename}")
            if apply_security(path, profile, workdir, interval, dns_mode):
                log(f"Ad/tracker provider diterapkan ({profile}, Android-YAML jika perlu): {filename}")
            if apply_youtube_guard(path, youtube_mode):
                log(f"YouTube guard diterapkan ({youtube_mode}): {filename}")

            config = _yaml_load_config(path)
            is_android = filename == (os.environ.get("OUTPUT_ANDROID_YAML", "openclash_android.yaml").strip() or "openclash_android.yaml")
            if compiled_mrs and not is_android:
                switched = apply_compiled_mrs(config, workdir, compiled_mrs)
                if switched:
                    _yaml_store_config(path, config)
                    log(f"MRS LKG lokal diterapkan: {filename} ({switched} provider)")

            semantic_mode = str(os.environ.get("SEMANTIC_RULE_OPTIMIZE", "router")).strip().lower()
            if semantic_mode not in {"off", "false", "0", "no"} and (semantic_mode == "all" or not is_android):
                removed_semantic = remove_safe_shadowed_domains(config)
                if removed_semantic:
                    _yaml_store_config(path, config)
                    log(f"Semantic rule dedup: {filename} (-{removed_semantic} shadowed DOMAIN)")

            if compress_manual and filename == "openclash_auto.yaml":
                result = compress_manual_routing(config, workdir, threshold=manual_threshold)
                if result.get("changed"):
                    _yaml_store_config(path, config)
                    log(
                        f"MANUAL routing dikompresi: {result.get('count')} inline rules -> "
                        f"RULE-SET,{result.get('provider')},MANUAL"
                    )

            sanitize_yaml(path)

        stats = yaml_transaction_stats(path)
        log(f"Single-pass YAML {filename}: loads={stats.get('loads', 0)}, writes={stats.get('writes', 0)}")

    # Browser filters handle cosmetic/path-level YouTube ads that a router
    # cannot reliably distinguish from normal video traffic by domain alone.
    write_youtube_filters(workdir, youtube_mode, youtube_filter_file)

def validate_yaml(workdir: Path, mihomo: Path, files: Iterable[str]) -> bool:
    ok = True
    strict = os.environ.get("REQUIRE_EXACT_MIHOMO_CORE", "true").strip().lower() not in {"0", "false", "no", "off"}
    try:
        version = assert_target_mihomo(mihomo, strict=strict)
        log(f"Validator core: {version}")
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        return False

    for filename in files:
        path = workdir / filename
        if not path.exists():
            continue
        log(f"Validasi target: {filename}")
        errors = validate_yaml_file(
            path,
            core_path=mihomo,
            require_exact_core=strict,
            parser_test=True,
        )
        if errors:
            ok = False
            print(f"[ERROR] {filename}")
            for error in errors:
                print("  - " + error)
        else:
            print(f"[OK] {filename}")
    return ok

def network_test() -> int:
    print(f"AkunYaml Target Runner v{APP_VERSION}")
    print(f"Python : {sys.version.split()[0]}")
    print(f"OpenSSL: {ssl.OPENSSL_VERSION}")
    print(f"curl   : {shutil.which('curl') or 'tidak ada'}")
    try:
        release = request_json(f"{GITHUB_API}/repos/{MIHOMO_REPO}/releases/latest")
        print(f"GitHub : OK, API reachable (stable={release.get('tag_name')})")
        print(f"Target : OpenClash {OPENCLASH_TARGET_VERSION}, {MIHOMO_TARGET_LABEL}")
        return 0
    except Exception as exc:
        print(f"GitHub : GAGAL\n{exc}")
        return 1


def parse_args():
    parser = argparse.ArgumentParser(description=f"AkunYaml runner for OpenClash {OPENCLASH_TARGET_VERSION} + {MIHOMO_TARGET_LABEL}")
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path, default=Path("local_config.json"))
    parser.add_argument("--max-nodes", type=int, default=None, help="Override MAX_NODES dari local_config.json")
    parser.add_argument("--min-nodes", type=int, default=None, help="Override MIN_OUTPUT_NODES dari local_config.json")
    parser.add_argument("--candidate-min", type=int)
    parser.add_argument("--urltest-pool", type=int)
    parser.add_argument("--nekobox-pool", type=int)
    parser.add_argument("--refresh-core", action="store_true")
    parser.add_argument("--refresh-binaries", action="store_true")
    parser.add_argument("--no-nekobox", action="store_true")
    parser.add_argument("--no-ws-only", action="store_true")
    parser.add_argument("--no-install-deps", action="store_true")
    parser.add_argument("--network-test", action="store_true")
    parser.add_argument("--adblock-profile", choices=("off", "balanced", "strict", "child-safe", "app-safe", "threat-safe"))
    parser.add_argument("--dns-adblock", choices=("off", "geosite"))
    parser.add_argument("--youtube-mode", choices=("off", "safe", "enhanced"))
    parser.add_argument(
        "--mihomo-path",
        type=Path,
        help=f"Path Mihomo exact target {MIHOMO_TARGET_LABEL}; pada OpenClash biasanya {DEFAULT_ROUTER_CORE}",
    )
    parser.add_argument(
        "--allow-non-target-core",
        action="store_true",
        help="Mode pengembangan saja: izinkan core selain target. Hasil tidak dianggap exact-target validated.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.network_test:
        return network_test()

    workdir = args.workdir.expanduser().resolve()
    workdir.mkdir(parents=True, exist_ok=True)
    log(f"Folder kerja: {workdir}")

    preliminary = dict(DEFAULT_ENV)
    preliminary.update(load_config(args.config))

    def _config_int(name: str, fallback: int) -> int:
        raw = str(preliminary.get(name, fallback)).strip()
        try:
            value = int(raw)
        except ValueError:
            value = fallback
        return value

    # CLI hanya meng-override jika user benar-benar memberikan argumen.
    # Sebelumnya default argparse 20/10 selalu menimpa local_config.json 10/6.
    args.max_nodes = args.max_nodes if args.max_nodes is not None else _config_int("MAX_NODES", 20)
    args.min_nodes = args.min_nodes if args.min_nodes is not None else _config_int("MIN_OUTPUT_NODES", 10)
    args.min_nodes = min(args.min_nodes, args.max_nodes)
    if args.max_nodes < 1 or args.min_nodes < 1:
        raise SystemExit("max/min nodes minimal 1")

    log(f"Target output: max={args.max_nodes}, minimum={args.min_nodes}")

    ensure_core_files(workdir, args.refresh_core)
    patch_core_compatibility(workdir)
    ensure_input_files(workdir)

    if not args.no_install_deps:
        install_dependencies()
    try:
        mihomo = select_target_mihomo(args, workdir, preliminary)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}")
        return 2
    if args.no_nekobox:
        preliminary["REQUIRE_NEKOBOX_TEST"] = "false"
    # sing-box tetap diperlukan untuk validasi output Android meski URL test dimatikan.
    singbox = ensure_binary(workdir, SINGBOX_REPO, "sing-box", select_singbox_asset, args.refresh_binaries)

    env = build_environment(args, workdir, mihomo, singbox)

    # apply_security() and feed_guard run in this process, while generate_yaml.py
    # receives `env` as a subprocess environment. Mirror security settings here
    # so both generation paths evaluate the exact same policy.
    security_env_keys = (
        "ADBLOCK_PROFILE", "ADBLOCK_PROVIDER_INTERVAL", "INDONESIA_ADBLOCK",
        "THREAT_IP_BLOCKING", "SECURITY_FEED_GUARD", "REFRESH_SECURITY_FEEDS",
        "FEED_REFRESH_TTL_SEC", "FEED_MAX_DROP_RATIO", "FEED_MAX_GROWTH_RATIO", "ADBLOCK_DEDUP_MODE",
        "AI_ADBLOCK_ENABLED", "AI_ADBLOCK_BASE_URL", "AI_ADBLOCK_MODEL", "AI_ADBLOCK_API_KEY_FILE",
        "AI_ADBLOCK_BATCH_SIZE", "AI_ADBLOCK_MIN_CONFIDENCE", "AI_ADBLOCK_TIMEOUT_SEC",
        "MANUAL_ROUTING_COMPRESS", "MANUAL_ROUTING_COMPRESS_THRESHOLD", "MRS_COMPILE", "SEMANTIC_RULE_OPTIMIZE",
        "OPENWRT_ADBLOCK_LEVEL", "OPENWRT_LITE_ADBLOCK_LEVEL",
        "THREAT_SAFE_FAMILY_DNS",
        "BUG_SERVERS", "BUG_MODE", "BUG_HEALTH_CHECK", "BUG_HEALTH_ATTEMPTS", "BUG_MAX_VARIANTS_PER_NODE",
        "BUG_TOTAL_VARIANTS_CAP", "BUG_MIN_BASE_NODES",
        "ANDROID_MULTI_HOST_MODE", "ANDROID_FALLBACK_HOST_LIMIT", "ANDROID_FALLBACK_TOTAL_CAP",
        "ANDROID_FALLBACK_INTERVAL", "ANDROID_FALLBACK_LAZY",
        "ANDROID_GLOBAL_FALLBACK_INTERVAL", "ANDROID_GLOBAL_FALLBACK_LAZY", "ANDROID_AUTO_FAST_LAZY",
        "ANDROID_MARKETPLACE_LIVE_COMPAT", "ANDROID_MARKETPLACE_LIVE_POLICY",
        "ANDROID_MARKETPLACE_LIVE_DOMAINS", "ANDROID_MARKETPLACE_LIVE_EXACT_DOMAINS",
        "ANDROID_BANKING_SAFE_MODE", "ANDROID_BANKING_DOMAINS", "ANDROID_BANKING_EXACT_DOMAINS",
        "SUBSCRIPTION_CACHE", "SUBSCRIPTION_CACHE_TTL_SEC", "SUBSCRIPTION_CACHE_STALE_IF_ERROR",
        "SUBSCRIPTION_CACHE_DIR", "PROVIDER_CACHE", "PROVIDER_CACHE_TTL_SEC", "PROVIDER_CACHE_FILE",
        "ADAPTIVE_CANDIDATES", "CANDIDATE_INITIAL", "CANDIDATE_MAX",
        "WARMUP_NODE_LIMIT", "WARMUP_INTERVAL", "WARMUP_LAZY",
        "CF_WARMUP_NODE_LIMIT", "CF_WARMUP_INTERVAL", "CF_WARMUP_LAZY",
        "FAST_NODE_LIMIT", "WAKEUP_INTERVAL", "AUTO_FAST_LAZY",
        "STREAMING_NODE_LIMIT", "STREAMING_HEALTH_LAZY", "PING_CHECK_INTERVAL", "PING_CHECK_LAZY",
        "FALLBACK_INTERVAL", "FALLBACK_LAZY", "BALANCE_INTERVAL", "LOAD_BALANCE_LAZY",
        "LOAD_BALANCE_STRATEGY", "LOAD_BALANCE_NODE_LIMIT", "KEEP_ALIVE_INTERVAL", "KEEP_ALIVE_IDLE",
        "AI_SERVICE_NODE_LIMIT",
    )
    for key in security_env_keys:
        if key in env:
            os.environ[key] = str(env[key])

    if env.get("SECURITY_FEED_GUARD", "true").strip().lower() not in {"0", "false", "no", "off"}:
        try:
            from feed_guard import refresh_security_feeds
            refresh_security_feeds(
                workdir,
                refresh=env.get("REFRESH_SECURITY_FEEDS", "true").strip().lower() not in {"0", "false", "no", "off"},
                log=log,
            )
        except Exception as exc:
            # Feed preflight is intentionally non-fatal. Remote Mihomo providers
            # keep their normal cache/update behavior if the workstation is offline.
            log(f"Security feed guard dilewati: {exc}")

    if env.get("AI_ADBLOCK_ENABLED", "false").strip().lower() not in {"0", "false", "no", "off"}:
        from ai_adblock_classifier import classify_candidates, refresh_streaming_candidates

        key_file = Path(env.get("AI_ADBLOCK_API_KEY_FILE", ".secrets/ai_adblock.key")).expanduser()
        if not key_file.is_absolute():
            key_file = workdir / key_file
        try:
            refresh_streaming_candidates(workdir, log=log)
            ai_result = classify_candidates(
                workdir,
                base_url=env.get("AI_ADBLOCK_BASE_URL", "https://ai.tamandata.com/v1"),
                model=env.get("AI_ADBLOCK_MODEL", "tamandata"),
                key_file=key_file,
                batch_size=max(1, min(100, int(env.get("AI_ADBLOCK_BATCH_SIZE", "25")))),
                min_confidence=max(0.95, min(1.0, float(env.get("AI_ADBLOCK_MIN_CONFIDENCE", "0.98")))),
                timeout=max(5.0, min(120.0, float(env.get("AI_ADBLOCK_TIMEOUT_SEC", "30")))),
                log=log,
            )
            log(f"AI adblock: {ai_result['status']} ({ai_result.get('count', 0)} kandidat)")
        except Exception as exc:
            log(f"AI adblock fail-open: {type(exc).__name__}: {exc}")

    log("Menjalankan generate_yaml.py")
    result = subprocess.run([sys.executable, "generate_yaml.py"], cwd=workdir, env=env, check=False)
    if result.returncode != 0:
        print(f"[ERROR] Pipeline generator gagal, exit={result.returncode}")
        return result.returncode

    output_files = (
        env.get("OUTPUT_YAML", OUTPUT_YAMLS[0]),
        env.get("OUTPUT_ANDROID_YAML", OUTPUT_YAMLS[1]),
        env.get("OUTPUT_LITE_YAML", OUTPUT_YAMLS[2]),
        env.get("OUTPUT_FRESH_YAML", OUTPUT_YAMLS[3]),
    )

    profile = (args.adblock_profile or env.get("ADBLOCK_PROFILE", "off")).strip().lower()
    if profile not in {"off", "balanced", "strict", "child-safe", "app-safe", "threat-safe"}:
        profile = "off"

    dns_mode = (args.dns_adblock or env.get("ADBLOCK_DNS_MODE", "off")).strip().lower()
    if dns_mode not in {"off", "geosite"}:
        dns_mode = "off"

    youtube_mode = (args.youtube_mode or env.get("YOUTUBE_ADBLOCK_MODE", "enhanced")).strip().lower()
    if youtube_mode not in {"off", "safe", "enhanced"}:
        youtube_mode = "enhanced"

    try:
        interval = max(3600, int(env.get("ADBLOCK_PROVIDER_INTERVAL", "43200")))
    except ValueError:
        interval = 43200

    youtube_filter_file = env.get("YOUTUBE_BROWSER_FILTER_FILE", "youtube_browser_filters.txt").strip() or "youtube_browser_filters.txt"

    os.environ["REFERENCE_PROFILE_MODE"] = env.get(
        "REFERENCE_PROFILE_MODE",
        "local-pinned",
    )
    os.environ["REFERENCE_PROFILE_FILE"] = env.get(
        "REFERENCE_PROFILE_FILE",
        "reference_profile_v047156.yaml",
    )
    os.environ["REFERENCE_PROFILE_URL"] = env.get(
        "REFERENCE_PROFILE_URL",
        REFERENCE_PROFILE_URL,
    )

    optimize_outputs(
        workdir,
        output_files,
        profile,
        interval,
        dns_mode,
        youtube_mode,
        youtube_filter_file,
    )

    if not validate_yaml(workdir, mihomo, output_files):
        print("\n[ERROR] Ada YAML yang gagal validasi.")
        print("Gunakan error tepat di atas untuk diagnosis.")
        return 2

    print("\n[OK] Semua output yang tersedia lolos validasi Mihomo.")
    for name in (
        *output_files,
        env.get("OUTPUT_SINGBOX_ANDROID", "singbox_android.json"),
        env.get("OUTPUT_AKUN", "akun.txt"),
        env.get("OUTPUT_CSV", "openclash_auto_report.csv"),
        env.get("OUTPUT_OPENCLASH_COMPAT_REPORT", "openclash_compat_report.csv"),
        youtube_filter_file,
    ):
        output_path = workdir / name
        if output_path.exists():
            print(f"  - {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
