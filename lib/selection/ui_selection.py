from Autodesk.Revit.Exceptions import OperationCanceledException
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType, PickBoxStyle
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic, XYZ, Color

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView


def rectangular_selection_by_category(built_in_category=None, as_elements=True, temp_bg_color=None):
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    selection_bg_color = Color(247, 191, 158) if temp_bg_color is None else Color(temp_bg_color.Red,
                                                                                  temp_bg_color.Green,
                                                                                  temp_bg_color.Blue)

    el = Fec(doc).OfCategory(built_in_category).WhereElementIsNotElementType().FirstElement()

    if el:
        category_id = el.Category.Id.IntegerValue

        try:
            app.BackgroundColor = selection_bg_color
            if category_id is None:
                selected_references = ui_doc.Selection.PickObjects(ObjectType.Element)
            else:
                selection_filter = ElementSelectFilter([int(category_id)])
                selected_references = ui_doc.Selection.PickObjects(ObjectType.Element, selection_filter)

            if as_elements:
                app.BackgroundColor = bg_color
                return [doc.GetElement(ref) for ref in selected_references]
            else:
                app.BackgroundColor = bg_color
                return list(selected_references)

        except OperationCanceledException:  # user_interrupt
            app.BackgroundColor = bg_color
            return None
    else:
        return None


class ElementSelectFilter(ISelectionFilter):
    def __init__(self, category_ids=None, *args):

        if category_ids is None:
            self.allowed_categories = None
        else:
            self.allowed_categories = category_ids

    def AllowElement(self, element):
        if self.allowed_categories is None:
            return True
        elif element.Category.Id.IntegerValue in self.allowed_categories:
            return True
        else:
            return False

    def AllowReference(self, reference, point):
        return True


"""function to hide selected elements from the revit ui"""


def hide_selection(ui_selection):
    """ get list of all views in which the elements will be hidden"""
    all_views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()

    """ check if selection is a Group or model elements"""
    for el in ui_selection:
        elem_cate_name = doc.GetElement(el).Category.Name
        if elem_cate_name == "Model Groups" or elem_cate_name == "Detail Groups":
            """hide model elements"""
            """ ############################################################################"""
            for view in all_views:
                try:
                    view.HideElements(doc.GetElement(el).GetMemberIds())
                except Exception:
                    pass
            """ ############################################################################"""

            """ ############################################################################"""
        else:
            """hide elements"""
            for view in all_views:
                try:
                    view.HideElements(ui_selection)
                except Exception:
                    pass
            """ ############################################################################"""


"""function to unhide selected elements from the revit ui"""


def unhide_selection(ui_selection):
    """ get list of all views in which the elements will be hidden"""
    all_views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()

    """ check if selection is a Group or model elements"""
    for el in ui_selection:
        elem_cate_name = doc.GetElement(el).Category.Name
        if elem_cate_name == "Model Groups" or elem_cate_name == "Detail Groups":
            """hide model elements"""
            """ ############################################################################"""
            for view in all_views:
                try:
                    view.UnhideElements(doc.GetElement(el).GetMemberIds())
                except Exception:
                    pass
            """ ############################################################################"""

            """ ############################################################################"""
        else:
            """hide elements"""
            for view in all_views:
                try:
                    view.UnhideElements(ui_selection)
                except Exception:
                    pass
            """ ############################################################################"""


def rectangular_selection(is_two_d_view=True, z_cord=None):
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    selection_bg_color = Color(247, 191, 158)

    try:
        app.BackgroundColor = selection_bg_color
        sel = ui_doc.Selection.PickBox(PickBoxStyle.Enclosing)
        # print("Selection Minimum Point: {}".format(sel.Min))
        # print("Selection Maximum Point: {}".format(sel.Max))

        app.BackgroundColor = bg_color

    except OperationCanceledException:
        app.BackgroundColor = bg_color
        return None

    _min = sel.Min
    _max = sel.Max

    # print("IS 2d: {}".format(is_two_d_view))
    # print("Z cord: {}".format(z_cord))
    # print("____________________________--")

    if is_two_d_view:
        min_z = 0
        max_z = 0
    else:
        if z_cord is None:
            min_z = 0
            max_z = 0
        else:
            # print("Length of z cords: {}".format(len(z_cord)))
            if len(z_cord) == 1:
                # print("len is 1")
                # print(z_cord[0])
                min_z = -z_cord[0]
                max_z = z_cord[0]
            elif len(z_cord) == 2:
                # print("len is 2")
                # print(z_cord[0])
                # print(z_cord[1])
                min_z = z_cord[0]
                max_z = z_cord[1]
            else:
                # Alert("Z Cord Error", header="invalid values in Z cord")
                return None
    # print("***************************************************")
    # print(min_z)
    # print(max_z)
    # print("***************************************************")

    selection_bounding_box_min = None
    selection_bounding_box_max = None
    res = ""

    if _min.X < _max.X and _min.Y > _max.Y:
        res = """selection direction was from top left to bottom right"""
        selection_bounding_box_min = XYZ(_min.X, _max.Y, min_z)
        selection_bounding_box_max = XYZ(_max.X, _min.Y, max_z)

    elif _min.X > _max.X and _min.Y < _max.Y:
        res = """selection direction was from bottom right to top left"""
        selection_bounding_box_min = XYZ(_max.X, _min.Y, min_z)
        selection_bounding_box_max = XYZ(_min.X, _max.Y, max_z)

    elif _min.X > _max.X and _min.Y > _max.Y:
        res = """selection direction was from top right to bottom left"""

        selection_bounding_box_min = XYZ(_max.X, _max.Y, min_z)
        selection_bounding_box_max = XYZ(_min.X, _min.Y, max_z)

    elif _min.X < _max.X and _min.Y < _max.Y:
        res = """selection direction was from bottom left to top right"""
        selection_bounding_box_min = XYZ(_min.X, _min.Y, min_z)
        selection_bounding_box_max = XYZ(_max.X, _max.Y, max_z)

    # print(res)
    # print("Min", selection_bounding_box_min)
    # print("Max", selection_bounding_box_max)

    return selection_bounding_box_min, selection_bounding_box_max


def decide_inclusion(self, selection_boundary, element_scope):
    """get walls in region"""
    walls = Fec(doc).OfCategory(Bic.OST_Walls).WhereElementIsNotElementType().ToElements()

    inside = 0
    outside = 0
    for wall in walls:
        wall_bbox = wall.get_BoundingBox(active_view)
        if wall_bbox.Min.X < self.selection_box_min.X or wall_bbox.Min.Y < self.selection_box_min.Y or \
                wall_bbox.Max.X > self.selection_box_max.X or wall_bbox.Max.Y > self.selection_box_max.Y:
            print("wall is beyond")
            outside += 1

        else:
            print("wall is inside scope")
            inside += 1

    print("Selected Walls: {}".format(inside))
    print("Rejected Walls: {}".format(outside))


def pick_point():
    sel = ui_doc.Selection.PickBox(PickBoxStyle.Enclosing)
    _min = sel.Min
    _max = sel.Max

    min_z = -1000
    max_z = abs(min_z)

    selection_bounding_box_min = None
    selection_bounding_box_max = None
    res = ""

    if _min.X < _max.X and _min.Y > _max.Y:
        res = """selection direction was from top left to bottom right"""
        selection_bounding_box_min = XYZ(_min.X, _max.Y, min_z)
        selection_bounding_box_max = XYZ(_max.X, _min.Y, max_z)

    elif _min.X > _max.X and _min.Y < _max.Y:
        res = """selection direction was from bottom right to top left"""
        selection_bounding_box_min = XYZ(_max.X, _min.Y, min_z)
        selection_bounding_box_max = XYZ(_min.X, _max.Y, max_z)

    elif _min.X > _max.X and _min.Y > _max.Y:
        res = """selection direction was from top right to bottom left"""
        selection_bounding_box_min = XYZ(_max.X, _max.Y, min_z)
        selection_bounding_box_max = XYZ(_min.X, _min.Y, max_z)

    elif _min.X < _max.X and _min.Y < _max.Y:
        res = """selection direction was from bottom left to top right"""
        selection_bounding_box_min = XYZ(_min.X, _min.Y, min_z)
        selection_bounding_box_max = XYZ(_max.X, _max.Y, max_z)

    # print(res)
    # print("Min", selection_bounding_box_min)
    # print("Max", selection_bounding_box_max)

    return selection_bounding_box_min, selection_bounding_box_max
