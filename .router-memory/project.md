# Project context

AkunYaml main, verified commit 7d0d47d9d68ea70fdf72f05a404a42ee014c97c4. Worktree clean before this audit; current changes are audit fixes. Recheck working tree/fingerprints before edits.

Entry bash update_all.sh, --offline skips account/feed refresh. unified_update stages local_runner (online only), local_update, independent_gameblock, then private output packaging. output includes accounts, OpenClash proxy/direct/gameblock, Sing-box Android/direct (NO gameblock), Mihomo Mac proxy/direct/gameblock. Root/local_build are necessary intermediates. No Git push or scheduler. Online runner may call configured AI.

Audit fixes: validate every bundled OpenClash/Mihomo YAML and both Sing-box JSON with installed cores before publication (previously Mac only); reject empty YAML policy; validate feed manifest structure, nonempty safe unique paths, allowed URLs/formats before downloading; reject unknown feed formats/YAML non-list payload; offline cache must match URL/path/format as well as SHA256. Old metadata without format requires one feed refresh. Cache refreshed successfully. Backup cleanup failure after successful publication now warns rather than falsely claiming rollback. Targeted lint fixes applied.

Verification: full pytest collection 44 passed (initial 33); targeted Ruff clean, py_compile/bash syntax/diff check passed. Actual independent_gameblock --refresh succeeded for 14 feeds; complete update_all.sh --offline succeeded including all profile core validation. Output permissions 600/700, manifest and lock cleanup verified. Online account refresh, AI endpoint health, account liveness and device runtime tests NOT performed. No claim exhaustive bug freedom.

Remaining limitations: offline validators can download geodata; O_EXCL lock can remain after hard kill; external/legacy processes can modify root sources concurrently; multi-directory cache/output publication not a single atomic transaction. Provider manual rules still require maintenance. Game baseline blocks broad msn.com/yandex.com. 14 independent feeds, local gameblock_policy, no HerYaml refresh dependency.

Private .secrets/ai_adblock.key JSON api_key/base_url/model mode 600, ignored; never print. Legacy importer/bootstrap/update_local removed in prior task; shared build_support retained.

Fingerprints:
build_support.py e6043f045592f17acd870e4bc9e18f02efc8f6447b92b9b983a0711d5f84ca27
independent_gameblock.py 4b22aad26b7831dd6e5bae2bee8db6c670869990b1e3c297f8762b61981fddc6
unified_update.py 8244a1b662fffb37a08a6f8509e426d3b7694ca24809cc33963ebc72f40d2514
local_update.py 0d2c7be6cbb29a5e28e64f444b5bbb2964c86545173f0576ce51dc8765927833
tests/test_build_support.py 9a5abdf005ca80d7fb59b93ed93d8c1504d8702eb13cccd3de99c5dcbc61a8c2
tests/test_independent_gameblock.py d16e844dc8a415e518a230395013c673dbe4db13b6a6e8fe097be49e0a5cc6bd
tests/test_unified_update.py b85cf87b88666058a373ee5e47f7672da8b2404d9417187cd2c06278908669f3
README.md 66b2bb36b5e578c803b26dcc5b49e5383d8e3c711b0187475ddcb0148194abf5

Publication change: user explicitly approved publishing all generated proxy/account credentials after warning. Removed local_build/output ignores; keep .secrets/runtime caches/validator databases/staging/backups ignored. Staged .gitignore plus 146 generated files (147 files total); no commit or push. README/generated README warn about exposure and local file-provider deployment. Tests 44 passed. Earlier audit changes remain unstaged; do not silently include unrelated work.
