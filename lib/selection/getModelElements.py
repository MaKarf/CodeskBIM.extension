from Autodesk.Revit.DB import Element, FilteredElementCollector, BuiltInCategory
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
ui_doc = __revit__.ActiveUIDocument
active_view = ui_doc.ActiveView


class GetModelElements:
    elements = List[Element]()

    def __init__(self, built_in_category):
        self.built_in_category = built_in_category
        self.get_model_elements_max_z_height()

    def get_model_elements_max_z_height(self, height_offset=4):
        map(self.process, self.built_in_category)

        """get all the max Z co-ordinates of all the model elements in the revit project"""
        mx = [i.get_BoundingBox(active_view).Max.Z for i in self.elements if i.get_BoundingBox(active_view) is not None]

        """ get the highest Z value"""
        max_z_element = max(mx) + height_offset

        return max_z_element

    def process(self, built_in_category):
        """get all element instances from the revit project"""
        walls = FilteredElementCollector(doc).OfCategory(
            built_in_category).WhereElementIsNotElementType().ToElements()

        [self.elements.Add(el) for el in walls]


if __name__ == '__main__':
    categories = [BuiltInCategory.OST_Walls,
                  BuiltInCategory.OST_Floors,
                  BuiltInCategory.OST_GenericModel,
                  BuiltInCategory.OST_Roofs
                  ]
    GetModelElements(categories)
