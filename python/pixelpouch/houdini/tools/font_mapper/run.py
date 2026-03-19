import sys
from typing import Optional

from pixelpouch.houdini.ops.window_policy import apply_standalone_window_policy
from pixelpouch.houdini.tools.font_mapper.views.font_mapper_window import (
    HoudiniFontMapper,
)
from pixelpouch.libs.core.environment_variable_key import (
    ExecutionContextEnv,
    PixelPouchEnvironmentVariables,
)
from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from pixelpouch.libs.core.qt.application import get_qapplication
from PySide6 import QtCore, QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)

PP_ENV = PixelPouchEnvironmentVariables()
_HOUDINI_FONTS_DIR = PP_ENV.PIXELPOUCH_LOCATION / "houdini" / "fonts"


def run(parent: Optional[QtWidgets.QMainWindow] = None) -> None:
    PP_ENV = PixelPouchEnvironmentVariables()

    is_vscode = PP_ENV.PIXELPOUCH_EXECUTION_CONTEXT == ExecutionContextEnv.VSCODE

    app = get_qapplication(create_if_missing=is_vscode)

    window = HoudiniFontMapper(export_path=_HOUDINI_FONTS_DIR, parent=parent)
    window.setWindowTitle("Font Mapper")
    window.setWindowFlags(QtCore.Qt.WindowType.Window)
    apply_standalone_window_policy(
        window,
        embed_in_houdini=False,
    )
    window.show()

    if is_vscode:
        sys.exit(app.exec())


if __name__ == "__main__":
    run()
