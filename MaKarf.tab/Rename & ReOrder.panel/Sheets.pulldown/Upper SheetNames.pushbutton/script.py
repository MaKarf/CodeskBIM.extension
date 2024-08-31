# -*- coding: utf-8 -*-

def run():
    import operator
    from Autodesk.Revit.DB import Transaction
    from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic

    ui_doc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    t = Transaction(doc, "Renumber Sheets")

    t.Start()
    try:
        sheets_collection = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()
        for x in sheets_collection:
            x.LookupParameter("Sheet Name").Set(x.Name.upper())
            # print(x.Name)
        t.Commit()
    except Exception:
        t.Commit()


run()
