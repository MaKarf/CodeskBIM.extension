"""##############################################################################################################"""
import itertools
import operator

"""#################################    I   M   P   O   R   T   S     ###########################################"""
"""##############################################################################################################"""

from Autodesk.Revit.DB import FilteredElementCollector as Fec
from Autodesk.Revit.DB import BuiltInCategory as Bic
from Autodesk.Revit.DB import Transaction

# from Autodesk.Revit import DB

ui_doc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

"""##############################################################################################################"""
"""#################################    I   M   P   O   R   T   S     ###########################################"""
"""##############################################################################################################"""

"""instantiate transaction manager"""
t = Transaction(doc, "Renamedoors")

""" get collection of views from active revit document"""

door_collection = Fec(doc).OfCategory(Bic.OST_Doors).WhereElementIsNotElementType().ToElements()
window_collection = Fec(doc).OfCategory(Bic.OST_Windows).WhereElementIsNotElementType().ToElements()
collection_list = [door_collection, window_collection]


class RenameDoorsAndWindows:

    def __init__(self, collection):

        self.collection = collection
        self.list_of_elements = []
        self.list_of_elements_dicts = []
        self.dict_key = "elem"
        self.dict_value = "elem_type"
        self.rename_elements()

    """####################################################################################################"""

    def create_dicts(self):
        for door in self.collection:
            """create dictionary of Revit element to Type Mark  and populate them into the list_of_elements list"""
            self.list_of_elements.append({self.dict_key: door, self.dict_value: door.Name})

        # """call the grouping function"""
        # self.group_dicts()

    def group_dicts(self):
        # print(self.dict_value)
        self.list_of_elements = sorted(self.list_of_elements, key=operator.itemgetter(self.dict_value))

        for i, g in itertools.groupby(self.list_of_elements, key=operator.itemgetter(self.dict_value)):
            self.list_of_elements_dicts.append(list(g))

        # """call the generate function"""
        # self.generate_names()

    def generate_names(self):
        type_count = 1
        # print(len(self.list_of_elements_dicts))
        for types in self.list_of_elements_dicts:
            # for v in types:
            #     print(v.items()[1])

            if str(types[0].get(self.dict_key).Category.Name) == "Windows":
                new_type_mark = "W{}".format(type_count)
            else:
                new_type_mark = "D{}".format(type_count)

            # print(types[0].get(self.dict_key).Symbol.LookupParameter("Type Name").AsString())
            # types[0].get(self.dict_key).Name = str(new_type_mark)
            # print(types[0].get(self.dict_key).Name)
            types[0].get(self.dict_key).Symbol.LookupParameter("Type Mark").Set(str(new_type_mark))

            type_count += 1
            instant_count = 1
            for elem in types:
                # print(elem.get(self.dict_key).Name, elem.get(self.dict_value))
                elem.get(self.dict_key).LookupParameter("Mark").Set(str(instant_count))

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
    rename_d = RenameDoorsAndWindows(door_collection)
    rename_w = RenameDoorsAndWindows(window_collection)
    t.Commit()


run()
