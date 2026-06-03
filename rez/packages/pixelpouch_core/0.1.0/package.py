name = "pixelpouch_core"
version = "0.1.0"


def commands():
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}python")
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}python/third_party")
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}houdini/python")
    env.PYTHONPATH.append("{env.PIXELPOUCH_LOCATION}houdini/hotkeys")
    env.PIXELPOUCH_RESOURCE_ROOT = (
        "{env.PIXELPOUCH_LOCATION}python/pixelpouch/resources"
    )
