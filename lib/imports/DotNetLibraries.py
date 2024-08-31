import clr

clr.AddReference("System")
clr.AddReference("System.Xml")
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference('AdWindows')
clr.AddReference("System.Windows.Forms")

"""importing the WPF module"""
try:
    clr.AddReference("IronPython.Wpf")
    import wpf
except Exception:
    clr.AddReferenceToFileAndPath(__WpfPath__)
    import wpf

import System
from System.Windows import Window, Media, Thickness, ResourceDictionary, RoutedEventHandler, Interop, Uri
from System.Windows.Input import KeyEventHandler, MouseButtonEventArgs, MouseWheelEventArgs
from System.Windows.Controls import StackPanel, Orientation, Label, ComboBox, ComboBoxItem, SelectionChangedEventHandler
from System.IO import MemoryStream
from System.Windows.Media.Imaging import BitmapImage
from System.Collections.Generic import List
