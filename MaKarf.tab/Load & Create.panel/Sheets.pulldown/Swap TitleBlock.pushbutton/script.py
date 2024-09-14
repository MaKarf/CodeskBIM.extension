from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec

from UI.Popup import Alert
from UI.xamlFiles.DropDownSelection import DropDownSelection
from titleBlocks import get_title_blocks, organize_sheets

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


def swap_sheets():
    tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()
    if len(tbs) == 0:
        Alert(title="No Title Block Found", header="No Title Block Found",
              content="Cannot proceed without a title block in the project")
    else:
        window = DropDownSelection(title="Select Title Block",
                                   label_name="Select Title Block",
                                   dropdown_list=get_title_blocks())
        selected_title_block_family = window.selected_item.Value

        if not window.exited_with_close_button:
            organize_sheets(selected_title_block_family)


def run():
    swap_sheets()


run()
