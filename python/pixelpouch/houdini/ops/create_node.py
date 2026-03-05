import hou
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)


def create_node(node_type: str, position: tuple[float, float] = (0, -1.0)) -> None:
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

    obj_node: hou.ObjNode = pane.pwd()
    if not isinstance(obj_node, hou.ObjNode):
        return

    op_node: hou.OpNode = obj_node.createNode(node_type)

    selected = hou.selectedNodes()

    if selected:
        node: hou.Node = selected[0]
        v2: hou.Vector2 = node.position()
        op_node.setPosition((v2.x() + position[1], v2.y() + position[1]))

    op_node.setSelected(on=True, clear_all_selected=True)

    logger.debug("%s" % op_node.position())
    logger.debug(f"Created node {node_type} in network {obj_node.path()}.")
