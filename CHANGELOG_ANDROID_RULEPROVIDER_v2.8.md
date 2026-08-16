# Android Rule-Provider Compatibility v2.8

Target: Clash Meta for Android profiles that cannot parse MRS rule providers.

Changes:

- `openclash_android.yaml` uses YAML rule providers only.
- No `.mrs` URL, `.mrs` path, or `format: mrs` remains in the Android output.
- `ads_domain` uses MetaCubeX `classical/category-ads-all.yaml` with `behavior: classical`.
- `tracker-domain` uses MetaCubeX `classical/tracker.yaml` with `behavior: classical`.
- Android threat protection uses YAML domain providers for malware, phishing, and cryptominers.
- The Android profile runs in `mode: rule` so ad/tracker/threat `RULE-SET` entries are evaluated.
- The final rule is `MATCH,GLOBAL`, preserving the previous global proxy behavior for normal traffic.
- LAN and RFC1918 traffic is sent to `DIRECT` before blocklists.
- Router/OpenClash outputs keep MRS providers for efficiency. Only the Android output is converted.

Validation:

```bash
python android_ruleprovider_audit.py openclash_android.yaml
python youtube_adblock_audit.py
python apply_existing.py --static-only
```
