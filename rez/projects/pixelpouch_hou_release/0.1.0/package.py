name = "pixelpouch_release"
version = "0.1.0"

requires = [
    "pixelpouch_houdini-0.1.0",
]

def commands():
    env.PIXELPOUCH_LOCATION = "{root}/../../../../"
    env.PIXELPOUCH_ENV = "release"

    # env.PIXELPOUCH_ENABLE_EXPERIMENTAL = "1"
