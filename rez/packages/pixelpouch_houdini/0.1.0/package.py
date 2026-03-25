name = "pixelpouch_houdini"
version = "0.1.0"

requires = ["houdini-21.0", "pixelpouch_core-0.1.0"]


def commands():
    env.HYTHON_LOCATION.append("{env.HOUDINI_LOCATION}/bin/hython.exe")
    # env.HOUDINI_PATH.append("{root}/../../../../houdini;&")
    # env.HOUDINI_TOOLBAR_PATH.append("{root}/../../../../houdini/toolbar;@/^")
    # env.HOUDINI_OTLSCAN_PATH.append("{root}/../../../../houdini/otls;&")
    # env.HOUDINI_PACKAGE_DIR.append("{root}/../../../../houdini/packages;&")
    # import os

    # print(os.getenv("HOUDINI_USER_PREF_DIR"))
    # p
