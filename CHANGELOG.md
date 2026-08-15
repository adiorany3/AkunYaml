# v2.0 Final

- Menggabungkan seluruh patch v1.1 sampai v1.5.
- Menghapus ketergantungan pada `GEOSITE,tracker`.
- Menggunakan `tracker.mrs` untuk tracker blocking.
- Menghapus `global-client-fingerprint` global dari core upstream dan output YAML.
- Memperbaiki referensi `MANUAL` pada lite YAML.
- Menormalkan path HTTP rule-provider menjadi path relatif.
- Membersihkan dangling `RULE-SET` dan proxy-group reference.
- Menghapus injeksi wildcard YouTube pada `nameserver-policy`.
- Menjadikan DNS adblock opt-in. Default `off` untuk kompatibilitas OpenClash.
- Mempertahankan `GEOSITE,category-ads-all,REJECT` pada rule-level.
- Menambahkan HaGeZi TIF Mini, Pop-Up Ads, dan Pro Mini untuk strict mode.
- Menambahkan TLS retry dan fallback curl tanpa menonaktifkan verifikasi SSL.
- Menyatukan fixer existing YAML ke `apply_existing.py`.
- Menyatukan audit/fix router ke `openclash_router_fix.sh`.
- Validasi router selalu memakai `SAFE_PATHS=/usr/share/openclash:/etc/ssl`.
