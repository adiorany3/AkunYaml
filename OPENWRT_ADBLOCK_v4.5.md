# OpenWrt Enhanced Adblock v4.5

Versi ini meningkatkan adblock hanya pada output OpenWrt/OpenClash router. Profil Android tidak diubah.

## Mode

- `OPENWRT_ADBLOCK_LEVEL=enhanced`: dipakai Auto dan Fresh Pool. Menambah HaGeZi Pro++ Mini dan popup/redirect feed di atas ABPindo, global ads, dan tracker provider yang sudah ada.
- `OPENWRT_LITE_ADBLOCK_LEVEL=compact`: dipakai Lite. Hanya menambah popup/redirect feed agar RAM tetap terkontrol.
- `standard`: perilaku lama.

## Urutan proteksi

1. LAN/private dan allowlist.
2. AI/YouTube compatibility guard.
3. Malware, phishing, cryptominer, scam, dan TIF.
4. HaGeZi Pro++ Mini pada Enhanced.
5. Popup/redirect ads.
6. Iklan Indonesia.
7. Global ads.
8. Tracker.
9. Routing normal.

## False-positive control

`adblock_allowlist.txt` tetap dievaluasi sebelum provider ad/tracker. DNS-level adblock tetap `off` secara default agar domain yang dibutuhkan aplikasi tidak gagal resolve sebelum rule allowlist dapat bekerja.

## Lite

Lite sengaja tidak memakai Pro++ Mini secara default. Gunakan `OPENWRT_LITE_ADBLOCK_LEVEL=enhanced` hanya jika router memiliki RAM yang cukup dan pengguna siap menangani false positive tambahan.
