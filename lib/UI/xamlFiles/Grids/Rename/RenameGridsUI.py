import clr

from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

from update_projects_data import ProjectData

from lib.UI.xamlFiles.Grids.GridsEngine import RenameGridsEngine

clr.AddReference("System.Windows")
from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler
from System.Windows import Visibility

from UI.xamlFiles.Grids.CommonImports import doc


class RenameGridsUI(BaseWPFClass):
    pd = ProjectData(doc.Title)
    path = pd.path

    def __init__(self, selection_class, include_hidden_grids=None):
        BaseWPFClass.__init__(self, xaml_file_name=r"Grids\Rename\RenameGrids.xaml", )

        self.selection_class = selection_class

        if len(self.selection_class.merged_vertical_and_horizontal_grids) != 0:
            self.rename_class = RenameGridsEngine(selection_class)

            hide_hidden_grids_checkbox = True if include_hidden_grids is None else False
            self.minus = self.hidden_grids_checkbox.Height if hide_hidden_grids_checkbox else 0

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

            self.hidden_grids_checkbox.Checked += RoutedEventHandler(self.toggle_hidden_grids)
            self.hidden_grids_checkbox.Unchecked += RoutedEventHandler(self.toggle_hidden_grids)

            self.button_run.Click += RoutedEventHandler(self.rename)
            self.save_grid_panel.Visibility = Visibility.Collapsed
            self.ui_save_button.Click += RoutedEventHandler(self.save_grid)

            self.collapse_save_panel("sender", "e")

            self.ShowDialog()
        else:
            """close window if there are no grids"""
            self.Close()

    def expand_save_panel(self, sender, e):
        self.save_grid_panel.Visibility = Visibility.Visible
        self.base_line.Visibility = Visibility.Visible
        self.Window.Height = 300 - self.minus
        self.ui_save_textbox.Focus()

    def collapse_save_panel(self, sender, e):
        self.save_grid_panel.Visibility = Visibility.Collapsed
        self.base_line.Visibility = Visibility.Collapsed
        self.Window.Height = 200 - self.minus

        self.ui_save_textbox.Text = ""
        self.ui_hint.Text = ""

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

    def toggle_hidden_grids(self, sender, e):
        # print sender.IsChecked
        vertical_and_horizontal_grids = self.selection_class.from_revit_db(sender.IsChecked)
        # print len(self.selection_class.merged_vertical_and_horizontal_grids)
        self.rename_class.update_collection(vertical_and_horizontal_grids)

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
        """update json"""
        if self.ui_save_textbox.Text == "":
            self.ui_hint.Text = "Option Name required"
        else:
            # self.Close()
            self.pd.save_grid_selection(self.ui_save_textbox.Text,
                                        self.selection_class.merged_vertical_and_horizontal_grids)
            """update ui"""
            self.ui_hint.Text = "Option saved successfully"
            self.ui_save_textbox.Text = ""
            self.ui_save_textbox.Focus()
            # print self.selection_class.merged_vertical_and_horizontal_grids

    def check_name(self, sender, e):
        option_name = self.ui_save_textbox.Text
        if option_name == "":
            self.ui_hint.Text = "Option Name required"
        elif option_name.lower() in self.pd.current_options_checker_list:
            self.ui_hint.Text = "Name already exist, proceed to override it"
        else:
            self.ui_hint.Text = ""
