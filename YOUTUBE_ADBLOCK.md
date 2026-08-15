# YouTube Ad Blocking

Mode default paket ini adalah `balanced + enhanced`.

Lapisan yang dipakai:

1. `ads_domain.mrs` dari MetaCubeX untuk domain iklan umum.
2. `tracker.mrs` dari MetaCubeX untuk tracker.
3. Rule endpoint iklan Google/YouTube terpisah seperti DoubleClick, Google Syndication, 2mdn, dan IMA SDK.
4. Playback guard untuk `youtube.com`, `googlevideo.com`, `ytimg.com`, dan domain playback lain agar tidak terkena blokir umum.
5. `youtube_browser_filters.txt` untuk elemen dan request path yang tidak bisa dibedakan oleh router hanya dari nama domain.

`googlevideo.com` sengaja tidak pernah diberi policy `REJECT` karena domain tersebut membawa media utama YouTube.

## Mac

Refresh normal:

```bash
./mac_refresh_accounts.sh
```

Pipeline sekarang juga menjalankan:

```bash
python3 youtube_adblock_audit.py --mode enhanced
```

Audit akan gagal jika domain playback ikut diblokir atau lapisan MRS utama hilang.

## Profil

Default `local_config.json`:

```json
"ADBLOCK_PROFILE": "balanced",
"ADBLOCK_DNS_MODE": "off",
"YOUTUBE_ADBLOCK_MODE": "enhanced"
```

`ADBLOCK_DNS_MODE` tetap `off` untuk mengurangi risiko video gagal diputar. Gunakan browser/content blocker bersama `youtube_browser_filters.txt` jika ingin hasil terbaik di browser.
