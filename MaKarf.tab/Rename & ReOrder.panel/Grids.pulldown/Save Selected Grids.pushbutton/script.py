from lib.update_projects_data import ProjectData

from lib.UI.xamlFiles.SaveGridsSelection import SaveGridsUIClass

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


active_view = ui_doc.ActiveView

SaveGridsUIClass(ProjectData)
