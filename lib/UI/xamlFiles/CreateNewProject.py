import os

from UI.xamlFiles.codeskbimWPFWindow import BaseWPFClass

import clr

clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import FolderBrowserDialog, DialogResult

from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler


class CreateProject(BaseWPFClass):
    project_name = ""
    project_path = ""
    make_path_default = False
    close_mode_value = ""

    default_project_folder = os.path.join(r"C:", r"{}\Documents".format(os.environ['HOMEPATH']))
    path_file_name = "default_path.txt"
    full_path = r"C:\ProgramData\Autodesk\Codesk\Makarf Add-in\docs\{}".format(path_file_name)
    chosen_default_project_folder = ""
    revit_file_path = None

    def __init__(self, xaml_file_name, default_path=None):
        BaseWPFClass.__init__(self, xaml_file_name)

        """check and create directory for path file if none exist else proceed"""
        self.prepare_directory()

        """Find the "button_run" button by its name"""
        check_file_name = self.Window.FindName("UI_project_name")
        select_folder = self.Window.FindName("select_folder")
        button_run = self.Window.FindName("button_run")

        """Attach the event handler to the button's "Click" event"""
        check_file_name.KeyUp += KeyEventHandler(self.check_file_name)
        select_folder.Click += RoutedEventHandler(self.select_folder_func)
        button_run.Click += RoutedEventHandler(self.finish_button)

        """check and create directory for path file if none exist else proceed"""
        self.prepare_directory()

        """UPDATE GUI ELEMENTS"""
        self.Window.FindName("UI_project_path").Text = self.default_project_folder
        self.Window.FindName("UI_project_name").Text = "Project 1"

        if self.Window.FindName("UI_project_name").Text in os.listdir(self.Window.FindName("UI_project_path").Text):
            self.Window.FindName("UI_project_name_validation").Text = "Project name already exist"
        else:
            self.Window.FindName("UI_project_name_validation").Text = "Valid project name"

        self.ShowDialog()
        # self.Show()

    def prepare_directory(self):
        path = r"C:\ProgramData\Autodesk\Codesk\Makarf Add-in\docs"
        try:
            if self.path_file_name in os.listdir(path):
                self.default_project_folder = open(self.full_path, "r").read()
        except:
            os.makedirs(path)
            with open(self.full_path, "w") as pt:
                pt.write(self.default_project_folder)
                pt.close()

    def finish_button(self, sender, e):
        self.project_name = self.Window.FindName("UI_project_name").Text
        self.project_path = self.Window.FindName("UI_project_path").Text
        self.make_path_default = self.Window.FindName("UI_set_default").IsChecked
        self.Close()
        self.close_mode_value = "indirect"

    def select_folder_func(self, sender, e):
        dialog = FolderBrowserDialog()
        result = dialog.ShowDialog()

        if result == DialogResult.OK:
            selected_folder = dialog.SelectedPath
            self.Window.FindName("UI_project_path").Text = selected_folder
            """update UI after selecting a new path"""
            self.check_file_name("a", "c")

        else:
            # print("Folder selection canceled or an error occurred.")
            pass

    def check_file_name(self, sender, e):
        try:
            if self.Window.FindName("UI_project_name").Text in os.listdir(self.Window.FindName("UI_project_path").Text):
                self.Window.FindName("UI_project_name_validation").Text = "Project name already exist"

            elif self.Window.FindName("UI_project_name").Text == "":
                self.Window.FindName("UI_project_name_validation").Text = "Project name cannot be empty"

            else:
                self.Window.FindName("UI_project_name_validation").Text = "Valid project name"

        except:
            self.Window.FindName("UI_project_name_validation").Text = "INVALID PATH"
        pass
