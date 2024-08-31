import operator
import sys

from Autodesk.Revit import DB

from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.UI import TaskDialog

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Revit Transaction")
active_view = ui_doc.ActiveView


class RenameGrids:
    def __init__(self):
        self.grids_collection = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().ToElements()
        self.grids_collection_list = []
        self.vertical_grids = []
        self.horizontal_grids = []

        self.get_ordered_grids()

        self.rename_grids()

    def get_ordered_grids(self):
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

                self.grids_collection_list.append(
                    {"elem": grid, "name": grid.Name, "orientation": orientation, "origin": origin})

            except AttributeError:
                td = TaskDialog("View Error")
                td.MainInstruction = "View Error - Resolve as follows:"
                td.MainContent = "Switch to a plan view and ensure all Grids are visible\n" \
                                 "\n" \
                                 "You may click on 'Reveal Hidden Element to display all hidden grids'"

                td.TitleAutoPrefix = False
                td.Show()
                """exit code when TaskDialog is closed"""
                sys.exit(1)

        """#########################################################################################################"""
        """#########################################################################################################"""

        for g in self.grids_collection_list:
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

    def temporal_rename_h_grid(self, reverse=True):
        self.horizontal_grids = sorted(self.horizontal_grids, key=operator.itemgetter("origin"),
                                       reverse=reverse)
        """####################################################################################################"""
        """####################################################################################################"""
        """prep to set temporal value to avoid error that says same already exist"""
        for h_grid in self.horizontal_grids:
            h_grid.get("elem").LookupParameter("Name").AsString()

            temp_name = str("0.00{}H".format(self.horizontal_grids.index(h_grid)))

            h_grid.get("elem").LookupParameter("Name").Set(temp_name)

    def temporal_rename_v_grid(self, reverse=False):
        self.vertical_grids = sorted(self.vertical_grids, key=operator.itemgetter("origin"),
                                     reverse=reverse)
        """####################################################################################################"""
        """####################################################################################################"""
        """prep to set temporal value to avoid error that says same already exist"""
        for v_grid in self.vertical_grids:
            v_grid.get("elem").LookupParameter("Name").AsString()

            temp_name = str("0.00{}V".format(self.vertical_grids.index(v_grid)))

            v_grid.get("elem").LookupParameter("Name").Set(temp_name)

        """####################################################################################################"""
        """####################################################################################################"""

    def final_rename_h_grid(self, prefix=""):
        """####################################################################################################"""
        """####################################################################################################"""
        """ set final name for the grid heads"""
        for h_grid_f in self.horizontal_grids:
            new_h_name = "{}{}".format(prefix, str(self.horizontal_grids.index(h_grid_f) + 1))
            h_grid_f.get("elem").LookupParameter("Name").Set(new_h_name)
        """####################################################################################################"""
        """####################################################################################################"""

    def final_rename_v_grid(self, prefix=""):
        """ set final name for the grid heads"""
        grid_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                        "S",
                        "T",
                        "U", "V", "W", "X", "Y", "Z", "A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.",
                        "K.",
                        "L.", "M.", "N.", "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."]
        for v_grid_f in self.vertical_grids:
            new_v_name = "{}{}".format(prefix, grid_letters[self.vertical_grids.index(v_grid_f)])
            v_grid_f.get("elem").LookupParameter("Name").Set(new_v_name)
        """####################################################################################################"""
        """####################################################################################################"""

    def rename_grids(self):
        t.Start()
        self.temporal_rename_h_grid()
        self.temporal_rename_v_grid()

        self.final_rename_h_grid()
        self.final_rename_v_grid()
        t.Commit()

    def reverse_h_grids(self, prefix=""):
        t.Start()
        self.temporal_rename_h_grid(reverse=False)
        self.final_rename_h_grid(prefix)
        t.Commit()

    def inverse_h_grids(self, prefix=""):
        t.Start()
        self.temporal_rename_h_grid(reverse=True)
        self.final_rename_h_grid(prefix)
        t.Commit()

    def reverse_v_grids(self, prefix=""):
        t.Start()
        self.temporal_rename_v_grid(reverse=True)
        self.final_rename_v_grid(prefix)
        t.Commit()

    def inverse_v_grids(self, prefix=""):
        t.Start()
        self.temporal_rename_v_grid(reverse=False)
        self.final_rename_v_grid(prefix)
        t.Commit()

    def swap_grid_names(self):
        t.Start()
        x = self.horizontal_grids
        y = self.vertical_grids
        self.horizontal_grids = y
        self.vertical_grids = x
        self.temporal_rename_h_grid()
        self.temporal_rename_v_grid()

        self.final_rename_h_grid()
        self.final_rename_v_grid()
        t.Commit()
        pass

    def reverse_swap_names(self):
        t.Start()
        x = self.horizontal_grids
        y = self.vertical_grids
        self.horizontal_grids = y
        self.vertical_grids = x

        self.temporal_rename_h_grid()
        self.temporal_rename_v_grid()

        self.final_rename_h_grid()
        self.final_rename_v_grid()
        t.Commit()
        pass


def get_view_by_name():
    para_name = DB.ParameterValueProvider(DB.ElementId(DB.BuiltInParameter.VIEW_NAME))
    filter_test = DB.FilterStringEquals()
    search = "Site"
    case_sensitive = True
    filter_rule = DB.FilterStringRule(para_name, filter_test, search, case_sensitive)

    param_filter = DB.ElementParameterFilter(filter_rule)

    vv = Fec(doc). \
        OfCategory(Bic.OST_Views). \
        WhereElementIsNotElementType(). \
        WherePasses(param_filter). \
        ToElements()
    return vv[0]
