# Security Optimization

Konfigurasi ini memakai pendekatan multi-platform untuk OpenClash/Mihomo pada router dan client Android berbasis Clash Meta/Mihomo.

## Profil balanced

Profil default adalah `balanced`.

### Router/OpenClash

- `threat-tif-mini`: HaGeZi Threat Intelligence Feeds Mini untuk malware, phishing, scam, cryptojacking, command-and-control, dan domain berbahaya lain.
- `ads_domain`: MetaCubeX category-ads-all dalam format MRS.
- `tracker-domain`: MetaCubeX tracker dalam format MRS.
- YouTube guard: memblokir endpoint iklan yang terpisah dari CDN video tanpa memblokir `googlevideo.com`.
- QUIC sniffing: dipertahankan pada target router yang mendukungnya.

### Android

- `ads_domain`: Chocolate4U category-ads-all dalam format YAML/domain.
- `tracker-domain`: MetaCubeX tracker dalam format YAML/classical.
- `threat-malware`: domain malware aktif.
- `threat-phishing`: domain phishing dan scam.
- `threat-cryptominers`: domain cryptominer.
- Sniffer hanya HTTP dan TLS untuk kompatibilitas Android.

Semua provider HTTP diperbarui otomatis setiap 12 jam secara default (`43200` detik).

## Profil strict

`strict` sekarang benar-benar berbeda dari `balanced`.

Pada router, strict menambahkan:

- `hagezi-pro-mini`: HaGeZi Multi PRO Mini.
- `popup-ads`: HaGeZi Pop-Up Ads untuk iklan popup yang mengganggu atau berbahaya.

Pada Android, strict menambahkan:

- `privacy-extra`: Blackmatrix7 Privacy classical YAML.

Mode strict memakai lebih banyak rule dan memiliki risiko false positive lebih tinggi. Gunakan allowlist bila ada layanan sah yang ikut terblokir.

## False positive

Tambahkan domain sah ke `adblock_allowlist.txt`, satu domain per baris. Runner akan menaruh allowlist sebelum seluruh blocklist.

Contoh:

```text
example.com
login.example.com
```

Jangan menambahkan wildcard atau URL lengkap. Masukkan nama domain saja.

## Dashboard OpenClash dari perangkat LAN

Default memakai:

```yaml
external-controller: 127.0.0.1:9090
```

Jika dashboard memang harus terhubung langsung ke port 9090 dari perangkat LAN, override saat generate:

```sh
export MIHOMO_EXTERNAL_CONTROLLER=0.0.0.0:9090
```

Jika controller dibuka ke LAN, gunakan firewall LAN yang ketat dan secret API yang kuat. Jangan expose port 9090 ke WAN.

## DNS adblock

`ADBLOCK_DNS_MODE` tetap `off` secara default. Rule-level blocking lebih aman untuk kompatibilitas aplikasi dan YouTube. Mode DNS dapat diaktifkan secara terpisah bila diperlukan.

## Update interval

Default:

```json
"ADBLOCK_PROVIDER_INTERVAL": "43200"
```

Nilai minimal yang diterima runner adalah 3600 detik. Untuk router dengan resource terbatas, 12 jam adalah pilihan yang lebih aman daripada refresh terlalu sering.

## Validasi

Android:

```bash
python android_ruleprovider_audit.py openclash_android.yaml
python adblock_provider_audit.py
```

Untuk memeriksa apakah URL upstream rule-provider masih dapat diakses:

```bash
python adblock_provider_audit.py --network
```

Semua output:

```bash
python youtube_adblock_audit.py
python validate_openclash_target.py --static-only
```

Jika exact Mihomo core target tersedia, gunakan parser validation juga.
