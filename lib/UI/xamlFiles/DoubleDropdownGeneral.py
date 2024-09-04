import clr
from System.Collections.Generic import List

from SortNatural import real_sorting
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

clr.AddReference("System.Windows")
from System.Windows.Controls import SelectionChangedEventHandler, ComboBoxItem
from System.Windows import RoutedEventHandler

from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


class DoubleDropDownSelection(BaseWPFClass):

    def __init__(self, title=None,
                 dropdown_list1=None, dropdown_list2=None,
                 label_name1=None, label_name2=None,
                 button_name=None):

        self.selected_item1 = None
        self.selected_item2 = None

        BaseWPFClass.__init__(self, xaml_file_name="DoubleDropDownSelection.xaml")
        self.dropdown_dict_data1 = real_sorting(list_to_be_sorted=dropdown_list1, dict_key="name")
        self.dropdown_dict_data2 = real_sorting(list_to_be_sorted=dropdown_list2, dict_key="name")

        """Find the "button_run" button by its name"""
        self.label_object1 = self.Window.FindName("label_object1")
        self.dropdown_object1 = self.Window.FindName("dropdown_object1")

        self.label_object2 = self.Window.FindName("label_object2")
        self.dropdown_object2 = self.Window.FindName("dropdown_object2")

        self.button_object = self.Window.FindName("button_object")

        if title is not None:
            self.Window.Title = title

        if label_name1 is not None:
            self.label_object1.Text = label_name1

        if label_name2 is not None:
            self.label_object2.Text = label_name2

        """update selection boxes with appropriate data source"""
        if dropdown_list1 is not None:
            """#####################################################################################"""
            new_proj_source = List[type(ComboBoxItem())]()
            for project_item in self.dropdown_dict_data1:
                proj_combo_box_item = ComboBoxItem()
                proj_combo_box_item.Content = project_item.get("name")
                new_proj_source.Add(proj_combo_box_item)

            self.dropdown_object1.ItemsSource = new_proj_source
            self.dropdown_object1.SelectedIndex = 0

            """update title block combobox"""
            sender = self.dropdown_dict_data1[0].get("name")
            self.select_item(sender=sender)
            """#####################################################################################"""
        if dropdown_list2 is not None:

            """##############################################################"""
            all_tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()
            title_block_families = []
            control_list = []
            for tb in all_tbs:
                if tb.Family.Name not in control_list:
                    control_list.append(tb.Family.Name)
                    title_block_families.append({"name": tb.Family.Name, "element": tb.Family})
            self.dropdown_dict_data2 = real_sorting(list_to_be_sorted=title_block_families, dict_key="name")
            """##############################################################"""

            new_source = List[type(ComboBoxItem())]()

            for project_item in self.dropdown_dict_data2:
                combo_box_item = ComboBoxItem()
                combo_box_item.Content = project_item.get("name")
                new_source.Add(combo_box_item)

            self.dropdown_object2.ItemsSource = new_source
            self.dropdown_object2.SelectedIndex = 0

        if button_name is not None:
            self.button_object.Content = button_name

        """Attach the event handler to the button's "Click" event"""
        self.dropdown_object1.SelectionChanged += SelectionChangedEventHandler(self.select_item)
        self.button_object.Click += RoutedEventHandler(self.button_run)

        self.ShowDialog()

    def select_item(self, sender=None, e=None):
        if isinstance(sender, str):
            compare = sender
        else:
            compare = sender.SelectedItem.Content

        def get_title_blocks(document):
            """Update ViewTemplates ListBox"""
            """##############################################################"""
            all_tbs = Fec(document).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()
            title_block_families = []
            control_list = []
            for tb in all_tbs:
                if tb.Family.Name not in control_list:
                    control_list.append(tb.Family.Name)
                    title_block_families.append({"name": tb.Family.Name, "element": tb.Family})
            """##############################################################"""

            sorted_tbs = real_sorting(list_to_be_sorted=title_block_families, dict_key="name")
            return sorted_tbs

        sel = [project_item.get("element") for project_item in self.dropdown_dict_data1 if
               project_item.get("name") == compare]

        if len(sel) != 0:
            new_source = List[type(ComboBoxItem())]()

            selected_doc = sel.pop()

            self.dropdown_dict_data2 = real_sorting(list_to_be_sorted=get_title_blocks(selected_doc), dict_key="name")

            for project_item in self.dropdown_dict_data2:
                combo_box_item = ComboBoxItem()
                combo_box_item.Content = project_item.get("name")
                new_source.Add(combo_box_item)

            self.dropdown_object2.ItemsSource = new_source
            self.dropdown_object2.SelectedIndex = 0

    def button_run(self, sender, e):
        """get the values if the user used the defaults values without selecting anything from the box"""
        selected_item1 = [i.get("element") for i in self.dropdown_dict_data1 if
                          i.get("name") == self.dropdown_object1.SelectedItem.Content]

        if len(selected_item1) != 0:
            self.selected_item1 = selected_item1.pop()

        try:
            """get the values if the user used the defaults values without selecting anything from the box"""
            selected_item2 = [i.get("element") for i in self.dropdown_dict_data2 if
                              i.get("name") == self.dropdown_object2.SelectedItem.Content]

            if len(selected_item2) != 0:
                self.selected_item2 = selected_item2.pop()
        except:
            pass

        self.Close()
