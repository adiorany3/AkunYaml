# ConvertYAML Local Runner

Runner ini menggantikan fungsi GitHub Actions untuk menjalankan pipeline ConvertYAML langsung di komputer.

## Apa yang dilakukan

- Mengunduh `generate_yaml.py`, `sumberyaml_core.py`, dan `requirements.txt` bila belum ada.
- Menyiapkan Mihomo terbaru sesuai Windows, macOS, atau Linux.
- Menyiapkan sing-box terbaru untuk validasi NekoBox.
- Mengambil sumber subscription publik yang didefinisikan oleh ConvertYAML.
- Menyaring kandidat.
- Melakukan tes Mihomo.
- Melakukan tes sing-box/NekoBox.
- Membuat `akun.txt`, YAML OpenClash, laporan CSV, dan laporan kualitas.
- Memvalidasi YAML hasil dengan Mihomo.
- Tidak memakai GitHub Actions.
- Tidak melakukan commit atau push Git.

## Syarat

- Python 3.10 atau lebih baru.
- Koneksi internet.
- Windows 10/11, macOS, atau Linux.
- Arsitektur x86_64/AMD64 atau ARM64.

## Cara paling mudah di Windows

1. Ekstrak ZIP ini.
2. Buka folder hasil ekstrak.
3. Klik dua kali `run_local_windows.bat`.
4. Tunggu sampai terminal menampilkan `Selesai`.
5. Ambil hasil utama:
   - `akun.txt`
   - `openclash_auto.yaml`
   - `openclash_android.yaml`
   - `openclash_lite.yaml`
   - `openclash_auto_report.csv`
   - `urltest_report.csv`
   - `nekobox_test_report.csv`

## macOS / Linux

Buka Terminal di folder ini:

```bash
chmod +x run_local_unix.sh
./run_local_unix.sh
```

## Menjalankan manual

```bash
python local_runner.py --max-nodes 20 --min-nodes 10
```

Contoh mencari pool lebih besar:

```bash
python local_runner.py \
  --max-nodes 20 \
  --candidate-min 3000 \
  --urltest-pool 100 \
  --nekobox-pool 40
```

Jika hanya ingin validasi Mihomo dan ingin melewati sing-box:

```bash
python local_runner.py --no-nekobox
```

Jika ingin mengizinkan network selain WebSocket:

```bash
python local_runner.py --no-ws-only
```

## Menambah sumber subscription

Edit:

```text
subscription_links.txt
```

Format:

```text
https://contoh-domain.example/subscription.txt
https://contoh-domain.example/nodes.txt
```

Gunakan hanya sumber publik atau sumber yang memang Anda berhak gunakan.

## Menambah node manual

Edit:

```text
manual_nodes.txt
```

Satu URI per baris:

```text
vless://...
vmess://...
trojan://...
ss://...
```

## Mengubah parameter

Anda dapat mengedit `local_config.json`.

Contoh:

```json
{
  "CANDIDATE_MIN": "2500",
  "URLTEST_POOL_NODES": "100",
  "NEKOBOX_POOL_NODES": "40",
  "URL_TEST_TIMEOUT_MS": "7000",
  "NEKOBOX_TEST_TIMEOUT_MS": "9000",
  "ATTEMPTS": "3",
  "REQUIRE_SUCCESSES": "2"
}
```

Lalu:

```bash
python local_runner.py --config local_config.json
```

## Update core dan binary

Unduh ulang core ConvertYAML:

```bash
python local_runner.py --refresh-core
```

Unduh ulang Mihomo dan sing-box:

```bash
python local_runner.py --refresh-binaries
```

Keduanya sekaligus:

```bash
python local_runner.py --refresh-core --refresh-binaries
```

## Catatan

Runner ini tidak memerlukan GitHub Actions. Namun, pencarian node tetap membutuhkan internet karena sumber subscription dan tes koneksi berada di internet.

Jika jumlah node yang lolos terlalu sedikit, naikkan `CANDIDATE_MIN`, `URLTEST_POOL_NODES`, atau timeout. Jangan langsung menaikkan semua parameter terlalu tinggi karena waktu pengujian dan penggunaan bandwidth ikut meningkat.


## Jika openclash_lite.yaml gagal karena MANUAL not found

Versi runner ini sudah memperbaiki kasus tersebut secara otomatis.

Jika hasil YAML lama sudah terbentuk dan Anda tidak ingin melakukan pencarian ulang, jalankan:

```bash
.venv/bin/python repair_existing_outputs.py
```

Pada Windows:

```bat
.venv\Scripts\python.exe repair_existing_outputs.py
```

Script akan:
- membuat backup `.yaml.bak`;
- menghapus `global-client-fingerprint` tingkat global;
- menghapus referensi grup yang tidak benar-benar ada;
- mengalihkan rule `MANUAL` ke `GLOBAL` jika grup MANUAL memang tidak tersedia;
- menjalankan validasi Mihomo ulang.


## Adblock dan perlindungan malware

Versi ini menambahkan profil keamanan pada semua YAML yang dihasilkan.

Default:

```json
"ADBLOCK_PROFILE": "balanced"
```

Profil tersedia:

- `off`: tidak menambahkan adblock/security rules.
- `balanced`: memblokir iklan, tracker, pop-up ads, malware, phishing, scam, dan cryptojacking dengan beban yang lebih masuk akal untuk router.
- `strict`: semua perlindungan `balanced` ditambah AdvertisingLite/AWAvenue. Potensi false positive lebih tinggi.

Jalankan profil strict:

```bash
.venv/bin/python local_runner.py --config local_config.json --adblock-profile strict
```

Jika sebuah domain normal ikut terblokir, masukkan domain tersebut ke:

```text
adblock_allowlist.txt
```

Satu domain per baris, misalnya:

```text
example.com
api.example.com
```

Allowlist ditempatkan sebelum semua rule pemblokiran sehingga mendapat prioritas `DIRECT`.

Sumber yang digunakan oleh profil balanced:

- MetaCubeX geosite `category-ads-all`
- MetaCubeX geosite `tracker`
- HaGeZi Threat Intelligence Feed Mini
- HaGeZi Pop-Up Ads

Profil strict menambahkan AdvertisingLite dari blackmatrix7/AWAvenue ecosystem.


## YouTube Optimized v1.3

Default:

```json
{
  "YOUTUBE_ADBLOCK_MODE": "enhanced",
  "YOUTUBE_BROWSER_FILTER_FILE": "youtube_browser_filters.txt"
}
```

Mode tersedia:

- `off`: tidak menerapkan perlakuan khusus YouTube.
- `safe`: melindungi domain playback dari blokir jaringan yang terlalu agresif dan membuat cosmetic filter.
- `enhanced`: sama seperti `safe`, ditambah filter request untuk endpoint iklan terpisah dari CDN video.

Jalankan seluruh pipeline:

```bash
.venv/bin/python local_runner.py --config local_config.json --youtube-mode enhanced
```

Untuk YAML yang sudah ada tanpa mencari akun ulang:

```bash
.venv/bin/python apply_youtube_optimized.py --mode enhanced
```

Jika playback YouTube bermasalah:

```bash
.venv/bin/python apply_youtube_optimized.py --mode safe
```

Rollback:

```bash
.venv/bin/python apply_youtube_optimized.py --restore
```

### Filter browser

File berikut dibuat otomatis:

```text
youtube_browser_filters.txt
```

Import file tersebut ke bagian custom filters / My filters pada blocker browser yang mendukung sintaks uBlock Origin/AdGuard.

Runner sengaja tidak memblokir `googlevideo.com` pada level DNS. Domain tersebut dipakai untuk media utama, sehingga pemblokiran kasar dapat memutus playback.

Optimasi YouTube tidak menjamin semua pre-roll atau mid-roll hilang setiap saat. YouTube mengubah player dan delivery iklan secara berkala. Gunakan filter bawaan blocker browser yang selalu diperbarui bersama file custom ini.


## v1.4: Perbaikan SSL/TLS macOS + Conda

Jika muncul:

```text
ssl.SSLEOFError: [SSL: UNEXPECTED_EOF_WHILE_READING]
```

runner v1.4 tidak menonaktifkan verifikasi SSL. Urutannya:

1. Python `urllib` memakai verified `SSLContext`.
2. Jika `certifi` tersedia, CA bundle certifi ikut dimuat.
3. Request dicoba ulang beberapa kali.
4. Jika jalur TLS Python/Conda tetap gagal, runner memakai `curl` sistem dengan verifikasi TLS aktif.
5. Download ditulis ke file `.part` lalu dipindahkan setelah sukses agar file rusak tidak dianggap valid.
6. Jika Mihomo atau sing-box sudah ada di `PATH`, runner dapat memakai binary tersebut tanpa mengakses GitHub release API.

Tes koneksi:

```bash
python local_runner.py --network-test
```

Jalankan normal:

```bash
python local_runner.py
```

Jika ingin memasang binary dengan Homebrew secara terpisah, runner juga dapat mendeteksinya dari `PATH`. Tidak perlu mematikan SSL verification.

Jika jaringan menggunakan VPN, proxy HTTPS, antivirus TLS inspection, atau captive portal dan bahkan `curl` gagal, selesaikan masalah koneksi tersebut terlebih dahulu.


## v1.5 OpenClash GeoData Fix

Perbaikan ini dibuat untuk log OpenClash dengan pola:

```text
GEOSITE,tracker,REJECT ... list tracker not found in GeoSite.dat
Parse config error: invalid domain
```

Perubahan:
- `GEOSITE,tracker,REJECT` dihapus.
- Tracker tetap diblokir melalui `tracker-domain.mrs` resmi MetaCubeX.
- DNS blocking memakai `geosite:category-ads-all` saja.
- Wildcard YouTube yang sebelumnya dimasukkan ke `dns.nameserver-policy` dihapus.
- YouTube tetap dilindungi dari salah blokir melalui rule `DOMAIN-SUFFIX`.
- `global-client-fingerprint` global dibersihkan.
- Semua HTTP rule-provider dipastikan memiliki `path` relatif.

### Memperbaiki YAML yang sudah ada

Tidak perlu mencari akun ulang:

```bash
cd /Users/macbookpro/Downloads/ConvertYAML_Local_Runner
python fix_openclash_v15.py
```

Lalu upload/test ulang:

```text
openclash_auto.yaml
```

Backup otomatis:

```text
openclash_auto.yaml.pre-v15-openclash.bak
```

### Generate ulang

Untuk generasi berikutnya, gunakan `local_runner.py` v1.5:

```bash
python local_runner.py
```
