#!/usr/bin/env python3
"""Benchmark DoH over HTTP/1.1 on this Mac; --self-test is offline.

Cold means first request of a new Session, not an empty resolver/system cache.
Warm means subsequent requests with connection reuse attempted, not guaranteed.
HTTP/2-only endpoints may fail here while working correctly in Mihomo.
"""
from __future__ import annotations

import argparse
import base64
import json
import math
import statistics
import struct
import time

import requests

RESOLVERS = {
    "Cloudflare": "https://1.1.1.1/dns-query",
    "Google": "https://dns.google/dns-query",
    "Quad9": "https://dns.quad9.net/dns-query",
    "AdGuard": "https://94.140.14.14/dns-query",
    "Cloudflare Family": "https://family.cloudflare-dns.com/dns-query",
    "BebasID Family": "https://family.dns.bebasid.com/dns-query",
}
DOMAINS = ("example.com", "github.com", "cloudflare.com")


def query(domain: str) -> bytes:
    labels = domain.encode("idna").split(b".")
    if any(not label or len(label) > 63 for label in labels):
        raise ValueError("Invalid DNS label")
    name = b"".join(bytes([len(label)]) + label for label in labels) + b"\0"
    if len(name) > 255:
        raise ValueError("DNS name too long")
    return struct.pack("!6H", 0, 0x0100, 1, 0, 0, 0) + name + struct.pack("!HH", 1, 1)


def validate_reply(data: bytes, sent: bytes) -> None:
    if len(data) < 12:
        raise ValueError("Truncated DNS header")
    ident, flags, questions, answers, _, _ = struct.unpack_from("!6H", data)
    if ident != 0 or not flags & 0x8000 or flags & 0x7A0F:
        raise ValueError("DNS error, truncation, or unexpected opcode")
    if questions != 1 or data[12:len(sent)] != sent[12:]:
        raise ValueError("DNS question mismatch")
    offset = len(sent)
    found = False
    for _ in range(answers):
        while True:
            if offset >= len(data):
                raise ValueError("Truncated answer name")
            length = data[offset]
            offset += 1
            if length == 0:
                break
            if length & 0xC0 == 0xC0:
                if offset >= len(data) or ((length & 63) << 8 | data[offset]) >= offset - 1:
                    raise ValueError("Invalid compression pointer")
                offset += 1
                break
            if length > 63 or offset + length > len(data):
                raise ValueError("Invalid answer label")
            offset += length
        if offset + 10 > len(data):
            raise ValueError("Truncated resource record")
        kind, cls, _, size = struct.unpack_from("!HHIH", data, offset)
        offset += 10
        if offset + size > len(data):
            raise ValueError("Truncated record data")
        if kind == 1 and cls == 1:
            if size != 4 or data[offset:offset + 4] in (b"\0" * 4, b"\x7f\0\0\x01"):
                raise ValueError("Invalid or blocked A answer")
            found = True
        offset += size
    if not found:
        raise ValueError("No positive A answer")


def self_test() -> None:
    sent = query("example.com")
    answer = b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 60, 4) + b"\x5d\xb8\xd8\x22"
    reply = struct.pack("!6H", 0, 0x8180, 1, 1, 0, 0) + sent[12:] + answer
    validate_reply(reply, sent)
    for bad in (b"", reply[:-1], reply[:3] + b"\x83" + reply[4:],
                reply[:2] + b"\x83\x80" + reply[4:],
                reply[:-4] + b"\0" * 4,
                reply[:len(sent)] + b"\xff\xff" + answer[2:]):
        try:
            validate_reply(bad, sent)
        except ValueError:
            continue
        raise AssertionError("Malformed reply accepted")
    try:
        validate_reply(reply, query("invalid.com"))
    except ValueError:
        pass
    else:
        raise AssertionError("Mismatched question accepted")
    print("DNS benchmark self-test: PASS")


def benchmark(rounds: int) -> list[dict]:
    results = {name: {"resolver": name, "url": url, "cold_ms": None,
                      "warm_ms": [], "errors": []} for name, url in RESOLVERS.items()}
    sessions = {name: requests.Session() for name in RESOLVERS}
    try:
        for session in sessions.values():
            # ponytail: measure this Mac without environment HTTP proxies;
            # benchmark on router/Android separately before changing their DNS.
            session.trust_env = False
        names = list(RESOLVERS)
        for index in range(rounds * len(DOMAINS)):
            sent = query(DOMAINS[index % len(DOMAINS)])
            encoded = base64.urlsafe_b64encode(sent).rstrip(b"=").decode("ascii")
            shift = index % len(names)
            for name in names[shift:] + names[:shift]:
                result = results[name]
                start = time.perf_counter()
                try:
                    with sessions[name].get(
                        RESOLVERS[name], params={"dns": encoded},
                        headers={"Accept": "application/dns-message"},
                        timeout=(3, 5), allow_redirects=False, stream=True,
                    ) as response:
                        if response.status_code != 200:
                            raise ValueError(f"HTTP {response.status_code}")
                        if response.headers.get("Content-Type", "").split(";")[0].strip().lower() != "application/dns-message":
                            raise ValueError("Unexpected content type")
                        data = bytearray()
                        for chunk in response.iter_content(4096):
                            data.extend(chunk)
                            if len(data) > 65535:
                                raise ValueError("Oversized DNS response")
                        validate_reply(bytes(data), sent)
                    elapsed = round((time.perf_counter() - start) * 1000, 2)
                    if index == 0:
                        result["cold_ms"] = elapsed
                    else:
                        result["warm_ms"].append(elapsed)
                except (requests.RequestException, ValueError) as exc:
                    result["errors"].append(f"{DOMAINS[index % len(DOMAINS)]}: {exc}")
    finally:
        for session in sessions.values():
            session.close()
    for result in results.values():
        warm = sorted(result.pop("warm_ms"))
        result["successes"] = len(warm) + int(result["cold_ms"] is not None)
        result["attempts"] = rounds * len(DOMAINS)
        result["warm_median_ms"] = round(statistics.median(warm), 2) if warm else None
        result["warm_p95_ms"] = warm[math.ceil(len(warm) * 0.95) - 1] if warm else None
    return sorted(results.values(), key=lambda item: (len(item["errors"]), item["warm_median_ms"] or math.inf))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--rounds", type=int, choices=range(1, 11), default=3)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        print(json.dumps(benchmark(args.rounds), indent=2))
