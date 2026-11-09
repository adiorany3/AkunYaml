# Project context

AkunYaml; root /Users/macbookpro/Documents/GitHub/AkunYaml; main; HEAD 7291ac0302f8963f8e566865eee4c25e13ba3c1e. Initial working tree clean.

Hako DNS: local_update.hako_singbox deep-copies profiles, replaces local resolver with direct Cloudflare DoH at IP 1.1.1.1:443, TLS verification/SNI cloudflare-dns.com, keeps resolver tags and DNS policies. Hijack DNS matches port 53. Android profiles untouched. unified_update.bundle generates Hako variants before adaptive guard and core validation.

Ready files: output/sing-box/singbox_hako_proxy.json and singbox_hako_direct_adblock.json. Existing security rules/accounts retained. No gameblock added.

Verified: both core checks pass (sing-box 1.14.2); tests/hako_dns_selftest.py passes; pytest tests/test_local_update.py tests/test_unified_update.py: 14 passed; diff --check passes. HTTPS DoH lookup for reported domain succeeded. Local SOCKS runtime experiment output unavailable; do not claim end-to-end success. Hako tunnel still requires user import/test.

SHA256 local_update.py d2f5dc506298e28816d37dcd176c7912404242edc9aba3db130c4afb5250c5ea; unified_update.py 4c63b912243f749210c5671dccc2441c3891d25f5cf00645f11f4056acc13ad6; tests/hako_dns_selftest.py 8fc7ff4eefa80a0e148fa0b3c8d5c3f210f42f8ef0de24ce95b97cb89bdc0032.
