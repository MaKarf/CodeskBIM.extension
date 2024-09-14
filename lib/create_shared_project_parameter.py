import os
import sys

from Autodesk.Revit.DB import BuiltInCategory, BuiltInParameterGroup, Transaction

from UI.Popup import Alert
from files_path import version_specific_files_path

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
revit_version = int(app.VersionNumber)
t = Transaction(doc, "Add Parameters")


class SharedParameters:
    """retrieve the existing shared parameter file"""
    existing_sp_file_path = app.SharedParametersFilename

    """set the existing sp file to empty if path does not exist"""
    if app.OpenSharedParameterFile() is None:
        app.SharedParametersFilename = ""
        existing_sp_file_path = ""

    sp_file = None
    sp_groups = None
    # print(sp_groups)
    # print("=" * 100)
    # for spg in sp_groups:
    #     print("SPG: ", spg)
    #
    # print("=" * 100)

    element_category_set = None
    selected_group_report = ""

    def __init__(self):

        """set the shared parameter file to codesk sp file or
           create a new codesk shared parameter if its no longer exist"""
        codesk_sp_file_path = version_specific_files_path.codeskBIM_General_SP_file
        if os.path.exists(codesk_sp_file_path):
            app.SharedParametersFilename = codesk_sp_file_path

        else:
            """recreate new sp file or copy from backup if not exist"""
            self.create_sp()
            app.SharedParametersFilename = codesk_sp_file_path
            # print("SP File Not Found")
            #
            # Alert(title="SP File Error",
            #       header="SP File Not Found",
            #       content="")
            # sys.exit()

        """access shared parameter file"""
        self.sp_file = app.OpenSharedParameterFile()
        self.sp_groups = self.sp_file.Groups
        self.revert_sp_file()

        """temporary set the shared parameter file to codesk's shared parameter file to add the necessary parameters
            and revert the parameter file back in case the user has set his own shared parameter file"""

    def create_category_set(self, built_in_category):
        category = doc.Settings.Categories
        element_category = category.get_Item(built_in_category)

        """do not create a new set to replace the previous set but add up"""
        if self.element_category_set is None:
            self.element_category_set = app.Create.NewCategorySet()

        self.element_category_set.Insert(element_category)
        # print("Category Set: {}".format(self.element_category_set))
        return self.element_category_set

    def create_category_set_and_group(self, group_name, built_in_category):
        category = doc.Settings.Categories
        element_category = category.get_Item(built_in_category)

        """do not create a new set to replace the previous set but add up"""
        if self.element_category_set is None:
            self.element_category_set = app.Create.NewCategorySet()

        self.element_category_set.Insert(element_category)
        # print("Category Set: {}".format(self.element_category_set))

        selected_group = self.sp_groups.get_Item(group_name)
        # print("Selected group: {}".format(selected_group))
        if selected_group is None:
            self.selected_group_report = group_name

        return selected_group

    def add_parameter_from_list(self, group_name, list_of_parameter_names, built_in_category):
        t.Start()
        selected_group = self.create_category_set_and_group(group_name, built_in_category)

        if selected_group:
            for param_def in selected_group.Definitions:

                if param_def.Name in list_of_parameter_names:
                    self.add_parameter(parameter_definition_name=param_def,
                                       parameter_type=BuiltInParameterGroup.PG_TEXT)

        else:
            Alert(title="Parameter Group not Found",
                  header="'{}' Not Found".format(self.selected_group_report),
                  content="Parameter '{}' not found in shared parameter file".format(self.selected_group_report))

        t.Commit()

    def add_parameter(self, parameter_definition_name, parameter_type=BuiltInParameterGroup.PG_TEXT):
        new_instance_binding = app.Create.NewInstanceBinding(self.element_category_set)
        doc.ParameterBindings.Insert(parameter_definition_name, new_instance_binding, parameter_type)

    def add_all_parameters_from_shared_parameter_group(self, group_name, built_in_category):
        t.Start()
        selected_group = self.create_category_set_and_group(group_name, built_in_category)

        if selected_group:
            # print("=" * 100)
            for param_def in selected_group.Definitions:
                # print(param_def)
                # print("Parameter Name: {}".format(param_def.Name))
                self.add_parameter(parameter_definition_name=param_def, parameter_type=BuiltInParameterGroup.PG_TEXT)
        else:
            Alert(title="Parameter Group not Found",
                  header="'{}' Not Found".format(self.selected_group_report),
                  content="Parameter '{}' not found in shared parameter file".format(self.selected_group_report))
        t.Commit()

    def add_parameter_by_name_equality(self, group_name, list_of_parameter_names, built_in_category):
        t.Start()
        selected_group = self.create_category_set_and_group(group_name, built_in_category)

        def add_param(parameter_name):
            if selected_group:
                for param_def in selected_group.Definitions:

                    if parameter_name == param_def.Name:
                        self.add_parameter(parameter_definition_name=param_def,
                                           parameter_type=BuiltInParameterGroup.PG_TEXT)

            else:
                Alert(title="Parameter Group not Found",
                      header="'{}' Not Found".format(self.selected_group_report),
                      content="Parameter '{}' not found in shared parameter file".format(self.selected_group_report))

        map(add_param, list_of_parameter_names)
        t.Commit()

    def add_parameter_by_string_inequality_search(self, group_name, string_to_search, built_in_category):
        t.Start()
        selected_group = self.create_category_set_and_group(group_name, built_in_category)

        if selected_group:
            for param_def in selected_group.Definitions:

                if string_to_search in str(param_def.Name):
                    self.add_parameter(parameter_definition_name=param_def,
                                       parameter_type=BuiltInParameterGroup.PG_TEXT)
        else:
            Alert(title="Parameter not Found",
                  header="'{}' Not Found".format(self.selected_group_report),
                  content="Parameter '{}' not found in shared parameter file".format(self.selected_group_report))

        t.Commit()

    def revert_sp_file(self):
        app.SharedParametersFilename = self.existing_sp_file_path
        # print("Reset SPF to: ", app.SharedParametersFilename)

    def create_sp(self):
        self.create_category_set_and_group("Grids", BuiltInCategory.OST_Sheets)

        parameters_list = ["Locality", "District_Municipality_Metropolis", "Region", "Street Name", "Plot Number"]
        self.add_parameter_from_list(group_name="Project Info",
                                     list_of_parameter_names=parameters_list,
                                     built_in_category=BuiltInCategory.OST_Sheets)

        self.revert_sp_file()
