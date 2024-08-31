# -*- coding: utf-8 -*-


"""
=====================================================================================================================
╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝ IMPORTS
=====================================================================================================================
"""
import operator
from Autodesk.Revit.DB import Transaction, ViewSheet
from rpw.ui.forms import FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox

"""
=====================================================================================================================
╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
 ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝ VARIABLES
=====================================================================================================================
"""

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Renumber Sheets")

"""
=====================================================================================================================
╔═╗╦ ╦╔╗╔╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
╠╣ ║ ║║║║║   ║ ║║ ║║║║╚═╗
╚  ╚═╝╝╚╝╚═╝ ╩ ╩╚═╝╝╚╝╚═╝ FUNCTIONS
=====================================================================================================================
"""

"""##############################################################################################################"""
"""####################################    A P P L I C A T I O N      ###########################################"""
"""##############################################################################################################"""


class RenumberSheets(FlexForm):

    def __init__(self, title="Title", components=(Label('Prefix')), **kwargs):
        super().__init__(title="Title", components=(Label('Prefix')), **kwargs)


        self.show()
        print(self.values.get("start"), self.values.get("prefix"), self.values.get("checkbox"))
        # self.renumber_sheets(self.values.get("start"), self.values.get("prefix"), self.values.get("checkbox"))

    @staticmethod
    def renumber_sheets(start, prefix, checkbox):

        """get collection of sheets selected on the UI forms"""
        UI_selected = ui_doc.Selection.GetElementIds()

        sheets_collection = [doc.GetElement(sheet_id) for sheet_id in UI_selected if
                             type(doc.GetElement(sheet_id)) == ViewSheet]

        dicts_sheets = [
            {"sheet_elem": elem, "sheet_name": name.Name,
             "sheet_number": number.LookupParameter("Sheet Number").AsString()}
            for elem, name, number in zip(sheets_collection, sheets_collection, sheets_collection)]

        """sort by number"""
        dicts_sheets.sort(key=operator.itemgetter(*['sheet_number']))

        # for d in dicts_sheets:
        #     print(d.get("sheet_number"))

        """prep to set temporal value to avoid error that says same already exist"""
        for sheet in dicts_sheets:
            mk = sheet.get("sheet_elem").LookupParameter("Sheet Number").AsString()
            # print(mk)
            temp_name = str("0.00{}".format(dicts_sheets.index(sheet)))
            # print(mk, temp_name)
            sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(temp_name)

        """reset the count for the final iteration"""
        start_number = int(start)
        alphabets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                     "U", "V", "W", "X", "Y", "Z", "A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.", "K.",
                     "L.", "M.", "N.", "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."]
        for f_sheet in dicts_sheets:

            if checkbox:
                final_number = str(prefix) + str(alphabets[dicts_sheets.index(f_sheet)])
                f_sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(final_number)
                start_number += 1
            else:

                if start_number < 10 and prefix == "0":
                    final_number = str(prefix) + str(prefix) + str(start_number)
                    # print("if: {}".format(final_number))

                elif start_number > 9 and prefix == "0":
                    final_number = str(prefix) + str(start_number)
                    # print("elif: {}".format(final_number))
                else:
                    final_number = str(prefix) + str(start_number)
                    # print("else: {}".format(final_number))

                f_sheet.get("sheet_elem").LookupParameter("Sheet Number").Set(final_number)
                start_number += 1


"""
=====================================================================================================================
╔╦╗╔═╗╦╔╗╔
║║║╠═╣║║║║
╩ ╩╩ ╩╩╝╚╝ MAIN
=====================================================================================================================
"""

if __name__ == "__main__":
    t.Start()
    try:
        component = [
            Label('Prefix'),
            TextBox('prefix', Text="0"),
            Label('Start Number'),
            TextBox('start', Text="1"),
            # Separator(),
            CheckBox(name='checkbox', default=False, checkbox_text='Alphabetical'),
            # Separator(),
            Button(button_text='Renumber Sheets')]

        RenumberSheets(title='Reverse Grids', components=component)
        t.Commit()
    except Exception:
        t.Commit()
