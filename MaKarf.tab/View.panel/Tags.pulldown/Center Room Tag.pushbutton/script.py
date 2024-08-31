from Autodesk.Revit.DB import Transaction, XYZ
from Autodesk.Revit.DB import FilteredElementCollector, SpatialElementTag

from lib.getView import threeDView

doc = __revit__.ActiveUIDocument.Document


def center_room_tag():
    """###########################################################################"""
    """TAG COLLECTOR [IN VIEW BY: doc.ActiveView.Id]"""
    room_tags = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(SpatialElementTag).ToElements()
    """###########################################################################"""

    transaction = Transaction(doc, 'Center room and tag')
    transaction.Start()
    for room_tag in room_tags:
        room = room_tag.Room
        room_pt = room.Location.Point

        room_bbox = room.get_BoundingBox(threeDView)
        x_pos = room_bbox.Min.X + (room_bbox.Max.X - room_bbox.Min.X) / 2
        y_pos = room_bbox.Min.Y + (room_bbox.Max.Y - room_bbox.Min.Y) / 2
        z_pos = room_pt.Z
        room_center = XYZ(x_pos, y_pos, z_pos)

        room.Location.Point = room_center
        room_tag.Location.Point = room_center

    transaction.Commit()


center_room_tag()
