import codecs
import json
import os
from collections import OrderedDict

from lib.pyrevitsupport import get_pyrevit_master_path


class OperationType:
    remove_from_json = 1
    add_to_json = 2

    def __init__(self):
        pass


class PyRevitExtensionManager:
    """##########################################################################################################"""
    __tab_name = "MaKarf"
    __reserved_extension = {

        "builtin": "False",
        "type": "extension",
        "rocket_mode_compatible": "True",
        "name": __tab_name,
        "description": "Set of custom buttons to automate the preparation of but not limited to working drawings.",
        "author": "Christopher Makafui Agbodzah",
        "author_profile": "https://www.linkedin.com/in/makarf",
        "url": "https://github.com/MaKarf/pyCodesk/.git",
        "website": "",
        "image": "",
        "dependencies": []
    }

    # __extension = {}
    __pyrevit_extension_data = {}

    def __init__(self):
        pt = r"E:\CodeskBIMRevitAddinSetup\pyCodeskKitchen\hazdobga\engineAndTabs\CodeskBIM.extension\extension.json"
        self.__extension = self.__load_json(pt)
        pyrevit_bin_path = get_pyrevit_master_path()
        pyrevit_master_path = pyrevit_bin_path.replace("bin", "")

        pyrevit_extensions_folder = os.path.join(pyrevit_master_path, "extensions")
        self.__pyrevit_extensions_json = os.path.join(pyrevit_extensions_folder, "extensions.json")
        # print(self.__pyrevit_extensions_json)

    def update_pyrevit_extensions_json(self, operation_type):
        """ codesk pyRevit extension data"""

        """ open pyRevit extension.json file to be updated with codesk extension data"""
        if os.path.exists(self.__pyrevit_extensions_json):
            self.__pyrevit_extension_data = self.__load_json(self.__pyrevit_extensions_json)
            list_of_tabs = self.__pyrevit_extension_data["extensions"]

            if operation_type == OperationType.add_to_json:
                if not self.__tab_exist(list_of_tabs):
                    self.__pyrevit_extension_data["extensions"].append(self.__extension)

                    self.__update_extension_data()
                    print("Added [{}] to pyrevit extensions".format(self.__tab_name))
                else:
                    print("Cannot add additional [{}]".format(self.__tab_name))

            elif operation_type == OperationType.remove_from_json:
                if self.__tab_exist(list_of_tabs):
                    self.__pyrevit_extension_data["extensions"] = [i for i in
                                                                   self.__pyrevit_extension_data["extensions"] if
                                                                   i["name"] != self.__tab_name]
                    print("Removed [{}] from pyrevit extensions".format(self.__tab_name))
                    self.__update_extension_data()
                else:
                    print("Removal of [{}] ignored".format(self.__tab_name))
            else:
                pass

    def __tab_exist(self, list_of_tabs):
        for tabs in list_of_tabs:
            if tabs["name"] == self.__tab_name:
                print("[{}] found in pyrevit extensions".format(self.__tab_name))
                return True
        print("[{}] not in pyrevit extensions".format(self.__tab_name))
        return False

    def __update_extension_data(self):
        """ Save the updated data back to the JSON file"""
        with codecs.open(self.__pyrevit_extensions_json, 'w', encoding='utf-8') as json_file:
            json.dump(self.__pyrevit_extension_data, json_file, indent=4, ensure_ascii=False)
            """ print results"""
            json_file.close()

    def __create_json(self):
        # """ create codesk plugin extension.json file"""
        # """ create codesk plugin extension.json file"""
        # json_path = os.path.join(os.path.abspath(""), "codesk", "CodeskBIM.extension", "extension.json")
        # try:
        #     with open(json_path, "w") as ex_ten_sion:
        #         # with open("codesk/CodeskBIM.extension/extension.json", "w") as ex_ten_sion:
        #         json.dump(self.extension, ex_ten_sion, indent=4)
        #         return True
        # except Exception as e_3:
        #     # self.root.sm.get_screen("home").ids.error_id.text = str(e_3)
        #     print(e_3)
        #     return False
        pass

    @staticmethod
    def __load_json(path):
        if os.path.exists(path):
            with codecs.open(path, 'r', encoding='utf-8') as json_file:
                return json.load(json_file, object_pairs_hook=OrderedDict)


if __name__ == "__main__":
    mk = PyRevitExtensionManager()
    mk.update_pyrevit_extensions_json(OperationType.add_to_json)
    # mk.update_pyrevit_extensions_json(OperationType.remove_from_json)
