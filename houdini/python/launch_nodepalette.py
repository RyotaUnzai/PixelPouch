import hou
from pixelpouch.houdini.ops.create_node import create_node
from pixelpouch.houdini.tools.nodepalette import api, run


def launch():
    api.create_node = create_node
    run.run(hou.ui.mainQtWindow())
