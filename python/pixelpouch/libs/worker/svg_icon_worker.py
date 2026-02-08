"""Background worker for rendering SVG icons into images.

This module provides a QRunnable-based worker that loads an SVG file from
a zip archive, renders it into a QImage using Qt's SVG renderer, and emits
the result asynchronously via Qt signals.
"""

import zipfile
from pathlib import Path

from PySide6 import QtCore, QtGui
from PySide6.QtSvg import QSvgRenderer


class SvgIconWorker(QtCore.QRunnable):
    """Worker that renders an SVG icon into a QImage in a background thread.

    This worker reads an SVG file from a zip archive, renders it at a fixed
    size into a transparent QImage, and emits the rendered image along with
    its associated row index when finished.
    """

    class Signals(QtCore.QObject):
        """Qt signals emitted by the SvgIconWorker.

        Attributes:
            finished: Signal emitted when rendering is complete. Provides
                the row index and the rendered QImage.
        """

        finished = QtCore.Signal(int, QtGui.QImage)

    def __init__(
        self,
        row: int,
        zip_path: Path,
        svg_path_in_zip: str,
        size: int,
    ) -> None:
        """Initializes the SVG icon worker.

        Args:
            row: Row index associated with the icon being rendered.
            zip_path: Path to the zip archive containing the SVG file.
            svg_path_in_zip: Internal path to the SVG file within the zip.
            size: Target width and height of the rendered image in pixels.
        """
        super().__init__()
        self.row = row
        self.zip_path = zip_path
        self.svg_path_in_zip = svg_path_in_zip
        self.size = size
        self.signals = SvgIconWorker.Signals()

    def run(self) -> None:
        """Executes the SVG rendering task.

        This method reads the SVG data from the zip archive, renders it into
        a transparent QImage using QSvgRenderer, and emits the finished
        signal with the resulting image.
        """
        with zipfile.ZipFile(self.zip_path) as zf:
            svg_bytes = zf.read(self.svg_path_in_zip)

        renderer = QSvgRenderer(QtCore.QByteArray(svg_bytes))

        image = QtGui.QImage(
            self.size,
            self.size,
            QtGui.QImage.Format.Format_ARGB32,
        )
        image.fill(QtCore.Qt.GlobalColor.transparent)

        painter = QtGui.QPainter(image)
        renderer.render(painter)
        painter.end()

        self.signals.finished.emit(self.row, image)
