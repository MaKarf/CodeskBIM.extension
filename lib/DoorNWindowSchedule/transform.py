import clr
from Autodesk.Revit.DB import XYZ

clr.AddReference("System")
from System.Collections.Generic import List

from Autodesk.Revit import DB

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


def visualize_geometry_objects(geometry_obj):
    def visualize(geometry_object):

        geometry_objects = List[DB.GeometryObject]()

        if isinstance(geometry_object, DB.XYZ):
            point = DB.Point.Create(geometry_object)
            geometry_objects.Add(point)
        else:
            geometry_objects.Add(geometry_object)

        cat_id = DB.ElementId(DB.BuiltInCategory.OST_GenericModel)

        direct_shape = DB.DirectShape.CreateElement(document=doc, categoryId=cat_id)
        direct_shape.SetShape(geometry_objects)
        return direct_shape

    if isinstance(geometry_obj, list):
        return map(visualize, geometry_obj)
    else:
        return visualize(geometry_obj)


class ClockwisePointRotation:

    def __init__(self):
        pass

    @staticmethod
    def at90_on_x_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(xyz.X, -xyz.Z, xyz.Y)

    @staticmethod
    def at180_on_x_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(xyz.X, -xyz.Y, -xyz.Z)

    @staticmethod
    def at270_on_x_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(xyz.X, xyz.Z, -xyz.Y)

    """####################################################"""

    @staticmethod
    def at90_on_y_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(xyz.Z, xyz.Y, -xyz.X)

    @staticmethod
    def at180_on_y_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(-xyz.X, xyz.Y, -xyz.Z)

    @staticmethod
    def at270_on_y_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(-xyz.Z, xyz.Y, xyz.X)

    """########################################################"""

    @staticmethod
    def at90_on_z_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(xyz.Y, -xyz.X, xyz.Z)

    @staticmethod
    def at180_on_z_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(-xyz.X, -xyz.Y, xyz.Z)

    @staticmethod
    def at270_on_z_axis(xyz=XYZ(), rotation_point=XYZ.Zero):
        return XYZ(-xyz.Y, xyz.X, xyz.Z)


def line_through_points(list_of_points, detail_drawing_view):

    created_lines_checker = []
    created_lines = []

    for i in range(len(list_of_points) - 1):
        try:
            line = DB.Line.CreateBound(list_of_points[i], list_of_points[i + 1])

            start_point = XYZ(round(line.GetEndPoint(0).X, 5),
                              round(line.GetEndPoint(0).Y, 5),
                              round(line.GetEndPoint(0).Z, 5))

            end_point = XYZ(round(line.GetEndPoint(1).X, 5),
                            round(line.GetEndPoint(1).Y, 5),
                            round(line.GetEndPoint(1).Z, 5))

            line_checker = "POINT_ONE={} POINT_TWO={}".format(start_point, end_point)
            reverse_line_checker = "POINT_ONE={} POINT_TWO={}".format(end_point, start_point)

            """check if another line lies on same location"""
            if line_checker in created_lines_checker or reverse_line_checker in created_lines_checker:
                """"""
                # print "line already exist"
            else:
                detail_curve = doc.Create.NewDetailCurve(detail_drawing_view, line)
                created_lines.append(detail_curve)

                # print "CREATED LINE : {}".format(line_checker)
                created_lines_checker.append(line_checker)
                created_lines_checker.append(reverse_line_checker)

        except Exception as ex:
            # print "exception___________{}".format(ex.__str__())
            pass

    return created_lines
