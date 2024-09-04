import clr

from engine_type import get_engine_type, EngineType

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference('AdWindows')
clr.AddReference("System.Windows.Forms")

from UI.xamlFiles.SetWPFColor import set_wpf_component_background_color

from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler

"""importing the WPF module"""
from initialize import wpf, extension_path

from os.path import join

from System.Windows import Interop
from System.Windows import Window, Media
from System.Windows import ResourceDictionary
from System import Uri

import Autodesk.Windows as AutodeskWindows
from Autodesk.Revit.UI import UIApplication

app = __revit__.Application
ui_app = UIApplication(app)

"""check if the command is being executed by pyrevit or CodeskBIMRevit add-in"""
engine_type = get_engine_type()
if engine_type == EngineType.codesk_engine:
    base_window = Window
else:
    from pyrevit.forms import WPFWindow
    base_window = WPFWindow


class BaseWPFClass(base_window):
    exited_with_close_button = True

    def __init__(self, xaml_file_name):
        """load resource dictionary to the xaml file"""
        xaml_folder = join(extension_path, r'lib\UI\xamlFiles')
        styles_path = join(xaml_folder, "codeskbimWPFWindowStyles.xaml")
        """get full path for xaml file"""
        xaml_file_path = join(xaml_folder, xaml_file_name)

        if engine_type == EngineType.codesk_engine:
            """load xaml file into the window"""
            wpf.LoadComponent(self, xaml_file_path)

            """set revit window as its parent window"""
            self.setup_owner()
        else:
            WPFWindow.__init__(self, xaml_file_path)

        self.Window = self

        """add resource dictionary"""
        r = ResourceDictionary()
        r.Source = Uri(styles_path)
        self.Resources = r

        """set background color"""
        set_wpf_component_background_color(hex_color="#E6ECF3", wpf_component=self)

        """Attach the closing event handler to the Window"""
        # self.Window.Closing += self.window_closing_handler
        self.KeyDown += self.close_on_escape

    def setup_owner(self):
        wih = Interop.WindowInteropHelper(self)
        wih.Owner = AutodeskWindows.ComponentManager.ApplicationWindow

    def close_on_escape(self, sender, e):
        # print e.Key
        if str(e.Key) == "Escape":
            self.Close()

    def close_window(self):
        self.exited_with_close_button = False
        self.Close()


# path = "test.xaml"
# ui = BaseWPFClass(path)
# ui.ShowDialog()
