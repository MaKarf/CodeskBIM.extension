import clr

from SortNatural import real_sorting
from UI.xamlFiles.SetWPFColor import set_wpf_component_background_color
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from getView import get2DView
from imports.DotNetSystem import List

clr.AddReference("System.Windows")
from System.Windows import RoutedEventHandler, Media
from System.Windows.Controls import ComboBoxItem, SelectionChangedEventHandler

from Autodesk.Revit.DB import Transaction

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "DoorsAndWindowsSchedule")
active_view = ui_doc.ActiveView

view2d = get2DView()


class DoorsAndWindowsSchedule(BaseWPFClass):

    def __init__(self, operation_list_data=None, sheets_list_data=None):
        self.operation_type = None
        self.selected_sheet = None

        BaseWPFClass.__init__(self, xaml_file_name="DoorsAndWindowsSchedule.xaml")
        self.operation_list_data = real_sorting(list_to_be_sorted=operation_list_data, dict_key="name")
        self.sheets_list_data = real_sorting(list_to_be_sorted=sheets_list_data, dict_key="name")

        """Attach the event handler to the button's "Click" event"""
        self.operation_type_dropdown_object.SelectionChanged += SelectionChangedEventHandler(self.select_operation)
        self.sheets_dropdown_object.SelectionChanged += SelectionChangedEventHandler(self.select_sheet)
        self.button_run.Click += RoutedEventHandler(self.create_button)

        """update selection boxes with appropriate data source"""
        if operation_list_data is not None:
            """#####################################################################################"""
            list1_source = List[type(ComboBoxItem())]()
            for project_item in self.operation_list_data:
                list1_combo_box_item = ComboBoxItem()
                list1_combo_box_item.Content = project_item.get("name")
                list1_source.Add(list1_combo_box_item)

            self.operation_type_dropdown_object.ItemsSource = list1_source
            self.operation_type_dropdown_object.SelectedIndex = 0
            """#####################################################################################"""

        if sheets_list_data is not None:
            """#####################################################################################"""
            list2_source = List[type(ComboBoxItem())]()
            for project_item2 in self.sheets_list_data:
                list2_combo_box_item = ComboBoxItem()
                list2_combo_box_item.Content = project_item2.get("name")
                list2_source.Add(list2_combo_box_item)

            self.sheets_dropdown_object.ItemsSource = list2_source
            self.sheets_dropdown_object.SelectedIndex = 0
            """#####################################################################################"""

        self.ShowDialog()

    def expand_save_panel(self, sender, e):
        self.Top -= 200
        self.Height = 570

        """set background color"""
        "A6C2E3"
        set_wpf_component_background_color(hex_color="#A6C2E3", wpf_component=self.settings)

    def collapse_save_panel(self, sender, e):
        self.Top += 200
        self.Height = 200

        """set background color"""
        set_wpf_component_background_color(hex_color="#E6ECF3", wpf_component=self.settings)

    def select_operation(self, sender, e):
        self.operation_type = [i.get("element") for i in self.operation_list_data if
                               i.get("name") == sender.SelectedItem.Content].pop()

    def select_sheet(self, sender, e):
        self.selected_sheet = [i.get("element") for i in self.sheets_list_data if
                               i.get("name") == sender.SelectedItem.Content].pop()

    def create_button(self, sender, e):
        self.Close()

    def save_grid(self, sender, e):
        name = self.ui_save_textbox.Text
        print("saved grid option with '{}'".format(name))
