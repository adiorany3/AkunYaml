# YouTube Ad Blocking

Mode default paket ini adalah `balanced + enhanced`.

## Strategi v2.7

Konfigurasi memakai dua lapisan agar pemblokiran lebih kuat tanpa mengorbankan playback.

### 1. Router / Mihomo

Rule router memblokir endpoint iklan yang dapat dipisahkan dari media utama:

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

`REJECT` dipakai agar koneksi iklan gagal cepat dan tidak menunggu timeout panjang.

### 2. Playback compatibility guard

Host berikut sengaja diizinkan sebelum blocklist iklan umum:

- `static.doubleclick.net`
- `jnn-pa.googleapis.com`

`static.doubleclick.net` dapat dibutuhkan oleh validasi playback YouTube. Jangan menggantinya dengan `DOMAIN-SUFFIX,doubleclick.net,REJECT`.

Domain media utama berikut juga selalu dijaga agar tidak terkena blocklist umum:

- `youtube.com`
- `youtu.be`
- `youtube-nocookie.com`
- `googlevideo.com`
- `ytimg.com`
- `youtubei.googleapis.com`
- `youtube.googleapis.com`
- `ggpht.com`

`googlevideo.com` tidak boleh diberi policy `REJECT` karena video utama dan sebagian iklan dapat memakai infrastruktur media yang sama.

### 3. Browser filter

File `youtube_browser_filters.txt` menangani bagian yang tidak dapat dibedakan di tingkat DNS/router, termasuk:

- elemen iklan feed dan player
- request `api/stats/ads`
- request `pagead`
- request `ptracking`
- pruning konservatif `adPlacements`, `adSlots`, dan `playerAds` pada respons awal halaman

Gunakan file ini sebagai custom filter pada content blocker yang kompatibel dengan sintaks uBlock Origin jika ingin hasil terbaik di browser.

## Profil

Default `local_config.json`:

```json
"ADBLOCK_PROFILE": "balanced",
"ADBLOCK_DNS_MODE": "off",
"YOUTUBE_ADBLOCK_MODE": "enhanced"
```

`ADBLOCK_DNS_MODE` tetap `off`. Rule routing lebih aman untuk YouTube karena DNS tidak dapat membedakan request berdasarkan path dan tidak dapat membedakan iklan dari media jika host delivery sama.

## Validasi

Jalankan:

```bash
python3 youtube_adblock_audit.py --mode enhanced
```

Audit memeriksa bahwa:

- provider ad dan tracker tersedia
- endpoint iklan utama tetap diblokir
- `googlevideo.com` tidak diblokir
- `static.doubleclick.net` tidak diblokir
- rule compatibility berada sebelum blocklist umum
- browser filter tidak memblokir media utama
