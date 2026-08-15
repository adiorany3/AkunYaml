# v2.4 Exact OpenClash

- Added strict proxy hostname/SNI/WS Host sanitation.
- Normalizes valid domains to lowercase.
- Removes malformed proxy domains before output.
- Default MAX_NODES reduced to 10.
- Added router exact-core validator using the installed Mihomo core.
- Directly tests the GitHub source.
- Can watch and capture `/tmp/yaml_sub_tmp_config.yaml`.
- Isolates every proxy using the exact router core.
- Automatically builds `/root/openclash_auto_exact_filtered.yaml` after removing failing proxies.
- If proxies all pass, isolates DNS, sniffer, rules and rule-providers.
