# AkunYaml v4.6 - YouTube Playback-Safe Adblock

## Tujuan

Mengurangi request iklan YouTube yang dapat dipisahkan di level domain tanpa memblokir CDN video utama. Perubahan hanya menambah layer router OpenWrt. Android tetap mengikuti profil v4.4/v4.5.

## Perubahan

- Menambah enam exact-host advertising/measurement pada OpenWrt Auto/Lite/Fresh.
- Menempatkan exact-host sebelum YouTube playback guard.
- Mempertahankan `static.doubleclick.net` sebagai compatibility route ke `YOUTUBE`.
- Mempertahankan `googlevideo.com`, `ytimg.com`, `youtubei.googleapis.com`, `youtube.googleapis.com`, dan `ggpht.com` sebagai playback route.
- Menambah toggle `YOUTUBE_ROUTER_EXTRA_ADS=true`.
- Memperkuat `youtube_browser_filters.txt` dengan exact-host yang sama untuk browser.
- Menambah `youtube_playback_safe_audit.py`.

## Batasan

DNS/routing tidak dapat membedakan iklan yang dikirim dari host media yang sama dengan video normal. Karena itu v4.6 tidak mencoba memblokir `googlevideo.com`.
