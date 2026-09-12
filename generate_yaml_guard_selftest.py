"""Offline regression for main's mandatory-manual and minimum-total guards."""
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import patch

import generate_yaml as generator


def check_guard(manual_count: int, automatic_count: int, minimum: int) -> None:
    manual = [SimpleNamespace(status="alive") for _ in range(manual_count)]
    automatic = [SimpleNamespace(status="alive") for _ in range(automatic_count)]
    with ExitStack() as stack:
        stack.enter_context(patch.dict(generator.os.environ, {
            "MIN_OUTPUT_NODES": str(minimum), "MAX_NODES": "10",
        }, clear=True))
        # Preserve source text: multi-host mode deliberately skips normalization.
        stack.enter_context(patch.object(generator, "TARGET_SERVERS", ["one.invalid", "two.invalid"]))
        stack.enter_context(patch.object(generator, "BUG_MODE", "fallback"))
        mocks = {}
        setup = {
            "_require_target_core": "offline-core",
            "build_links_text": "https://source.invalid/subscription",
            "_merge_saved_candidate_seed": "https://source.invalid/subscription",
            "_read_text_file": "manual fixture" if manual else "",
            "parse_manual_nodes_unscreened": (manual, []),
            "check_node_bug_compat": None,
            "process_sources": (automatic, automatic, [], []),
            "unique_names": None,
        }
        for name, value in setup.items():
            mocks[name] = stack.enter_context(patch.object(generator, name, return_value=value))
        mocks["compat"] = stack.enter_context(patch.object(
            generator, "_mihomo_openclash_compatibility_filter",
            side_effect=lambda nodes, **kwargs: (nodes, []),
        ))
        for name in ("_mihomo_url_test_nodes", "_singbox_url_test_nodes"):
            mocks[name] = stack.enter_context(patch.object(
                generator, name,
                side_effect=lambda nodes, **kwargs: (nodes, len(nodes), "offline pass", []),
            ))
        stack.enter_context(patch.object(
            generator, "_smart_select_nodes", side_effect=lambda nodes, limit: nodes[:limit],
        ))
        forbidden = []
        for name in (
            "build_openclash_yaml", "build_openclash_android_yaml",
            "_build_lite_yaml_from_text", "_build_node_quality_report",
            "_build_fresh_pool_report", "_build_fresh_pool_json",
            "build_csv", "build_akun_txt", "_build_singbox_android_json",
            "atomic_write_text", "validate_generated_text_with_core",
        ):
            forbidden.append(stack.enter_context(patch.object(
                generator, name, side_effect=AssertionError(f"Guard reached {name}"),
            )))
        for target in (
            "builtins.open", "pathlib.Path.open", "pathlib.Path.mkdir",
            "pathlib.Path.write_text", "pathlib.Path.write_bytes",
            "requests.sessions.Session.request", "socket.socket", "subprocess.Popen",
        ):
            forbidden.append(stack.enter_context(patch(
                target, side_effect=AssertionError(f"Unexpected I/O: {target}"),
            )))
        stack.enter_context(patch("builtins.print"))
        assert generator.main() == 3
        mocks["process_sources"].assert_called_once()
        assert mocks["_mihomo_url_test_nodes"].call_count == 2
        mocks["_singbox_url_test_nodes"].assert_called_once()
        assert mocks["_mihomo_url_test_nodes"].call_args_list[0].args[0] == automatic
        assert mocks["_mihomo_url_test_nodes"].call_args_list[1].args[0] == manual
        for mock in forbidden:
            mock.assert_not_called()


if __name__ == "__main__":
    check_guard(manual_count=0, automatic_count=3, minimum=2)
    check_guard(manual_count=1, automatic_count=1, minimum=3)
    print("PASS: 2 main guard cases; no builders, publication, network, or account I/O")
