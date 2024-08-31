import clr

from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from lib.UI.xamlFiles.forms import ListItem

clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System.Collections.Generic import List
from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler
from System.Windows import Visibility, Thickness
from System.Windows.Controls import SelectionMode, StackPanel, Orientation, CheckBox

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView


class CheckboxSelection(BaseWPFClass):

    def __init__(self, items=None, select_multiple=True, parser_class=None, window_title="Selection Window",
                 window_width=None, window_height=None,
                 selection_name="Select Elements", finish_button_text_name="Finish"):
        BaseWPFClass.__init__(self, xaml_file_name="CheckboxSelection.xaml", )

        self.parser_class = parser_class

        if window_title is not None:
            self.Window.Title = window_title

        if window_width is not None:
            self.Window.Width = window_width

        if window_height is not None:
            self.Window.Height = window_height

        self.select_multiple = select_multiple

        self.given_dict_items = items
        self.selected_items = []

        """Find elements by their name"""
        self.top_allowance_panel = self.Window.FindName("top_allowance_panel")
        self.bottom_allowance_panel = self.Window.FindName("bottom_allowance_panel")

        self.top_error_message = self.Window.FindName("top_error_message")
        self.bottom_error_message = self.Window.FindName("bottom_error_message")
        self.top_error_message.Visibility = Visibility.Collapsed
        self.bottom_error_message.Visibility = Visibility.Collapsed

        self.textbox_filter = self.Window.FindName("textbox_filter")
        self.selection_type_text_label = self.Window.FindName("selection_type_text_label")
        self.main_list_box = self.Window.FindName("main_list_box")
        self.main_list_box_checkbox = self.main_list_box.FindName("main_list_box_checkbox")

        self.check_mode_panel = self.Window.FindName("check_mode_panel")
        self.check_all = self.Window.FindName("check_all")
        self.check_none = self.Window.FindName("check_none")
        self.finish_button = self.Window.FindName("finish_button")

        self.selection_type_text_label.Content = selection_name
        self.finish_button.Content = finish_button_text_name

        self.items = self.generate_list_items()

        self.main_list_box.ItemsSource = self.items

        """Attach the event handler to the button's "Click" event"""
        self.check_all.Click += RoutedEventHandler(self.button_select_all)
        self.check_none.Click += RoutedEventHandler(self.button_select_none)
        self.textbox_filter.KeyUp += KeyEventHandler(self.text_filter_updated)

        self.finish_button.Click += RoutedEventHandler(self.finish_selection)

        """hide the select all and select none button if intended for single selection"""
        if not self.select_multiple:
            self.check_mode_panel.Visibility = Visibility.Collapsed
            self.Window.Height -= 25
            self.main_list_box.SelectionMode = SelectionMode.Single

        # # Attach key down and key up event handlers
        # self.Window.KeyDown += self.on_key_down
        # self.Window.KeyUp += self.on_key_up
        #
        # # Global variables to track shift state and last clicked checkbox
        # self.shift_pressed = False
        # self.last_clicked_checkbox = None

    def __iter__(self):
        """Return selected items."""
        return iter(self.selected_items)

    def generate_list_items(self):
        list_of_items = List[type(ListItem(cls=self))]()

        if self.given_dict_items is not None:
            for item in self.given_dict_items:
                list_of_items.Add(ListItem(cls=self, name=item.get("name"), element=item.get("element"),
                                           select_multiple=self.select_multiple))
            return list_of_items
        return None

    def text_filter_updated(self, sender, e):
        """Function to filter items in the main_ListBox."""
        filtered_list_of_items = List[type(ListItem(cls=self))]()
        filter_keyword = self.textbox_filter.Text

        """ RESTORE ORIGINAL LIST"""
        if not filter_keyword:
            self.main_list_box.ItemsSource = self.items
            return

        """ FILTER ITEMS"""
        for item in self.items:
            if filter_keyword.lower() in item.check_box.Content.lower():
                filtered_list_of_items.Add(item)

        """ UPDATE LIST OF ITEMS"""
        self.main_list_box.ItemsSource = filtered_list_of_items

    def select_mode(self, mode):
        """Helper function for following buttons:
        - button_select_all
        - button_select_none"""

        list_of_items = List[type(ListItem(cls=self))]()
        checked = True if mode == 'all' else False
        for item in self.main_list_box.ItemsSource:
            item.check_box.IsChecked = checked
            list_of_items.Add(item)

        """update the selected elements list"""
        self.selected_items = []  # """empty the list for further operation"""
        [self.selected_items.append(item.element) for item in self.main_list_box.ItemsSource if mode == 'all']

        self.main_list_box.ItemsSource = list_of_items

    def button_select_all(self, sender, e):
        """ """
        self.select_mode(mode='all')

    def button_select_none(self, sender, e):
        """ """
        self.select_mode(mode='none')

    def checker(self, sender):
        # print(sender.Content)
        check = sender.IsChecked
        check_inverse = False if check is True else True

        for item in self.main_list_box.ItemsSource:

            if item.check_box.Content == sender.Content:
                if self.select_multiple:

                    if item.element in self.selected_items:
                        if not check:
                            self.selected_items.remove(item.element)
                    else:
                        if check:
                            self.selected_items.append(item.element)

                else:
                    if item.element in self.selected_items:
                        if not check:
                            self.selected_items = []
                    else:
                        if check:
                            self.selected_items = []
                            self.selected_items.append(item.element)

            else:
                if not self.select_multiple:
                    item.check_box.IsChecked = check_inverse

    def finish_selection(self, sender, e):
        """Button to finalize selection"""
        """Reset Filter"""
        self.lock = False
        self.textbox_filter.Text = ''
        self.close_window()

    # def on_checkbox_click(self, sender, e):
    #     global last_clicked_checkbox
    #     if shift_pressed:
    #         start_index = checkboxes.index(last_clicked_checkbox)
    #         end_index = checkboxes.index(sender)
    #         for i in range(min(start_index, end_index), max(start_index, end_index) + 1):
    #             checkboxes[i].IsChecked = True
    #     last_clicked_checkbox = sender
    #
    # def on_key_down(self, sender, e):
    #     global shift_pressed
    #     if e.Key == Wpf.Input.Key.LeftShift or e.Key == Wpf.Input.Key.RightShift:
    #         shift_pressed = True
    #
    # def on_key_up(self, sender, e):
    #     global shift_pressed
    #     if e.Key == Wpf.Input.Key.LeftShift or e.Key == Wpf.Input.Key.RightShift:
    #         shift_pressed = False
