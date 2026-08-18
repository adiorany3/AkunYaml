# Changelog v4.5 OpenWrt Enhanced Adblock

- Menambah `ROUTER_ENHANCED_AD_PROVIDERS` sebagai policy router-only.
- Menambah provider `hagezi-pro-plus-mini` pada Auto dan Fresh Pool.
- Mempertahankan focused `popup-ads` pada mode enhanced/compact meski `ADBLOCK_DEDUP_MODE=lean`.
- Menambah mode `compact` untuk OpenWrt Lite.
- Menambah `OPENWRT_ADBLOCK_LEVEL=enhanced` dan `OPENWRT_LITE_ADBLOCK_LEVEL=compact`.
- Memperluas Feed Guard agar memvalidasi feed enhanced dan menyimpan Last-Known-Good.
- Android tidak menerima provider baru.
