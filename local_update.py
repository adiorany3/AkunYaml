"""Build direct profiles locally, without Hermes or network access."""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path

import yaml

from openclash_target import atomic_write_text


def direct_clash(source: dict) -> dict:
    config = copy.deepcopy(source)
    for key in ("proxies", "proxy-providers", "proxy-groups", "listeners", "secret", "external-controller", "external-ui-url"):
        config.pop(key, None)
    config["mode"] = "rule"
    rules = []
    for rule in config.get("rules", []):
        parts = rule.split(",")
        index = -2 if parts[-1] == "no-resolve" else -1
        if parts[index] not in {"DIRECT", "REJECT", "REJECT-DROP", "PASS"}:
            parts[index] = "DIRECT"
        rules.append(",".join(parts))
    config["rules"] = rules
    used = {r.split(",")[1] for r in rules if r.startswith("RULE-SET,")}
    config["rule-providers"] = {k: v for k, v in config.get("rule-providers", {}).items() if k in used}
    for provider in config["rule-providers"].values():
        if "proxy" in provider:
            provider["proxy"] = "DIRECT"
    dns = config.get("dns", {})
    for key in ("nameserver", "fallback", "default-nameserver", "proxy-server-nameserver"):
        if key in dns:
            dns[key] = [server.split("#")[0] for server in dns[key]]
    return config


def direct_singbox(source: dict) -> dict:
    config = copy.deepcopy(source)
    config["outbounds"] = [{"type": "direct", "tag": "direct"}]
    config.pop("experimental", None)

    def rewrite(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"outbound", "detour", "download_detour"}:
                    value[key] = "direct"
                else:
                    rewrite(item)
        elif isinstance(value, list):
            for item in value:
                rewrite(item)

    rewrite(config)
    config.setdefault("route", {})["final"] = "direct"
    return config


def build(root: Path, output: Path) -> list[Path]:
    root, output = root.resolve(), output.resolve()
    if output == root or root.is_relative_to(output):
        raise ValueError("Output harus folder terpisah, bukan root proyek atau induknya")
    clash = yaml.safe_load((root / "openclash_auto.yaml").read_text())
    singbox = json.loads((root / "singbox_android.json").read_text())
    if not isinstance(clash, dict) or not clash.get("rules"):
        raise ValueError("Sumber Clash tidak memiliki aturan")
    if not isinstance(singbox, dict) or not singbox.get("route", {}).get("rules"):
        raise ValueError("Sumber Sing-box tidak memiliki aturan")
    clash, singbox = direct_clash(clash), direct_singbox(singbox)
    assets = []
    for provider in clash.get("rule-providers", {}).values():
        if provider.get("type") != "file":
            continue
        relative = Path(provider["path"])
        source = (root / relative).resolve()
        if relative.is_absolute() or not source.is_relative_to(root):
            raise ValueError("Path provider tidak aman")
        if not source.is_file():
            raise FileNotFoundError(f"Provider lokal tidak tersedia: {relative}")
        assets.append((source, relative))
    output.mkdir(parents=True, exist_ok=True)
    for source, relative in assets:
        target = output / relative
        if not target.resolve().is_relative_to(output):
            raise ValueError("Path output provider tidak aman")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    files = {
        "openclash_noproxy.yaml": yaml.safe_dump(clash, sort_keys=False, allow_unicode=True),
        "singbox_direct_adblock.json": json.dumps(singbox, indent=2, ensure_ascii=False) + "\n",
    }
    remote = [k for k, v in clash.get("rule-providers", {}).items() if v.get("type") == "http"]
    remote += [v["tag"] for v in singbox.get("route", {}).get("rule_set", []) if v.get("type") == "remote"]
    files["build_report.json"] = json.dumps({
        "mode": "local-snapshot", "proxy_accounts": 0,
        "remote_providers_at_runtime": remote,
        "note": "Build offline; provider remote membutuhkan internet saat runtime. Kesegaran aturan mengikuti sumber lokal.",
    }, indent=2) + "\n"
    for name, text in files.items():
        atomic_write_text(output / name, text)
    return [output / name for name in files]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=Path("local_build"))
    args = parser.parse_args()
    root = args.workdir.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    try:
        for path in build(root, output):
            print(f"[OK] {path}")
    except (OSError, ValueError, KeyError, yaml.YAMLError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())