# Target Fix Changelog

Target: OpenClash v0.47.156 + Mihomo Meta alpha-ge183c58 (`e183c58`).

## Fixed

- Fixed hidden backspace character in delay regex. `86MS` is now parsed as 86.
- Added exact Mihomo revision validation.
- Added final YAML static and Mihomo parser validation before output writes.
- Added duplicate proxy/group checks and dangling reference checks.
- Added proxy-group cycle detection.
- Added rule policy and RULE-SET provider validation.
- Added MRS provider validation.
- Added printable ASCII identifier validation for the OpenClash v0.47.156 target.
- Prevented `local_runner.py` from overwriting target-pinned generator files from another repository.
- Changed default reference mode from remote/locked to local-pinned.
- Added `reference_profile_v047156.yaml`.
- Fixed default security configuration mismatch that could access an undefined tracker provider.
- Added friendly exact-core failure output.
- Added `--mihomo-path` and development-only `--allow-non-target-core`.
- Added `validate_openclash_target.py`.
- Reworked `apply_existing.py` with backup, validation and automatic rollback.
- Added exact OpenClash/core version checks to router scripts.
- Added local `SOURCE_FILE` support to exact-core router isolation.
- Moved obsolete fixers to `legacy/` so they cannot accidentally become the normal workflow.
- Removed `.DS_Store` and `__pycache__` artifacts.
- Reduced Python requirements to the dependencies used by the active package.

## Validation performed on this package

- All active root Python files compile.
- All active shell scripts pass syntax validation.
- All four bundled YAML outputs pass the target static validator.
- No hidden control characters remain in active text/config files.
- Delay extraction test passes for `86MS` and `210MS`.
- Exact-core version gate accepts a simulated `alpha-ge183c58` version and rejects a non-target core.

A real Mihomo parser test must be run with the architecture-specific `alpha-ge183c58` binary on the target system. The binary is intentionally not bundled in this archive.
