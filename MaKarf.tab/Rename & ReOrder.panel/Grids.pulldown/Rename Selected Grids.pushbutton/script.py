import operator
import sys
from Autodesk.Revit import DB
from Autodesk.Revit.DB import Color
from Autodesk.Revit.DB import Transaction, FilteredElementCollector as Fec
from Autodesk.Revit.Exceptions import OperationCanceledException
from Autodesk.Revit.UI import TaskDialog

from lib.UI.Popup import Alert
from lib.UI.xamlFiles.RenameGrids import RenameGrids
from lib.selection.ui_selection import rectangular_selection_by_category

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Rename Grids")
active_view = ui_doc.ActiveView


class GetGrids:
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    dialog_bg_color = Color(33, 40, 50)
    selection_bg_color = Color(247, 191, 158)

    vertical_grids = []
    horizontal_grids = []

    vertical_sub_grids = []
    horizontal_sub_grids = []

    grids_collection = []
    grids_subs_collection = []

    def __init__(self):
        """#########################################################################################################"""
        """#########################################################################################################"""

        """select grids"""
        self.select_grids_to_rename()

        """selects list of grids to rename"""
        self.select_subs_grids_to_rename()

        """ prep and reorder selected grids"""
        self.get_ordered_grids()

    def select_grids_to_rename(self):
        # app.BackgroundColor = self.dialog_bg_color
        # Alert("", header="Select Grids to Rename")
        try:
            app.BackgroundColor = self.selection_bg_color
            """grids category = -2000220"""
            self.grids_collection = rectangular_selection_by_category(DB.BuiltInCategory.OST_Grids)
            # self.get_ordered_grids()
            app.BackgroundColor = self.bg_color
        except OperationCanceledException as user_interrupt:
            app.BackgroundColor = self.bg_color

            Alert("", header="No Grid was selected")
            sys.exit()
            pass

    def select_subs_grids_to_rename(self):
        app.BackgroundColor = self.dialog_bg_color
        # Alert("", header="Select sub Grids")
        try:
            app.BackgroundColor = self.dialog_bg_color
            self.grids_subs_collection = [i.Id for i in rectangular_selection_by_category(DB.BuiltInCategory.OST_Grids)]
            app.BackgroundColor = self.bg_color
        except OperationCanceledException as user_interrupt:
            app.BackgroundColor = self.bg_color
            pass

        """#########################################################################################################"""
        """#########################################################################################################"""

    def get_ordered_grids(self):
        grids_collection_list = []
        for grid in self.grids_collection:
            """get viewports placed on sheet"""

            try:
                b_box = grid.get_BoundingBox(active_view)
                grid_length = b_box.Max.X - b_box.Min.X
                grid_height = b_box.Max.Y - b_box.Min.Y

                if grid_length > grid_height:
                    orientation = "horizontal"
                    origin = b_box.Max.Y - (grid_height / 2)
                else:
                    orientation = "vertical"
                    origin = b_box.Max.X - (grid_length / 2)

                if grid.Id in self.grids_subs_collection:
                    # print("{} found in sub list".format(grid))
                    grids_collection_list.append(
                        {"elem": grid, "name": grid.Name, "orientation": orientation, "origin": origin, "sub": True})
                else:
                    grids_collection_list.append(
                        {"elem": grid, "name": grid.Name, "orientation": orientation, "origin": origin, "sub": False})
                    # print("{} NOT SUB".format(grid))

            except AttributeError:
                td = TaskDialog("View Error")
                td.MainInstruction = "View Error - Resolve as follows:"
                td.MainContent = "Switch to a plan view and ensure Grids are visible"

                td.TitleAutoPrefix = False
                td.Show()
                """exit code when TaskDialog is closed"""
                sys.exit(1)

        """#########################################################################################################"""
        """#########################################################################################################"""
        """reset values"""
        self.vertical_grids = []
        self.horizontal_grids = []

        for g in grids_collection_list:
            if g.get("orientation") == "horizontal":
                self.horizontal_grids.append(g)
            else:
                self.vertical_grids.append(g)

        self.vertical_grids = sorted(self.vertical_grids, key=operator.itemgetter("origin"), reverse=False)
        self.horizontal_grids = sorted(self.horizontal_grids, key=operator.itemgetter("origin"), reverse=True)

        """#########################################################################################################"""
        """#########################################   R   E   P   O   R   T   #####################################"""
        """#########################################################################################################"""

        """#########################################################################################################"""
        """#########################################   R   E   P   O   R   T   #####################################"""
        """#########################################################################################################"""
        return [self.horizontal_grids, self.vertical_grids]


if Fec(doc).OfCategory(DB.BuiltInCategory.OST_Grids).WhereElementIsNotElementType().FirstElement() is not None:
    grids = GetGrids().get_ordered_grids()

    RenameGrids(parsed_grids_collection=grids, include_hidden_grids=False, hide_hidden_grids_checkbox=True)

else:
    Alert(title="No Grids Found", header="No Grids Found", content="Place grids and retry")
