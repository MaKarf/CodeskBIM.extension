# """Provide access to Revit API.
revit_folder = r"C:\Program Files\Autodesk\Revit 2021"
import sys

sys.path.append(revit_folder)

from os.path import join

import clr

ASSEMBLY_FILE_TYPE = 'dll'
ASSEMBLY_FILE_EXT = '.dll'

ipy_assmname = 'IronPython'
ipy_dllpath = join("IPY277", ipy_assmname + ASSEMBLY_FILE_EXT)

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('AdWindows')
clr.AddReference('UIFramework')
clr.AddReference('UIFrameworkServices')

# Update the full path to 'RevitAPI.dll'

# clr.AddReferenceToFile('RevitAPI')
# clr.AddReferenceToFile('RevitAPIUI')

import UIFramework
import UIFrameworkServices


# import Autodesk.Internal as AdInternal
# import Autodesk.Private as AdPrivate
# import Autodesk.Windows as AdWindows

# from Autodesk.Revit import Attributes
# from Autodesk.Revit import ApplicationServices
# from Autodesk.Revit import DB
# from Autodesk.Revit import UI

from IronPython.Modules import Wpf as wpf

# wpf = IronPython.Modules.Wpf


def get_product_serial_number():
    """Return serial number of running host instance."""
    return UIFrameworkServices.InfoCenterService.ProductSerialNumber


def is_product_demo():
    """Determine if product is using demo license"""
    return get_product_serial_number() == '000-00000000'


def is_api_object(data_type):
    """Check if given object belongs to Revit API"""
    if hasattr(data_type, 'GetType'):
        return 'Autodesk.Revit.' in data_type.GetType().Namespace

