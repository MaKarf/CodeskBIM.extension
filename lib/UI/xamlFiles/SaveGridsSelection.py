from Autodesk.Revit import DB
from Autodesk.Revit.DB import Color
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.Exceptions import OperationCanceledException

from UI.Popup import Alert
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from selection.ui_selection import rectangular_selection_by_category

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Save Selected Grids")

active_view = ui_doc.ActiveView


class SelectElement:
    def __init__(self, db_element_type):
        self.db_element_type = db_element_type

    def select(self):
        """######################################################################################################"""
        ui_selected = ui_doc.Selection.GetElementIds()
        grids = [int(grid_id.IntegerValue) for grid_id in ui_selected if
                 type(doc.GetElement(grid_id)) == self.db_element_type]
        """pop up the grid selection dialog box if no grid was selected on the screen before the button press"""
        if len(grids) == 0:
            return self.select_grids()
        else:
            return grids

    @staticmethod
    def select_grids():
        bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
        selection_bg_color = Color(247, 191, 158)
        try:
            app.BackgroundColor = selection_bg_color

            grids_collection = rectangular_selection_by_category(DB.BuiltInCategory.OST_Grids)
            # self.get_ordered_grids()
            app.BackgroundColor = bg_color

            return [int(i.Id.IntegerValue) for i in grids_collection]

        except OperationCanceledException as user_interrupt:
            app.BackgroundColor = bg_color

            Alert("", header="No Grid was selected")


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
        BaseWPFClass.__init__(self, xaml_file_name="SaveGridsSelection.xaml")

        self.pd = project_data_class(doc.Title)

        self.path = self.pd.path

        """######################################################################################################"""
        self.selected_grids = SelectElement(DB.Grid).select()
        """######################################################################################################"""

        self.ShowDialog()

    def button_click_run(self, sender, e):
        """update json"""
        if self.ui_option_name.Text == "":
            self.ui_hint.Text = "Option Name required"
        else:
            self.Close()
            self.pd.save_grid_selection(self.selected_grids, self.ui_option_name.Text,
                                        is_sub=self.ui_is_sub_grid.IsChecked)


def ui_button_run(self, sender, e):
    if self.operation_type == "Delete":
        self.delete_view_template()
    else:
        self.transfer_view_templates()
