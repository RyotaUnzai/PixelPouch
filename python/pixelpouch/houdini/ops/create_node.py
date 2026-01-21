import hou


def create_node(node_type: str) -> None:
    pane = hou.ui.paneTabUnderCursor()
    if not pane or pane.type() != hou.paneTabType.NetworkEditor:
        pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.NetworkEditor)

    if not pane:
        raise hou.Error("No Network Editor found")

    parent = pane.pwd()
    parent.createNode(node_type)
