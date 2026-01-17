from PySide6 import QtWidgets

from ..controller import NodePaletteController


class NodePaletteWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.controller = NodePaletteController()

        layout = QtWidgets.QVBoxLayout(self)

        btn = QtWidgets.QPushButton("Create Null")
        btn.clicked.connect(lambda: self.controller.create("null"))

        layout.addWidget(btn)
