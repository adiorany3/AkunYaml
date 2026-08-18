# v3.8 Security Hardening

Tanggal: 2026-08-18

## Perubahan inti

- Menambahkan `security_policy.py` sebagai satu sumber definisi provider security untuk generator inti dan local runner.
- Menghapus duplikasi katalog malware, phishing, cryptominer, fake/scam, TIF, iklan regional, dan threat IP dari `local_runner.py`.
- Generator inti sekarang membaca profil security yang sama dengan local runner.
- Menghilangkan blok suffix `doubleclick.net` yang terlalu luas dari jalur Lite generator.
- Menjaga exact compatibility host YouTube sebelum provider iklan.
- Menambahkan `THREAT_IP_BLOCKING=true` agar threat-IP dapat dinonaktifkan tanpa mematikan threat-domain.
- Menambahkan `feed_guard.py` untuk preflight feed, sanity check jumlah entry, SHA-256, dan Last-Known-Good cache.
- Update feed yang terlalu kecil, kosong, invalid, atau berubah ekstrem tidak menimpa Last-Known-Good.
- Refresh feed dijalankan paralel agar tidak menambah waktu startup secara linear.
- Menambahkan generator snapshot YAML regional untuk Android. Snapshot hanya diaktifkan jika feed berhasil divalidasi.
- Android tetap tidak memakai provider security MRS/text.
- Menambahkan `security_hardening_audit.py` untuk regresi source-of-truth, rule order, Lite, Android, dan Last-Known-Good.

## Konfigurasi baru

```text
THREAT_IP_BLOCKING=true
SECURITY_FEED_GUARD=true
REFRESH_SECURITY_FEEDS=true
FEED_MAX_DROP_RATIO=0.65
FEED_MAX_GROWTH_RATIO=4.0
```

## Hasil validasi

- Python compile: OK
- Threat-safe audit: OK
- YouTube audit: OK
- Android YAML-provider audit: OK
- App ads audit: OK
- Streaming ads audit: OK
- Popup/game ads audit: OK
- Security hardening audit: OK
- Static OpenClash target validation: OK

Exact parser test tidak dijalankan pada environment Linux ini karena binary `.local_bin/mihomo` di paket adalah Mach-O ARM64.
