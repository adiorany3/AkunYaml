# ConvertYAML Local Runner v2.0 Final

Versi ini menggantikan patch v1.1 sampai v1.5. Gunakan hanya file dari paket ini agar fixer lama tidak menimpa konfigurasi dengan pola yang berbeda.

## File utama

- `local_runner.py`: generate akun/YAML baru.
- `apply_existing.py`: sanitasi dan optimasi YAML yang sudah ada tanpa mencari akun ulang.
- `openclash_router_fix.sh`: audit dan fix konfigurasi aktif OpenClash di router.
- `local_config.json`: konfigurasi default.

## Perbaikan yang sudah digabung

- GitHub Actions tidak diperlukan.
- TLS Python/Conda memakai retry dan fallback `curl`, tanpa mematikan verifikasi SSL.
- Mihomo dan sing-box disiapkan otomatis.
- `global-client-fingerprint` global dibersihkan.
- Bug `GLOBAL -> MANUAL` pada lite YAML diperbaiki.
- `GEOSITE,tracker` tidak digunakan.
- Tracker memakai `tracker.mrs` resmi MetaCubeX.
- HTTP rule-provider selalu memakai path relatif.
- Dangling `RULE-SET` dan referensi proxy-group invalid dibersihkan.
- DNS adblock default `off` untuk kompatibilitas OpenClash. Pemblokiran tetap aktif di `rules`.
- `GEOSITE,category-ads-all,REJECT` tetap digunakan.
- Malware/phishing: HaGeZi TIF Mini.
- Pop-up ads: HaGeZi Pop-Up Ads.
- Strict mode menambah HaGeZi Pro Mini.
- YouTube tidak memblokir `googlevideo.com` secara kasar.
- Filter browser YouTube dibuat terpisah.
- Validator router menggunakan `SAFE_PATHS=/usr/share/openclash:/etc/ssl`.

## macOS / Linux

```bash
chmod +x run_local_unix.sh
./run_local_unix.sh
```

Atau:

```bash
python local_runner.py --config local_config.json
```

Tes GitHub/TLS:

```bash
python local_runner.py --network-test
```

## YAML yang sudah ada

```bash
python apply_existing.py
```

Mode ketat:

```bash
python apply_existing.py --profile strict
```

DNS adblock opt-in:

```bash
python apply_existing.py --dns-adblock geosite
```

Default tetap `off` karena rule-level blocking lebih portable pada OpenClash.

## Router OpenClash

Upload `openclash_router_fix.sh` ke `/tmp`, lalu:

```sh
chmod +x /tmp/openclash_router_fix.sh
sh /tmp/openclash_router_fix.sh
```

Fix pola lama:

```sh
sh /tmp/openclash_router_fix.sh --fix
```

Validasi menggunakan environment yang sesuai OpenClash modern:

```sh
SAFE_PATHS=/usr/share/openclash:/etc/ssl \
/etc/openclash/core/clash_meta -t -d /etc/openclash -f /etc/openclash/openclash_auto.yaml
```

## YouTube

Network-level blocker tidak bisa menjamin semua pre-roll/mid-roll YouTube hilang tanpa risiko merusak playback. Runner menjaga domain media utama tetap routable dan membuat `youtube_browser_filters.txt` untuk blocker browser.

Jangan menambahkan `googlevideo.com` ke `REJECT`.

## Hapus penggunaan file lama

Jangan gunakan lagi:

- `repair_existing_outputs.py`
- `apply_security_existing.py`
- `apply_youtube_optimized.py`
- `fix_openclash_v15.py`
- `openclash_active_fix.sh`
- `openclash_active_fix_v2.sh`

Semua fungsi pentingnya sudah digabung ke v2.0.
