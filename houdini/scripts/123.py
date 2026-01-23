import os

import debug_attach_bootstrap
from pixelpouch.libs.core.environment_variable_key import EnvironmentVariableKey
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory

logger = PixelPouchLoggerFactory.get_logger(__name__)

if os.environ.get(EnvironmentVariableKey.HOUDINI_DEBUG):
    logger.info(
        "[Houdini] Houdini debugging"
    )
    debug_attach_bootstrap.main()