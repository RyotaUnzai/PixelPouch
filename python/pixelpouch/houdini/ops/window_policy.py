from typing import Protocol

from hou_wrapper import hou
from PySide6 import QtCore, QtWidgets


class QtWindowProtocol(Protocol):
    def setParent(self, parent: QtWidgets.QWidget | None) -> None: ...
    def setWindowFlags(self, type: QtCore.Qt.WindowType) -> None: ...


def apply_standalone_window_policy(
    window: QtWindowProtocol,
    *,
    embed_in_houdini: bool,
) -> None:
    """
    Apply window parenting / flags policy for DCC environments.

    - Houdini:
        - Parent to hou.qt.mainWindow()
        - Force standalone window (not embedded)
    - Non-Houdini:
        - No-op

    Args:
        window:
            Any Qt widget/window supporting setParent / setWindowFlags.
        embed_in_houdini:
            If True, embed into Houdini UI.
            If False, force standalone window behavior.
    """
    main_window_getter = getattr(getattr(hou, "qt", None), "mainWindow", None)
    if not callable(main_window_getter):
        return

    if not embed_in_houdini:
        main_window = main_window_getter()
        if isinstance(main_window, QtWidgets.QWidget):
            window.setParent(main_window)
            window.setWindowFlags(QtCore.Qt.WindowType.Window)
