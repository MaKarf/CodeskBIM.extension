from Autodesk.Revit import DB
from Autodesk.Revit.DB import Transaction, XYZ, FilteredElementCollector
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Renumber Sheets")


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


# type_id = doc.GetDefaultElementTypeId(DB.ElementTypeGroup.ViewTypeSection)
doors = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsNotElementType().ToElements()


def vft():
    elem = Fec(doc).OfClass(DB.ViewFamilyType).ToElements()
    """rewrite this code for a faster results using WherePasses method"""
    for v in elem:
        # print(v)
        if v is not None and v.ViewFamily == DB.ViewFamily.Section:
            return v.Id


def create_section_line(list_of_door_or_window_elements):
    for i in list_of_door_or_window_elements:
        b = i.get_BoundingBox(None)

        # print("{}\n{}".format(ft2mm(b.Min), ft2mm(b.Max)))
        door_origin = i.GetTransform().Origin
        # print("origin: {}".format(ft2mm(door_origin)))

        start_point = i.Host.Location.Curve.GetEndPoint(0)
        end_point = i.Host.Location.Curve.GetEndPoint(1)

        if ft2mm(start_point[1]) == ft2mm(end_point[1]):
            door_left_end_point = XYZ(b.Min.X, b.Min.Y, 0)
            door_right_end_point = XYZ(b.Max.X, b.Min.Y, 0)
            door_width_coordinate = door_right_end_point - door_left_end_point

            door_width = b.Max.X - b.Min.X
            door_height = b.Max.Z - b.Min.Z
            door_thickness = b.Max.Y - b.Min.Y

            door_direction = door_width_coordinate.Normalize()
            z_direction = DB.XYZ.BasisZ
            view_direction = door_direction.CrossProduct(z_direction)

            # print("horizontal")
            # print("door left end point: {}".format(ft2mm(door_left_end_point)))
            # print("door right end point: {}".format(ft2mm(door_right_end_point)))
            # print("door widths: {}".format(ft2mm(door_width)))
            # print("door direction: {}".format(ft2mm(door_direction)))
            # print("view_direction: {}".format(ft2mm(view_direction)))

        else:
            door_left_end_point = XYZ(b.Min.X, b.Min.Y, 0)
            door_right_end_point = XYZ(b.Min.X, b.Max.Y, 0)
            door_width_coordinate = door_right_end_point - door_left_end_point

            door_width = b.Max.Y - b.Min.Y
            door_height = b.Max.Z - b.Min.Z
            door_thickness = b.Max.X - b.Min.X

            door_direction = door_width_coordinate.Normalize()
            z_direction = DB.XYZ.BasisZ
            view_direction = door_direction.CrossProduct(z_direction)

        #     print("vertical")
        #     print("door bottom end point: {}".format(ft2mm(door_left_end_point)))
        #     print("door top end point: {}".format(ft2mm(door_right_end_point)))
        #     print("door widths: {}".format(ft2mm(door_width)))
        #     print("door direction: {}".format(ft2mm(door_direction)))
        #     print("view_direction: {}".format(ft2mm(view_direction)))
        #     print("z_direction: {}".format(ft2mm(z_direction)))
        #
        # print("\n\n\n")

        tr = DB.Transform.Identity
        tr.Origin = door_origin
        tr.BasisX = door_direction
        tr.BasisY = z_direction
        tr.BasisZ = view_direction

        b_box = DB.BoundingBoxXYZ()
        b_box.Transform = tr

        """ offset value: half the door width + allowance of 100mm"""

        """ subtract the offset from the Min X-coordinate and add same to the Max X-coordinate"""
        """ the sides of the crop view spreads from the center of the door, and thats why half the door width is neede
        for the offset, then actual offset of 100mm for allowance"""
        """the top of the door doesnt need any offset because it comes with its own builtin offset"""

        """ offset of 100mm also to the base of the door because 
        the crop view is set exactly on the boundary by default"""

        b_box.Min = XYZ(-mm2ft(100) - (door_width * 0.5), -mm2ft(100), -mm2ft(300))
        b_box.Max = XYZ(door_width * 0.5 + mm2ft(100), door_height, door_thickness)
        type_id = vft()
        DB.ViewSection.CreateSection(doc, sectionViewFamilyTypeId, b_box)


t.Start()
sectionViewFamilyTypeId = vft()
create_section_line(doors)
t.Commit()
