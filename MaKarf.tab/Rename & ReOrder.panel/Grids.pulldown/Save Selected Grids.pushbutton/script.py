from update_projects_data import ProjectData

from UI.xamlFiles.Grids.Save.SaveGridsSelection import SaveGridsUIClass

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


active_view = ui_doc.ActiveView

SaveGridsUIClass(ProjectData)
