# Threat-Safe v3.5

Profil `threat-safe` memperluas `app-safe` dengan proteksi terhadap scam/fake, malware, phishing, cryptojacking, command-and-control (C2), dan infrastruktur berbahaya yang dikenal.

## Strategi performa

- OpenClash Lite: domain threat intelligence saja. Tidak memuat daftar IP TIF.
- Android: provider YAML-only untuk malware, phishing/scam, dan cryptominer agar tetap kompatibel dengan core lama.
- OpenClash Auto dan Fresh Pool: domain threat intelligence + IP TIF untuk koneksi ke IP berbahaya yang tidak bergantung pada DNS.
- Tidak mengaktifkan NRD/DGA jutaan domain, blok seluruh URL shortener, badware hoster root-domain, atau seluruh TLD berisiko karena potensi false positive dan overhead.

## Batas perlindungan

Mihomo/OpenClash adalah lapisan network filtering, bukan antivirus/EDR. Ia dapat memutus akses ke domain/IP yang diketahui berbahaya, tetapi tidak dapat membersihkan malware yang sudah berjalan pada perangkat, memeriksa file lokal secara penuh, atau menjamin deteksi zero-day. Gunakan proteksi perangkat/OS yang aktif dan selalu diperbarui.

## Update provider

Provider keamanan menggunakan interval 43.200 detik (12 jam). Untuk daftar yang berubah cepat, ini menjaga keseimbangan antara freshness dan jumlah fetch pada router.
