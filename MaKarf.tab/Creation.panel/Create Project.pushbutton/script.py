import os

from Autodesk.Revit.UI import UIApplication, TaskDialog

from UI.xamlFiles.CreateNewProject import CreateProject

app = __revit__.Application
uiApp = UIApplication(app)
PATH_SCRIPT = os.path.dirname(__file__)

global_revit_file_path = ""


class CreateNewProject:
    default_project_folder = os.path.join(r"C:", r"{}\Documents".format(os.environ['HOMEPATH']))
    chosen_default_project_folder = ""
    project_name = ""
    revit_file_path = None

    def __init__(self):
        self.path_file_name = "default_path.txt"
        path = r"C:\ProgramData\Autodesk\Codesk\Makarf Add-in\docs"

        self.full_path = r"C:\ProgramData\Autodesk\Codesk\Makarf Add-in\docs\{}".format(self.path_file_name)
        try:
            if self.path_file_name in os.listdir(path):
                # print("yes")
                self.default_project_folder = open(self.full_path, "r").read()
                # print(self.default_project_folder)

        except:
            # print("no")
            os.makedirs(path)
            with open(self.full_path, "w") as pt:
                pt.write(self.default_project_folder)
                pt.close()

    def create_revit_project_directory(self):
        """ list of folders to be created"""
        rvt = "RVT"
        pdf = "PDF"
        exports = "Exports"
        docs = "Docs"
        lumion = "Lumion"
        base_files = "Base files"

        folders = [rvt, pdf, exports, docs, lumion, base_files]

        """#########################################################################################################"""
        """call the UI class and parse in the default path to be displayed"""
        UI_results = CreateProject(xaml_file_name="CreateNewProject.xaml", default_path=self.default_project_folder)
        """#########################################################################################################"""

        """if the window wasn't closed by the close button"""
        if UI_results.close_mode_value == "indirect":
            if UI_results.project_name != "":
                self.project_name = UI_results.project_name

                if UI_results.make_path_default:
                    with open(self.full_path, "w") as ps:
                        ps.write(UI_results.project_path)
                        ps.close()
                    self.default_project_folder = open(self.full_path, "r").read()
                    self.chosen_default_project_folder = self.default_project_folder
                else:
                    self.chosen_default_project_folder = UI_results.project_path

                """check if the already folder exist in the destination"""
                try:
                    if UI_results.project_name in os.listdir(self.chosen_default_project_folder):
                        TaskDialog.Show("Project Name already exist", "Project Not created. Name already exist")

                    else:
                        for folder in folders:
                            project_folder = r"{}\{}".format(self.chosen_default_project_folder, self.project_name)
                            sub_folder = r"{}\{}".format(project_folder, folder)
                            # print(sub_folder)
                            os.makedirs(sub_folder)

                        """create_revit_project"""
                        """get the the revit version and use its version template to create the revit file"""
                        revit_version = "RVT {}".format(app.VersionNumber)
                        template_path = r"C:\ProgramData\Autodesk\{}\Templates\English\DefaultMetric.rte".format(
                            revit_version)
                        default_project_template = app.DefaultProjectTemplate

                        self.revit_file_path = r"{0}\{1}\{2}\{1}.rvt".format(self.chosen_default_project_folder,
                                                                             self.project_name, rvt)

                        global global_revit_file_path
                        global_revit_file_path = self.revit_file_path
                        """create project"""
                        new_project_doc = app.NewProjectDocument(default_project_template)

                        """save project"""
                        new_project_doc.SaveAs(self.revit_file_path)
                        return self.revit_file_path
                except:
                    TaskDialog.Show("Specified path does not exist", "Specified path does not exist")
            else:
                TaskDialog.Show("Project Name cannot be empty", "Project Name cannot be empty")
        else:
            # print("Operation Cancelled")
            pass


def open_project_file():
    """open project"""
    """ opening the created revit file does not work when trying o open from th class level
    so this function has to be isolated as a def outside the class scope"""
    file_path = CreateNewProject().create_revit_project_directory()
    # print("File path: ".format(file_path))
    if file_path is not None:
        uiApp.OpenAndActivateDocument(file_path)


open_project_file()
