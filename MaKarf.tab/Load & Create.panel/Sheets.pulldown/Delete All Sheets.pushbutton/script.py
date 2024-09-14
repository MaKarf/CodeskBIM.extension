from Autodesk.Revit.DB import BuiltInCategory as Bic, ViewType, FilteredElementCollector as Fec, Transaction

from UI.Popup import Alert

from lib import ListToStringConvert
from lib.getView import set3DView

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Deleted all sheets")
active_view = ui_doc.ActiveView

sheets = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElementIds()

if active_view.ViewType == ViewType.DrawingSheet or len(ui_doc.GetOpenUIViews()) == 1:
    set3DView()


t.Start()
doc.Delete(sheets)
t.Commit()

"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
# failed_sheets = []
# t.Start()
# for sheet_id in sheets:
#     sheet_element = doc.GetElement(sheet_id)
#     try:
#         doc.Delete(sheet_id)
#     except:
#         failed_sheets.append("{} - {} [id = {}]".format(sheet_element.SheetNumber, sheet_element.Name, sheet_id.IntegerValue))
# t.Commit()
#
# data = ListToStringConvert.to_vertical_string(failed_sheets)
#
# Alert(title="Failed Sheets", header="Failed to delete Sheet:", content=data)
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
"""++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
