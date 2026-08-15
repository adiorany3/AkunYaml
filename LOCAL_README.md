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
