# AkunYaml

A suite of ad‑blocking audits for YAML based rule sets. It can audit Netflix playback safety, provider blocklists, app‑specific rules, streaming services, popup/game filters, and gambling‑sponsor detection.

## Features
- Configurable via `config.yaml` (override defaults for files, Netflix domains, broad‑block rules, and audit scripts).
- Flexible logging: console, optional file output, and debug mode (`-v/--verbose`).
- Self‑checks to ensure Netflix domains are never broad‑blocked.
- Simple CLI entry point (`python -m akunyaml.ads_audit` or `adaudit`).
- Unit‑tests with pytest and CI via GitHub Actions.

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the audit suite (JSON report)
python -m akunyaml.ads_audit --report audit.json

# Run with HTML report
python -m akunyaml.ads_audit --html-report audit.html
```
```bash
# Install dependencies
pip install -r requirements.txt

# Run the audit suite
python -m akunyaml.ads_audit

# With verbose logging and log file
python -m akunyaml.ads_audit -v --log-file audit.log
```

## Configuration
Create a `config.yaml` in the repository root to override defaults. See `config.yaml` example for the available keys.

## Development
- Run tests: `pytest -q`
- Lint: `ruff check .`
- Type‑check: `mypy .`

## Local workflow script
A convenience script `run_all.sh` is provided to install dependencies, lint, type‑check, and run tests in one step. Make it executable with `chmod +x run_all.sh` and execute `./run_all.sh`.

## License
MIT
