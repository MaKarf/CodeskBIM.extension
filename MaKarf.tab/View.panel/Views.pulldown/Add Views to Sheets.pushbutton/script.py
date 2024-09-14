from UI.Popup import Alert
from UI.xamlFiles.PlaceViewsOnSheets import PlaceViewsOnSheets
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView


sheet_list = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()


if sheet_list:
    ui = PlaceViewsOnSheets(sheet_list)
    ui.ShowDialog()
else:
    Alert(title="No Sheet found", header="No sheets found", content="Create sheets and retry")
