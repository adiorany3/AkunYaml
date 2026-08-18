# Android Multi-Host Primary Fallback v4.1

> Catatan: v4.1 telah digantikan oleh `ANDROID_COLD_FALLBACK_v4.2.md` karena fallback per akun dapat menambah health-check bertingkat pada Android.


v4.1 mengubah strategi multi-host khusus output `openclash_android.yaml`.

## Perilaku baru

Jika `BUG_SERVERS` berisi beberapa host, host pertama selalu menjadi primary. Host berikutnya hanya menjadi fallback untuk akun yang sama.

Contoh konfigurasi:

```json
{
  "BUG_SERVERS": [
    "primary.example",
    "backup-1.example",
    "backup-2.example"
  ],
  "BUG_MODE": "fallback",
  "ANDROID_MULTI_HOST_MODE": "primary-fallback",
  "ANDROID_FALLBACK_HOST_LIMIT": "3",
  "ANDROID_FALLBACK_TOTAL_CAP": "24",
  "ANDROID_FALLBACK_INTERVAL": "180",
  "ANDROID_FALLBACK_LAZY": "true"
}
```

Gunakan hanya hostname/IP yang Anda miliki atau berhak gunakan.

Untuk satu akun, builder Android membentuk struktur logis seperti berikut:

```yaml
proxies:
  - name: AKUN-001-H1
    server: primary.example
  - name: AKUN-001-H2
    server: backup-1.example
  - name: AKUN-001-H3
    server: backup-2.example

proxy-groups:
  - name: AKUN-001-FB
    type: fallback
    proxies:
      - AKUN-001-H1
      - AKUN-001-H2
      - AKUN-001-H3
```

Policy group utama hanya menerima `AKUN-001-FB`, bukan ketiga varian host tersebut. Ini mencegah `url-test` utama memilih host cadangan sebagai kandidat sejajar ketika host pertama sebenarnya masih dapat digunakan.

## Mode Android

`primary-fallback` adalah default. Host pertama selalu primary dan host lain menjadi fallback per akun.

`primary` hanya menghasilkan host pertama. Tidak ada endpoint fallback tambahan.

`inherit` mempertahankan perilaku multi-host v4.0 untuk Android. Semua varian mengikuti strategi global. Gunakan hanya jika memang diperlukan.

## Batas fallback

`ANDROID_FALLBACK_HOST_LIMIT` membatasi jumlah host per akun. Nilai default 3.

`ANDROID_FALLBACK_TOTAL_CAP` membatasi total endpoint Android. Semua akun tetap mendapat host utama terlebih dahulu. Slot yang tersisa baru digunakan untuk host cadangan secara round-robin.

`ANDROID_FALLBACK_INTERVAL` mengatur interval health-check group fallback per akun.

`ANDROID_FALLBACK_LAZY=true` menjaga fallback tetap hemat probe ketika logical node tersebut tidak sedang digunakan.

## Output lain

Perubahan ini hanya berlaku untuk `openclash_android.yaml`. Output berikut tetap menggunakan strategi multi-host global:

- `openclash_auto.yaml`
- `openclash_lite.yaml`
- `openclash_fresh_pool.yaml`
- `akun.txt`
