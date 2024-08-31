import os

from lib.UI.xamlFiles.RenumberSheetsUI import RenumberSheetsUI

from Autodesk.Revit.DB import Transaction, ViewSheet, FilteredElementCollector as fec, BuiltInCategory as bic

from lib.SortNatural import real_sorting

from lib.UI.xamlFiles.RenumberSheetsPrefix import RenumberSheetsPrefix
from lib.sheets import get_ordered_sheets_as_dict

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Renumber Sheets")

active_view_id = doc.ActiveView.Id
active_view = doc.GetElement(active_view_id)
active_view_level = active_view.GenLevel
PATH_SCRIPT = os.path.dirname(__file__)

"""##############################################################################################################"""
"""####################################    A P P L I C A T I O N      ###########################################"""
"""##############################################################################################################"""


class RenumberSheets:
    sheets_collection = []

    def __init__(self):
        self.select_sheets()

    def select_sheets(self):
        """get collection of sheets selected on the UI forms"""
        pre_selection = ui_doc.Selection.GetElementIds()

        pre_selected_sheets = [doc.GetElement(sheet_id) for sheet_id in pre_selection if
                               type(doc.GetElement(sheet_id)) == ViewSheet]

        """pop up the sheets selection dialog box if no sheets was selected on the project browser before
        pressing the renumber button"""

        if len(pre_selected_sheets) == 0:
            alpha_dicts = {}
            numeric_dicts = {}

            sorted_sheet_list = get_ordered_sheets_as_dict()

            """##################################################################################################"""
            """##################################################################################################"""
            ui_selection = RenumberSheetsUI(sorted_sheet_list)

            sheets_to_rename = ui_selection.selected_items
            prefix = ui_selection.prefix
            try:
                start = int(ui_selection.start_number)
            except:
                start = 1

            if len(sheets_to_rename) != 0:
                self.renumber_sheets(sheets_to_rename, start, prefix)
            else:
                # print "nothing selected or canceled"
                pass

        else:
            ui = RenumberSheetsPrefix()
            start = ui.start
            prefix = ui.prefix
            self.renumber_sheets(pre_selected_sheets, start, prefix)

    @staticmethod
    def renumber_sheets(sheets_collection, start, prefix, checkbox=False):
        cover_page_name = ".COVER"
        dicts_sheets_unsorted = [
            {"sheet_elem": elem, "sheet_name": name.Name,
             "sheet_number": number.LookupParameter("Sheet Number").AsString()}
            for elem, name, number in zip(sheets_collection, sheets_collection, sheets_collection)]

        """sort by number"""
        dicts_sheets = real_sorting(dicts_sheets_unsorted, "sheet_number")

        """prep to set temporal value to avoid error that says SHEET NUMBER ALREADY EXIST"""
        for sheet in dicts_sheets:
            mk = sheet.get("sheet_elem").LookupParameter("Sheet Number").AsString()

            if cover_page_name in mk.upper():
                # print(mk)
                temp_name = str("0.00{} {}".format(dicts_sheets.index(sheet), cover_page_name))
                # print(mk, temp_name)
                sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(temp_name)
            else:
                temp_name = str("0.00{}".format(dicts_sheets.index(sheet)))
                # print(mk, temp_name)
                sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(temp_name)

        """reset the count for the final iteration"""
        start_number = int(start)
        alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                     "U", "V", "W", "X", "Y", "Z", "A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.", "K.",
                     "L.", "M.", "N.", "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."]

        for f_sheet in dicts_sheets:
            """#############################################################################################"""
            """ decide whether renaming is alphabetical or numerical"""
            if checkbox:
                final_number = str(prefix) + str(alphabets[dicts_sheets.index(f_sheet)])
                f_sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(final_number)

            else:
                temp_sheet_name = f_sheet.get("sheet_elem").LookupParameter("Sheet Number").AsString()

                if start_number < 10 and prefix == "0":
                    """ add additional zero to the beginning of the sheet numbers below 10"""
                    if cover_page_name in temp_sheet_name.upper():
                        final_number = str(prefix) + str(prefix) + str(start_number - 1) + cover_page_name
                        start_number -= 1
                    else:
                        final_number = str(prefix) + str(prefix) + str(start_number)
                    # print("if: {}".format(final_number))

                elif start_number > 9 and prefix == "0":
                    """ use only one zero to the beginning of the sheet numbers above 10"""
                    if "cover" in temp_sheet_name.lower():
                        final_number = str(prefix) + str(start_number - 1) + cover_page_name
                        start_number -= 1
                    else:
                        final_number = str(prefix) + str(start_number)
                    # print("elif: {}".format(final_number))
                else:
                    """ set sheet number using user defined prefix"""
                    if "cover" in temp_sheet_name.lower():
                        final_number = str(prefix) + str(start_number - 1) + cover_page_name
                        start_number -= 1
                    else:
                        final_number = str(prefix) + str(start_number)
                    # print("else: {}".format(final_number))

                f_sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(final_number)
                start_number += 1


"""##############################################################################################################"""

"""##############################################################################################################"""


def run():
    t.Start()
    RenumberSheets()
    t.Commit()


run()
