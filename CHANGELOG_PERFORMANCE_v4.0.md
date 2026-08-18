# Changelog v4.0 Performance

## Performance

- Reduced default background direct-node health probes from about 38.33/min on Auto/Lite/Android and 45/min on Fresh Pool to about 9.33/min in the packaged outputs.
- Kept `WARM-UP` and `AUTO-FAST` active while moving diagnostic/specialized groups to lazy checks.
- Added a global multi-host expansion budget with base-node preservation.
- Added persistent subscription caching with TTL, ETag, Last-Modified, and stale-if-error behavior.
- Added persistent provider/RDAP cache with TTL.
- Added adaptive candidate windows with progressive expansion.
- Reduced the default candidate minimum from 1200 to 250.
- Limited AI service health pools to 8 nodes by default.

## Reliability

- Cache writes use temporary files plus atomic replace.
- Invalid numeric settings remain clamped by existing safe readers.
- Candidates outside the adaptive cap are explicitly marked skipped.
- Multi-host variant cap never removes base accounts.

## Validation

- Added `performance_budget_audit.py`.
- Existing threat-safe, YouTube, Android provider, app ads, streaming, popup/game, security hardening, and multi-host audits remain part of the regression suite.
