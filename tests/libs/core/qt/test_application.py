import sys
from typing import Generator

import pytest

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    QtCore = None  # type: ignore[assignment]
    QtWidgets = None  # type: ignore[assignment]

from pixelpouch.libs.core.qt.application import (
    QtApplicationError,
    get_qapplication,
)

pytestmark = pytest.mark.qt


@pytest.fixture
def clean_qt_app() -> Generator[None, None, None]:
    """
    Ensure no QApplication exists before and after a test.

    Qt allows only one application instance per process.
    This fixture enforces isolation for tests that rely on
    application creation behavior.
    """
    if QtCore is None or QtWidgets is None:
        pytest.skip("PySide6 is not available")

    app = QtCore.QCoreApplication.instance()
    if app is not None:
        app.quit()
        del app

    yield

    app = QtCore.QCoreApplication.instance()
    if app is not None:
        app.quit()
        del app


def test_raises_if_no_app_and_creation_disabled(clean_qt_app):
    """
    If no QApplication exists and create_if_missing is False,
    QtApplicationError should be raised.
    """
    with pytest.raises(QtApplicationError):
        get_qapplication(create_if_missing=False)


def test_creates_qapplication_if_missing_and_allowed(clean_qt_app):
    """
    If no application exists and create_if_missing is True,
    a QApplication should be created.
    """
    app = get_qapplication(create_if_missing=True)

    assert isinstance(app, QtWidgets.QApplication)
    assert QtWidgets.QApplication.instance() is app


def test_returns_existing_qapplication():
    """
    If a QApplication already exists, it should be returned
    regardless of create_if_missing flag.
    """
    assert QtWidgets is not None

    existing = QtWidgets.QApplication.instance()
    if existing is None:
        existing = QtWidgets.QApplication(sys.argv)

    app = get_qapplication(create_if_missing=False)

    assert app is existing
