from typing import Callable

from PySide6 import QtWidgets

WidgetFactory = dict[str, Callable[[str], QtWidgets.QWidget]]


WIDGET_FACTORY: WidgetFactory = {
    "QPushButton": lambda name: QtWidgets.QPushButton(name),
}
