# Changelog v4.4 Android Banking Safe

- Menambahkan `android_banking_policy.py` sebagai policy Android terpisah.
- Default Banking Safe Mode hanya mencakup `seabank.co.id`.
- SeaBank sekarang menggunakan `DIRECT` sebelum privacy/ad/tracker filtering.
- Menambahkan `+.seabank.co.id` ke `dns.fake-ip-filter`.
- Menambahkan normal public DoH policy untuk `+.seabank.co.id`.
- Menambahkan `+.seabank.co.id` ke `sniffer.skip-domain`.
- Critical malware, phishing, dan cryptominer tetap memiliki prioritas lebih tinggi daripada Banking Safe Mode.
- Menambahkan konfigurasi `ANDROID_BANKING_SAFE_MODE`, `ANDROID_BANKING_DOMAINS`, dan `ANDROID_BANKING_EXACT_DOMAINS`.
- Menambahkan `android_banking_safe_audit.py`.
- `local_runner.py` dinaikkan menjadi `4.4-android-banking-safe`.
- `openclash_auto.yaml`, `openclash_lite.yaml`, dan `openclash_fresh_pool.yaml` tetap byte-identik dengan v4.3.
- Health-check Android tetap sekitar 4 probe aktif/menit.
