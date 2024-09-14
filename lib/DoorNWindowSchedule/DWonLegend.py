"""fast imports"""
from Autodesk.Revit import DB
from Autodesk.Revit.DB import BuiltInCategory as Bic, XYZ, BoundingBoxXYZ

from unitConvert import mm2ft
from sheets import get_ordered_sheets_as_dict
from DoorNWindowSchedule.Enumerations import title_block_margin_percent, title_block_info_panel_space, \
    IgnoreSidesOfRectangle, DoorsAndWindowsScheduleViewport

from DoorNWindowSchedule.LegendComponent import place_legend_on_sheet, create_reference_planes_from_center, \
    DoorsAndWindows, create_and_get_drafting_view

"""slow imports"""
from DoorNWindowSchedule.LineDrawing import CreateRectangle, CreateDandWViewport
from DoorNWindowSchedule.doorsNwindowsMethods import ft2mm
from UI.xamlFiles.DoorsAndWindowsSchedule import DoorsAndWindowsSchedule


app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document

active_view = doc.ActiveView

row_heights = []


class CreateSchedule:
    def __init__(self):
        self.element_types = None

        self.elements_in_schedule = {}
        self.nth_sheet = 0
        self.title_block = None
        self.height_in_mm = None
        self.width_in_mm = None
        self.outline = None

        self.stepped_times = 0
        self.row_number = 1
        self.counter = 0

        self.horizontal_x_pos = None
        self.viewport_top_y_pos = None
        self.viewport_base_y_pos = None

        self.selected_legend = None
        self.selected_sheet = None

        self.set_ui_parameters()

        self.overall_height_lists = self.prep_row_height()
        self.viewport_height = self.overall_height_lists[self.stepped_times]

        self.starting()

    def set_ui_parameters(self):
        """##############################################################################################"""
        """#######################################  POP UP UI ###########################################"""
        operation_type_data = DoorsAndWindows.get_all_as_ui_dropdown_data()
        sheet_data = get_ordered_sheets_as_dict()
        ui = DoorsAndWindowsSchedule(operation_list_data=operation_type_data, sheets_list_data=sheet_data)
        self.selected_sheet = ui.selected_sheet
        self.selected_legend = create_and_get_drafting_view()
        self.element_types = ui.operation_type

        print "SELECTED SHEET: {}".format(self.selected_sheet)
        print "SELECTED LEGEND: {}".format(self.selected_legend)
        print "SELECTED TYPE: {}".format(self.element_types)

        """##############################################################################################"""
        """##############################################################################################"""

        """get title block"""
        if self.selected_sheet is not None:
            dep = self.selected_sheet.GetDependentElements(DB.ElementCategoryFilter(Bic.OST_TitleBlocks))
            ttb_id = dep[0] if dep else None
            if ttb_id is not None:
                self.title_block = doc.GetElement(ttb_id)

        """#######################################  POP UP UI ###########################################"""
        """##############################################################################################"""

    def starting(self):
        self.init()
        self.process()

    def prep_init(self):

        height_in_ft = float(self.title_block.LookupParameter("Sheet Height").AsDouble())
        width_in_ft = float(self.title_block.LookupParameter("Sheet Width").AsDouble())
        self.height_in_mm = ft2mm(height_in_ft)
        self.width_in_mm = ft2mm(width_in_ft)

        """create outline for placement extent"""
        self.outline = CreateRectangle(ignore_sides=IgnoreSidesOfRectangle.all)
        margin = self.width_in_mm * title_block_margin_percent
        self.outline.from_center(height_in_mm=self.height_in_mm,
                                 width_in_mm=self.width_in_mm,
                                 drawing_view=self.selected_legend,
                                 margin=(margin,
                                         margin,
                                         margin + (self.width_in_mm * title_block_info_panel_space),
                                         margin))

        self.stepped_times = 0
        self.row_number = 1
        self.counter = 0

        self.viewport_height = height_in_ft

        """NEW METHOD"""
        self.horizontal_x_pos = self.outline.lower_left_point.X
        self.viewport_top_y_pos = self.outline.upper_left_point.Y
        self.viewport_base_y_pos = self.outline.upper_left_point.Y - self.viewport_height

    def prep_row_height(self):
        self.prep_init()

        overall_height_lists = []
        row_height_lists = []

        scale = self.selected_legend.Scale
        scale_factor = float(scale) / 100
        offset = mm2ft(10) * scale_factor

        x_margin = mm2ft(0) * scale_factor
        y_margin = mm2ft(0) * scale_factor

        # print len(self.element_types)
        """pre calculation """
        offset = DoorsAndWindowsScheduleViewport.width_allowance * scale_factor

        for index, data in enumerate(self.element_types):
            self.counter += 1
            # print data
            element = data.get("element")
            elem_width = data.get("width")
            elem_height = data.get("height")

            """get elements bounding box"""
            elem_bb = element.get_BoundingBox(self.selected_legend)

            row_height_lists.append(elem_height)
            # print row_height_lists

            viewport_width = elem_width + offset

            """compute min and max bb values"""
            min_x = self.horizontal_x_pos
            min_y = self.viewport_base_y_pos
            min_z = 0

            max_x = min_x + viewport_width
            max_y = self.viewport_top_y_pos
            max_z = 0

            mn = XYZ(min_x, min_y, min_z)
            mx = XYZ(max_x, max_y, max_z)

            bb = BoundingBoxXYZ()
            bb.Min = mn
            bb.Max = mx

            """check if the right line of the viewport enters the data pane"""
            if mx.X > self.outline.upper_right_point.X:
                """check if the space left is okay for the element to freely reside"""
                width_space_left = self.outline.upper_right_point.X - mn.X
                sharable_units = width_space_left / self.counter  # divide by number of items on the row
                squeezed_width = elem_width + float(offset) / 2  # using half of the offset to squeeze object in place

                """##############################################################################################"""
                """##############################################################################################"""
                if width_space_left < squeezed_width:
                    """put the item on the next line rather"""

                    last_item = row_height_lists[-1]

                    row_height_lists.pop(-1)
                    overall_height_lists.append(
                        max(row_height_lists) + DoorsAndWindowsScheduleViewport.table_height_with_both_allowance)

                    row_height_lists = [last_item]

                    # print "move to next line"

                    """reset counter after every row"""
                    """utilize the counter only if the sharable unit variable will be used"""
                    self.counter = 0

                    """set the bbox to the next line with space in between"""
                    """reset parameters"""
                    self.stepped_times += 1
                    self.row_number += 1

                    """NEW METHOD"""
                    self.horizontal_x_pos = self.outline.lower_left_point.X
                    self.viewport_top_y_pos -= self.viewport_height
                    self.viewport_base_y_pos -= self.viewport_height

                    """check if the baseline extends beyond the title block base"""
                    if self.viewport_base_y_pos > self.outline.lower_left_point.Y:
                        """viewport fits within same title block space"""
                        """check the space between the viewport base and the title block base line limit"""
                        vertical_allowance = self.viewport_base_y_pos - self.outline.lower_left_point.Y
                        if vertical_allowance < self.viewport_height:
                            """set the viewport base line to the title block base line to avoid gap between
                            the last viewport on the base of the last viewport and the title block base line limit"""
                            self.viewport_base_y_pos = self.outline.lower_left_point.Y
                        else:
                            """maintain the viewport baseline"""
                    else:
                        """#####################################################################################"""
                        """############################### move to next sheet ##################################"""
                        """#####################################################################################"""
                        """create new title block"""
                        self.nth_sheet += 1
                        """reset parameters to beginning"""
                        """create the title block element and place it on the sheet"""

                        self.prep_init()

                    """compute min and max bb values"""
                    min_x = self.horizontal_x_pos
                    min_y = self.viewport_base_y_pos
                    min_z = 0

                    max_x = min_x + viewport_width
                    max_y = self.viewport_top_y_pos
                    max_z = 0

                    mn = XYZ(min_x, min_y, min_z)
                    mx = XYZ(max_x, max_y, max_z)

                    bb.Min = mn
                    bb.Max = mx
                else:
                    """squeeze the item on the space"""
                    # print "squeeze the item on the space"
                    bb.Max = XYZ(self.outline.upper_right_point.X, mx.Y, mx.Z)

                """##############################################################################################"""
                """##############################################################################################"""

            """update the new x pos"""
            self.horizontal_x_pos = max_x

            """get the highest door height for the remaining items in the last row if the last row has items"""
            if index + 1 == len(self.element_types):
                if row_height_lists:
                    overall_height_lists.append(max(row_height_lists) +
                                                DoorsAndWindowsScheduleViewport.table_height_with_both_allowance)

                """reset initial parameters"""
                self.stepped_times = 0
                self.row_number = 1
                self.counter = 0

            """prep location text box height for row"""

        return overall_height_lists

    def init(self):

        height_in_ft = float(self.title_block.LookupParameter("Sheet Height").AsDouble())
        width_in_ft = float(self.title_block.LookupParameter("Sheet Width").AsDouble())
        self.height_in_mm = ft2mm(height_in_ft)
        self.width_in_mm = ft2mm(width_in_ft)

        """create a line on the legend view before place on sheet | create overall outline on title block"""
        create_reference_planes_from_center(view=self.selected_legend,
                                            height_in_mm=self.height_in_mm,
                                            width_in_mm=self.width_in_mm)

        """place view on sheet"""
        place_legend_on_sheet(tt_block=self.title_block,
                              legend=self.selected_legend,
                              placement_sheet=self.selected_sheet)

        """create outline for placement extent"""
        self.outline = CreateRectangle()
        margin = self.width_in_mm * title_block_margin_percent
        self.outline.from_center(height_in_mm=self.height_in_mm,
                                 width_in_mm=self.width_in_mm,
                                 drawing_view=self.selected_legend,
                                 margin=(margin,
                                         margin,
                                         margin + (self.width_in_mm * title_block_info_panel_space),
                                         margin))

        self.stepped_times = 0
        self.row_number = 1
        self.counter = 0

        # """OLD METHOD"""
        # self.horizontal_x_pos = self.outline.lower_left_point.X
        # self.viewport_top_y_pos = self.outline.upper_left_point.Y - (self.viewport_height * self.stepped_times)
        # self.viewport_base_y_pos = self.outline.upper_left_point.Y - (self.viewport_height * self.row_number)

        """NEW METHOD"""
        self.horizontal_x_pos = self.outline.lower_left_point.X
        self.viewport_top_y_pos = self.outline.upper_left_point.Y
        self.viewport_base_y_pos = self.outline.upper_left_point.Y - self.viewport_height

    def process(self):

        scale = self.selected_legend.Scale
        scale_factor = float(scale) / 100
        offset = mm2ft(10) * scale_factor

        x_margin = mm2ft(0) * scale_factor
        y_margin = mm2ft(0) * scale_factor

        # print len(self.element_types)
        """pre calculation """
        offset = mm2ft(2000) * scale_factor

        for data in self.element_types:
            self.counter += 1

            element = data.get("element")
            elem_width = data.get("width")
            elem_height = data.get("height")

            """get elements bounding box"""
            elem_bb = element.get_BoundingBox(self.selected_legend)

            # print "\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            # print "WIDTH: {}  ________________  HEIGHT: {}".format(elem_width, elem_height)

            viewport_width = elem_width + offset

            """compute min and max bb values"""
            min_x = self.horizontal_x_pos
            min_y = self.viewport_base_y_pos
            min_z = 0

            max_x = min_x + viewport_width
            """set minimum width for the viewport"""
            if max_x - min_x < DoorsAndWindowsScheduleViewport.minimum_viewport_width:
                max_x = min_x + DoorsAndWindowsScheduleViewport.minimum_viewport_width

            max_y = self.viewport_top_y_pos
            max_z = 0

            mn = XYZ(min_x, min_y, min_z)
            mx = XYZ(max_x, max_y, max_z)

            bb = BoundingBoxXYZ()
            bb.Min = mn
            bb.Max = mx

            """check if the right line of the viewport enters the data pane"""
            if mx.X > self.outline.upper_right_point.X:
                """check if the space left is okay for the element to freely reside"""
                width_space_left = self.outline.upper_right_point.X - mn.X
                sharable_units = width_space_left / self.counter  # divide by number of items on the row
                squeezed_width = elem_width + (float(offset) / 2)  # using half of the offset to squeeze object in place

                """##############################################################################################"""
                """##############################################################################################"""
                if width_space_left < squeezed_width:
                    """put the item on the next line rather"""

                    # print "move to next line"

                    """reset counter after every row"""
                    """utilize the counter only if the sharable unit variable will be used"""
                    self.counter = 0

                    """set the bbox to the next line with space in between"""
                    """reset parameters"""
                    self.stepped_times += 1
                    self.row_number += 1

                    """NEW METHOD"""
                    self.horizontal_x_pos = self.outline.lower_left_point.X
                    self.viewport_top_y_pos -= self.viewport_height
                    self.viewport_base_y_pos -= self.viewport_height

                    """ set new viewport height"""
                    self.viewport_height = self.overall_height_lists[self.stepped_times]

                    """check if the baseline extends beyond the title block base"""
                    if self.viewport_base_y_pos > self.outline.lower_left_point.Y:
                        """viewport fits within same title block space"""
                        """check the space between the viewport base and the title block base line limit"""
                        vertical_allowance = self.viewport_base_y_pos - self.outline.lower_left_point.Y
                        if vertical_allowance < self.viewport_height:
                            """set the viewport base line to the title block base line to avoid gap between
                            the last viewport on the base of the last viewport and the title block base line limit"""
                            self.viewport_base_y_pos = self.outline.lower_left_point.Y
                        else:
                            """maintain the viewport baseline"""
                    else:
                        """#####################################################################################"""
                        """############################### move to next sheet ##################################"""
                        """#####################################################################################"""
                        """create new title block"""
                        new_legend_view_id = self.selected_legend.Duplicate(DB.ViewDuplicateOption.Duplicate)
                        self.selected_legend = doc.GetElement(new_legend_view_id)
                        self.selected_legend.Name = "{}-{}".format(self.selected_legend.Name, self.nth_sheet)
                        self.nth_sheet += 1
                        """reset parameters to beginning"""
                        """create the title block element and place it on the sheet"""

                        self.selected_sheet = DB.ViewSheet.Create(doc, self.title_block.GetTypeId())

                        """create the title block element and place it on the sheet"""
                        self.title_block = doc.Create.NewFamilyInstance(XYZ(0, 0, 0), self.title_block.Symbol,
                                                                        self.selected_sheet)

                        old_view = doc.GetElement(self.title_block.OwnerViewId)
                        old_view_sheet_number = old_view.LookupParameter("Sheet Number").AsValueString()

                        self.selected_sheet.Name = old_view.Name
                        self.selected_sheet.SheetNumber = "{}-{}".format(old_view_sheet_number, self.nth_sheet)

                        self.init()

                    """compute min and max bb values"""
                    min_x = self.horizontal_x_pos
                    min_y = self.viewport_base_y_pos
                    min_z = 0

                    max_x = min_x + viewport_width
                    max_y = self.viewport_top_y_pos
                    max_z = 0

                    mn = XYZ(min_x, min_y, min_z)
                    mx = XYZ(max_x, max_y, max_z)

                    bb.Min = mn
                    bb.Max = mx
                else:
                    """squeeze the item on the space"""
                    # print "squeeze the item on the space"
                    bb.Max = XYZ(self.outline.upper_right_point.X, mx.Y, mx.Z)

                """##############################################################################################"""
                """##############################################################################################"""

            vp = CreateDandWViewport(bbox=bb, elem_data=data, drawing_view=self.selected_legend)

            """update the new x pos"""
            self.horizontal_x_pos = max_x

            # print element.Name
            self.elements_in_schedule.update({"type_name": element.Name, "viewport": vp})
            # print self.stepped_times
