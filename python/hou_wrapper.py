from typing import TYPE_CHECKING

__all__ = ["hou"]

if TYPE_CHECKING:
    import hou
else:
    try:
        import hou
    except ImportError:
        from unittest.mock import MagicMock

        hou = MagicMock()
