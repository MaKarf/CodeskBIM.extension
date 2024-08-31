# import clr
#
# clr.AddReference('RevitAPI')
# from Autodesk.Revit.DB import *
#
# clr.AddReference('RevitAPIUI')
# from Autodesk.Revit.UI import *
#
# clr.AddReference('System')
#
# doc = __revit__.ActiveUIDocument.Document
# cur_view = doc.ActiveView
# # Start transaction
# t = Transaction(doc, 'Tag Elements')
#
#
# class TagAllDoors:
#     views_list = []
#
#     def __init__(self):
#         t.Start()
#         map(self.doors, self.views_list)
#         """#########################################################################################################"""
#         """#########################################################################################################"""
#         # Commit transaction
#         t.Commit()
#
#     def doors(self, revit_view):
#         """#########################################################################################################"""
#         """#########################################################################################################"""
#
#         views_collection = FilteredElementCollector(doc) \
#             .OfCategory(BuiltInCategory.OST_Views) \
#             .WhereElementIsNotElementType() \
#             .ToElements()
#
#         """extract only elevation views and discard elevation view templates"""
#         for vi in views_collection:
#             if not vi.IsTemplate:
#                 if vi.ViewType == ViewType.FloorPlan or ViewType.Elevation or ViewType.Section:
#                     # print(vi.Name)
#                     self.views_list.append(vi)
#                     # elevations_list.append(el)
#
#         """########################################################################################################"""
#         """########################################################################################################"""
#         # Get all elements in the view
#         untagged = FilteredElementCollector(doc, cur_view.Id) \
#             .WhereElementIsNotElementType() \
#             .WhereElementIsViewIndependent() \
#             .ToElements()
#
#         """Tag elements"""
#         for i in untagged:
#             if not i.IsHidden(revit_view):
#                 if i.Category and i.Category.Name in ['Doors', 'Windows']:
#                     try:
#                         IndependentTag.Create(doc, revit_view.Id, Reference(i), True, TagMode.TM_ADDBY_CATEGORY,
#                                               TagOrientation.Horizontal, XYZ(0, 0, 0))
#                     except:
#                         pass
#
#
# TagAllDoors()
