name = "houdini"
version = "21.0"

def commands():
    env.HOUDINI_LOCATION = "{env.HOUDINI_LOCATION}"
    env.PATH.append("{env.HOUDINI_LOCATION}/bin")
