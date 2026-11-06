# AkunYaml

Generator lokal akun, profil OpenClash/Mihomo, Sing-box, adblock, dan gameblock.
Tidak membutuhkan Hermes. Gunakan **satu perintah** dan ambil hasil di **output/**.

## Pemakaian

Update akun dan feed melalui internet, lalu bangun semua hasil:

```bash
bash /Users/macbookpro/Documents/GitHub/AkunYaml/update_all.sh
```

Bangun ulang sumber/cache lokal tanpa refresh:

```bash
bash /Users/macbookpro/Documents/GitHub/AkunYaml/update_all.sh --offline
```

Prasyarat: Python dan dependensi `requirements.txt` sudah terpasang; validator
Mihomo/Sing-box lokal tersedia. Skrip memilih `.venv/bin/python`, atau interpreter
dari `PYTHON`. Tidak ada instalasi pip, Git pull/push, atau scheduler otomatis.
Runner online dapat mengunduh core dan memakai AI jika diaktifkan.
Jangan menjalankan beberapa refresh bersamaan.

## Hasil

Lokasi utama: `/Users/macbookpro/Documents/GitHub/AkunYaml/output/`

| Folder | Isi |
|---|---|
| `akun/` | Daftar akun hasil generator |
| `openclash/proxy/` | Auto, Android, lite, fresh pool |
| `openclash/direct/` | Adblock tanpa proxy |
| `openclash/gameblock/` | Adblock + blokir game tanpa proxy |
| `sing-box/` | Android berakun dan direct/adblock |
| `mihomo-mac/proxy/`, `direct/`, `gameblock/` | Profil Mihomo untuk Mac |

Salin **folder profil beserta `rule_providers/`**, bukan YAML saja. OpenClash
ditujukan untuk OpenWrt; Mac memakai Mihomo dengan system proxy HTTP/SOCKS
`127.0.0.1:7890`, bukan TUN otomatis. Aktifkan satu profil Mac saja.
**Sing-box gameblock belum tersedia.**

`output/manifest.json` mencatat mode, waktu sumber, dan hash. Waktu packaging
bukan bukti akun aktif. Jika satu tahap gagal/parsial, hasil terpadu lama tidak
diganti; file internal di root dapat sudah berubah. Mode offline hanya memakai
snapshot, dan validator masih dapat membutuhkan database jika belum tersedia.

## Konfigurasi yang perlu dikenali

- `local_config.json`: pengaturan runner akun dan AI.
- `akun_manual.txt`: input akun manual, bukan output.
- `.secrets/ai_adblock.key`: JSON privat dengan `api_key`, `base_url`, dan `model`;
  permission `600`. Endpoint/model privat diprioritaskan. Environment
  `AI_ADBLOCK_API_KEY` dapat mengganti key. Format key polos lama masih didukung.
- `gameblock_policy/sources.json`: katalog 14 feed independen.
- `gameblock_policy/baseline/`: aturan khusus dan pengecualian lokal.

Feed gameblock/adblock diperbarui langsung dari HaGeZi, ABPindo, anti-AD,
Chocolate4U, dan MetaCubeX, bukan dari hasil jadi HerYaml. Baseline awal berasal
dari [HerYaml](https://github.com/adiorany3/HerYaml); kebijakan khusus tetap
dipelihara lokal. Gameblock memblokir game itu sendiri, termasuk blokir luas
`msn.com` dan `yandex.com` dari baseline. Tidak menjamin semua iklan/game terblokir.

## Struktur internal

`update_all.sh` → `unified_update.py` menjalankan:
1. `local_runner.py`: refresh profil berakun (dilewati saat offline).
2. `local_update.py`: bangun profil direct.
3. `independent_gameblock.py`: bangun gameblock dari kebijakan dan feed/cache.
4. Packaging serta validasi varian Mac ke `output/`.

`build_support.py` menyediakan unduhan, validasi, dan publikasi bertahap.
`local_build/`, `.runtime_cache/independent_gameblock/`, serta profil di root
masih diperlukan sebagai hasil antara/cache. Jangan hapus sumber aturan,
`.local_bin/`, atau cache bila membutuhkan build offline. Dokumen versi lama
merupakan referensi historis, bukan panduan menjalankan update saat ini.

Output mengandung akun: diabaikan Git, file `600`, direktori `700`.
Jangan unggah `.secrets/` atau `output/` ke publik.

## Pengujian

```bash
cd /Users/macbookpro/Documents/GitHub/AkunYaml
.venv/bin/python -m pytest tests -q
```

Validasi sintaks tidak membuktikan semua akun aktif atau semua aplikasi bebas
false positive. Periksa profil pada perangkat target sebelum penggunaan rutin.