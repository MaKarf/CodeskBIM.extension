# -*- coding: utf-8 -*-
from math import pi

from Autodesk.Revit.DB import Color, FilteredElementCollector as Fec, BuiltInCategory as Bic, ViewFamilyType, \
    ViewFamily, ElementId, FamilyInstance
from System.Collections.Generic import List

from UI.xamlFiles.CheckBoxAndDropdown import CheckBoxAndDropdown
from codeskResource.loadfamilies import get_families_path, load_family
from searchElement import string_search_get_element_type_by_class_name

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


def radian_to_angle(radian_value):
    degree = pi * 180
    return degree / radian_value


def angle_to_radian(angle_value):
    degree = pi / 180
    return degree * angle_value


def get_true_north():
    b = Fec(doc).OfCategory(Bic.OST_ProjectBasePoint).WhereElementIsNotElementType().ToElements()
    angle = b[0].LookupParameter("Angle to True North")
    return angle


def true_north_value_as_angle():
    return float(get_true_north().AsValueString().strip("°"))


def true_north_value_as_radian():
    return get_true_north().AsDouble()


def set_true_north(angle_value):
    angle = angle_to_radian(angle_value)
    get_true_north().Set(angle)


def create_text_types():
    text_type = string_search_get_element_type_by_class_name(search_name="2.5mm Arial")

    if text_type is not None:

        try:
            rooms_text = text_type.Duplicate("Codesk Schedule Small")
            rooms_text.LookupParameter("Leader/Border Offset").Set(0)

            font = (mm2ft(1.5) * 100) / 100
            rooms_text.LookupParameter("Text Size").Set(font)
            rooms_text.LookupParameter("Bold").Set(1)
            rooms_text.LookupParameter("Color").Set(Color(106, 17, 140))
        except Exception:
            pass

        try:
            title_text = text_type.Duplicate("Codesk Schedule Title")
            title_text.LookupParameter("Leader/Border Offset").Set(0)

            font = (mm2ft(3) * 100) / 100
            title_text.LookupParameter("Text Size").Set(font)
            title_text.LookupParameter("Bold").Set(1)
            title_text.LookupParameter("Color").Set(Color(106, 17, 140))
        except Exception:
            pass

        try:
            header_text = text_type.Duplicate("Codesk Schedule Header")
            header_text.LookupParameter("Leader/Border Offset").Set(0)

            font = (mm2ft(2.5) * 100) / 100
            header_text.LookupParameter("Text Size").Set(font)
            header_text.LookupParameter("Bold").Set(1)
            header_text.LookupParameter("Color").Set(Color(106, 17, 140))  # Color(R: 255; G: 255; B: 255)
            # print(header_text.LookupParameter("Color"))
        except Exception:
            pass

        try:
            values_text = text_type.Duplicate("Codesk Schedule Values")
            values_text.LookupParameter("Leader/Border Offset").Set(0)

            font = (mm2ft(2.5) * 100) / 100
            values_text.LookupParameter("Text Size").Set(font)
        except Exception:
            pass

        return True

    else:
        return None


def ft2mm(digit):
    if str(type(digit)) == "<type 'XYZ'>":
        res = (round(float(digit[0]) / 0.003281),
               round(float(digit[1]) / 0.003281),
               round(float(digit[2]) / 0.003281))
        # print(res)
        return res

    elif str(type(digit)) == "<type 'float'>":
        res = round(float(digit) / 0.003281)
        # print(res)
        return res

    elif str(type(digit)) == "<type 'int'>":
        res = int(round(float(digit) / 0.003281))
        # print(res)
        return res


def mm2ft(digit):
    if str(type(digit)) == "<type 'XYZ'>":
        res = (round((float(digit[0]) * 0.003281), 5),
               round((float(digit[1]) * 0.003281), 5),
               round((float(digit[2]) * 0.003281), 5))
        # print(res)
        return res

    elif str(type(digit)) == "<type 'float'>":
        res = round((float(digit) * 0.003281), 5)
        # print(res)
        return res

    elif str(type(digit)) == "<type 'int'>":
        res = round((float(digit) * 0.003281), 5)
        # print(res)
        return res


def vft():
    elem = Fec(doc).OfClass(ViewFamilyType).ToElements()
    ids = []
    """rewrite this code for a faster results using WherePasses method"""
    for v in elem:
        if v is not None and v.ViewFamily == ViewFamily.Detail:
            ids.append(v.Id)
            break
    for x in elem:
        if x is not None and x.ViewFamily == ViewFamily.Section:
            ids.append(x.Id)
            break
    return ids


def rounding(x):
    return round(x, 6)


def rounding_xyz(xyz):
    x = round(xyz[0], 6)
    y = round(xyz[1], 6)
    z = round(xyz[2], 6)
    result = (x, y, z)
    return result


def hide_sections():
    selected_elem = Fec(doc).OfCategory(Bic.OST_Viewers).WhereElementIsNotElementType().ToElements()

    section_views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()

    isoElems = List[ElementId]()

    for item in selected_elem:
        isoElems.Add(item.Id)

    for v in section_views:
        v.HideElements(isoElems)


def load_schedule_tag(element_category_name="Doors", ):
    tag_name = "CodeskSchedule{}Tag.rfa".format(element_category_name)
    families_path_list = get_families_path()
    tag = [i for i in families_path_list if i.split("\\")[-1] == tag_name]
    tag_path = tag.pop() if tag else None
    # print tag_path

    if tag_path is not None:
        loaded_family = load_family(tag_path, transact=False)
        return loaded_family
    else:
        return None


def get_title_block_with_sheet(provided_sheet):
    dependants = provided_sheet.GetDependentElements(None) if provided_sheet is not None else None

    title_block_and_sheet = [{"sheet": provided_sheet, "title_block": doc.GetElement(i)} for i in dependants if
                             type(doc.GetElement(i)) == FamilyInstance and
                             doc.GetElement(i).Category.Name == "Title Blocks"].pop() if dependants else None

    return title_block_and_sheet


def set_schedule_type_and_sheet():
    """get all sheets for display"""
    sheets = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()

    """generate sheet data"""
    sheets_data = [{"name": "{} - {}".format(i.SheetNumber, i.Name), "element": i} for i in sheets] if sheets else []

    doors_collection = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsNotElementType().ToElements()
    windows_collection = Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsNotElementType().ToElements()

    """create a dictionary of 'name':'item name in list, 'object':'item object for post process'"""
    dropdown_list = [{"name": "{} Schedule".format(i[0].Category.Name), "element": i} for i in
                     [doors_collection, windows_collection]]

    ui = CheckBoxAndDropdown(
        dropdown_list=dropdown_list,
        checkbox_data=sheets_data,
        select_multiple=False,
        parser_class=None,
        window_title="",
        selection_name="Select Sheet",
        finish_button_text_name="Generate",
        drop_down_label="Schedule Type: ",
        checkbox_container_height=350)
    ui.show_dialog()

    return ui if not ui.lock else None
