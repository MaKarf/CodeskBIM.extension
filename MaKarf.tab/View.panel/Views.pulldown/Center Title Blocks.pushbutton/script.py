from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Revit Transaction")


def update_project_browser():
    """Function to close and reopen ProjectBrowser so changes to Sheetnumber would become visible."""
    from Autodesk.Revit.UI import DockablePanes, DockablePane
    project_browser_id = DockablePanes.BuiltInDockablePanes.ProjectBrowser
    project_browser = DockablePane(project_browser_id)
    project_browser.Hide()


def get_views_on_sheet(sheet):
    """Function to return all views found on the given sheet."""
    viewports_ids = sheet.GetAllViewports()
    viewports = [doc.GetElement(viewport_id) for viewport_id in viewports_ids]
    views_ids = [viewport.ViewId for viewport in viewports]
    views = [doc.GetElement(view_id) for view_id in views_ids]
    return views


def title_block_on_origin():
    """Function to get TitleBlock from given ViewSheet.
    It will not return any TitleBlocks if there are more than 1 on ViewSheet.
    :returns TitleBlock"""

    all_TitleBlocks = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()
    for x in all_TitleBlocks:
        # print(x.Location.Point)
        """ get view sheet on which title block sits"""
        view_from_title_block = doc.GetElement(x.OwnerViewId)

        """ get the view's origin; which is always 0,0,0"""
        view_origin = view_from_title_block.Origin

        "subtract the current location of the title block from the origin to set the title blocks "
        "location back to 0,0,0. This part is needed for the move to work because the current location of the"
        "title block is referenced and captured into the process"
        new_loc = view_origin - x.Location.Point

        """ finally move the title block with the Move method """
        x.Location.Move(new_loc)


def run():
    t.Start()
    try:
        title_block_on_origin()
        t.Commit()

    except Exception:
        t.Commit()


run()
