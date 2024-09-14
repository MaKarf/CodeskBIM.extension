import sys

from UI.Popup import Alert

app = __revit__.Application
ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document

from Autodesk.Revit.DB import FilteredElementCollector as Fec, BuiltInCategory


def get_builtin_category_id(built_in_category):
    try:
        category_id = Fec(doc).OfCategory(built_in_category).ToElements()[0].Category.Id

        return str(category_id)
    except Exception as e:
        # print(e)
        Alert(title="Parameter Error",
              header="No Element of '{}' Category found".format(str(built_in_category).replace("OST_", "")),
              content="No element of Built-In-Category '{}' exist in this Project".format(built_in_category))
        sys.exit()


if __name__ == "__main__":
    get_builtin_category_id(BuiltInCategory.OST_Sheets)
