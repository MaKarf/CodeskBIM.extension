from Autodesk.Revit import DB
from Autodesk.Revit.DB import Line, XYZ, BoundingBoxXYZ
from Autodesk.Revit.Exceptions import ArgumentsInconsistentException

from DoorNWindowSchedule.Enumerations import IgnoreSidesOfRectangle, CodeskTextNoteType, \
    DoorsAndWindowsScheduleViewport, DoorsAndWindowsScheduleTextNote
from DoorNWindowSchedule.textNoteTypes import get_text_not_type
from DoorNWindowSchedule.transform import ClockwisePointRotation, line_through_points
from imports.DotNetSystem import List
from unitConvert import mm2ft, ft2mm

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


class CreateRectangle:

    def __init__(self, ignore_sides=()):
        # self.height_in_mm = height_in_mm
        # self.width_in_mm = width_in_mm
        self.ignore_sides = ignore_sides

        # self.drawing_view = drawing_view
        # self.scale = drawing_view.Scale
        # self.scale_factor = float(self.scale) / 100

        # self.left_offset = mm2ft(offset[0]) * self.scale_factor
        # self.top_offset = mm2ft(offset[1]) * self.scale_factor
        # self.right_offset = mm2ft(offset[2]) * self.scale_factor
        # self.base_offset = mm2ft(offset[3]) * self.scale_factor

        self.left_line = None
        self.right_line = None
        self.top_line = None
        self.bottom_line = None
        self.bounding_box = None

        self.upper_left_point = None
        self.upper_right_point = None
        self.lower_left_point = None
        self.lower_right_point = None

        # self.from_center()

    def from_bb_man_max(self, drawing_view, element_min_xyz, element_max_xyz, margin=(0, 0, 0, 0)):
        scale = drawing_view.Scale
        scale_factor = float(scale) / 100

        left_offset = mm2ft(margin[0]) * scale_factor
        top_offset = mm2ft(margin[1]) * scale_factor
        right_offset = mm2ft(margin[2]) * scale_factor
        base_offset = mm2ft(margin[3]) * scale_factor

        bb = BoundingBoxXYZ()

        # bb.Min = XYZ(-width_in_ft + left_offset, -height_in_ft + base_offset, 0)
        # bb.Max = XYZ(width_in_ft - right_offset, height_in_ft - top_offset, 0)

        bb.Min = element_min_xyz
        bb.Max = element_max_xyz

        self.create_lines(bb, drawing_view)

    def from_center(self, drawing_view, height_in_mm, width_in_mm, margin=(0, 0, 0, 0)):

        scale = drawing_view.Scale
        scale_factor = float(scale) / 100

        left_offset = mm2ft(margin[0]) * scale_factor
        top_offset = mm2ft(margin[1]) * scale_factor
        right_offset = mm2ft(margin[2]) * scale_factor
        base_offset = mm2ft(margin[3]) * scale_factor

        height_in_ft = mm2ft(height_in_mm / 2) * scale
        width_in_ft = mm2ft(width_in_mm / 2) * scale

        bb = BoundingBoxXYZ()
        bb.Min = XYZ(-width_in_ft + left_offset, -height_in_ft + base_offset, 0)
        bb.Max = XYZ(width_in_ft - right_offset, height_in_ft - top_offset, 0)

        self.create_lines(bb, drawing_view)

    def create_lines(self, bb, drawing_view):
        created_lines = List[DB.ElementId]()
        points = [
            XYZ(bb.Min.X, bb.Min.Y, 0),
            XYZ(bb.Max.X, bb.Min.Y, 0),
            XYZ(bb.Max.X, bb.Max.Y, 0),
            XYZ(bb.Min.X, bb.Max.Y, 0)
        ]

        self.upper_left_point = XYZ(bb.Min.X, bb.Max.Y, 0)
        self.upper_right_point = bb.Max
        self.lower_left_point = bb.Min
        self.lower_right_point = XYZ(bb.Max.X, bb.Min.Y, 0)

        self.bounding_box = bb

        # print "\n################################"

        for i in range(len(points)):
            # print i
            start_point = points[i]

            """Connect the last point to the first point to form a closed loop"""
            end_point = points[(i + 1) % len(points)]

            # print "START POINT: {}  ________________  END POINT: {}".format(start_point, end_point)

            try:

                line = Line.CreateBound(start_point, end_point)
                # curve_loop.Append(line)
                if drawing_view is not None:
                    # created_line = doc.Create.NewDetailCurve(legend_view, line)

                    if i == 0:
                        if IgnoreSidesOfRectangle.bottom not in self.ignore_sides:
                            self.bottom_line = doc.Create.NewDetailCurve(drawing_view, line)
                            created_lines.Add(self.bottom_line.Id)

                    elif i == 1:
                        if IgnoreSidesOfRectangle.right not in self.ignore_sides:
                            self.right_line = doc.Create.NewDetailCurve(drawing_view, line)
                            created_lines.Add(self.right_line.Id)

                    elif i == 2:
                        if IgnoreSidesOfRectangle.top not in self.ignore_sides:
                            self.top_line = doc.Create.NewDetailCurve(drawing_view, line)
                            created_lines.Add(self.top_line.Id)

                    elif i == 3:
                        if IgnoreSidesOfRectangle.left not in self.ignore_sides:
                            self.left_line = doc.Create.NewDetailCurve(drawing_view, line)
                            created_lines.Add(self.left_line.Id)

                    else:
                        # print "err"
                        """"""

            except ArgumentsInconsistentException as ex:
                # print "ERROR: {}".format(i)
                # print ex
                """"""

        return created_lines


class CreateDandWViewport(CreateRectangle):

    def __init__(self, elem_data, bbox, drawing_view=None):
        CreateRectangle.__init__(self)

        self.element_data = elem_data
        self.element = self.element_data.get("element")
        self.element_width = self.element_data.get("width")
        self.element_height = self.element_data.get("height")

        self.bbox = bbox
        self.view = drawing_view

        self.element_category = ""
        self.element_name = ""
        self.element_total_placed = 0
        self.element_locations = []

        self.create_viewport()

        CreateCells(drawing_view=drawing_view, bounding_box=self.bbox, elements_data=self.element_data)

    def create_viewport(self):
        self.create_lines(bb=self.bbox, drawing_view=self.view)


class CreateCells:
    """points input"""

    def __init__(self, drawing_view, bounding_box, elements_data, **kwargs):
        self.view = drawing_view
        self.scale = self.view.Scale
        self.scale_factor = float(self.scale) / 100

        self.horizontal_interval = DoorsAndWindowsScheduleViewport.horizontal_interval
        self.location_textbox_height = DoorsAndWindowsScheduleViewport.location_textbox_height
        self.horizontal_rows = DoorsAndWindowsScheduleViewport.horizontal_rows

        self.bb = bounding_box

        # self.bottom_left_point = self.bb.Min
        # self.top_right_point = None
        # self.top_left_point = None
        # self.bottom_right_point = None

        self.element_data = elements_data
        self.element = self.element_data.get("element")
        self.element_width = self.element_data.get("width")
        self.element_height = self.element_data.get("height")

        self.width = self.bb.Max.X - self.bb.Min.X

        text_note_types = get_text_not_type()
        self.header_text = text_note_types.get(CodeskTextNoteType.schedule_header)
        self.values_text = text_note_types.get(CodeskTextNoteType.schedule_values)
        self.title_text = text_note_types.get(CodeskTextNoteType.schedule_title)
        self.small_text = text_note_types.get(CodeskTextNoteType.schedule_small_text)

        """ ################################################################################################## """
        """ ################################################################################################## """
        """if the door or window is a curtain type, use the instance width and height parameters
         instead of the type because curtain wall doors and windows has not height and width type parameters"""

        """list them in reverse order"""
        if self.element_data.get("total") == 1:
            report_total = "{} unit".format(self.element_data.get("total"))
        else:
            report_total = "{} units".format(self.element_data.get("total"))

        self.values = [{"header": "Total", "value": report_total},
                       {"header": "Width", "value": "{} mm".format(ft2mm(int(self.element_width)))},
                       {"header": "Height", "value": "{} mm".format(ft2mm(int(self.element_height)))},
                       {"header": "Level",
                        "value": self.element_data.get("element").LookupParameter("Level").AsString()}]

        self.horizontal_lines_array()

        """##################################################################################################"""
        """ #################  D R A W    D O O R    O R   W I N D O W    O U T L I N E      ################"""
        """##################################################################################################"""
        """draw door or window outline"""

        # self.draw_element_outline()

        """##################################################################################################"""
        """##################################################################################################"""

    def draw_element_outline(self):

        side_margin = (self.width - self.element_width) / 2

        """the center of the viewport"""
        viewport_bb = DB.BoundingBoxXYZ()

        element_bbox_min_y_cord = self.bb.Min.Y + DoorsAndWindowsScheduleViewport.table_height_with_base_allowance

        viewport_bb.Min = XYZ(self.bb.Min.X + side_margin, element_bbox_min_y_cord, 0)
        viewport_bb.Max = XYZ(viewport_bb.Min.X + self.element_width, viewport_bb.Min.Y + self.element_height, 0)

        """##################################################################################################"""
        """ #################  D R A W    D O O R    O R   W I N D O W    O U T L I N E      ################"""
        """##################################################################################################"""

        # ln = CreateRectangle().create_lines(viewport_bb, self.view)
        # grouped_element = doc.Create.NewGroup(ln)

        try:
            grouped_element = draw_element_outline_on_view(drawing_view=self.view,
                                                           element=self.element,
                                                           scale_factor=self.scale_factor)

            """rename group to the element type name"""
            grouped_element.GroupType.Name = self.element.Symbol.get_Parameter(
                DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()

            """compute the center xyz point of the viewport"""

            placement_min = XYZ(self.bb.Min.X, self.bb.Min.Y + DoorsAndWindowsScheduleViewport.table_height, 0)
            placement_max = XYZ(self.bb.Max.X, self.bb.Max.Y, 0)

            placement_center_point = (placement_min.Add(placement_max)).Divide(2)

            """save the xyz center point of the grouped element"""
            grouped_element_center_point = grouped_element.Location.Point

            """align the center of the grouped element to the center of the viewport"""
            grouped_element.Location.Point = grouped_element_center_point + \
                                             (placement_center_point.Subtract(grouped_element_center_point))
        except Exception as ex:
            print ex

        """##################################################################################################"""
        """ ############  E N D     D R A W    D O O R    O R   W I N D O W    O U T L I N E      ###########"""
        """##################################################################################################"""

    def horizontal_lines_array(self):
        """#################################################################################################"""
        """get room names"""
        """filter out """
        room_objects_list = [i for i in self.element_data.get("rooms") if i]

        room_names_list = [name.LookupParameter("Name").AsString() for name in room_objects_list]

        """remove duplicate room names"""
        refined_room_names_list = []
        [refined_room_names_list.append(x) for x in room_names_list if x not in refined_room_names_list]

        location_text_top_y_pos = self.bb.Min.Y + (
                self.horizontal_interval * self.horizontal_rows) + self.location_textbox_height

        """create the top line of the table"""
        bl = DB.Line.CreateBound(self.bb.Min, DB.XYZ(self.bb.Max.X, self.bb.Min.Y, 0))

        location_top_line = doc.Create.NewDetailCurve(self.view, bl)
        location_top_line.Location.Move(
            XYZ(0, (self.horizontal_interval * self.horizontal_rows) + self.location_textbox_height, 0))

        type_name_text_note = DB.TextNote.Create(doc, self.view.Id,
                                                 XYZ(self.bb.Min.X + DoorsAndWindowsScheduleTextNote.margin,
                                                     location_text_top_y_pos - DoorsAndWindowsScheduleTextNote.margin,
                                                     0),
                                                 "Locations: ",
                                                 self.header_text.Id)
        type_name_text_note.VerticalAlignment = DB.VerticalTextAlignment.Top

        """add header texts"""
        type_mark_text_note = DB.TextNote.Create(doc, self.view.Id,
                                                 XYZ(self.bb.Min.X + DoorsAndWindowsScheduleTextNote.margin,
                                                     location_text_top_y_pos - DoorsAndWindowsScheduleViewport.horizontal_interval,
                                                     0),
                                                 "first_text",
                                                 self.small_text.Id)

        type_mark_text_note.VerticalAlignment = DB.VerticalTextAlignment.Top

        """stretch the text note to fill the table to accommodate all available room names """

        updated_text = ""
        for name in refined_room_names_list:
            index = refined_room_names_list.index(name)
            if index == 0:
                updated_text = updated_text + name
            else:
                updated_text = updated_text + ", " + name
            # print updated_text

        """set the text note text to the cumulated texts"""
        type_mark_text_note.Text = updated_text

        """set the width of the text within the viewport limit"""
        type_mark_text_note.Width = (bl.Length * 0.95) / self.scale

        """################################################################################################ """
        """################################################################################################ """

        for x in range(self.horizontal_rows):
            interval = x * self.horizontal_interval
            h_line = doc.Create.NewDetailCurve(self.view, bl)
            """create copies of lines to form horizontal rows for the table"""
            h_line.Location.Move(XYZ(0, interval, 0))

            """#####################################################################################################"""
            """  create detail annotation"""
            """#####################################################################################################"""
            if x != self.horizontal_rows - 1:
                """add header texts"""

                text_note = DB.TextNote.Create(doc, self.view.Id,
                                               XYZ(self.bb.Min.X + DoorsAndWindowsScheduleTextNote.margin,
                                                   self.bb.Min.Y + interval + (
                                                           self.horizontal_interval * 0.1),
                                                   0),
                                               str(self.values[x].get("header")),
                                               self.header_text.Id)
                text_note.VerticalAlignment = DB.VerticalTextAlignment.Bottom

                """add values texts"""

                text_note_vals = DB.TextNote.Create(doc, self.view.Id,
                                                    XYZ(self.bb.Min.X + DoorsAndWindowsScheduleTextNote.margin + DoorsAndWindowsScheduleViewport.header_cell_width,
                                                        self.bb.Min.Y + interval + (
                                                                self.horizontal_interval * 0.1), 0),
                                                    str(self.values[x].get("value")),
                                                    self.values_text.Id)
                text_note_vals.VerticalAlignment = DB.VerticalTextAlignment.Bottom

            """ ################################################################################################## """
            """  END OF DOORS OPERATIONS"""
            """ ################################################################################################## """

        """create vertical division line"""
        v_line_start = XYZ(self.bb.Min.X + DoorsAndWindowsScheduleViewport.header_cell_width, self.bb.Min.Y, 0)
        v_line_end = XYZ(v_line_start.X, self.bb.Min.Y +
                         (self.horizontal_interval * (self.horizontal_rows - 1)), 0)
        vl = DB.Line.CreateBound(v_line_start, v_line_end)
        doc.Create.NewDetailCurve(self.view, vl)


def draw_element_outline_on_view(drawing_view, element, scale_factor=1.0):
    created_line_ids = List[DB.ElementId]()
    created_lines = []

    options = DB.Options()
    geometry_element = element.get_Geometry(options)

    if drawing_view:

        if drawing_view:

            try:
                """Get the transformation to the legend view's plane"""
                """Iterate through the geometry and project onto the legend view"""

                """######################################################################"""
                """iteration over element types placed in the model"""
                for geometry_object in geometry_element:

                    if isinstance(geometry_object, DB.GeometryInstance):
                        geometry_types = geometry_object.GetSymbolGeometry()
                        # print "{} - Number of Door or Window types placed in the model"
                        list_of_outlines_curve_loop = []
                        """######################################################################"""
                        for geo_ele in geometry_types:
                            # map(visualize_geometry_objects, [geo_ele])

                            if isinstance(geo_ele, DB.Solid):
                                solid = geo_ele
                                # print "solid"

                                """######################################################################"""
                                for face in solid.Faces:

                                    """######################################################################"""
                                    for edge in face.GetEdgesAsCurveLoops():
                                        edge_lines = list(edge.GetCurveLoopIterator())

                                        rotated_points = [(ClockwisePointRotation.at270_on_x_axis(xyz_point)
                                                           for xyz_point in line.Tessellate()).next()
                                                          for line in edge_lines]
                                        # print len(rotated_points)

                                        """set all Z coordinates to 0 since the drawing is on a 2d view."""
                                        """add the reference stating point of the respective table"""
                                        transformed_points = [XYZ(p.X, p.Y, 0) for p in rotated_points]

                                        """Create Detail Components for each point"""

                                        geometric_lines = line_through_points(transformed_points, drawing_view)
                                        created_lines.extend(geometric_lines)

                                        break
                        """ get the entire points or outline of an element type; say Door type 1 """
                        # print list_of_outlines_curve_loop

                        """ group the geometries at this point"""

            finally:
                """Ensure the transaction is closed properly"""
                # print "finally"
    else:
        # print "drawing view not found"
        """"""

    [created_line_ids.Add(i.Id) for i in created_lines]
    grouped_geometry = doc.Create.NewGroup(created_line_ids)
    """return the grouped geometry"""
    return grouped_geometry
