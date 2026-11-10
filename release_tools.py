"""Credential-free change preview and explicit public artifact export."""
import argparse
import hashlib
import json
import shutil
import tempfile
from collections import Counter
from pathlib import Path

import yaml

from build_support import publish


def profiles(folder):
    paths = set(folder.glob("openclash/*/*.yaml")) | set(folder.glob("mihomo-mac/*/*.yaml")) | set(folder.glob("sing-box/*.json"))
    return {p.relative_to(folder).as_posix(): p for p in paths}


def preview(old, new):
    before, after = profiles(old), profiles(new)
    changes = []
    for name in sorted(before.keys() | after.keys()):
        left, right = before.get(name), after.get(name)
        if left is None or right is None:
            changes.append({"profile": name, "status": "added" if left is None else "removed"})
            continue
        if left.read_bytes() == right.read_bytes():
            continue
        parse = json.loads if name.endswith(".json") else yaml.safe_load
        a, b = parse(left.read_text()), parse(right.read_text())
        if not isinstance(a, dict) or not isinstance(b, dict):
            raise TypeError("Profil preview tidak valid")
        rules_a = a.get("rules", a.get("route", {}).get("rules", []))
        rules_b = b.get("rules", b.get("route", {}).get("rules", []))
        canonical = lambda values: Counter(json.dumps(value, sort_keys=True) for value in values)
        ca, cb = canonical(rules_a), canonical(rules_b)
        changes.append({"profile": name, "status": "changed", "rules_added": sum((cb - ca).values()),
                        "rules_removed": sum((ca - cb).values()), "rule_order_changed": ca == cb and rules_a != rules_b,
                        "dns_changed": a.get("dns") != b.get("dns"),
                        "accounts_changed": a.get("proxies", a.get("outbounds")) != b.get("proxies", b.get("outbounds")),
                        "groups_changed": a.get("proxy-groups") != b.get("proxy-groups"),
                        "providers_changed": a.get("rule-providers", a.get("route", {}).get("rule_set")) != b.get("rule-providers", b.get("route", {}).get("rule_set"))})
    # Only aggregate values are published: never raw nodes, rules, DNS URLs or diffs.
    return {"profiles_changed": len(changes), "changes": changes}


def public_export(source, target):
    source, target = source.resolve(), target.resolve()
    if source == target or source.is_relative_to(target) or target.is_relative_to(source):
        raise ValueError("Ekspor publik harus folder terpisah dari sumber")
    if target.exists():
        marker = target / "manifest.json"
        try:
            owned = json.loads(marker.read_text()).get("scope") == "public-blocklist-only"
        except (OSError, ValueError, AttributeError):
            owned = False
        if not owned or any(p.name not in {"manifest.json", "adaptive_blocklist.txt"} for p in target.iterdir()):
            raise ValueError("Menolak menimpa folder yang bukan ekspor publik terkelola")
    allowed = source / "security/adaptive_blocklist.txt"
    if not allowed.is_file() or allowed.is_symlink() or not allowed.resolve().is_relative_to(source):
        raise ValueError("Blocklist publik lokal tidak tersedia")
    from domain_policy_tools import domain

    entries = allowed.read_text().splitlines()
    for entry in entries:
        if domain(entry) != entry:
            raise ValueError("Blocklist mengandung entri non-domain")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as temporary:
        stage = Path(temporary) / "release"
        stage.mkdir(mode=0o700)
        shutil.copyfile(allowed, stage / "adaptive_blocklist.txt")
        metadata = {"scope": "public-blocklist-only", "entries": len(entries),
                    "sha256": hashlib.sha256(allowed.read_bytes()).hexdigest(),
                    "note": "Tidak berisi profil berakun, kredensial, manifest privat, atau log koneksi."}
        (stage / "manifest.json").write_text(json.dumps(metadata, indent=2) + "\n")
        for path in stage.iterdir():
            path.chmod(0o600)
        publish(stage, target)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    diff = commands.add_parser("preview")
    diff.add_argument("old", type=Path)
    diff.add_argument("new", type=Path)
    export = commands.add_parser("export-public")
    export.add_argument("source", type=Path)
    export.add_argument("target", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "preview":
            if not args.old.is_dir() or not args.new.is_dir():
                raise ValueError("Kedua folder profil harus tersedia")
            print(json.dumps(preview(args.old, args.new), indent=2))
        else:
            print(public_export(args.source, args.target))
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        parser.exit(2, f"[ERROR] {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
