import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication


class QtApplicationError(RuntimeError):
    """Raised when a valid QApplication cannot be obtained."""


def get_qapplication(
    *,
    create_if_missing: bool = False,
    argv: list[str] | None = None,
) -> QApplication:
    """
    Return a QApplication instance in a safe and type-correct way.

    This function supports DCC environments (Houdini, Maya),
    standalone execution (VSCode, scripts), and test environments.

    Args:
        create_if_missing:
            If True, create a new QApplication when none exists.
            Typically True for standalone tools, False for DCC.
        argv:
            Optional argv passed to QApplication constructor.

    Returns:
        QApplication instance.

    Raises:
        QtApplicationError:
            - No Qt application exists and creation is disabled
            - QtWidgets is not available (QCoreApplication only)
    """
    app = QCoreApplication.instance()

    if app is None:
        if not create_if_missing:
            raise QtApplicationError(
                "QApplication is not initialized and auto-creation is disabled."
            )

        return QApplication(argv or sys.argv)

    if not isinstance(app, QApplication):
        raise QtApplicationError(
            "QApplication is required, but only QCoreApplication is available."
        )

    return app
