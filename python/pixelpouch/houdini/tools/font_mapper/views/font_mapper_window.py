from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pixelpouch.houdini.tools.font_mapper.models.font_map_model import FontMapListModel
from pixelpouch.houdini.tools.font_mapper.views.export_widget import ExportWidget
from pixelpouch.libs.core.logging_factory import (
    PixelPouchLoggerFactory,
)
from PySide6 import QtWidgets

if TYPE_CHECKING:
    from pixelpouch.houdini.tools.font_mapper.views.font_assigne_widget import (
        FontAssigneWidget,
    )

logger = PixelPouchLoggerFactory.get_logger(__name__)


class HoudiniFontMapper(QtWidgets.QWidget):

    def __init__(
        self, export_path: Path, parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        """Initializes the icon browser window.

        Args:
            zip_path: Path to the ZIP archive containing SVG files.
            parent: Optional Qt parent widget.
        """
        super().__init__(parent)
        self._export_widget = ExportWidget(parent=parent, export_path=export_path)
        self._pushbutton_export = QtWidgets.QPushButton("Export font.map")

        listmodel = FontMapListModel.load_from_json()
        self._font_assigne_widgets: list[FontAssigneWidget] = listmodel.create_widgets(
            fonts_dir=export_path, parent=self
        )

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self._export_widget)
        for widget in self._font_assigne_widgets:
            layout.addWidget(widget)

        verticalSpacer = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

        layout.addItem(verticalSpacer)
        layout.addWidget(self._pushbutton_export)

        self._pushbutton_export.clicked.connect(self._export_font_map)

    def _export_font_map(self) -> None:
        export_dir = Path(self._export_widget.export_path())
        if not export_dir.exists():
            QtWidgets.QMessageBox.warning(
                self, "Export", f"Directory not found:\n{export_dir}"
            )
            return

        lines = ["# A flat list of UI font usage to font name mappings"]
        for widget in self._font_assigne_widgets:
            target, font_name = widget.font_map_entry()
            col = len(target)
            tabs = ""
            while col < 24:
                tabs += "\t"
                col = (col // 8 + 1) * 8
            lines.append(f'{target}{tabs}"{font_name}"')

        output_path = export_dir / "font.map"
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        logger.debug("Exported font.map to %s", output_path)
