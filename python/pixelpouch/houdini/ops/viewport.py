"""Viewport utility functions for Houdini.

This module provides helper functions for interacting with the Houdini
Scene Viewer. It currently includes a utility to toggle the viewport
background color scheme for quick visual switching.
"""

import hou
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)


def toggle_viewport_background():
    """Cycles the Scene Viewer viewport background color scheme.

    This function attempts to find the Scene Viewer under the mouse cursor.
    If none is found, it falls back to the first available Scene Viewer in the
    current desktop. The viewport color scheme is then toggled in the
    following order:

    Dark → Grey → Light → Dark

    Raises:
        hou.Error: If no Scene Viewer can be found in the current UI context.
    """
    pane = hou.ui.paneTabUnderCursor()
    used_fallback = False
    if not pane or pane.type() != hou.paneTabType.SceneViewer:
        pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)

    if not pane:
        logger.error("No Scene Viewer found.")
        hou.ui.displayMessage("No Scene Viewer found.")
        raise hou.Error("No Scene Viewer found.")

    if used_fallback:
        logger.debug(
            "Scene Viewer not under cursor; using first available Scene Viewer."
        )

    viewport: hou.SceneViewer = pane.curViewport()
    settings: hou.GeometryViewportSettings = viewport.settings()
    color_scheme: hou.EnumValue = settings.colorScheme()

    if color_scheme == hou.viewportColorScheme.Dark:
        settings.setColorScheme(hou.viewportColorScheme.Grey)
        new_scheme = "Grey"
    elif color_scheme == hou.viewportColorScheme.Grey:
        settings.setColorScheme(hou.viewportColorScheme.Light)
        new_scheme = "Light"
    else:
        settings.setColorScheme(hou.viewportColorScheme.Dark)
        new_scheme = "Dark"

    logger.info("Viewport background color scheme set to %s.", new_scheme)
