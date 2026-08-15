# v2.3 Reference-Locked

- Uses the proven ConvertYAML/openclash_auto.yaml routing profile as baseline.
- Preserves newly generated proxies and proxy groups.
- Removes tracker-domain and RULE-SET tracker-domain.
- Removes direct GEOSITE category-ads-all injection.
- Restores ads_domain and youtube_domain MRS providers.
- Restores the full known-good routing rules, including MANUAL Indonesia rules.
- Keeps node compatibility filtering from v2.1.
- Removes deprecated global-client-fingerprint.
- Adds fix_reference_locked.py and openclash_auto_fixed.yaml.
