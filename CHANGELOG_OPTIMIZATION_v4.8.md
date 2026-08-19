# Changelog v4.8 Precision Optimization

## Added

- `manual_routing_provider.py`
- `mrs_compile.py`
- `semantic_rule_audit.py`
- `single_pass_yaml_audit.py`
- `optimization_v48_audit.py`
- `mrs_compile_selftest.py`
- local `manual-routing` classical rule-provider
- fail-open validated MRS compilation
- YAML transaction statistics

## Changed

- post-processing now uses one YAML load and one final write per output
- Auto MANUAL inline block is replaced in place by one RULE-SET reference
- router outputs remove only safe same-policy DOMAIN overlaps
- YouTube playback audit now validates effective REJECT coverage instead of requiring redundant exact rules
- strict hostname validation preserves original transport hostname spelling

## Preserved

- Android output remains byte-identical to v4.7
- threat protection remains enabled
- regional/global ad blocking remains enabled
- YouTube playback guard remains enabled
- marketplace and banking Android compatibility remain unchanged
- multi-host and cold fallback behavior remain unchanged

## Measured bundled output

| Output | v4.7 rules | v4.8 rules | v4.7 bytes | v4.8 bytes |
|---|---:|---:|---:|---:|
| Auto | 453 | 180 | 38,969 | 29,235 |
| Lite | 166 | 164 | 26,306 | 26,219 |
| Fresh Pool | 181 | 179 | 40,300 | 40,213 |
| Android | 375 | 375 | 33,114 | 33,114 |
