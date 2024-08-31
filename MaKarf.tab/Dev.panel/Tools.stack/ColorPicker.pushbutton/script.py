from lib.UI.xamlFiles.ColorPickerWindow import ColorPickerWindow
from Autodesk.Revit.DB import Color

app = __revit__.Application

picked_color = ColorPickerWindow().picked_color
if picked_color is not None:
    revit_color = Color(picked_color[1], picked_color[2], picked_color[3])
    app.BackgroundColor = revit_color
