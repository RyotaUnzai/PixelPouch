"""Utilities for attaching debugpy to a running Houdini-related process.

This module provides lightweight runtime helpers for starting a debugpy server
in a background thread and for monitoring the lifetime of an external process
(e.g. Houdini). When the watched process terminates, the current process exits
immediately to avoid orphaned helper processes.
"""

from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

import debugpy
import psutil
from pixelpouch.libs.core.environment_variable_key import (
    PixelPouchEnvironmentVariables,
)
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory

if TYPE_CHECKING:
    from pathlib import Path

logger = PixelPouchLoggerFactory.get_logger(__name__)
PP_ENV = PixelPouchEnvironmentVariables()


@dataclass(slots=True)
class ProcessWatchdog:
    """Watch for the existence of a specific process and exit if it disappears.

    This class periodically scans running processes by name. If the target
    process is no longer found, the current process terminates immediately.
    """

    ready_file: Path
    interval: float = 0.5
    _thread: Optional[threading.Thread] = None
    process_name: str = ""

    def start(self) -> None:
        """Start the watchdog thread.

        The watchdog runs as a daemon thread and continuously checks whether
        the target process is still alive.
        """
        self._thread = threading.Thread(
            target=self._run,
            name="ProcessWatchdog",
            daemon=True,
        )
        self._thread.start()

    def _run(self) -> None:
        """Background loop that monitors the target process.

        If the watched process is no longer detected, the current process
        exits immediately using ``os._exit``.
        """
        while True:
            if not self._houdini_alive():
                self._cleanup_on_process_exit()
                os._exit(0)
            time.sleep(self.interval)

    def _houdini_alive(self) -> bool:
        """Check whether the target process is currently running.

        Returns:
            ``True`` if a running process matches ``process_name``,
            ``False`` otherwise.
        """
        for proc in psutil.process_iter(attrs=["name"]):
            try:
                if proc.info["name"] and proc.info["name"].lower() == self.process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def _cleanup_on_process_exit(self) -> None:
        """Cleanup resources when the watched process exits."""
        if self.ready_file is None:
            return

        try:
            if self.ready_file.exists():
                self.ready_file.unlink()
                logger.info("[Watchdog] debugpy ready marker removed")
        except Exception:
            # cleanup failure must not block shutdown
            logger.exception("[Watchdog] failed to cleanup debugpy ready marker")


@dataclass(slots=True)
class DebugpyRuntime:
    """Runtime controller for starting a debugpy server in a background thread.

    This class ensures that debugpy is started only once, even if ``start`` is
    called multiple times. The debugpy server runs asynchronously and listens
    on the specified host and port.
    """

    host: str
    port: int
    python_location: Path
    ready_file: Path

    _started: bool = field(default=False, init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def start(self) -> None:
        """Start the debugpy server if it has not already been started.

        This method is thread-safe and returns immediately after spawning
        the background thread.
        """
        with self._lock:
            if self._started:
                return
            self._started = True

        threading.Thread(
            target=self._run,
            name="PixelPouchDebugpyThread",
            daemon=True,
        ).start()

    def _run(self) -> None:
        """Background thread entry point for running debugpy.

        This method configures debugpy with the provided Python executable
        and starts listening on the configured host and port.
        """
        try:
            debugpy.configure(python=self.python_location.as_posix())
            _, actual_port = debugpy.listen((self.host, self.port))
            logger.info(f"[Houdini] debugpy listening on {self.host}:{actual_port}")
            self._mark_debugpy_ready()

        except Exception:
            logger.exception("[Houdini] debugpy failed")

    def _mark_debugpy_ready(self) -> None:
        try:
            self.ready_file.write_text("ready", encoding="utf-8")
            logger.info("[Houdini] debugpy ready marker written")
        except Exception:
            logger.exception("[Houdini] failed to write debugpy ready marker")
