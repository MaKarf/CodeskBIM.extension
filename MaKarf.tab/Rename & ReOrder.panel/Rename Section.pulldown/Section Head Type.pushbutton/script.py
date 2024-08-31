from Autodesk.Revit import DB
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction

from lib import phases
from lib.AppMethods import Alert
from lib.searchElement import SearchElementTypeByName

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Change Head Type")
active_view = ui_doc.ActiveView
phase = phases.new_construction_phase


class SetSectionHead:
    def __init__(self):
        pass

    grid_line = Fec(doc).OfCategory(Bic.OST_Grids).WhereElementIsNotElementType().FirstElement()
    grid_head_type = SearchElementTypeByName(document=doc,
                                             built_in_category=DB.BuiltInCategory.OST_GridHeads,
                                             built_in_parameter=DB.BuiltInParameter.SYMBOL_NAME_PARAM,
                                             search_name="MK_Grid Head",
                                             family_category_name="Grid")

    """raise exception if there is no section placed yet """
    if grid_line is None:
        Alert(content="Place at lease ONE Grid line and retry",
              title="Results",
              header="No Grid Lines found")
    else:
        t.Start()
        doc.GetElement(grid_line.GetTypeId()).LookupParameter("Symbol").Set(grid_head_type.results.Id)
        t.Commit()

    """###########################################################################################################"""
    """+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""
    """###########################################################################################################"""
    try:
        section_line = [i for i in Fec(doc).OfCategory(Bic.OST_Viewers).WhereElementIsNotElementType().ToElements()
                        if doc.GetElement(i.GetTypeId()).ViewFamily == DB.ViewFamily.Section][0]

        section_head_type = SearchElementTypeByName(document=doc,
                                                    built_in_category=DB.BuiltInCategory.OST_SectionHeads,
                                                    built_in_parameter=DB.BuiltInParameter.SYMBOL_NAME_PARAM,
                                                    search_name="MK_Section Head_M",
                                                    family_category_name="Section")
        t.Start()
        section_head_id = doc.GetElement(section_line.GetTypeId()).LookupParameter("Section Tag").AsElementId()

        doc.GetElement(section_head_id).LookupParameter("Section Head").Set(section_head_type.results.Id)
        doc.GetElement(section_head_id).LookupParameter("Section Tail").Set(section_head_type.results.Id)
        """raise exception if there is no section placed yet """
        t.Commit()

    except IndexError:
        Alert(content="Place at lease ONE section line and retry",
              title="Results",
              header="No section Lines found")

    # tag.ChangeTypeId(mk_door_tag_type.Id)
    # tag.LookupParameter("Leader Line").Set(0)
    # def tag_element(self):
    #     """add tags to the elements"""
    #     # for e in data_dicts:
    #     det_sect_view = e.get("associated elevation view")
    #     bb = e.get("elem").get_BoundingBox(None)
    #
    #     tag = DB.IndependentTag.Create(doc, det_sect_view.Id, Reference(e.get("elem")), True,
    #                                    DB.TagMode.TM_ADDBY_CATEGORY,
    #                                    DB.TagOrientation.Horizontal, DB.XYZ(0, 0, 0))
    #     y_pos = (bb.Max.Z - bb.Min.Z) * 0.6
    #     tag.Location.Move(DB.XYZ(0, 0, - y_pos))
    #
    #     """replace tag type with MK_Door Tag"""
    #     try:
    #         mk_door_tag_type = string_search_get_element_type_by_name("CodeskScheduleDoorTag",
    #                                                                   DB.BuiltInParameter.SYMBOL_NAME_PARAM)
    #     except ValueError:
    #         """if tag not found, load them and continue"""
    #         LoadTags().retrieve_families()
    #         mk_door_tag_type = string_search_get_element_type_by_name("CodeskScheduleDoorTag",
    #                                                                   DB.BuiltInParameter.SYMBOL_NAME_PARAM)
    #
    #     tag.ChangeTypeId(mk_door_tag_type.Id)
    #     tag.LookupParameter("Leader Line").Set(0)


SetSectionHead()
