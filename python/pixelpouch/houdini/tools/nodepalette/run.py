from pixelpouch.houdini.tools.nodepalette.views.window import NodePaletteWindow
from PySide6 import QtCore, QtWidgets


def run(parent: QtWidgets.QMainWindow) -> None:
    _window = NodePaletteWindow(parent)
    _window.setWindowFlags(QtCore.Qt.WindowType.Window)
    _window.resize(300, 200)
    _window.show()
