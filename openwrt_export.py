"""Export OpenClash subscription profiles with downloadable local providers."""
import copy
import hashlib
import json
from pathlib import Path

import yaml

RAW_BASE = "https://raw.githubusercontent.com/adiorany3/AkunYaml/main/output/"


def subscription_profile(config, source_folder, stage):
    result = copy.deepcopy(config)
    # OpenClash's import/UI checks expect a selectable group even for direct-only
    # profiles. Keep the source genuinely proxy-free: DIRECT is a built-in route,
    # not a fabricated proxy account. Routing/blocking rules remain unchanged.
    if not result.get("proxies") and not result.get("proxy-providers"):
        result.setdefault("proxies", [])
        if not result.get("proxy-groups"):
            result["proxy-groups"] = [
                {"name": "DIRECT-ONLY", "type": "select", "proxies": ["DIRECT"]}
            ]
    for provider in result.get("rule-providers", {}).values():
        if provider.get("type") != "file":
            continue
        relative = Path(provider["path"])
        origin = (source_folder / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not origin.is_relative_to(source_folder.resolve()):
            raise ValueError("Path provider OpenWrt tidak aman")
        if not origin.is_file():
            raise FileNotFoundError(f"Provider OpenWrt hilang: {relative}")
        published = origin.relative_to(stage.resolve()).as_posix()
        # Distinct cache names prevent collisions between imported profiles.
        digest = hashlib.sha256(published.encode()).hexdigest()[:12]
        provider.update({"type": "http", "url": RAW_BASE + published,
                         "path": f"./rule_provider/akunyaml-{digest}{relative.suffix}",
                         "interval": 43200})
    return result


def export(stage):
    destination = stage / "openclash/subscription"
    destination.mkdir()
    profiles = []
    for source in sorted((stage / "openclash").glob("*/*.yaml")):
        if source.parent == destination:
            continue
        config = yaml.safe_load(source.read_text())
        result = subscription_profile(config, source.parent, stage)
        target = destination / source.name
        if target.exists():
            raise ValueError("Nama subscription duplikat")
        target.write_text(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
        profiles.append({"file": target.name, "url": RAW_BASE + "openclash/subscription/" + target.name})
    accounts = yaml.safe_load((stage / "openclash/proxy/openclash_auto.yaml").read_text()).get("proxies", [])
    if not accounts:
        raise ValueError("Tidak ada akun untuk proxy-provider OpenClash")
    (stage / "akun/openclash_proxy_provider.yaml").write_text(yaml.safe_dump({"proxies": accounts}, sort_keys=False, allow_unicode=True))
    (destination / "urls.json").write_text(json.dumps(profiles, indent=2) + "\n")
    return profiles