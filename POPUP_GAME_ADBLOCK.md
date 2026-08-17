# Popup & Mobile Game Ad Protection v3.3

## Tujuan
Mengurangi popup/popunder browser dan iklan yang berasal dari SDK monetisasi game/aplikasi Android tanpa memblokir CDN game, asset server, atau host video/audio utama.

## Strategi performa
- Tidak menambah HTTP rule-provider baru.
- Menambah daftar kecil `DOMAIN-SUFFIX` lokal.
- Provider HaGeZi Pop-Up Ads dan PRO Mini tetap menjadi lapisan update otomatis.
- MetaCubeX/Android ads provider tetap menjadi lapisan umum.
- Rule tambahan berfungsi sebagai fallback untuk jaringan iklan game yang paling umum.

## Jaringan yang ditargetkan
Lapisan tambahan mencakup namespace iklan dari AppLovin, Unity Ads, ironSource/Supersonic, Vungle/Liftoff, Chartboost, InMobi, AdColony, Mintegral, Pangle, Tapjoy, Start.io, Fyber/Digital Turbine, serta beberapa jaringan popunder browser.

## Yang tidak diblokir
- CDN game umum.
- domain login Google/Apple/Facebook.
- `googlevideo.com`.
- seluruh `spotifycdn.com`.
- seluruh `akamaized.net`.
- domain pembayaran.

## Batas teknis
Popup yang dibuat sepenuhnya oleh JavaScript dari domain situs yang sama tidak selalu dapat dihentikan oleh DNS/Mihomo. Gunakan companion filter browser untuk kasus tersebut. Game yang mensyaratkan rewarded ad dapat menampilkan pesan "ad unavailable" setelah jaringan iklannya diblokir.
