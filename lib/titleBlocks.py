from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory as Bic, Transaction, ViewSheet, XYZ, \
    FamilyInstance
from Autodesk.Revit.Exceptions import ArgumentException

from SortNatural import real_sorting
from UI.Popup import Alert
from UI.xamlFiles.CheckboxSelection import CheckboxSelection

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document


def get_title_blocks(document=doc):
    all_tbs = Fec(document).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()
    title_block_families = []
    control_list = []
    for tbl in all_tbs:
        if tbl.Family.Name not in control_list:
            control_list.append(tbl.Family.Name)
            title_block_families.append({"name": tbl.Family.Name, "element": tbl.Family})

    sorted_tbs = real_sorting(list_to_be_sorted=title_block_families, dict_key="name")
    return sorted_tbs


def create_sheets(sheets, selected_title_block_family):
    t = Transaction(doc, "Create sheets")
    t.Start()
    try:
        for sheet_dicts in sheets:
            new_sheet = ViewSheet.Create(doc, selected_title_block_family.GetTypeId())

            """get a single title block from a list of its types"""
            t_block = [doc.GetElement(i) for i in selected_title_block_family.GetFamilySymbolIds()][0]

            """create the title block element and place it on the sheet"""
            doc.Create.NewFamilyInstance(XYZ(0, 0, 0), t_block, new_sheet)

            new_sheet.Name = sheet_dicts.get("sheet_name")
            new_sheet.Name.upper()
            new_sheet.SheetNumber = sheet_dicts.get("sheet_number")

        t.Commit()

    except ArgumentException:
        t.RollBack()
        Alert(title="Sheet Number Error", header="Same sheet number detected",
              content="Some sheets number are already used in existing sheets")

    """ set the active view to the first sheet in the created sheet list"""
    ui_doc.ActiveView = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().FirstElement()


def organize_sheets(selected_title_block_family):
    t = Transaction(doc, "Organize sheets")
    project_title_blocks = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()
    t.Start()
    try:
        title_block_types = selected_title_block_family.GetFamilySymbolIds()

        ttb_types_dicts = [{"obj": doc.GetElement(i), "ids": i,
                            "name": doc.GetElement(i).LookupParameter("Type Name").AsString()}
                           for i in title_block_types]

        if len(title_block_types) == 6:
            """title_block_compatibility = True"""

            for title_block in project_title_blocks:
                sheet_name = title_block.LookupParameter("Sheet Name").AsString().upper()
                sheet_number = title_block.LookupParameter("Sheet Number").AsString().upper()
                """ use the appropriate title block type if it was designed by MaKarf"""
                if "MAIN COVER" in sheet_name:
                    rep = [i.get("ids") for i in ttb_types_dicts if i.get("name") == "3DS COVER PAGE"][0]
                    title_block.ChangeTypeId(rep)

                elif sheet_name == "COVER PAGE":
                    rep = [i.get("ids") for i in ttb_types_dicts if i.get("name") == "MAIN COVER PAGE"][0]
                    title_block.ChangeTypeId(rep)

                elif "INDEX" in sheet_name or "LIST" in sheet_name:
                    rep = [i.get("ids") for i in ttb_types_dicts if i.get("name") == "INDEX PAGE"][0]
                    title_block.ChangeTypeId(rep)

                elif "3D" in sheet_name or "3D VIEW" in sheet_name:
                    rep = [i.get("ids") for i in ttb_types_dicts if i.get("name") == "3DS COVER PAGE"][0]
                    title_block.ChangeTypeId(rep)

                elif ".COVER" in str(sheet_number).upper():
                    rep = [i.get("ids") for i in ttb_types_dicts if i.get("name") == "DRAWING TYPE COVER"][0]
                    title_block.ChangeTypeId(rep)

                else:
                    rep = \
                        [i.get("ids") for i in ttb_types_dicts if i.get("name") == "DRAWINGS TITLE BLOCK"][0]
                    title_block.ChangeTypeId(rep)
        else:
            [i.ChangeTypeId([i.get("ids") for i in ttb_types_dicts][0]) for i in project_title_blocks]

        t.Commit()

    except ArgumentException:
        t.RollBack()


def get_title_block_on_sheet():
    """get all sheets for display"""
    sheets = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()

    """generate sheet data"""
    sheets_data = [{"name": "{} - {}".format(i.SheetNumber, i.Name), "element": i} for i in sheets]

    """display sheets on UI"""
    check = CheckboxSelection(select_multiple=False, items=sheets_data)
    check.show_dialog()

    """"get selected sheet"""
    sheet = check.selected_items.pop() if check.selected_items else None

    dependants = sheet.GetDependentElements(None) if sheet is not None else None

    title_block = [doc.GetElement(i) for i in dependants if type(doc.GetElement(i)) == FamilyInstance and
                   doc.GetElement(i).Category.Name == "Title Blocks"].pop() if dependants else None

    """##############################################################################################"""
    """return title block on the selected sheet ensure to return none id locked or ui was cancelled"""
    """##############################################################################################"""
    return title_block if not check.lock else None


def get_title_block_with_sheet(provided_sheet=None):

    if provided_sheet is None:
        """get all sheets for display"""
        sheets = Fec(doc).OfCategory(Bic.OST_Sheets).WhereElementIsNotElementType().ToElements()

        """generate sheet data"""
        sheets_data = [{"name": "{} - {}".format(i.SheetNumber, i.Name), "element": i} for i in sheets]

        """display sheets on UI"""
        check = CheckboxSelection(select_multiple=False, items=sheets_data)
        check.show_dialog()

        """"get selected sheet"""
        sheet = check.selected_items.pop() if check.selected_items else None

        dependants = sheet.GetDependentElements(None) if sheet is not None else None

        title_block_and_sheet = [{"sheet": sheet, "title_block": doc.GetElement(i)} for i in dependants if
                                 type(doc.GetElement(i)) == FamilyInstance and
                                 doc.GetElement(i).Category.Name == "Title Blocks"].pop() if dependants else None

        """##############################################################################################"""
        """return title block on the selected sheet ensure to return none id locked or ui was cancelled"""
        """##############################################################################################"""
        return title_block_and_sheet if not check.lock else None
    else:
        sheet = provided_sheet

        dependants = sheet.GetDependentElements(None) if sheet is not None else None

        title_block_and_sheet = [{"sheet": sheet, "title_block": doc.GetElement(i)} for i in dependants if
                                 type(doc.GetElement(i)) == FamilyInstance and
                                 doc.GetElement(i).Category.Name == "Title Blocks"].pop() if dependants else None

        """##############################################################################################"""
        """return title block on the selected sheet ensure to return none id locked or ui was cancelled"""
        """##############################################################################################"""
        return title_block_and_sheet
