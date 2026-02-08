"""Node palette window implementation for Houdini.

This module defines a Qt-based window that displays a palette of Houdini
SOP nodes as selectable widgets. Node definitions are loaded from a JSON
configuration file, styled using a QSS stylesheet, and instantiated via
a widget factory. Selecting an item triggers node creation through the
associated controller.
"""

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
    """Main window for displaying and interacting with a node palette.

    This widget presents a grid-based icon view of available Houdini SOP
    node types. Node metadata is loaded from a JSON file, icons are resolved
    via Houdini's API, and user interaction is delegated to a controller
    responsible for node creation.
    """

    ICON_SIZE = 60
    SPACING = 6
    ITEM_SIZE = ICON_SIZE + SPACING

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        """Initializes the node palette window.

        This sets up the UI layout, configures the list widget appearance,
        loads node configuration data, initializes the controller and models,
        and establishes signal connections.

        Args:
            parent: Optional parent widget.
        """
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
        """Creates and populates list widget items from the widget model.

        For each widget definition, this method resolves the corresponding
        Houdini node type, creates a list item with icon and metadata, and
        adds it to the list widget. Unsupported widget types or missing
        node types are logged and skipped.
        """
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
        """Sets up Qt signal-slot connections for the window."""
        self._ui.listWidget.itemClicked.connect(self._on_item_clicked)

    def _on_item_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        """Handles list item selection and triggers node creation.

        The selected item's associated Houdini node type is retrieved and
        passed to the controller to create a new node instance.

        Args:
            item: The list widget item that was clicked.
        """
        node_type: hou.NodeType = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.controller.create(node_type=node_type.name())
