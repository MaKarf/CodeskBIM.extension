import clr

from lib.UI.xamlFiles.RenameGrids import RenameGrids
from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

clr.AddReference("System.Windows.Forms")

from System.Windows import RoutedEventHandler
from System.Windows.Controls import SelectionChangedEventHandler

from System.Windows import Visibility


class LoadAndRenameGrids(BaseWPFClass):
    selected_combobox_option_key = ""
    items_source = []

    def __init__(self, xaml_file_name):
        BaseWPFClass.__init__(self, xaml_file_name)

        """Find the "button_run" button by its name"""
        rename_button_object = self.Window.FindName("rename_button")
        load_option_object = self.Window.FindName("load_option")
        delete_option_object = self.Window.FindName("delete_option")

        """Attach the event handler to the button's "Click" event"""

        rename_button_object.Click += RoutedEventHandler(self.rename_button_click)
        load_option_object.SelectionChanged += SelectionChangedEventHandler(self.load_option_click)
        delete_option_object.Click += RoutedEventHandler(self.delete_option_click)

        self.ShowDialog()

    def delete_option_click(self, sender, event_args):
        """Define the event handler for the Delete button click"""
        # selected_item = self.Window.FindName("combo_box").SelectedItem
        # if selected_item is not None:
        #     self.data_object.ItemsSource.Remove(selected_item)
        #
        #     """delete from database"""
        #     self.rename_class.pd.delete_grid_option(self.selected_combobox_option_key)
        #
        #     """set the next item"""
        #     if len(self.data_object.ItemsSource) > 0:
        #         self.Window.FindName("combo_box").SelectedIndex = 0  # Set the first item as the default selected item
        pass

    def load_option_click(self, sender, e):
        pass

    def rename_button_click(self, sender, e):
        self.close_window()
        RenameGrids()
