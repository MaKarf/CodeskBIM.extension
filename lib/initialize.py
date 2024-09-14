import sys
from os.path import join
import clr

from codeskResource.mkExtensionPath import mk_extension_path

try:
    app = __revit__.Application  # when app is evoked by UIApplication

except AttributeError:
    app = __revit__  # when evoked by event handler such as a pyrevit hook


extension_path = mk_extension_path()
__basePath__ = extension_path  # extension path for the codesk engine
# print extension_path

lib_folder = join(extension_path, "lib")
dlls_folder = join(lib_folder, "DLL")

files_path_dll = join(dlls_folder, "CodeskBIMRevitFilesPath.dll")
__filesPathDLL__ = files_path_dll

codesk_dll = join(dlls_folder, "CodeskBIMRevit{}.dll".format(app.VersionNumber))
__codeskDLL__ = codesk_dll

wpf_assembly_name = "IronPython.Wpf"
__WpfPath__ = join(dlls_folder, "{}.dll".format(wpf_assembly_name))

sys.path.append(extension_path)  # make it possible to type lib in front of modules imported from the lib

clr.AddReferenceToFileAndPath(files_path_dll)
clr.AddReferenceToFileAndPath(codesk_dll)
clr.AddReferenceToFileAndPath(__WpfPath__)

""" from namespaces import class"""
""" import CodeskBIMRevit namespaces from the C# .dll"""
from CodeskBIMRevit import *
from CodeskBIMRevitFilesPath import FilesPath

"""importing the WPF module"""
"""options for importing WPF module"""
Import IronPython
print IronPython
from IronPython.Modules import Wpf  # import wpf using the c# Wpf naming convention
from IronPython.Modules import Wpf as wpf  # import wpf using the pyrevit naming convention



