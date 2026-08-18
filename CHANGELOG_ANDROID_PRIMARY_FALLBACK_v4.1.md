# Changelog v4.1 Android Primary-Fallback

## Perubahan

- Android tidak lagi memasukkan seluruh varian multi-host sebagai kandidat sejajar ke policy group utama.
- `BUG_SERVERS[0]` selalu menjadi host pertama untuk setiap akun Android.
- Host berikutnya hanya digunakan melalui fallback per akun.
- Menambahkan `ANDROID_MULTI_HOST_MODE` dengan mode `primary-fallback`, `primary`, dan `inherit`.
- Menambahkan `ANDROID_FALLBACK_HOST_LIMIT`.
- Menambahkan `ANDROID_FALLBACK_TOTAL_CAP`.
- Menambahkan `ANDROID_FALLBACK_INTERVAL`.
- Menambahkan `ANDROID_FALLBACK_LAZY`.
- Global multi-host Auto/Lite/Fresh Pool tetap tidak berubah.
- Existing security, threat-safe, Indonesia adblock, YouTube guard, AI routing, dan performance profile tetap dipertahankan.
