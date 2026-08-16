# Responsiveness Optimization

Profil ini menekan latency dan jitter tanpa melemahkan adblock/malware protection.

Perubahan utama:

- `tcp-concurrent: true` dipertahankan agar Mihomo mencoba seluruh IP hasil DNS dan memakai koneksi TCP yang berhasil lebih dulu.
- TCP keepalive menggunakan interval 15 detik dan idle 30 detik agar koneksi idle lebih cepat dijaga pada router yang selalu menyala.
- DNS memakai cache ARC. `fallback-lazy-query: true` mencegah query fallback ganda saat hasil utama masih valid.
- `proxy-server-nameserver` dipisahkan agar hostname node tidak bergantung pada alur DNS proxy yang sedang dibangun.
- Rule IP private memakai `no-resolve` sehingga tidak memicu resolusi DNS yang tidak diperlukan.
- Pool `WARM-UP` dibatasi ke 5 node tercepat dan tetap aktif setiap 20 detik.
- `AUTO-FAST` memantau maksimum 8 node setiap 45 detik.
- Health check sekunder dibuat lazy atau diperjarang untuk mengurangi CPU, koneksi latar belakang, dan jitter pada router.
- `GLOBAL` hanya memeriksa grup otomatis inti, bukan seluruh node dan seluruh grup aplikasi secara berulang.

Tujuan profil ini adalah respons browsing dan aplikasi yang lebih stabil. Profil ini tidak mengubah MTU atau mengaktifkan HTTP/3 DNS secara paksa karena kedua pengaturan tersebut sangat tergantung ISP dan dapat memperburuk koneksi pada jaringan tertentu.
