import sys

from pixelpouch.houdini.tools.icon_browser.views.svg_browser_window import (
    HoudiniIconBrowserWindow,
)
from pixelpouch.libs.core.environment_variable_key import (
    ExecutionContextEnv,
    PixelPouchEnvironmentVariables,
)
from pixelpouch.libs.core.houdini import HoudiniEnvironmentVariables
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory
from pixelpouch.libs.core.qt.application import get_qapplication
from pixelpouch.libs.core.qt.window_policy import (
    apply_standalone_window_policy,
)

logger = PixelPouchLoggerFactory.get_logger(__name__)


def run() -> None:
    HOU_ENV = HoudiniEnvironmentVariables()
    PP_ENV = PixelPouchEnvironmentVariables()

    zip_path = HOU_ENV.HOUDINI_LOCATION / "houdini/config/Icons/icons.zip"

    is_vscode = PP_ENV.PIXELPOUCH_EXECUTION_CONTEXT == ExecutionContextEnv.VSCODE

    app = get_qapplication(create_if_missing=is_vscode)

    window = HoudiniIconBrowserWindow(zip_path)

    apply_standalone_window_policy(
        window,
        embed_in_houdini=False,
    )
    window.show()

    if is_vscode:
        sys.exit(app.exec())


if __name__ == "__main__":
    run()
