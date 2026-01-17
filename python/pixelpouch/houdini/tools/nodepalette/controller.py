from . import api


class NodePaletteController:
    def create(self, node_type: str) -> None:
        if api.create_node is None:
            raise RuntimeError("create_node is not registered")

        api.create_node(node_type)
