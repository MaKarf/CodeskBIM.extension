from SortNatural import real_sorting
from revit_app import doc
from Autodesk.Revit.DB import BuiltInParameter as Bip, FilteredElementCollector as Fec, BuiltInCategory as Bic


def get_ordered_sheets_as_dict():
    all_views = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()

    all_sheets_list = [{"name": "{} - {}".format(sheet.LookupParameter("Sheet Number").AsString(),
                                                 sheet.LookupParameter("Sheet Name").AsString()),
                        "element": sheet,
                        "number": sheet.LookupParameter("Sheet Number").AsString()}
                       for sheet in all_views]

    sorted_sheet_list = real_sorting(all_sheets_list, "number")

    return sorted_sheet_list
