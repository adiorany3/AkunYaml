#!/usr/bin/env python3
from pathlib import Path
import yaml

PATH = Path(__file__).with_name('openclash_android.yaml')
DOMAIN = 'seabank.co.id'
RULE = f'DOMAIN-SUFFIX,{DOMAIN},DIRECT'
CRITICAL = (
    'RULE-SET,threat-malware,REJECT',
    'RULE-SET,threat-phishing,REJECT',
    'RULE-SET,threat-cryptominers,REJECT',
)


def fail(msg: str) -> None:
    raise SystemExit('[FAIL] ' + msg)

cfg = yaml.safe_load(PATH.read_text(encoding='utf-8')) or {}
if cfg.get('mode') != 'rule':
    fail('Android mode harus rule')

dns = cfg.get('dns') or {}
fake = [str(x) for x in dns.get('fake-ip-filter') or []]
if '+.' + DOMAIN not in fake:
    fail('SeaBank belum dikecualikan dari Fake-IP')

policy = dns.get('nameserver-policy') or {}
normal = policy.get('+.' + DOMAIN)
expected = ['https://1.1.1.1/dns-query', 'https://dns.google/dns-query']
if normal != expected:
    fail(f'Nameserver policy SeaBank bukan public DoH: {normal!r}')

skip = [str(x) for x in (cfg.get('sniffer') or {}).get('skip-domain') or []]
if '+.' + DOMAIN not in skip:
    fail('SeaBank belum masuk sniffer skip-domain')

rules = [str(x) for x in cfg.get('rules') or []]
if RULE not in rules:
    fail('Rule DIRECT SeaBank tidak ditemukan')
bi = rules.index(RULE)
for critical in CRITICAL:
    if critical not in rules or rules.index(critical) > bi:
        fail('Banking DIRECT harus berada setelah critical threat rules')

# Banking rule must be before marketplace/ad/tracker compatibility boundary.
for marker in (
    'DOMAIN-SUFFIX,shopee.co.id,GLOBAL',
    'RULE-SET,privacy-extra,REJECT',
    'RULE-SET,ads_domain,REJECT',
    'RULE-SET,tracker-domain,REJECT',
):
    if marker in rules and bi > rules.index(marker):
        fail(f'Banking DIRECT terlambat, berada setelah {marker}')

for r in rules:
    low = r.lower()
    if DOMAIN in low and ',reject' in low:
        fail(f'SeaBank masih memiliki explicit REJECT: {r}')

print('[OK] Android Banking Safe Mode')
print(f'  rule index       : {bi}')
print('  route            : DIRECT')
print('  fake-ip          : bypass')
print('  sniffer          : skipped')
print('  DNS              : public DoH policy')
