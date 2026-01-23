name = "pixelpouch_houdini"
version = "0.1.0"

requires = [
    "houdini-21.0",
    "pixelpouch_core-0.1.0"
]

def commands():
    env.HYTHON_LOCATION.append(
        "{env.HOUDINI_LOCATION}/bin/hython.exe"
    )
    env.HOUDINI_PATH.append(
        "{root}/../../../../houdini;&"
    )
    env.HOUDINI_TOOLBAR_PATH.append(
        "{root}/../../../../houdini/toolbar;@/^"
    )
