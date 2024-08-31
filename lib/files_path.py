import os

import clr

""" add a reference to your C# .dll"""
try:
    clr.AddReferenceToFileAndPath(__filesPathDLL__)
except:
    _filesPathDLL = r"{}\Autodesk\Revit\Addins\{}\CodeskBIMRevit\CodeskBIMRevitFilesPath.dll".format(
        os.environ.get("APPDATA"),
        __revit__.Application.VersionNumber
    )
    # print(_filesPathDLL)

    clr.AddReferenceToFileAndPath(_filesPathDLL)

""" import CodeskBIMRevit namespaces from the C# .dll"""
from CodeskBIMRevitFilesPath import FilesPath

"""get the FilesPath class from c#"""
files_path = FilesPath
version_specific_files_path = FilesPath(__revit__.Application.VersionNumber)


