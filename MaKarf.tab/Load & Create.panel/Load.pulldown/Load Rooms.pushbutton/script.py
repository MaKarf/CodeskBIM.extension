from files_path import files_path

import xlrd
from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction

from UI.xamlFiles.DropDownSelection import DropDownSelection
from AppMethods import Alert

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Load Rooms")

tbs = Fec(doc).OfCategory(Bic.OST_TitleBlocks).WhereElementIsElementType().ToElements()[0]
title_block_id = tbs.GetTypeId


class LoadRoomsFromExcel:

    def __init__(self):
        """instantiate a workbook"""
        self.my_book = xlrd.open_workbook(files_path.excel_file)

        # self.create_sheets()
        self.read_sheets()

    def read_sheets(self):
        """ set selected worksheet for further processing"""
        my_sheet = self.my_book.sheet_by_name("Finishes")

        room_name = my_sheet.col_values(0)
        floor_finish = my_sheet.col_values(1)
        skirting = my_sheet.col_values(2)
        ceiling_finish = my_sheet.col_values(3)
        wall_finish = my_sheet.col_values(4)

        # print(room_name)
        # print(floor_finish)
        # print(skirting)
        # print(ceiling_finish)
        # print(wall_finish)

        """the phase to be used in addition to create unplaced room"""
        phases_data_list = [{"name": phase.Name, "element": phase} for phase in doc.Phases]
        select_phase_ui = DropDownSelection(title="Assign phase to Rooms", label_name="Select Phase",
                                            dropdown_list=phases_data_list)
        selected_phase = select_phase_ui.selected_item.Value

        if selected_phase is not None:

            room_dicts = [
                {"r_name": r_name, "r_floor": r_floor, "r_skirting": r_skirting, "r_ceiling": r_ceiling,
                 "r_wall": r_wall}
                for r_name, r_floor, r_skirting, r_ceiling, r_wall in
                zip(room_name, floor_finish, skirting, ceiling_finish, wall_finish)]

            """ assign the remaining finishes to the unplaced rooms"""
            t.Start()
            for r_data in room_dicts:
                # print(r_data)
                unplaced_room = doc.Create.NewRoom(selected_phase)
                # print(unplaced_room)
                unplaced_room.LookupParameter("Name").Set(r_data.pop("r_name"))
                unplaced_room.LookupParameter("Floor Finish").Set(r_data.pop("r_floor"))
                unplaced_room.LookupParameter("Comments").Set(r_data.pop("r_skirting"))
                unplaced_room.LookupParameter("Ceiling Finish").Set(r_data.pop("r_ceiling"))
                unplaced_room.LookupParameter("Wall Finish").Set(r_data.pop("r_wall"))
            t.Commit()

            Alert(title="Success", header="Successfully loaded rooms",
                  content="Assigned to phase: {}".format(selected_phase.Name))

    """##############################################################################################################"""
    """##############################################################################################################"""


LoadRoomsFromExcel()
