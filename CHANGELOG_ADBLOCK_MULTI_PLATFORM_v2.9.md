# Adblock Multi-Platform v2.9

Tanggal: 2026-08-17

## Perubahan

- Adblock tetap aktif pada OpenClash/OpenWrt dan diperkuat untuk Android.
- Android `ads_domain` dipindahkan ke Chocolate4U `category-ads-all.yaml` dengan `behavior: domain` untuk rule-provider YAML yang lebih ringan dan kompatibel.
- Android tetap memakai provider malware, phishing, cryptominer, dan tracker yang dapat update otomatis.
- `strict` kini berbeda nyata dari `balanced`.
- Router strict menambahkan HaGeZi Multi PRO Mini dan HaGeZi Pop-Up Ads.
- Android strict menambahkan Blackmatrix7 Privacy YAML.
- Allowlist tetap diproses sebelum blocklist.
- YouTube playback guard tetap dipertahankan.
- Provider interval tetap default 43200 detik atau 12 jam.
- Dokumentasi Android baru ditambahkan di `ANDROID_ADBLOCK.md`.

## Validasi

- `android_ruleprovider_audit.py`: OK.
- `youtube_adblock_audit.py`: OK untuk seluruh output.
- `validate_openclash_target.py --static-only`: OK untuk seluruh output.
