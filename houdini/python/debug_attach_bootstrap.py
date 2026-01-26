"""Entry point for enabling debugpy attachment in a Houdini environment.

This module conditionally starts a debugpy runtime and a process watchdog when
Houdini debugging is enabled via an environment variable. It is intended to be
used as a lightweight bootstrap script.
"""

from typing import Optional

from pixelpouch.libs.core.debug import DebugpyRuntime, ProcessWatchdog
from pixelpouch.libs.core.environment_variable_key import (
    PixelPouchEnv,
    PixelPouchEnvironmentVariables,
)
from pixelpouch.libs.core.houdini import HoudiniEnvironmentVariables
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)
HOU_ENV = HoudiniEnvironmentVariables()
PP_ENV = PixelPouchEnvironmentVariables()


_RUNTIME: Optional[DebugpyRuntime] = None


def main() -> None:
    """Initialize debugpy runtime when Houdini debugging is enabled.

    This function checks the ``PIXELPOUCH_DEBUGGER_ENABLE`` environment variable and, if it
    is set, starts a process watchdog for the Houdini process and launches a
    debugpy runtime configured for the current hython executable.
    """
    if not (PP_ENV.PIXELPOUCH_DEBUGGER_ENABLE):
        logger.info("PIXELPOUCH_DEBUGGER_ENABLE is False")
        return

    if PP_ENV.PIXELPOUCH_ENV == PixelPouchEnv.DEV:
        ready_file = PP_ENV.PIXELPOUCH_LOCAL_DATA_DIR / ".debugpy_ready"

        ProcessWatchdog(process_name="houdini.exe", ready_file=ready_file).start()
        global _RUNTIME
        _RUNTIME = DebugpyRuntime(
            python_location=HOU_ENV.HYTHON_LOCATION,
            host=PP_ENV.PIXELPOUCH_HOST,
            port=PP_ENV.PIXELPOUCH_PORT,
            ready_file=ready_file,
        )

        logger.info("DebugpyRuntime Start")
        _RUNTIME.start()
