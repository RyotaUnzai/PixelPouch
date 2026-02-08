import hou
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)


def create_node(node_type: str) -> None:
    pane = hou.ui.paneTabUnderCursor()
    used_fallback = False
    if not pane or pane.type() != hou.paneTabType.NetworkEditor:
        pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.NetworkEditor)
        used_fallback = True

    if not pane:
        logger.error(
            "Failed to create node '%s': no Network Editor found.",
            node_type,
        )
        raise hou.Error("No Network Editor found")

    if used_fallback:
        logger.warning(
            "No Network Editor under cursor; using the first available Network Editor."
        )

    parent = pane.pwd()
    parent.createNode(node_type)

    logger.info(
        "Created node '%s' in network '%s'.",
        node_type,
        parent.path(),
    )
