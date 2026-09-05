#!/usr/bin/env python3
"""Conservative offline AI classification for explicit adblock candidates."""
from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import stat
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DOMAIN_RE = re.compile(
    r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$",
    re.IGNORECASE,
)
ALLOWED_LABELS = {"allow", "block", "review"}
BLOCK_CATEGORIES = {"advertising", "tracking"}


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


def is_allowlisted(domain: str, allowlist: set[str]) -> bool:
    return any(domain == allowed or domain.endswith("." + allowed) for allowed in allowlist)


def parse_response(content: str, expected: list[str]) -> list[dict[str, Any]]:
    data = json.loads(content)
    if not isinstance(data, dict) or set(data) != {"results"} or not isinstance(data["results"], list):
        raise ValueError("response harus object dengan satu field results")
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in data["results"]:
        if not isinstance(item, dict) or set(item) != {"domain", "label", "category", "confidence", "reason"}:
            raise ValueError("item response memiliki schema tidak valid")
        domain = normalize_domain(str(item["domain"]))
        label = str(item["label"]).lower()
        category = str(item["category"]).lower()
        confidence = item["confidence"]
        reason = str(item["reason"]).strip()
        if domain is None or domain in seen or label not in ALLOWED_LABELS:
            raise ValueError("domain atau label response tidak valid")
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
        '{"results":[{"domain":"exact input","label":"allow|block|review","category":"advertising|tracking|service|unknown","confidence":0.0,"reason":"short reason"}]}. '
        "Use block only for dedicated advertising or tracking hosts with clear evidence. Use allow for normal service/content/auth/payment/CDN domains. "
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
    with urllib.request.urlopen(request, timeout=timeout, context=ssl.create_default_context()) as response:
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
    batch_size: int = 25,
    min_confidence: float = 0.98,
    timeout: float = 30.0,
    log=print,
) -> dict[str, Any]:
    candidates_path = workdir / "adblock_ai_candidates.txt"
    output_path = workdir / ".runtime_cache" / "ai_adblock_blocklist.txt"
    report_path = workdir / ".runtime_cache" / "ai_adblock_report.json"
    allowlist = set(load_domains(workdir / "adblock_allowlist.txt"))
    candidates = [domain for domain in load_domains(candidates_path) if not is_allowlisted(domain, allowlist)]
    output_path.unlink(missing_ok=True)
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
    args = parser.parse_args()
    result = classify_candidates(args.workdir.resolve(), base_url=args.base_url, model=args.model, key_file=args.key_file)
    print(f"AI adblock status: {result['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
