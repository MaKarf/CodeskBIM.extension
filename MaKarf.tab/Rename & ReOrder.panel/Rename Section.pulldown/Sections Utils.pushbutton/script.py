# -*- coding: utf-8 -*-
import operator
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import ViewType, Category

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Revit Transaction")

views_collection = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()


def get_elevation_view():
    elevations_list = []
    """extract only elevation views and discard elevation view templates"""
    for el in views_collection:
        if el.ViewType == ViewType.Elevation and not el.IsTemplate:
            # print(section.Name)
            elevations_list.append(el)
    return elevations_list


def get_section_views():
    sections_list = []
    """extract only elevation views and discard elevation view templates"""
    for section in views_collection:
        if section.ViewType == ViewType.Section and not section.IsTemplate:
            # print(section)
            sections_list.append(section)
    return sections_list


def get_elevations_section_n_views():
    view_list = []
    """extract only elevation views and discard elevation view templates"""
    for section in views_collection:
        if section.ViewType == ViewType.Section and not section.IsTemplate:
            # print(section)
            view_list.append(section)

    """extract only elevation views and discard elevation view templates"""
    for ele in views_collection:
        if ele.ViewType == ViewType.Elevation and not ele.IsTemplate:
            # print(section.Name)
            view_list.append(ele)

    return view_list


# section_element = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements().[0]


def hide_sections_in_view():
    cate = Category.GetCategory(doc, Bic.OST_Sections)
    print(cate.Name)
    for elev in get_elevations_section_n_views():
        # if section_element.CanBeHidden(elev):
        try:
            elev.SetCategoryHidden(cate.Category.Id, True)
        except Exception:
            pass


def run():
    t.Start()
    hide_sections_in_view()
    t.Commit()


run()
