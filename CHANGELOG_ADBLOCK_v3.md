# Changelog Adblock v3

## Tujuan

Versi ini mengoptimalkan YouTube dan ad/tracker blocking tanpa membuat media CDN ikut terblokir. Fokusnya adalah routing yang benar, failover streaming, deduplikasi provider, Android compatibility, dan browser-level filtering untuk bagian yang memang tidak dapat diselesaikan hanya dengan DNS/router.

## Perubahan utama

### YouTube routing tidak lagi ter-shadow

Versi sebelumnya dapat menulis playback host ke `GLOBAL` pada tahap post-processing. Akibatnya `RULE-SET,youtube_domain,YOUTUBE` yang berada lebih bawah hampir tidak menangani trafik utama. v3 selalu memilih policy `YOUTUBE` jika grup tersebut tersedia.

### Semua profil memiliki grup YOUTUBE

`openclash_auto`, `openclash_lite`, `openclash_android`, dan `openclash_fresh_pool` sekarang mempunyai grup `YOUTUBE` dengan automatic fallback. Lite dan Android dibuatkan grup ringan saat post-processing jika generator awal tidak menyediakannya.

Default:

- fallback
- interval 120 detik
- lazy health-check
- timeout 3000 ms
- max failure 2

### YouTube MRS pada profil router

Auto, Lite, dan Fresh Pool menggunakan `youtube_domain.mrs` dari MetaCubeX. Android tetap explicit-domain only untuk menjaga provider tetap YAML-only.

### Exact `ads.youtube.com`

`ads.youtube.com` sekarang ditolak sebelum `DOMAIN-SUFFIX,youtube.com,YOUTUBE`. Ini mencegah endpoint iklan yang berada di bawah namespace YouTube ikut lolos melalui playback guard.

### Compatibility guard dipertahankan

`static.doubleclick.net` dan `jnn-pa.googleapis.com` tetap dapat diakses dan diarahkan melalui `YOUTUBE`. Tidak ada broad `DOMAIN-SUFFIX,doubleclick.net,REJECT`.

### Provider dedup mode

Default baru:

```json
"ADBLOCK_DEDUP_MODE": "lean"
```

Pada router, v3 melepas provider yang overlap:

- `hagezi-pro-mini`
- `popup-ads`
- `turtlecute-coverage`
- `streaming-ad-safe`

Broad filtering tetap ditangani `ads_domain.mrs` dan `tracker.mrs`. Tiga host streaming-ad yang high-confidence dijadikan exact rules sehingga provider inline terpisah tidak diperlukan. App ads, intrusive/game ad suffixes, threat feeds, fake/scam, dan threat IP tetap aktif sesuai profil.

### Ukuran konfigurasi turun

Dibanding ZIP AI Proxy v2 sebelum patch:

| Profil | Provider v2 | Provider v3 | YAML v2 | YAML v3 |
| --- | ---: | ---: | ---: | ---: |
| auto | 14 | 10 | 41,004 B | ~36.8 KB |
| lite | 12 | 9 | 28,215 B | ~24.5 KB |
| android | 7 | 6 | 29,048 B | ~29.1 KB |
| fresh_pool | 14 | 10 | 42,403 B | ~38.2 KB |

Android tidak mengecil banyak karena profil tersebut memang menggunakan provider YAML kompatibilitas dan explicit ad rules.

### Android compatibility cleanup

Provider `chatgpt_voice` text dari AI Proxy v2 tidak lagi dipasang di Android. Static OpenAI Voice/IP guards tetap tersedia, sehingga routing AI tidak hilang tetapi audit Android kembali YAML-only dan tanpa MRS/text provider.

### Browser filters

`youtube_browser_filters.txt` ditambah:

- exact `ads.youtube.com`
- feed ad-slot cleanup
- search ad-slot cleanup
- watch-next ad-slot cleanup

Filter tetap tidak memblokir `googlevideo.com` atau `static.doubleclick.net`.

## Hasil validasi

- seluruh `*_audit.py` lulus
- `youtube_adblock_audit.py --mode enhanced --dedup lean` lulus pada 4 profil
- Android provider audit lulus, YAML-only, MRS refs 0
- static target validation lulus untuk OpenClash v0.47.156 + Mihomo alpha-ge183c58
- post-processing dua kali menghasilkan output identik, sehingga pipeline idempotent

## Batas teknis

Router tidak dapat menjamin 100% penghilangan iklan YouTube in-stream karena iklan dan video normal dapat berbagi host/CDN. v3 sengaja tidak memblokir media delivery secara agresif. Browser content blocker tetap menjadi lapisan terbaik untuk request berbasis path, DOM, dan response-level ad objects.
