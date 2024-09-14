import clr

from SortNatural import real_sorting
from UI.xamlFiles.CheckboxSelection import CheckboxSelection
from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass
from UI.xamlFiles.forms import ListItem

clr.AddReference("System.Windows.Forms")
clr.AddReference("System")
from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler
from System.Windows import Visibility, Thickness
from System.Windows.Controls import CheckBox, StackPanel, Orientation, SelectionChangedEventHandler

from collections import defaultdict

from Autodesk.Revit.DB import FilteredElementCollector, View, ElementTransformUtils, CopyPasteOptions, ElementId, \
    Transform, TransactionGroup, Transaction

from UI.Popup import Alert
from codeskResource.codesk_transaction import codesk_transaction as transaction

from System.Collections.Generic import List
from System.Windows.Controls import ComboBoxItem

"""GLOBAL VARIABLES"""
app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView


class TransferViewTemplate(BaseWPFClass):

    def __init__(self):
        BaseWPFClass.__init__(self, xaml_file_name="TransferViewTemplate.xaml")
        self.operation_type = "Transfer"

        self.opened_docs = [i for i in app.Documents]

        self.active_doc = self.get_active_doc()
        self.inactive_projects_dict = []
        self.update_project_data()

        self.select_multiple = True
        self.list_view_templates = None

        self.selected_items = []
        self.copy_from_doc = None
        self.copy_to_doc = doc

        self.indirect_selection = None

        """Find elements by their name"""
        self.check_override = self.Window.FindName("check_override")
        self.dropdown_label = self.Window.FindName("dropdown_label")
        self.UI_CopyFrom = self.Window.FindName("UI_CopyFrom")
        self.UI_ViewTemplates_ListBox = self.Window.FindName("UI_ViewTemplates_ListBox")

        self.transfer_option = self.Window.FindName("transfer_option")
        self.delete_option = self.Window.FindName("delete_option")

        self.textbox_filter = self.Window.FindName("textbox_filter")
        self.check_all = self.Window.FindName("check_all")
        self.check_none = self.Window.FindName("check_none")
        self.finish_button = self.Window.FindName("finish_button")

        """Attach the event handler to the button's "Click" event"""
        self.UI_CopyFrom.SelectionChanged += SelectionChangedEventHandler(self.ui_combo_box_changed)

        self.check_all.Click += RoutedEventHandler(self.button_select_all)
        self.check_none.Click += RoutedEventHandler(self.button_select_none)
        self.textbox_filter.KeyUp += KeyEventHandler(self.text_filter_updated)
        self.finish_button.Click += RoutedEventHandler(self.ui_button_run)

        self.transfer_option.Checked += RoutedEventHandler(self.transfer_operation)
        self.transfer_option.Unchecked += RoutedEventHandler(self.transfer_operation)

        self.delete_option.Checked += RoutedEventHandler(self.delete_operation)
        self.delete_option.Unchecked += RoutedEventHandler(self.delete_operation)

        if len(self.inactive_projects_dict) == 0:
            Alert(title="Alert", header="Only one project is opened",
                  content="You need to open at least two projects to complete this operation")

        elif len(self.inactive_projects_dict) == 1:
            self.copy_from_doc = self.inactive_projects_dict.pop().get("element")

            ui = CheckboxSelection(items=self.get_view_template__dict_list())

            ui.ShowDialog()
            selected_templates = ui.selected_items

            if len(selected_templates) != 0:
                self.indirect_selection = selected_templates
                self.ui_button_run("sender", "e")

        else:
            self.projects_dict_data = real_sorting(list_to_be_sorted=self.inactive_projects_dict, dict_key="name")
            """update selection boxes with appropriate data source"""
            self.add_inactive_projects_combo_box_items()

            self.ShowDialog()

    def __iter__(self):
        """Return selected items."""
        return iter(self.selected_items)

    def get_active_doc(self):
        return [d for d in self.opened_docs if d.ActiveView].pop()

    def get_view_template__dict_list(self):
        """Update ViewTemplates ListBox"""
        view_templates = [v for v in FilteredElementCollector(self.copy_from_doc).OfClass(View).ToElements() if
                          v.IsTemplate]

        dict_view_templates = real_sorting(
            list_to_be_sorted=[{"name": v.Name, "element": v} for v in view_templates], dict_key="name")
        return dict_view_templates

    def text_filter_updated(self, sender, e):
        """Function to filter items in the main_ListBox."""
        filtered_list_of_items = List[type(ListItem(cls=self))]()
        filter_keyword = self.textbox_filter.Text

        """ RESTORE ORIGINAL LIST"""
        if not filter_keyword:
            self.UI_ViewTemplates_ListBox.ItemsSource = self.list_view_templates
            return

        """ FILTER ITEMS"""
        for item in self.list_view_templates:
            if filter_keyword.lower() in item.check_box.Content.lower():
                filtered_list_of_items.Add(item)

        """ UPDATE LIST OF ITEMS"""
        self.UI_ViewTemplates_ListBox.ItemsSource = filtered_list_of_items

    def select_mode(self, mode):
        """Helper function for following buttons:
        - button_select_all
        - button_select_none"""

        list_of_items = List[type(ListItem(cls=self))]()
        checked = True if mode == 'all' else False
        try:
            for item in self.UI_ViewTemplates_ListBox.ItemsSource:
                item.check_box.IsChecked = checked
                list_of_items.Add(item)

            self.UI_ViewTemplates_ListBox.ItemsSource = list_of_items
        except Exception as ex:
            print(ex)

    def button_select_all(self, sender, e):
        """ """
        self.select_mode(mode='all')

    def button_select_none(self, sender, e):
        """ """
        self.select_mode(mode='none')

    def checker(self, sender):
        check = sender.IsChecked
        check_inverse = False if check is True else True

        for item in self.UI_ViewTemplates_ListBox.ItemsSource:

            if item.check_box.Content == sender.Content:
                if not self.select_multiple:
                    self.selected_items = []
                    self.selected_items.append(item.element)
                else:
                    self.selected_items.append(item.element)
            else:
                if not self.select_multiple:
                    item.check_box.IsChecked = check_inverse

    def add_inactive_projects_combo_box_items(self):
        """Function to Add Project Titles to ComboBoxes on the start of the GUI."""

        for project_item in self.projects_dict_data:
            item = ComboBoxItem()
            item.Content = project_item.get("name")
            item.IsSelected = False
            self.UI_CopyFrom.Items.Add(item)

        self.UI_CopyFrom.SelectedIndex = 0
        # self.selected_project = self.UI_CopyFrom.SelectedItem

    def ui_combo_box_changed(self, sender=None, e=None):
        # print sender
        self.update_project_data()
        """deselect everything in the previous project before setting to another project
        to avoid unwanted selection"""

        def get_selected_project_name(element):
            for combo_box_item in element.Items:
                if combo_box_item.IsSelected:
                    return combo_box_item.Content

        if sender is not None:
            copy_from_doc = [project_item.get("element") for project_item in self.projects_dict_data if
                             project_item.get("name") == get_selected_project_name(sender)]
            try:
                self.copy_from_doc = copy_from_doc.pop()
            except IndexError:
                """ignore this error"""
                pass

        try:
            list_view_templates = List[type(ListItem(cls=self))]()
            vts = self.get_view_template__dict_list()

            if vts is not None:
                for item in vts:
                    list_view_templates.Add(ListItem(cls=self, name=item.get("name"), element=item.get("element"),
                                                     select_multiple=self.select_multiple))

            self.list_view_templates = list_view_templates
            self.UI_ViewTemplates_ListBox.ItemsSource = list_view_templates

        except IndexError:
            """print("Project selection Error")"""

    def remove_view_template_same_name(self, selected_view_templates_names):
        """This function will scan Project where ViewTemplates is being copied to for ViewTemplates with the same name.
        If there are any matches, it will return a dictionary of a ViewTemplate name and views it is assigned to
        e.g. {ViewTemplate.Name : list(View1,View2)}
        And then it will delete it from the project."""

        """CONTAINER"""
        dict_used_view_templates_doc_to = defaultdict(list)

        """CHECK IF VIEW TEMPLATES EXISTS AND WHETHER TO OVERRIDE THEM OR NOT"""
        view_templates_doc_to = [v for v in FilteredElementCollector(self.copy_to_doc).OfClass(View).ToElements() if
                                 v.IsTemplate]
        views_doc_to = [v for v in FilteredElementCollector(self.copy_to_doc).OfClass(View).ToElements() if
                        not v.IsTemplate]

        """DELETE VIEW TEMPLATES WITH SAME NAME + MAKE DICT"""
        for vt in view_templates_doc_to:
            # CHECK IF SAME NAME EXISTS
            if vt.Name not in selected_view_templates_names:
                continue

            """FIND VIEWS WHERE VIEW TEMPLATE USED"""
            for v in views_doc_to:
                vt_id = v.ViewTemplateId
                if vt_id and vt_id != ElementId(-1):
                    vt_name = self.copy_to_doc.GetElement(vt_id).Name
                    if vt_name in selected_view_templates_names:
                        dict_used_view_templates_doc_to[vt_name].append(v.Id)

        """DELETE SIMILAR VIEW TEMPLATES"""
        for vt in view_templates_doc_to:
            if vt.Name in selected_view_templates_names:
                if vt.Name not in dict_used_view_templates_doc_to:
                    dict_used_view_templates_doc_to[vt.Name] = []
                self.copy_to_doc.Delete(vt.Id)

        return dict_used_view_templates_doc_to

    def assign_view_templates(self, dict_deleted_view_templates_doc_to):
        for vt_name, list_view_ids in dict_deleted_view_templates_doc_to.items():
            """FIND VIEW TEMPLATE WITH SAME NAME"""
            view_templates_doc_to = [v for v in FilteredElementCollector(self.copy_to_doc).OfClass(View).ToElements() if
                                     v.IsTemplate]
            new_vt = [v for v in view_templates_doc_to if v.Name == vt_name][0]

            """SET VIEW TEMPLATE TO VIEWS"""
            for view_id in list_view_ids:
                view = self.copy_to_doc.GetElement(view_id)
                view.ViewTemplateId = new_vt.Id

    def delete_view_template(self):
        """SELECTED VIEW TEMPLATES"""
        ids = List[ElementId]()
        # try:
        selected_view_templates = [ids.Add(item.element.Id) for item in self.UI_ViewTemplates_ListBox.ItemsSource if
                                   item.check_box.IsChecked]

        with Transaction(self.copy_from_doc, "Delete View Templates") as t:
            t.Start()

            self.copy_from_doc.Delete(ids)

            """refresh the combobox"""
            self.ui_combo_box_changed(sender=self.UI_CopyFrom, e=None)
            t.Commit()
        # except:
        #     pass

    def transfer_view_templates(self):
        """Reset Filter"""
        self.textbox_filter.Text = ''

        """SELECTED VIEW TEMPLATES"""

        """check if the view templates were selected by the CheckboxSelection UI or the TransferViewTemplate UI"""
        if self.indirect_selection is None:
            selected_view_templates = [item.element for item in self.UI_ViewTemplates_ListBox.ItemsSource if
                                       item.check_box.IsChecked]
        else:
            selected_view_templates = self.indirect_selection

        selected_view_templates_ids = [vt.Id for vt in selected_view_templates]
        selected_view_templates_names = [vt.Name for vt in selected_view_templates]

        """CHECK IF VIEW TEMPLATE SELECTED"""
        if not selected_view_templates_ids:
            Alert(title="Alert", header="No ViewTemplates selected.", content="Please Try Again")

        with TransactionGroup(doc, "Transfer view template") as tg:
            tg.Start()

            """REMOVE VIEW TEMPLATES WITH SAME NAME AS SELECTED"""
            dict_deleted_view_templates_doc_to = {}
            if self.check_override.IsChecked:
                with transaction(self.copy_to_doc, 'Remove Same ViewTemplates'):
                    dict_deleted_view_templates_doc_to = self.remove_view_template_same_name(
                        selected_view_templates_names)

            """COPY VIEW TEMPLATES"""
            list_selected_view_templates = List[ElementId](selected_view_templates_ids)
            copy_opts = CopyPasteOptions()
            with transaction(self.copy_to_doc, 'Copy ViewTemplates'):
                ElementTransformUtils.CopyElements(self.copy_from_doc,
                                                   list_selected_view_templates,
                                                   self.copy_to_doc,
                                                   Transform.Identity,
                                                   copy_opts)

            """ASSIGN VIEW TEMPLATE TO VIEWS THAT HAD SAME VIEW TEMPLATE NAME"""
            if self.check_override.IsChecked:
                with transaction(self.copy_to_doc, 'Assign ViewTemplates'):
                    self.assign_view_templates(dict_deleted_view_templates_doc_to)

            tg.Assimilate()

        """REPORT"""
        body_message = ""
        for vt in selected_view_templates:
            if vt.Name in dict_deleted_view_templates_doc_to.keys():
                # print("[Updated    ] - {}".format(vt.Name))
                msg = "[Updated] - {}".format(vt.Name)
                body_message += "{}\n".format(msg)
            else:
                # print('[Added New] - {}'.format(vt.Name))
                msg = '[Added New] - {}'.format(vt.Name)
                body_message += "{}\n".format(msg)

        # print('-' * 50)
        body_message += "{}\n".format('-' * 50)
        was_were = 'ViewTemplates were' if len(selected_view_templates) > 1 else 'ViewTemplate was'
        # print('Script is complete.\n {} {} Transferred.'.format(len(selected_view_templates), was_were))
        msg = '{} {} Transferred.'.format(len(selected_view_templates), was_were)

        body_message += "{}\n".format(msg)

        Alert(title="Results", header="View Templates Successfully Transferred", content=body_message)

    def transfer_operation(self, sender, e):
        if sender.IsChecked:
            self.delete_option.IsChecked = False
            self.check_override.Visibility = Visibility.Visible
            self.finish_button.Content = "Transfer ViewTemplates"
            self.operation_type = "Transfer"
        else:
            self.delete_option.IsChecked = True
            self.check_override.Visibility = Visibility.Collapsed
            self.finish_button.Content = "Delete ViewTemplates"
            self.operation_type = "Delete"

            self.update_project_data()

        """update selection boxes with appropriate data source"""
        self.update_project_combo_box()

    def delete_operation(self, sender, e):
        if sender.IsChecked:
            self.transfer_option.IsChecked = False
            self.check_override.Visibility = Visibility.Collapsed
            self.finish_button.Content = "Delete ViewTemplates"
            self.operation_type = "Delete"
        else:
            self.transfer_option.IsChecked = True
            self.check_override.Visibility = Visibility.Visible
            self.finish_button.Content = "Transfer ViewTemplates"
            self.operation_type = "Transfer"
        self.update_project_combo_box()

    def update_project_combo_box(self):
        self.projects_dict_data = real_sorting(list_to_be_sorted=self.inactive_projects_dict, dict_key="name")
        """update selection boxes with appropriate data source"""
        self.UI_CopyFrom.Items.Clear()
        self.add_inactive_projects_combo_box_items()

    def update_project_data(self):
        if self.operation_type == "Delete":
            self.inactive_projects_dict = [{"name": d.Title, "element": d} for d in self.opened_docs
                                           if not d.IsFamilyDocument
                                           and d.Title != "CodeskBIM Revit Plugin Reference Project"]

        else:
            self.inactive_projects_dict = [{"name": d.Title, "element": d} for d in self.opened_docs
                                           if not d.IsFamilyDocument
                                           and not d.ActiveView]

    def ui_button_run(self, sender, e):
        if self.operation_type == "Delete":
            self.delete_view_template()
        else:
            self.transfer_view_templates()
