from files_path import version_specific_files_path
from UI.xamlFiles.TransferViewTemplate import TransferViewTemplate

"""GLOBAL VARIABLES"""
app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView

"""open the reference project behind the scene"""
codesk_reference_doc = app.OpenDocumentFile(version_specific_files_path.codeskRefernceProjectDocumentPath)

mk = TransferViewTemplate()

"""close the reference project after operation"""
try:
    codesk_reference_doc.Close()
except:
    pass