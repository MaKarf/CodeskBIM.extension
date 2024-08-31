import clr

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference('AdWindows')
clr.AddReference("System.Windows.Forms")

from lib.UI.xamlFiles.SetWPFColor import set_wpf_component_background_color

from System.Windows import RoutedEventHandler
from System.Windows.Input import KeyEventHandler

"""importing the WPF module"""
try:
    clr.AddReference("IronPython.Wpf")
    import wpf
except Exception:
    clr.AddReferenceToFileAndPath(__WpfPath__)
    import wpf

from os.path import join

from System.Windows import Interop
from System.Windows import Window, Media
from System.Windows import ResourceDictionary
from System import Uri

import Autodesk.Windows as AutodeskWindows
from Autodesk.Revit.UI import UIApplication

app = __revit__.Application
ui_app = UIApplication(app)


class BaseWPFClass(Window):
    exited_with_close_button = True

    def __init__(self, xaml_file_name):

        self.lock = True

        """load resource dictionary to the xaml file"""
        xaml_folder = join(__basePath__, r'lib\UI\xamlFiles')

        styles_path = join(xaml_folder, "codeskbimWPFWindowStyles.xaml")

        """get full path for xaml file"""
        xaml_file_path = join(xaml_folder, xaml_file_name)

        """load xaml file into the window"""
        wpf.LoadComponent(self, xaml_file_path)

        """set revit window as its parent window"""
        self.setup_owner()
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

    def hide(self):
        self.Hide()

    def show(self, modal=False):
        """Show window."""
        if modal:
            return self.ShowDialog()
        # else open non-modal
        self.Show()

    def show_dialog(self):
        """Show modal window."""
        return self.ShowDialog()

# path = r"E:\CodeskBIM Revit Addin Setup\pyCodeskKitchen\ksedoc\CodeskBIM.extension\lib\UI\xamlFiles\test.xaml"
# ui = BaseWPFClass(path)
# ui.ShowDialog()
