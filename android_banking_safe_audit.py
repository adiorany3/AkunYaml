#!/usr/bin/env python3
from pathlib import Path
import yaml

from android_banking_policy import suffix_domains

PATH = Path(__file__).with_name('openclash_android.yaml')
DOMAINS = suffix_domains()
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
policy = dns.get('nameserver-policy') or {}
skip = [str(x) for x in (cfg.get('sniffer') or {}).get('skip-domain') or []]
rules = [str(x) for x in cfg.get('rules') or []]
expected_dns = ['https://1.1.1.1/dns-query', 'https://dns.google/dns-query']

for domain in DOMAINS:
    if '+.' + domain not in fake:
        fail(f'{domain} belum dikecualikan dari Fake-IP')
    if policy.get('+.' + domain) != expected_dns:
        fail(f'Nameserver policy {domain} bukan public DoH: {policy.get("+." + domain)!r}')
    if '+.' + domain not in skip:
        fail(f'{domain} belum masuk sniffer skip-domain')

    rule = f'DOMAIN-SUFFIX,{domain},DIRECT'
    if rule not in rules:
        fail(f'Rule DIRECT {domain} tidak ditemukan')
    financial_index = rules.index(rule)
    for critical in CRITICAL:
        if critical not in rules or rules.index(critical) > financial_index:
            fail(f'{domain} DIRECT harus berada setelah critical threat rules')

    for marker in (
        'DOMAIN-SUFFIX,shopee.co.id,GLOBAL',
        'RULE-SET,privacy-extra,REJECT',
        'RULE-SET,ads_domain,REJECT',
        'RULE-SET,tracker-domain,REJECT',
    ):
        if marker in rules and financial_index > rules.index(marker):
            fail(f'{domain} DIRECT terlambat, berada setelah {marker}')

    for configured_rule in rules:
        if domain in configured_rule.lower() and ',reject' in configured_rule.lower():
            fail(f'{domain} masih memiliki explicit REJECT: {configured_rule}')

print('[OK] Android Banking/QRIS Safe Mode')
print(f'  protected sample : {len(DOMAINS)} domains')
print('  route             : DIRECT')
print('  fake-ip           : bypass')
print('  sniffer           : skipped')
print('  DNS               : public DoH policy')
