import clr

from SortNatural import real_sorting
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

from lib.UI.Popup import Alert
from lib.UI.WPFuiData import ComboBoxData

clr.AddReference("System.Windows")
from System.Windows.Controls import SelectionChangedEventHandler
from System.Windows import RoutedEventHandler


class DropDownSelection(BaseWPFClass):
    selected_item = None
    dropdown_dict_data = []

    def __init__(self, title=None, label_name=None, dropdown_list=None, button_name=None,
                 show_window_automatically=True):

        """update selection boxes with appropriate data source"""
        if dropdown_list is not None:

            BaseWPFClass.__init__(self, xaml_file_name="DropDownSelection.xaml")
            # print dropdown_list
            """Find the "button_run" button by its name"""
            self.top_allowance_panel = self.Window.FindName("top_allowance_panel")
            self.bottom_allowance_panel = self.Window.FindName("bottom_allowance_panel")

            self.label_object = self.Window.FindName("label_object")
            self.dropdown_object = self.Window.FindName("dropdown_object")
            self.button_object = self.Window.FindName("button_object")

            if title is not None:
                self.Window.Title = title

            if label_name is not None:
                self.label_object.Text = label_name

            """Attach the event handler to the button's "Click" event"""
            self.dropdown_object.SelectionChanged += SelectionChangedEventHandler(self.selection_changed)
            self.button_object.Click += RoutedEventHandler(self.button_run)

            self.update_selection(dropdown_list)

            if button_name is not None:
                self.button_object.Content = button_name

            if show_window_automatically:
                self.ShowDialog()

        else:
            Alert(title="No Data", header="No Data fed", content="No need to display UI if no data was fed")
            self.Close()

    def update_selection(self, dict_data):
        # print dict_data
        if len(dict_data) != 0:
            dropdown_dict_data = real_sorting(list_to_be_sorted=dict_data, dict_key="name")
            self.dropdown_dict_data = [ComboBoxData(display_name=i["name"], selected_item_value=i["element"])
                                       for i in dropdown_dict_data]

            self.dropdown_object.ItemsSource = self.dropdown_dict_data
            self.dropdown_object.DisplayMemberPath = "Name"

            self.dropdown_object.SelectedIndex = 0
            self.selected_item = self.dropdown_object.SelectedItem
        else:
            self.dropdown_object.ItemsSource = []

    def button_run(self, sender, e):
        self.selection_changed(sender, e)
        self.close_window()

    def selection_changed(self, sender, e):
        self.selected_item = self.dropdown_object.SelectedItem
        return self.selected_item


""" How to use the Class"""

"""from UI.xamlFiles.DropDownSelection import DropDownSelection

# create a dictionary of 'name':'item name in list, 'object':'item object for post process'
dropdown_list = [{"name": "Item {}".format(i), "object": i} for i in range(10)]
DropDownSelection(
    title="Select Rooms",
    label_name="Make a Choice",
    dropdown_list=dropdown_list,
    button_name="Click")    
"""

# # create a dictionary of 'name':'item name in list, 'object':'item object for post process'
# dropdown_list = [{"name": "Item {}".format(i + 1), "object": i} for i in range(10)]
# results = DropDownSelection(
#     title="Select Rooms",
#     label_name="Make a Choice",
#     dropdown_list=dropdown_list,
#     button_name="Click")
# print(results)
