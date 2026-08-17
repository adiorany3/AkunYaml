# Changelog v3.3 - Popup & Game Ad Protection

- Menambahkan 31 suffix fallback untuk popup/popunder dan SDK iklan game/mobile.
- Tidak menambahkan provider HTTP baru, sehingga overhead update/runtime tetap kecil.
- Mempertahankan HaGeZi Popup Ads, HaGeZi PRO Mini, MetaCubeX category-ads-all, tracker, threat feeds, child-safe DNS, Turtlecute coverage, YouTube guard, dan streaming-safe v3.2.
- Menambahkan companion browser filter yang konservatif.
- Menambahkan `popup_game_ad_audit.py` untuk memastikan semua output memuat rule yang sama dan tidak memblokir CDN media utama secara luas.
