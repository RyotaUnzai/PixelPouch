name = "houdini"
version = "21.0"


def commands():
    env.HOUDINI_LOCATION = "{env.HOUDINI_LOCATION}"
    env.PATH.append("{env.HOUDINI_LOCATION}/bin")
    env.HOUDINI_USER_PREF_DIR = "{env.PROJECT_ROOT}houdini21.0"
    env.HOUDINI_MENU_PATH.append("{root}/menu;&")
