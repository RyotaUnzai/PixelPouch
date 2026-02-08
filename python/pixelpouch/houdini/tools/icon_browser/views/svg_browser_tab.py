"""Qt widget representing a single SVG browser tab.

This module defines a QWidget used as a tab inside the SVG icon browser.
Each tab displays SVG icons belonging to a single folder within a ZIP
archive. Icons are shown in an icon-based list view with filtering and
lazy icon loading support.
"""

from pathlib import Path

from pixelpouch.houdini.tools.icon_browser.delegates.svg_icon_delegate import (
    SvgIconDelegate,
)
from pixelpouch.houdini.tools.icon_browser.models.svg_browser_model import (
    SvgZipListModel,
)
from pixelpouch.houdini.tools.icon_browser.models.svg_filter_model import (
    SvgFilterProxyModel,
)
from pixelpouch.houdini.tools.icon_browser.views.ui_svg_browser_tab import Ui_Form
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from PySide6 import QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)


class SvgBrowserTab(QtWidgets.QWidget):
    """Widget that displays SVG icons for a single folder.

    This widget combines a source model, filter proxy model, and custom
    item delegate to present SVG icons in an icon-based list view. It
    provides a small public API for search filtering and icon preloading.
    """

    def __init__(
        self,
        zip_path: Path,
        svg_paths: list[str],
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        """Initializes the SVG browser tab.

        Args:
            zip_path: Path to the ZIP archive containing SVG files.
            svg_paths: List of SVG file paths belonging to this tab.
            parent: Optional Qt parent widget.
        """
        super().__init__(parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)

        self._ui.listView.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        self._ui.listView.setResizeMode(QtWidgets.QListView.ResizeMode.Adjust)
        self._ui.listView.setSpacing(8)
        self._ui.listView.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection
        )

        self.source_model = SvgZipListModel(zip_path, svg_paths)
        self.proxy_model = SvgFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.source_model)

        self._ui.listView.setModel(self.proxy_model)
        self._ui.listView.setItemDelegate(SvgIconDelegate(self._ui.listView))

    # Public API
    def apply_search(self, text: str) -> None:
        """Applies a text-based filter to the SVG list.

        Args:
            text: Search text used to filter SVG entries.
        """
        self.proxy_model.setFilterRegularExpression(text)

    def preload_icons(self, limit: int = 15) -> None:
        """Preloads a limited number of SVG icons.

        This method triggers asynchronous icon generation for the first
        ``limit`` rows in the source model.

        Args:
            limit: Maximum number of icons to preload.
        """
        for row in range(min(limit, self.source_model.rowCount())):
            self.source_model.request_icon(row)
