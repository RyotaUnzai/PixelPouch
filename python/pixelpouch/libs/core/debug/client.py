"""
Client utility for sending Python code to a running DCC send server.

- Request / response style
- No dependency on print()
- Suitable for OSS / pytest / mypy / pyright
"""

from __future__ import annotations

import json
import logging
import socket
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------------
# logging (stdlib only)
# ----------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------
# types
# ----------------------------------------------------------------------


Response = dict[str, Any]


# ----------------------------------------------------------------------
# client
# ----------------------------------------------------------------------


@dataclass(slots=True)
class SendPythonClient:
    """TCP client for sending Python code to a DCC process.

    This class is transport-only and does not perform any printing.
    """

    host: str = "127.0.0.1"
    port: int = 7001
    timeout: float = 3.0
    encoding: str = "utf-8"
    buffer_size: int = 1024 * 1024

    # -------------------------------------------------------------

    def send_code(self, code: str) -> Response:
        """Send Python code and return structured response.

        Raises:
            RuntimeError: If connection or protocol fails.
        """
        request = {"code": code}

        try:
            with socket.create_connection(
                (self.host, self.port),
                timeout=self.timeout,
            ) as sock:
                payload = json.dumps(request).encode(self.encoding)
                sock.sendall(payload)

                logger.info(
                    "Sent %d bytes to %s:%d",
                    len(payload),
                    self.host,
                    self.port,
                )

                response_bytes = sock.recv(self.buffer_size)
                if not response_bytes:
                    raise RuntimeError("No response received from DCC")

        except Exception as exc:
            logger.error(
                "Failed to send code to %s:%d",
                self.host,
                self.port,
            )
            logger.exception(exc)
            raise RuntimeError("Failed to send Python code to DCC") from exc

        try:
            response: Response = json.loads(response_bytes.decode(self.encoding))
        except Exception as exc:
            raise RuntimeError("Invalid response from DCC") from exc

        return response

    # -------------------------------------------------------------

    def send_file(self, path: Path) -> Response:
        """Send Python source code from a file."""
        if not path.exists():
            raise FileNotFoundError(path)

        code = path.read_text(encoding=self.encoding)
        return self.send_code(code)


# ----------------------------------------------------------------------
# CLI entry (presentation layer only)
# ----------------------------------------------------------------------


def _main(argv: list[str]) -> int:
    if len(argv) != 2:
        logger.error("Usage: %s <python_file>", Path(argv[0]).name)
        return 1

    client = SendPythonClient()

    try:
        response = client.send_file(Path(argv[1]))
    except Exception:
        return 2

    # ---- presentation (CLI responsibility) ----------------------

    status = response.get("status")
    stdout = response.get("stdout")
    stderr = response.get("stderr")
    result = response.get("result")

    print("=== STATUS ===")
    print(status)

    if stdout:
        print("=== STDOUT ===")
        print(stdout)

    if stderr:
        print("=== STDERR ===")
        print(stderr)

    if result is not None:
        print("=== RESULT ===")
        print(result)

    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
