import hou

pane = hou.ui.paneTabUnderCursor()
if not pane or pane.type() != hou.paneTabType.SceneViewer:
    pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)

if not pane:
    hou.ui.displayMessage("No Scene Viewer found.")
    raise hou.Error("No Scene Viewer found.")

viewport: hou.SceneViewer = pane.curViewport()
settings: hou.GeometryViewportSettings = viewport.settings()
color_scheme: hou.EnumValue = settings.colorScheme()

if color_scheme == hou.viewportColorScheme.Dark:
    settings.setColorScheme(hou.viewportColorScheme.Grey)
elif color_scheme == hou.viewportColorScheme.Grey:
    settings.setColorScheme(hou.viewportColorScheme.Light)
else:
    settings.setColorScheme(hou.viewportColorScheme.Dark)
