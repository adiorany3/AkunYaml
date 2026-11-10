# Project context

AkunYaml root /Users/macbookpro/Documents/GitHub/AkunYaml; branch main; HEAD d30922ca9c998423fd5f6a39b81e84953337b850. Uncommitted authorized development changes listed below; existing generated outputs unchanged.

Implemented unified health report, static domain explanation with explicit uncertainty and local MRS decoding via core, aggregate credential-free release preview (output/changes.json), separate public blocklist-only export that rejects unrelated targets, direct Sing-box gameblock translation preserving adjacent DIRECT/REJECT policy precedence, opt-in private bounded handshake history with failure ranking penalty, and one-command local checks. Default publication and ranking unchanged. History requires NODE_HISTORY_ENABLED=true; handshake is not full proxy connectivity. Public export is opt-in; complete output still contains credentials.

Architecture: domain_policy_tools shares provider parser for rule_simulation and singbox_gameblock. unified_update stages generated Sing-box gameblock, validates all profiles, records validation count, health and change reports before atomic publication. node_history called after source batch checks in sumberyaml_core; 20 samples per node, 10000 nodes, seven-day expiry. check_local --full uses temporary copies and local cores, no refresh or deployment. README documents CLI commands and limits.

Verification: final check_local.py --full passed 141 pytest tests, changed-module lint, and real Mihomo/Sing-box gameblock integration. compileall and diff --check passed. Domain explanation and no-change preview smoke checks passed. No online refresh, active profile changes, commit or push. Next successful update publishes new reports and Sing-box profile. Preview compares definitions, not provider content; static explanation marks unsupported runtime context uncertain. Legacy core lint debt not reformatted.

AI adblock follow-up: local_config AI_ADBLOCK_ENABLED=false; local_runner now requires explicit truthy opt-in for classification/cache. generate_yaml skips stale AI cache when disabled. Non-AI feeds unchanged, secrets/cache preserved, existing outputs not rebuilt. Added tests/test_ai_optional.py; 31 targeted tests and full check_local --full (141 tests and both cores) passed. security_feed_report.md was already modified at task start; left intact.

SHA256:
- health_report.py: 004ceef7fa324e4001dcfe611fd5449174972e67e9fb427d190ebc69b5cfbccf
- domain_policy_tools.py: 0bff11ab1443b2ee3531cc07b1996562e6f8bc7ac0b47c057d6d5b84311099bb
- release_tools.py: dad9fde934d9de3662c495abc1c70e9f8308c15aac5dc4d02ffb593dbc27cbfe
- singbox_gameblock.py: 62d7ddd98b518530f8602f34e7038fea5c084f28e830ee502dfeabd29e7bb2f2
- node_history.py: 6f406994f3c4fef968a9db44a955f205d8d92adfa5224d86eca3938500092e3e
- check_local.py: 59c1795e51fda630dc839317342f7f8eba69b8a0e58e2861ab9eddfac5908af7
- rule_simulation.py: 15f7c5c3c594a8a8329be40c0c38ff210161ecdf4b1b0a1b18aade52e4db254e
- unified_update.py: 347ed7a0ea5fe9f3f001b88d6cdbd725b939d04284927ad8bfcce37aad98da4c
- sumberyaml_core.py: 36a7c9e15de599e8a2b7379783047e0044cfb85798ec481d31c8939b62ac982f
- tests/test_development_tools.py: 1680901bd04e9d1bb60c40224068fc844d4b1a17fdc02c3420ccdd4d64745fd4
- tests/test_health_report.py: 00c259f2c789ec41ed8b202929239300d34141cba3dc47fed02c183a33e8b01f
- README.md: 78d877c1728b0280c1b2b4cbb07f5acdae3f8a7c08e64bb41b686116b2c41585
- tests/test_unified_update.py: 2228273247bddb5a28973d0eea61415b84f709361484a70d82161c537b43698a
- local_config.json: 7f8ae18a0ef2a299507b0d3bb4c19df8039aa92fdf3778f88d7fe4195fc655b3
- local_runner.py: 0e203f78357bbd7660031b73a00a28279e16e9e7492b8cea1e9960c742bc2cb5
- generate_yaml.py: c8db3afba9e02177b96ff4c491be61d35eb1bbfc758d6de7826549313e6ab795
- tests/test_ai_optional.py: 3fef62494c16c649cc188de30b22902a21b5e5bcdc9b2249357144d92d6c33c0
