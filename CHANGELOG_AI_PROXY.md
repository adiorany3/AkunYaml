# AI Proxy Routing v2

Tanggal: 2026-08-18

## Tujuan

Versi v2 memprioritaskan kestabilan sesi AI, konsistensi IP keluar, dan ketahanan terhadap false-positive adblock atau threat filtering. Desainnya tetap memakai proxy yang sudah tersedia di profil, tanpa menambahkan node eksternal.

## Arsitektur AI v2

Trafik AI tidak lagi diarahkan ke satu health-check generik. Empat grup layanan dibuat terpisah:

- `AI-OPENAI` untuk ChatGPT, OpenAI, Sora, autentikasi, aset, dan Voice
- `AI-CLAUDE` untuk Claude dan Anthropic
- `AI-GEMINI` untuk Gemini, AI Studio, dan endpoint Generative AI Google yang relevan
- `AI-OTHER` untuk Copilot, Perplexity, Grok, DeepSeek, Mistral, Meta AI, Qwen, Kimi, Poe, dan Cohere

Grup `AI` tetap dipertahankan sebagai alias kompatibilitas, tetapi tidak lagi menjadi target rule langsung. Ini mencegah konfigurasi lama atau UI OpenClash kehilangan referensi grup.

## Seleksi node

- `AI-STABLE` mengambil maksimal 8 node otomatis tercepat dengan target delay maksimal 250 ms
- `AI-BACKUP` mengambil maksimal 8 node berikutnya dengan target delay maksimal 700 ms
- `AI-MANUAL` menampung node manual sebagai opsi terakhir
- Grup layanan menggunakan kandidat stable, backup, lalu manual secara berurutan
- Pada `openclash_fresh_pool.yaml`, node lambat di luar batas backup tidak lagi masuk pool utama layanan AI

`fallback` dipertahankan karena Mihomo memilih node tersedia pertama berdasarkan urutan. Dengan demikian ranking kandidat lebih penting daripada perpindahan terus-menerus mengikuti perubahan latency kecil.

## Health-check

- Interval layanan AI: 300 detik
- `lazy: true`
- Timeout: 5000 ms
- `max-failed-times: 2`
- `AI-MANUAL` diperiksa paling cepat setiap 600 detik
- OpenAI diuji melalui `https://chatgpt.com/favicon.ico`
- Claude diuji melalui `https://claude.ai/favicon.ico`
- Gemini diuji melalui `https://gemini.google.com/favicon.ico`
- AI lain memakai `https://www.gstatic.com/generate_204`
- Expected HTTP status ditentukan secara eksplisit untuk menghindari node yang sekadar bisa tersambung tetapi gagal mengakses layanan

## Rule OpenAI dan ChatGPT

Rule kritis OpenAI ditempatkan sebelum adblock dan threat provider. Cakupan meliputi domain utama, autentikasi, static content, user content, WebSocket di bawah `chatgpt.com`, dan dependency yang tercantum pada panduan jaringan OpenAI.

ChatGPT Voice memakai dua lapisan:

1. Snapshot IP resmi sebagai rule `IP-CIDR` agar Voice masih punya jalur saat remote ruleset tidak bisa diambil
2. Provider `chatgpt_voice` berbasis ruleset Sukka yang dibangun dari `https://openai.com/chatgpt-voice.json` sehingga daftar dapat mengikuti perubahan upstream tanpa menangkap seluruh trafik UDP port 3478

Desain ini sengaja tidak memakai rule global `DST-PORT,3478` karena port yang sama dapat dipakai aplikasi TURN lain.

## Dynamic AI ruleset

Profil router memakai lapisan dinamis tambahan:

- `openai_domain` dari MetaCubeX `openai.mrs`
- `ai_category` dari MetaCubeX `category-ai-!cn.mrs`
- `chatgpt_voice` dari Sukka AI CIDR ruleset

Urutannya adalah static critical rules, dynamic AI ruleset, lalu YouTube/adblock/threat rules. Static rules menjadi fallback ketika provider eksternal belum tersedia.

Profil Android tetap menggunakan static AI domain rules dan text provider ChatGPT Voice. MRS domain provider tidak dipaksakan karena pipeline Android memiliki guard kompatibilitas untuk core yang menolak atau tidak stabil saat membaca provider MRS tertentu.

## DNS

Resolver umum `threat-safe` tetap memakai BebasID Family agar kebijakan keamanan lama tidak melemah. Domain AI utama mempunyai `nameserver-policy` khusus ke resolver non-filtered Cloudflare dan Google untuk mengurangi kegagalan akibat DNS filtering yang tidak relevan terhadap layanan AI.

`proxy-server-nameserver` tetap dipakai untuk resolusi hostname node proxy.

## Pipeline regenerasi

`local_runner.py` diperbaiki agar proses refresh tidak mengembalikan rule AI v1. Pipeline akhir mempertahankan urutan:

1. LAN dan private network
2. AI service guard
3. YouTube compatibility dan network ad rules
4. Threat, tracker, dan adblock provider
5. Routing kategori lain dan final route

Tahap YouTube guard juga sudah diperbaiki agar tidak lagi menyisipkan `REJECT` di depan rule AI setelah tahap security selesai.

`reference_profile_v047156.yaml` sudah membawa AI v2 sehingga `openclash_auto.yaml` tidak kehilangan konfigurasi ketika reference profile diterapkan ulang.

## TLS proxy

`skip-cert-verify` pada node yang sudah ada tidak dipaksa menjadi `false`. Sebagian node memakai pola bug-host, SNI, atau Cloudflare WebSocket yang dapat gagal bila certificate verification diubah tanpa tes langsung terhadap server. Pilihan ini menjaga kompatibilitas. Audit TLS per node dapat dilakukan terpisah bila endpoint dapat diuji langsung dari lingkungan OpenClash.

## File yang diperbarui

- `openclash_auto.yaml`
- `openclash_lite.yaml`
- `openclash_android.yaml`
- `openclash_fresh_pool.yaml`
- `reference_profile_v047156.yaml`
- `sumberyaml_core.py`
- `local_runner.py`
- `local_config.json`

## Validasi

- Python compile `sumberyaml_core.py`, `local_runner.py`, `generate_yaml.py`, dan validator: OK
- Parser YAML untuk seluruh output: OK
- Validator statis target OpenClash v0.47.156 + Mihomo alpha-ge183c58: OK
- Semua anggota proxy-group mengarah ke proxy atau group yang valid: OK
- Semua target policy rule valid: OK
- Semua `RULE-SET` memiliki provider yang sesuai: OK
- Tidak ada rule langsung yang kembali menargetkan alias legacy `AI`: OK
- AI guard berada sebelum rule `REJECT`: OK
- Simulasi reference profile, responsiveness, security, dan YouTube post-processing mempertahankan AI v2: OK

Binary `.local_bin/mihomo` di paket merupakan Mach-O ARM64 macOS, sehingga parser binary tersebut tidak dapat dijalankan pada lingkungan validasi Linux. Pemeriksaan target yang dapat dijalankan di lingkungan ini dilakukan dengan mode statis proyek.

## Rujukan teknis

- OpenAI network recommendations: https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps
- OpenAI Voice IP source: https://openai.com/chatgpt-voice.json
- Mihomo proxy-group documentation: https://wiki.metacubex.one/en/config/proxy-groups/
- MetaCubeX rule data: https://github.com/MetaCubeX/meta-rules-dat
- Sukka ruleset project: https://github.com/SukkaW/Surge
