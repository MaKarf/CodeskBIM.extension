import clr

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")

from System.Windows.Controls import StackPanel, Orientation, Label, ComboBox, ComboBoxItem, SelectionChangedEventHandler
from System.Collections.Generic import List
from System.Windows import Thickness

from lib.UI.xamlFiles.CheckboxSelection import CheckboxSelection

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document

stack_panel = """
<StackPanel HorizontalAlignment="Center" Orientation="Horizontal" Margin="10,15,0,0">
            <TextBlock x:Name="label_object2" Text="Select" Width="100" Height="20" />
            <ComboBox x:Name="dropdown_object2" Width="150" Height="20" Margin="10,0,0,0">
            </ComboBox>
        </StackPanel>
"""


class CheckBoxAndDropdown(CheckboxSelection):
    def __init__(self,
                 dropdown_list=(),
                 checkbox_data=(),
                 select_multiple=False,
                 parser_class=None,
                 window_title="",
                 selection_name="Finish",
                 finish_button_text_name="Select",
                 drop_down_label="",
                 checkbox_container_height=350):

        CheckboxSelection.__init__(self, items=checkbox_data, select_multiple=select_multiple,
                                   parser_class=parser_class,
                                   window_title=window_title,
                                   selection_name=selection_name, finish_button_text_name=finish_button_text_name)
        self.schedule_type = None
        self.dropdown_label = drop_down_label
        self.checkbox_container_height = checkbox_container_height

        self.dropdown_list = dropdown_list
        self.dropdown_object = None

        self.add_button(host_panel=self.bottom_allowance_panel)
        self.main_list_box.Height = self.checkbox_container_height
        self.bottom_allowance_panel.Margin = Thickness(0, 10, 0, 5)
        # self.show_dialog()

    def add_button(self, host_panel):
        panel = StackPanel()
        panel.Orientation = Orientation.Horizontal

        label = Label()
        label.Content = self.dropdown_label

        self.dropdown_object = ComboBox()
        self.dropdown_object.SelectionChanged += SelectionChangedEventHandler(self.update_schedule_type)
        # self.dropdown_object.Height = 20
        self.dropdown_object.Width = 120

        """update selection boxes with appropriate data source"""
        if self.dropdown_list is not None:
            """#####################################################################################"""
            schedule_type_source = List[type(ComboBoxItem())]()
            for schedule_type in self.dropdown_list:
                schedule_type_combo_box_item = ComboBoxItem()
                schedule_type_combo_box_item.Content = schedule_type.get("name")
                schedule_type_source.Add(schedule_type_combo_box_item)

            self.dropdown_object.ItemsSource = schedule_type_source
            self.dropdown_object.SelectedIndex = 0
            """#####################################################################################"""
        panel.Children.Add(label)
        panel.Children.Add(self.dropdown_object)
        host_panel.Children.Add(panel)

    def update_schedule_type(self, sender, event):
        item = [i.get("element") for i in self.dropdown_list if i.get("name") == sender.SelectedItem.Content]
        self.schedule_type = item.pop() if item else None
