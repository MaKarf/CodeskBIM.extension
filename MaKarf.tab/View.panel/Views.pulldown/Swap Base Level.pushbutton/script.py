from Autodesk.Revit import DB

from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic, BuiltInParameter as Bip

from System.Collections.Generic import List

from UI.Popup import Alert
from UI.xamlFiles.DropDownSelection import DropDownSelection

doc = __revit__.ActiveUIDocument.Document

el = Fec(doc).OfCategory(Bic.OST_Walls).WhereElementIsNotElementType().ToElements()
lvs = Fec(doc).OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()

t = DB.Transaction(doc, "Replace level")


def element_category_and_instance_filter(built_in_category):
    """Find all door instances in the project by finding all elements that both belong to the door"""
    """category and are family instances."""
    family_instance_filter = DB.ElementClassFilter(DB.FamilyInstance)

    """Create a category filter for Doors"""
    door_category_filter = DB.ElementCategoryFilter(Bic.OST_Doors)

    """Create a logic And filter for all Door FamilyInstances"""
    elements_filter = DB.LogicalAndFilter(family_instance_filter, door_category_filter)

    return elements_filter


def get_level_by_name(level_name, as_view=False):
    collector = Fec(doc)
    if as_view:
        all_levels = collector.OfCategory(Bic.OST_Views).WhereElementIsNotElementType().ToElements()
    else:
        all_levels = collector.OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()

    try:
        return [level for level in all_levels if level.Name == level_name].pop()
    except IndexError:
        # print("Level Name not found")
        return None


def element_level_filter(level_name):
    try:
        """get the level id"""
        level_id = get_level_by_name(level_name).Id
        """filter elements with base level of level specified level"""
        level_filter = DB.ElementLevelFilter(level_id)
        return level_filter
    except AttributeError:
        return None


def move_to_level(source_level, element_to_move, new_level):
    """check if it has a Level Parameter"""
    try:
        options = DB.CopyPasteOptions()

        DB.ElementTransformUtils.CopyElements(sourceView=source_level,
                                              elementsToCopy=element_to_move,
                                              destinationView=new_level,
                                              additionalTransform=None,
                                              options=options
                                              )
        doc.Delete(element_to_move)

    except Exception as e:
        # print e
        pass


def set_new_base_level(current_level_name, new_level_name):
    """get levels by their name"""
    current_level = get_level_by_name(current_level_name)
    new_level = get_level_by_name(new_level_name)

    """get levels as views"""
    current_level_as_view = get_level_by_name(current_level_name, as_view=True)
    new_level_as_view = get_level_by_name(new_level_name, as_view=True)

    """create an ICollection to keep all the element Ids for move and delete"""
    element_to_delete = List[DB.ElementId]()

    lf = element_level_filter(current_level_name)
    if lf is not None:
        """check for elements to be set"""
        lev_filter = Fec(doc).WherePasses(lf).ToElements()
        # print len(lev_filter)

        t.Start()
        for i in lev_filter:
            # print(type(i))
            # param = i.get_Parameter(Bip.ROOM_LEVEL_ID)

            if isinstance(i, DB.FamilyInstance):
                param = i.get_Parameter(Bip.FAMILY_LEVEL_PARAM)

                """check if parameter exist or has value"""
                if param is not None:
                    if not param.IsReadOnly:
                        param.Set(new_level.Id)

            else:

                if i.get_Parameter(Bip.ROOM_LEVEL_ID) is not None:
                    """add to list for future processing"""
                    if i.get_Parameter(Bip.ROOM_LEVEL_ID).IsReadOnly:
                        # print(type(i))
                        element_to_delete.Add(i.Id)

                elif i.LookupParameter("Base Constraint") is not None:  # """for Walls"""

                    i.LookupParameter("Base Constraint").Set(new_level.Id)

                elif i.LookupParameter("Base Level") is not None:  # """for Ceilings, Floors, Railings, Roofs"""
                    i.LookupParameter("Base Level").Set(new_level.Id)

                elif i.get_Parameter(Bip.LEVEL_PARAM) is not None:  # """for Plantings, Site components"""
                    i.get_Parameter(Bip.LEVEL_PARAM).Set(new_level.Id)

        """move and delete required elements to the new level after all the easy swapping to avoid system error
        message saying 'Elements were deleted' """
        move_to_level(source_level=current_level_as_view, element_to_move=element_to_delete,
                      new_level=new_level_as_view)
        t.Commit()

        """check for remaining elements not set"""
        lev_filter = Fec(doc).WherePasses(lf).ToElements()
        # print len(lev_filter)
    else:
        Alert(title="Error",
              header="Invalid Level name",
              content="No Level with name '{}' found".format(current_level_name))


collected_levels = Fec(doc).OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()
ui_data_list = [{"name": i.Name, "element": i.Name} for i in collected_levels]

current_level_ui = DropDownSelection(title="Change Level", label_name="Current Level", dropdown_list=ui_data_list)
current_level_nam = current_level_ui.selected_item

if current_level_nam is not None:
    ui_data_list.remove({"name": current_level_nam, "element": current_level_nam})

    new_level_ui = DropDownSelection(title="Change Level", label_name="New Level", dropdown_list=ui_data_list)
    new_level_nam = new_level_ui.selected_item

    # print current_level_nam
    # print new_level_nam

    if new_level_nam is not None:
        set_new_base_level(current_level_nam, new_level_nam)

