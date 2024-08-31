from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic, Transaction, ElementId, ViewType
from System.Collections.Generic import List

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Unhide Section Lines")



""" collect all views from revit database"""
all_views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()

""" filter out only the section and elevation views"""
filtered_all_views = [view for view in all_views
                      if view.ViewType == ViewType.Section and not view.IsTemplate
                      or view.ViewType == ViewType.Elevation and not view.IsTemplate]

""" collect all section lines and elevation markers. They are of the 'Viewers' category """
all_secLines_and_elevationMarkers = Fec(doc).OfCategory(Bic.OST_Viewers).WhereElementIsNotElementType().ToElements()

hide_able_els = List[ElementId]()

t.Start()
""" iterate through each view"""
for view in filtered_all_views:

    """ iterate through the list of sectionLines and elevationsMarkers and create new list and ignore
     the section line that if equal to the current view in operation because 
     we cannot hide an object from its own view"""
    for viewer in all_secLines_and_elevationMarkers:
        if view.Name != viewer.Name:
            hide_able_els.Add(viewer.Id)

            view.UnhideElements(hide_able_els)

    """reset hide able list after every main loop"""
    hide_able_els = List[ElementId]()
t.Commit()

