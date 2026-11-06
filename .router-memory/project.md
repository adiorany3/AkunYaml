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
