from Autodesk.Revit import DB
from Autodesk.Revit.DB import ElementParameterFilter, BuiltInCategory, FilteredElementCollector, BuiltInParameter

from AppMethods import Alert
from loadfamilies import load_family

"""imports"""
from Autodesk.Revit.DB import ElementParameterFilter, FilteredElementCollector
from Autodesk.Revit.UI import TaskDialog

# import sys

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


class SearchElementTypeByName:
    doc = None
    built_in_category = None
    built_in_parameter = None
    search_name = ""
    results = None
    family_category_name = ""

    def __init__(self, document=doc,
                 built_in_category=DB.BuiltInCategory.OST_GridHeads,
                 built_in_parameter=DB.BuiltInParameter.SYMBOL_NAME_PARAM,
                 search_name="MK_Grid Head",
                 family_category_name="",
                 load_family_if_not_found=True):

        self.doc = document
        self.built_in_category = built_in_category
        self.built_in_parameter = built_in_parameter
        self.search_name = search_name
        self.family_category_name = family_category_name

        results = self.search()
        if results is None:
            if load_family_if_not_found:
                """load family if none is found"""

                load_family([self.family_category_name])
                # print("loading tags")
                #
                results2 = self.search()
                if results2 is None:
                    Alert(content="Ensure the Grid Head families are loaded into the project",
                          title="Results",
                          header="None of Codesk GridHead was found")

    def search(self):
        para_name = DB.ParameterValueProvider(DB.ElementId(self.built_in_parameter))
        filter_test = DB.FilterStringEquals()
        case_sensitive = True

        try:
            """method by revit 2023"""
            filter_rule = DB.FilterStringRule(para_name, filter_test, self.search_name)
        except TypeError:
            """method by revit 2022 and below"""
            filter_rule = DB.FilterStringRule(para_name, filter_test, self.search_name, case_sensitive)

        param_filter = ElementParameterFilter(filter_rule)

        vv = FilteredElementCollector(self.doc). \
            OfCategory(self.built_in_category). \
            WhereElementIsElementType(). \
            WherePasses(param_filter). \
            ToElements()
        try:
            self.results = vv[0]
            return self.results
        except ValueError:
            return None


class SearchElementByName:
    doc = None
    built_in_category = None
    built_in_parameter = None
    search_name = ""
    results = None
    family_category_name = ""

    def __init__(self, document=doc,
                 built_in_category=DB.BuiltInCategory.OST_GridHeads,
                 built_in_parameter=DB.BuiltInParameter.SYMBOL_NAME_PARAM,
                 search_name="MK_Grid Head",
                 family_category_name=""):

        self.doc = document
        self.built_in_category = built_in_category
        self.built_in_parameter = built_in_parameter
        self.search_name = search_name
        self.family_category_name = family_category_name

        self.search()

    def search(self):
        para_name = DB.ParameterValueProvider(DB.ElementId(self.built_in_parameter))
        filter_test = DB.FilterStringEquals()
        case_sensitive = True

        try:
            """method by revit 2023"""
            filter_rule = DB.FilterStringRule(para_name, filter_test, self.search_name)
        except TypeError:
            """method by revit 2022 and below"""
            filter_rule = DB.FilterStringRule(para_name, filter_test, self.search_name, case_sensitive)

        param_filter = ElementParameterFilter(filter_rule)

        vv = FilteredElementCollector(self.doc). \
            OfCategory(self.built_in_category). \
            WhereElementIsNotElementType(). \
            WherePasses(param_filter). \
            ToElements()
        try:
            self.results = vv[0]
            return self.results
        except ValueError:
            return None


def string_search_get_element_type_by_class_name(search_name="", of_class=DB.TextNoteType,
                                                 bip=BuiltInParameter.ALL_MODEL_TYPE_NAME):
    para_name = DB.ParameterValueProvider(DB.ElementId(bip))
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
        OfClass(of_class). \
        WhereElementIsElementType(). \
        WherePasses(param_filter). \
        ToElements()

    if str(vv) == "List[Element]()":
        return None
    else:
        return vv[0]


def string_search_get_element_type_by_name(search_name="", built_in_category=None, built_in_parameter=None):
    """imports"""

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

    for x in vv:
        print x

    if str(vv) == "List[Element]()":
        return None
    else:
        return vv[0]


if __name__ == "__main__":
    mk = string_search_get_element_type_by_name("MK_Door Tag", DB.BuiltInParameter.SYMBOL_NAME_PARAM)
    print(mk)
