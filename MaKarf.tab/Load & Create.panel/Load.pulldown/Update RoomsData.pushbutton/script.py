from files_path import files_path

import xlrd
from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
t = Transaction(doc, "Update Room Data")


class UpdateDataRoomsFromExcel:
    room_dicts = None
    new_construction_phase = None

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
        """unplaced room worked only for New Construction phase"""

        for rm_name in room_name:
            """ extract only the New Construction phase object"""
            for phase in doc.Phases:
                if phase.Name == "New Construction":
                    self.new_construction_phase = phase
                    break

        self.room_dicts = [
            {"r_name": r_name, "r_floor": r_floor, "r_skirting": r_skirting, "r_ceiling": r_ceiling,
             "r_wall": r_wall}
            for r_name, r_floor, r_skirting, r_ceiling, r_wall in
            zip(room_name, floor_finish, skirting, ceiling_finish, wall_finish)]

    def update_room_data(self, checker_keywords_list, room_object):
        """ assign the remaining finishes to the unplaced rooms"""
        for r_data in self.room_dicts:
            if checker(checker_keywords_list, r_data.get("r_name")):
                room_object.LookupParameter("Name").Set(room_object.LookupParameter("Name").AsString().upper())
                room_object.LookupParameter("Floor Finish").Set(r_data.get("r_floor"))
                room_object.LookupParameter("Comments").Set(r_data.get("r_skirting"))
                room_object.LookupParameter("Ceiling Finish").Set(r_data.get("r_ceiling"))
                room_object.LookupParameter("Wall Finish").Set(r_data.get("r_wall"))
                return
            else:
                # if r_data.get("r_name").upper() == "ROOM":
                room_object.LookupParameter("Name").Set(room_object.LookupParameter("Name").AsString().upper())
                room_object.LookupParameter("Floor Finish").Set(r_data.get("r_floor"))
                room_object.LookupParameter("Comments").Set(r_data.get("r_skirting"))
                room_object.LookupParameter("Ceiling Finish").Set(r_data.get("r_ceiling"))
                room_object.LookupParameter("Wall Finish").Set(r_data.get("r_wall"))
                return

    """##############################################################################################################"""
    """##############################################################################################################"""


def checker(keyword_list, room_name):
    for word in keyword_list:
        if word in room_name:
            return True


rms = Fec(doc).OfCategory(Bic.OST_Rooms).WhereElementIsNotElementType().ToElements()

washroom_keywords = ["WASH", "BATH", "TOILET", "WC", "W/C", "W/R", "WR"]
outdoor_keywords = ["LOBBY", "CORRIDOR", "VERANDA", "PORCH"]
bedroom_keywords = ["BEDROOM", "BED"]
kitchen_keywords = ["KIT", "KITCHEN"]
store_keywords = ["STO", "STORE", "STORAGE"]
living_keywords = ["LIVING", "HALL", "DINING", "FAMILY", "PLAY", "GAME", "PRAYER", "STUDY"]
office_keywords = ["OFFICE"]


def run():
    excel_rooms = UpdateDataRoomsFromExcel()
    t.Start()
    for room_obj in rms:
        name = room_obj.LookupParameter("Name").AsString().upper()
        # leve = i.LookupParameter("Level").AsValueString()
        # print(leve)

        if checker(bedroom_keywords, name):
            # print("bedroom ===  ", name)
            excel_rooms.update_room_data(bedroom_keywords, room_obj)

        elif checker(kitchen_keywords, name):
            # print("kitchen ===  ", name)
            excel_rooms.update_room_data(kitchen_keywords, room_obj)

        elif checker(washroom_keywords, name):
            # print("Wet room ===  ", name)
            excel_rooms.update_room_data(washroom_keywords, room_obj)

        elif checker(outdoor_keywords, name):
            # print("Outdoor ===  ", name)
            excel_rooms.update_room_data(outdoor_keywords, room_obj)

        elif checker(store_keywords, name):
            # print("Store room ===  ", name)
            excel_rooms.update_room_data(store_keywords, room_obj)

        elif checker(living_keywords, name):
            # print("Living room ===  ", name)
            excel_rooms.update_room_data(living_keywords, room_obj)

        elif checker(office_keywords, name):
            # print("Office room ===  ", name)
            excel_rooms.update_room_data(office_keywords, room_obj)

        else:
            # print("General Room")
            excel_rooms.update_room_data(office_keywords, room_obj)
            pass
    t.Commit()


run()
