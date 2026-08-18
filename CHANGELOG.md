# v4.3 Android Marketplace Live Compatibility

- Android-only compatibility guard for marketplace live/video sessions.
- Critical malware/phishing/cryptominer rules remain higher priority.
- Marketplace endpoints are protected from broad privacy/ad/tracker false positives.
- Adds real-IP DNS, normal DoH policy, and sniffer skip for marketplace live/CDN traffic.
- Keeps the v4.2 Android cold-fallback topology and ~4 active probes/min.

# v4.1 Android Primary-Fallback

- Android multi-host sekarang selalu memakai `BUG_SERVERS[0]` sebagai host utama.
- Host ke-2 dan seterusnya hanya berada di fallback per akun, bukan menjadi kandidat sejajar di group utama.
- Tambah `ANDROID_MULTI_HOST_MODE=primary-fallback` (default), `primary`, dan `inherit`.
- Tambah batas host/cap/interval fallback Android.
- Profil router Auto/Lite/Fresh Pool tidak diubah.
- Lihat `ANDROID_MULTI_HOST_FALLBACK_v4.1.md`.

# v4.0 Performance

- Health-check aktif dikonsolidasikan ke hot pool kecil.
- Subscription cache persisten ditambahkan dengan TTL, ETag, Last-Modified, dan stale-if-error.
- Provider/RDAP cache persisten ditambahkan dengan TTL.
- Candidate pool menjadi adaptif, mulai dari 250 dan berkembang saat diperlukan.
- Multi-host fallback mendapat global variant budget tanpa menghapus base node.
- Audit baru: `performance_budget_audit.py` dan `performance_cache_selftest.py`.
- Lihat `PERFORMANCE_V4.md` dan `PERFORMANCE_COMPARISON_v3.9_vs_v4.0.md`.

# v3.8 Security Hardening

- Security provider dipusatkan di `security_policy.py`.
- Feed preflight + Last-Known-Good ditambahkan melalui `feed_guard.py`.
- Lite tidak lagi memiliki broad `doubleclick.net` reject pada generator inti.
- `THREAT_IP_BLOCKING` menjadi sakelar terpisah.
- Snapshot YAML iklan regional Android dibuat otomatis setelah feed lolos validasi.
- Audit baru: `security_hardening_audit.py`.

## Adblock v3 - YouTube / Streaming Optimization
- Routing YouTube sekarang selalu menuju grup `YOUTUBE`, tidak lagi ter-shadow oleh `GLOBAL`.
- Grup `YOUTUBE` memakai fallback otomatis, health-check 120 detik, lazy, timeout 3000 ms.
- Tambah exact reject `ads.youtube.com` sebelum playback guard.
- Default `ADBLOCK_DEDUP_MODE=lean`: MRS ads/tracker tetap aktif, provider overlap router dilepas.
- Browser filter YouTube diperkuat tanpa memblokir `googlevideo.com` atau `static.doubleclick.net`.
- Android kembali YAML-only dengan static AI Voice/IP guards.
- Lihat `CHANGELOG_ADBLOCK_v3.md` untuk detail dan hasil audit.

## v3.6 Threat-Safe Precision

- Dedicated router providers for malware, phishing, and cryptominers.
- Threat rules now run before general ad/tracker rules.
- Family-category DNS is explicit and limited to child-safe/threat-safe profiles.
- Stronger false-positive audit: allowlist-first, no heuristic DOMAIN-KEYWORD reject, no fallback DNS bypass.
- TIF mini remains a broad safety net; TIF IP remains disabled on Lite.

## v3.5 Threat-Safe
- Profil baru `threat-safe`: anti-scam/fake + threat intelligence domain.
- TIF IP extension aktif pada Auto/Fresh, dilewati pada Lite dan Android untuk performa/kompatibilitas.
- Audit regresi baru: `threat_safe_audit.py`.
# v3.3 Popup & Game Ad Protection

- Tambah fallback popup/popunder dan mobile-game ad SDK tanpa provider HTTP baru.
- Tambah browser companion filter dan audit khusus.
- Pertahankan child-safe, streaming-safe, YouTube guard, dan Turtlecute coverage.

# v2.5 Security Hardening - 2026-08-16

- Menambahkan `threat-tif-mini` berbasis HaGeZi Threat Intelligence Feeds Mini untuk memblokir malware, phishing, scam, spam, dan domain C2.
- Menggunakan rule-provider `behavior: domain` + `format: text`, yang didukung native oleh Mihomo.
- Menempatkan LAN/private dan allowlist sebelum blocklist untuk mengurangi false positive pada layanan lokal.
- Menghapus rule terlalu luas `DOMAIN-KEYWORD,adservice`, `analytics`, dan `tracker`.
- Menambahkan QUIC sniffing pada 443/8443 agar rule domain lebih efektif pada HTTP/3.
- Membatasi `external-controller` ke `127.0.0.1:9090` secara default.
- Membatasi klien proxy LAN ke RFC1918 + loopback melalui `lan-allowed-ips`.
- Menetapkan profil adblock default ke `balanced`; DNS-level adblock tetap `off` untuk kompatibilitas dan false-positive lebih rendah.
- Memperbarui semua output utama: `openclash_auto.yaml`, `openclash_lite.yaml`, `openclash_fresh_pool.yaml`, dan `openclash_android.yaml`.

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
