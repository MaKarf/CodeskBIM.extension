import json

from Autodesk.Revit.DB import BoundingBoxXYZ, Line

from lib.imports.DotNetSystem import List
from Autodesk.Revit import DB

from lib.unitConvert import mm2ft

sheet_size_scale_factor = 1.41
A3SheetWidth = 420
A3SheetHeight = 297
title_block_margin_percent = 2.55
title_block_info_panel_space = 15.47619047619048


class DoorsAndWindowsScheduleTextNote:
    margin = mm2ft(50)

    def __init__(self):
        pass


class DoorsAndWindowsScheduleViewport:
    width_allowance = mm2ft(2000)

    table_base_allowance = mm2ft(90)
    table_top_allowance = mm2ft(90)

    top_and_down_allowance = table_base_allowance + table_top_allowance

    horizontal_interval = mm2ft(250)
    location_textbox_height = mm2ft(600)
    horizontal_rows = 5

    height_allowance = mm2ft(1000)

    table_height = (horizontal_rows * horizontal_interval) + location_textbox_height

    table_height_with_base_allowance = (horizontal_rows * horizontal_interval) + \
                                       location_textbox_height + \
                                       table_base_allowance

    table_height_with_both_allowance = table_height + top_and_down_allowance

    minimum_viewport_width = mm2ft(1400)
    header_cell_width = mm2ft(650)

    table_vertical_sep_ratio = 0.33
    min_table_vertical_sep_ratio = 0.55

    def __init__(self):
        pass

    @staticmethod
    def calc_overall_viewport_height(element_height):
        return DoorsAndWindowsScheduleViewport.table_height_with_both_allowance + element_height


class IgnoreSidesOfRectangle:
    def __init__(self):
        pass

    left = "left"
    right = "right"
    top = "top"
    bottom = "bottom"
    none = ()

    all = (left, right, top, bottom)
    verticals = (left, right)
    horizontals = (top, bottom)


class CodeskTextNoteType:
    def __init__(self):
        pass

    schedule_title = "Codesk Schedule Title"
    schedule_header = "Codesk Schedule Header"
    schedule_values = "Codesk Schedule Values"
    schedule_small_text = "Codesk Schedule Small"

    text_not_types_list = [schedule_title, schedule_header, schedule_values, schedule_small_text]


class DoorsAndWindowsScheduleJsonData:
    def __init__(self):
        pass

    viewports = {
        "overall_bounding_box": BoundingBoxXYZ(),
        "table": {"lines": List[Line], "texts": List[DB.TextNote]},
        "geometry_area": BoundingBoxXYZ(),
        "geometry_lines": List[Line],
        "geometry_points": List[DB.Point],
        "rooms": List[DB.TextNote]
    }

    sheet_data = {
        "rows": {"row_height": float, "viewports": List[type(viewports)]},
        "sheet": DB.ViewSheet,
        "title_block": DB.FamilyInstance
    }

    # screening_jason_data = List[type(sheet_data)]
    screening_jason_data = []

    @staticmethod
    def write_to_json(json_file_path, json_data):
        with open(json_file_path, "w") as js:
            json.dump(json_data, js, indent=4)
            js.close()

    @staticmethod
    def read_json(json_file_path):
        with open(json_file_path, 'r') as js:
            data = json.load(js)

            # bin_subs = data["subsType"]
            # binary_date = data["trialStart"]

            js.close()
            return data
