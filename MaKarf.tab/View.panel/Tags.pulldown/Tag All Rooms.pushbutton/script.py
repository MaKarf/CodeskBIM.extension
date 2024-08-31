# """
# Selects unbound rooms in model
#
# TESTED REVIT API: 2015, 2016, 2017
#
# Author: Jared Friedman | github.com/jbf1212
#
# This file is shared on www.revitapidocs.com
# For more information visit http://github.com/gtalarico/revitapidocs
# License: http://github.com/gtalarico/revitapidocs/blob/master/LICENSE.md
# """
# from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementId
# from Autodesk.Revit.DB import Transaction, LinkElementId
# from Autodesk.Revit.DB import UV
# from System.Collections.Generic import List
#
#
# def run():
#     ui_doc = __revit__.ActiveUIDocument
#     doc = ui_doc.Document
#     t = Transaction(doc, "Revit Transaction")
#
#     # GET ALL ROOMS IN MODEL
#     rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)
#     viw = FilteredElementCollector(doc).OfCategory(
#         BuiltInCategory.OST_Views)  # .WhereElementIsNotElementType().ToElement()
#
#     view_ids = None
#     vv = List[ElementId]([v.Id for v in viw])
#     for x in viw:
#         if x.Name == "Level 00":
#             print(x.Name, x.Id)
#             view_ids = x.Id
#
#     ub_rooms = []
#
#     for r in rooms:
#         if r.Area > 0:
#             pass
#         else:
#             ub_rooms.append(r)
#
#     # SELECT UNBOUND ROOMS
#     collection = List[ElementId]([r.Id for r in ub_rooms])
#     # print(collection)
#     # selection = uidoc.Selection
#     # print(selection)
#     # selection.SetElementIds(collection)
#
#     i = LinkElementId(collection[0])
#
#     t.Start()
#     doc.Create.NewRoomTag(i, UV(0, 0), view_ids)
#     t.Commit()
#
# # TaskDialog.Show('Unbound Rooms', "{} unbound rooms selected". format(len(ub_rooms)))
#
#
# run()
