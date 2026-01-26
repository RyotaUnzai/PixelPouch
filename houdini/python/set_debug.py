
import os
import threading
from pathlib import Path

import debugpy
import hou
from debugpy._vendored.force_pydevd import pydevd
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)

PROJECT_PATH = os.getenv("PIXELPOURCH_PATH") or ""
PORT_FILE = Path(PROJECT_PATH) / ".debugpy_port"



def _force_kill_hython():
    try:
        pid = os.getpid()
        os.system(f"taskkill /F /PID {pid}")
    except Exception:
        pass

def stop_debugpy():
    logger.info("[Houdini] debugpy port stopping")
    try:
        pydevd.stoptrace()
        logger.info("[Houdini] debugpy port stopped")
    except Exception as e:
        logger.error(f"[Houdini] debugpy port stopped error: {e}")

def _on_hip_event(event_type):
    if event_type == hou.hipFileEventType.BeforeExit:
        stop_debugpy()
        _force_kill_hython()

def register_exit_hook():
    hou.hipFile.addEventCallback(
        [hou.hipFileEventType.BeforeExit],
        _on_hip_event
    )

def listen_debugpy():
    debugpy.configure(
        python=r"C:\Program Files\Side Effects Software\Houdini 21.0.512\bin\hython.exe"
    )

    _, port = debugpy.listen(("127.0.0.1", 6214))

def start_debugpy():
    _lock = threading.Lock()
    with _lock:
        if hasattr(hou.session, "_pixelpouch_debugpy_started"):
            return
        hou.session._pixelpouch_debugpy_started = True

    def _run():
        try:
            debugpy.configure(
                python=r"C:\Program Files\Side Effects Software\Houdini 21.0.512\bin\hython.exe"
            )

            _, port = debugpy.listen(("127.0.0.1", 6214))

            # write-once
            # if not PORT_FILE.exists():
            #     PORT_FILE.write_text(
            #         f"{port}",
            #         encoding="utf-8"
            #     )

            logger.info(f"[Houdini] debugpy listening on {port}")
            debugpy.wait_for_client()
            logger.info("[Houdini] debugger attached")

        except Exception as e:
            logger.error(f"[Houdini] debugpy error: {e}")

    threading.Thread(target=_run, daemon=True).start()


def main():
    if os.getenv("HOUDINI_DEBUG"):
        start_debugpy()

