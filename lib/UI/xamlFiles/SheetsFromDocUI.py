import clr
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic
from System.Collections.Generic import List

from lib.SortNatural import real_sorting

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")

from System.Windows.Controls import StackPanel, Orientation, TextBox, Label, ComboBoxItem, ComboBox, \
    SelectionChangedEventHandler, TextBlock
from System.Windows import RoutedEventHandler, Thickness
from System.Windows import Visibility

from lib.UI.xamlFiles.DropDownSelection import DropDownSelection


class SheetsFromDocUI(DropDownSelection):

    def __init__(self, doc_items=None, title_block_items=None):
        DropDownSelection.__init__(self, dropdown_list=title_block_items)
        self.Window.Height = 180
        self.docs_list = doc_items
        self.title_block_list = title_block_items

        self.label_object.Text = "Title Block"

        self.selected_project = None
        # self.selected_title_block = None

        """add_top_allowance buttons"""
        self.docs_combobox = self.add_button(host_panel=self.top_allowance_panel,
                                             label_name="Select Project",
                                             event_function=self.on_selection_changed)

        # self.prefix_label = self.add_button(host_panel=self.bottom_allowance_panel,
        #                                     label_name="Prefix", on_key_up_function=self.prefix_textbox_key_up, )

        self.ShowDialog()

    # @staticmethod
    def add_button(self, host_panel, label_name="Text", event_function=None):
        # panel = StackPanel()
        host_panel.Orientation = Orientation.Horizontal
        host_panel.Margin = Thickness(0, 20, 0, 0)

        label = TextBlock()
        label.Text = label_name
        label.Width = 100

        combobox = ComboBox()
        combobox.Height = 20
        combobox.Width = 150
        combobox.Margin = Thickness(10, 0, 0, 0)
        for project_item in self.docs_list:
            combo_box_item = ComboBoxItem()
            combo_box_item.Content = project_item.get("name")
            combo_box_item.IsSelected = False

            combobox.Items.Add(combo_box_item)

        combobox.SelectedIndex = 0
        self.selected_project = combobox.SelectedItem

        """add event handler"""
        if event_function is not None:
            combobox.SelectionChanged += SelectionChangedEventHandler(event_function)

        host_panel.Children.Add(label)
        host_panel.Children.Add(combobox)
        # host_panel.Children.Add(panel)

        return combobox

    def on_selection_changed(self, sender, e):

        def get_title_blocks(doc):
            """Update ViewTemplates ListBox"""
            tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()

            sorted_tbs = real_sorting(
                list_to_be_sorted=[{"name": tb.LookupParameter("Family Name").AsString(), "element": tb} for tb in tbs],
                dict_key="name")
            return sorted_tbs

        sel = [project_item.get("element") for project_item in self.docs_list if
               project_item.get("name") == sender.SelectedItem.Content]

        # print selected_doc

        # print(self.docs_list[1].get("name") == sender.SelectedItem.Content)
        # print(selected_doc)

        # self.dropdown_object.Items.Clear()
        if len(sel) != 0:

            new_source = []

            selected_doc = sel.pop()
            for project_item in get_title_blocks(selected_doc):
                combo_box_item = ComboBoxItem()
                combo_box_item.Content = project_item.get("name")
                # combo_box_item.IsSelected = False
                new_source.append(combo_box_item)

            self.dropdown_object.ItemsSource = new_source
