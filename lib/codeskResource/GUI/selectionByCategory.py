import sys

from codeskResource.ui_selection import selection_from_ui

from Autodesk.Revit.DB import Color
from Autodesk.Revit.Exceptions import OperationCanceledException
from rpw.ui.forms import Alert

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document

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
            """grids category = -2000220"""
            grids_collection = selection_from_ui(ui_doc, doc, -2000220)
            # self.get_ordered_grids()
            app.BackgroundColor = bg_color

            return [int(i.Id.IntegerValue) for i in grids_collection]

        except OperationCanceledException as user_interrupt:
            app.BackgroundColor = bg_color

            Alert("", header="No Grid was selected")
            sys.exit()
