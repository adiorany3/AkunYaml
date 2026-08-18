#!/usr/bin/env python3
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import sumberyaml_core as core


class DummyResponse:
    def __init__(self, status_code: int, text: str = "", headers: dict | None = None, payload: dict | None = None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}
        self._payload = payload or {}
        self.ok = 200 <= status_code < 300

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self) -> dict:
        return self._payload


def make_node(index: int) -> core.ProxyNode:
    return core.ProxyNode(
        name=f"N{index}",
        type="vless",
        original_server=f"origin{index}.example",
        port=443,
        raw=f"vless://id{index}@origin{index}.example:443?security=tls&type=ws&host=sni{index}.example&sni=sni{index}.example#N{index}",
        clash={"name": f"N{index}", "type": "vless", "server": f"origin{index}.example", "port": 443, "network": "ws"},
        key=f"k{index}",
    )


def test_subscription_cache() -> None:
    old_get = core.requests.get
    with tempfile.TemporaryDirectory() as td:
        os.environ["SUBSCRIPTION_CACHE"] = "true"
        os.environ["SUBSCRIPTION_CACHE_DIR"] = td
        os.environ["SUBSCRIPTION_CACHE_TTL_SEC"] = "1800"
        calls: list[dict] = []

        def first_get(url, timeout=None, headers=None):
            calls.append(dict(headers or {}))
            return DummyResponse(200, "vless://abc@example.com:443#x", {"ETag": '"abc"', "Last-Modified": "Tue, 18 Aug 2026 10:00:00 GMT"})

        core.requests.get = first_get
        first = core.fetch_url_cached("https://example.test/sub", 1)
        second = core.fetch_url_cached("https://example.test/sub", 1)
        assert "cache-updated" in first[2]
        assert "cache-hit fresh" in second[2]
        assert len(calls) == 1

        os.environ["SUBSCRIPTION_CACHE_TTL_SEC"] = "0"

        def revalidate(url, timeout=None, headers=None):
            calls.append(dict(headers or {}))
            return DummyResponse(304)

        core.requests.get = revalidate
        third = core.fetch_url_cached("https://example.test/sub", 1)
        assert "cache-revalidated" in third[2]
        assert calls[-1].get("If-None-Match") == '"abc"'

        def offline(*args, **kwargs):
            raise RuntimeError("offline")

        core.requests.get = offline
        fourth = core.fetch_url_cached("https://example.test/sub", 1)
        assert "stale-cache fallback" in fourth[2]
    core.requests.get = old_get


def test_provider_cache() -> None:
    old_get = core.requests.get
    old_resolve = core._resolve_original_ip
    with tempfile.TemporaryDirectory() as td:
        cache_file = Path(td) / "provider.json"
        os.environ["PROVIDER_CACHE"] = "true"
        os.environ["PROVIDER_CACHE_FILE"] = str(cache_file)
        os.environ["PROVIDER_CACHE_TTL_SEC"] = "1209600"
        os.environ["PROVIDER_LOOKUP_WORKERS"] = "1"
        core._PROVIDER_CACHE.clear(); core._RDAP_CACHE.clear()
        core._PROVIDER_CACHE_SAVED_AT.clear(); core._RDAP_CACHE_SAVED_AT.clear()
        core._PROVIDER_CACHE_LOADED = False; core._PROVIDER_CACHE_DIRTY = False
        core._resolve_original_ip = lambda host: "203.0.113.10"
        calls = []
        core.requests.get = lambda *a, **k: (calls.append(1) or DummyResponse(200, payload={"name": "DIGITALOCEAN-TEST"}))
        first = make_node(1); first.best_delay_ms = 100
        core.unique_names([first])
        assert cache_file.is_file() and first.original_provider == "DIGITALOCEAN" and len(calls) == 1

        core._PROVIDER_CACHE.clear(); core._RDAP_CACHE.clear()
        core._PROVIDER_CACHE_SAVED_AT.clear(); core._RDAP_CACHE_SAVED_AT.clear()
        core._PROVIDER_CACHE_LOADED = False; core._PROVIDER_CACHE_DIRTY = False
        core.requests.get = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("network should not be used"))
        second = make_node(1); second.best_delay_ms = 100
        core.unique_names([second])
        assert second.original_provider == "DIGITALOCEAN"
    core.requests.get = old_get
    core._resolve_original_ip = old_resolve


def test_multi_host_budget() -> None:
    old = (core.TARGET_SERVERS, core.TARGET_SERVER, core.BUG_MODE, core.BUG_MAX_VARIANTS_PER_NODE, core.BUG_TOTAL_VARIANTS_CAP, core.BUG_MIN_BASE_NODES)
    try:
        core.TARGET_SERVERS = ("host1.example", "host2.example", "host3.example")
        core.TARGET_SERVER = "host1.example"
        core.BUG_MODE = "fallback"
        core.BUG_MAX_VARIANTS_PER_NODE = 3
        core.BUG_TOTAL_VARIANTS_CAP = 24
        core.BUG_MIN_BASE_NODES = 8
        assert len(core.expand_multi_host_variants([make_node(i) for i in range(10)])) == 24
        assert len(core.expand_multi_host_variants([make_node(i) for i in range(30)])) == 30
    finally:
        core.TARGET_SERVERS, core.TARGET_SERVER, core.BUG_MODE, core.BUG_MAX_VARIANTS_PER_NODE, core.BUG_TOTAL_VARIANTS_CAP, core.BUG_MIN_BASE_NODES = old


def main() -> int:
    test_subscription_cache()
    test_provider_cache()
    test_multi_host_budget()
    print("[OK] subscription cache + provider cache + multi-host budget selftest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
