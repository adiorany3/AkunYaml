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

## Laporan kesehatan

Setiap update yang berhasil menerbitkan `output/health_report.md` bersama manifest.
Ringkasannya mencatat mode update, akun yang dipertahankan, jumlah profil lulus
validasi core, umur sumber/feed gameblock, dan status adaptive guard saat packaging.
Laporan diterbitkan bersama profil melalui staging; update gagal tidak menggantinya.

Untuk membaca ulang kondisi laporan lokal tanpa jaringan atau membangun profil:

```bash
/Users/macbookpro/Documents/GitHub/AkunYaml/.venv/bin/python /Users/macbookpro/Documents/GitHub/AkunYaml/health_report.py
```

Perintah tersebut hanya menampilkan ringkasan terminal, tidak menulis file.
Manifest lama yang belum mencatat validasi ditandai tidak diketahui. Umur sumber
bukan bukti node aktif; status adaptive guard adalah snapshot saat packaging.
Tidak ada kredensial, URI akun, atau log koneksi yang dimasukkan ke ringkasan.

## Pemeriksaan dan pengembangan lokal

Semua perintah berikut dijalankan dengan interpreter proyek:
`/Users/macbookpro/Documents/GitHub/AkunYaml/.venv/bin/python`.

- **Jelaskan domain:** jalankan `/Users/macbookpro/Documents/GitHub/AkunYaml/rule_simulation.py --domain example.com --config /Users/macbookpro/Documents/GitHub/AkunYaml/local_build/gameblock/openclash_noproxy_gameblock.yaml`.
  Provider lokal termasuk MRS dibaca tanpa refresh. Hasil memuat rule, urutan,
  policy, dan nama provider. Exit 2 berarti tidak ada keputusan pasti karena
  rule/provider yang belum dapat dievaluasi; ini bukan pengganti engine runtime.
- **Preview perubahan:** setiap update sukses menyimpan `output/changes.json`.
  Untuk membandingkan dua folder paket sebelum publikasi, jalankan
  `/Users/macbookpro/Documents/GitHub/AkunYaml/release_tools.py preview /path/absolut/paket-lama /path/absolut/paket-baru`.
  Ringkasan mencatat jumlah rule ditambah/dihapus, perubahan urutan, DNS, akun,
  grup, dan definisi provider tanpa menampilkan kredensial. Ini bukan gate approval
  otomatis atau pemeriksaan perubahan isi provider yang definisinya tetap.
- **Ekspor publik opsional:** jalankan
  `/Users/macbookpro/Documents/GitHub/AkunYaml/release_tools.py export-public /Users/macbookpro/Documents/GitHub/AkunYaml/output /path/absolut/paket-publik`.
  Hanya blocklist adaptif yang tervalidasi sebagai domain dan manifest hash/jumlah
  yang diekspor. Profil berakun, log, dan manifest privat tidak ikut disalin.
  Folder tujuan harus terpisah; folder pengguna yang bukan ekspor terkelola tidak
  akan ditimpa. **Default output dan publikasi akun saat ini tidak berubah.**
  Paket output lengkap tetap harus diperlakukan sebagai privat; tidak ada auto-push.
- **Riwayat stabilitas opsional:** set `NODE_HISTORY_ENABLED=true` saat menjalankan
  update. Maksimal 20 sampel per node dan 10.000 node disimpan privat selama
  tujuh hari di `.runtime_cache/node_history.json`, identitas berupa hash.
  Setelah tiga sampel, rasio kegagalan menambah penalti ranking tanpa meloloskan
  node yang gagal tes saat ini. Median/jitter dan kegagalan beruntun tersedia
  melalui `/Users/macbookpro/Documents/GitHub/AkunYaml/node_history.py` atau
  `node_history.summary`. Ini riwayat handshake, bukan bukti akses internet
  penuh. Default nonaktif menjaga perilaku ranking saat ini; jangan jalankan
  generator bersamaan ketika riwayat diaktifkan.
- **Pemeriksaan satu pintu:** jalankan `/Users/macbookpro/Documents/GitHub/AkunYaml/check_local.py`.
  Semua test dalam `tests/` dan lint modul pengembangan diperiksa. Tambahkan
  `--full` untuk validasi integrasi gameblock pada salinan sementara dengan core
  Mihomo/Sing-box lokal; cache/provider/database lokal harus tersedia. Tidak ada
  refresh feed, perubahan profil terbit, pengaturan jaringan, atau auto-deploy.

## AI adblock opsional

AI tidak diperlukan untuk adblock utama. `AI_ADBLOCK_ENABLED` pada konfigurasi
proyek kini `false`; feed publisher, korelasi adaptif non-AI, allowlist, dan
validasi core tetap bekerja. Saat nonaktif, runner tidak menjalankan klasifikasi
AI dan generator tidak membaca cache blocklist AI lama. Cache/kunci tidak dihapus.
Profil yang sudah diterbitkan tidak berubah sampai dibangun ulang.

Untuk mengaktifkan kembali secara sadar, ubah `AI_ADBLOCK_ENABLED` menjadi `true`
di `/Users/macbookpro/Documents/GitHub/AkunYaml/local_config.json` dan siapkan
endpoint/model/kunci privat. AI hanya pelengkap; kegagalan klasifikasi ditangani
fail-open. Pengaturan grup routing layanan AI seperti `AI_TEST_URL` berbeda dari
AI adblock dan tidak dinonaktifkan oleh perubahan ini.

## Analisis adaptif adblock/malware

Update online kini mengorelasikan daftar langsung dari publisher berbeda.
Host yang muncul pada minimal dua publisher dalam kategori yang sama masuk
overlay blokir exact-host. Ini bukan pembuktian independen: publisher bisa
memakai sumber dasar yang sama. Allowlist dan pengecualian DIRECT di baseline
dipertahankan; satu sumber/tebakan AI tidak cukup untuk auto-block overlay.

```bash
bash /Users/macbookpro/Documents/GitHub/AkunYaml/update_all.sh --security-only
```

Perintah itu memperbarui analisis dan feed keamanan tanpa refresh akun/API AI.
Hasil diterapkan sebelum validasi ke semua profil di `output/`, termasuk
Sing-box. Laporan ada di `output/security/`. Bukti overlay berlaku 24 jam:
build offline setelah kedaluwarsa tidak memasukkannya. Profil yang sudah
terpasang di device tidak dapat mencabut aturan sendiri: deploy hasil baru.
Aturan feed/baseline biasa tetap berlaku terpisah dari overlay adaptif.

Ini tahap awal korelasi feed, **bukan mesin penelusuran berita atau deteksi
zero-day mandiri**. Tidak mengeksekusi sampel malware, memindai target, atau
mengirim riwayat browsing ke luar. Belum ada scheduler/auto-push/auto-deploy.
URLhaus/ThreatFox berautentikasi belum diintegrasikan. Blokir domain tidak
menggantikan patch, segmentasi LAN, firewall, dan endpoint protection.

## Tambah banyak game dan impor log lokal

Edit `/Users/macbookpro/Documents/GitHub/AkunYaml/gameblock_policy/manual_domains.txt`:
satu domain atau URL HTTP/HTTPS per baris. Daftar ini adalah persetujuan blokir
seluruh subdomain; tidak perlu mengedit YAML besar. Duplikat dihapus saat build.
Kemudian jalankan `bash /Users/macbookpro/Documents/GitHub/AkunYaml/update_all.sh --offline`
(atau tanpa `--offline` untuk refresh feed). Daftar manual melengkapi feed kategori
game, bukan menggantikannya. Entri salah membatalkan build agar kesalahan terlihat.

Untuk menemukan kandidat dari ekspor koneksi OpenClash/Mihomo lokal:

```bash
/Users/macbookpro/Documents/GitHub/AkunYaml/.venv/bin/python /Users/macbookpro/Documents/GitHub/AkunYaml/game_domain_policy.py /path/absolut/connections.json
```

Mendukung snapshot JSON `connections[].metadata.host`, JSONL dengan `metadata.host`,
dan log teks tujuan `--> host:port`. Batas input 20 MiB. Laporan privat ada di
`.runtime_cache/game_candidates.json`, bukan di GitHub/output. Tidak menyimpan
IP perangkat atau isi baris log. Tidak ada upload atau panggilan AI.
Kemunculan host bukan bukti game: tinjau kandidat, lalu salin hanya domain game
yang disetujui ke `manual_domains.txt`. Domain CDN/login/payment bersama jangan
diblokir sembarangan. `allow_domains.txt` mengecualikan kandidat dari review dan
menolak konflik daftar manual; **tidak membuat aturan DIRECT** atau mengalahkan
feed keamanan. Belum membaca log router otomatis dan belum mendukung semua format.

## Hasil

### Impor OpenClash OpenWrt melalui URL

Gunakan `output/openclash/subscription/openclash_auto.yaml` untuk konfigurasi
lengkap berakun. Varian ini mengubah provider lokal menjadi HTTP agar OpenClash
dapat mengunduh dependensinya, bukan mengharapkan folder pendamping terpasang.
URL setelah seluruh hasil di-commit/push ke branch `main`:

```text
https://raw.githubusercontent.com/adiorany3/AkunYaml/main/output/openclash/subscription/openclash_auto.yaml
```

Pada OpenClash, tambahkan URL itu sebagai subscription konfigurasi, unduh,
pilih profil, dan gunakan core **Meta/Mihomo**, bukan core Clash lama.
Untuk noproxy/gameblock, gunakan varian `subscription`, bukan folder `gameblock`:

```text
https://raw.githubusercontent.com/adiorany3/AkunYaml/main/output/openclash/subscription/openclash_noproxy_gameblock.yaml
```

Gameblock OpenClash mengikuti struktur HerYaml: akun dari generator lokal,
grup `MANUAL` bertipe `select` berisi `DIRECT` sebagai pilihan pertama lalu akun,
dan `MATCH,MANUAL`. Default tetap direct, akun opsional dipilih secara manual.
`store-selected` dimatikan agar pilihan proxy lama tidak pulih saat impor baru.
Varian direct/adblock biasa tetap memakai `DIRECT-ONLY` tanpa akun.
Jika versi OpenClash masih menolak daftar akun kosong, kirim error lengkap;
jangan menambahkan akun dummy yang berpotensi mengganggu routing.
Target lokal proyek: OpenClash v0.47.156 + Mihomo alpha-ge183c58. Versi perangkat
lain perlu diperiksa jika ada error. Provider MRS memerlukan dukungan core yang
sesuai; router harus dapat mengakses GitHub Raw. Repository privat tidak dapat
dibaca anonim oleh URL ini. Jangan menaruh token GitHub di URL publik.

Untuk hanya mengambil akun ke konfigurasi sendiri, gunakan
`output/akun/openclash_proxy_provider.yaml` sebagai **proxy-provider**, bukan
sebagai konfigurasi lengkap. `akun.txt` adalah daftar URI dan bukan YAML lengkap.
Daftar URL varian lengkap ada di `output/openclash/subscription/urls.json`.
File dalam `openclash/proxy/`, `direct/`, `gameblock/` tetap untuk pemasangan
folder lengkap secara manual. Update tidak otomatis push ke GitHub.

Lokasi utama: `/Users/macbookpro/Documents/GitHub/AkunYaml/output/`

| Folder | Isi |
|---|---|
| `akun/` | Daftar akun hasil generator |
| `openclash/proxy/` | Auto, Android, lite, fresh pool |
| `openclash/direct/` | Adblock tanpa proxy |
| `openclash/gameblock/` | Adblock + blokir game, DIRECT default + akun MANUAL opsional |
| `sing-box/` | Android berakun dan direct/adblock |
| `mihomo-mac/proxy/`, `direct/`, `gameblock/` | Profil Mihomo untuk Mac |

Salin **folder profil beserta `rule_providers/`**, bukan YAML saja. OpenClash
ditujukan untuk OpenWrt; Mac memakai Mihomo dengan system proxy HTTP/SOCKS
`127.0.0.1:7890`, bukan TUN otomatis. Aktifkan satu profil Mac saja.
**Sing-box gameblock DIRECT tersedia setelah update berikutnya** melalui
`output/sing-box/singbox_direct_gameblock.json`, dengan kebijakan lokal yang sama
serta validasi core. Aturan yang belum bisa diterjemahkan membatalkan publikasi,
bukan dilewati diam-diam.

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
Semua profil OpenClash/Mihomo dan Sing-box diperiksa core lokal sebelum
publikasi. Jika katalog URL/format feed berubah atau cache berasal dari versi
lama yang belum mencatat format, jalankan refresh online sekali sebelum offline.
Cache tidak boleh dianggap cocok hanya karena nama file dan hash-nya valid.
`local_build/`, `.runtime_cache/independent_gameblock/`, serta profil di root
masih diperlukan sebagai hasil antara/cache. Jangan hapus sumber aturan,
`.local_bin/`, atau cache bila membutuhkan build offline. Dokumen versi lama
merupakan referensi historis, bukan panduan menjalankan update saat ini.

## Publikasi hasil ke GitHub

`local_build/` dan `output/` dilacak Git, termasuk akun/profil proxy sesuai
persetujuan pemilik. **Repository publik mengekspos kredensial proxy**; siapa pun
yang dapat membaca repository dapat menyalinnya. Permission lokal `600`/`700`
tidak melindungi file yang sudah dipublikasikan. `.secrets/`, cache internal,
database validator, backup dan staging tetap diabaikan Git.

Setelah update berhasil, tinjau hasil lalu commit/push:

```bash
cd /Users/macbookpro/Documents/GitHub/AkunYaml
git add local_build output
git commit -m "Update generated device profiles"
git push origin HEAD
```

Perintah update tidak otomatis melakukan commit/push. Publikasi pertama juga
memerlukan perubahan `.gitignore` agar hasil berikutnya tetap terlacak.
URL Raw YAML saja tidak memasang provider `type: file` secara otomatis: salin
folder profil lengkap beserta `rule_providers/` ke direktori kerja core pada
setiap device. Manifest mencatat waktu sumber, bukan jaminan akun masih aktif.

## Pengujian

Jika runner mengembalikan `exit 3`, node baru tidak memenuhi syarat minimum.
Update terpadu kini melanjutkan pembaruan keamanan memakai akun/profil lama,
tetap memvalidasi seluruh hasil, dan mencatat `account_refresh: retained-old`
di manifest. Ini bukan keberhasilan refresh akun. Profil lama hilang/tidak valid
atau kegagalan tahap lain tetap membatalkan publikasi.

```bash
cd /Users/macbookpro/Documents/GitHub/AkunYaml
.venv/bin/python -m pytest tests -q
```

Validasi sintaks tidak membuktikan semua akun aktif atau semua aplikasi bebas
false positive. Periksa profil pada perangkat target sebelum penggunaan rutin.