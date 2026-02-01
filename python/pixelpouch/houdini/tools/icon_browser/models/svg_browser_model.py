"""Qt item model for displaying SVG entries from a ZIP archive.

This module provides a QAbstractListModel implementation that represents
SVG file paths stored inside a ZIP archive. Icons are generated lazily and
asynchronously using a worker and a global QThreadPool to avoid blocking
the UI thread.
"""

from pathlib import Path

from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from pixelpouch.libs.worker.svg_icon_worker import (
    SvgIconWorker,
)
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QThreadPool

logger = PixelPouchLoggerFactory.get_logger(__name__)


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
        self._thread_pool = QThreadPool.globalInstance()
        self._loading: set[int] = set()

    def rowCount(
        self,
        parent: QtCore.QModelIndex | None = None,
    ) -> int:
        """Returns the number of rows in the model.

        Args:
            parent: Parent model index (unused for list models).

        Returns:
            The number of SVG entries.
        """
        return len(self._svg_paths)

    def data(self, index: QtCore.QModelIndex, role: int) -> None | str:
        """Returns data for the given model index and role.

        Args:
            index: Model index identifying the row.
            role: Qt item data role.

        Returns:
            The SVG path string for DisplayRole, otherwise None.
        """
        if not index.isValid():
            return None

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self._svg_paths[index.row()]

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
        """Requests asynchronous icon generation for the given row.

        If the icon is already loaded or currently being generated, this
        method does nothing.

        Args:
            row: Row index of the SVG entry.
        """
        if row in self._icons or row in self._loading:
            return

        self._loading.add(row)

        worker = SvgIconWorker(
            row,
            self._zip_path,
            self._svg_paths[row],
            self._icon_size,
        )
        worker.signals.finished.connect(self._on_icon_ready)
        self._thread_pool.start(worker)

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
