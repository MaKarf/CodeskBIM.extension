from UI.xamlFiles.Grids.CommonImports import SelectionType
from UI.xamlFiles.Grids.Rename.RenameGrids import RenameGrids


mk = RenameGrids(SelectionType.select_from_db, include_hidden_grids=False)
# mk = RenameGrids(SelectionType.select_from_ui)
# mk = RenameGrids(SelectionType.select_from_options)

# from UI.xamlFiles.Grids.CommonImports import t, active_view
# from getView import EnableRevealHiddenElements
#
# t.Start()
# """reveal hidden elements before selecting grids from view to capture hidden ones as well"""
# EnableRevealHiddenElements(active_view)
#
# # DisableRevealHiddenElements(view2d)
# t.Commit()
# from lib.imports.document import Fec, doc, Bic, active_view
#
# a = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().ToElements()
# print len(a)
#
# b = [i for i in a if i.get_BoundingBox(active_view)]
# print len(b)
