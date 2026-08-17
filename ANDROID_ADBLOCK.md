# Android Adblock and Threat Protection

Paket ini menyediakan `openclash_android.yaml` untuk client Android berbasis Clash Meta/Mihomo yang menerima konfigurasi YAML.

## Tujuan

- Memblokir domain iklan yang mengganggu.
- Memblokir tracker umum.
- Memblokir domain malware, phishing/scam, dan cryptominer.
- Menjaga YouTube tetap dapat memutar video dengan normal.
- Menjaga kompatibilitas dengan build Android yang tidak menerima rule-provider MRS.
- Memperbarui rule-provider secara otomatis tanpa regenerate YAML setiap kali daftar upstream berubah.

## Mode balanced

Mode default adalah `balanced`.

Android menggunakan provider berikut:

- `ads_domain`: Chocolate4U `category-ads-all.yaml`.
- `tracker-domain`: MetaCubeX tracker YAML classical.
- `threat-malware`: domain malware aktif.
- `threat-phishing`: domain phishing dan scam.
- `threat-cryptominers`: domain cryptominer.

Provider memakai `type: http` dan interval update default 43200 detik atau 12 jam.

`openclash_android.yaml` tetap memakai:

```yaml
mode: rule
```

Rule terakhir tetap:

```yaml
MATCH,GLOBAL
```

Dengan susunan ini, trafik yang tidak diblokir tetap mengikuti group `GLOBAL`.

## Mode strict

Mode `strict` menambahkan `privacy-extra` dari Blackmatrix7. Mode ini dapat memblokir tracker tambahan, tetapi risiko false positive lebih tinggi.

Untuk menerapkan mode strict ke file yang sudah ada:

```bash
python apply_existing.py --static-only --profile strict
```

Jika exact Mihomo core tersedia:

```bash
python apply_existing.py \
  --profile strict \
  --core /path/ke/mihomo-alpha-ge183c58
```

Untuk kembali ke balanced:

```bash
python apply_existing.py --static-only --profile balanced
```

## Allowlist

Jika aplikasi atau situs sah ikut terblokir, tambahkan domain ke:

```text
adblock_allowlist.txt
```

Satu domain per baris. Jangan masukkan URL lengkap.

Contoh:

```text
example.com
login.example.com
```

Allowlist dipasang sebelum blocklist sehingga domain tersebut mendapat prioritas `DIRECT`.

## Kompatibilitas Android

Profil Android sengaja tidak memakai `.mrs` untuk provider keamanan. Provider memakai YAML agar tetap kompatibel dengan build Clash Meta for Android yang lebih lama.

Sniffer Android hanya memakai HTTP dan TLS. QUIC sniffer tidak ditambahkan karena beberapa build Android menolak key tersebut.

## Catatan YouTube

Pemblokiran pada level domain tidak dapat membedakan seluruh iklan YouTube dari trafik video biasa karena sebagian infrastruktur dapat dipakai bersama. Karena itu konfigurasi menjaga domain playback seperti `googlevideo.com` tetap tidak diblokir.

File `youtube_browser_filters.txt` disediakan untuk browser/content blocker yang mendukung filter kosmetik dan request-level. Jangan memasukkan file itu sebagai Clash rule-provider.

## v3.3 Popup & game ads
Profil `child-safe` juga memuat fallback lokal untuk jaringan popup/popunder dan SDK iklan game/mobile. Rule memakai `DOMAIN-SUFFIX` dan tidak menambah HTTP provider baru. Jika game bergantung pada rewarded ads, tombol reward dapat menjadi tidak tersedia. Ini lebih aman daripada memblokir CDN atau server asset game secara luas.
