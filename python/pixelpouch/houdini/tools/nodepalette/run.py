from PySide6 import QtCore

from .views.window import NodePaletteWindow

_window = None


def run(parent) -> None:
    global _window

    if _window:
        _window.raise_()
        _window.activateWindow()
        return

    _window = NodePaletteWindow(parent)
    _window.setWindowFlags(QtCore.Qt.Window)
    _window.resize(300, 200)
    
    _window.destroyed.connect(_on_window_destroyed)
    _window.show()


def _on_window_destroyed():
    global _window
    _window = None