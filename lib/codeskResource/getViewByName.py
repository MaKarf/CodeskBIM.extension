# -*- coding: utf-8 -*-
"""
=====================================================================================================================
╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
=====================================================================================================================
"""
from Autodesk.Revit import DB
from Autodesk.Revit.DB import FilteredElementCollector, ElementParameterFilter, BuiltInCategory

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


class GetViewByName:
    @staticmethod
    def get_views_by_name(view_name="{3D}"):
        para_name = DB.ParameterValueProvider(DB.ElementId(DB.BuiltInParameter.VIEW_NAME))
        filter_test = DB.FilterStringContains()
        search = view_name
        filter_rule = DB.FilterStringRule(para_name, filter_test, search)

        param_filter = ElementParameterFilter(filter_rule)

        vv = FilteredElementCollector(doc). \
            OfCategory(BuiltInCategory.OST_Views). \
            WhereElementIsNotElementType(). \
            WherePasses(param_filter). \
            ToElements()
        # for i in vv:
        #     print(i)
        return vv

    @staticmethod
    def get_view_by_name(view_name="{3D}"):
        para_name = DB.ParameterValueProvider(DB.ElementId(DB.BuiltInParameter.VIEW_NAME))
        filter_test = DB.FilterStringEquals()
        search = view_name
        filter_rule = DB.FilterStringRule(para_name, filter_test, search)

        param_filter = ElementParameterFilter(filter_rule)

        vv = FilteredElementCollector(doc). \
            OfCategory(BuiltInCategory.OST_Views). \
            WhereElementIsNotElementType(). \
            WherePasses(param_filter). \
            ToElements()
        # for i in vv:
        #     print(i)
        return vv[0]


def string_search_get_element_type_by_name(search_name="", built_in_category=None, built_in_parameter=None):
    """imports"""
    from Autodesk.Revit.DB import ElementParameterFilter, BuiltInCategory, FilteredElementCollector
    from Autodesk.Revit.UI import TaskDialog
    import sys

    para_name = DB.ParameterValueProvider(DB.ElementId(built_in_parameter))
    filter_test = DB.FilterStringEquals()
    case_sensitive = True

    try:
        """method by revit 2023"""
        filter_rule = DB.FilterStringRule(para_name, filter_test, search_name)
    except TypeError:
        """method by revit 2022 and below"""
        filter_rule = DB.FilterStringRule(para_name, filter_test, search_name, case_sensitive)

    param_filter = ElementParameterFilter(filter_rule)

    vv = FilteredElementCollector(doc). \
        OfCategory(built_in_category). \
        WhereElementIsElementType(). \
        WherePasses(param_filter). \
        ToElements()

    if str(vv) == "List[Element]()":
        td = TaskDialog("Error")
        td.MainInstruction = "Family not found"
        td.MainContent = "Load family '{}' into project and retry".format(search_name)

        td.TitleAutoPrefix = False
        td.Show()
        """exit code when TaskDialog is closed"""
        sys.exit(1)
        # return None
    else:
        print(vv)
        """return element from list"""
        return vv[0]


if __name__ == "__main__":
    mk = string_search_get_element_type_by_name("MK_Door Tag", DB.BuiltInParameter.SYMBOL_NAME_PARAM)
    print(mk)

