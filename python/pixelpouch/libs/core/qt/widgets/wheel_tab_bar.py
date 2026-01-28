# pixelpouch/houdini/tools/icon_browser/widgets/wheel_tab_bar.py


from PySide6 import QtGui, QtWidgets


class WheelTabBar(QtWidgets.QTabBar):
    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if self.count() == 0:
            return

        delta = event.angleDelta().y()
        if delta == 0:
            return

        current = self.currentIndex()

        if delta > 0:
            next_index = current - 1
        else:
            next_index = current + 1

        next_index = max(0, min(self.count() - 1, next_index))
        if next_index != current:
            self.setCurrentIndex(next_index)

        event.accept()
