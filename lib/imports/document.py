from Autodesk.Revit import DB
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic, BuiltInParameter as Bip
from Autodesk.Revit.UI import UIApplication

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
uiApp = UIApplication(app)
active_view = doc.ActiveView
Fec = Fec
Bic = Bic
Bip = Bip
