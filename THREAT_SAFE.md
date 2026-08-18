# Threat-Safe v3.6 Precision

Profil `threat-safe` difokuskan pada pemblokiran ancaman dengan urutan yang lebih presisi dan mudah diaudit.

## Urutan proteksi

1. LAN/private bypass.
2. AI/service compatibility guard.
3. `adblock_allowlist.txt`.
4. YouTube/streaming compatibility guard.
5. Malware aktif.
6. Phishing/scam.
7. Cryptominer.
8. Fake/scam intelligence.
9. TIF mini sebagai safety net yang lebih luas.
10. Malicious IP pada Auto/Fresh Pool.
11. Ads dan tracker.
12. Rule aplikasi/routing lain.

Allowlist selalu berada sebelum blocklist. Domain yang perlu dipulihkan karena false positive cukup ditambahkan satu per baris ke `adblock_allowlist.txt`.

## Pemblokiran kategori berisiko

`threat-safe` menggunakan resolver kategori keluarga sebagai lapisan DNS tambahan. Pendekatan ini menjaga daftar kategori berukuran besar tetap di sisi resolver dan tidak memasukkan daftar domain kategori tersebut ke YAML OpenClash. Fallback DNS menggunakan kebijakan yang sama agar tidak menjadi jalur bypass.

Gunakan `THREAT_SAFE_FAMILY_DNS=true` untuk mempertahankan lapisan ini. Nilai default pada paket v3.6 adalah `true`.

## Malware precision layer

Router sekarang memakai provider malware, phishing, dan cryptominer yang terpisah sebelum TIF mini. Pemisahan ini memberi tiga keuntungan:

- audit lebih jelas;
- diagnosis false positive lebih mudah;
- kategori ancaman aktif mendapat prioritas sebelum feed threat intelligence yang lebih luas.

TIF mini tetap dipertahankan sebagai safety net. Auto dan Fresh Pool juga mempertahankan TIF IP dengan `no-resolve`. Lite tetap domain-only agar penggunaan RAM lebih rendah.

## Perlindungan false positive

- Tidak menggunakan `DOMAIN-KEYWORD,...,REJECT` sebagai heuristic keamanan.
- Tidak memblokir seluruh CDN/media namespace.
- Tidak memblokir seluruh TLD hanya karena dianggap berisiko.
- Allowlist dievaluasi sebelum provider ancaman.
- `app-safe` tidak lagi otomatis memakai DNS kategori keluarga. Hanya `child-safe` dan `threat-safe` yang mengaktifkannya.

## Batas perlindungan

Mihomo/OpenClash adalah network filter. Sistem ini dapat memutus koneksi ke domain dan IP yang diketahui berbahaya, tetapi bukan antivirus/EDR dan tidak dapat membersihkan malware yang sudah berjalan pada perangkat.

## Update provider

Provider keamanan menggunakan interval default 43.200 detik atau 12 jam. Nilai ini tetap dapat diubah melalui `ADBLOCK_PROVIDER_INTERVAL`.
