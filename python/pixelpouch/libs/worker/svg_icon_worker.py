import zipfile
from pathlib import Path

from PySide6 import QtCore, QtGui
from PySide6.QtSvg import QSvgRenderer


class SvgIconWorker(QtCore.QRunnable):
    """
    SVG をバックグラウンドで QImage まで生成する Worker
    """

    class Signals(QtCore.QObject):
        finished = QtCore.Signal(int, QtGui.QImage)

    def __init__(
        self,
        row: int,
        zip_path: Path,
        svg_path_in_zip: str,
        size: int,
    ) -> None:
        super().__init__()
        self.row = row
        self.zip_path = zip_path
        self.svg_path_in_zip = svg_path_in_zip
        self.size = size
        self.signals = SvgIconWorker.Signals()

    def run(self) -> None:
        with zipfile.ZipFile(self.zip_path) as zf:
            svg_bytes = zf.read(self.svg_path_in_zip)

        renderer = QSvgRenderer(QtCore.QByteArray(svg_bytes))

        image = QtGui.QImage(
            self.size,
            self.size,
            QtGui.QImage.Format_ARGB32,
        )
        image.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(image)
        renderer.render(painter)
        painter.end()

        self.signals.finished.emit(self.row, image)
