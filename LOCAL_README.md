# AkunYaml Target Package

Target paket ini:

- OpenClash: `v0.47.156`
- Mihomo Meta: `alpha-ge183c58`
- Mihomo revision: `e183c58`
- OpenWrt core path: `/etc/openclash/core/clash_meta`

Paket ini dikunci ke target di atas. Generator tidak lagi menganggap Mihomo terbaru sebagai validator yang setara.

## Perbaikan utama

1. `sumberyaml_core.py`
   - Memperbaiki regex delay `MS` yang sebelumnya mengandung control character tersembunyi.
   - Nama seperti `NODE-86MS` sekarang terbaca sebagai 86 ms dan dapat diranking dengan benar.

2. `generate_yaml.py`
   - Wajib memeriksa versi Mihomo sebelum generate.
   - Default `REQUIRE_EXACT_MIHOMO_CORE=true`.
   - Filter kompatibilitas node memakai core target yang sama.
   - Empat YAML final diuji lagi sebelum ditulis.
   - Final validation memeriksa struktur YAML, referensi proxy/group, rule-provider, rule policy, dan parser Mihomo.

3. `local_runner.py`
   - Tidak lagi menimpa source target dengan source remote.
   - Tidak lagi memakai Mihomo latest secara diam-diam untuk mode normal.
   - Mendeteksi core dari `--mihomo-path`, `MIHOMO_PATH`, `/etc/openclash/core/clash_meta`, `.local_bin/mihomo`, atau PATH.
   - Core selain `alpha-ge183c58` ditolak secara default.
   - Reference profile memakai snapshot lokal `reference_profile_v047156.yaml`.
   - Default adblock profile `balanced` mengaktifkan ads, tracker, dan threat protection pada router serta Android.
   - Android memakai rule-provider YAML agar tidak bergantung pada MRS.
   - Profil `strict` menambah HaGeZi PRO Mini + Pop-Up Ads pada router dan privacy list tambahan pada Android.
   - Provider diperbarui otomatis setiap 12 jam secara default.
   - DNS-level adblock tetap `off` untuk mengurangi false positive dan menjaga kompatibilitas.

4. `openclash_target.py`
   - Satu modul validasi target.
   - Cek exact revision Mihomo.
   - Cek duplicate proxy/group.
   - Cek dangling reference.
   - Cek proxy-group cycle.
   - Cek `RULE-SET` dan policy target.
   - Cek MRS provider.
   - Cek hidden control character.
   - Menjalankan `mihomo -t` untuk final parser test.

5. Router scripts
   - `openclash_router_fix.sh` sekarang memeriksa OpenClash `0.47.156` dan core `alpha-ge183c58` sebelum menyatakan config valid.
   - `openclash_exact_core_filter.sh` menolak proses jika exact target core tidak terdeteksi.

6. Utility lama
   - Fixer lama dipindahkan ke `legacy/`.
   - Jangan gunakan file dalam `legacy/` untuk target ini.

## File utama

- `local_runner.py`: generate dan validasi lengkap.
- `generate_yaml.py`: generator utama.
- `sumberyaml_core.py`: parser dan builder YAML.
- `openclash_target.py`: validator target.
- `validate_openclash_target.py`: validator CLI.
- `apply_existing.py`: perbaiki YAML yang sudah ada dengan rollback otomatis jika validasi gagal.
- `reference_profile_v047156.yaml`: baseline DNS, sniffer, provider, dan rules yang dipin lokal.
- `local_config.json`: konfigurasi default target.
- `openclash_router_fix.sh`: audit dan fix config pada router.
- `ANDROID_ADBLOCK.md`: panduan adblock dan threat protection Android.
- `SECURITY_OPTIMIZATION.md`: detail profil balanced/strict dan sumber provider.
- `adblock_provider_audit.py`: audit interval, URL, format provider, dan opsional cek upstream.
- `openclash_exact_core_filter.sh`: isolate proxy dengan exact core router.

## Generate di OpenWrt atau Linux

Pastikan exact core tersedia.

```sh
/etc/openclash/core/clash_meta -v
```

Output versi harus menunjukkan `alpha` dan revision `e183c58`.

Jalankan:

```sh
export MIHOMO_PATH=/etc/openclash/core/clash_meta
python3 local_runner.py --config local_config.json
```

Atau:

```sh
python3 local_runner.py \
  --config local_config.json \
  --mihomo-path /etc/openclash/core/clash_meta
```

## Generate di macOS atau Linux desktop

Binary exact `alpha-ge183c58` tidak dibundel karena binary berbeda untuk setiap OS dan arsitektur.

Set path core Anda:

```bash
export MIHOMO_PATH=/path/ke/mihomo-alpha-ge183c58
./run_local_unix.sh
```

Jika exact core tidak ada, runner berhenti dan tidak mengklaim hasil sebagai exact-target compatible.

`--allow-non-target-core` hanya untuk pengembangan. Jangan gunakan hasil mode itu sebagai validasi final router.

## Windows

Set environment variable `MIHOMO_PATH` ke binary exact target, lalu jalankan:

```bat
run_local_windows.bat
```

Atau:

```bat
python local_runner.py --config local_config.json --mihomo-path C:\path\mihomo.exe
```

## Validasi YAML tanpa regenerate

Validasi statis:

```bash
python validate_openclash_target.py --static-only
```

Validasi dengan exact core:

```bash
python validate_openclash_target.py \
  --core /etc/openclash/core/clash_meta
```

Default file yang diperiksa:

- `openclash_auto.yaml`
- `openclash_android.yaml`
- `openclash_lite.yaml`
- `openclash_fresh_pool.yaml`

## Perbaiki YAML yang sudah ada

Dengan exact core:

```bash
python apply_existing.py --core /etc/openclash/core/clash_meta
```

Hanya static check:

```bash
python apply_existing.py --static-only
```

Script membuat backup di `backup_target/`. Jika validasi gagal setelah perubahan, script otomatis rollback.


## Adblock multi-platform

Default tetap balanced:

```bash
python apply_existing.py --static-only --profile balanced
```

Untuk proteksi lebih agresif:

```bash
python apply_existing.py --static-only --profile strict
```

Android menggunakan `openclash_android.yaml`. Rule-provider Android memakai YAML dan akan memperbarui daftar dari upstream sesuai interval provider. Tambahkan false positive ke `adblock_allowlist.txt`.

## Audit router

Upload script ke router, lalu:

```sh
chmod +x /tmp/openclash_router_fix.sh
sh /tmp/openclash_router_fix.sh
```

Untuk memperbaiki pola lama yang sudah diketahui:

```sh
sh /tmp/openclash_router_fix.sh --fix
```

Script hanya menyatakan `CONFIG VALID` jika config parser lolos dan exact target check juga lolos.

## Exact proxy isolation

Di router:

```sh
sh openclash_exact_core_filter.sh test
```

Jika source gagal:

```sh
sh openclash_exact_core_filter.sh isolate
```

Script menguji proxy satu per satu menggunakan `/etc/openclash/core/clash_meta`.

## Reference profile

`REFERENCE_PROFILE_MODE` default adalah `local-pinned`.

File baseline:

```text
reference_profile_v047156.yaml
```

Generator tidak mengambil DNS, sniffer, providers, atau rules dari repo remote dalam mode default. Ini mencegah perubahan eksternal mengubah hasil tanpa perubahan pada paket lokal.

## Catatan output

Paket tidak menyertakan binary Mihomo target. Gunakan core milik router atau binary yang sesuai OS/arsitektur Anda.

Keempat YAML bawaan sudah melewati static validator paket ini. Exact Mihomo parser test harus dilakukan menggunakan binary `alpha-ge183c58` pada perangkat Anda.
