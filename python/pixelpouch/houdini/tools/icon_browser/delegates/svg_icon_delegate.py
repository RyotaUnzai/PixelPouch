"""Qt item delegate for rendering SVG icons in an icon browser view.

This module defines a custom QStyledItemDelegate responsible for painting
SVG icons and their labels in an icon-based list view. It works in
conjunction with SvgFilterProxyModel and SvgZipListModel to lazily request
icons and render selection-aware visuals.
"""

from pixelpouch.houdini.tools.icon_browser.models import (
    SvgFilterProxyModel,
    SvgZipListModel,
)
from pixelpouch.libs.core.logging import PixelPouchLoggerFactory
from PySide6 import QtCore, QtGui, QtWidgets

logger = PixelPouchLoggerFactory.get_logger(__name__)


class SvgIconDelegate(QtWidgets.QStyledItemDelegate):
    """Item delegate that renders SVG icons with labels.

    This delegate draws an icon preview and its corresponding file name
    centered below the icon. Icons are requested lazily from the source
    model when not yet available.
    """

    ICON_PADDING = 4
    TEXT_HEIGHT = 20

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> None:
        """Paints an SVG icon item.

        This method retrieves the underlying source model index, requests
        icon generation if necessary, and renders the icon and label. The
        selection state is respected when drawing background and text
        colors.

        Args:
            painter: QPainter used for rendering.
            option: Style options describing the item state.
            index: Model index of the item to paint.
        """
        proxy = index.model()
        if not isinstance(proxy, SvgFilterProxyModel):
            logger.debug("Unexpected model type in SvgIconDelegate.paint")
            return

        source = proxy.sourceModel()
        if not isinstance(source, SvgZipListModel):
            logger.debug("Unexpected source model type in SvgIconDelegate.paint")
            return

        proxy_model: SvgFilterProxyModel = proxy
        source_model: SvgZipListModel = source

        source_index = proxy_model.mapToSource(index)
        row = source_index.row()

        painter.save()

        rect = option.rect

        if option.state & QtWidgets.QStyle.StateFlag.State_Selected:
            painter.fillRect(rect, option.palette.highlight())

        icon_rect = QtCore.QRect(
            rect.x() + self.ICON_PADDING,
            rect.y() + self.ICON_PADDING,
            rect.width() - self.ICON_PADDING * 2,
            rect.height() - self.TEXT_HEIGHT - self.ICON_PADDING * 2,
        )

        icon = source_model.get_icon(row)
        if icon is None:
            source_model.request_icon(row)
        else:
            icon.paint(
                painter,
                icon_rect,
                QtCore.Qt.AlignmentFlag.AlignCenter,
            )

        text_rect = QtCore.QRect(
            rect.x(),
            rect.bottom() - self.TEXT_HEIGHT,
            rect.width(),
            self.TEXT_HEIGHT,
        )

        text_color = (
            option.palette.highlightedText().color()
            if option.state & QtWidgets.QStyle.StateFlag.State_Selected
            else option.palette.text().color()
        )
        painter.setPen(text_color)

        painter.drawText(
            text_rect,
            QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.TextFlag.TextSingleLine,
            source_index.data(),
        )

        painter.restore()

    def sizeHint(
        self,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> QtCore.QSize:
        """Returns the preferred size for an icon item.

        Args:
            option: Style options describing the item state.
            index: Model index of the item.

        Returns:
            The preferred item size as a QSize.
        """
        return QtCore.QSize(96, 96)

    def helpEvent(
        self,
        event: QtGui.QHelpEvent,
        view: QtWidgets.QAbstractItemView,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ) -> bool:
        """Handles tooltip display for SVG items.

        When hovering over an item, this method shows a tooltip containing
        the SVG file name resolved from the source model.

        Args:
            event: Help event triggering the tooltip.
            view: View associated with this delegate.
            option: Style options describing the item state.
            index: Model index under the cursor.

        Returns:
            True if the tooltip was shown, otherwise False.
        """
        if not index.isValid():
            return False

        proxy = index.model()
        if not isinstance(proxy, SvgFilterProxyModel):
            logger.debug("Unexpected model type in SvgIconDelegate.helpEvent")
            return False

        proxy_model: SvgFilterProxyModel = proxy
        source_index: QtCore.QModelIndex = proxy_model.mapToSource(index)

        text = source_index.data()
        if not text:
            return False

        QtWidgets.QToolTip.showText(
            event.globalPos(),
            text,
            view,
        )
        return True
