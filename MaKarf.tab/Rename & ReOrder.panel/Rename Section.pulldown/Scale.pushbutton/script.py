# -*- coding: utf-8 -*-
"""
=====================================================================================================================
╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
=====================================================================================================================
"""
import operator
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import ViewType

"""
=====================================================================================================================
╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
 ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
=====================================================================================================================
"""

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Revit Transaction")

"""
=====================================================================================================================
╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
=====================================================================================================================
"""

"""##############################################################################################################"""
"""####################################    A P P L I C A T I O N      ###########################################"""
"""##############################################################################################################"""

views_collection = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()


def get_section_views():
    sections_list = []
    """extract only elevation views and discard elevation view templates"""
    for section in views_collection:
        if section.ViewType == ViewType.Section and not section.IsTemplate:
            # print(section.Name)
            sections_list.append(section)
    return sections_list


sections_list_global = get_section_views()


def hide_at_scales():
    for sects in sections_list_global:
        """ lookup and set parameter"""
        sects.LookupParameter("Hide at scales coarser than").Set(1000)


def view_detail_level():
    for view in views_collection:
        """ ignore view templates"""
        if not view.IsTemplate:
            # print(view.LookupParameter("Detail Level").AsValueString())
            """Course : 1, Medium: 2, Fine: 3"""
            try:
                view.LookupParameter("Detail Level").Set(3)
            except Exception:
                # print(view.Name)
                pass

    """##############################################################################################################"""
    """##############################################################################################################"""


def run():
    t.Start()
    hide_at_scales()
    view_detail_level()
    t.Commit()


run()
