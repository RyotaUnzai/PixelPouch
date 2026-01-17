
import os
import socket
import threading
from pathlib import Path

import debugpy
import hou

PROJECT_PATH = os.getenv("PIXELPOURCH_PATH") or ""
PORT_FILE = Path(PROJECT_PATH) / ".debugpy_port"

_lock = threading.Lock()


def cleanup_debugpy_port():
    try:
        if PORT_FILE.exists():
            PORT_FILE.unlink()
            print("[Houdini] debugpy port file removed")
    except Exception as e:
        print(f"[Houdini] cleanup error: {e}")

def _on_hip_event(event_type):
    if event_type == hou.hipFileEventType.BeforeExit:
        cleanup_debugpy_port()


def start_debugpy():
    with _lock:
        if hasattr(hou.session, "_pixelpouch_debugpy_started"):
            return
        hou.session._pixelpouch_debugpy_started = True

    def _run():
        if PORT_FILE.exists():
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
            sock.close()

            debugpy.configure(
                python=r"C:\Program Files\Side Effects Software\Houdini 21.0.512\bin\hython.exe"
            )

            debugpy.listen(("127.0.0.1", port))

            # write-once
            if not PORT_FILE.exists():
                PORT_FILE.write_text(
                    f"{port}",
                    encoding="utf-8"
                )

            print(f"[Houdini] debugpy listening on {port}")
            debugpy.wait_for_client()
            print("[Houdini] debugger attached")

        except Exception as e:
            print(f"[Houdini] debugpy error: {e}")

    threading.Thread(target=_run, daemon=False).start()


def main():
    if os.getenv("HOUDINI_DEBUG"):
        start_debugpy()

