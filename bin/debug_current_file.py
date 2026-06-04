from __future__ import annotations

import runpy
import sys
from pathlib import Path


def _infer_module_name(
    file_path: Path, workspace_root: Path
) -> tuple[str | None, Path]:
    """Infer a module name and import root from a Python file path."""

    python_root = workspace_root / "python"
    if python_root.exists() and python_root in file_path.parents:
        relative_path = file_path.relative_to(python_root)
        if file_path.name == "__init__.py":
            module_parts = relative_path.parent.parts
        else:
            module_parts = relative_path.with_suffix("").parts

        if not module_parts:
            return None, python_root

        return ".".join(module_parts), python_root

    package_parts: list[str] = []
    current = file_path.parent

    while (current / "__init__.py").exists():
        package_parts.append(current.name)
        current = current.parent

    if not package_parts:
        return None, file_path.parent

    package_parts.reverse()
    if file_path.name != "__init__.py":
        package_parts.append(file_path.stem)

    return ".".join(package_parts), current


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"Usage: {Path(argv[0]).name} <python_file>")
        return 1

    file_path = Path(argv[1]).resolve()
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return 2

    workspace_root = Path(__file__).resolve().parent.parent
    module_name, import_root = _infer_module_name(file_path, workspace_root)
    sys.path.insert(0, str(import_root))

    if module_name is None:
        runpy.run_path(str(file_path), run_name="__main__")
        return 0

    runpy.run_module(module_name, run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
