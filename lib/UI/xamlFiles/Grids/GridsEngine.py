import operator

from UI.xamlFiles.Grids.CommonImports import Color, t
from getView import get2DView

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView

view2d = get2DView()


class RenameGridsEngine:
    bg_color = Color(app.BackgroundColor.Red, app.BackgroundColor.Green, app.BackgroundColor.Blue)
    dialog_bg_color = Color(33, 40, 50)
    selection_bg_color = Color(247, 191, 158)

    vertical_grids = []
    horizontal_grids = []
    all_grids_collections = []

    vertical_sub_grids = []
    horizontal_sub_grids = []

    grids_subs_collection = []

    unstructured_grids_collection = []

    vertical_and_horizontal_grids = []
    merged_vertical_and_horizontal_grids = []

    def __init__(self, selection_class):

        self.selection_class = selection_class

        parsed_grids_collection = selection_class.vertical_and_horizontal_grids

        self.update_collection(parsed_grids_collection)

    def update_collection(self, horizontal_and_vertical_grids):
        if horizontal_and_vertical_grids is not None and len(horizontal_and_vertical_grids) == 2:
            self.horizontal_grids = horizontal_and_vertical_grids[0]
            self.vertical_grids = horizontal_and_vertical_grids[1]
            self.all_grids_collections = self.horizontal_grids + self.vertical_grids

    def name_exist(self, name):
        r"""name cannot contain any of the following \ : { } [ ] | ; < > ? ` ~"""
        gen_name_list = ["{}{}".format(i, name) for i in ["^", ".", "_", "'", "*"]]

        grid_names = [i.get("elem").Name for i in self.selection_class.excluded_grids]

        if name in grid_names:
            """Name exist"""

            existing_grid = list(filter(lambda x: x.get("name") == name, self.selection_class.excluded_grids)).pop()
            for new_name in gen_name_list:
                if new_name not in grid_names:
                    """change name of existing grid"""
                    existing_grid["elem"].LookupParameter("Name").Set(new_name)
        return name

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
