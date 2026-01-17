import atexit

import hou
import set_debug

if __name__ == "__main__":
    atexit.register(set_debug.cleanup_debugpy_port)
    hou.hipFile.addEventCallback(set_debug._on_hip_event)
    set_debug.main()