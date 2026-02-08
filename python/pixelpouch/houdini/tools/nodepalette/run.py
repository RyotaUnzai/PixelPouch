from typing import Optional

from pixelpouch.houdini.tools.nodepalette.views.window import NodePaletteWindow
from PySide6 import QtCore, QtWidgets


def run(parent: Optional[QtWidgets.QMainWindow] = None) -> None:
    window = NodePaletteWindow(parent)
    window.setWindowFlags(QtCore.Qt.WindowType.Window)
    window.resize(300, 200)
    window.show()


if __name__ == "__main__":
    run()
