# Project context

AkunYaml root /Users/macbookpro/Documents/GitHub/AkunYaml; branch main HEAD 75aa6b4133257b7dc6d59f13b1d6e23d8eb41a3b. Existing uncommitted adaptive/README/note changes preserved and fingerprints verified. Current follow-up adds translator validation, parity tests and expanded lint coverage.

Architecture: unified_update stages health/change reports and Sing-box gameblock before validated atomic publication. domain_policy_tools explains local Clash decisions, marking unsupported contexts uncertain. singbox_gameblock preserves adjacent DIRECT/REJECT precedence. release_tools public export opt-in blocklist-only. node_history opt-in private handshake ranking; AI adblock disabled.

Security: ad allowlist exempts adaptive advertising only, not two-known-publisher malware. Category-specific publisher support revalidated on cache read. Exact-host overlay preserves leading Sing-box sniff/hijack-dns and existing routes/default. General allowlist already routes through GLOBAL/proxy, not DIRECT. Account/DNS/routing defaults unchanged.

Follow-up implemented from suggestions: translator rejects non-text rule lists and early/repeated MATCH,DIRECT rather than silently skipping terminal decisions. New tests/test_policy_parity.py compares representative Clash explanation and generated Sing-box decisions for login, CAPTCHA, malware, ads exact-host, game apex/subdomains, and lookalike legitimate domains. Adds terminal/malformed-rule regressions. check_local now lints adaptive modules and parity tests too. README updated.

Verification: check_local.py --full passed 158 pytest tests, configured module lint and native Mihomo/Sing-box gameblock validation on temporary copies. diff --check passed. No rebuild/deploy of published outputs, live account connectivity checks, commit or push. Future: actual device smoke tests for login/payment/streaming and proxy fallback require known device/account environment; offline policy checks cannot prove internet access.

SHA256:
- adaptive_guard.py: d69ed44e345282a54bc73e167d1758d39b87710d120c23751ac3ac002477cf6a
- tests/test_adaptive_guard.py: fb9e9a6d588126dcb052ee126fa24b1636c2f3f91d4d380e98bca81a76b610de
- singbox_gameblock.py: 6b2dd852fc73945136aea9e15fa0ead4ada0a821416ed2647ccc3df18b90c986
- tests/test_policy_parity.py: 2f2974665b724f3d89661ad0169db51c2eb376e5031c4a19e97d7f373bcdcc10
- check_local.py: e26de2972adfd5c9caae985169f3ddee6a3b55e09b6019ed486595bee6420f92
- README.md: e188b78a26dde2274f9c7b3ba2df3b2a245d4338d11348b7292b552f80cadaa9

Cleanup follow-up: removed only untracked development caches (.pytest_cache, .ruff_cache, .mypy_cache, root/tests __pycache__), 8,171,223 logical bytes. Added ignore rules for test/lint/type caches and .DS_Store. Tracked backup_target preserved (apply_existing uses it); empty .build preserved (core build script uses it). Profiles, accounts, secrets, cores, feeds and offline caches untouched. Verification: 22 policy/adaptive tests passed without cache/bytecode generation, Ruff --no-cache passed, diff --check passed.
- .gitignore: fee610ce3030d16c43d9edeef3433d53c9fe99ab8867508b031118d289723aac
