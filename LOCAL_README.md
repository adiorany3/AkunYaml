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


## v2.2 OpenClash Safe

Jika OpenClash menunjukkan:

```text
Finished initial GeoSite rule category-ads-all => REJECT
invalid domain
```

runner tidak lagi memasukkan HaGeZi TXT secara langsung sebagai Mihomo
`rule-provider behavior: domain`.

Default security sekarang hanya:

```text
GEOSITE,category-ads-all,REJECT
RULE-SET,tracker-domain,REJECT
```

`tracker-domain` menggunakan `tracker.mrs` resmi MetaCubeX.

Perbaiki YAML lama tanpa mencari akun ulang:

```bash
python fix_invalid_domain.py
```

Lalu unggah/subscription ulang `openclash_auto.yaml`.

Cek router:

```sh
sh diagnose_invalid_domain.sh AkunBaru
```

Bagian `Legacy providers that must be gone` harus menampilkan:

```text
tidak ditemukan
```


## v2.3 Reference-Locked

v2.3 membandingkan langsung known-good `ConvertYAML/openclash_auto.yaml`
dengan failing `AkunYaml/openclash_auto.yaml`.

Output `openclash_auto.yaml` sekarang dibangun dengan aturan:

- `proxies` dan `proxy-groups`: hasil pencarian terbaru;
- `profile`, `sniffer`, `dns`, `rule-providers`, `rules`: dari baseline
  ConvertYAML yang sudah terbukti berjalan;
- tidak ada `tracker-domain`;
- tidak ada injeksi langsung `GEOSITE,category-ads-all`;
- adblock menggunakan `RULE-SET,ads_domain,REJECT`;
- YouTube menggunakan `RULE-SET,youtube_domain,YOUTUBE`;
- rule `MANUAL` Indonesia dipulihkan;
- `global-client-fingerprint` global dibuang karena deprecated.

Perbaiki file lama tanpa mencari akun ulang:

```bash
python fix_reference_locked.py
```

Generate baru:

```bash
python local_runner.py --config local_config.json
```

`openclash_auto_fixed.yaml` adalah hasil perbaikan langsung terhadap
AkunYaml yang sedang error ketika paket v2.3 dibuat.


## v2.4 Exact OpenClash

v2.4 tidak lagi menganggap validasi Mihomo di Mac sebagai keputusan final.

`openclash_exact_core_filter.sh` dijalankan di router dan menggunakan core
OpenClash yang benar-benar terpasang.

### 1. Tes URL GitHub langsung

```sh
sh openclash_exact_core_filter.sh test
```

Jika `AkunYaml` direct valid tetapi update LuCI gagal, berarti OpenClash
mengubah config saat subscription update.

### 2. Tangkap config sementara OpenClash

```sh
sh openclash_exact_core_filter.sh watch
```

Saat script menunggu, tekan Update `AkunBaru` di LuCI.

Jika `/tmp/yaml_sub_tmp_config.yaml` menjadi invalid, script otomatis
menyimpannya ke:

```text
/root/AkunBaru_CAPTURED_BAD.yaml
```

### 3. Exact node isolation

Script menguji setiap proxy satu per satu dengan core router.

Node yang ditolak core akan dihapus dari output:

```text
/root/openclash_auto_exact_filtered.yaml
```

Kemudian seluruh YAML difinal-test lagi.

Jika semua node lolos tetapi config tetap invalid, script mengisolasi
`dns`, `sniffer`, serta `rules/rule-providers`.

### Strict domain filter

Generator Mac juga sekarang:

- menormalisasi SNI/Host ke lowercase;
- menolak whitespace/wildcard/URL pada server, SNI, dan WS Host;
- menolak label DNS kosong atau malformed;
- membersihkan referensi proxy-group sesudah node dibuang.

Default `MAX_NODES` diturunkan ke 10 agar sama dengan skala output
known-good saat ini.
