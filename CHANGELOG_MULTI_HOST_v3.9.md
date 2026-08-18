# Changelog v3.9 Multi-Host

- Menambahkan `BUG_SERVERS` sebagai array pada `local_config.json`.
- Menambahkan mode `primary`, `fallback`, dan `distribute`.
- Menambahkan preflight health-check multi-host dengan `BUG_HEALTH_CHECK`.
- Menambahkan `BUG_HEALTH_ATTEMPTS` untuk membatasi biaya probe.
- Menambahkan `BUG_MAX_VARIANTS_PER_NODE` untuk membatasi jumlah varian per akun.
- Pada mode `fallback`, builder membuat varian proxy per host sehingga group url-test/fallback Mihomo dapat menghindari endpoint yang gagal.
- `akun.txt` dan fresh candidate links mengikuti host yang dikonfigurasi.
- `local_runner.load_config()` sekarang mempertahankan array/dict JSON secara aman ketika dipindahkan ke environment subprocess.
- Default tetap hanya memakai host lama. Tidak ada host pihak ketiga baru yang ditambahkan otomatis.

Gunakan hanya hostname/IP yang Anda miliki atau berwenang untuk gunakan.
