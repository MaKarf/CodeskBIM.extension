"""##############################################################################################################"""
"""#################################    I   M   P   O   R   T   S     ###########################################"""
"""##############################################################################################################"""

from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import Transaction

from Autodesk.Revit.DB import ViewType

"""##############################################################################################################"""
"""#################################    I   M   P   O   R   T   S     ###########################################"""
"""##############################################################################################################"""

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Rename Elevations")

""" get collection of views from active revit document"""
views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()


def rename_elevation_names():
    """ start Revit transaction """
    t.Start()
    for view in views:

        """extract only elevation views and discard elevation view templates"""
        if view.ViewType == ViewType.Elevation and not view.IsTemplate:
            current_view_name = view.Name
            # print("old view name :" + str(view.Name))

            new_view_name = str(current_view_name) + " Elevation"

            """ lookup and set parameter"""
            view.LookupParameter("View Name").Set(new_view_name)
            # print("new view name :" + str(view.Name))

    """ end/close Revit transaction """
    t.Commit()


def run():
    rename_elevation_names()

run()
