"""Conservative exact-host blocking from fresh, cross-publisher evidence."""
import hashlib
import ipaddress
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta

from ai_adblock_classifier import is_allowlisted, load_domains
from build_support import fetch
from feed_guard import _parse_domains
from openclash_target import atomic_write_text

SOURCES = {
    "hagezi-threat": ("hagezi", "malware", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/tif.mini-onlydomains.txt"),
    "chocolate-threat": ("chocolate4u", "malware", "https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/release/malware.txt"),
    "hagezi-ads": ("hagezi", "adblock", "https://raw.githubusercontent.com/hagezi/dns-blocklists/main/wildcard/pro-onlydomains.txt"),
    "abpindo-ads": ("abpindo", "adblock", "https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/domain.txt"),
}
TTL_HOURS = 24


def protected_domains(root):
    allowed = set(load_domains(root / "adblock_allowlist.txt"))
    # Retain explicit service exceptions from the maintained local policy.
    baseline = root / "gameblock_policy/baseline/openclash_noproxy_gameblock.yaml"
    if baseline.exists():
        import yaml
        for rule in yaml.safe_load(baseline.read_text()).get("rules", []):
            parts = rule.split(",")
            if len(parts) == 3 and parts[0] in {"DOMAIN", "DOMAIN-SUFFIX"} and parts[2] == "DIRECT":
                allowed.add(parts[1])
    return allowed


def evaluate(evidence, allowlist):
    accepted, review = {}, 0
    for category in ("malware", "adblock"):
        support = {}
        for name, domains in evidence.items():
            publisher, kind, _ = SOURCES[name]
            if kind != category:
                continue
            for domain in domains:
                try:
                    ipaddress.ip_address(domain)
                    continue
                except ValueError:
                    pass
                if _parse_domains(domain) != [domain]:
                    continue
                support.setdefault(domain, set()).add(publisher)
        for domain, publishers in support.items():
            if is_allowlisted(domain, allowlist):
                continue
            if len(publishers) >= 2:
                accepted[domain] = {"category": category, "publishers": sorted(publishers)}
            else:
                review += 1
    return accepted, review


def refresh(root):
    def download(item):
        name, (_, _, url) = item
        raw = fetch(url)
        domains = set(_parse_domains(raw.decode("utf-8")))
        if len(domains) < 10:
            raise ValueError(f"Feed adaptive tidak valid: {name}")
        return name, domains, hashlib.sha256(raw).hexdigest()

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(download, SOURCES.items()))
    allowlist = protected_domains(root)
    accepted, review = evaluate({name: domains for name, domains, _ in results}, allowlist)
    now = datetime.now(UTC)
    report = {
        "generated_at": now.isoformat(), "expires_at": (now + timedelta(hours=TTL_HOURS)).isoformat(),
        "policy": "two-publishers-exact-host-v1", "accepted": accepted,
        "single_source_review_count": review,
        "sources": [{"name": name, "url": SOURCES[name][2], "entries": len(domains), "sha256": digest} for name, domains, digest in results],
        "limitations": "Publisher agreement is not independent ground truth; feeds may share upstream data. No malware execution, scanning, or AI-only blocking.",
    }
    cache = root / ".runtime_cache/adaptive_guard.json"
    cache.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(cache, json.dumps(report, indent=2) + "\n")
    return report


def snapshot(root, now=None):
    path = root / ".runtime_cache/adaptive_guard.json"
    if not path.exists():
        return {"status": "unavailable", "accepted": {}}
    report = json.loads(path.read_text())
    if report.get("policy") != "two-publishers-exact-host-v1":
        raise ValueError("Policy cache adaptive tidak dikenali")
    now = now or datetime.now(UTC)
    generated = datetime.fromisoformat(report["generated_at"])
    expires = datetime.fromisoformat(report["expires_at"])
    if generated.tzinfo is None or expires.tzinfo is None:
        raise ValueError("Timestamp cache harus timezone-aware")
    if generated > now or expires <= now or expires - generated > timedelta(hours=TTL_HOURS):
        return {"status": "expired", "accepted": {}}
    allowed = protected_domains(root)
    report["accepted"] = {d: v for d, v in report["accepted"].items() if _parse_domains(d) == [d] and len(set(v.get("publishers", []))) >= 2 and not is_allowlisted(d, allowed)}
    report["status"] = "fresh"
    return report


def apply(stage, root):
    report = snapshot(root)
    domains = sorted(report["accepted"])
    if domains:
        import yaml
        for folder in (stage / "openclash", stage / "mihomo-mac"):
            for path in folder.glob("*/*.yaml"):
                config = yaml.safe_load(path.read_text())
                config["rules"] = [f"DOMAIN,{domain},REJECT" for domain in domains] + config["rules"]
                path.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True))
        for path in (stage / "sing-box").glob("*.json"):
            config = json.loads(path.read_text())
            config["route"]["rules"].insert(0, {"domain": domains, "action": "reject"})
            path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n")
    destination = stage / "security"
    destination.mkdir()
    # Do not publish local browsing telemetry or candidate history.
    (destination / "adaptive_blocklist.txt").write_text("\n".join(domains) + ("\n" if domains else ""))
    (destination / "adaptive_report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report["status"]