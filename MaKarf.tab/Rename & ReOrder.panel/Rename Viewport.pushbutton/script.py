from Autodesk.Revit import DB

from Autodesk.Revit.DB import BuiltInCategory as Bic, ViewType
from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import Transaction

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Rename Viewports")

sheet_name_keywords = ["ELECTRIC", "PLUMBING", "POWER", "LIGHT", "WATER"]


def checker(keyword_list, sheet_name):
    for word in keyword_list:
        if word in sheet_name:
            return True


assigned_names = []



def viewport_title_on_sheet():
    sheets_collection = Fec(doc).OfCategory(Bic.OST_Sheets)
    assign_duplicate_names_counter = 1
    for sheet in sheets_collection:
        """get viewports placed on sheet"""
        vps_set = sheet.GetAllViewports()
        # print(vps_set)

        """extract/get list of viewport object from viewport ids set"""
        vps_object_list = [doc.GetElement(vps_ids) for vps_ids in vps_set]
        # print(sheet.Name, vps_object)

        """get viewport name"""
        # print(sheet.Name, [vpn.LookupParameter("View Name").AsString() for vpn in vps_object])

        """set parameter for sheets with only one viewport"""
        if len(vps_object_list) == 1:
            try:
                vps_object = vps_object_list[0]
                """ vps_object[0] get the only object in the list of viewports"""
                vps_object.LookupParameter("Title on Sheet").Set(sheet.Name)

                """ rename corresponding view names"""
                assoc_view = doc.GetElement(vps_object.ViewId)
                if assoc_view.ViewType == DB.ViewType.FloorPlan:

                    if sheet.Name in assigned_names:
                        assign_duplicate_names_counter += 1
                        assoc_view.LookupParameter("View Name").Set("{} {}".format(sheet.Name, assign_duplicate_names_counter))
                    else:
                        assoc_view.LookupParameter("View Name").Set(sheet.Name)
                    assigned_names.append(sheet.Name)

            except IndexError:
                pass

        else:
            # print(sheet.Name, "has two")
            """if "ELECTRICAL" in sheet.Name.upper() or "PLUMBING" in sheet.Name.upper():"""
            if checker(sheet_name_keywords, sheet.Name.upper()):
                v = [i for i in vps_object_list if doc.GetElement(i.ViewId).ViewType == ViewType.FloorPlan]
                if len(v) != 0:
                    # print(v)
                    """ vps_object[0] get the only object in the list of viewports"""
                    try:
                        vps_object = v[0]
                        vps_object.LookupParameter("Title on Sheet").Set(sheet.Name)

                        """ rename corresponding view names"""
                        assoc_view = doc.GetElement(vps_object.ViewId)
                        if assoc_view.ViewType == DB.ViewType.FloorPlan:

                            if sheet.Name in assigned_names:
                                assign_duplicate_names_counter += 1
                                assoc_view.LookupParameter("View Name").Set("{} {}".format(sheet.Name, assign_duplicate_names_counter))
                            else:
                                assoc_view.LookupParameter("View Name").Set(sheet.Name)
                            assigned_names.append(sheet.Name)

                    except IndexError:
                        pass
        if "SITE" in sheet.Name:
            try:
                v = [i for i in vps_object_list if doc.GetElement(i.ViewId).ViewType == ViewType.FloorPlan][0]
                """ vps_object[0] get the only object in the list of viewports"""
                v.LookupParameter("Title on Sheet").Set("{}".format(sheet.Name).replace(" & SITE", ""))
            except IndexError:
                pass


def run():
    t.Start()
    # try:
    viewport_title_on_sheet()
    # except Exception:
    #     pass
    t.Commit()


run()
