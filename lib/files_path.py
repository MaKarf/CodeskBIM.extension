import os
from initialize import app, FilesPath

"""get the FilesPath class from c#"""
files_path = FilesPath
version_specific_files_path = FilesPath(app.VersionNumber)

