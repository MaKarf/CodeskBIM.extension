from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction
from UI.Popup import Alert

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "North Point")


# def update_project_browser():
#     """Function to close and reopen ProjectBrowser so changes to Sheetnumber would become visible."""
#     from Autodesk.Revit.UI import DockablePanes, DockablePane
#     project_browser_id = DockablePanes.BuiltInDockablePanes.ProjectBrowser
#     project_browser = DockablePane(project_browser_id)
#     project_browser.Hide()


def get_views_on_sheet(sheet):
    """Function to return all views found on the given sheet."""
    viewports_ids = sheet.GetAllViewports()
    viewports = [doc.GetElement(viewport_id) for viewport_id in viewports_ids]
    views_ids = [viewport.ViewId for viewport in viewports]
    views = [doc.GetElement(view_id) for view_id in views_ids]
    return views


def get_title_block_on_sheet(sheet):
    """Function to get TitleBlock from given ViewSheet.
    It will not return any TitleBlocks if there are more than 1 on ViewSheet.
    :returns TitleBlock"""

    all_TitleBlocks = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()
    title_blocks_on_sheet = []

    for title_block in all_TitleBlocks:
        if title_block.OwnerViewId == sheet.Id:
            title_blocks_on_sheet.append(title_block)

    if not title_blocks_on_sheet:
        # Alert("{}".format(sheet.SheetNumber), title="Results", header="No TitleBlocks found on ")
        # # print("***No TitleBlocks were found on given ViewSheet ({}***".format(sheet.SheetNumber))
        pass

    elif len(title_blocks_on_sheet) > 1:
        # Alert( "This did not affected the the success of the operation, however you may like to remove all and keep
        # only " "one Title Block on the sheet ", title="Results", header="Multiple TitleBlocks on {}".format(
        # sheet.SheetNumber)) # print("***There are more than 1 TitleBlock on given ViewSheet ({})****".format(
        # sheet.SheetNumber))
        pass

    else:
        return title_blocks_on_sheet[0]


def hide_north_points():
    sheets_collection = Fec(doc).OfCategory(Bic.OST_Sheets)

    """ variables to display final results"""
    collect_ON_results = []
    collect_OFF_results = []

    for sheet in sheets_collection:

        title_block = get_title_block_on_sheet(sheet)

        north_point_parameter_set = title_block.GetParameters("Show/Hide North Point")

        for np_parameter in north_point_parameter_set:
            flag = str(sheet.Name).upper()
            if "PLAN" in flag or "LAYOUT" in flag or "GF" in flag or "FF" in flag or "SF" in flag or "FLOOR" in flag:
                collect_ON_results.append(str(sheet.Name))
                np_parameter.Set(1)

            else:
                collect_OFF_results.append(str(sheet.Name))
                np_parameter.Set(0)

    """ checking to see if a sheet has the north point parameter. 
    if sheet has no [Show/Hide North Point] parameter, throw an alert to the user
     else throw success alert to user"""
    sheet_test = 0
    for sh in sheets_collection:
        y = get_title_block_on_sheet(sh).GetParameters("Show/Hide North Point")
        if len(list(y)) > 0:
            sheet_test += 1
        # print(list(y))
    # print(sheet_test)

    # if sheet_test == 0:
    #     Alert("None of your Title Block has a North Point visibility parameter ", title="Results",
    #           header="North Points Visibility Error")
    # else:
    #     Alert("Have been hidden on all Non Plan Title Blocks", title="Results",
    #           header="Success - North Points Operation")


t.Start()
try:
    hide_north_points()
    t.Commit()

except Exception:
    t.Commit()
