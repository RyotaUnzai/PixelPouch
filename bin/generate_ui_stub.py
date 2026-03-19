"""Generate a .pyi stub for a pyside6-uic generated ui_*.py file.

Usage:
    python generate_ui_stub.py <input_ui_py> <output_pyi>
"""

import ast
import sys
from pathlib import Path


def _extract_setupui_attributes(tree: ast.Module) -> dict[str, str]:
    """Return {attr_name: type_name} for self.xxx = SomeClass(...) in setupUi."""
    attributes: dict[str, str] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if not (isinstance(item, ast.FunctionDef) and item.name == "setupUi"):
                continue
            for stmt in ast.walk(item):
                if not isinstance(stmt, ast.Assign):
                    continue
                for target in stmt.targets:
                    if not (
                        isinstance(target, ast.Attribute)
                        and isinstance(target.value, ast.Name)
                        and target.value.id == "self"
                    ):
                        continue
                    if not isinstance(stmt.value, ast.Call):
                        continue
                    func = stmt.value.func
                    if isinstance(func, ast.Name):
                        attributes[target.attr] = func.id
                    elif isinstance(func, ast.Attribute):
                        attributes[target.attr] = func.attr

    return attributes


def _extract_imports(tree: ast.Module) -> dict[str, str]:
    """Return {symbol_name: module_path} for all `from X import Y` statements."""
    imports: dict[str, str] = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        module = node.module or ""
        for alias in node.names:
            name = alias.asname or alias.name
            imports[name] = module

    return imports


def generate_pyi(py_path: Path) -> str:
    source = py_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    all_imports = _extract_imports(tree)
    attributes = _extract_setupui_attributes(tree)

    # Collect which modules are needed for the attribute types
    needed: dict[str, list[str]] = {}
    resolved: dict[str, str] = {}

    for attr, type_name in attributes.items():
        if type_name in all_imports:
            module = all_imports[type_name]
            needed.setdefault(module, [])
            if type_name not in needed[module]:
                needed[module].append(type_name)
            resolved[attr] = type_name
        else:
            resolved[attr] = type_name  # keep as-is (may be unresolved)

    lines: list[str] = []

    # Import lines (re-export style to match stubgen output)
    for module in sorted(needed):
        symbols = ", ".join(f"{n} as {n}" for n in sorted(needed[module]))
        lines.append(f"from {module} import {symbols}")

    if lines:
        lines.append("")

    # Class stub
    lines.append("class Ui_Form:")
    for attr, type_name in resolved.items():
        lines.append(f"    {attr}: {type_name}")
    lines.append("    def setupUi(self, Form) -> None: ...")
    lines.append("    def retranslateUi(self, Form) -> None: ...")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_ui.py> <output.pyi>")
        sys.exit(1)

    py_path = Path(sys.argv[1])
    pyi_path = Path(sys.argv[2])

    if not py_path.exists():
        print(f"Error: file not found: {py_path}", file=sys.stderr)
        sys.exit(1)

    content = generate_pyi(py_path)
    pyi_path.write_text(content, encoding="utf-8")
    print(f"Stub written to {pyi_path}")


if __name__ == "__main__":
    main()
