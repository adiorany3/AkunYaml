# Project context

AkunYaml main, verified commit 5ff68079c040d5726f8270b595587c412a9e9e4f. Existing provider_cache change preserved. User requested smarter adblock/malware processing. Added adaptive_guard.py, integrated into unified_update: online refresh correlates 4 public feeds (HaGeZi threat/ad, Chocolate4U malware, ABPindo ads), same-category support from >=2 publishers auto-blocks exact hosts only. Publisher agreement not independent ground truth. AI/single-source not sufficient for adaptive overlay. Baseline DIRECT exceptions and adblock_allowlist applied, IPs excluded, cache expires after 24h; invalid timestamp/policy rejected. Overlay applied only to output OpenClash/Mihomo/Sing-box before core validation. output/security contains accepted evidence/report; no browsing telemetry published. Ordinary existing feeds/AI path remain separate.

Added --security-only to update_all.sh to refresh adaptive/feed security without account runner/API AI. No scheduler, news ingestion, zero-day detection, automatic push/deploy. URLhaus/ThreatFox authenticated APIs not integrated. This is correlation of existing live upstream evidence, not fully autonomous malware analysis. Offline builds omit expired overlay; already deployed devices require redeploy to remove old rules.

Verification: full pytest 49 passed, targeted Ruff/diff check clean. Concurrent external unified update/account runner was active; own security-only run correctly refused due lock. Did NOT remove lock/stop user process. Fresh adaptive cache existed with 553 accepted hosts, 4 sources. Validated overlay in isolated copy: 9 YAML profiles + 2 Sing-box profiles passed installed cores. No production output replaced by isolated test. External runner may change outputs independently. No own AI calls or account refresh.

Primary update_all.sh outputs output/, local_build retained. Both generated folders now intentionally versioned with explicit user approval of public credential exposure. .secrets/cache remain ignored. Private AI file JSON api_key/base_url/model; never print. Source gameblock_policy maintained local, 14 independent gameblock feeds. Sing-box gameblock still unavailable (adaptive malware overlay supported).

Fingerprints:
adaptive_guard.py 13d79ac213c059eb38b4d2a0d195bdcd34ce774edcb7bba262a7604cbe762e3f
unified_update.py 21091e32949cc4b1a836e6f10eeb4def53f68bf4207a3b484eaef3c2e2203de7
tests/test_adaptive_guard.py aeb0eb204869d75f0b7d48158e56e859226ca9ae36611964d5a46c5b8d2a39fb
README.md 79eb96a01a19a3e81ccac786b64eb0ccea9700bc13a0d4df0379bc534f4f8ec2

AI response bug fix: Extra data log addressed by accepting one JSON object with optional Markdown fence/plain trailing prose; reject additional structured data and duplicate keys, preserve full schema/exact-domain validation. Invalid-format/schema batch retries once then fail-open. Mock regression suite now full pytest 58 passed; new test lint/py_compile/diff check passed. Existing classifier lint issues remain (shebang, timeout alias, broad catch/type conventions); no live API calls. Cannot determine outer API versus inner model formatting from log alone.
ai_adblock_classifier.py 577ca9eadbeff7a93009eb2786663197cbe42c6d62cd0412fe45f0ae82e7e1be
tests/test_ai_response_format.py 356733516b8f1d1197c809156428135a1fa473ec7640cff6311b6f68f6683b6a
