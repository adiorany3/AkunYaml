# Mac + GitHub Workflow Update

- Menambahkan `mac_build_target_core.sh` untuk build Mihomo exact commit `e183c58` pada Intel dan Apple Silicon Mac.
- Menambahkan `mac_refresh_accounts.sh` untuk git pull, refresh akun, generate YAML, exact-core validation, dan optional git push.
- Menambahkan shortcut Finder `.command`.
- Menambahkan `openwrt_git_pull_update.sh` untuk pull YAML terbaru di router dan parser-test sebelum copy ke OpenClash.
- `run_local_unix.sh` otomatis memakai workflow Mac saat dijalankan di macOS.
- Memperbaiki bug `local_config.json` yang sebelumnya ditimpa default argparse `20/10`; sekarang default `MAX_NODES=10` dan `MIN_OUTPUT_NODES=6` dari config benar-benar berlaku.
- Menambahkan `.gitignore` untuk `.venv`, local binary/build cache, `__pycache__`, dan `.DS_Store`.
