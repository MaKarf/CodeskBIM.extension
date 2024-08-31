import clr

from lib.AppMethods import CopyColorToClipboard
from lib.UI.Popup import Alert

clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
clr.AddReference('AdWindows')

try:
    app = __revit__.Application
    version = app.VersionNumber
except:
    version = "2021"

wpf_assembly_name = "IronPython.Wpf"
codesk_assembly_name = "CodeskBIMRevit{}".format(version)

try:
    clr.AddReference(wpf_assembly_name)
    clr.AddReference(codesk_assembly_name)
    import wpf
except:
    clr.AddReferenceToFileAndPath(__codeskDLL__)
    clr.AddReferenceToFileAndPath(__codeskDLL__.replace(codesk_assembly_name, wpf_assembly_name))
    import wpf

from CodeskBIMRevit.FilesPath import extension_path

from Microsoft.Win32.SafeHandles import SafeFileHandle

import Autodesk.Windows as AutodeskWindows

import System
from System.IO import MemoryStream
from System import Uri
from System.Drawing import Bitmap, Graphics, Image
from System.Windows import Window, WindowStyle, WindowState, Interop, Thickness, ResourceDictionary, Media, \
    RoutedEventHandler, Point
from System.Windows.Forms import Cursor, Screen, Clipboard
from System.Windows.Media.Imaging import BitmapImage
# from System.Windows.Media import Point
from System.Windows.Input import MouseButtonEventArgs, MouseWheelEventArgs

from os.path import join


class ColorPickerWindow(Window):

    def __init__(self):
        """load resource dictionary to the xaml file"""

        self.xaml_folder = join(extension_path, r'lib\UI\xamlFiles')

        styles_path = join(self.xaml_folder, "codeskbimWPFWindowStyles.xaml")

        """get full path for xaml file"""
        xaml_file_path = join(self.xaml_folder, "ColorPickerWindow.xaml")

        """load xaml file into the window"""
        wpf.LoadComponent(self, xaml_file_path)

        """add resource dictionary"""
        r = ResourceDictionary()
        r.Source = Uri(styles_path)
        self.Resources = r

        self.set_cursor()

        """set revit window as its parent window"""
        wih = Interop.WindowInteropHelper(self)
        wih.Owner = AutodeskWindows.ComponentManager.ApplicationWindow

        self.AllowsTransparency = True
        self.Background = Media.Brushes.Transparent
        self.WindowStyle = WindowStyle.None
        self.WindowState = WindowState.Maximized

        """create the image from screenshot and set the image object to the bitmap image parameter"""
        self.set_background_image_from_screenshot()

        """pin the window to top"""
        self.Topmost = True

        self.zoom_counter = 1

        self.point = None
        self.mouse_pos = None

        self.picked_color = None
        self.hex_color = None
        self.rgb_color = None

        self.Loaded += RoutedEventHandler(self.init_window)

        self.mouse_move("sender", "e")
        self.ShowDialog()

    def set_contrasting_text_color(self):
        background_color = self.txt.Background.Color
        # print background_color
        luminance = 0.299 * background_color.R + 0.587 * background_color.G + 0.114 * background_color.B
        # print luminance
        text_color = Media.Colors.White if luminance < 128 else Media.Colors.Black

        color_brush = Media.Color.FromArgb(text_color.A, text_color.R, text_color.G, text_color.B)
        self.txt.Foreground = Media.SolidColorBrush(text_color)
        self.txt.BorderBrush = Media.SolidColorBrush(text_color)

    def set_background_image_from_screenshot(self):
        """Capture a screenshot of the primary screen"""
        screen = Screen.PrimaryScreen

        """Create a bitmap to capture the screen"""
        screenshot = Bitmap(screen.Bounds.Width, screen.Bounds.Height)

        """Create a Graphics object from the screenshot"""
        with Graphics.FromImage(screenshot) as graphics:
            graphics.CopyFromScreen(screen.Bounds.X, screen.Bounds.Y, 0, 0, screen.Bounds.Size)

        """Convert the screenshot to a byte array (PNG format)"""
        image_stream = MemoryStream()
        screenshot.Save(image_stream, System.Drawing.Imaging.ImageFormat.Png)
        image_bytes = image_stream.ToArray()

        bitmap_image = BitmapImage()
        """Create a BitmapImage from the byte array"""
        """instantiate the bitmap image in parameter"""

        bitmap_image.BeginInit()
        bitmap_image.StreamSource = MemoryStream(image_bytes)
        bitmap_image.EndInit()

        """Set the window's background to the captured image"""
        # self.Background = Media.ImageBrush(self.bitmap_image)
        self.image.Source = bitmap_image

    def init_window(self, sender, e):
        pass

    def zoom(self, sender, e):

        scale = 1.0

        if e.Delta > 0:
            scale *= 1.1

            if self.zoom_counter == 1:
                self.point = Cursor.Position
                self.mouse_pos = self.point

            if self.point != self.mouse_pos:
                self.point = self.mouse_pos
            self.zoom_counter += 1

        else:
            scale /= 1.1
            self.zoom_counter -= 1

        if self.zoom_counter < 1:
            scale = 1.0
            self.zoom_counter = 1

        # print "Point: {}".format(self.point)
        # print "Mouse Pos: {}".format(self.mouse_pos)
        # print "------------------------------------------------------------\n\n"

        if self.point is not None:
            mat_trans = self.grid2.RenderTransform
            mat = mat_trans.Matrix

            mat.ScaleAt(scale, scale, self.point.X, self.point.Y)
            mat_trans.Matrix = mat
            e.Handled = True

    def mouse_move(self, sender, e):
        """display current color while the mouse moves on the screen"""
        mouse_position = Cursor.Position

        offset = 0
        h_offset = mouse_position.X + offset
        v_offset = mouse_position.Y + offset

        color = self.capture_color(exit_operation=False)

        """set background color"""
        media_color = Media.Color.FromArgb(color[0], color[1], color[2], color[3])
        self.txt.Background = Media.SolidColorBrush(media_color)

        self.txt.Margin = Thickness(h_offset, v_offset, 0, 0)
        self.rgb_color = "R:{1} G:{2} B:{3}".format(color[0], color[1], color[2], color[3])
        self.hex_color = self.argb_to_hex(color)

        self.txt.Content = "{}\n\n{}".format(self.rgb_color, self.hex_color)
        self.set_contrasting_text_color()

    def capture_color(self, exit_operation):
        """Get the current mouse cursor position"""
        mouse_position = Cursor.Position

        """Capture the color at the mouse cursor position"""
        with System.Drawing.Bitmap(1, 1) as screen:
            with System.Drawing.Graphics.FromImage(screen) as g:
                g.CopyFromScreen(mouse_position, System.Drawing.Point.Empty, System.Drawing.Size(1, 1))
                picked_color = screen.GetPixel(0, 0)
                color = (picked_color.A, picked_color.R, picked_color.G, picked_color.B)

                if exit_operation:
                    self.Close()
                return color

    def mouse_right_button_down_handler(self, sender, e):
        self.Close()
        """copy both rgb and hex color code to clipboard"""
        CopyColorToClipboard(rgb_color=self.rgb_color, hex_color=self.hex_color)

    def mouse_left_button_down_handler(self, sender, e):
        if isinstance(e, MouseButtonEventArgs):
            self.picked_color = self.capture_color(exit_operation=True)
            # print(self.picked_color)

        """Prevent further handling of the event"""
        e.Handled = True
        pass

    @staticmethod
    def argb_to_hex(argb=()):
        a = int(argb[0])
        r = int(argb[1])
        g = int(argb[2])
        b = int(argb[3])

        """Ensure the values are within the valid range (0-255)"""
        alpha = max(0, min(255, a))
        red = max(0, min(255, r))
        green = max(0, min(255, g))
        blue = max(0, min(255, b))

        """Convert the values to hexadecimal strings and format them"""
        hex_color = "#{:02X}{:02X}{:02X}{:02X}".format(alpha, red, green, blue)
        return hex_color

    def set_cursor(self):
        """Load your custom cursor image from a file"""
        cursor_image = Image.FromFile(join(self.xaml_folder, "cursor.png"))

        """Create a custom cursor from the image"""
        custom_cursor = cursor_image.GetHicon()

        handle = SafeFileHandle(custom_cursor, True)
        self.Cursor = System.Windows.Interop.CursorInteropHelper.Create(handle)

    def close_on_escape(self, sender, e):
        if str(e.Key) == "Escape":
            self.Close()


if __name__ == "__main__":
    ColorPickerWindow()
