import clr

from SortNatural import real_sorting
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

clr.AddReference("System.Windows")
from System.Windows.Controls import SelectionChangedEventHandler
from System.Windows import RoutedEventHandler


class DropDownSelection(BaseWPFClass):
    selected_item = None

    def __init__(self, title=None, label_name=None, dropdown_list=None, button_name=None):
        BaseWPFClass.__init__(self, xaml_file_name="DropDownSelection.xaml")
        self.dropdown_dict_data = real_sorting(list_to_be_sorted=dropdown_list, dict_key="name")

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

        """update selection boxes with appropriate data source"""
        if dropdown_list is not None:
            self.dropdown_object.ItemsSource = [i.get("name") for i in self.dropdown_dict_data]
            self.dropdown_object.SelectedIndex = 0
            # self.selected_item = self.dropdown_object.SelectedItem

        if button_name is not None:
            self.button_object.Content = button_name

        """Attach the event handler to the button's "Click" event"""
        self.dropdown_object.SelectionChanged += SelectionChangedEventHandler(self.select_item)
        self.button_object.Click += RoutedEventHandler(self.button_run)

        self.ShowDialog()

    def button_run(self, sender, e):
        self.select_item("sender", "event")
        self.Close()

    def select_item(self, sender, e):
        self.selected_item = [i.get("element") for i in self.dropdown_dict_data if
                              i.get("name") == self.dropdown_object.SelectedItem].pop()
        # print(self.selected_item)
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
