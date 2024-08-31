import clr

from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from lib.getView import get2DView, EnableRevealHiddenElements, DisableRevealHiddenElements

clr.AddReference("System.Windows")
from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler
from System.Windows import Visibility

import operator

from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic
from Autodesk.Revit.DB import Transaction, Color

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Rename Grids")
active_view = ui_doc.ActiveView

view2d = get2DView()


class RenameGridsUI(BaseWPFClass):

    def __init__(self, parser_class, include_hidden_grids=False, hide_hidden_grids_checkbox=False):
        BaseWPFClass.__init__(self, xaml_file_name="RenameGrids.xaml", )
        self.rename_class = parser_class

        self.hidden_grids_checkbox.IsChecked = include_hidden_grids

        if hide_hidden_grids_checkbox:
            self.hidden_grids_checkbox.Visibility = Visibility.Collapsed

        """Attach the event handler to the button's "Click" event"""
        self.UI_VGrid_check.Checked += RoutedEventHandler(self.reverse_vertical)
        self.UI_VGrid_check.Unchecked += RoutedEventHandler(self.inverse_vertical)
        self.prefix_vertical.Click += RoutedEventHandler(self.prefix_vertical_func)

        self.alphabetic_grid_prefix.KeyUp += KeyEventHandler(self.prefix_vertical_func)

        self.UI_HGrid_check.Checked += RoutedEventHandler(self.reverse_horizontal)
        self.UI_HGrid_check.Unchecked += RoutedEventHandler(self.inverse_horizontal)
        self.prefix_horizontal.Click += RoutedEventHandler(self.prefix_horizontal_func)
        self.numeric_grid_prefix.KeyUp += KeyEventHandler(self.prefix_horizontal_func)

        self.swap_grids.Checked += RoutedEventHandler(self.swap_grid_names)
        self.swap_grids.Unchecked += RoutedEventHandler(self.reverse_swap_names)

        self.save_grids_checkbox.Checked += RoutedEventHandler(self.expand_save_panel)
        self.save_grids_checkbox.Unchecked += RoutedEventHandler(self.collapse_save_panel)

        self.hidden_grids_checkbox.Checked += RoutedEventHandler(self.include_hidden_grids)
        self.hidden_grids_checkbox.Unchecked += RoutedEventHandler(self.exclude_hidden_grids)

        self.button_run.Click += RoutedEventHandler(self.rename)
        self.save_grid_panel.Visibility = Visibility.Collapsed
        self.ui_save_button.Click += RoutedEventHandler(self.save_grid)

        self.ShowDialog()

    def expand_save_panel(self, sender, e):
        self.save_grid_panel.Visibility = Visibility.Visible
        self.Window.Height = 240

    def collapse_save_panel(self, sender, e):
        self.save_grid_panel.Visibility = Visibility.Collapsed
        self.Window.Height = 200

    def reverse_horizontal(self, sender, e):
        self.rename_class.reverse_h_grids(self.numeric_grid_prefix.Text)

    def inverse_horizontal(self, sender, e):
        self.rename_class.inverse_h_grids(self.numeric_grid_prefix.Text)

    def reverse_vertical(self, sender, e):
        self.rename_class.reverse_v_grids(self.alphabetic_grid_prefix.Text)

    def inverse_vertical(self, sender, e):
        self.rename_class.inverse_v_grids(self.alphabetic_grid_prefix.Text)

    def reverse_swap_names(self, sender, e):
        self.rename_class.reverse_swap_names()

    def swap_grid_names(self, sender, e):
        self.rename_class.swap_grid_names()

    def rename(self, sender, e):
        self.rename_class.rename_grids()

    def include_hidden_grids(self, sender, e):
        self.rename_class.get_all_grids_collections()

    def exclude_hidden_grids(self, sender, e):
        self.rename_class.get_visible_grids_only()

    """reuse the inverse method for assigning prefix to the grids names since those methods do not reverse the order
    of the names but just add prefixes.
    There is n need to add the prefix methods inside the .py UI class. It has been tackled here"""

    def prefix_horizontal_func(self, sender, e):
        self.inverse_horizontal("a", "b")

    def prefix_vertical_func(self, sender, e):
        self.inverse_vertical("a", "b")

    def close_button(self, sender, e):
        self.Close()

    def save_grid(self, sender, e):
        name = self.ui_save_textbox.Text
        print("saved grid option with '{}'".format(name))


class RenameGridsEngine:
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    dialog_bg_color = Color(33, 40, 50)
    selection_bg_color = Color(247, 191, 158)

    vertical_grids = []
    horizontal_grids = []

    vertical_sub_grids = []
    horizontal_sub_grids = []

    grids_subs_collection = []

    unstructured_grids_collection = []

    def __init__(self, parsed_grids_collection=None, include_hidden_grids=False):

        self.all_grids_collections = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().ToElements()
        self.include_hidden_grids = include_hidden_grids

        if parsed_grids_collection is None:
            if self.include_hidden_grids:
                self.get_all_grids_collections()
            else:
                self.get_visible_grids_only()
        else:
            self.horizontal_grids = parsed_grids_collection[0]
            self.vertical_grids = parsed_grids_collection[1]

    def get_visible_grids_only(self):
        self.unstructured_grids_collection = [i for i in self.all_grids_collections if i.get_BoundingBox(get2DView())]
        self.get_ordered_grids()

    def get_all_grids_collections(self):
        self.unstructured_grids_collection = self.all_grids_collections

        t.Start()
        EnableRevealHiddenElements(view2d)
        self.get_ordered_grids()
        DisableRevealHiddenElements(view2d)
        t.Commit()

    def name_exist(self, name):
        gen_name_list = ["{}{}".format(i, name) for i in ["*", ".", "_", "'", "^", ":"]]

        grid_names = [i.Name for i in self.all_grids_collections]

        if name in grid_names:
            for nm in gen_name_list:
                if nm not in grid_names:
                    return nm

        else:
            return name

    def get_ordered_grids(self):

        grids_collection_list = []
        for grid in self.unstructured_grids_collection:
            """get viewports placed on sheet"""

            # try:
            b_box = grid.get_BoundingBox(view2d)
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

        """#########################################################################################################"""
        """#########################################################################################################"""
        """reset values"""
        self.horizontal_grids = []
        self.vertical_grids = []
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
        grid_letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                        "S",
                        "T",
                        "U", "V", "W", "X", "Y", "Z", "A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.",
                        "K.",
                        "L.", "M.", "N.", "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."]

        """####################################################################################################"""
        """####################################################################################################"""
        """ set final name for the grid heads"""
        new_h_name = ""
        previous_name = ""
        new_sub_name = ""

        sub_alpha = 0
        sub_nums = grid_letters[sub_alpha]

        # sub_nums = 1
        pos = 1
        for h_grid_f in self.horizontal_grids:
            if pos == 1:
                new_h_name = "{}{}".format(prefix, str(pos))
                previous_name = new_h_name

                h_grid_f.get("elem").LookupParameter("Name").Set(self.name_exist(new_h_name))
                pos += 1

            else:
                if h_grid_f.get("sub") is True:
                    new_sub_name = "{}{}".format(previous_name, sub_nums)

                    sub_alpha += 1
                    sub_nums = grid_letters[sub_alpha]

                    h_grid_f.get("elem").LookupParameter("Name").Set(self.name_exist(new_sub_name))

                else:
                    new_h_name = "{}{}".format(prefix, str(pos))

                    h_grid_f.get("elem").LookupParameter("Name").Set(self.name_exist(new_h_name))
                    previous_name = new_h_name
                    """reset sub number"""

                    sub_nums = grid_letters[0]
                    pos += 1

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
        # for v_grid_f in self.vertical_grids:
        #     new_v_name = "{}{}".format(prefix, grid_letters[self.vertical_grids.index(v_grid_f)])
        #     v_grid_f.get("elem").LookupParameter("Name").Set(new_v_name)

        new_v_name = ""
        previous_name = ""
        new_sub_name = ""
        sub_nums = 1
        pos_alpha = 0
        pos = grid_letters[pos_alpha]
        for v_grid_f in self.vertical_grids:

            if pos == "A":
                new_v_name = "{}{}".format(prefix, str(pos))
                previous_name = new_v_name

                v_grid_f.get("elem").LookupParameter("Name").Set(self.name_exist(new_v_name))
                pos_alpha += 1
                pos = grid_letters[pos_alpha]

            else:
                if v_grid_f.get("sub") is True:
                    new_sub_name = "{}{}".format(previous_name, sub_nums)
                    sub_nums += 1

                    v_grid_f.get("elem").LookupParameter("Name").Set(self.name_exist(new_sub_name))

                else:
                    new_v_name = "{}{}".format(prefix, str(pos))

                    v_grid_f.get("elem").LookupParameter("Name").Set(self.name_exist(new_v_name))
                    previous_name = new_v_name
                    """reset sub number"""
                    sub_nums = 1
                    pos_alpha += 1
                    pos = grid_letters[pos_alpha]
        """####################################################################################################"""
        """####################################################################################################"""

    def rename_grids(self, transaction=True):

        if transaction:
            t.Start()

        self.temporal_rename_h_grid()
        self.temporal_rename_v_grid()

        self.final_rename_h_grid()
        self.final_rename_v_grid()

        if transaction:
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


class RenameGrids:
    def __init__(self, parsed_grids_collection=None, include_hidden_grids=False, hide_hidden_grids_checkbox=False):
        self.rename_class = RenameGridsEngine(parsed_grids_collection, include_hidden_grids)
        RenameGridsUI(parser_class=self.rename_class,
                      include_hidden_grids=include_hidden_grids,
                      hide_hidden_grids_checkbox=hide_hidden_grids_checkbox
                      )
