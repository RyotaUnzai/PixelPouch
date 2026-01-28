from pydantic import BaseModel


class WidgetModel(BaseModel):
    name: str
    widget: str


class WidgetListModel(BaseModel):
    widgets: list[WidgetModel]
