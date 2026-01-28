import hou
from pixelpouch.houdini.ops.create_node import create_node
from pixelpouch.houdini.tools.nodepalette import api, run


def launch() -> None:
    api.create_node = create_node
    run.run(hou.qt.mainWindow())
