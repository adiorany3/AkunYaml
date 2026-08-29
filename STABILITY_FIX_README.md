# OpenClash Stability Fix

Perbaikan ini dibuat untuk menjaga koneksi non-blokir tetap stabil dan mengurangi putus-nyambung akibat pergantian node yang terlalu sering.

Perubahan utama:

- Health-check `url-test` diperlambat menjadi minimal 300 detik, timeout minimal 5000 ms, tolerance minimal 150 ms, dan kegagalan minimal 3 kali sebelum dianggap bermasalah.
- Group `fallback` sekarang lebih konservatif: interval minimal 300 detik, timeout minimal 5000 ms, dan 3 kegagalan sebelum pindah jalur.
- DNS utama family-safe tetap dipertahankan. Ditambahkan fallback Cloudflare Families agar DNS tidak mati total ketika resolver utama bermasalah.
- `prefer-h3` dimatikan untuk DNS agar resolver tidak bergantung pada jalur QUIC/UDP yang lebih mudah terganggu pada sebagian ISP/router.
- Resolver hostname proxy tetap memakai Cloudflare/Google publik, sehingga domain server proxy tidak ikut gagal karena filtering DNS kategori.
- Ditambahkan fake-IP compatibility filter untuk STUN, Xbox, dan Nintendo agar aplikasi real-time/gaming tidak mudah gagal karena fake-IP.
- Duplikasi `keep-alive-interval` di profil Android dibersihkan.
- `local_config.json` dan `local_runner.py` ikut diperbarui agar regenerasi tidak mengembalikan tuning agresif lama.

Catatan: rule `REJECT`, adblock, gambling, malware, scam, dan blokir lain yang sudah ada tidak dihapus.
