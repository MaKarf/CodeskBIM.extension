import os
import sys

from Autodesk.Revit.DB.ElementTransformUtils import CopyElements

from Autodesk.Revit import DB
from Autodesk.Revit.DB import Transaction, FilteredElementCollector as Fec, BuiltInCategory as Bic
from Autodesk.Revit.Exceptions import OperationCanceledException
from System.Collections.Generic import List

from lib.UI.Popup import Alert
from lib.files_path import version_specific_files_path

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView
t = Transaction(doc, "Load Site Plan")


def set_active_view(sheet=None):
    sheet_number = sheet.LookupParameter("Sheet Number").AsString()
    # sheet_number = sheet
    collector = Fec(doc)
    sheets = collector.OfClass(DB.ViewSheet).ToElements()

    sheet_view = None
    for sheet in sheets:
        if sheet.SheetNumber == sheet_number:
            sheet_view = sheet
            break

    if sheet_view is None:
        # Sheet not found, handle the error
        # raise Exception("Sheet not found.")
        pass

    ui_doc.ActiveView = sheet_view


def load_site_plan():
    path = version_specific_files_path.codeskSitePlanReferncePath
    if not os.path.exists(path):
        Alert(title="File Not Found", header="Reference ile to import from is not found", content="")
        return None

    site_plan_doc = app.OpenDocumentFile(path)

    views = Fec(site_plan_doc).OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
    drafting_view = [i for i in views if i.ViewType == DB.ViewType.DraftingView][0]
    drafting_view_icollection = List[DB.ElementId]()
    drafting_view_icollection.Add(drafting_view.Id)

    x = [site_plan_doc.GetElement(i) for i in drafting_view.GetDependentElements(None)]
    site_plan_drawings = [i.Id for i in x if
                          i.GetType() == DB.DetailLine or i.GetType() == DB.TextNote or i.GetType() == DB.DetailArc]

    site_plan_drawings_icollection = List[DB.ElementId]()
    [site_plan_drawings_icollection.Add(i) for i in site_plan_drawings]

    try:
        t.Start()
        """first copy and paste drafting view"""
        drafting_view_created = CopyElements(
            sourceDocument=site_plan_doc,
            elementsToCopy=drafting_view_icollection,
            destinationDocument=doc,
            transform=None,
            options=None)

        destination_view = doc.GetElement(drafting_view_created[0])

        """then copy and paste the detail elements on the source drafting view"""
        CopyElements(
            sourceView=drafting_view,
            elementsToCopy=site_plan_drawings_icollection,
            destinationView=destination_view,
            additionalTransform=None,
            options=None)

        site_plan_sheet = [s for s in Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements() if
                           ("BLOCK PLAN" in s.Name.upper() and "SITE" in s.Name.upper()) or
                           ("SETTING OUT" in s.Name.upper() and "SITE" in s.Name.upper()) or
                           "SITE PLAN" in s.Name.upper()]

        """2nd check"""
        if not site_plan_sheet:
            site_plan_sheet = \
                [s for s in Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements() if
                 "BLOCK PLAN" in s.Name.upper()]

            if not site_plan_sheet:
                site_plan_sheet = None
                t.Commit()
                return None
            else:
                site_plan_sheet = site_plan_sheet[0]
        else:
            site_plan_sheet = site_plan_sheet[0]

        de = site_plan_sheet.GetDependentElements(None)
        title_block = \
            [doc.GetElement(fi) for fi in de if type(doc.GetElement(fi)) == DB.FamilyInstance and doc.GetElement(
                fi).Category.Name == "Title Blocks"][0]
        try:
            bbox = title_block.get_BoundingBox(site_plan_sheet)

            ttb_height = bbox.Max.Y - bbox.Min.Y
            title_block_width = bbox.Max.X - bbox.Min.X

            viewport_location = DB.XYZ(bbox.Min.X, bbox.Min.Y + (ttb_height * 0.5), 0)
            site_plan_viewport = DB.Viewport.Create(doc, site_plan_sheet.Id, destination_view.Id, viewport_location)

            """shift the viewport a little away from the title block"""
            vp_box = site_plan_viewport.get_BoundingBox(site_plan_sheet)
            vp_width = vp_box.Max.X - vp_box.Min.X
            site_plan_viewport.Location.Move(DB.XYZ(bbox.Min.X + (0.5 * vp_width) + (0.075 * vp_width), 0, 0))

            """close site plan document without saving"""
            site_plan_doc.Close(False)
        except AttributeError:
            pass
        t.Commit()

        set_active_view(site_plan_sheet)
        return site_plan_sheet

    except OperationCanceledException:
        """close site plan document without saving"""
        site_plan_doc.Close(False)
        t.RollBack()


load_site_plan()
