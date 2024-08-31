from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction
from Autodesk.Revit.UI import UIApplication

from lib.UI.Popup import Alert
from lib.UI.xamlFiles.DoubleDropDownSelection import DoubleDropDownSelection
from lib.UI.xamlFiles.DropDownSelection import DropDownSelection
from lib.titleBlocks import get_title_blocks, create_sheets, organize_sheets

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
app = __revit__.Application
uiApp = UIApplication(app)

t = Transaction(doc, "Create sheets from Doc")


class SheetsFromDoc:

    def __init__(self):
        self.inactive_docs = [{"element": i, "name": i.Title} for i in app.Documents if
                              not i.IsFamilyDocument and
                              not i.IsLinked and
                              not i.ActiveView]

        self.sheets_from_selected_doc()

    def sheets_from_selected_doc(self):

        tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()

        """create a dictionary of 'name':'item name in list, 'object':'item object for post process'"""
        title_block_list = [{"name": tb.LookupParameter("Family Name").AsString(), "element": tb} for tb in tbs]

        selected_doc = None
        selected_title_block_family = None
        window = None

        if len(self.inactive_docs) == 0:
            Alert(title="Open project",
                  header="Only one Project is opened",
                  content="You need to open more than one project to perform this task")

        elif len(self.inactive_docs) == 1:
            selected_doc = self.inactive_docs.pop().get("element")
            try:
                window = DropDownSelection(title="Select Title Block",
                                           label_name="Select Title Block",
                                           dropdown_list=get_title_blocks())
                selected_title_block_family = window.selected_item
            except Exception as ex:
                print(ex)
                """"""

        elif len(self.inactive_docs) > 1:
            window = DoubleDropDownSelection(dropdown_list1=self.inactive_docs, dropdown_list2=title_block_list,
                                             label_name1="Select Project", label_name2="Title Block")
            selected_doc = window.selected_item1
            selected_title_block_family = window.selected_item2

        if window is not None and not window.exited_with_close_button:
            """ check if selected title block has parametric compatibility with the code"""
            if selected_title_block_family is not None:

                sheets = [{"sheet_name": sh.Name, "sheet_number": sh.SheetNumber, "title": sh.Title} for sh in
                          Fec(selected_doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()]

                if len(sheets) != 0:
                    create_sheets(sheets=sheets, selected_title_block_family=selected_title_block_family)
                    organize_sheets(selected_title_block_family)
