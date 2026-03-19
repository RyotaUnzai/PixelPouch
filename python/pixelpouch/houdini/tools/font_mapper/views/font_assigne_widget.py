from pathlib import Path
from typing import Optional

from pixelpouch.houdini.tools.font_mapper.views.ui_font_assigne_widget import Ui_Form
from pixelpouch.libs.core.environment_variable_key import PixelPouchEnvironmentVariables
from pixelpouch.libs.core.logging_factory import (
    PixelPouchLoggerFactory,
)
from PySide6 import QtGui, QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)

PP_ENV = PixelPouchEnvironmentVariables()
_HOUDINI_FONTS_DIR = PP_ENV.PIXELPOUCH_LOCATION / "houdini" / "fonts"
_fonts_loaded = False


def _load_project_fonts(path: Path) -> None:
    global _fonts_loaded
    if _fonts_loaded:
        return
    for font_file in path.glob("*.[ot]tf"):
        QtGui.QFontDatabase.addApplicationFont(str(font_file))
        logger.debug("Loaded font: %s", font_file.name)
    _fonts_loaded = True


class FontAssigneWidget(QtWidgets.QWidget):

    def __init__(
        self,
        fonts_dir: Path,
        target: str = "",
        fontfamily: str = "",
        style: str = "",
        parent: Optional[QtWidgets.QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)
        self._ui.label_target_role.setText(target)

        _load_project_fonts(fonts_dir)

        families = sorted(QtGui.QFontDatabase.families())
        self._ui.comboBox_fontfamily.addItems(families)

        if fontfamily:
            self._ui.comboBox_fontfamily.setCurrentText(fontfamily)

        self._update_styles(fontfamily, style)

        self._ui.comboBox_fontfamily.currentTextChanged.connect(self._on_family_changed)
        self._ui.pushButton_set_font.clicked.connect(self._on_open_font_dialog)

    def _update_styles(self, family: str, current_style: str = "") -> None:
        styles = QtGui.QFontDatabase.styles(family)
        self._ui.comboBox_style.clear()
        self._ui.comboBox_style.addItems(styles)
        if current_style and current_style in styles:
            self._ui.comboBox_style.setCurrentText(current_style)

    def _on_family_changed(self, family: str) -> None:
        self._update_styles(family)

    def _on_open_font_dialog(self) -> None:
        ok, font = QtWidgets.QFontDialog.getFont(parent=self)
        if ok:
            self._ui.comboBox_fontfamily.setCurrentText(font.family())
            self._update_styles(font.family(), QtGui.QFontDatabase.styleString(font))

    def font_map_entry(self) -> tuple[str, str]:
        """Returns (target, font_name) for font.map output."""
        target = self._ui.label_target_role.text()
        family = self._ui.comboBox_fontfamily.currentText()
        style = self._ui.comboBox_style.currentText()
        font_name = f"{family} {style}" if style and style != "Regular" else family
        return target, font_name
