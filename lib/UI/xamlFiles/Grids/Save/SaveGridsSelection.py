from Autodesk.Revit.DB import Color
from Autodesk.Revit.DB import Transaction
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

from lib.UI.xamlFiles.Grids.CommonImports import SelectionType
from lib.UI.xamlFiles.Grids.Selection import SelectGrids

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Save Selected Grids")

active_view = ui_doc.ActiveView


class SaveGridsUIClass(BaseWPFClass):
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    dialog_bg_color = Color(33, 40, 50)
    selection_bg_color = Color(247, 191, 158)

    vertical_grids = []
    horizontal_grids = []

    vertical_sub_grids = []
    horizontal_sub_grids = []

    grids_collection = []
    grids_subs_collection = []

    def __init__(self, project_data_class=None):
        BaseWPFClass.__init__(self, xaml_file_name=r"Grids\Save\SaveGridsSelection.xaml")

        self.pd = project_data_class(doc.Title)

        self.path = self.pd.path

        """######################################################################################################"""

        self.selected_grids = SelectGrids(
            selection_type=SelectionType.select_from_ui).merged_vertical_and_horizontal_grids
        # print self.selected_grids
        """######################################################################################################"""

        self.ShowDialog()

    def button_click_run(self, sender, e):
        """update json"""
        if self.ui_option_name.Text == "":
            self.ui_hint.Text = "Option Name required"
        else:
            self.Close()
            self.pd.save_grid_selection(self.ui_option_name.Text, self.selected_grids)

    def check_name(self, sender, e):
        option_name = self.ui_option_name.Text
        if option_name == "":
            self.ui_hint.Text = "Option Name required"
        elif option_name.lower() in self.pd.current_options_checker_list:
            self.ui_hint.Text = "Name already exist, proceed to override it"
        else:
            self.ui_hint.Text = ""

    def ui_button_run(self, sender, e):
        if self.operation_type == "Delete":
            self.delete_view_template()
        else:
            self.transfer_view_templates()
