import itertools
import operator

from Autodesk.Revit import DB
from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction, BuiltInCategory, \
    ElementCategoryFilter, Line, XYZ, BoundingBoxXYZ

from lib.SortNatural import real_sorting
from lib.phases import new_construction_phase
from lib.unitConvert import mm2ft, ft2mm

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "legend component")
active_view = doc.ActiveView

"""######################################################################################################"""
"""######################################################################################################"""


def create_reference_planes_from_center(view, height_in_mm, width_in_mm, offset=(0, 0, 0, 0)):
    created_lines = []
    scale = view.Scale
    scale_factor = float(scale) / 100

    left_offset = mm2ft(offset[0]) * scale
    top_offset = mm2ft(offset[1]) * scale
    right_offset = mm2ft(offset[2]) * scale
    base_offset = mm2ft(offset[3]) * scale

    height_in_ft = mm2ft(height_in_mm / 2) * scale
    width_in_ft = mm2ft(width_in_mm / 2) * scale

    """get the bounding box of the column"""
    bb = BoundingBoxXYZ()
    bb.Min = XYZ(-width_in_ft + left_offset, -height_in_ft + base_offset, 0)
    bb.Max = XYZ(width_in_ft - right_offset, height_in_ft - top_offset, 0)

    points = [
        XYZ(bb.Min.X, bb.Min.Y, 0),
        XYZ(bb.Max.X, bb.Min.Y, 0),
        XYZ(bb.Max.X, bb.Max.Y, 0),
        XYZ(bb.Min.X, bb.Max.Y, 0)
    ]

    for i in range(len(points)):
        start_point = points[i]

        """Connect the last point to the first point to form a closed loop"""
        end_point = points[(i + 1) % len(points)]

        line = Line.CreateBound(start_point, end_point)

        # created_line = doc.Create.NewDetailCurve(legend_view, line)

        """Create a ReferencePlane by specifying a ReferenceArray, which defines the plane"""
        reference_plane = doc.Create.NewReferencePlane(
            start_point,  # Origin point of the reference plane
            end_point,  # Direction vector of the reference plane
            XYZ(0, 0, 1),  # Normal vector of the reference plane
            view
        )

        # created_lines.append(created_line)

    return created_lines


def place_legend_on_sheet(tt_block, legend, placement_sheet):
    v = Fec(doc).OfCategory(Bic.OST_Viewports).WhereElementIsElementType().FirstElement()

    if tt_block is not None:
        if placement_sheet is not None:
            bb = tt_block.get_BoundingBox(placement_sheet)
            x_pos = bb.Min.X + (bb.Max.X - bb.Min.X) / 2
            y_pos = bb.Min.Y + (bb.Max.Y - bb.Min.Y) / 2

            """place on sheet"""
            viewport_location = DB.XYZ(x_pos, y_pos, 0)

            if legend is not None:
                vp = DB.Viewport.Create(doc, placement_sheet.Id, legend.Id, viewport_location)

                vp_col = [i for i in vp.GetValidTypes() if
                          doc.GetElement(i).LookupParameter("Show Extension Line").AsInteger() == 0 and
                          doc.GetElement(i).LookupParameter("Show Title").AsInteger() == 0]
                try:
                    """change viewport type to hide extension line"""
                    vp.ChangeTypeId(vp_col.pop())

                except IndexError:
                    """create and set a new viewport with hidden title and extension line if none exist"""
                    created_vp = doc.GetElement(vp.GetTypeId()).Duplicate("Hidden Title and Extension")
                    created_vp.LookupParameter("Show Extension Line").Set(0)
                    created_vp.LookupParameter("Show Title").Set(0)
                    vp.ChangeTypeId(created_vp.Id)


def place_legend_component():
    door = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsElementType().FirstElement()
    window = Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsElementType().FirstElement()

    """place a door on the legend_view view"""
    ui_doc.PromptToPlaceElementTypeOnLegendView(door)

    """place a window on the legend_view view"""
    ui_doc.PromptToPlaceElementTypeOnLegendView(window)

    """category filter to get only Legend Components"""
    category_filter = ElementCategoryFilter(BuiltInCategory.OST_LegendComponents)

    dep = doc.ActiveView.GetDependentElements(category_filter)
    for index, element in enumerate(dep):
        # print doc.GetElement(e)
        print index, " -- ", doc.GetElement(element)


def create_and_get_drafting_view(given_name=None):
    view_type = None
    for leg in Fec(doc).OfClass(DB.ViewFamilyType).WhereElementIsElementType().ToElements():
        if leg.ViewFamily == DB.ViewFamily.Drafting:
            view_type = leg
            break

    created_legend = DB.ViewDrafting.Create(document=doc, viewFamilyTypeId=view_type.Id)
    created_legend.Scale = 50

    if given_name is not None:
        try:
            created_legend.Name = given_name
        except:
            """name exist"""
            pass

    return created_legend


class DoorsAndWindows:
    doors_collection = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsNotElementType().ToElements()
    windows_collection = Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsNotElementType().ToElements()

    def __init__(self):
        # self.ordered_door_types = self.instantiate_type(self.doors_collection)
        # self.ordered_window_types = self.instantiate_type(self.windows_collection)
        pass

    @staticmethod
    def get_all_as_ui_dropdown_data():
        dw = DoorsAndWindows()
        doors = dw.get_door_types_as_data_dict()
        windows = dw.get_window_types_as_data_dict()

        data_list = []

        if doors is not None:
            data_list.append({"name": "Doors", "element": doors})

        if windows is not None:
            data_list.append({"name": "Windows", "element": windows})

        if doors is not None and windows is not None:
            doors_n_windows = doors
            doors_n_windows.extend(windows)
            data_list.append({"name": "Doors & Windows", "element": doors_n_windows})

        return data_list

    # @property
    def get_door_types_as_data_dict(self):
        return self.instantiate_type(self.doors_collection)

    # @property
    def get_window_types_as_data_dict(self):
        return self.instantiate_type(self.windows_collection)

    @staticmethod
    def instantiate_type(door_or_window_collections):

        list_of_elements = []
        list_of_elements_dicts = []
        family_type = "family_type"
        if len(door_or_window_collections) == 0:
            return None
        else:

            for item in door_or_window_collections:
                # print(door.Name)

                """get element width"""
                element_width = item.Symbol.get_Parameter(DB.BuiltInParameter.CASEWORK_WIDTH).AsDouble()
                if element_width == 0:
                    element_width = item.get_Parameter(DB.BuiltInParameter.CASEWORK_WIDTH).AsDouble()

                """get element width"""
                element_height = item.Symbol.get_Parameter(DB.BuiltInParameter.WINDOW_HEIGHT).AsDouble()
                if element_height == 0:
                    element_height = item.get_Parameter(DB.BuiltInParameter.WINDOW_HEIGHT).AsDouble()

                """get attached room names"""
                if item.Room[new_construction_phase]:
                    room = item.Room[new_construction_phase]
                    # print(room_name.LookupParameter("Name").AsString())
                else:
                    if item.FromRoom[new_construction_phase]:
                        room = item.FromRoom[new_construction_phase]
                    elif item.ToRoom[new_construction_phase]:
                        room = item.ToRoom[new_construction_phase]
                    else:
                        room = None

                """create dictionary of Revit element to Type Mark  and populate them into the list_of_elements list"""
                list_of_elements.append({"element": item,
                                         family_type: item.Name,
                                         "room": room,
                                         "width": element_width,
                                         "height": element_height})

            """sort dicts"""
            list_of_elements = real_sorting(list_of_elements, dict_key=family_type)

            # for f in self.list_of_elements:
            #     print(f.get(self.element_type))

            """ group dicts by name"""
            index_count = 0
            for i, g in itertools.groupby(list_of_elements, key=operator.itemgetter(family_type)):
                grouped_list = list(g)
                """compile the room names from individual rooms to the selected door data for display in the schedule"""
                room_list = [items.get("room") for items in grouped_list]

                """remove duplicate rooms from list"""
                refined_room_list = room_list

                # print(room_list)
                # print("\n\n\n")
                total = len(grouped_list)

                """add total units of each door or window type to dictionary"""
                """update dicts with total"""
                """get only one instance from all instances of all types using the [0]"""
                selected_element = grouped_list[0]
                selected_element.update({"total": total, "rooms": refined_room_list})

                # print(selected_element)
                list_of_elements_dicts.append(selected_element)

            """sort dicts"""
            list_of_elements_dicts = real_sorting(list_of_elements_dicts, dict_key=family_type)
            return list_of_elements_dicts
