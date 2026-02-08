"""Utilities for grouping SVG files inside a ZIP archive.

This module provides helper functions for organizing SVG files stored in a ZIP
archive. SVG paths are grouped by their top-level folder to support structured
browsing and presentation in UI components.
"""

import zipfile
from collections import defaultdict
from pathlib import Path

from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)


def group_svgs_by_folder(zip_path: Path) -> dict[str, list[str]]:
    """Groups SVG files in a ZIP archive by their top-level folder.

    SVG file paths are grouped based on the first path component. Files that
    are located at the root level of the ZIP archive (i.e. without any folder)
    are grouped under the key ``"root"``.

    Args:
        zip_path: Path to the ZIP archive containing SVG files.

    Returns:
        A dictionary mapping top-level folder names to lists of SVG file paths
        inside the ZIP archive.
    """
    groups: dict[str, list[str]] = defaultdict(list)

    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".svg"):
                continue

            parts = name.split("/")
            folder = parts[0] if len(parts) > 1 else "root"
            groups[folder].append(name)

    return dict(groups)
