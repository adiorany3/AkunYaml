# v2.1 OpenClash Compatible

- Validate every parsed proxy with current Mihomo using an isolated `-t` config.
- Skip incompatible automatic and manual nodes before final YAML/account output.
- Prevent one invalid node from breaking an entire Mihomo URL-test batch.
- Increase candidate pool before compatibility filtering.
- Add `openclash_compat_report.csv`.
- Make NekoBox/sing-box validation optional by default for OpenClash-focused usage.
