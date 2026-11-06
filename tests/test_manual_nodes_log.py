"""Exercise the actual generator log expression without network/node checks."""
import ast
from pathlib import Path


def test_manual_summary_omits_skipped_count(capsys):
    source = Path(__file__).resolve().parents[1] / "generate_yaml.py"
    tree = ast.parse(source.read_text())
    summary = next(
        node for node in ast.walk(tree)
        if isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "print"
        and any(
            isinstance(part, ast.Constant)
            and isinstance(part.value, str)
            and "Manual nodes TCPing/compat passed:" in part.value
            for argument in node.value.args
            for part in ast.walk(argument)
        )
    )
    exec(compile(ast.Module(body=[summary], type_ignores=[]), str(source), "exec"), {  # noqa: S102 - execute only the local print expression
        "manual_nodes": [object()], "manual_skipped": ["failed one", "failed two"],
    })
    assert capsys.readouterr().out == "[INFO] Manual nodes TCPing/compat passed: 1\n"