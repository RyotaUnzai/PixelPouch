from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


class QssLoaderError(RuntimeError):
    """Raised when QSS loading or parsing fails."""


# =========================
# Regex Models
# =========================


@dataclass(frozen=True)
class ImportRule:
    """Model for @import url("..."); rules."""

    pattern: re.Pattern[str]


@dataclass(frozen=True)
class RootVarPattern:
    """Patterns for :root variable parsing."""

    root_block: re.Pattern[str]
    variable: re.Pattern[str]
    var_call: re.Pattern[str]


IMPORT_RULE = ImportRule(pattern=re.compile(r'@import\s+url\("([^"]+)"\);'))

ROOT_VAR_PATTERN = RootVarPattern(
    root_block=re.compile(r":root\s*\{.*?\}", re.DOTALL),
    variable=re.compile(r"--([\w-]+)\s*:\s*([^;]+);"),
    var_call=re.compile(r"var\(\s*--([\w-]+)\s*\)"),
)


# =========================
# Loader
# =========================


class QssLoader:
    """
    QSS loader and parser.

    Responsibilities:
    - Load QSS files
    - Resolve @import rules safely
    - Expand :root variables

    Notes:
    - Qt / PySide / PyQt independent
    - Python 3.11+
    - pytest / mypy / pyright friendly
    """

    def __init__(self, root: Path) -> None:
        self._root = root.resolve()

    def load(self, path: Path) -> str:
        """
        Load and process a QSS file.

        Args:
            path: Path to the root QSS file.

        Returns:
            Processed QSS content.

        Raises:
            QssLoaderError: On invalid path, import failure, or parsing error.
        """
        path = path.resolve()

        if not path.is_file():
            raise QssLoaderError(f"QSS file not found: {path}")

        content = path.read_text(encoding="utf-8-sig")
        content = self._resolve_imports(content, base_dir=path.parent)
        content = self._expand_root_variables(content)
        return content

    # -------------------------
    # Internal processing
    # -------------------------

    def _resolve_imports(self, content: str, base_dir: Path) -> str:
        for match in IMPORT_RULE.pattern.finditer(content):
            relative_path = match.group(1)
            target = (base_dir / relative_path).resolve()

            if not target.is_file():
                raise QssLoaderError(f"Imported QSS not found: {relative_path}")

            # Security: prevent path traversal
            if not target.is_relative_to(self._root):
                raise QssLoaderError(f"Illegal @import path: {relative_path}")

            imported = target.read_text(encoding="utf-8-sig")
            content = content.replace(match.group(0), imported)

        return content

    def _expand_root_variables(self, content: str) -> str:
        variables: dict[str, str] = {}

        for block in ROOT_VAR_PATTERN.root_block.findall(content):
            for name, value in ROOT_VAR_PATTERN.variable.findall(block):
                variables[name] = value.strip()
            content = content.replace(block, "")

        def replacer(m: re.Match[str]) -> str:
            name = m.group(1)
            return variables.get(name, m.group(0))

        return ROOT_VAR_PATTERN.var_call.sub(replacer, content)
