import clr
from Autodesk.Revit.UI import TaskDialog

from lib.UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

clr.AddReference("System.Windows.Forms")

from System.Windows import RoutedEventHandler

import json
import os

from Autodesk.Revit.DB import BuiltInParameter, Transaction
from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic
from lib.update_projects_data import ProjectData

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView
t = Transaction(doc, "Update project info")


class SetProjectInfo(BaseWPFClass):
    json_file_path = os.path.join(os.path.dirname(__file__), "project_info.json")
    close_mode_value = ""
    """Get the project information element"""
    sheet_info = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()
    project_info = doc.ProjectInformation

    """ setting Built-In_parameters using the get_Parameter method"""
    project_name = project_info.get_Parameter(BuiltInParameter.PROJECT_NAME)
    client_name = project_info.get_Parameter(BuiltInParameter.CLIENT_NAME)
    project_address = project_info.get_Parameter(BuiltInParameter.PROJECT_ADDRESS)
    project_issue_date = project_info.get_Parameter(BuiltInParameter.PROJECT_ISSUE_DATE)

    project_name_text = project_name.AsString()
    client_name_text = client_name.AsString()
    project_address_text = project_address.AsString()
    project_issue_date_text = project_issue_date.AsString()

    # print(project_name_text)
    # print(client_name_text)
    # print(project_address_text)
    # print(project_issue_date_text)

    """get revit file path"""
    revit_file_path = doc.PathName
    """extract only revit file name with file extension"""
    only_rvt_name = revit_file_path.split("\\")[-1]
    """remove the file name from path to get the mother folder instead"""
    project_folder = revit_file_path.replace(only_rvt_name, "")

    project_data_class = ProjectData(doc.Title)
    try:
        # print("##############################################################################3")

        # print("Project Data class: {}\n".format(project_data_class))

        active_project_data_dict = project_data_class.active_project_data_dict
        # print("active_project_data_dict: {}\n".format(active_project_data_dict))

        project_data_path = project_data_class.path
        # print("project_data_path: {}\n".format(project_data_path))

        data = active_project_data_dict["project_info"]
        # print("project_info_data_dict: {}\n".format(data))
        # print("##############################################################################3")
    except Exception as e:
        TaskDialog.Show(str(e), "Unknown Error - Please retry")
        """ rollback all changes"""
        project_data_class.rollback_changes()

    def __init__(self, xaml_file_name, parser_class=None):
        BaseWPFClass.__init__(self, xaml_file_name)

        """Find the "button_run" button by its name"""
        button_run = self.Window.FindName("button_run")

        """Attach the event handler to the button's "Click" event"""
        button_run.Click += RoutedEventHandler(self.button_run_func)

        """ get rename grids operational class instance"""
        self.cls = parser_class

        self.set_text("UI_project_name")
        self.set_text("UI_client_name")
        self.set_text("UI_locality")
        self.set_text("UI_district")
        self.set_text("UI_region")
        self.set_text("UI_plot")
        self.set_text("UI_street")
        self.set_text("UI_date")
        self.set_text("UI_designed_by")
        self.set_text("UI_drawn_by")
        self.set_text("UI_checked_by")

        self.ShowDialog()

    def get_text(self, object_name):
        return self.Window.FindName(object_name).Text

    def set_text(self, object_name):
        self.Window.FindName(object_name).Text = self.data[object_name.replace("UI_", "")]

    def remove_non_ascii_chars(self, object_name):
        return self.Window.FindName(object_name).Text.replace('\xa0', ' ')

    def button_run_func(self, sender, e):

        # self.project_name = self.Window.FindName("UI_project_name").Text
        # self.project_path = self.Window.FindName("UI_project_path").Text
        # self.make_path_default = self.Window.FindName("UI_set_default").IsChecked
        # self.Close()
        # self.close_mode_value = "indirect"

        """ replace unknown space characters with a valid space character in the file name invalid characters are
        occurred when the revit name is copied and pasted from somewhere
        _name.replace('\xa0', ' ') """

        # self.button_close("a", "c")
        self.Close()
        self.close_mode_value = "indirect"

        project_name = self.remove_non_ascii_chars("UI_project_name")
        client_name = self.remove_non_ascii_chars("UI_client_name")
        locality = self.remove_non_ascii_chars("UI_locality")
        district = self.remove_non_ascii_chars("UI_district")
        region = self.remove_non_ascii_chars("UI_region")
        plot = self.remove_non_ascii_chars("UI_plot")
        street = self.remove_non_ascii_chars("UI_street")

        date = self.remove_non_ascii_chars("UI_date")
        designed_by = self.remove_non_ascii_chars("UI_designed_by")
        drawn_by = self.remove_non_ascii_chars("UI_drawn_by")
        checked_by = self.remove_non_ascii_chars("UI_checked_by")

        try:

            location = "{0}, {1} - {2}".format(locality, district, region)

            if plot == "" and street == "":
                area = ""

            elif plot == "" and street != "":
                area = ""

            elif plot != "" and street == "":
                area = "ON {}, ".format(plot)
            else:
                area = "ON {0}, {1} ".format(street, plot)

            project_title = "PROPOSED {0} TO BE BUILT {1}AT {2}".format(project_name, area, location).upper()

            # print("\n")
            # # print(location)
            # print(project_title)

            """ #################################################################################################"""
            """ #################################################################################################"""

            """Get the parameter definition of the project parameter you want to set"""

            """Get the project information element"""
            sheet_info = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()
            project_info = doc.ProjectInformation

            t.Start()
            """ setting Built-In_parameters using the get_Parameter method"""
            project_info.get_Parameter(BuiltInParameter.PROJECT_NAME).Set(project_title)
            project_info.get_Parameter(BuiltInParameter.CLIENT_NAME).Set(client_name)
            project_info.get_Parameter(BuiltInParameter.PROJECT_ADDRESS).Set(location)
            project_info.get_Parameter(BuiltInParameter.PROJECT_ISSUE_DATE).Set(date)

            """ setting shared parameters using the LookupParameter method"""
            for i in sheet_info:
                i.get_Parameter(BuiltInParameter.SHEET_DESIGNED_BY).Set(designed_by)
                i.get_Parameter(BuiltInParameter.SHEET_DRAWN_BY).Set(drawn_by)
                i.get_Parameter(BuiltInParameter.SHEET_CHECKED_BY).Set(checked_by)

                """=========================================================================="""
                """parameters for the shared parameters of the site plan"""
                try:
                    i.LookupParameter("Project Name").Set(project_name)
                    i.LookupParameter("Locality").Set(locality)
                    i.LookupParameter("District_Municipality_Metropolis").Set(district)
                    i.LookupParameter("Region").Set(region)
                    i.LookupParameter("Plot Number").Set(plot)
                    i.LookupParameter("Street Name").Set(street)

                except AttributeError:
                    """parameter not found"""
                    # print("parameter not found", i)
                    pass
                """=========================================================================="""

            t.Commit()
            """ #################################################################################################"""
            """ #################################################################################################"""

        except KeyError:
            pass
        """update json files with new project information"""
        self.data["project_name"] = project_name
        self.data["client_name"] = client_name
        self.data["locality"] = locality
        self.data["district"] = district
        self.data["region"] = region
        self.data["plot"] = plot
        self.data["street"] = street
        self.data["date"] = date
        self.data["designed_by"] = designed_by
        self.data["drawn_by"] = drawn_by
        self.data["checked_by"] = checked_by

        """update json file with new option"""
        self.project_data_class.existing_projects[self.project_data_class.revit_file_name]["project_info"] = self.data
        with open(self.project_data_path, "w") as f:
            json.dump({"documents": self.project_data_class.existing_projects}, f, indent=4)
