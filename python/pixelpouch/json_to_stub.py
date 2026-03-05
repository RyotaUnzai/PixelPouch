import json
import re
from pathlib import Path

# =========================
# 型正規化
# =========================


def normalize_type(type_str: str | None) -> str:
    if not type_str:
        return "Any"
    if "void" in type_str:
        return "None"
    if "bool" in type_str:
        return "bool"
    if "int" in type_str:
        return "int"
    if "string" in type_str:
        return "str"
    if "Matrix4" in type_str:
        return "Matrix4"
    return "Any"


SIG_RE = re.compile(r"\((.*?)\)\s*(?:->\s*'(.+?)')?")


def parse_signature(sig: str):
    m = SIG_RE.search(sig)
    if not m:
        return [], "Any"

    args_raw, ret_raw = m.groups()
    args = []

    for arg in args_raw.split(","):
        arg = arg.strip()
        if arg in {"self", "/"}:
            continue

        if ":" in arg:
            name, typ = arg.split(":", 1)
            args.append(f"{name.strip()}: {normalize_type(typ)}")
        else:
            args.append(arg)

    return args, normalize_type(ret_raw)


# =========================
# 各ファイル生成
# =========================


def generate_classes(data: dict) -> str:
    lines = ["from typing import Any", ""]
    for name, obj in data.items():
        if obj.get("type") != "type":
            continue

        lines.append(f"class {name}:")
        members = obj.get("members", {})
        if not members:
            lines.append("    pass")
            lines.append("")
            continue

        for mname, minfo in members.items():
            sig = minfo.get("signature")
            if not sig:
                continue
            args, ret = parse_signature(sig)
            arg_str = ", ".join(["self"] + args)
            lines.append(f"    def {mname}({arg_str}) -> {ret}: ...")

        lines.append("")
    return "\n".join(lines)


def generate_functions(data: dict) -> str:
    lines = ["from typing import Any", ""]
    for name, obj in data.items():
        if obj.get("type") not in {"function", "builtin_function_or_method"}:
            continue

        sig = obj.get("signature")
        if not sig:
            continue

        args, ret = parse_signature(sig)
        arg_str = ", ".join(args)
        lines.append(f"def {name}({arg_str}) -> {ret}: ...")

    return "\n".join(lines)


def generate_constants(data: dict) -> str:
    lines = ["from typing import Any", ""]
    for name, obj in data.items():
        if obj.get("signature") is None and obj.get("type") != "type":
            lines.append(f"{name}: Any")
    return "\n".join(lines)


def generate_entry() -> str:
    return "\n".join(
        [
            "from ._hou_classes import *",
            "from ._hou_functions import *",
            "from ._hou_constants import *",
            "from .hou_ext import *",
            "",
        ]
    )


# =========================
# 実行
# =========================


def main():
    src = Path(r"Q:\Github\PixelPouch\python\stubs\hou.json")
    out_dir = Path(r"Q:\Github\PixelPouch\python\stubs\houdini")
    out_dir.mkdir(parents=True, exist_ok=True)

    data = json.loads(src.read_text(encoding="utf-8"))

    (out_dir / "_hou_classes.pyi").write_text(generate_classes(data), encoding="utf-8")
    (out_dir / "_hou_functions.pyi").write_text(
        generate_functions(data), encoding="utf-8"
    )
    (out_dir / "_hou_constants.pyi").write_text(
        generate_constants(data), encoding="utf-8"
    )
    (out_dir / "hou.pyi").write_text(generate_entry(), encoding="utf-8")

    print("Houdini stubs generated successfully")


if __name__ == "__main__":
    main()
