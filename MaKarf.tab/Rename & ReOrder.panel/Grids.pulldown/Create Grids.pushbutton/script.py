from Autodesk.Revit import DB
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import XYZ, Line, Grid, FilteredElementCollector as Fec, BuiltInCategory as Bic
from System.Collections.Generic import List

from UI.xamlFiles.DoubleTextBox import DoubleTextBox
from UI.xamlFiles.Grids.CommonImports import SelectionType
from UI.xamlFiles.Grids.Rename.RenameGrids import RenameGrids

from codeskResource.codeskUnitConverter import ft2mm
from selection.getModelElements import GetModelElements
from selection.ui_selection import rectangular_selection

from unitConvert import mm2ft

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

    main_grids = []

    boundary_lines = List[DB.ElementId]()

    selection_box_min = None
    selection_box_max = None

    """get the the highest Z coordinate from the highest model element from the revit project"""
    categories = [Bic.OST_Walls,
                  Bic.OST_Floors,
                  Bic.OST_GenericModel,
                  Bic.OST_Roofs
                  ]
    max_z = GetModelElements(categories).get_model_elements_max_z_height()

    # print(max_z)

    def __init__(self, db_element_type=None):
        self.get_grid_boundaries()

        ui = DoubleTextBox(title="Exclude Walls From Griding",
                           label_name1="Wall Length Exclusion (mm)",
                           label_name2="Wall Height Exclusion (mm)",
                           button_name="Finish")

        self.wall_length_limit = mm2ft(float(ui.text_results1))
        self.wall_height_limit = mm2ft(float(ui.text_results2))

        self.db_element_type = db_element_type

        self.get_walls()
        self.create_grids()

    def get_grid_boundaries(self):
        rect_selection = rectangular_selection(is_two_d_view=False)

        self.selection_box_min = rect_selection[0]
        self.selection_box_max = rect_selection[1]

        """##################################################################################"""
        """set the extents for the grids"""
        self.h_grid_start_x = self.selection_box_min.X
        self.h_grid_end_x = self.selection_box_max.X

        self.v_grid_start_y = self.selection_box_min.Y
        self.v_grid_end_y = self.selection_box_max.Y

    def get_walls(self):
        """get all walls in the revit project"""
        all_walls = Fec(doc).OfCategory(
            Bic.OST_Walls).WhereElementIsNotElementType().ToElements()

        """ second filter: remove kerbs and short walls from wall collection"""
        """1.968504 equals 600mm in feet
        remove all short wall length walls as well"""
        filtered_walls = [wall for wall in all_walls
                          if wall.LookupParameter("Length").AsDouble() > self.wall_length_limit
                          and wall.LookupParameter("Unconnected Height").AsDouble() > self.wall_height_limit
                          ]

        walls_in_region = []
        location_id_check_list = []

        """#########################################################################################################"""
        """filter out only walls in selection region"""
        inside = 0
        outside = 0
        for wall in filtered_walls:
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

        # """ second filter: remove kerbs and short walls from wall collection"""
        # """1.968504 equals 600mm in feet"""
        # self.v_walls = [vw for vw in self.v_walls if vw.LookupParameter("Unconnected Height").AsDouble() > 1.968504]
        # self.h_walls = [vw for vw in self.h_walls if vw.LookupParameter("Unconnected Height").AsDouble() > 1.968504]

    def create_grids(self):
        existing_grids = Fec(doc).OfCategory(
            Bic.OST_Grids).WhereElementIsNotElementType().ToElements()
        # print(existing_grids)

        """ filter out walls with grids"""
        existing_grid_x_axis = [i.Curve.Origin[0] for i in existing_grids]
        existing_grid_y_axis = [i.Curve.Origin[1] for i in existing_grids]

        existing_grid_ = [i for i in existing_grids]

        t.Start()
        # try:
        for v_wall in self.v_walls:
            grid_x_axis = v_wall.Location.Curve.Origin[0]

            """check if a grid is already placed in the same location to avoid duplicate grid placement on same 
            location"""
            if grid_x_axis not in existing_grid_x_axis:
                """create grid lines"""
                vertical_start_point = XYZ(grid_x_axis, self.v_grid_start_y, 0)
                vertical_end_point = XYZ(grid_x_axis, self.v_grid_end_y, 0)
                line = Line.CreateBound(vertical_start_point, vertical_end_point)

                created_grid = Grid.Create(doc, line)
                self.main_grids.append(created_grid)

                """adjust grids height using bounding box"""
                created_grid.SetVerticalExtents(0, self.max_z)
            else:
                grid_index = existing_grid_x_axis.index(grid_x_axis)
                grid_to_extend = existing_grid_[grid_index]

                prev_grid = grid_to_extend
                prev_grid_name = prev_grid.Name

                """delete existing grid and use its properties to create a new one"""
                doc.Delete(prev_grid.Id)

                vertical_start_point = XYZ(grid_x_axis, self.v_grid_start_y, 0)
                vertical_end_point = XYZ(grid_x_axis, self.v_grid_end_y, 0)

                line = Line.CreateBound(vertical_start_point, vertical_end_point)
                new_v_grid = Grid.Create(doc, line)
                self.main_grids.append(new_v_grid)

                """adjust grids height using bounding box"""
                new_v_grid.SetVerticalExtents(0, self.max_z)

                new_v_grid.Name = prev_grid_name

                """ PARAMETERS FOR EXTENDING GRIDS START AND END POINTS INSTEAD OF DELETING AND RECREATING """

        for h_wall in self.h_walls:
            grid_y_axis = h_wall.Location.Curve.Origin[1]

            """check if a grid is already placed in the same location to avoid duplicate grid placement on
            same location"""
            if grid_y_axis not in existing_grid_y_axis:
                """create grid lines"""
                horizontal_start_point = XYZ(self.h_grid_start_x, grid_y_axis, 0)
                horizontal_end_point = XYZ(self.h_grid_end_x, grid_y_axis, 0)
                line = Line.CreateBound(horizontal_start_point, horizontal_end_point)

                grid = Grid.Create(doc, line)
                self.main_grids.append(grid)

                doc.GetElement(grid.GetTypeId()).LookupParameter("Plan View Symbols End 1 (Default)").Set(1)

                """adjust grids height using bounding box"""
                grid.SetVerticalExtents(0, self.max_z)

            else:

                grid_y_index = existing_grid_y_axis.index(grid_y_axis)
                grid_to_extend = existing_grid_[grid_y_index]

                prev_grid = grid_to_extend
                prev_grid_name = prev_grid.Name

                """delete existing grid and use its properties to create a new one"""
                doc.Delete(prev_grid.Id)

                horizontal_start_point = XYZ(self.h_grid_start_x, grid_y_axis, 0)
                horizontal_end_point = XYZ(self.h_grid_end_x, grid_y_axis, 0)
                line = Line.CreateBound(horizontal_start_point, horizontal_end_point)

                new_h_grid = Grid.Create(doc, line)
                self.main_grids.append(new_h_grid)

                new_h_grid.Name = prev_grid_name

                """adjust grids height using bounding box"""
                new_h_grid.SetVerticalExtents(0, self.max_z)

        t.Commit()


created_grids = SelectElement()

ui = RenameGrids(selection_type=SelectionType.select_from_list,
                 include_hidden_grids=None,
                 list_of_grids=created_grids.main_grids)
