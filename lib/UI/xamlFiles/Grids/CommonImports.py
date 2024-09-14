from Autodesk.Revit import DB
from Autodesk.Revit.DB import Transaction, Color, FilteredElementCollector as Fec, BuiltInCategory as Bic

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Rename Grids")
active_view = ui_doc.ActiveView


class SelectionType:
    def __init__(self):
        pass

    select_from_ui = 1
    select_from_db = 2
    select_from_options = 3
    select_from_list = 4
