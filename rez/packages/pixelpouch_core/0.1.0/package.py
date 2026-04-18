name = "pixelpouch_core"
version = "0.1.0"


def commands():
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}python")
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}python/third_party")
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}houdini/python")
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}houdini/hotkeys")
