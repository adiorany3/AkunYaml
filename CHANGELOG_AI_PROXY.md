# AI Proxy Routing Update

Tanggal: 2026-08-18

## Tujuan
Membuat trafik layanan AI lebih stabil menggunakan proxy yang sudah tersedia tanpa melemahkan lapisan adblock dan threat-safe.

## Perubahan
- Menambahkan proxy-group `AI` bertipe `fallback` yang menggunakan node fisik secara langsung.
- Default health-check AI menggunakan `https://chatgpt.com/favicon.ico`.
- Interval health-check AI 120 detik, timeout 6000 ms, dan maksimal 3 kegagalan sebelum failover.
- Menambahkan routing khusus AI sebelum rule adblock, tracker, dan threat intelligence.
- Menjaga egress IP lebih stabil selama sesi AI karena `AI` tidak bergantung pada grup `url-test` yang dapat berganti node karena perubahan latency kecil.
- Menambahkan dukungan konfigurasi `AI_TEST_URL`, `AI_HEALTH_INTERVAL`, dan `AI_HEALTH_TIMEOUT_MS`.
- Memastikan post-processing `local_runner.py` mengembalikan AI rules setelah reference profile diterapkan.

## Layanan yang diarahkan ke AI
- OpenAI / ChatGPT / Sora
- Anthropic / Claude
- Google Gemini / AI Studio / Generative Language API / Vertex AI endpoint
- Microsoft Copilot / GitHub Copilot
- Perplexity
- xAI / Grok
- Poe
- DeepSeek
- Mistral
- Meta AI
- Qwen
- Kimi
- Cohere

## File keluaran yang diperbarui
- `openclash_auto.yaml`
- `openclash_lite.yaml`
- `openclash_android.yaml`
- `openclash_fresh_pool.yaml`
- `sumberyaml_core.py`
- `local_runner.py`
- `local_config.json`

## Validasi
- Python compile untuk `sumberyaml_core.py` dan `local_runner.py`: OK.
- Static OpenClash target validation untuk empat YAML: OK.
- Semua target rule mengarah ke proxy atau proxy-group yang valid: OK.
- Semua AI rules berada sebelum threat/adblock rules: OK.
- Simulasi reference-profile + security post-processing mempertahankan 28 AI rules dan group `AI`: OK.
- Binary `.local_bin/mihomo` tidak dapat dieksekusi di lingkungan Linux karena merupakan Mach-O ARM64 macOS. Ini bukan error pada YAML.
