#!/usr/bin/env python3
"""Conservative offline AI classification for explicit adblock candidates."""
from __future__ import annotations

import argparse
import json
import os
import re
import socket
import ssl
import stat
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

MAX_API_RETRIES = 2
RETRY_DELAYS_SEC = (1, 2)
RETRYABLE_HTTP_STATUS = {429, 500, 502, 503, 504}


def _is_timeout(error: BaseException) -> bool:
    reason = getattr(error, "reason", error)
    return isinstance(error, (TimeoutError, socket.timeout)) or isinstance(reason, (TimeoutError, socket.timeout))


def _open_api(request: urllib.request.Request, timeout: float):
    for attempt in range(MAX_API_RETRIES + 1):
        try:
            return urllib.request.urlopen(request, timeout=timeout, context=ssl.create_default_context())
        except urllib.error.HTTPError as exc:
            error, retryable = exc, exc.code in RETRYABLE_HTTP_STATUS
        except urllib.error.URLError as exc:
            error, retryable = exc, _is_timeout(exc)
        except (TimeoutError, socket.timeout) as exc:
            error, retryable = exc, True
        if not retryable or attempt == MAX_API_RETRIES:
            raise error
        time.sleep(RETRY_DELAYS_SEC[attempt])


DOMAIN_RE = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)
ALLOWED_LABELS = {"allow", "block", "review"}
BLOCK_CATEGORIES = {"advertising", "tracking", "gambling", "predatory_lending", "scam"}
STREAMING_MARKERS = {
    "disneyplus", "freewheel", "fwmrm", "hulu", "netflix", "paramountplus",
    "peacocktv", "roku", "spotify", "twitch", "youtube",
}
TELEMETRY_MARKERS = {
    "ad", "ads", "advertising", "analytics", "beacon", "bloodhound", "crashdump",
    "event", "events", "log", "logs", "metric", "metrics", "pixel", "telemetry", "track", "tracker",
}
CANDIDATE_FEEDS = (
    ".feed_cache/last_good/hagezi-pro-plus-mini.txt",
    ".feed_cache/last_good/popup-ads.txt",
)
DISCOVERY_FEEDS = CANDIDATE_FEEDS + (
    ".feed_cache/last_good/ads_indonesia.txt",
    ".feed_cache/last_good/gambling-mini.txt",
    ".feed_cache/last_good/threat-fake-scam.txt",
)
DISCOVERY_MARKERS = {
    "bet", "casino", "gacor", "gambling", "judi", "judol", "loan", "lottery",
    "pinjaman", "pinjol", "poker", "scam", "slot", "sportsbook", "togel", "toto",
}
STRONG_DISCOVERY_MARKERS = {"judol", "pinjol", "togel", "gacor", "sportsbook", "casino", "gambling", "pinjaman"}
EXISTING_BLOCKLISTS = (
    "rule_providers/universal-adblock-safe.yaml",
    "rule_providers/ads_indonesia_android.yaml",
    ".feed_cache/last_good/gambling-mini.txt",
)


def normalize_domain(raw: str) -> str | None:
    value = raw.strip().lower().rstrip(".")
    if not value or value.startswith(("#", "!", ";")):
        return None
    value = re.sub(r"^https?://", "", value).split("/", 1)[0].split(":", 1)[0]
    if value.startswith(("*.", "+.")):
        value = value[2:]
    return value if DOMAIN_RE.fullmatch(value) and ".." not in value else None


def load_domains(path: Path) -> list[str]:
    if not path.exists():
        return []
    return sorted({domain for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines() if (domain := normalize_domain(raw))})


def _has_label(domain: str, markers: set[str]) -> bool:
    return bool(set(re.split(r"[.-]", domain)) & markers)


def _discovery_score(domain: str) -> int:
    labels = re.split(r"[.-]", domain)
    compact = "".join(labels)
    score = sum(label in STRONG_DISCOVERY_MARKERS for label in labels) * 3
    score += sum(label in DISCOVERY_MARKERS for label in labels)
    score += sum(2 for marker in STRONG_DISCOVERY_MARKERS if marker in compact)
    return score


def _has_streaming_marker(domain: str) -> bool:
    labels = re.split(r"[.-]", domain)
    return any(
        label == marker or label.startswith(marker) or label.endswith(marker)
        for label in labels
        for marker in STREAMING_MARKERS
    )


def is_allowlisted(domain: str, allowlist: set[str]) -> bool:
    return any(domain == allowed or domain.endswith("." + allowed) for allowed in allowlist)


def refresh_streaming_candidates(workdir: Path, *, log=print) -> list[str]:
    """Rebuild exact candidates from LKG feeds; AI decides final category."""
    allowlist = set(load_domains(workdir / "adblock_allowlist.txt"))
    existing = {
        domain for relative_path in EXISTING_BLOCKLISTS
        for domain in load_domains(workdir / relative_path)
    }
    discovered = {
        domain
        for relative_path in CANDIDATE_FEEDS
        for domain in load_domains(workdir / relative_path)
        if _has_streaming_marker(domain)
        and _has_label(domain, TELEMETRY_MARKERS)
    }
    discovered.update(
        domain
        for relative_path in DISCOVERY_FEEDS
        for domain in load_domains(workdir / relative_path)
        if _has_label(domain, DISCOVERY_MARKERS) or _discovery_score(domain) >= 2
    )
    discovered -= existing
    discovered = {domain for domain in discovered if not is_allowlisted(domain, allowlist)}
    output = workdir / ".runtime_cache" / "ai_adblock_candidates.txt"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        "# Generated from refreshed Last-Known-Good feeds; AI classification still required.\n"
        + "".join(f"{domain}\n" for domain in sorted(discovered)),
        encoding="utf-8",
    )
    temporary.replace(output)
    log(f"AI adblock candidates: {len(discovered)} host telemetri streaming terkini")
    return sorted(discovered)


def parse_response(content: str, expected: list[str]) -> list[dict[str, Any]]:
    data = json.loads(content)
    if not isinstance(data, dict) or set(data) != {"results"} or not isinstance(data["results"], list):
        raise ValueError("response harus object dengan satu field results")
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in data["results"]:
        if not isinstance(item, dict) or set(item) != {"domain", "label", "category", "confidence", "reason"}:
            raise ValueError("item response memiliki schema tidak valid")
        if any(not isinstance(item[key], str) for key in ("domain", "label", "category", "reason")):
            raise ValueError("domain, label, category, dan reason harus string")
        domain = normalize_domain(str(item["domain"]))
        label = str(item["label"]).lower()
        category = str(item["category"]).lower()
        confidence = item["confidence"]
        reason = str(item["reason"]).strip()
        if domain is None or domain in seen or label not in ALLOWED_LABELS:
            raise ValueError("domain atau label response tidak valid")
        if category not in BLOCK_CATEGORIES | {"service", "unknown"}:
            raise ValueError("category response tidak valid")
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= float(confidence) <= 1:
            raise ValueError("confidence response tidak valid")
        if not reason or len(reason) > 240:
            raise ValueError("reason response tidak valid")
        seen.add(domain)
        results.append({"domain": domain, "label": label, "category": category, "confidence": float(confidence), "reason": reason})
    if seen != set(expected) or len(results) != len(expected):
        raise ValueError("response harus memuat setiap domain input tepat sekali")
    return results


def _read_api_key(path: Path | None) -> str:
    key = os.environ.get("AI_ADBLOCK_API_KEY", "").strip()
    if key:
        return key
    if path is None or not path.exists():
        return ""
    if os.name == "posix" and stat.S_IMODE(path.stat().st_mode) & 0o077:
        raise PermissionError(f"permission file key harus 600: {path}")
    return path.read_text(encoding="utf-8").strip()


def _classify_batch(base_url: str, model: str, api_key: str, domains: list[str], timeout: float) -> list[dict[str, Any]]:
    endpoint = base_url.rstrip("/") + "/chat/completions"
    if not endpoint.startswith("https://"):
        raise ValueError("AI_ADBLOCK_BASE_URL wajib HTTPS")
    prompt = (
        "Classify each domain for network-level ad blocking. Return only strict JSON with schema "
        '{"results":[{"domain":"exact input","label":"allow|block|review","category":"advertising|tracking|gambling|predatory_lending|scam|service|unknown","confidence":0.0,"reason":"short reason"}]}. '
        "Use block only for dedicated advertising, tracking, gambling, predatory lending, or scam hosts with clear evidence from multiple hostname signals. Distinguish casino/togel/judol/pinjol promotion from legitimate banking, loan, payment, news, and review sites. Use allow for normal service/content/auth/payment/CDN domains. "
        "Use review whenever uncertain. Preserve every input domain exactly once. Domains: "
        + json.dumps(domains, separators=(",", ":"))
    )
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "You are a conservative domain safety classifier. False-positive blocks are worse than missed ads."},
            {"role": "user", "content": prompt},
        ],
    }).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "Accept": "application/json"},
    )
    with _open_api(request, timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("response API tidak memiliki choices[0].message.content") from exc
    if not isinstance(content, str):
        raise ValueError("content response API bukan string")
    return parse_response(content, domains)


def classify_candidates(
    workdir: Path,
    *,
    base_url: str,
    model: str,
    key_file: Path | None,
    batch_size: int = 5,
    min_confidence: float = 0.98,
    timeout: float = 90.0,
    log=print,
) -> dict[str, Any]:
    candidate_paths = (
        workdir / "adblock_ai_candidates.txt",
        workdir / ".runtime_cache" / "ai_adblock_candidates.txt",
    )
    output_path = workdir / ".runtime_cache" / "ai_adblock_blocklist.txt"
    report_path = workdir / ".runtime_cache" / "ai_adblock_report.json"
    allowlist = set(load_domains(workdir / "adblock_allowlist.txt"))
    candidates = sorted({
        domain
        for candidate_path in candidate_paths
        for domain in load_domains(candidate_path)
        if not is_allowlisted(domain, allowlist)
    })
    output_path.unlink(missing_ok=True)
    report_path.unlink(missing_ok=True)
    if not candidates:
        return {"status": "skipped", "reason": "tidak ada kandidat non-allowlist", "count": 0}

    api_key = _read_api_key(key_file)
    if not api_key:
        return {"status": "skipped", "reason": "API key lokal tidak tersedia", "count": len(candidates)}

    accepted: set[str] = set()
    review: list[dict[str, Any]] = []
    try:
        for start in range(0, len(candidates), batch_size):
            batch = candidates[start:start + batch_size]
            for item in _classify_batch(base_url, model, api_key, batch, timeout):
                if (
                    item["label"] == "block"
                    and item["category"] in BLOCK_CATEGORIES
                    and item["confidence"] >= min_confidence
                    and not is_allowlisted(item["domain"], allowlist)
                ):
                    accepted.add(item["domain"])
                else:
                    review.append(item)
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError) as exc:
        log(f"AI adblock fail-open: {type(exc).__name__}: {exc}")
        return {"status": "failed-open", "reason": str(exc), "count": len(candidates)}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    output_tmp.write_text(
        "# Generated by ai_adblock_classifier.py; exact hosts only.\n" + "".join(f"{domain}\n" for domain in sorted(accepted)),
        encoding="utf-8",
    )
    output_tmp.replace(output_path)
    report = {"status": "updated", "model": model, "candidates": len(candidates), "blocked": sorted(accepted), "review": review}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    log(f"AI adblock: {len(accepted)} exact host diterima, {len(review)} allow/review")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Conservative offline AI adblock classifier")
    parser.add_argument("--workdir", type=Path, default=Path.cwd())
    parser.add_argument("--base-url", default=os.environ.get("AI_ADBLOCK_BASE_URL", "https://ai.tamandata.com/v1"))
    parser.add_argument("--model", default=os.environ.get("AI_ADBLOCK_MODEL", "tamandata"))
    parser.add_argument("--key-file", type=Path, default=Path(os.environ.get("AI_ADBLOCK_API_KEY_FILE", ".secrets/ai_adblock.key")))
    parser.add_argument("--batch-size", type=int, default=int(os.environ.get("AI_ADBLOCK_BATCH_SIZE", "5")))
    parser.add_argument("--min-confidence", type=float, default=float(os.environ.get("AI_ADBLOCK_MIN_CONFIDENCE", "0.98")))
    parser.add_argument("--timeout", type=float, default=float(os.environ.get("AI_ADBLOCK_TIMEOUT_SEC", "90")))
    parser.add_argument("--no-refresh", action="store_true", help="gunakan feed Last-Known-Good tanpa refresh")
    args = parser.parse_args()
    workdir = args.workdir.expanduser().resolve()
    key_file = args.key_file.expanduser()
    if not key_file.is_absolute():
        key_file = workdir / key_file
    if not args.no_refresh:
        try:
            from feed_guard import refresh_security_feeds
            refresh_security_feeds(workdir, refresh=True)
        except Exception as exc:
            print(f"AI adblock feed refresh gagal: {type(exc).__name__}")
            return 1
    refresh_streaming_candidates(workdir)
    result = classify_candidates(
        workdir,
        base_url=args.base_url,
        model=args.model,
        key_file=key_file,
        batch_size=max(1, min(100, args.batch_size)),
        min_confidence=max(0.95, min(1.0, args.min_confidence)),
        timeout=max(5.0, min(120.0, args.timeout)),
    )
    print(f"AI adblock status: {result['status']}"
          + (f": {result['reason']}" if result.get("reason") else ""))
    return 1 if result["status"] == "failed-open" else 0


if __name__ == "__main__":
    raise SystemExit(main())
