import clr

clr.AddReference("PresentationFramework")
clr.AddReference("WindowsBase")
clr.AddReference("System.Xaml")  # Depending on your environment, you may need this

from System.IO import StringReader
from System.Xml import XmlReader
from System.Windows.Markup import XamlReader
from System.Windows import Visibility


def load_xaml_from_string(xaml):
    """Convert the XAML string into a StackLayout object"""
    string_reader = StringReader(xaml)
    xml_reader = XmlReader.Create(string_reader)  # Create an XmlReader from StringReader
    return XamlReader.Load(xml_reader)
