# Adblock High-Score v3.1

- Menambahkan coverage kecil untuk domain yang diuji Turtlecute Ad Blocker Test.
- Router/OpenClash memakai inline domain rule-provider agar lookup efisien dan tidak menambah HTTP provider runtime.
- Android memakai exact DOMAIN rules untuk kompatibilitas core lama.
- `static.doubleclick.net` sengaja tidak diblokir oleh coverage benchmark untuk menjaga kompatibilitas YouTube.
- Provider utama ads/tracker/threat tetap update setiap 12 jam.
- Snapshot Turtlecute dapat direfresh saat generator dijalankan dengan `REFRESH_TURTLECUTE=true`.
- Filter browser opsional ditambah untuk cosmetic/script checks yang memang tidak bisa ditangani oleh DNS/OpenClash.
