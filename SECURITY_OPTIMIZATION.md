# Security Optimization

Konfigurasi ini memakai pendekatan balanced untuk OpenClash/Mihomo pada router.

## Proteksi yang aktif

- `threat-tif-mini`: blok domain malware, phishing, scam, spam, cryptojacking, dan command-and-control.
- `ads_domain`: blok domain iklan dari MetaCubeX category-ads-all.
- `tracker-domain`: blok tracker dari MetaCubeX.
- YouTube guard: blok endpoint iklan yang terpisah dari CDN video, tanpa memblokir `googlevideo.com`.
- QUIC sniffing: membantu rule domain tetap bekerja pada HTTP/3.
- LAN/private bypass: trafik lokal diproses DIRECT sebelum blocklist.
- Controller hardening: API Mihomo hanya listen di loopback secara default.
- `lan-allowed-ips`: proxy LAN dibatasi ke loopback dan jaringan RFC1918.

## False positive

Tambahkan domain sah ke `adblock_allowlist.txt`, satu domain per baris. Runner akan menaruh allowlist sebelum seluruh blocklist.

Contoh:

```text
example.com
login.example.com
```

Jangan menambahkan wildcard atau URL lengkap. Masukkan nama domain saja.

## Dashboard OpenClash dari perangkat LAN

Default baru memakai:

```yaml
external-controller: 127.0.0.1:9090
```

Ini mengurangi permukaan serangan API. Jika dashboard Anda memang harus terhubung langsung ke port 9090 dari perangkat LAN, override dengan environment berikut saat generate:

```sh
export MIHOMO_EXTERNAL_CONTROLLER=0.0.0.0:9090
```

Jika membuka controller ke LAN, gunakan firewall LAN yang ketat dan secret API yang kuat. Jangan expose port 9090 ke WAN.

## DNS adblock

`ADBLOCK_DNS_MODE` tetap `off` secara default. Rule-level blocking lebih aman untuk kompatibilitas aplikasi dan YouTube. Mode DNS dapat diaktifkan secara terpisah bila diperlukan.

## Sumber rule

- MetaCubeX meta-rules-dat untuk ads dan tracker.
- HaGeZi DNS Blocklists, Threat Intelligence Feeds Mini untuk malware/phishing.

Provider diperbarui setiap 12 jam (`43200` detik).
