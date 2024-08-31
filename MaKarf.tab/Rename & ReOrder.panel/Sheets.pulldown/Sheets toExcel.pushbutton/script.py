import clr

clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import SaveFileDialog

import operator
import os

from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic
import xlsxwriter
from lib.UI.Popup import Alert

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Export Sheets")


def export_to_excel():
    """Some data we want to write to the worksheet."""
    sheets_collection = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()

    dicts_sheets = [
        {"sheet_elem": elem,
         "sheet_name": name.Name,
         "sheet_number": number.LookupParameter("Sheet Number").AsString()
         }
        for elem, name, number in zip(sheets_collection, sheets_collection, sheets_collection)
    ]

    """sort by number"""
    dicts_sheets.sort(key=operator.itemgetter(*['sheet_number']))

    """ Create a workbook and add a worksheet """
    dialog = SaveFileDialog()
    dialog.FileName = "Revit Sheets Export"
    dialog.Filter = "Excel files (*.xlsx)|*.xlsx|All files (*.*)|*.*"
    dialog.CheckPathExists = True
    dialog.InitialDirectory = r"C:\\"
    dialog.DefaultExt = "xlsx"
    dialog.Title = "Save Sheet Export"
    dialog.RestoreDirectory = True

    res = dialog.ShowDialog()

    if str(res) == "OK":
        path = dialog.FileName

        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet()

        """Start from the first cell. Rows and columns are zero indexed."""
        row = 1
        col = 0

        """Write the headings to file"""
        worksheet.write(0, 0, 'SHEET NUMBER')
        worksheet.write(0, 1, 'SHEET NAME')

        """Iterate over the data and write it out row by row."""
        for sheet in dicts_sheets:
            worksheet.write(row, col, sheet.get("sheet_number"))
            worksheet.write(row, col + 1, sheet.get("sheet_name"))
            row += 1
        workbook.close()


t.Start()
try:
    export_to_excel()
    t.Commit()
    Alert(content="", title="Results", header="Sheets successfully exported to Excel")
except Exception:
    t.Commit()
