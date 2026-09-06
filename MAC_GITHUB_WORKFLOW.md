# AkunYaml: Mac + GitHub + OpenClash

Target paket:

- OpenClash `v0.47.156`
- Mihomo Meta `alpha-ge183c58`
- Source Mihomo exact commit `e183c58`

## 1. Clone repository di Mac

Jalankan Terminal:

```bash
git clone https://github.com/adiorany3/AkunYaml.git
cd AkunYaml
```

Gunakan file versi paket ini di repository tersebut, lalu commit/push satu kali bila belum ada di GitHub.

## 2. Refresh akun dari Mac

```bash
chmod +x mac_build_target_core.sh mac_refresh_accounts.sh *.command
./mac_refresh_accounts.sh
```

Alurnya:

1. `git pull --rebase --autostash` dari branch aktif.
2. Membuat `.venv` jika belum ada.
3. Menginstal dependency Python.
4. Membangun Mihomo exact `e183c58` untuk Apple Silicon atau Intel Mac jika belum tersedia.
5. Mengambil sumber akun dari `DEFAULT_LINKS` dan `subscription_links.txt`.
6. Menguji kandidat.
7. Generate empat YAML OpenClash.
8. Memvalidasi hasil dengan exact core.

Output utama:

- `openclash_auto.yaml`
- `openclash_android.yaml`
- `openclash_lite.yaml`
- `openclash_fresh_pool.yaml`
- `akun.txt`

## 3. Refresh lalu push otomatis ke GitHub

```bash
./mac_refresh_accounts.sh --push
```

Script hanya menambahkan output generator dan laporan ke commit. Folder lokal `.venv`, `.local_bin`, dan `.build` tidak ikut GitHub.

## 4. Cara praktis dari Finder

Double-click:

- `mac_pull_and_refresh.command` untuk pull + cari akun + generate.
- `mac_pull_refresh_push.command` untuk pull + cari akun + generate + commit + push.

Jika macOS menolak file `.command`, jalankan sekali:

```bash
chmod +x *.command *.sh
```

## 5. Mengambil hasil terbaru di OpenWrt

Jika repository juga di-clone pada router:

```sh
cd /root/AkunYaml
git pull --ff-only origin main
```

Kemudian salin YAML utama ke folder konfigurasi OpenClash sesuai nama konfigurasi yang Anda gunakan, misalnya:

```sh
cp openclash_auto.yaml /etc/openclash/config/openclash_auto.yaml
```

Sebelum restart, periksa core router:

```sh
/etc/openclash/core/clash_meta -v
```

Target harus mengandung `alpha` dan `e183c58`.

Lalu validasi bila Python tersedia:

```sh
python3 validate_openclash_target.py --core /etc/openclash/core/clash_meta openclash_auto.yaml
```

## 6. Menambah sumber akun

Masukkan URL subscription ke `subscription_links.txt`, satu URL per baris. Untuk node individual, masukkan URI ke `manual_nodes.txt`, satu URI per baris.

Jangan edit `akun.txt` sebagai input karena file tersebut merupakan output generator.

## 7. Pull langsung dari GitHub di OpenWrt

Paket juga menyediakan `openwrt_git_pull_update.sh`. Dari folder repository pada router:

```sh
chmod +x openwrt_git_pull_update.sh
./openwrt_git_pull_update.sh
```

Script akan:

1. `git pull --ff-only origin main`.
2. Memastikan `/etc/openclash/core/clash_meta` adalah `alpha` commit `e183c58`.
3. Menyalin provider ke direktori versi baru di `/etc/openclash/`, menyesuaikan path provider pada salinan YAML, lalu menjalankan parser test menggunakan core router.
4. Hanya jika lolos, menyimpan YAML sebelumnya sebagai `.bak` dan mengganti `openclash_auto.yaml` secara atomik di `/etc/openclash/config/`.
5. Tidak me-restart OpenClash otomatis.

`OPENCLASH_DATA_DIR` dapat mengganti direktori data default `/etc/openclash`.
Versi provider lama sengaja disimpan untuk rollback; hapus hanya versi yang tidak lagi direferensikan konfigurasi aktif maupun backup.
Parser test bukan uji konektivitas: periksa provider termuat, login, bank, dan browsing melalui LuCI setelah penerapan.

Untuk lokasi repository atau nama config berbeda:

```sh
REPO_DIR=/root/AkunYaml BRANCH=main CONFIG_NAME=openclash_auto.yaml ./openwrt_git_pull_update.sh
```

> Jika Anda memasukkan subscription atau akun private, jangan gunakan `--push` ke repository public. YAML hasil generate juga dapat berisi credential proxy.
