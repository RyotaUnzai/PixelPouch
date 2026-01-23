name = "pixelpouch_core"
version = "0.1.0"

def commands():
    env.PYTHONPATH.append(
        "{root}/../../../../python"
    )

    env.PYTHONPATH.append(
        "{root}/../../../../python/third_party"
    )

    env.PYTHONPATH.append(
        "{root}/../../../../houdini/python"
    )

    env.PYTHONPATH.append(
        "{root}/../../../../houdini/hotkeys"
    )
