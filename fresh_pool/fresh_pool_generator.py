#!/usr/bin/env python3
"""Generate fresh pool candidates with optimized parallel URL testing.

- Reads candidate URLs from ``fresh_candidates.txt`` (one per line).
- Performs async HTTP HEAD requests with a 2 second timeout.
- Caches results in ``.cache/fresh_pool_cache.json`` so unchanged lists are
  skipped on subsequent runs.
- Writes a concise JSON report (``fresh_candidates.json``) and updates the
  markdown report ``fresh_candidates_report.md`` with the top N candidates.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Tuple

import aiohttp

# ---------------------------------------------------------------------------
# Configuration (can be overridden via environment variables if needed)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
CANDIDATES_FILE = BASE_DIR / "fresh_candidates.txt"
JSON_REPORT = BASE_DIR / "fresh_candidates.json"
MARKDOWN_REPORT = BASE_DIR / "fresh_candidates_report.md"
CACHE_FILE = BASE_DIR / ".cache" / "fresh_pool_cache.json"
TOP_N = int(os.getenv("FRESH_POOL_TOP_N", "20"))
TIMEOUT = float(os.getenv("FRESH_POOL_TIMEOUT", "2.0"))
# ---------------------------------------------------------------------------

logger = logging.getLogger("fresh_pool")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)


def _load_candidates() -> List[str]:
    """Read candidate URLs (or domains) from the text file.
    Empty lines and lines starting with ``#`` are ignored.
    """
    if not CANDIDATES_FILE.is_file():
        logger.error("Candidates file %s not found", CANDIDATES_FILE)
        return []
    candidates = []
    for line in CANDIDATES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        candidates.append(line)
    return candidates


def _hash_candidates(candidates: List[str]) -> str:
    """Return a SHA‑256 hash of the candidate list (order‑sensitive)."""
    m = hashlib.sha256()
    for c in candidates:
        m.update(c.encode("utf-8"))
        m.update(b"\n")
    return m.hexdigest()

async def _test_one(session: aiohttp.ClientSession, url: str) -> Tuple[str, int | None, str | None]:
    """Perform a HEAD request (fallback to GET) and return (url, ms, status).
    If the request fails or times out, ``ms`` and ``status`` are ``None``.
    """
    start = asyncio.get_event_loop().time()
    try:
        async with session.head(url, timeout=TIMEOUT) as resp:
            ms = int((asyncio.get_event_loop().time() - start) * 1000)
            return url, ms, f"HTTP {resp.status}"
    except Exception:
        # Try GET as a fallback (some servers reject HEAD)
        try:
            async with session.get(url, timeout=TIMEOUT) as resp:
                ms = int((asyncio.get_event_loop().time() - start) * 1000)
                return url, ms, f"HTTP {resp.status}"
        except Exception:
            return url, None, None

async def _run_tests(candidates: List[str]) -> List[Tuple[str, int | None, str | None]]:
    """Run URL tests in parallel using a limited number of connections.
    """
    connector = aiohttp.TCPConnector(limit_per_host=10, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [ _test_one(session, url) for url in candidates ]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results


def _load_cache() -> dict:
    if CACHE_FILE.is_file():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Failed to read cache %s: %s", CACHE_FILE, e)
    return {}


def _save_cache(data: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _write_json_report(results: List[Tuple[str, int | None, str | None]]) -> None:
    # Build a list of dicts sorted by latency (fastest first, None last)
    items = []
    for url, ms, status in results:
        items.append({"url": url, "latency_ms": ms, "status": status})
    items.sort(key=lambda x: (x["latency_ms"] is None, x["latency_ms"]))
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(items),
        "candidates": items,
    }
    JSON_REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Wrote JSON report with %d entries to %s", len(items), JSON_REPORT)


def _update_markdown_top_n(results: List[Tuple[str, int | None, str | None]]) -> None:
    # Load existing markdown (if any) and replace the "Kandidat Fresh Teratas" section.
    if not MARKDOWN_REPORT.is_file():
        logger.warning("Markdown report %s not found – skipping update", MARKDOWN_REPORT)
        return
    content = MARKDOWN_REPORT.read_text(encoding="utf-8").splitlines()
    # Find the start of the list (look for a line that begins with "## Kandidat Fresh Teratas")
    start_idx = None
    for i, line in enumerate(content):
        if line.strip().startswith("## Kandidat Fresh Teratas"):
            start_idx = i
            break
    if start_idx is None:
        logger.warning("Could not locate section in markdown – skipping update")
        return
    # Build new list lines (top N)
    top = sorted(results, key=lambda x: (x[1] is None, x[1]))[:TOP_N]
    new_lines = ["## Kandidat Fresh Teratas"]
    for idx, (url, ms, status) in enumerate(top, 1):
        ms_str = f"{ms}ms" if ms is not None else "timeout"
        new_lines.append(f"{idx}. `{url}` (latency={ms_str}, status={status or 'error'})")
    # Replace old lines after the header until the next heading or end of file
    end_idx = start_idx + 1
    while end_idx < len(content) and not content[end_idx].startswith("##"):
        end_idx += 1
    new_content = content[:start_idx] + new_lines + content[end_idx:]
    MARKDOWN_REPORT.write_text("\n".join(new_content), encoding="utf-8")
    logger.info("Updated markdown report with top %d candidates", len(top))


def main() -> int:
    candidates = _load_candidates()
    if not candidates:
        logger.error("No candidates to process")
        return 1
    # Compute hash for cache validation
    cur_hash = _hash_candidates(candidates)
    cache = _load_cache()
    if cache.get("hash") == cur_hash and "results" in cache:
        logger.info("Cache hit – using previously stored results")
        results = cache["results"]
    else:
        logger.info("Cache miss – performing parallel URL tests")
        results = asyncio.run(_run_tests(candidates))
        cache = {"hash": cur_hash, "results": results}
        _save_cache(cache)
    # Write JSON and update markdown
    _write_json_report(results)
    _update_markdown_top_n(results)
    return 0

if __name__ == "__main__":
    sys.exit(main())
