import os.path

import clr
import xlrd

from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from lib.files_path import files_path
from lib.loadfamilies import load_family
from lib.titleBlocks import create_sheets, organize_sheets, get_title_blocks

clr.AddReference("System.Windows")
from System.Windows.Controls import SelectionChangedEventHandler
from System.Windows import RoutedEventHandler

from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Create sheets from Excel")


class CreateSheets(BaseWPFClass):

    def __init__(self):
        BaseWPFClass.__init__(self, xaml_file_name="CreateSheets.xaml")

        """########################################################################################################"""
        tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().FirstElement()
        if tbs is None:
            load_family(os.path.join(files_path.annotation_families, "CodeskBIM_Free Advanced_A3 Title Block.rfa"),
                        transact=True)
            """No title block type found in the project"""
            tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().FirstElement()

        self.title_block_id = tbs.GetTypeId()
        self.worksheet = None
        self.sheets = None
        self.title_block_compatibility = True
        self.ttb_types_dicts = []
        self.selected_title_block = None

        self.ui_ttb_list_data = None
        self.ui_sheet_list_data = None

        self._sheet_dict = []
        """instantiate a workbook"""
        self.my_book = xlrd.open_workbook(files_path.excel_file)

        """prep_ui_data"""
        self.ui_sheet_list_data = self.my_book.sheet_names()

        tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()
        self.ui_ttb_list_data = [{"name": tb.LookupParameter("Family Name").AsString(), "element": tb} for tb in tbs]
        """########################################################################################################"""

        """Find the "button_run" button by its name"""
        self.excel_sheet_name = self.Window.FindName("excel_sheet_name")
        self.title_block = self.Window.FindName("title_block")
        create_button = self.Window.FindName("create_button")

        """update selection boxes with appropriate data source"""
        self.excel_sheet_name.ItemsSource = self.ui_sheet_list_data
        self.excel_sheet_name.SelectedIndex = 0
        self.worksheet = self.excel_sheet_name.SelectedItem

        self.title_block.SelectedIndex = 0
        self.selected_title_block = self.title_block.SelectedItem
        self.title_block.ItemsSource = [i.get("name") for i in get_title_blocks()]

        """Attach the event handler to the button's "Click" event"""
        self.excel_sheet_name.SelectionChanged += SelectionChangedEventHandler(self.select_sheet_type)
        self.title_block.SelectionChanged += SelectionChangedEventHandler(self.select_title_block)
        create_button.Click += RoutedEventHandler(self.button_run)

        self.ShowDialog()

    def read_sheets(self):
        """ set selected worksheet for further processing"""
        my_sheet = self.my_book.sheet_by_name(self.worksheet)

        sheet_numbers = ["{}".format(num) for num in my_sheet.col_values(0)]
        sheet_names = my_sheet.col_values(1)

        """remove decimal points from name"""
        for num in sheet_numbers:
            if num[-2:] == ".0":
                # print(num)

                """remove decimal points from name"""
                if len(num) == 3:
                    sheet_numbers[sheet_numbers.index(num)] = num.replace(num, "00{}".format(num.replace(".0", "")))
                else:

                    sheet_numbers[sheet_numbers.index(num)] = num.replace(num, "0{}".format(num.replace(".0", "")))

            else:
                """cater for cover page numbers with a mix of letters and numbers"""
                if len(num) == 2 and num[0] == "0":
                    sheet_numbers[sheet_numbers.index(num)] = num

                elif len(num) == 2 and num[0] != "0":
                    sheet_numbers[sheet_numbers.index(num)] = num.replace(num, "00{}".format(num))

                else:
                    sheet_numbers[sheet_numbers.index(num)] = num.replace(num, "0{}".format(num))

        self.sheets = [{"sheet_number": sheet_number, "sheet_name": sheet_name} for sheet_number, sheet_name in
                       zip(sheet_numbers, sheet_names)]
        self.sheets.pop(0)

        return self.sheets

    def button_run(self, sender, e):
        self.close_window()

        self.selected_title_block = [i.get("element") for i in self.ui_ttb_list_data if
                                     i.get("name") == self.title_block.SelectedItem].pop().Family

        self.read_sheets()

        if self.exited_with_close_button:
            pass
        else:
            if len(self.sheets) != 0:
                create_sheets(sheets=self.sheets, selected_title_block_family=self.selected_title_block)
                organize_sheets(self.selected_title_block)

    def select_title_block(self, sender, e):
        self.selected_title_block = self.title_block.SelectedItem

    def select_sheet_type(self, sender, e):
        self.worksheet = self.excel_sheet_name.SelectedItem
