"""Qt item model for displaying SVG entries from a ZIP archive.

This module provides a QAbstractListModel implementation that represents
SVG file paths stored inside a ZIP archive. Icons are generated lazily and
asynchronously using a worker and a global QThreadPool to avoid blocking
the UI thread.
"""

from pathlib import Path, PurePosixPath
from types import ModuleType
from typing import TYPE_CHECKING, Optional

from pixelpouch.libs.core.environment_variable_key import (
    ExecutionContextEnv,
    PixelPouchEnvironmentVariables,
)
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from pixelpouch.libs.worker.svg_icon_worker import SvgIconWorker
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThreadPool

if TYPE_CHECKING:
    from types import ModuleType


logger = PixelPouchLoggerFactory.get_logger(__name__)

PP_ENV = PixelPouchEnvironmentVariables()


class SvgZipListModel(QtCore.QAbstractListModel):
    """List model that exposes SVG paths and lazily generated icons.

    Each row corresponds to a single SVG file path inside a ZIP archive.
    Icons are generated on demand in background threads and cached once
    loaded.
    """

    def __init__(
        self,
        zip_path: Path,
        svg_paths: list[str],
        icon_size: int = 32,
        parent: QtCore.QObject | None = None,
    ) -> None:
        """Initializes the SVG ZIP list model.

        Args:
            zip_path: Path to the ZIP archive containing SVG files.
            svg_paths: List of SVG file paths inside the ZIP archive.
            icon_size: Size of the generated icons in pixels.
            parent: Optional Qt parent object.
        """
        super().__init__(parent)
        self._zip_path = zip_path
        self._svg_paths = svg_paths
        self._icon_size = icon_size

        self._icons: dict[int, QtGui.QIcon] = {}
        self._loading: set[int] = set()

        self._thread_pool = QThreadPool.globalInstance()

        # --------------------------------------------------
        # Execution context detection (PixelPouch standard)
        self._hou: Optional[ModuleType]

        if PP_ENV.PIXELPOUCH_EXECUTION_CONTEXT == ExecutionContextEnv.HOUDINI:
            import hou

            self._hou = hou
        else:
            self._hou = None

    def rowCount(
        self,
        parent: QtCore.QModelIndex | QtCore.QPersistentModelIndex | None = None,
    ) -> int:
        """Returns the number of rows in the model.

        Args:
            parent: Parent model index (unused for list models).

        Returns:
            The number of SVG entries.
        """
        return len(self._svg_paths)

    def data(
        self,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> None | str:
        """Returns data for the given model index and role.

        Args:
            index: Model index identifying the row.
            role: Qt item data role.

        Returns:
            The SVG path string for DisplayRole, otherwise None.
        """
        if not index.isValid():
            return None

        row = index.row()

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._svg_paths[row]

        return None

    def get_icon(self, row: int) -> QtGui.QIcon | None:
        """Returns the cached icon for a given row, if available.

        Args:
            row: Row index of the SVG entry.

        Returns:
            The corresponding QIcon if loaded, otherwise None.
        """
        return self._icons.get(row)

    def request_icon(self, row: int) -> None:
        """Requests asynchronous icon generation for the specified row.

        This method initiates icon loading if the icon has not already been
        generated and is not currently being loaded. It first attempts to
        retrieve the icon from Houdini, and if that fails, falls back to
        generating the icon from an SVG file inside a zip archive.

        Args:
            row: Index of the row corresponding to the SVG entry.
        """
        if row in self._icons or row in self._loading:
            return

        self._loading.add(row)

        if self._try_houdini_icon(row):
            return

        self._request_zip_icon(row)

    def _try_houdini_icon(self, row: int) -> bool:
        """Attempts to load an icon using Houdini's built-in icon system.

        If Houdini is available and the icon exists, the icon is stored,
        the loading state is cleared, and the model is notified of the data
        change.

        Args:
            row: Index of the row corresponding to the SVG entry.

        Returns:
            True if the icon was successfully loaded from Houdini; otherwise False.
        """
        if self._hou is None:
            return False

        name = self._make_houdini_icon_name(row)

        try:
            icon = self._hou.qt.Icon(name)
        except self._hou.OperationFailed:
            logger.debug("Houdini icon not found: %s", name)
            return False

        self._icons[row] = icon
        self._loading.discard(row)

        idx = self.index(row)
        self.dataChanged.emit(idx, idx)
        return True

    def _request_zip_icon(self, row: int) -> None:
        """Requests icon generation from an SVG file inside a zip archive.

        This method creates a worker responsible for loading and rendering
        the SVG icon asynchronously, connects its completion signal, and
        schedules it on the thread pool.

        Args:
            row: Index of the row corresponding to the SVG entry.
        """
        worker = SvgIconWorker(
            row=row,
            zip_path=self._zip_path,
            svg_path_in_zip=self._svg_paths[row],
            size=self._icon_size,
        )
        worker.signals.finished.connect(self._on_icon_ready)
        self._thread_pool.start(worker)

    def _make_houdini_icon_name(self, row: int) -> str:
        """Constructs a Houdini icon name from the SVG path at the given row.

        The icon name is generated by combining the parent directory name
        and the file stem of the SVG path.

        Args:
            row: Index of the row corresponding to the SVG entry.

        Returns:
            A string representing the Houdini icon name.
        """
        path = PurePosixPath(self._svg_paths[row])
        return f"{path.parent.name}_{path.stem}"

    @QtCore.Slot(int, QtGui.QImage)
    def _on_icon_ready(self, row: int, image: QtGui.QImage) -> None:
        """Handles completion of asynchronous icon generation.

        This slot converts the generated image to a QIcon, stores it in the
        cache, and emits the appropriate dataChanged signal.

        Args:
            row: Row index of the generated icon.
            image: Generated icon image.
        """
        pixmap = QtGui.QPixmap.fromImage(image)
        self._icons[row] = QtGui.QIcon(pixmap)
        self._loading.discard(row)

        idx = self.index(row)
        self.dataChanged.emit(idx, idx)
