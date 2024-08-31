from Autodesk.Revit.DB import BuiltInCategory as Bic, ViewType, FilteredElementCollector as Fec, Transaction


ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Deleted all sheets")
active_view = ui_doc.ActiveView

sheets = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElementIds()

if active_view.ViewType == ViewType.DrawingSheet:
    views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
    for view in views:
        if view.ViewType == ViewType.ThreeD and not view.IsTemplate:
            ui_doc.ActiveView = view
            break

t.Start()
doc.Delete(sheets)
t.Commit()


