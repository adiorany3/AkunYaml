"""Export OpenClash subscription profiles with downloadable local providers."""
import copy
import hashlib
import json
import shutil
from pathlib import Path

import yaml

RAW_BASE = "https://raw.githubusercontent.com/adiorany3/AkunYaml/main/output/"


def manual_gameblock(config, accounts):
    """HerYaml layout: DIRECT first, optional real accounts, MATCH to MANUAL."""
    result = copy.deepcopy(config)
    names = [item.get("name") for item in accounts]
    if not names or any(not isinstance(name, str) or not name or name in {"DIRECT", "REJECT", "MANUAL"} for name in names) or len(set(names)) != len(names):
        raise ValueError("Akun MANUAL kosong, duplikat, atau memakai nama reserved")
    rules = result.get("rules", [])
    if not rules or rules[-1] != "MATCH,DIRECT":
        raise ValueError("Baseline gameblock harus berakhir MATCH,DIRECT")
    result["proxies"] = copy.deepcopy(accounts)
    result["proxy-groups"] = [{"name": "MANUAL", "type": "select", "proxies": ["DIRECT", *names]}]
    rules[-1] = "MATCH,MANUAL"
    # Avoid restoring an old proxy selection after an updated profile import.
    result.setdefault("profile", {})["store-selected"] = False
    return result


def gameblock_account_profile(config, game_config, game_folder, proxy_folder):
    """Clone an account profile and prepend refreshed game feeds before all routing exceptions."""
    result = copy.deepcopy(config)
    providers = result.setdefault("rule-providers", {})
    source_providers = game_config.get("rule-providers", {})
    for name in ("games-blackmatrix", "games-category", "game-block-online"):
        provider = source_providers.get(name)
        if not isinstance(provider, dict) or provider.get("type") != "file":
            raise ValueError(f"Provider gameblock hilang/tidak lokal: {name}")
        relative = Path(provider.get("path", ""))
        origin = (game_folder / relative).resolve()
        if relative.is_absolute() or ".." in relative.parts or not origin.is_relative_to(game_folder.resolve()) or not origin.is_file():
            raise FileNotFoundError(f"Provider gameblock tidak aman/hilang: {name}")
        if name in providers:
            raise ValueError(f"Nama provider gameblock bentrok: {name}")
        target_relative = Path("rule_providers/gameblock") / f"{name}{origin.suffix}"
        target = proxy_folder / target_relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origin, target)
        providers[name] = {**copy.deepcopy(provider), "path": "./" + target_relative.as_posix()}

    manual_rules = []
    for rule in game_config.get("rules", []):
        if rule == "RULE-SET,game-block-online,REJECT":
            break
        if rule.startswith("DOMAIN-SUFFIX,") and rule.endswith(",REJECT"):
            manual_rules.append(rule)
    game_rules = ["RULE-SET,games-blackmatrix,REJECT", "RULE-SET,games-category,REJECT", "RULE-SET,game-block-online,REJECT", *manual_rules]
    result["rules"] = game_rules + [rule for rule in result.get("rules", []) if rule not in game_rules]
    return result


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
    accounts = yaml.safe_load((stage / "openclash/proxy/openclash_auto.yaml").read_text()).get("proxies", [])
    if not accounts:
        raise ValueError("Tidak ada akun untuk proxy-provider OpenClash")
    gameblock = stage / "openclash/gameblock/openclash_noproxy_gameblock.yaml"
    config = manual_gameblock(yaml.safe_load(gameblock.read_text()), accounts)
    gameblock.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))

    proxy = stage / "openclash/proxy"
    game_config = yaml.safe_load(gameblock.read_text())
    account_config = yaml.safe_load((proxy / "openclash_auto.yaml").read_text())
    game_account = gameblock_account_profile(account_config, game_config, gameblock.parent, proxy)
    (proxy / "openclash_auto_gameblock.yaml").write_text(yaml.safe_dump(game_account, sort_keys=False, allow_unicode=True))

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
    (stage / "akun/openclash_proxy_provider.yaml").write_text(yaml.safe_dump({"proxies": accounts}, sort_keys=False, allow_unicode=True))
    (destination / "urls.json").write_text(json.dumps(profiles, indent=2) + "\n")
    return profiles