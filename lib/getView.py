from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction, XYZ, ViewSheet, \
    ViewType, View, TemporaryViewMode

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
app = __revit__.Application

views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()


def get3DView(views_list):
    nv = list(filter(lambda vw: vw.ViewType == ViewType.ThreeD and not vw.IsTemplate, views_list))
    # print nv
    return nv.pop() if nv else None


def set3DView():
    trd = get3DView(views)
    twd = get2DView(views)
    ui_doc.ActiveView = trd if trd else twd


def get2DView(views_list=views):
    nv = list(filter(lambda vw: vw.ViewType == ViewType.FloorPlan and not vw.IsTemplate, views_list))
    # print nv
    return nv.pop() if nv else None


def EnableRevealHiddenElements(view):
    view.EnableRevealHiddenMode()


def DisableRevealHiddenElements(view):
    view.DisableTemporaryViewMode(TemporaryViewMode.RevealHiddenElements)


threeDView = get3DView(views)
