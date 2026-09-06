from types import SimpleNamespace

from generate_yaml import _smart_select_nodes


def node(name: str, protocol: str, network: str, latency: int) -> SimpleNamespace:
    return SimpleNamespace(
        name=name,
        clash={"name": name, "type": protocol, "network": network},
        type=protocol,
        url_test_success=True,
        nekobox_ready=True,
        url_test_ms=latency,
        nekobox_test_ms=latency + 10,
        jitter_ms=5,
        attempts=3,
        success_count=3,
    )


def main() -> None:
    candidates = [
        node("fast-vless", "vless", "grpc", 30),
        node("fast-trojan", "trojan", "grpc", 40),
        node("video-vmess-1", "vmess", "ws", 100),
        node("video-vmess-2", "vmess", "ws", 110),
        node("video-vmess-3", "vmess", "ws", 120),
    ]
    selected = _smart_select_nodes(candidates, 2)
    assert len(selected) == 5
    assert sum("VMESS-VIDEO" in item.usage_groups for item in selected) == 3
    assert selected[0].name == "fast-vless"


if __name__ == "__main__":
    main()
