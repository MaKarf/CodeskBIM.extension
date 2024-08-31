import sys

from Autodesk.Revit.DB import Transaction, BoundingBoxXYZ, XYZ, Color
from Autodesk.Revit.Exceptions import OperationCanceledException
from Autodesk.Revit.UI.Selection import PickBoxStyle

doc = __revit__.ActiveUIDocument.Document
ui_doc = __revit__.ActiveUIDocument
active_view = ui_doc.ActiveView
app = __revit__.Application
rvt_year = int(app.VersionNumber)
t = Transaction(doc, "Crop view")


def rectangular_selection(is_two_d_view=True, z_cord=None):
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    selection_bg_color = Color(247, 191, 158)

    try:
        app.BackgroundColor = selection_bg_color
        selection = ui_doc.Selection.PickBox(PickBoxStyle.Enclosing)
        proceed(selection)
        app.BackgroundColor = bg_color

    except OperationCanceledException:
        app.BackgroundColor = bg_color
        sys.exit()


def proceed(sel):
    """rearrange the minimum and maximum values from the unordered selection points"""
    min_x = min(sel.Min.X, sel.Max.X)
    min_y = min(sel.Min.Y, sel.Max.Y)
    min_z = min(sel.Min.Z, sel.Max.Z)

    max_x = max(sel.Min.X, sel.Max.X)
    max_y = max(sel.Min.Y, sel.Max.Y)
    max_z = max(sel.Min.Z, sel.Max.Z)

    selection_bounding_box_min = XYZ(min_x, min_y, min_z)
    selection_bounding_box_max = XYZ(max_x, max_y, max_z)

    # print("Selection Minimum Point: {}".format(sel.Min))
    # print("Selection Maximum Point: {}".format(sel.Max))
    # print("\n************************************************\n")
    # print("Actual Minimum Point: {}".format(selection_bounding_box_min))
    # print("Actual Maximum Point: {}".format(selection_bounding_box_max))
    # print("\n************************************************\n************************************************")
    # print("CROP MIN", active_view.CropBox.Min)
    # print("CROP MAX", active_view.CropBox.Max)
    # print("\n************************************************\n************************************************")

    orientation = ""
    active_view_crop_box = active_view.CropBox

    """create new bounding box"""
    new_bbox = BoundingBoxXYZ()

    if active_view.ViewDirection.IsAlmostEqualTo(XYZ(0, 1, 0)):
        orientation = "North"

        """ new_position = old value + (new value - old value)"""
        new_crop_view_min_x = active_view_crop_box.Min.X + (selection_bounding_box_min.X - active_view_crop_box.Min.X)
        new_crop_view_max_x = active_view_crop_box.Max.X + (selection_bounding_box_max.X - active_view_crop_box.Max.X)
        new_crop_view_max_y = active_view_crop_box.Max.Z + (selection_bounding_box_max.Z - active_view_crop_box.Max.Z)
        new_crop_view_min_y = active_view_crop_box.Min.Z + (selection_bounding_box_min.Z - active_view_crop_box.Min.Z)

        """update new bounding box Min and Max values"""
        new_bbox.Min = XYZ(new_crop_view_min_x, new_crop_view_min_y - 4, active_view_crop_box.Min.Y)
        new_bbox.Max = XYZ(new_crop_view_max_x, new_crop_view_max_y - 4, active_view_crop_box.Max.Y)
        t.Start()
        active_view.CropBox = new_bbox
        turn_crop_on()
        t.Commit()

    elif active_view.ViewDirection.IsAlmostEqualTo(XYZ(0, -1, 0)):
        orientation = "South"

        """ new_position = old value + (new value - old value)"""
        new_crop_view_min_x = active_view_crop_box.Min.X + (selection_bounding_box_min.X - active_view_crop_box.Min.X)
        new_crop_view_max_x = active_view_crop_box.Max.X + (selection_bounding_box_max.X - active_view_crop_box.Max.X)
        new_crop_view_max_y = active_view_crop_box.Max.Z + (selection_bounding_box_max.Z - active_view_crop_box.Max.Z)
        new_crop_view_min_y = active_view_crop_box.Min.Z + (selection_bounding_box_min.Z - active_view_crop_box.Min.Z)

        """update new bounding box Min and Max values"""
        new_bbox.Min = XYZ(new_crop_view_min_x, new_crop_view_min_y - 4, active_view_crop_box.Min.Y)
        new_bbox.Max = XYZ(new_crop_view_max_x, new_crop_view_max_y - 4, active_view_crop_box.Max.Y)
        t.Start()
        active_view.CropBox = new_bbox
        turn_crop_on()
        t.Commit()

    elif active_view.ViewDirection.IsAlmostEqualTo(XYZ(-1, 0, 0)):
        orientation = "West"

    elif active_view.ViewDirection.IsAlmostEqualTo(XYZ(1, 0, 0)):
        orientation = "East"

        # """ new_position = old value + (new value - old value)"""
        # new_crop_view_min_x = active_view_crop_box.Min.X + (selection_bounding_box_min.X - active_view_crop_box.Min.X)
        # new_crop_view_max_x = active_view_crop_box.Max.X + (selection_bounding_box_max.X - active_view_crop_box.Max.X)
        #
        # new_crop_view_min_y = active_view_crop_box.Min.Y + (selection_bounding_box_min.Y - active_view_crop_box.Min.Y)
        # new_crop_view_max_y = active_view_crop_box.Max.Y + (selection_bounding_box_max.Y - active_view_crop_box.Max.Y)
        #
        # """update new bounding box Min and Max values"""
        # new_bbox.Min = XYZ(new_crop_view_min_x, new_crop_view_min_y, active_view_crop_box.Min.Z)
        # new_bbox.Max = XYZ(new_crop_view_max_x, new_crop_view_max_y, active_view_crop_box.Max.Z)
        # print("Calculated Minimum Point: {}".format(new_bbox.Min))
        # print("Calculated Maximum Point: {}".format(new_bbox.Max))
        # t.Start()
        # active_view.CropBox = new_bbox
        # t.Commit()

    elif active_view.ViewDirection.IsAlmostEqualTo(XYZ(0, 0, 1)):
        orientation = "Plan"

        left_offset = active_view_crop_box.Min.X - selection_bounding_box_min.X
        right_offset = active_view_crop_box.Max.X - selection_bounding_box_max.X
        top_offset = active_view_crop_box.Max.Y - selection_bounding_box_max.Y
        bottom_offset = active_view_crop_box.Min.Y - selection_bounding_box_min.Y
        # print(left_offset, right_offset, top_offset, bottom_offset)

        """update new bounding box Min and Max values"""
        new_bbox.Min = XYZ(active_view_crop_box.Min.X - left_offset, active_view_crop_box.Min.Y - bottom_offset,
                           active_view_crop_box.Min.Z)
        new_bbox.Max = XYZ(active_view_crop_box.Max.X - right_offset, active_view_crop_box.Max.Y - top_offset,
                           active_view_crop_box.Max.Z)
        t.Start()
        active_view.CropBox = new_bbox
        turn_crop_on()
        t.Commit()

    # print("active view is {}".format(orientation))


def turn_crop_on():
    active_view.CropBoxActive = True
    active_view.CropBoxVisible = True


rectangular_selection(is_two_d_view=False)
