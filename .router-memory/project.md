# Project context

AkunYaml main, inspected commit 28f9dac36e8abfd634757fdf893c6ee10dcadd1c, initially clean. Current task builds bulk approved game-domain list and local log candidate import.

Added game_domain_policy.py: normalize plain domains/HTTP URLs, reject IPs/malformed entries; read manual_domains.txt, deduplicate approved suffix REJECT rules and prepend to gameblock. Seeded games.co.id/easy-games.io/coolgamesfree.org. allow_domains.txt is candidate exclusion/conflict check only, never inserts DIRECT. Existing baseline game rules retained; category feed still active. Integrated with independent_gameblock and build report.

CLI imports local JSON connection snapshot connections[].metadata.host, JSONL metadata.host, or Mihomo text destination arrow. Input bounded 20MiB. Candidate report .runtime_cache/game_candidates.json mode600, ignored Git, no source IP/raw logs/API upload. All observed unknown hosts remain review, not inferred games. User manually approves by copying domain into list. No live router log used.

Validation: full pytest 100 passed, targeted Ruff/diff clean, CLI help works. Offline unified build and all core profile validation completed successfully. Not committed/pushed/deployed. Post-build changes only reject malformed URL/port input; tests rerun.

Main entry update_all.sh, --offline/--security-only; output/ user-facing, local_build intermediates. Both versioned with user approval of credential exposure; .secrets/cache ignored. Private AI JSON api_key/base_url/model; never print. Independent gameblock uses direct feeds; local baseline remains needed. Sing-box gameblock unavailable. OpenClash gameblock export now real local accounts/MANUAL select DIRECT first/MATCH,MANUAL; subscription HTTP providers for URL import. Core local alpha-ge183c58; user alpha-smart-gdaf3ad0 not tested. Geodata seeded locally for temporary validators. Publish requires commit/push, may fail network.

Fingerprints:
game_domain_policy.py baa0fa77e939249716fbff18ecb6f9402a5469be7213e704ce35ef9927864e99
independent_gameblock.py 7ba77785934a194c7b4a61b8e48909a4c7204d968e51436be62142f7a6000baa
gameblock_policy/manual_domains.txt 867bb1604544067033dded17d7dae6a0bab08711094c5d61e3a567eb1519f53d
tests/test_game_domain_policy.py 2caf50d265fb34af1c4ce5e21f7226437e6371b0deb1bd00e5d1a82b91e8edaf
