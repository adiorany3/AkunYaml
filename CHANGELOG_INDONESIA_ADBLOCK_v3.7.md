# Changelog v3.7 - Indonesia Adblock

Tanggal: 18 Agustus 2026

## Ditambahkan

- Provider `ads_indonesia` untuk OpenClash router.
- Sumber regional memakai ABPindo DNS/domain list.
- Rule regional ditempatkan setelah threat protection dan sebelum provider iklan global.
- Toggle `INDONESIA_ADBLOCK=true` pada konfigurasi lokal.
- Audit `adblock_provider_audit.py` sekarang memverifikasi provider regional pada output router.
- File referensi subscription browser `browser_filter_subscriptions_v3.7.txt`.

## Presisi

- Tidak mengimpor seluruh sintaks browser ke OpenClash.
- Tidak menggunakan keyword-domain agresif.
- Allowlist tetap didahulukan.
- Profil Android tetap YAML-only untuk kompatibilitas.

## Output tervalidasi

- openclash_auto.yaml
- openclash_lite.yaml
- openclash_fresh_pool.yaml
- openclash_android.yaml
