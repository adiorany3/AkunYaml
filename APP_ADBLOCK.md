# App-Safe Adblock v3.4

Profil `app-safe` memperluas profil `child-safe` untuk memblokir iklan di aplikasi Android dan aplikasi desktop tanpa memblokir CDN, login, update, push notification, atau domain media utama secara luas.

## Lapisan baru

- 10 namespace SDK iklan aplikasi tambahan.
- 31 endpoint iklan OEM Android yang spesifik untuk Xiaomi/MIUI dan OPPO/Realme/HeyTap.
- 35 endpoint iklan aplikasi desktop Windows/Microsoft/MSN dan Apple/macOS.
- Router memakai satu inline `app-ad-safe` provider agar tidak menambah HTTP fetch runtime.
- Android memakai `DOMAIN`/`DOMAIN-SUFFIX` langsung untuk kompatibilitas core YAML lama.
- Semua proteksi v3.3 tetap aktif: threat, tracker, popup, game ads, streaming-safe, child-safe DNS, dan Turtlecute coverage.

## Batas teknis

Iklan yang berasal dari domain/API yang sama dengan konten utama tidak selalu dapat diblokir di level DNS/routing tanpa risiko merusak aplikasi. Karena itu profil ini menghindari blokir seluruh CDN dan domain layanan utama.

## Profil

Gunakan `--profile app-safe` pada `apply_existing.py` atau `--adblock-profile app-safe` pada local runner.
