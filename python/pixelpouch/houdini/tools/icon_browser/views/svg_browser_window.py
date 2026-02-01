"""Qt window for browsing and selecting SVG icons from a ZIP archive.

This module defines a QWidget-based window that allows users to browse,
filter, and select SVG icons stored inside a ZIP archive. SVG files are
grouped by folder and presented in tabbed views with lazy icon loading
to maintain UI responsiveness.
"""

from pathlib import Path
from typing import Optional

from pixelpouch.houdini.ops.svg_category import regroup_svgs_for_ui
from pixelpouch.houdini.tools.icon_browser.views import (
    SvgBrowserTab,
)
from pixelpouch.houdini.tools.icon_browser.views.ui_svg_browser_window import Ui_Form
from pixelpouch.libs.core.logging_factory import (
    PixelPouchLoggerFactory,
)
from pixelpouch.libs.core.qt.widgets import WheelTabBar
from PySide6 import QtCore, QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)


CATEGORY_JSON_PATH = Path(__file__).parents[1] / "data/svg_category_map.json"


class HoudiniIconBrowserWindow(QtWidgets.QWidget):
    """Main window for browsing SVG icons contained in a ZIP archive.

    This widget groups SVG files by their folder structure, displays each
    group in a separate tab, supports text-based filtering, and reflects
    the currently selected SVG entry. Icons are preloaded lazily on a
    per-tab basis.
    """

    def __init__(
        self, zip_path: Path, parent: Optional[QtWidgets.QWidget] = None
    ) -> None:
        """Initializes the icon browser window.

        Args:
            zip_path: Path to the ZIP archive containing SVG files.
            parent: Optional Qt parent widget.
        """
        super().__init__(parent)
        self._ui = Ui_Form()
        self._ui.setupUi(self)

        self._ui.lineEdit_search_edit.textChanged.connect(self._on_search)
        self._ui.lineEdit_selected_edit.setReadOnly(True)
        self._ui.tabWidget.setTabBar(WheelTabBar())
        self._ui.tabWidget.currentChanged.connect(self._on_tab_changed)

        self._zip_path = zip_path
        self._preloaded_tabs: set[int] = set()

        self.setWindowTitle("Houdini Icon Browser")
        self.resize(1000, 720)

        groups = regroup_svgs_for_ui(
            zip_path=self._zip_path,
            category_map_path=CATEGORY_JSON_PATH,
        )
        if not groups:
            logger.warning("No SVG files found in zip: %s", self._zip_path)

        for category, svg_paths in groups.items():
            tab = SvgBrowserTab(
                zip_path=self._zip_path,
                svg_paths=svg_paths,
                parent=self._ui.tabWidget,
            )

            tab._ui.listView.selectionModel().currentChanged.connect(
                self._on_selection_changed
            )

            self._ui.tabWidget.addTab(tab, category)

    def _current_tab(self) -> SvgBrowserTab | None:
        """Returns the currently active SVG browser tab.

        Returns:
            The current SvgBrowserTab instance if available, otherwise None.
        """
        tab = self._ui.tabWidget.currentWidget()
        return tab if isinstance(tab, SvgBrowserTab) else None

    def _on_search(self, text: str) -> None:
        """Applies a search filter to the active tab.

        Args:
            text: Search text entered by the user.
        """
        tab = self._current_tab()
        if tab:
            tab.apply_search(text)

    def _on_selection_changed(
        self,
        current: QtCore.QModelIndex,
        _: QtCore.QModelIndex,
    ) -> None:
        tab = self._current_tab()
        if not tab or not current.isValid():
            self._ui.lineEdit_selected_edit.clear()
            return

        source_index = tab.proxy_model.mapToSource(current)
        self._ui.lineEdit_selected_edit.setText(source_index.data())

    def _on_tab_changed(self, index: int) -> None:
        """Handles tab change events.

        This method reapplies the current search filter, preloads icons for
        the tab on first activation, and updates the selected SVG display.

        Args:
            index: Index of the newly activated tab.
        """
        tab = self._current_tab()
        if not tab:
            return

        # Preserve the current search filter
        tab.apply_search(self._ui.lineEdit_search_edit.text())

        # Preload icons on first activation only
        if index not in self._preloaded_tabs:
            self._preloaded_tabs.add(index)
            tab.preload_icons(limit=15)

        # Update the selected SVG display
        sel = tab._ui.listView.currentIndex()
        if sel.isValid():
            self._on_selection_changed(sel, QtCore.QModelIndex())
        else:
            self._ui.lineEdit_selected_edit.clear()
