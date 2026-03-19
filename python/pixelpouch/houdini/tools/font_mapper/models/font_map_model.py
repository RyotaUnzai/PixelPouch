import json
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel

if TYPE_CHECKING:
    from pixelpouch.houdini.tools.font_mapper.views.font_assigne_widget import (
        FontAssigneWidget,
    )
    from PySide6 import QtWidgets

_DATA_PATH = Path(__file__).parent.parent / "data" / "font_map.json"


class FontMapModel(BaseModel):
    target: str
    fontfamily: str
    style: str = "Regular"

    def create_widget(
        self, fonts_dir: Path, parent: Optional["QtWidgets.QWidget"] = None
    ) -> "FontAssigneWidget":
        from pixelpouch.houdini.tools.font_mapper.views.font_assigne_widget import (
            FontAssigneWidget,
        )

        return FontAssigneWidget(
            fonts_dir=fonts_dir,
            target=self.target,
            fontfamily=self.fontfamily,
            style=self.style,
            parent=parent,
        )


class FontMapListModel(BaseModel):
    items: list[FontMapModel]

    @classmethod
    def load_from_json(cls, path: Path = _DATA_PATH) -> "FontMapListModel":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        items = [
            FontMapModel(
                target=k, fontfamily=v["fontfamily"], style=v.get("style", "Regular")
            )
            for k, v in data.items()
        ]
        return cls(items=items)

    def create_widgets(
        self, fonts_dir: Path, parent: Optional["QtWidgets.QWidget"] = None
    ) -> list["FontAssigneWidget"]:
        return [
            item.create_widget(fonts_dir=fonts_dir, parent=parent)
            for item in self.items
        ]
