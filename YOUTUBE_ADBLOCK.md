# YouTube Ad Blocking v3

Mode default paket ini adalah `threat-safe + enhanced + lean`.

## Arsitektur

YouTube v3 memakai dua lapisan. OpenClash/Mihomo menangani host iklan yang dapat dipisahkan dengan aman, tracker, threat feed, serta routing streaming. `youtube_browser_filters.txt` menangani elemen dan request berbasis path yang tidak dapat dibedakan hanya dari domain/IP.

Urutan rule penting:

1. LAN/private dan routing AI
2. YouTube compatibility hosts
3. exact/high-confidence YouTube ad hosts
4. YouTube playback routing
5. threat / general ads / tracker
6. kategori routing lain

Dengan urutan ini, endpoint iklan seperti `ads.youtube.com` ditolak sebelum `DOMAIN-SUFFIX,youtube.com,YOUTUBE` sempat menangkapnya.

## Routing YouTube

Semua output sekarang memiliki grup `YOUTUBE`. Grup menggunakan `fallback` agar pemilihan jalur streaming otomatis dan egress tidak berganti tanpa alasan.

Default health-check:

```yaml
url: https://www.gstatic.com/generate_204
interval: 120
lazy: true
timeout: 3000
max-failed-times: 2
```

Profil router menggunakan `youtube_domain.mrs` dari MetaCubeX ditambah explicit playback guards. Profil Android sengaja tidak memakai MRS untuk menjaga kompatibilitas dengan core Clash Meta for Android yang lebih lama. Android tetap memiliki explicit guards.

Playback/compatibility yang selalu menuju `YOUTUBE` sebelum broad ad lists:

- `static.doubleclick.net`
- `jnn-pa.googleapis.com`
- `youtube.com`
- `youtu.be`
- `youtube-nocookie.com`
- `googlevideo.com`
- `ytimg.com`
- `youtubei.googleapis.com`
- `youtube.googleapis.com`
- `ggpht.com`

Jangan memblokir `googlevideo.com` secara global. Video normal dan iklan dapat berbagi infrastruktur media. `static.doubleclick.net` juga sengaja tidak diblokir karena ada kasus playback browser yang gagal ketika `instream/ad_status.js` tidak dapat dimuat.

## Exact/high-confidence ad rules

Rule berikut dievaluasi sebelum playback guard:

- `ads.youtube.com`
- `googleads.g.doubleclick.net`
- `ad.doubleclick.net`
- `pubads.g.doubleclick.net`
- `securepubads.g.doubleclick.net`
- `pagead2.googlesyndication.com`
- `tpc.googlesyndication.com`
- `www.googleadservices.com`
- `imasdk.googleapis.com`
- `2mdn.net`
- `googlesyndication.com`
- `googleadservices.com`

Policy tetap `REJECT` agar request gagal cepat. Paket tidak memakai `REJECT-DROP` untuk lapisan ini.

## Adblock dedup v3

Router menggunakan mode `lean` secara default:

```json
"ADBLOCK_DEDUP_MODE": "lean"
```

Mode ini mempertahankan:

- `ads_domain` MetaCubeX MRS
- `tracker-domain` MetaCubeX MRS
- `threat-tif-mini`
- threat fake/scam dan IP intelligence sesuai profil
- `app-ad-safe`
- explicit intrusive/game-ad suffixes
- tiga exact streaming-ad hosts
- explicit YouTube ad rules

Provider yang overlap seperti `hagezi-pro-mini`, `popup-ads`, `turtlecute-coverage`, dan `streaming-ad-safe` tidak dipasang pada router dalam mode lean. Ini mengurangi provider runtime dan file YAML. Untuk eksperimen coverage lama, set `ADBLOCK_DEDUP_MODE=full` sebelum menjalankan generator.

## Browser filter

`youtube_browser_filters.txt` menambahkan cosmetic filters untuk slot/promoted UI, request `api/stats/ads`, `pagead`, `ptracking`, exact `ads.youtube.com`, serta pruning konservatif `adPlacements`, `adSlots`, dan `playerAds`.

File tersebut tidak memblokir `googlevideo.com` maupun `static.doubleclick.net`.

DNS-level blocking tetap `off` secara default karena DNS tidak melihat path request dan tidak bisa membedakan iklan dari playback ketika keduanya berbagi host.

## Validasi

```bash
python3 youtube_adblock_audit.py --mode enhanced --dedup lean
python3 android_ruleprovider_audit.py
python3 validate_openclash_target.py --static-only \
  openclash_auto.yaml openclash_android.yaml \
  openclash_lite.yaml openclash_fresh_pool.yaml
```

Referensi kompatibilitas playback yang menjadi dasar keputusan untuk tidak memblokir `static.doubleclick.net` secara luas:

- HaGeZi issue #9446, 19 Maret 2026: https://github.com/hagezi/dns-blocklists/issues/9446
