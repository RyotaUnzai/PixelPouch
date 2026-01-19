from PySide6 import QtCore

from .views.window import NodePaletteWindow


def run(parent) -> None:
    _window = NodePaletteWindow(parent)
    _window.setWindowFlags(QtCore.Qt.Window)
    _window.resize(300, 200)
    _window.show()
