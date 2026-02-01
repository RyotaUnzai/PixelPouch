from __future__ import annotations

import json
from typing import TYPE_CHECKING, Mapping

from pixelpouch.houdini.ops.svg_grouping import group_svgs_by_folder
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from pixelpouch.libs.core.utility import load_json

if TYPE_CHECKING:
    from pathlib import Path

logger = PixelPouchLoggerFactory.get_logger(__name__)


OTHER_CATEGORY_NAME = "Other"


def load_svg_category_map(path: Path) -> dict[str, set[str]]:
    """
    Load SVG category mapping from JSON.

    Returns:
        dict[str, set[str]] mapping category -> folder names
    """
    with path.open("r", encoding="utf-8") as f:
        raw: Mapping[str, list[str]] = json.load(f)

    return {category: set(folders) for category, folders in raw.items()}


def regroup_svgs_for_ui(
    zip_path: Path,
    category_map_path: Path,
) -> dict[str, list[str]]:
    """
    Regroup SVGs into UI categories based on a JSON category mapping.

    - Categories defined in JSON are used first
    - Any folder not listed in JSON is grouped into "Other"
    - Empty categories are removed
    - "Other" is always placed at the end

    Args:
        zip_path: Path to SVG ZIP archive
        category_map_path: Path to JSON category definition

    Returns:
        Ordered dict-like mapping (insertion order preserved):
        category name -> list of SVG paths
    """
    # SVGs grouped by original folder name (e.g. SOP, DOP, ...)
    raw_groups = group_svgs_by_folder(zip_path)

    # JSON: category -> [folder names]
    category_map: Mapping[str, list[str]] = load_json(category_map_path)

    ui_groups: dict[str, list[str]] = {}
    used_folders: set[str] = set()

    # 1. Explicit categories (JSON order is preserved)
    for category, folders in category_map.items():
        svg_list: list[str] = []

        for folder in folders:
            if folder in raw_groups:
                svg_list.extend(raw_groups[folder])
                used_folders.add(folder)

        if svg_list:
            ui_groups[category] = svg_list

    # 2. Everything else -> Other
    other_svgs: list[str] = []
    for folder, svg_paths in raw_groups.items():
        if folder not in used_folders:
            other_svgs.extend(svg_paths)

    if other_svgs:
        ui_groups[OTHER_CATEGORY_NAME] = other_svgs

    return ui_groups
