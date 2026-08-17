# Adblock Multi-Platform v3.0 Child-Safe

- Menambahkan profil `child-safe` untuk OpenClash/OpenWrt dan Android.
- Child-safe menggunakan lapisan blocking setara strict.
- DNS utama dan fallback diarahkan ke family DNS agar kategori iklan, tracker, malware, konten dewasa, dan judi diblokir di tingkat DNS.
- `proxy-server-nameserver` tidak diubah agar resolusi hostname proxy tetap stabil.
- Guard YouTube tetap mempertahankan `googlevideo.com`, `youtube.com`, `ytimg.com`, dan domain playback lain agar video tidak rusak.
- Endpoint iklan YouTube yang dapat dipisahkan tetap ditolak.
- Profil balanced dan strict tetap tersedia.
- Default tetap balanced.
