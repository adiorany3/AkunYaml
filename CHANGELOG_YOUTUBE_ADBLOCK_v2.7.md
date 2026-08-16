# YouTube Adblock v2.7

Tanggal: 2026-08-16

Perubahan:

- Menghapus blokir `DOMAIN-SUFFIX,doubleclick.net,REJECT` yang terlalu luas.
- Menghapus blokir `static.doubleclick.net` karena dapat mengganggu validasi playback YouTube.
- Menambahkan compatibility guard untuk `static.doubleclick.net` dan `jnn-pa.googleapis.com` sebelum blocklist umum.
- Mempertahankan blokir endpoint iklan DoubleClick yang spesifik.
- Mempertahankan `googlevideo.com` dan domain playback utama sebelum provider iklan/tracker.
- Menambah filter browser konservatif untuk `adPlacements`, `adSlots`, dan `playerAds`.
- Memperbarui `youtube_adblock_audit.py` untuk mendeteksi regresi playback.
- Menyinkronkan perubahan ke generator, profil referensi, dan seluruh output OpenClash utama.
