from pathlib import Path
from typing import Optional

from pixelpouch.houdini.tools.font_mapper.views.ui_export_widget import Ui_Form
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from PySide6 import QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)


class ExportWidget(QtWidgets.QWidget):

    def __init__(
        self, export_path: Path, parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        super().__init__(parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._ui.lineEdit_exportpath.setText(export_path.as_posix())
        self._ui.pushButton_set_exportpath.clicked.connect(self.set_dir)

    def export_path(self) -> str:
        return self._ui.lineEdit_exportpath.text()

    def set_dir(self) -> None:
        current = self._ui.lineEdit_exportpath.text()
        path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Export Directory", current
        )
        if path:
            self._ui.lineEdit_exportpath.setText(path)
            logger.debug("Export path changed: %s", path)
