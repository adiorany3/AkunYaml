# AkunYaml v4.0 Performance

v4.0 focuses on reducing repeated work in the generator and unnecessary health-check traffic on OpenClash/Mihomo.

## Main changes

### Efficient health-check profile

Only the small hot pools stay active by default:

- `WARM-UP`: 4 nodes, 60 second interval, active.
- `AUTO-FAST`: up to 8 nodes, 90 second interval, active.
- `PING-CHECK`: lazy, 300 second interval.
- `WARM-UP-CF`: lazy, 120 second interval.
- `STREAMING-FAST`: lazy.
- `FALLBACK`: lazy, 180 second interval.
- `LOAD-BALANCE`: lazy, 300 second interval.

A lazy group is still available. Mihomo checks it when the group is actually used instead of continuously probing the same nodes in the background.

## Multi-host budget

New settings:

```json
{
  "BUG_TOTAL_VARIANTS_CAP": "24",
  "BUG_MIN_BASE_NODES": "8"
}
```

The cap limits duplicated fallback variants. Base accounts are never removed by the cap. For example, 10 base nodes with three target hosts produce at most 24 runtime variants. A 30-node fresh pool keeps all 30 base nodes and does not expand past them when the configured cap is 24.

## Persistent subscription cache

```json
{
  "SUBSCRIPTION_CACHE": "true",
  "SUBSCRIPTION_CACHE_TTL_SEC": "1800",
  "SUBSCRIPTION_CACHE_STALE_IF_ERROR": "true",
  "SUBSCRIPTION_CACHE_DIR": ".runtime_cache/subscriptions"
}
```

Features:

- fresh TTL cache;
- HTTP `ETag` revalidation;
- HTTP `Last-Modified` revalidation;
- stale cache fallback when an upstream subscription is temporarily unavailable;
- atomic cache writes.

## Persistent provider and RDAP cache

```json
{
  "PROVIDER_CACHE": "true",
  "PROVIDER_CACHE_TTL_SEC": "1209600",
  "PROVIDER_CACHE_FILE": ".runtime_cache/provider_cache.json"
}
```

Provider/ASN labels can be reused for 14 days. This avoids repeating DNS/RDAP work on every generation.

## Adaptive candidate pool

```json
{
  "ADAPTIVE_CANDIDATES": "true",
  "CANDIDATE_INITIAL": "250",
  "CANDIDATE_MAX": "2000",
  "CANDIDATE_MIN": "250"
}
```

The tester starts with a smaller candidate window and expands only when it cannot obtain enough healthy nodes. Candidates outside the configured cap are reported as intentionally skipped instead of being silently left pending.

## Performance budget audit

Run:

```bash
python performance_budget_audit.py
```

The audit checks active direct node probes per minute, lazy group policy, YAML size, cache settings, adaptive candidate settings, and the global multi-host budget.
