# Changelog v4.3 Android Marketplace Live

- Added Android-only marketplace live compatibility policy.
- Preserved malware/phishing/cryptominer checks ahead of marketplace bypass rules.
- Moved marketplace compatibility ahead of privacy, ad, and tracker rejection.
- Added real-IP `fake-ip-filter` entries for marketplace/live domains.
- Added normal public DoH policy for marketplace/live domains.
- Added sniffer skip entries for marketplace/live domains.
- Added Shopee media CDN coverage including `susercontent.com`.
- Added TikTok Shop/Live media coverage without whitelisting the whole `tiktok.com` suffix.
- Preserved explicit TikTok advertising endpoint blocking.
- Added `ANDROID_MARKETPLACE_LIVE_COMPAT`, policy, and custom-domain settings.
- Added `android_marketplace_live_audit.py` regression test.
- Android health-check budget remains ~4 active probes/min.
- Router Auto/Lite/Fresh Pool YAML outputs remain byte-identical to v4.2.
