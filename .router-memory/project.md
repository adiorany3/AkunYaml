# Project context

AkunYaml /Users/macbookpro/Documents/GitHub/AkunYaml; main HEAD b14823c18c30e62a68140975db9b7e4926939b00. Pre-existing runtime cache, build reports/output changes preserved.

Mac builder build_mac_noproxy.py now supports --gameblock. Default retains direct output. Gameblock reads output/mihomo-mac/gameblock/config.yaml and creates sibling openclash_noproxy_gameblock.yaml (~19 MiB). User HerYaml reference read via web; output adapts reference-style local policy, not exact upstream copy. All 20 provider snapshots embedded inline; no network/file providers. No accounts/groups; localhost only, System Proxy, TUN disabled deliberately pending client testing. Public DoH, 12562 rules; game-block-online and games-category REJECT forced before DIRECT exceptions. Original source untouched.

Validation: generator exact Mihomo alpha-ge183c58 parser succeeded before atomic publication. tests/mac_gameblock_selftest.py passes. pytest tests/test_gameblock_priority.py: 14 passed. git diff --check clean. No GUI/runtime tunnel validation. Regenerate: .venv/bin/python build_mac_noproxy.py --gameblock. Unified update can replace output directory; rerun builder afterward.

SHA256 builder 5361a047843b32ff1fcee70e6d7dbc782d348a337e56f7eea9e1eb596a70673a; game source d4f16bb0f0be1e40e93e031c371c417020a638b4033ec0d6aa45b5d149f056fa; game output f5faeb1ed99ba5aba5b82ad4ef1ef272d6ff10f6c2a8f6642bfd5fe78d6225e9.

Prior Hako DNS issue unresolved: parser-valid DoH variants still reported internet loss; OS checks saw disconnected despite GUI report. Need internal Hako logs before more changes.
