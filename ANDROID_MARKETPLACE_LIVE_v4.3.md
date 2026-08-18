# Android Marketplace Live Compatibility v4.3

Version 4.3 fixes marketplace live/video sessions that could be blocked by the Android security profile.

## What changed

Android now has a dedicated marketplace compatibility guard. The guard is evaluated after the high-confidence malware, phishing, and cryptominer providers, but before privacy, advertising, and tracker rules.

This keeps security protection active while preventing broad ad/tracker filters from breaking first-party marketplace session and live-media endpoints.

The Android profile also applies three transport protections to marketplace endpoints:

- real-IP operation through `fake-ip-filter`;
- normal public DoH via `nameserver-policy`, bypassing family-category DNS for those endpoints;
- TLS/HTTP sniffer skip to avoid unnecessary destination override on live/CDN traffic.

## Default protected marketplace namespaces

The built-in list covers core first-party/live namespaces for Shopee, Tokopedia, Lazada, Blibli, Bukalapak, and selected TikTok Shop/Live media infrastructure.

The whole `tiktok.com` suffix is intentionally not whitelisted. Explicit TikTok advertising endpoints remain blockable.

## Settings

```json
{
  "ANDROID_MARKETPLACE_LIVE_COMPAT": "true",
  "ANDROID_MARKETPLACE_LIVE_POLICY": "GLOBAL",
  "ANDROID_MARKETPLACE_LIVE_DOMAINS": "",
  "ANDROID_MARKETPLACE_LIVE_EXACT_DOMAINS": ""
}
```

An empty domain setting uses the conservative built-in defaults from `android_marketplace_policy.py`.

For custom domains, provide a JSON array or comma-separated list. Example:

```json
{
  "ANDROID_MARKETPLACE_LIVE_DOMAINS": [
    "example-marketplace.co.id",
    "example-cdn.com"
  ]
}
```

## Security order

```text
LAN/private
AI/YouTube compatibility
Malware
Phishing
Cryptominers
Marketplace Live compatibility
Privacy filters
Inline app/streaming ad rules
Regional/global ads
Trackers
MATCH -> GLOBAL
```

This change is Android-only. Router outputs remain unchanged.
