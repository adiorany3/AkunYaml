# AkunYaml v4.8 Precision Optimization

Version 4.8 focuses on structural and runtime efficiency without expanding the blocking surface.

## 1. MANUAL routing compression

`openclash_auto.yaml` previously carried a large contiguous block of MANUAL routing rules inline.

v4.8 moves this block into:

`rule_providers/manual-routing.yaml`

The main configuration now references it with:

```yaml
- RULE-SET,manual-routing,MANUAL
```

The provider uses `behavior: classical` because the original block contains a mix of `DOMAIN-SUFFIX`, `DOMAIN`, and `DOMAIN-KEYWORD` rules. This preserves the original matching semantics.

Measured result on the bundled configuration:

- Auto rules: 453 -> 180
- Auto YAML: 38,969 bytes -> 29,235 bytes
- Local MANUAL provider: 271 payload rules

## 2. Single-pass YAML post-processing

The optimization pipeline now keeps one in-memory YAML object for each output while applying:

1. sanitation
2. reference profile merge
3. network hardening
4. responsiveness tuning
5. security/adblock policy
6. YouTube compatibility policy
7. MRS substitution when validated
8. semantic deduplication
9. MANUAL provider compression
10. final sanitation

The file is serialized only once at the end of the transaction.

Self-test result:

- loads: 1
- writes: 1

A compatibility comparison with all v4.8-only transformations disabled produced the same parsed configuration as the v4.7 pipeline for Auto, Lite, Fresh Pool, and Android.

## 3. Conservative semantic deduplication

The optimizer removes only an exact `DOMAIN` rule when all of these conditions are true:

- an earlier `DOMAIN-SUFFIX` already covers the hostname
- both rules use the same policy
- the earlier rule therefore already determines the same result

The optimizer does not rewrite:

- `DOMAIN-KEYWORD`
- rules with different policies
- RULE-SET rules
- provider order
- later suffix rules
- Android by default

Router semantic audit after optimization: 0 safe overlaps remaining.

## 4. Validated MRS compilation

Validated Last-Known-Good text feeds can be compiled to local MRS only when a runnable Mihomo binary successfully performs the conversion.

Rules:

- only `domain` and `ipcidr` text providers are eligible
- `classical` providers are never converted
- source data must first pass Feed Guard
- conversion failure keeps the original text provider
- Android never receives this local MRS substitution

Default:

```json
"MRS_COMPILE": "auto"
```

The bundled Mihomo binary is macOS ARM64 and cannot execute in the Linux validation environment. Therefore the bundled YAML continues to use its existing provider formats. The MRS fallback path was verified with an isolated compiler self-test.

## 5. New settings

```json
{
  "MANUAL_ROUTING_COMPRESS": "true",
  "MANUAL_ROUTING_COMPRESS_THRESHOLD": "40",
  "SEMANTIC_RULE_OPTIMIZE": "router",
  "MRS_COMPILE": "auto"
}
```

`SEMANTIC_RULE_OPTIMIZE=router` intentionally leaves the Android output unchanged.

## 6. Compatibility

The bundled Android YAML is byte-identical to v4.7.

SHA-256:

`87fe571a19a225213ae5bd270dd3c8731f300dd0d6f420c81017264303b7db27`

Static validation target remains:

- OpenClash v0.47.156
- Mihomo alpha-ge183c58
