Rule Provider Structure v4.2

Security:
- security-malware.yaml  : malware/phishing protection
- security-scam.yaml     : scam/fraud domains
- security-gambling.yaml : gambling domains
- security-adult.yaml    : adult content
- security-pinjol.yaml   : illegal loan patterns

Privacy:
- ads_indonesia_android.yaml

Policy:
- whitelist-common.yaml has higher priority than block rules.

Maintenance:
- Update interval recommended: 86400 seconds
- Avoid broad keyword blocking to reduce false positives
