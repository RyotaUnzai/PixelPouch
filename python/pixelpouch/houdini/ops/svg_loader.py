"""Utilities for loading and caching SVG icons from ZIP archives.

This module provides helper functions to enumerate SVG files stored in a ZIP
archive and to load SVG data as QIcon objects. Loaded icons are cached in
memory to avoid redundant rendering and improve performance when the same
icons are requested multiple times.
"""

import zipfile
from pathlib import Path
from typing import Iterable

from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from PySide6 import QtCore, QtGui
from PySide6.QtSvg import QSvgRenderer

logger = PixelPouchLoggerFactory.get_logger(__name__)

IconCacheKey = tuple[str, str, int]
_ICON_CACHE: dict[IconCacheKey, QtGui.QIcon] = {}


def iter_svg_files_in_zip(zip_path: Path) -> Iterable[str]:
    """Iterates over SVG file paths stored in a ZIP archive.

    This function recursively enumerates all files in the ZIP archive and
    yields paths that end with the ``.svg`` extension. The returned paths
    are sorted lexicographically.

    Args:
        zip_path: Path to the ZIP archive.

    Yields:
        SVG file paths inside the ZIP archive.
    """
    with zipfile.ZipFile(zip_path) as zf:
        for name in sorted(zf.namelist()):
            if name.lower().endswith(".svg"):
                yield name


def load_svg_icon_from_zip(
    zip_path: Path,
    svg_path_in_zip: str,
    size: int,
) -> QtGui.QIcon:
    """Loads an SVG file from a ZIP archive and returns it as a QIcon.

    The rendered icon is cached using the ZIP path, SVG path, and icon size
    as the cache key. Subsequent calls with the same parameters return the
    cached icon without re-rendering.

    Args:
        zip_path: Path to the ZIP archive containing the SVG file.
        svg_path_in_zip: Path to the SVG file inside the ZIP archive.
        size: Width and height of the generated icon in pixels.

    Returns:
        A QIcon rendered from the SVG file.
    """
    key: IconCacheKey = (str(zip_path), svg_path_in_zip, size)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]

    with zipfile.ZipFile(zip_path) as zf:
        svg_bytes = zf.read(svg_path_in_zip)

    renderer = QSvgRenderer(QtCore.QByteArray(svg_bytes))
    if not renderer.isValid():
        logger.error(
            "Failed to load SVG icon from '%s' in ZIP '%s': invalid SVG data.",
            svg_path_in_zip,
            zip_path,
        )
        return QtGui.QIcon()

    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtCore.Qt.GlobalColor.transparent)

    painter = QtGui.QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    icon = QtGui.QIcon(pixmap)
    _ICON_CACHE[key] = icon
    return icon
