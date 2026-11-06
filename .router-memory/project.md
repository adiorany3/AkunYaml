# Project context

AkunYaml main, inspected commit 2e2cc5de82be43bdaeef48197952f944c0d690bd. Worktree initially clean. User reports unable to import accounts into OpenClash OpenWrt; exact router error/version unavailable. Found concrete packaging issue: existing YAML uses local file providers not downloaded when importing raw YAML alone.

Added openwrt_export.py to unified packaging after adaptive overlay, before all-core validation. Generates six complete output/openclash/subscription/*.yaml variants: file rule providers become HTTPS providers referencing published output companion assets. Distinct cache names, safe local path checks, missing dependencies abort. Existing external HTTP/inline providers retained. URLs currently fixed to adiorany3/AkunYaml main; all generated outputs must be committed/pushed for URLs to exist. Existing local/manual deployment profiles untouched.

Also output/akun/openclash_proxy_provider.yaml contains proxies mapping (10 existing nodes), intended for proxy-provider integration not full config. akun.txt is URI list, not config YAML. README explains subscription Raw URL, Meta/Mihomo core, router access and public/private GitHub limitations. Target project core OpenClash v0.47.156 + Mihomo alpha-ge183c58, other versions unverified. Core import validity does not imply account liveness.

Verification: full pytest 69 passed, targeted Ruff/py_compile/diff check clean. Actual update_all.sh --offline succeeded validating all original and six subscription profiles plus Sing-box. Six profiles have no file rule providers; all generated URL asset paths exist locally; account provider shape verified. No account refresh/remote GitHub push/device runtime test performed. Generated output files changed and new ones untracked pending commit.

Prior features retained: independent gameblock feeds, adaptive overlay, exit-3 account retention, strict AI parser with per-domain fallback. .secrets/ai_adblock.key JSON api_key/base_url/model ignored; never print. local_build/output intentionally Git-trackable with user consent for credential exposure; caches ignored. One entry update_all.sh, --offline and --security-only supported.

Fingerprints:
openwrt_export.py 0f2c608486e2987aa3238aa3b0e6efa29fda5db97ce7d31dd9d9360225c79ed0
unified_update.py 0bf3b94be8a02cfb216a75c475929aa1c5eba6043b71ff6e25563e03e7a2afe3
tests/test_openwrt_export.py 9e2d005cc0c618aa1bd41e174d5331343fe2a28784bbbb7724290f43a3ac254a
README.md 8df09d8bd410d3daf823a7092d0e1d6b759b07340bdfe0c5793156bc5c689dec

OpenClash direct import fix at commit a3eb4050e4f2d257d3de667ab457ae401fc5c1d2: user core OpenClash v0.48.002 alpha-smart-gdaf3ad0; selects error no proxies/proxy-groups (exact raw error unavailable). Remote provided /gameblock URL has 19 file providers and no accounts/groups; /subscription has 19 HTTP providers. Added proxies empty list + DIRECT-ONLY select group containing built-in DIRECT only to direct subscription exports. No fake accounts, rules unchanged, original local profiles untouched. 71 tests passed, Ruff/py_compile/diff check clean, actual offline unified build succeeded including core validation. Verified generated gameblock subscription DIRECT-ONLY and zero accounts. Exact smart core/router UI untested; installed core remains alpha-ge183c58. Changes local only, not committed/pushed in this task; URL still needs publishing to reflect fix.

HerYaml structure clarification at e1c6d236b1be60ad5ef9604b66cd78508e55ed51: fetched reference currently has 3 real VLESS accounts, MANUAL select [DIRECT, accounts], MATCH,MANUAL; name noproxy did NOT mean no accounts. User explicitly wants this format. Added manual_gameblock in exporter: output OpenClash gameblock/local+subscription includes existing generator accounts (10), MANUAL DIRECT-first, final MATCH,MANUAL; store-selected false to avoid restoring old proxy selection. Baseline blocking rules unchanged; no HerYaml credential copied. Original local_build and Mac direct/gameblock remain proxy-free. Validation: 75 tests passed; Ruff/py_compile/diff clean; offline unified build passed all cores. Verified both generated output profiles 10 accounts/MANUAL/DIRECT-first. Not committed/pushed, exact user smart core still untested.
openwrt_export.py ff0da002933e398cab3aea81be489989dd75d8fce80602f81e5b6993e1621fa2
unified_update.py d0b319241149f8e067809d3a96f0fea3f7970155c4314e3339a654861439f7bf
tests/test_openwrt_export.py 181bbc09c00ac4c439feba757fdc5ab218e3d6b6b6d40c8e7988a9c9042f4c4e
