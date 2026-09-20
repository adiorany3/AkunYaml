#!/usr/bin/env python3
"""Offline regression: refresh settings, probe budgets, account retention."""
import json
import os
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

import yaml

import local_runner as runner
from generate_yaml import _build_singbox_android_json, _validate_singbox_json

ROOT = Path(__file__).resolve().parent


def main():
    settings = {key: str(value) for key, value in json.loads((ROOT / "local_config.json").read_text()).items()}
    # Exercise nondefault values so missing parent-process propagation cannot pass.
    settings.update(GLOBAL_HEALTH_INTERVAL="420", GENERIC_FALLBACK_INTERVAL="480",
                    GENERIC_HEALTH_TIMEOUT_MS="6500", GENERIC_MAX_FAILED_TIMES="4",
                    AI_HEALTH_INTERVAL="360", AI_HEALTH_TIMEOUT_MS="7000",
                    AI_OPENAI_TEST_URL="https://example.com/health",
                    SECURITY_FEED_GUARD="false", AI_ADBLOCK_ENABLED="false")
    with TemporaryDirectory() as folder, ExitStack() as stack:
        root = Path(folder)
        path = root / "openclash_auto.yaml"
        names = ("GLOBAL", "CLEAN", "AI-OPENAI", "AUTO-FAST", "FALLBACK", "LOAD-BALANCE", "MANUAL", "REDDIT")
        config = {
            "proxies": [{"name": "MANUAL-test", "type": "trojan", "server": "example.com", "port": 443, "password": "test-only"}],
            "proxy-groups": [{"name": name, "type": "select" if name in {"MANUAL", "REDDIT"} else "load-balance" if name == "LOAD-BALANCE" else "url-test" if name == "AUTO-FAST" else "fallback",
                              "proxies": ["MANUAL"] if name == "REDDIT" else ["MANUAL-test"]} for name in names],
            "rules": ["DOMAIN,example.com,MANUAL", "MATCH,GLOBAL"],
        }
        path.write_text(yaml.safe_dump(config))
        args = SimpleNamespace(network_test=False, workdir=root, config=ROOT / "local_config.json",
                               max_nodes=None, min_nodes=None, refresh_core=False,
                               no_install_deps=True, no_nekobox=False, refresh_binaries=False)
        stack.enter_context(patch.dict(os.environ, {}, clear=True))
        stack.enter_context(patch.object(runner, "parse_args", return_value=args))
        for name in ("ensure_core_files", "patch_core_compatibility", "ensure_input_files", "log"):
            stack.enter_context(patch.object(runner, name))
        stack.enter_context(patch.object(runner, "select_target_mihomo", return_value=root / "mihomo"))
        stack.enter_context(patch.object(runner, "ensure_binary", return_value=root / "sing-box"))
        stack.enter_context(patch.object(runner, "build_environment", return_value=settings))

        class StopBeforeGeneration(Exception):
            pass

        def verify(*args, **kwargs):
            assert kwargs["env"] == settings
            assert runner.apply_responsiveness(path)
            tuned = yaml.safe_load(path.read_text())
            groups = {group["name"]: group for group in tuned["proxy-groups"]}
            assert groups["GLOBAL"]["interval"] == 420
            assert groups["GLOBAL"]["proxies"][0] == "LOAD-BALANCE"
            assert groups["CLEAN"]["interval"] == 480
            assert groups["CLEAN"]["timeout"] == 6500
            assert groups["CLEAN"]["max-failed-times"] == 4
            assert groups["AI-OPENAI"]["interval"] == 360
            assert groups["AI-OPENAI"]["timeout"] == 7000
            assert groups["AI-OPENAI"]["url"] == settings["AI_OPENAI_TEST_URL"]
            for name, interval in (("AUTO-FAST", 180), ("FALLBACK", 180), ("LOAD-BALANCE", 300)):
                assert groups[name]["interval"] == interval and groups[name]["lazy"]
            assert groups["REDDIT"]["proxies"] == ["MANUAL"]
            assert groups["MANUAL"]["proxies"] == ["MANUAL-test"]
            assert tuned["proxies"] == config["proxies"]
            assert tuned["rules"] == config["rules"]
            assert not runner.apply_responsiveness(path), "Optimizer must be idempotent"
            with patch.dict(os.environ, {"AI_HEALTH_INTERVAL": "invalid", "AI_HEALTH_TIMEOUT_MS": "invalid"}):
                runner.apply_responsiveness(path)
                ai = next(group for group in yaml.safe_load(path.read_text())["proxy-groups"] if group["name"] == "AI-OPENAI")
                assert ai["interval"] == 300 and ai["timeout"] == 5000
            raise StopBeforeGeneration

        stack.enter_context(patch.object(runner.subprocess, "run", side_effect=verify))
        try:
            runner.main()
        except StopBeforeGeneration:
            pass
        else:
            raise AssertionError("Refresh did not reach generator")

    nodes = [SimpleNamespace(name=name, tier="MANUAL", type="vmess", tcp_reachable=True,
                             url_test_success=success, url_test_status=status, url_test_ms=latency,
                             clash={"type": "vmess", "server": "example.com", "port": 443,
                                    "uuid": "00000000-0000-4000-8000-000000000001", "cipher": "auto"})
             for name, success, status, latency in (
                 ("slow", True, "HTTP 204", 200), ("failed", False, "HTTP 500", 1),
                 ("fast", True, "HTTP 204", 40), ("untested", True, "skipped-disabled", 0),
                 ("equal", True, "HTTP 200", 40),
             )]
    with patch.dict(os.environ, {"SINGBOX_URLTEST_NODE_LIMIT": "2"}):
        text = _build_singbox_android_json(nodes)
    result = json.loads(text)
    groups = {item["tag"]: item for item in result["outbounds"]}
    assert groups["AUTO-FAST"]["outbounds"] == ["fast", "equal"]
    assert groups["AUTO-FAST"]["interrupt_exist_connections"] is False
    assert set(groups["proxy"]["outbounds"][1:]) == {node.name for node in nodes}
    assert sum(item["type"] == "urltest" for item in result["outbounds"]) == 1
    _validate_singbox_json(text, str(ROOT / ".local_bin/sing-box"))
    print("PASS: refresh propagation, lazy probe intervals, idempotence, routing/account retention, ranked sing-box pool and core validation")


if __name__ == "__main__":
    main()
