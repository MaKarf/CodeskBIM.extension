import clr

from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from UI.xamlFiles.forms import ListItem

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")

from System.Collections.Generic import List
from System.Windows.Controls import SelectionChangedEventHandler, ComboBoxItem
from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler

from Autodesk.Revit import DB
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic
from Autodesk.Revit.DB import Transaction

from SortNatural import real_sorting
from unitConvert import mm2ft

from UI.Popup import Alert

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Place view")
active_view = ui_doc.ActiveView


class PlaceViewsOnSheets(BaseWPFClass):

    def __init__(self, sheets):
        BaseWPFClass.__init__(self, xaml_file_name="PlaceViewsOnSheets.xaml")

        self.sheet_list = sheets

        self.lock = False

        self.placement_array = "horizontal"

        self.select_multiple = True
        self.active_listbox = None
        self.selected_views = []
        self.selected_sheets = []
        self.active_listbox_data = []
        self.views_listbox_data = []

        self.data = self.prepare_data()
        self.sheets_data = self.data.get("sheets")
        self.view_type_data = self.data.get("views")

        """Find the "button_run" button by its name"""
        self.view_type_filter = self.Window.FindName("view_type_filter")
        self.report_selected = self.Window.FindName("report_selected")

        self.vertical_array_checkbox = self.Window.FindName("vertical_array_checkbox")
        self.horizontal_array = self.Window.FindName("horizontal_array_checkbox")

        self.views_list_box_panel = self.Window.FindName("views_list_box_panel")
        self.views_list_box = self.Window.FindName("views_list_box")

        self.sheets_list_box_panel = self.Window.FindName("sheets_list_box_panel")
        self.sheets_list_box = self.Window.FindName("sheets_list_box")

        self.views_selector = self.Window.FindName("views_selector")
        self.sheets_selector = self.Window.FindName("sheets_selector")

        self.search = self.Window.FindName("search")
        self.button_run = self.Window.FindName("button_run")

        self.select_all = self.Window.FindName("select_all")
        self.select_none = self.Window.FindName("select_none")

        self.run_button = self.Window.FindName("run_button")

        """Attach the event handler to the button's "Click" event"""
        self.view_type_filter.SelectionChanged += SelectionChangedEventHandler(self.filter_by_view_type)

        self.views_selector.Checked += RoutedEventHandler(self.select_views)
        self.views_selector.Unchecked += RoutedEventHandler(self.select_views)

        self.vertical_array_checkbox.Checked += RoutedEventHandler(self.set_vertical_array)
        self.vertical_array_checkbox.Unchecked += RoutedEventHandler(self.set_vertical_array)

        self.horizontal_array_checkbox.Checked += RoutedEventHandler(self.set_horizontal_array)
        self.horizontal_array_checkbox.Unchecked += RoutedEventHandler(self.set_horizontal_array)

        self.sheets_selector.Checked += RoutedEventHandler(self.select_sheets)
        self.sheets_selector.Unchecked += RoutedEventHandler(self.select_sheets)

        self.search.KeyUp += KeyEventHandler(self.search_filter)
        self.select_all.Click += RoutedEventHandler(self.button_select_all)
        self.select_none.Click += RoutedEventHandler(self.button_select_none)

        self.Window.KeyDown += self.search_in_textbox

        """set the window size"""
        self.focused_width = (self.Window.Width - 50) * 0.7
        self.unfocused_width = (self.Window.Width - 50) * 0.3

        """set items sources"""
        self.view_type_combobox_data = self.update_views_data()
        self.view_type_filter.SelectedIndex = 0

        self.sheets_listbox_data = self.generate_list_items(self.sheets_data)
        self.sheets_list_box.ItemsSource = self.sheets_listbox_data

        """init the view window to display"""
        self.views_selector.IsChecked = True

    @staticmethod
    def get_views_by_type(view_type):
        vl = [view for view in Fec(doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
              if view.ViewType == view_type and not view.IsTemplate and view.Name]

        list_to_sort = [{"name": str(v.Name), "element": v, } for v in vl if v is not None]
        res = real_sorting(list_to_be_sorted=list_to_sort,
                           dict_key="name")
        return res

    def prepare_data(self):
        """##############################################################################################"""
        elevations = self.get_views_by_type(DB.ViewType.Elevation)
        sections = self.get_views_by_type(DB.ViewType.Section)
        floor_plan = self.get_views_by_type(DB.ViewType.FloorPlan)
        ceiling_plan = self.get_views_by_type(DB.ViewType.CeilingPlan)
        threeDs = self.get_views_by_type(DB.ViewType.ThreeD)
        drafting_view = self.get_views_by_type(DB.ViewType.DraftingView)

        grouped_views = [elevations, sections, floor_plan, ceiling_plan, drafting_view, threeDs]

        temp_all_views = []

        for sub_views in grouped_views:
            try:
                for ind_views in sub_views:
                    temp_all_views.append(ind_views)
            except:
                """exception for empty view types"""
                pass

        ordered_grouped_views = []
        for gp in grouped_views:
            try:
                view_typ = gp[0].get("element").ViewType
                ordered_grouped_views.append({"name": str(view_typ), "element": gp})
            except:
                """exception for empty view types"""
                pass

        ordered_grouped_views.append({"name": "All Views", "element": temp_all_views})

        sheets = [{"name": i.Name, "element": i} for i in self.sheet_list]

        return {"views": ordered_grouped_views, "sheets": sheets}

    def set_vertical_array(self, sender, e):
        if sender.IsChecked:
            self.horizontal_array_checkbox.IsChecked = False
            self.placement_array = "vertical"
        else:
            self.horizontal_array_checkbox.IsChecked = True
            self.placement_array = "horizontal"

    def set_horizontal_array(self, sender, e):
        if sender.IsChecked:
            self.vertical_array_checkbox.IsChecked = False
            self.placement_array = "horizontal"
        else:
            self.vertical_array_checkbox.IsChecked = True
            self.placement_array = "vertical"

    def update_views_data(self):
        views_combobox_data = List[type(ComboBoxItem())]()

        for project_item in self.view_type_data:
            combo_box_item = ComboBoxItem()
            combo_box_item.Content = project_item.get("name")
            views_combobox_data.Add(combo_box_item)

            # print project_item
            # print "__________________________________"
            # print "__________________________________"

        self.view_type_filter.ItemsSource = views_combobox_data

        return views_combobox_data

    def generate_list_items(self, data_items):
        list_of_items = List[type(ListItem(cls=self))]()

        if data_items is not None:
            for item in data_items:
                list_of_items.Add(ListItem(cls=self, name=item.get("name"), element=item.get("element"),
                                           select_multiple=True))
            return list_of_items
        return None

    def select_views(self, sender, e):

        if self.views_selector.IsChecked:
            self.sheets_selector.IsChecked = False

            """switch an active listbox data to views data, and set search target to views data"""
            self.active_listbox = self.views_list_box
            self.active_listbox_data = self.views_listbox_data

            self.disable_views_checkboxes(False)

            self.views_list_box_panel.Width = self.focused_width
            self.sheets_list_box_panel.Width = self.unfocused_width
        else:
            self.sheets_selector.IsChecked = True
            self.views_list_box_panel.Width = self.unfocused_width
            self.sheets_list_box_panel.Width = self.focused_width

            """switch an active listbox data to, and set search target to sheets data"""
            self.active_listbox = self.sheets_list_box
            self.active_listbox_data = self.sheets_listbox_data
            self.disable_views_checkboxes(True)

    def select_sheets(self, sender, e):
        if self.sheets_selector.IsChecked:

            """switch an active listbox data to, and set search target to sheets data"""
            self.active_listbox = self.sheets_list_box
            self.active_listbox_data = self.sheets_listbox_data

            self.disable_views_checkboxes(True)

            self.views_selector.IsChecked = False
            self.views_list_box_panel.Width = self.unfocused_width
            self.sheets_list_box_panel.Width = self.focused_width
        else:
            self.views_selector.IsChecked = True

            """switch an active listbox data to views data, and set search target to views data"""
            self.active_listbox = self.views_list_box
            self.active_listbox_data = self.views_listbox_data

            self.disable_views_checkboxes(False)

            self.views_list_box_panel.Width = self.focused_width
            self.sheets_list_box_panel.Width = self.unfocused_width

    def disable_views_checkboxes(self, boolean):

        disable_views = True if boolean else False

        self.view_type_filter.IsEnabled = False if boolean else True
        try:
            for view_item in self.views_list_box.ItemsSource:
                view_item.IsEnabled = not disable_views

            for sheet_item in self.sheets_list_box.ItemsSource:
                sheet_item.IsEnabled = disable_views
        except:
            pass

    def filter_by_view_type(self, sender, e):
        sel = sender.SelectedItem.Content

        """switch an active listbox data to selected sheet type data, and set search target to views data"""
        data = [dt.get("element") for dt in self.view_type_data if dt.get("name") == sel]
        try:
            self.views_listbox_data = self.generate_list_items(data.pop())
            self.views_list_box.ItemsSource = self.views_listbox_data
            self.active_listbox_data = self.views_listbox_data
        except:
            pass

    def search_filter(self, sender, e):
        """Function to filter items in the main_ListBox."""
        filtered_list_of_items = List[type(ListItem(cls=self))]()
        textbox_text = self.search.Text
        # print self.search.Text

        """ RESTORE ORIGINAL LIST"""
        if textbox_text == "":
            self.active_listbox.ItemsSource = self.active_listbox_data
            return

        """ FILTER ITEMS"""
        for item in self.active_listbox_data:

            if textbox_text.lower() in item.check_box.Content.lower():
                filtered_list_of_items.Add(item)
                # print item.check_box.Content

        """ UPDATE LIST OF ITEMS WITH SEARCHED NAME"""
        self.active_listbox.ItemsSource = filtered_list_of_items

    def checker(self, sender):
        # print("PRINT TAG", sender.Tag)
        check = sender.IsChecked
        # print(check)
        check_inverse = False if check is True else True

        for item in self.active_listbox.ItemsSource:

            if item.check_box.Tag == sender.Tag:

                if self.select_multiple:
                    if self.active_listbox == self.views_list_box:

                        if item.element in self.selected_views:
                            if not check:
                                self.selected_views.remove(item.element)
                        else:
                            if check:
                                self.selected_views.append(item.element)

                    else:
                        if item.element in self.selected_sheets:
                            if not check:
                                self.selected_sheets.remove(item.element)
                        else:
                            if check:
                                self.selected_sheets.append(item.element)

                else:
                    if self.active_listbox == self.views_list_box:
                        if item.element in self.selected_views:
                            if not check:
                                self.views_list_box = []
                            else:
                                self.selected_views = []
                                self.selected_views.append(item.element)

                    else:
                        if item.element in self.selected_sheets:
                            if not check:
                                self.sheets_list_box = []
                            else:
                                self.selected_sheets = []
                                self.selected_sheets.append(item.element)


            else:
                if not self.select_multiple:
                    item.check_box.IsChecked = check_inverse

    def select_mode(self, mode):
        """Helper function for following buttons:
        - button_select_all
        - button_select_none"""

        list_of_items = List[type(ListItem(cls=self))]()
        checked = True if mode == 'all' else False
        for item in self.active_listbox.ItemsSource:
            item.check_box.IsChecked = checked
            list_of_items.Add(item)

        """update the selected elements list"""

        if self.active_listbox == self.views_list_box:
            self.selected_views = []  # """empty the list for further operation"""
            [self.selected_views.append(item.element) for item in self.active_listbox.ItemsSource if mode == 'all']

        else:
            self.selected_sheets = []  # """empty the list for further operation"""
            [self.selected_sheets.append(item.element) for item in self.active_listbox.ItemsSource if mode == 'all']

        self.active_listbox.ItemsSource = list_of_items

    def button_select_all(self, sender, e):
        """ """
        self.select_mode(mode='all')

    def button_select_none(self, sender, e):
        """ """
        self.select_mode(mode='none')

    def search_in_textbox(self, sender, e):
        # if str(e.Key) != "Escape" or str(e.Key) != "Shift":
        #     # print("typed", e.Key)
        #     self.search.Text += str(e.Key)
        pass

    def place_views(self, sender, e):
        if len(self.selected_sheets) < 1:
            Alert(header="Select Sheet(s)", content="")

        elif len(self.selected_views) < 1:
            Alert(header="Select a View", content="")

        else:
            SelectedViewsAndTBlocks(self).place_views_on_sheet()


class SelectedViewsAndTBlocks:

    def __init__(self, ui_class_ref):

        self.lock = ui_class_ref.lock

        if not self.lock:
            self.selected_views = ui_class_ref.selected_views
            self.selected_sheets = ui_class_ref.selected_sheets

            self.sheet = self.selected_sheets.pop()
            self.array_type = ui_class_ref.placement_array

            dependants = self.sheet.GetDependentElements(None)

            title_block = [doc.GetElement(i) for i in dependants if type(doc.GetElement(i)) == DB.FamilyInstance and
                           doc.GetElement(i).Category.Name == "Title Blocks"].pop()
            self.tt_bb = title_block.get_BoundingBox(self.sheet)

            self.title_block_height = self.tt_bb.Max.Y - self.tt_bb.Min.Y
            self.title_block_width = self.tt_bb.Max.X - self.tt_bb.Min.X

            """process"""
            num_of_views = len(self.selected_views)

            self.title_block_x_pos = self.tt_bb.Min.X
            self.title_block_allowable_width = self.title_block_width * 0.75
            self.horizontal_limit = self.title_block_x_pos + self.title_block_allowable_width

            self.viewport_allocated_width = self.title_block_allowable_width / num_of_views
            self.viewport_allocated_height = self.title_block_height / num_of_views

    def horizontal_array(self):
        for view in self.selected_views:
            counter = self.selected_views.index(view)

            horizontal_offset = mm2ft(10)
            half_viewport_x_offset = self.viewport_allocated_width / 2

            viewport_x_pos = self.title_block_x_pos + (
                    counter * self.viewport_allocated_width) + half_viewport_x_offset + horizontal_offset

            viewport_y_pos = self.title_block_height / 2

            viewport_location = DB.XYZ(viewport_x_pos, viewport_y_pos, 0)

            if not view.LookupParameter("Sheet Number").AsElementId():
                DB.Viewport.Create(doc, self.sheet.Id, view.Id, viewport_location)

    def vertical_array(self):
        for view in self.selected_views:
            counter = self.selected_views.index(view)
            title_block_y_pos = self.tt_bb.Min.Y
            vertical_offset = mm2ft(10)
            half_viewport_y_offset = self.viewport_allocated_height / 2

            viewport_x_pos = self.title_block_width / 2
            viewport_y_pos = title_block_y_pos + (
                    counter * self.viewport_allocated_height) + half_viewport_y_offset + vertical_offset

            viewport_location = DB.XYZ(viewport_x_pos, viewport_y_pos, 0)

            DB.Viewport.Create(doc, self.sheet.Id, view.Id, viewport_location)

    def place_views_on_sheet(self):
        if not self.lock:
            t.Start()
            if self.array_type == "horizontal":
                self.horizontal_array()
            else:
                self.vertical_array()
            t.Commit()
