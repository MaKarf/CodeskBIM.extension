from Autodesk.Revit import DB
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec

from lib import phases

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
active_view = ui_doc.ActiveView
phase = phases.new_construction_phase


def get_section_type(type_name):
    section_types = [i for i in Fec(doc).OfCategory(Bic.OST_Viewers).WhereElementIsNotElementType().ToElements()
                     if doc.GetElement(i.GetTypeId()).ViewFamily == DB.ViewFamily.Section][0].GetValidTypes()

    try:
        return [doc.GetElement(i) for i in section_types if
                doc.GetElement(i).LookupParameter("Type Name").AsString() == type_name].pop()
    except IndexError:
        return None


def change_head(section_lines_to_change):
    try:
        """get existing section line"""
        section = [i for i in Fec(doc).OfCategory(Bic.OST_Viewers).WhereElementIsNotElementType().ToElements()
                   if doc.GetElement(i.GetTypeId()).ViewFamily == DB.ViewFamily.Section][0].GetTypeId()
        section_line = doc.GetElement(section)

        """create a separate section line for the purpose of creating doors and windows schedule"""
        try:
            empty_section_line = section_line.Duplicate("EmptyLines")
        except:
            empty_section_line = get_section_type("EmptyLines")

        """when the searched is found"""

        section_tag_id = empty_section_line.LookupParameter("Section Tag").AsElementId()
        section_tag = doc.GetElement(section_tag_id)

        """check if the empty tag already exist"""
        try:
            empty_section_tag = section_tag.Duplicate("EmptyHeads")
        except Exception:
            empty_section_tag = [doc.GetElement(i) for i in section_tag.GetSimilarTypes() if
                                 doc.GetElement(i).LookupParameter(
                                     "Type Name").AsValueString() == "EmptyHeads"].pop()

        """set head and tail to <none>"""
        empty_section_tag.LookupParameter("Section Head").Set(DB.ElementId.InvalidElementId)
        empty_section_tag.LookupParameter("Section Tail").Set(DB.ElementId.InvalidElementId)

        """change the section tag of the selected section lines to EmptyHeads"""
        empty_section_line.LookupParameter("Section Tag").Set(empty_section_tag.Id)

        """change the section line types to EmptyLines"""
        [i.ChangeTypeId(empty_section_line.Id) for i in section_lines_to_change]

    except IndexError as er:
        print er
        return None
