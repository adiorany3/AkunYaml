# Changelog v3.6 Threat-Safe Precision

- Naik versi runtime menjadi `3.6-precision-threatsafe-adblock-v3`.
- Menambahkan provider router terpisah untuk malware, phishing, dan cryptominer.
- Mengubah prioritas threat-safe menjadi: malware -> phishing -> cryptominer -> fake/scam -> TIF mini -> TIF IP -> ads/tracker.
- Mempertahankan TIF mini sebagai safety net setelah kategori ancaman aktif.
- Mempertahankan TIF IP pada OpenClash Auto dan Fresh Pool.
- OpenClash Lite tetap tanpa TIF IP.
- Mempertahankan Android dalam format YAML-only.
- Menambahkan `THREAT_SAFE_FAMILY_DNS=true` ke konfigurasi lokal.
- Membatasi DNS kategori keluarga hanya untuk `child-safe` dan `threat-safe` agar `app-safe` lebih presisi.
- Menambahkan audit urutan threat layer, family DNS/fallback, dan larangan heuristic `DOMAIN-KEYWORD,...,REJECT`.
- Mempertahankan allowlist sebelum semua blocklist.
- Mempertahankan YouTube compatibility guard, AI routing guard, streaming-safe, popup/game ad protection, dan app-safe rules.
