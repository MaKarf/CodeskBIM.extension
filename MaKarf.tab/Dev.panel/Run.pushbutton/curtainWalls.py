import os.path

from Autodesk.Revit import DB
from Autodesk.Revit.DB import XYZ, FilteredElementCollector
from Autodesk.Revit.DB.Structure import StructuralType

from lib.UI.xamlFiles.CheckboxSelection import CheckboxSelection
from lib.files_path import files_path
from lib.imports.DotNetSystem import List
from lib.loadfamilies import load_family

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


t = DB.Transaction(doc, "Test")

levels_collection = DB.FilteredElementCollector(doc).OfCategory(
    DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()


def get_all_curtain_walls():
    dr = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
    all_c_walls = \
        [
            {
                "element": i, "name": "{}Lx{}H".format(i.LookupParameter("Length").AsValueString(),
                                                       i.LookupParameter("Unconnected Height").AsValueString())
            }
            for i in dr if i.LookupParameter("Number")
        ]
    """refine cw types"""
    return all_c_walls


def refined_curtain_walls(all_c_walls):
    refined_c_walls = []
    name_checker = []
    for i in all_c_walls:
        """set computed cw name into comment parameter"""
        i.get("element").LookupParameter("Comments").Set(i.get("name"))

        if i.get("name") in name_checker:
            pass
        else:
            refined_c_walls.append(i)
            name_checker.append(i.get("name"))

    return refined_c_walls


def get_codesk_curtain_window():
    all_window = DB.FilteredElementCollector(doc).OfCategory(
        DB.BuiltInCategory.OST_Windows).WhereElementIsElementType().ToElements()

    try:
        return [i for i in all_window if i.FamilyName == "CodeskBIM_Curtain_Window__Adaptive"].pop()

    except IndexError:
        """load the codesk curtain window family"""

        window = load_family(os.path.join(files_path.model_families, "CodeskBIM_Curtain_Window__Adaptive.rfa"),
                             transact=False)

        return window.pop() if window else None


def get_wall_from_curtain_wall(parent_gen_wall, invert_selection=False):
    """Use BoundingBoxIsInside filter to find elements with a bounding box that is contained(inside completely)
    by the given Outline in the document."""

    """Create a Outline, use a minimum and maximum XYZ point to initialize the outline."""
    cw_bb = parent_gen_wall.get_BoundingBox(None)

    offset = 0  # 0.00328 * 50
    outline = DB.Outline(XYZ(cw_bb.Min.X - offset, cw_bb.Min.Y - offset, cw_bb.Min.Z - offset),
                         XYZ(cw_bb.Max.X + offset, cw_bb.Max.Y + offset, cw_bb.Max.Z + offset))

    inside_filter = DB.BoundingBoxIntersectsFilter(outline=outline, inverted=invert_selection)

    """get list of only wall that fall within the scope"""
    search_results_ids = FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Walls).WherePasses(
        inside_filter).ToElementIds()

    """exclude the parent generic wall from the list"""
    search_results_ids.Remove(parent_gen_wall.Id)

    search_results_elements = [doc.GetElement(i) for i in search_results_ids]
    # search_results_elements = search_results.ToElements()

    """use this method if you want to include any other category of element within the scope outline"""
    # search_results = FilteredElementCollector(doc).WherePasses(inside_filter).ToElementIds()

    ui_doc.Selection.SetElementIds(search_results_ids)

    return_data = [{"parent_wall": parent_gen_wall, "curtain_wall": cw} for cw in search_results_elements]
    return return_data


def collect_curtain_walls(levels=()):
    checker = []
    collected_curtain_walls = []

    """Get all generic walls in the model from specific level"""

    if len(levels) == 0:
        refined_walls = FilteredElementCollector(doc).OfCategory(
            DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
    else:
        refined_walls = []
        for level in levels:
            """Get all generic walls in the model"""
            collector = FilteredElementCollector(doc).OfCategory(
                DB.BuiltInCategory.OST_Walls).WhereElementIsNotElementType()

            level_filter = DB.ElementLevelFilter(level.Id)
            walls_on_level = collector.WherePasses(level_filter).ToElements()

            refined_walls.extend(walls_on_level)

    """get only curtain walls"""
    generic_walls = [wall for wall in refined_walls if wall.WallType.Kind != DB.WallKind.Curtain]

    for wall in generic_walls:
        embedded_c_walls = get_wall_from_curtain_wall(wall)

        """loop through the list of curtain walls on each generic wall and collect them"""
        for cw in embedded_c_walls:
            if cw.get("curtain_wall").Id.IntegerValue in checker:
                pass
            else:
                collected_curtain_walls.append(cw)
                checker.append(cw.get("curtain_wall").Id.IntegerValue)

    return collected_curtain_walls


def replace_curtain_walls():
    checkbox_data = [{"name": i.Name, "element": i} for i in levels_collection]
    ui = CheckboxSelection(items=checkbox_data)

    ui.show_dialog()
    selected_levels = ui.selected_items

    if len(selected_levels) == 0:
        pass
    else:

        refined_c_walls = collect_curtain_walls(selected_levels)

        my_window = get_codesk_curtain_window()
        curtain_walls_to_delete = List[DB.ElementId]()

        all_walls = DB.FilteredElementCollector(doc).OfCategory(
            DB.BuiltInCategory.OST_Walls).WhereElementIsElementType().ToElements()

        previous_window = None

        for index, j in enumerate(refined_c_walls):
            parent_wall = j.get("parent_wall")
            curtain_wall = j.get("curtain_wall")

            length = curtain_wall.LookupParameter("Length")
            height = curtain_wall.LookupParameter("Unconnected Height")

            base_offset = curtain_wall.LookupParameter("Base Offset").AsValueString()
            # report = "TYPE {}\tLength: {}\tHeight: {}\tBase Offset: {}".format(index, length, height, base_offset)
            #
            # print "{}______________________________________________________________________________________".format(i)
            # print report
            # print "{}______________________________________________________________________________________\n".format(i)

            name = "{}x{}".format(length.AsValueString(), height.AsValueString())
            try:
                new_window = my_window.Duplicate(name)
            except Exception:
                new_window = [doc.GetElement(i) for i in previous_window.GetValidTypes() if
                              doc.GetElement(i).LookupParameter("Type Name").AsString() == name].pop()

            new_window.LookupParameter("Height").Set(height.AsDouble())
            new_window.LookupParameter("Width").Set(length.AsDouble())

            level = doc.GetElement(curtain_wall.LevelId)

            cw_bb = curtain_wall.get_BoundingBox(None)

            x_cord = cw_bb.Min.X + ((cw_bb.Max.X - cw_bb.Min.X) * 0.5)
            y_cord = cw_bb.Min.Y + ((cw_bb.Max.Y - cw_bb.Min.Y) * 0.5)
            z_cord = cw_bb.Min.Z

            location = XYZ(x_cord, y_cord, z_cord)
            host = parent_wall

            generic_wall_type = \
                [wall for wall in all_walls if wall.Kind != DB.WallKind.Curtain][0]
            curtain_wall.ChangeTypeId(generic_wall_type.Id)

            curtain_walls_to_delete.Add(curtain_wall.Id)

            """create the title block element and place it on the sheet"""
            previous_window = doc.Create.NewFamilyInstance(location,
                                                           new_window,
                                                           host,
                                                           level,
                                                           StructuralType.NonStructural)

        """return an IList of walls id to be deleted"""
        return curtain_walls_to_delete
    return None


t.Start()
walls_to_del = replace_curtain_walls()

"""delete the redundant curtain wall from the model"""
if walls_to_del is not None:
    doc.Delete(walls_to_del)

t.Commit()
