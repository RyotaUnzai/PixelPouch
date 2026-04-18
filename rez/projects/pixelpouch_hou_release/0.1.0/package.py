name = "pixelpouch_release"
version = "0.1.0"

requires = [
    "pixelpouch_houdini-0.1.0",
]


def commands():
    env.PIXELPOUCH_LOCATION = "{env.PIXELPOUCH_LOCATION}"
    env.PIXELPOUCH_ENV = "release"
    env.PIXELPOUCH_EXECUTION_CONTEXT = "houdini"
    env.PIPELINE_LOG_LEVEL = "INFO"
    env.HOUDINI_SPLASH_MESSAGE = "   PIXELPOUCH - RELEASE"
    env.HOUDINI_SPLASH_FILE = (
        "{env.PIXELPOUCH_LOCATION}houdini/images/houdinincsplash.png"
    )

    # env.PIXELPOUCH_ENABLE_EXPERIMENTAL = "1"
