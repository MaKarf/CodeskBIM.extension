"""##############################################################################################################"""
import itertools
import operator

"""#################################    I   M   P   O   R   T   S     ###########################################"""
"""##############################################################################################################"""

from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import Transaction

from Autodesk.Revit import DB

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

"""##############################################################################################################"""
"""#################################    I   M   P   O   R   T   S     ###########################################"""
"""##############################################################################################################"""

"""instantiate transaction manager"""
t = Transaction(doc, "Rename windows")


class RenameWindow:
    collection = Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsNotElementType().ToElements()
    renamable_types = []

    def __init__(self):
        self.get_renamable_types()
        self.rename_door_types()
        self.list_of_elements = []
        self.list_of_elements_dicts = []
        self.elem_obj_dict_key = "elem"
        self.elem_type_obj_dict_key = "elem_type"
        self.rename_elements()

    """####################################################################################################"""

    def get_renamable_types(self):
        type_list = []
        type_list_N = []
        for i in Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsNotElementType().ToElements():
            """create dictionary of Revit element to Type Mark  and populate them into the list_of_elements list"""
            type_list.append({"element_object": i, "element_type": i.Name})

        """sort dicts"""
        type_list = sorted(type_list, key=operator.itemgetter("element_type"))
        """ group dicts by name"""
        for k, g in itertools.groupby(type_list, key=operator.itemgetter("element_type")):
            type_list_N.append(list(g)[0])

        """######################################################################################################"""
        placed_element_types = []
        for tp in type_list_N:
            tt_id = tp.get("element_object").GetTypeId()
            tt = doc.GetElement(tt_id)
            tt_name = tt.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            placed_element_types.append({"element": tt, "element_name": tt_name})
            # print(tt_name)

        """######################################################################################################"""
        all_element_types = []
        # print("\n\n\n")
        for eleme in Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsElementType().ToElements():
            all_ee_name = eleme.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            all_element_types.append({"element": eleme, "element_name": all_ee_name})
            # print(all_ee_name)

        """######################################################################################################"""
        renamable_types = []

        def renamable(name):
            # rename_able = []
            for items in all_element_types:
                if items.get("element_name") == name.get("element_name"):
                    # print("Selected {}".format(items))
                    renamable_types.append(items)

        """ get all rename-able element types placed in the model and leave the unplaced types untouched"""
        map(renamable, placed_element_types)
        """assign results to class parameter to be used by other methods"""
        self.renamable_types = renamable_types

    def rename_door_types(self):
        """ RENAME FAMILY TYPES"""
        for m in self.renamable_types:
            count = self.renamable_types.index(m) + 1

            window_width = m.get("element").get_Parameter(DB.BuiltInParameter.WINDOW_WIDTH).AsValueString().replace(",", "")
            window_height = m.get("element").get_Parameter(DB.BuiltInParameter.WINDOW_HEIGHT).AsValueString().replace(",", "")
            # window_name = m.get("element").get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
            dimension = "({}mm x {}mm)".format(window_width, window_height)

            m.get("element").Name = "Window Type {} {}".format(count, dimension)
            # print(dimension, window_name)
        """####################################################################################################"""
        """ RENAME MARKS AND TYPE MARKS"""
        """####################################################################################################"""

    def create_dicts(self):
        for window in self.collection:
            """create dictionary of Revit element to Type Mark  and populate them into the list_of_elements list"""
            self.list_of_elements.append({self.elem_obj_dict_key: window, self.elem_type_obj_dict_key: window.Name})

    def group_dicts(self):
        # print(self.elem_type_obj_dict_key)
        self.list_of_elements = sorted(self.list_of_elements, key=operator.itemgetter(self.elem_type_obj_dict_key))

        for i, g in itertools.groupby(self.list_of_elements, key=operator.itemgetter(self.elem_type_obj_dict_key)):
            self.list_of_elements_dicts.append(list(g))

    def generate_names(self):
        type_count = 1
        # print(len(self.list_of_elements_dicts))

        for types in self.list_of_elements_dicts:
            el = types[0].get(self.elem_obj_dict_key)
            el_type = types[0].get(self.elem_type_obj_dict_key)
            """extract door type number from door type name"""
            if el_type[14] == "(":
                type_mark_number = el_type[12]
                # print(type_mark_number)
                new_type_mark = "W{}".format(type_mark_number)
                el.Symbol.LookupParameter("Type Mark").Set(str(new_type_mark))

            elif el_type[15] == "(":
                type_mark_number = el_type[12:14]
                # print(type_mark_number)
                new_type_mark = "W{}".format(type_mark_number)
                el.Symbol.LookupParameter("Type Mark").Set(str(new_type_mark))

            elif el_type[16] == "(":
                type_mark_number = el_type[13:15]
                new_type_mark = "W{}".format(type_mark_number)
                el.Symbol.LookupParameter("Type Mark").Set(str(new_type_mark))

            type_count += 1
            instant_count = 1
            for elem in types:
                elem.get(self.elem_obj_dict_key).LookupParameter("Mark").Set(str(instant_count))
                instant_count += 1

    def rename_elements(self):
        self.create_dicts()
        self.group_dicts()
        self.generate_names()

    """####################################################################################################"""
    """ END OF RENAME MARKS AND TYPE MARKS"""
    """####################################################################################################"""


def run():
    t.Start()
    rename_w = RenameWindow()
    t.Commit()


run()
