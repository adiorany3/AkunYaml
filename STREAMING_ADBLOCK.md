# Streaming Ad Protection v3.2

## Tujuan
Menambah pemblokiran iklan streaming secara konservatif tanpa memblokir namespace CDN utama yang juga membawa audio/video normal.

## Default child-safe
Exact host yang diblokir:
- `video-akpcw.spotifycdn.com`
- `805ba.v.fwmrm.net`
- `tvm-mtv-freewheel.akamaized.net`

Router memakai `streaming-ad-safe` sebagai inline domain provider. Android memakai exact `DOMAIN,...,REJECT` agar kompatibel dengan core YAML lama. Tidak ada HTTP provider baru sehingga tidak ada fetch runtime tambahan.

## Yang sengaja tidak diblokir secara luas
- `spotifycdn.com`
- `scdn.co`
- `fwmrm.net`
- `akamaized.net`
- CDN audio/video utama lain

Pemblokiran suffix luas dapat memutus musik, video, artwork, lisensi, atau inisialisasi player.

## Batas teknis
Iklan audio/video yang disisipkan langsung ke stream atau memakai infrastruktur media yang sama tidak selalu dapat dibedakan oleh DNS/Mihomo. Dalam kasus seperti itu, memaksa blokir dapat membuat player berhenti atau buffering.

## Lapisan lain yang tetap aktif
- MetaCubeX `category-ads-all`
- tracker provider
- HaGeZi PRO Mini
- popup ads
- threat intelligence
- child-safe family DNS
- Turtlecute benchmark coverage
- YouTube conservative guard
