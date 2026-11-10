"""Translate the direct gameblock policy, refusing unsupported semantics."""
import copy

from domain_policy_tools import FIELDS, provider_rules


def build(source, clash, folder, core):
    from local_update import direct_singbox

    config = direct_singbox(source)
    blocks = []
    groups = {}
    last_policy = None
    for raw in clash.get("rules", []):
        parts = raw.split(",")
        if parts == ["MATCH", "DIRECT"]:
            continue
        if len(parts) not in {3, 4} or parts[2] not in {"REJECT", "REJECT-DROP", "DIRECT"}:
            raise ValueError("Gameblock hanya mendukung DIRECT/REJECT")
        policy = "DIRECT" if parts[2] == "DIRECT" else "REJECT"
        if policy != last_policy:
            groups = {}
            blocks.append((policy, groups))
            last_policy = policy
        if len(parts) == 4 and parts[3] != "no-resolve":
            raise ValueError("Opsi rule tidak didukung")
        if parts[0] == "RULE-SET":
            rules = provider_rules(folder, clash["rule-providers"][parts[1]], core)
        else:
            rules = [(parts[0], parts[1])]
        for kind, value in rules:
            if kind not in FIELDS:
                raise ValueError("Jenis rule gameblock tidak didukung: " + kind)
            groups.setdefault(FIELDS[kind], set()).add(value)
    if not clash.get("rules") or clash["rules"][-1] != "MATCH,DIRECT":
        raise ValueError("Gameblock harus berakhir MATCH,DIRECT")
    if not blocks:
        raise ValueError("Gameblock kosong")
    # Aggregate only adjacent equal policies, preserving allowlist/deny precedence.
    blocked = []
    for policy, fields in blocks:
        for field, values in fields.items():
            action = {"action": "route", "outbound": "direct"} if policy == "DIRECT" else {"action": "reject"}
            blocked.append({field: sorted(values), **action})
    route = config.setdefault("route", {})
    previous = route.get("rules", [])
    technical = [copy.deepcopy(rule) for rule in previous if rule.get("action") in {"sniff", "hijack-dns"}]
    route["rules"] = technical + blocked
    route.pop("rule_set", None)
    for rule in config.get("dns", {}).get("rules", []):
        if "rule_set" in rule:
            raise ValueError("DNS memakai rule_set lama; terjemahan dihentikan")
    route["final"] = "direct"
    return config
