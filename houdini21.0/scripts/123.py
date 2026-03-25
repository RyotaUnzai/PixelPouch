"""Houdini startup script for PixelPouch initialization.

This module is executed automatically by Houdini at startup (``123.py``).
It initializes PixelPouch-specific runtime behavior, including ensuring
required local data directories exist and conditionally enabling the Python
debugger based on environment configuration.
"""

import debug_attach_bootstrap
from pixelpouch.libs.core.debug.server import SendPythonServer
from pixelpouch.libs.core.environment_variable_key import PixelPouchEnvironmentVariables
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)

#: PixelPouch environment variable accessor initialized from the current
#: process environment.
PP_ENV = PixelPouchEnvironmentVariables()

if not PP_ENV.PIXELPOUCH_LOCAL_DATA_DIR.exists():
    PP_ENV.PIXELPOUCH_LOCAL_DATA_DIR.mkdir()


if PP_ENV.PIXELPOUCH_DEBUGGER_ENABLE:
    server = SendPythonServer(port=7001)
    server.start()

    logger.info("[Houdini] Houdini debugging")
    debug_attach_bootstrap.main()
