import json
from functools import partial
from pathlib import Path
from typing import Optional

import hou
from pixelpouch.houdini.tools.nodepalette.controller import NodePaletteController
from pixelpouch.houdini.tools.nodepalette.models.widgets_model import (
    WidgetListModel,
)
from pixelpouch.houdini.tools.nodepalette.views.ui_window import Ui_Form
from pixelpouch.houdini.tools.nodepalette.widget_factory import (
    WIDGET_FACTORY,
)
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory
from PySide6 import QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_FILE = DATA_DIR / "node.json"


class NodePaletteWindow(QtWidgets.QWidget):
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)

        self._ui = Ui_Form()
        self._ui.setupUi(self)

        with open(DATA_FILE) as f:
            data: dict = json.load(f)
        self.controller = NodePaletteController()

        widget_list_model = WidgetListModel.model_validate(data)

        sop_cat = hou.sopNodeTypeCategory()
        for widget_model in widget_list_model.widgets:
            factory = WIDGET_FACTORY.get(widget_model.widget)
            if factory is None:
                logger.error(
                    "Unsupported widget type: %s",
                    widget_model.widget,
                )
                continue

            widget = factory(widget_model.name)
            if isinstance(widget, QtWidgets.QPushButton):
                widget.clicked.connect(
                    partial(self.controller.create, node_type=widget_model.name)
                )
                node_type = hou.nodeType(sop_cat, widget_model.name)
                widget.setIcon(hou.qt.Icon("PLASMA_App"))

            self._ui.verticalLayout.addWidget(widget)

    def _on_create_clicked(self, node_type: str) -> None:
        self.controller.create(node_type=node_type)


"""
import sys
from importlib import reload

for name, module in list(sys.modules.items()):
    if "nodepalette" in name and module is not None:
        try:
            reload(module)
            print(f"reloaded: {name}")
        except Exception as e:
            print(f"failed: {name} -> {e}")

"""
