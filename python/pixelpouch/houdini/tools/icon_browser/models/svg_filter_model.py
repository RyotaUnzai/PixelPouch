"""Qt proxy model for filtering SVG list entries.

This module defines a QSortFilterProxyModel subclass that provides
case-insensitive text filtering for SVG list models. Filtering is applied
to the first column and matches rows whose display text satisfies the
current regular expression.
"""

from pixelpouch.libs.core.logging_factory import PixelPouchLoggerFactory
from PySide6 import QtCore

logger = PixelPouchLoggerFactory.get_logger(__name__)


class SvgFilterProxyModel(QtCore.QSortFilterProxyModel):
    """Proxy model that filters SVG entries by name.

    This proxy model performs case-insensitive filtering based on a regular
    expression applied to the display data of the first column.
    """

    def __init__(self, parent: QtCore.QObject | None = None) -> None:
        """Initializes the SVG filter proxy model.

        Args:
            parent: Optional Qt parent object.
        """
        super().__init__(parent)
        self.setFilterCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterKeyColumn(0)

    def filterAcceptsRow(
        self,
        source_row: int,
        source_parent: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
    ) -> bool:
        """Determines whether a source row should be included.

        A row is accepted if no filter pattern is set, or if the display
        text of the row matches the current filter regular expression.

        Args:
            source_row: Row index in the source model.
            source_parent: Parent index in the source model.

        Returns:
            True if the row should be included in the filtered model,
            otherwise False.
        """
        index = self.sourceModel().index(source_row, 0, source_parent)
        name = index.data()
        if not self.filterRegularExpression().pattern():
            return True
        return self.filterRegularExpression().match(name).hasMatch()
