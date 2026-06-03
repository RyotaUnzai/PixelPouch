from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from PySide6 import QtCore

T = TypeVar("T")


def execute_in_houdini_main_thread(
    callback: Callable[..., T],
    *args: object,
    **kwargs: object,
) -> None:
    """Execute a callable on Houdini's main thread when possible.

    Houdini UI code can become unstable if top-level Qt widgets are created or
    shown directly from the Python Shell or from a re-entrant callback. When
    ``hdefereval`` is available, this helper defers execution to Houdini's main
    thread. Outside Houdini, it falls back to a queued Qt timer callback.
    """

    def _invoke() -> None:
        callback(*args, **kwargs)

    try:
        import hdefereval  # type: ignore[import-not-found]
    except ImportError:
        QtCore.QTimer.singleShot(0, _invoke)
        return

    hdefereval.executeDeferred(_invoke)
