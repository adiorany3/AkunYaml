# YouTube Playback-Safe v4.6

Profil ini memprioritaskan kelancaran video. Router memblokir endpoint iklan yang dapat dipisahkan, lalu mengarahkan domain playback utama ke grup `YOUTUBE`.

## Router-only exact layer

```text
adservice.google.com
pagead2.googleadservices.com
afs.googlesyndication.com
stats.g.doubleclick.net
m.doubleclick.net
mediavisor.doubleclick.net
```

Semua memakai `REJECT`. Layer hanya aktif pada `openclash_auto.yaml`, `openclash_lite.yaml`, dan `openclash_fresh_pool.yaml`.

## Playback protection

Domain berikut tidak boleh diberi `REJECT` oleh layer YouTube:

```text
static.doubleclick.net
googlevideo.com
ytimg.com
youtubei.googleapis.com
youtube.googleapis.com
ggpht.com
```

## Setting

```json
"YOUTUBE_ADBLOCK_MODE": "enhanced",
"YOUTUBE_ROUTER_EXTRA_ADS": "true"
```

Set `YOUTUBE_ROUTER_EXTRA_ADS=false` bila ingin kembali ke perilaku v4.5 tanpa menghapus kode.
