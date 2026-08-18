# Code Optimization Pass - 2026-08-18

Target tetap OpenClash v0.47.156 dan Mihomo alpha-ge183c58. Perubahan ini fokus pada waktu proses, determinisme, dan robustness tanpa mengubah desain threat-safe, adblock, YouTube guard, AI routing, atau target final YAML.

## Perubahan

1. `process_sources()` sekarang menghapus subscription URL duplikat sambil mempertahankan urutan sumber.
2. Fetch subscription tetap concurrent, tetapi hasil diproses sesuai urutan input agar candidate pool deterministik antar-run.
3. Share URI yang identik dari mirror subscription hanya diparse sekali.
4. `MAX_WORKERS`, `ATTEMPTS`, `REQUIRE_SUCCESSES`, candidate multiplier, candidate minimum, dan reserve pool dinormalisasi agar nilai nol atau negatif tidak merusak ThreadPoolExecutor atau scoring.
5. Thread pool node testing dipakai ulang untuk semua batch. Sebelumnya executor dibuat dan dihancurkan pada setiap batch.
6. Jeda 30 ms pada TCP/TLS/WebSocket probe hanya dilakukan di antara percobaan. Tidak ada sleep setelah percobaan terakhir.
7. Provider/ASN lookup pada `unique_names()` sekarang concurrent dan dibatasi oleh `PROVIDER_LOOKUP_WORKERS`, default 8. Urutan penamaan node tetap mengikuti urutan input.
8. OpenClash compatibility filter sekarang memakai adaptive batch validation:
   - seluruh pool dites dalam satu Mihomo process terlebih dahulu;
   - jika gagal, pool dibagi menjadi isolation batch kecil;
   - hanya batch yang gagal yang dites per-node.
9. Opsi baru `OPENCLASH_COMPAT_ISOLATION_BATCH_SIZE`, default 8.
10. Nilai runtime utama di `generate_yaml.py` di-clamp sebelum dipakai pipeline.

## Validasi

- Python compileall: OK.
- Static validator OpenClash v0.47.156 + Mihomo alpha-ge183c58: OK untuk auto, lite, android, fresh pool.
- Threat-safe audit: OK.
- YouTube/adblock audit: OK.
- Android rule-provider audit: OK.
- App ad audit: OK.
- Streaming ad audit: OK.
- Popup/game ad audit: OK.
- Regression simulasi subscription: URL duplikat hanya di-fetch sekali dan urutan sumber tetap deterministik.
- Regression simulasi compatibility filter: 60 node valid selesai melalui 1 Mihomo process pada fast path.
- Regression simulasi compatibility filter dengan 1 node rusak dari 20: 19 node valid tetap lolos dan node rusak terisolasi.

## Catatan

Binary `.local_bin/mihomo` pada paket adalah Mach-O ARM64 macOS. Lingkungan Linux ini tidak menjalankan exact binary tersebut. Karena itu validasi target di lingkungan ini memakai static validator proyek. Parser exact-core tetap wajib pada pipeline target yang memiliki binary kompatibel.
