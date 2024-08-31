import clr
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic, ViewType
from Autodesk.Revit.DB import Line, Transaction, XYZ, FillPatternElement, FilledRegion, FilledRegionType, \
    CurveLoop

from lib.AppMethods import Alert
from lib.ElementVisibility import is_visible_in_view

clr.AddReference("System")
from System.Collections.Generic import List

"""Get the active document"""
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc, "Create Filled Region on Column")

"""Get all structural columns in the model"""
columns = Fec(doc).OfCategory(Bic.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()


def create_lines(plan_view):
    curve_loop_list = List[CurveLoop]()

    """Loop through each column and create lines from their boundaries"""
    for column in columns:

        if not column.IsHidden(plan_view):  # if column not permanently hidden

            if is_visible_in_view(column, plan_view):  # if column is visible in view
                """Get the geometry of the column"""
                if column.HasSweptProfile:
                    sp = column.GetSweptProfile().GetSweptProfile().Curves

                    """get the bounding box of the column"""
                    bb = column.get_BoundingBox(plan_view)

                    points = [
                        XYZ(bb.Min.X, bb.Min.Y, 0),
                        XYZ(bb.Max.X, bb.Min.Y, 0),
                        XYZ(bb.Max.X, bb.Max.Y, 0),
                        XYZ(bb.Min.X, bb.Max.Y, 0)
                    ]

                    curve_loop = CurveLoop()
                    for i in range(len(points)):
                        start_point = points[i]

                        """Connect the last point to the first point to form a closed loop"""
                        end_point = points[(i + 1) % len(points)]

                        line = Line.CreateBound(start_point, end_point)
                        curve_loop.Append(line)

                    curve_loop_list.Add(curve_loop)
                else:
                    Alert(header="Cannot create outlines from this column")
    return curve_loop_list


def get_solid_fill_pattern():
    """Function to create a solid fill pattern"""

    """Check if the solid fill pattern already exists"""
    patterns = Fec(doc).OfClass(FillPatternElement).ToElements()

    try:
        solid_fill_pattern = [i for i in patterns if i.Name == "<Solid fill>"].pop()
        return solid_fill_pattern
    except IndexError:

        """If not, create a new solid fill pattern"""
        with Transaction(doc, "Create Solid Fill Pattern") as transaction:
            transaction.Start()

            solid_fill_pattern = FillPatternElement.Create(doc, FillPatternElement.SOLID_FILL_REGIONAL)
            transaction.Commit()

        return solid_fill_pattern


def create_filled_region(plan_view):
    t.Start()
    """Function to create a filled region with solid fill pattern"""
    """Get a solid fill pattern"""
    solid_fill_pattern_id = get_solid_fill_pattern()

    """Get a filled region type"""
    filled_region_type = Fec(doc).OfClass(FilledRegionType).ToElements()

    def select_filled_region():
        for f in filled_region_type:
            filled_region_type_name = f.LookupParameter("Type Name").AsString()
            pattern = get_solid_fill_pattern()
            # print pattern

            if doc.GetElement(f.ForegroundPatternId).Name == pattern.Name:
                # print filled_region_type_name
                return f

    filled_region_type = select_filled_region()

    if filled_region_type is None:
        """If not, create a new filled region type"""
        with Transaction(doc, "Create Filled Region Type") as transaction:
            transaction.Start()

            filled_region_type = FilledRegionType.Create(doc, "Solid Fill Type", solid_fill_pattern_id)

            transaction.Commit()

    """Create a new filled region"""
    curve_loop = create_lines(plan_view)
    if len(curve_loop) > 0:

        try:
            filled_region = FilledRegion.Create(doc, filled_region_type.Id, plan_view.Id, curve_loop)
            filled_region.LookupParameter("Comments").Set("Filled Region on Column")
            t.Commit()
        except Exception:
            Alert(title="Filed Region Creation Error", header="Column Intersection Error",
                  content="Some Columns may be intersecting others. Please rectify and retry")

            t.RollBack()
            return None
    else:
        Alert(title="", header="No Structural Column\nplaced",
              content="")
        t.RollBack()


def delete_filled_regions():
    """get filled regions"""
    fr = Fec(doc).OfCategory(Bic.OST_DetailComponents).WhereElementIsNotElementType().ToElements()

    t.Start()
    [doc.Delete(i.Id) for i in fr if i.LookupParameter("Comments").AsString() == "Filled Region on Column"]
    t.Commit()


views = Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
selected_views = [view for view in views if view.ViewType == ViewType.FloorPlan and not view.IsTemplate]

map(create_filled_region, selected_views)

# delete_filled_regions()
