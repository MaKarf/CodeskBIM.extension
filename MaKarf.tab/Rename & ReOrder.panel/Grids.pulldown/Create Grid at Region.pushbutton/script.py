import sys
from Autodesk.Revit import DB
from Autodesk.Revit.DB import Color, XYZ, Line, Grid, FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import OperationCanceledException
from System.Collections.Generic import List

from lib.UI.Popup import Alert
from lib.UI.xamlFiles.RenameGrids import RenameGridsEngine
from lib.codeskResource.codeskUnitConverter import ft2mm
from lib.selection.select_from_ui import rectangular_selection

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Create Grids")

active_view = ui_doc.ActiveView


class SelectElement:
    v_grid_start_y = None
    v_grid_end_y = None

    h_grid_start_x = None
    h_grid_end_x = None

    v_walls = []
    h_walls = []

    boundary_lines = List[DB.ElementId]()

    selection_box_min = None
    selection_box_max = None

    def __init__(self, db_element_type=None):
        self.db_element_type = db_element_type
        # self.get_grid_boundaries()
        self.pick_point()
        self.get_walls()
        self.create_grids()

    def get_grid_boundaries(self):
        """get selected elements"""
        boundary_lines = self.select_elements()

        """######################################################################################################"""
        """ check for the validity of the elements"""
        """######################################################################################################"""
        if len(boundary_lines) > 4:
            Alert(title="Selection Error", header="MORE than FOUR elements are selected",
                  content="Boundary lines must be four detail lines or model lines\n"
                          "enclosing the model on left, right, top and down")
            return None
        elif len(boundary_lines) < 4:
            Alert(title="Selection Error", header="LESS than FOUR elements are selected",
                  content="Boundary lines must be four detail lines or model lines\n"
                          "enclosing the model on left, right, top and down")
            return None

        else:
            pass

        for lns in boundary_lines:
            if lns.GetType() == DB.DetailLine or lns.GetType() == DB.ModelLine:
                pass
            else:
                Alert(title="Selection Error", header="Boundary lines must be either Detail Lines or Model Lines",
                      content="Boundary lines must be either Detail Lines or Model Lines")
                return None
        """######################################################################################################"""
        """######################################################################################################"""

        h = []
        v = []

        for i in boundary_lines:
            bbox = i.get_BoundingBox(active_view)
            print(bbox.Max, bbox.Min)
            if bbox.Min.Y == bbox.Max.Y:
                """get horizontal lines"""
                h.append(i)

            elif bbox.Min.X == bbox.Max.X:
                """get vertical lines"""
                v.append(i)
        """##################################################################################"""
        print("h", h)
        print("v", v)

        if h[0].get_BoundingBox(active_view).Min.Y < h[1].get_BoundingBox(active_view).Min.Y:
            base_line = h[0]
            top_line = h[1]
        else:
            base_line = h[1]
            top_line = h[0]
        """##################################################################################"""

        """##################################################################################"""
        if v[0].get_BoundingBox(active_view).Min.X < v[1].get_BoundingBox(active_view).Min.X:
            left_line = v[0]
            right_line = v[1]
        else:
            right_line = v[1]
            left_line = v[0]
        """##################################################################################"""
        """set the extents for the grids"""
        self.h_grid_start_x = left_line.get_BoundingBox(active_view).Min.X
        self.h_grid_end_x = right_line.get_BoundingBox(active_view).Min.X

        self.v_grid_start_y = base_line.get_BoundingBox(active_view).Min.Y
        self.v_grid_end_y = top_line.get_BoundingBox(active_view).Min.Y

        """get selection bounding box"""
        top_box = top_line.get_BoundingBox(active_view)
        base_box = base_line.get_BoundingBox(active_view)
        # print(base_box)

        self.selection_box_min = XYZ(base_box.Min.X, base_box.Min.Y, -1000)
        self.selection_box_max = XYZ(top_box.Max.X, top_box.Max.Y, 1000)

        # print(self.selection_box_min)
        # print(self.selection_box_max)

    def pick_point(self):
        rect_selection = rectangular_selection()

        self.selection_box_min = rect_selection[0]
        self.selection_box_max = rect_selection[1]

        """##################################################################################"""
        """set the extents for the grids"""
        self.h_grid_start_x = self.selection_box_min.X
        self.h_grid_end_x = self.selection_box_max.X

        self.v_grid_start_y = self.selection_box_min.Y
        self.v_grid_end_y = self.selection_box_max.Y

    def select_elements(self):
        """get selected elements"""
        ui_selected = ui_doc.Selection.GetElementIds()

        if len(ui_selected) == 0:
            bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
            selection_bg_color = Color(247, 191, 158)
            try:
                app.BackgroundColor = selection_bg_color

                boundary_lines = rectangular_selection(BuiltInCategory.OST_Lines)

                app.BackgroundColor = bg_color

                [self.boundary_lines.Add(i.Id) for i in boundary_lines]
                return [i for i in boundary_lines]

            except OperationCanceledException as user_interrupt:
                app.BackgroundColor = bg_color

                Alert("", header="Operation cancelled")
                sys.exit()

        else:
            [self.boundary_lines.Add(i) for i in ui_selected]

            boundary_lines = [doc.GetElement(i) for i in ui_selected]
            return [i for i in boundary_lines]

    def get_walls(self):
        """get all walls in the revit project"""
        all_walls = FilteredElementCollector(doc).OfCategory(
            BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

        walls_in_region = []
        location_id_check_list = []

        """#########################################################################################################"""
        """filter out only walls in selection region"""
        inside = 0
        outside = 0
        for wall in all_walls:
            wall_bbox = wall.get_BoundingBox(active_view)

            # print("__________________________________________________________")
            # print("selection min : {}".format(self.selection_box_min))
            # print("selection max : {}".format(self.selection_box_max))
            # print("__________")
            # print("wall min : {}".format(wall_bbox.Min))
            # print("wall max : {}".format(wall_bbox.Max))
            # print("__________________________________________________________")

            if wall_bbox.Min.X < self.selection_box_min.X or wall_bbox.Min.Y < self.selection_box_min.Y or \
                    wall_bbox.Max.X > self.selection_box_max.X or wall_bbox.Max.Y > self.selection_box_max.Y:
                # print("wall is beyond")
                outside += 1

            else:
                # print("wall is inside scope")
                inside += 1
                walls_in_region.append(wall)

        # print("Selected Walls: {}".format(inside))
        # print("Rejected Walls: {}".format(outside))
        """#########################################################################################################"""

        for x in walls_in_region:
            try:
                wall_center = x.Location.Curve.Origin
                # print(wall_center)

                start_point = x.Location.Curve.GetEndPoint(0)
                end_point = x.Location.Curve.GetEndPoint(1)
                # print("startpoint", start_point)
                # print("endpoint", end_point)
                # print("___________________________-")

                if ft2mm(start_point[0]) == ft2mm(end_point[0]):
                    # print("vertical wall")
                    location_id = ft2mm(start_point[0])

                    if location_id not in location_id_check_list:
                        self.v_walls.append(x)
                        location_id_check_list.append(location_id)

                elif ft2mm(start_point[1]) == ft2mm(end_point[1]):
                    # print("horizontal")
                    location_id = ft2mm(start_point[1])

                    if location_id not in location_id_check_list:
                        self.h_walls.append(x)
                        location_id_check_list.append(location_id)

                else:
                    pass
            except AttributeError:
                # print(x)
                pass
        # print("verticals:", len(self.v_walls))
        # print("horizontals:", len(self.h_walls))

    def create_grids(self):
        t.Start()
        try:
            for h_wall in self.h_walls:
                grid_y_axis = h_wall.Location.Curve.Origin[1]

                """create grid lines"""
                horizontal_start_point = XYZ(self.h_grid_start_x, grid_y_axis, 0)
                horizontal_end_point = XYZ(self.h_grid_end_x, grid_y_axis, 0)
                line = Line.CreateBound(horizontal_start_point, horizontal_end_point)

                grid = Grid.Create(doc, line)
                doc.GetElement(grid.GetTypeId()).LookupParameter("Plan View Symbols End 1 (Default)").Set(1)

            for v_wall in self.v_walls:
                grid_x_axis = v_wall.Location.Curve.Origin[0]

                """create grid lines"""
                vertical_start_point = XYZ(grid_x_axis, self.v_grid_start_y, 0)
                vertical_end_point = XYZ(grid_x_axis, self.v_grid_end_y, 0)
                line = Line.CreateBound(vertical_start_point, vertical_end_point)

                Grid.Create(doc, line)

            """ delete boundary lines after successfully creating grids"""
            doc.Delete(self.boundary_lines)

            t.Commit()
        except Exception as e:
            Alert(title="Error", header="Unknown Error",
                  content=str(e))
            t.RollBack()
            sys.exit()


SelectElement()
RenameGridsEngine()

