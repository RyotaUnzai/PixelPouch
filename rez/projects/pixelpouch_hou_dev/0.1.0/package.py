name = "pixelpouch_dev"
version = "0.1.0"

requires = [
    "pixelpouch_houdini-0.1.0",
]


def commands():
    env.PIXELPOUCH_LOCATION = "{env.PIXELPOUCH_LOCATION}"
    env.PIXELPOUCH_ENV = "dev"
    env.PIXELPOUCH_DEBUGGER_ENABLE = "1"
    env.PIXELPOUCH_HOST = "127.0.0.1"
    env.PIXELPOUCH_PORT = "6214"
    env.PIXELPOUCH_EXECUTION_CONTEXT = "houdini"
    env.PIPELINE_LOG_LEVEL = "DEBUG"
    env.HOUDINI_SPLASH_MESSAGE = "   PIXELPOUCH - DEV"
    env.HOUDINI_SPLASH_FILE = (
        "{env.PIXELPOUCH_LOCATION}houdini/images/houdinincsplash.png"
    )
    # env.PIXELPOUCH_ENABLE_EXPERIMENTAL = "1"
