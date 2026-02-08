import sys
from typing import Optional

import pytest

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except ImportError:
    QtCore = None  # type: ignore[assignment]
    QtGui = None  # type: ignore[assignment]
    QtWidgets = None  # type: ignore[assignment]

from pixelpouch.libs.core.qt.widgets.wheel_tab_bar import WheelTabBar

pytestmark = pytest.mark.qt


@pytest.fixture(scope="session")
def qapp() -> QtWidgets.QApplication:
    """
    Ensure a QApplication exists.

    Qt allows only one application instance per process.
    """
    if QtWidgets is None:
        pytest.skip("PySide6 is not available")

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    return app


def _wheel_event(delta_y: int) -> QtGui.QWheelEvent:
    """
    Create a synthetic QWheelEvent.

    Positive delta_y: wheel up
    Negative delta_y: wheel down
    """
    assert QtCore is not None
    assert QtGui is not None

    return QtGui.QWheelEvent(
        QtCore.QPointF(0.0, 0.0),  # position
        QtCore.QPointF(0.0, 0.0),  # globalPosition
        QtCore.QPoint(0, 0),  # pixelDelta
        QtCore.QPoint(0, delta_y),  # angleDelta
        QtCore.Qt.MouseButton.NoButton,
        QtCore.Qt.KeyboardModifier.NoModifier,
        QtCore.Qt.ScrollPhase.ScrollUpdate,
        False,
    )


def _create_tab_bar(tabs: list[str], current: Optional[int] = None) -> WheelTabBar:
    bar = WheelTabBar()
    for tab in tabs:
        bar.addTab(tab)

    if current is not None:
        bar.setCurrentIndex(current)

    return bar


def test_wheel_event_no_tabs(qapp):
    bar = WheelTabBar()

    event = _wheel_event(120)
    bar.wheelEvent(event)

    # QTabBar default currentIndex is -1 when empty
    assert bar.currentIndex() == -1


def test_wheel_event_scroll_down_moves_forward(qapp):
    bar = _create_tab_bar(["A", "B", "C"], current=1)

    event = _wheel_event(-120)
    bar.wheelEvent(event)

    assert bar.currentIndex() == 2


def test_wheel_event_scroll_up_moves_backward(qapp):
    bar = _create_tab_bar(["A", "B", "C"], current=1)

    event = _wheel_event(120)
    bar.wheelEvent(event)

    assert bar.currentIndex() == 0


def test_wheel_event_does_not_go_below_zero(qapp):
    bar = _create_tab_bar(["A", "B"], current=0)

    event = _wheel_event(120)
    bar.wheelEvent(event)

    assert bar.currentIndex() == 0


def test_wheel_event_does_not_exceed_max_index(qapp):
    bar = _create_tab_bar(["A", "B"], current=1)

    event = _wheel_event(-120)
    bar.wheelEvent(event)

    assert bar.currentIndex() == 1


def test_wheel_event_zero_delta_does_nothing(qapp):
    bar = _create_tab_bar(["A", "B"], current=0)

    event = _wheel_event(0)
    bar.wheelEvent(event)

    assert bar.currentIndex() == 0


def test_wheel_event_is_accepted(qapp):
    bar = _create_tab_bar(["A", "B"], current=0)

    event = _wheel_event(-120)
    bar.wheelEvent(event)

    assert event.isAccepted()
