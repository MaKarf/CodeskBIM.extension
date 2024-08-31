import os

import clr
from Autodesk.Revit.DB import ViewSheet
from pyrevit import forms

clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import Visibility

PATH_SCRIPT = os.path.dirname(__file__)

ui_doc = __revit__.ActiveUIDocument
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

active_view_id = doc.ActiveView.Id
active_view = doc.GetElement(active_view_id)
active_view_level = active_view.GenLevel


class ListItem:
    """Helper Class for displaying selected sheets in my custom GUI."""

    def __init__(self, Name='Unnamed', element=None, checked=False):
        self.Name = Name
        self.IsChecked = checked
        self.element = element


class SelectSheetsFromDialog(forms.WPFWindow):
    def __init__(self, sheet_list=None, label="Select Elements:", select_multiple=True):

        alpha_sheet_list = sheet_list[0]
        numeric_sheet_list = sheet_list[1]

        if sheet_list is None:
            numeric_sheet_list = {}
            alpha_sheet_list = {}
        self.form = forms.WPFWindow.__init__(self, "RenumberSheets_Split.xaml")

        self.alphabets_only = False
        self.SelectMultiple = select_multiple

        self.alpha_given_dict_items = {k: v for k, v in alpha_sheet_list.items() if k}
        self.numeric_given_dict_items = {k: v for k, v in numeric_sheet_list.items() if k}

        self.alpha_items = self.generate_list_items(self.alpha_given_dict_items)
        self.numeric_items = self.generate_list_items(self.numeric_given_dict_items)

        self.selected_items = []

        # UPDATE GUI ELEMENTS
        self.text_label.Content = label
        self.deselect_other_checkboxes = True

        if not select_multiple:
            self.UI_Buttons_all_none.Visibility = Visibility.Collapsed

        self.intro_sheets_ListBox.ItemsSource = self.alpha_items
        self.main_ListBox.ItemsSource = self.numeric_items

        """select all sheets on startup"""
        self.select_mode(mode='all')

        self.ShowDialog()

    def __iter__(self):
        """Return selected items."""
        return iter(self.selected_items)

    @staticmethod
    def generate_list_items(given_dict_items):
        """Function to create a ICollection to pass to ListBox in GUI"""

        list_of_items = List[type(ListItem())]()
        first = True

        for sheet_name, sheet_elem in given_dict_items.items():
            # print(sheet_elem)
            checked = True if first else False
            first = False
            list_of_items.Add(ListItem(sheet_name, sheet_elem))

        return list_of_items

    @property
    def prefix(self):
        return self.ui_prefix.Text

    @property
    def start_count(self):
        return int(self.ui_start_number.Text)

    def check_alphabets_checkbox(self, sender, e):
        self.deselect_other_checkboxes = True
        """check the checkbox"""
        self.alphabets_only = True

        """check all the checkboxes in the intro list box"""
        list_of_intro_items = List[type(ListItem())]()
        for intro_item in self.intro_sheets_ListBox.ItemsSource:
            intro_item.IsChecked = True
            list_of_intro_items.Add(intro_item)
        self.intro_sheets_ListBox.ItemsSource = list_of_intro_items

        """check all the checkboxes in the main list box"""
        list_of_main_items = List[type(ListItem())]()
        for main_item in self.main_ListBox.ItemsSource:
            main_item.IsChecked = False
            list_of_main_items.Add(main_item)
        self.main_ListBox.ItemsSource = list_of_main_items

        return self.alphabets_only

    def uncheck_alpha(self, sender, e):
        """check the checkbox"""
        # print("unchecked")
        self.deselect_other_checkboxes = False
        self.ui_alphabets_only.IsChecked = False

    def uncheck_alphabets_checkbox(self, sender, e):
        """check the checkbox"""
        if self.deselect_other_checkboxes:
            """uncheck all the checkboxes in the intro list box"""
            list_of_intro_items = List[type(ListItem())]()
            for intro_item in self.intro_sheets_ListBox.ItemsSource:
                intro_item.IsChecked = False
                list_of_intro_items.Add(intro_item)
            self.intro_sheets_ListBox.ItemsSource = list_of_intro_items

        if self.deselect_other_checkboxes:
            """check all the checkboxes in the main list box"""
            list_of_main_items = List[type(ListItem())]()
            for main_item in self.main_ListBox.ItemsSource:
                main_item.IsChecked = True
                list_of_main_items.Add(main_item)
            self.main_ListBox.ItemsSource = list_of_main_items

        self.alphabets_only = False
        return self.alphabets_only

    """#############################################################################################"""

    def text_filter_updated(self, sender, e):
        """Function to filter items in the main_ListBox."""
        filtered_list_of_items = List[type(ListItem())]()
        filter_keyword = self.textbox_filter.Text

        # RESTORE ORIGINAL LIST
        if not filter_keyword:
            self.main_ListBox.ItemsSource = self.numeric_items

            return

        # FILTER ITEMS
        for item in self.numeric_items:
            if filter_keyword.lower() in item.Name.lower():
                filtered_list_of_items.Add(item)

        # UPDATE LIST OF ITEMS
        self.main_ListBox.ItemsSource = filtered_list_of_items

    def ui_main_item_checked(self, sender, e):
        # SINGLE SELECTION
        if not self.SelectMultiple:
            filtered_list_of_items = List[type(ListItem())]()
            for item in self.main_ListBox.Items:
                item.IsChecked = True if item.Name == sender.Content.Text else False
                print(sender.Content.Text)
                filtered_list_of_items.Add(item)
            self.main_ListBox.ItemsSource = filtered_list_of_items
    
    def ui_intro_item_checked(self, sender, e):
        detect_all_checks = False
        if False in [item_1.IsChecked for item_1 in self.intro_sheets_ListBox.Items]:
            detect_all_checks = False
            # print(detect_all_checks)
        else:
            detect_all_checks = True
            # print(detect_all_checks)

        if detect_all_checks:
            self.deselect_other_checkboxes = True
            self.ui_alphabets_only.IsChecked = True

    def select_mode(self, mode):
        """Helper function for following buttons:
        - button_select_all
        - button_select_none"""

        list_of_items = List[type(ListItem())]()
        checked = True if mode == 'all' else False
        for item in self.main_ListBox.ItemsSource:
            item.IsChecked = checked
            list_of_items.Add(item)

        self.main_ListBox.ItemsSource = list_of_items

    def button_select_all(self, sender, e):
        """ """
        self.select_mode(mode='all')

    def button_select_none(self, sender, e):
        """ """
        self.select_mode(mode='none')

    def button_select(self, sender, e):
        """Button to finilize selection"""
        # Reset Filter
        self.textbox_filter.Text = ''
        self.Close()

        """compile selections from the numeric listbox"""
        selected_items = []
        for item in self.main_ListBox.ItemsSource:
            if item.IsChecked:
                selected_items.append(item.element)
                # print(item.Name)

        """compile selections from the alpha listbox"""
        for item2 in self.intro_sheets_ListBox.ItemsSource:
            if item2.IsChecked:
                selected_items.append(item2.element)
                # print(item.Name)
        self.selected_items = selected_items


class SelectedSheetsWindow(forms.WPFWindow):
    """GUI for View renaming tool."""

    def __init__(self):
        """use this if the xaml file is located in the pushbutton folder"""
        self.form = forms.WPFWindow.__init__(self, "RenumberSheets_Prefix.xaml")
        self.alphabets_only = False
        self.selected_items = []
        self.ShowDialog()

    def __iter__(self):
        """Return selected items."""
        return iter(self.selected_items)

    # >>>>>>>>>> PROPERTIES
    @property
    def prefix(self):
        return self.ui_prefix.Text

    @property
    def start_count(self):
        return int(self.ui_start_number.Text)

    def check_alphabets_checkbox(self, sender, e):
        self.alphabets_only = True
        return self.alphabets_only

    def uncheck_alphabets_checkbox(self, sender, e):
        self.alphabets_only = False
        return self.alphabets_only

    # >>>>>>>>>> GUI EVENTS
    def button_click_run(self, sender, e):
        self.Close()
