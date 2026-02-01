import json
from pathlib import Path
from typing import Any, Optional

import hou
from pixelpouch.houdini.tools.nodepalette.controller import NodePaletteController
from pixelpouch.houdini.tools.nodepalette.models.widgets_model import (
    WidgetListModel,
)
from pixelpouch.houdini.tools.nodepalette.views.ui_window import Ui_Form
from pixelpouch.houdini.tools.nodepalette.widget_factory import (
    WIDGET_FACTORY,
)
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from pixelpouch.libs.core.parsing.qss import loader
from PySide6 import QtCore, QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "node.json"
QSS_FILE = DATA_DIR / "main.qss"

SOP_CAT: hou.OpNodeTypeCategory = hou.sopNodeTypeCategory()
QSSLOADER = loader.QssLoader(DATA_DIR)


class NodePaletteWindow(QtWidgets.QWidget):
    ICON_SIZE = 60
    SPACING = 6
    ITEM_SIZE = ICON_SIZE + SPACING

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._ui.listWidget.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self._ui.listWidget.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self._ui.listWidget.setMovement(QtWidgets.QListView.Movement.Static)
        self._ui.listWidget.setSpacing(self.SPACING)
        self._ui.listWidget.setUniformItemSizes(True)
        self._ui.listWidget.setIconSize(QtCore.QSize(self.ICON_SIZE, self.ICON_SIZE))
        self._ui.listWidget.setGridSize(QtCore.QSize(self.ITEM_SIZE, self.ITEM_SIZE))
        self._ui.listWidget.setStyleSheet(QSSLOADER.load(QSS_FILE))

        with open(DATA_FILE) as f:
            data: dict[str, Any] = json.load(f)

        self.controller = NodePaletteController()

        self.widget_list_model = WidgetListModel.model_validate(data)
        self._create_widgets()
        self._setup_connections()

    def _create_widgets(self) -> None:
        for widget_model in self.widget_list_model.widgets:
            factory = WIDGET_FACTORY.get(widget_model.widget)
            if factory is None:
                logger.error(f"Unsupported widget type: {widget_model.widget}")
                continue
            node_type = hou.nodeType(SOP_CAT, widget_model.name)
            if node_type is None:
                logger.warning("NodeType not found: {widget_model.name}")
                continue

            item = QtWidgets.QListWidgetItem()
            item.setIcon(hou.qt.Icon(node_type.icon()))
            item.setToolTip(node_type.description())
            item.setData(QtCore.Qt.ItemDataRole.UserRole, node_type)
            self._ui.listWidget.addItem(item)

    def _setup_connections(self) -> None:
        self._ui.listWidget.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        node_type: hou.NodeType = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.controller.create(node_type=node_type.name())
