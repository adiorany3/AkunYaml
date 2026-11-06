# Project context

AkunYaml main, commit 68df270143d4af9449571ca6591f1e4a999354fa. Existing dirty AI/generator changes preserved. Verify working tree and hashes before relying on facts.

Primary entry: bash update_all.sh (online) or --offline. unified_update.py runs local_runner, local_update, independent_gameblock, then publishes private output/. Sources/root profiles/local_build retained as required intermediates. Output: akun; openclash proxy/direct/gameblock; sing-box Android/direct (NO gameblock); mihomo-mac proxy/direct/gameblock. Mac uses localhost system proxy 7890, no automatic TUN. Manifest records source mtimes/hashes, not account liveness. No Git push/pip install/scheduler. Failed stages keep previous unified output, but internal sources may change.

Cleanup completed: removed legacy HerYaml importer gameblock_update.py, one-time gameblock_bootstrap.py, redundant update_local.sh, obsolete importer tests. Extracted live fetch/validate/publish helpers into build_support.py and updated both consumers. Replaced deleted tests with publish rollback/download/validator tests. Removed untracked obsolete .runtime_cache/heryaml_gameblock (21187370 bytes), retained independent_gameblock cache. No active references to deleted components remain. README rewritten to concise 89-line primary usage/reference; historical docs not deleted without dependency evidence. Current gameblock lock .runtime_cache/gameblock.lock.

Verification after cleanup: tests/ 31 passed; bash syntax/py_compile/diff check passed; complete bash update_all.sh --offline succeeded, republished output and validated Mac/gameblock configurations. Deleted paths absent; active cache present. No online account refresh performed.

Gameblock: 14 direct feeds from HaGeZi/ABPindo/anti-AD/Chocolate4U/MetaCubeX, local gameblock_policy baseline. 11984 top-level rules/20 providers from earlier live refresh. Manual baseline not automatically rediscovered. Broad msn.com/yandex.com blocks retained. Feed integrity guard and staged publication. No HerYaml runtime refresh dependency.

Private AI .secrets/ai_adblock.key JSON api_key/base_url/model, permission 600/ignored; never print. Output files 600/directories 700/ignored. Do not delete local_build, active cache, providers or root profiles without refactoring consumers.

Fingerprints:
build_support.py fa3f8670c8263fabc5af450a5e3735737b961e1d1825439a88785784f1a6aedd
independent_gameblock.py c4e6d44297c44807161866b965167e8b81dbcf1f23f3f9c19c70b89feb87590f
unified_update.py b2c7e4c979a0b7b737e38e810e6c268f1cb480fd3929b9b4e95a32e60c334cbc
tests/test_build_support.py 4d2b575a3db9cfb5287c2980df8b2450b89896ca389c6985437dd51bc39a4481
README.md 64678387fb749752eb054ee567b157ed2ad0cb9d7be07ab984e9b6fa43fd58e4
update_all.sh 6655dbe7d7f5165db91a43fcbd46396a1e0136714bb7f31c5efca2ac84c34075
