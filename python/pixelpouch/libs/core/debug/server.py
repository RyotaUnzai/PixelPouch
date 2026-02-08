"""
Request/response style Python execution server for DCC (Houdini).

- Executes received Python code
- Captures stdout / stderr
- Returns structured result as JSON
"""

from __future__ import annotations

import json
import socket
import threading
import traceback
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass, field
from io import StringIO
from typing import Any, Optional

from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)


@dataclass(slots=True)
class SendPythonServer:
    host: str = "127.0.0.1"
    port: int = 7001
    buffer_size: int = 1024 * 1024

    _thread: Optional[threading.Thread] = field(default=None, init=False)
    _started: bool = field(default=False, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    # -------------------------------------------------------------

    def start(self) -> None:
        """Start server (idempotent)."""
        with self._lock:
            if self._started:
                logger.debug("[SendPython] already started")
                return
            self._started = True

        self._thread = threading.Thread(
            target=self._run,
            name="SendPythonServer",
            daemon=True,
        )
        self._thread.start()

        logger.info("[SendPython] server started on %s:%d", self.host, self.port)

    # -------------------------------------------------------------

    def _run(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind((self.host, self.port))
                server.listen(1)

                logger.info("[SendPython] listening")

                while True:
                    conn, addr = server.accept()
                    with conn:
                        logger.debug("[SendPython] connection from %s", addr)
                        self._handle_connection(conn)

        except Exception:
            logger.exception("[SendPython] server crashed")

    # -------------------------------------------------------------

    def _handle_connection(self, conn: socket.socket) -> None:
        try:
            payload = conn.recv(self.buffer_size)
            if not payload:
                return

            request = json.loads(payload.decode("utf-8"))
            code = request.get("code")

            if not isinstance(code, str):
                raise ValueError("Invalid request: 'code' must be string")

            response = self._execute(code)
            conn.sendall(json.dumps(response).encode("utf-8"))

        except Exception:
            error = {
                "status": "error",
                "stdout": "",
                "stderr": traceback.format_exc(),
                "result": None,
            }
            conn.sendall(json.dumps(error).encode("utf-8"))
            logger.exception("[SendPython] failed to handle request")

    # -------------------------------------------------------------

    def _execute(self, code: str) -> dict[str, Any]:
        stdout_buf = StringIO()
        stderr_buf = StringIO()

        local_ns: dict[str, Any] = {}

        try:
            with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
                exec(code, globals(), local_ns)

            result = local_ns.get("result")

            return {
                "status": "ok",
                "stdout": stdout_buf.getvalue(),
                "stderr": stderr_buf.getvalue(),
                "result": result,
            }

        except Exception:
            return {
                "status": "error",
                "stdout": stdout_buf.getvalue(),
                "stderr": traceback.format_exc(),
                "result": None,
            }
