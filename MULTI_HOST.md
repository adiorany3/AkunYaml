# Multi-Host Failover v3.9

Fitur ini memungkinkan satu akun/proxy memakai beberapa target host/IP untuk failover. Gunakan hanya host atau server yang Anda miliki atau berhak gunakan.

## Setting

Edit `local_config.json`:

```json
{
  "BUG_SERVERS": [
    "host-a.example.net",
    "host-b.example.net"
  ],
  "BUG_MODE": "fallback",
  "BUG_HEALTH_CHECK": "true",
  "BUG_HEALTH_ATTEMPTS": "1",
  "BUG_MAX_VARIANTS_PER_NODE": "3"
}
```

## Mode

- `primary`: hanya memakai host pertama.
- `fallback`: membuat varian proxy per host. Group Mihomo `url-test` dan `fallback` akan menghindari endpoint yang gagal.
- `distribute`: menyebarkan akun ke beberapa host secara deterministik tanpa menggandakan jumlah proxy.

## Guard

- Maksimal 8 target host/IP dibaca dari konfigurasi.
- URL, path, userinfo, dan `host:port` ditolak. Masukkan hostname/IP saja.
- Duplikat otomatis dihapus.
- `BUG_MAX_VARIANTS_PER_NODE` dibatasi 1 sampai 8.
- `BUG_HEALTH_ATTEMPTS` dibatasi 1 sampai 3.
- Jika daftar tidak valid atau kosong, generator kembali ke target default lama.
- Pada multi-host aktif, `manual_nodes.txt` tidak lagi ditimpa ke host pertama sebelum parsing agar SNI/Host asli tidak hilang.
