from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction, XYZ, ViewSheet, \
    ViewType, View, TemporaryViewMode

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
app = __revit__.Application


def get3DView():
    views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
    for view in views:
        if view.ViewType == ViewType.ThreeD and not view.IsTemplate:
            return view


def set3DView():
    ui_doc.ActiveView = get3DView()


def get2DView():
    views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
    for view in views:
        if view.ViewType == ViewType.FloorPlan and not view.IsTemplate:
            return view


def EnableRevealHiddenElements(view):
    view.EnableRevealHiddenMode()


def DisableRevealHiddenElements(view):
    view.DisableTemporaryViewMode(TemporaryViewMode.RevealHiddenElements)


threeDView = get3DView()
