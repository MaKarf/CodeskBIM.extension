import sys

from Autodesk.Revit.DB import BuiltInCategory, Transaction, ElementId, Category, IFamilyLoadOptions, FamilySource, \
    FamilyInstance, CategoryType
from Autodesk.Revit.Exceptions import ArgumentException, InvalidOperationException
from Autodesk.Revit.UI import UIApplication

from SortNatural import real_sorting
from UI.Popup import Alert
from UI.xamlFiles.CheckboxSelection import CheckboxSelection
from familyCategories import family_categories

app = __revit__.Application
ui_app = UIApplication(app)

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
revit_version = int(app.VersionNumber)
t = Transaction(doc, "Change Family Category")
selection = ui_doc.Selection.GetElementIds()


class FamilyLoadOptions(IFamilyLoadOptions):
    """A Class implementation for loading families"""

    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        """Defines behavior when a family is found in the model."""
        overwriteParameterValues = True
        return overwriteParameterValues

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        """Defines behavior when a shared family is found in the model."""
        source = FamilySource.Project
        # source = FamilySource.Family
        overwriteParameterValues = True
        return overwriteParameterValues


def swap_family_category(built_in_category):
    opened_families = []
    """###########################################################################################"""
    list_of_families = []
    """remove duplicates"""
    # print(len(selection))
    if len(selection) > 1:
        [list_of_families.append(ids) for ids in selection if
         doc.GetElement(ids).Symbol.Family not in list_of_families]
    else:
        list_of_families = selection
    """###########################################################################################"""

    for element_id in list_of_families:
        element = doc.GetElement(element_id)

        """isolate all family instances"""
        if isinstance(element, FamilyInstance):
            family_symbol = element.Symbol
            """family object found inside the project"""
            family_inside_project = element.Symbol.Family

            """proceed if selected family is in an editable state or no transaction is currently in state"""
            if family_symbol and family_symbol.Family.IsEditable:
                family_doc = doc.EditFamily(family_inside_project)

                """family object as opened in isolation"""
                own_family = family_doc.OwnerFamily

                """###########################################################################################"""
                t.Start()
                """get category id from database without reference to any selected revit element"""
                category_id = ElementId(built_in_category)
                try:
                    own_family.FamilyCategory = Category.GetCategory(doc, category_id)
                except ArgumentException:
                    Alert(title="Forbidden Attempt", header="Selected Category cannot be changed to {}".format(
                        str(built_in_category).replace("OST_", "")),
                          content="")
                    t.RollBack()
                    sys.exit()

                opened_families.append(family_doc)
                t.Commit()
                """###########################################################################################"""

    """Reload the modified family back into the project"""
    options = FamilyLoadOptions()

    for family_doc in opened_families:
        try:
            family_doc.LoadFamily(doc, options)
            """close family doc without saving it"""
            family_doc.Close(False)
        except InvalidOperationException:
            Alert(title="Cancelled", header="Operation Cancelled", content="")
            sys.exit()


def select_family_category():
    categories = doc.Settings.Categories

    categories_list = []
    for c in categories:
        if c.CategoryType == CategoryType.Model:
            if c.Name in family_categories:
                # mk = "{0} ({1})".format(c.Name, c.Id.IntegerValue)

                categories_list.append(c)

    """create a dictionary of 'name':'item name in list, 'object':'item object for post process'"""

    items = real_sorting(list_to_be_sorted=[{"element": i, "name": i.Name} for i in categories_list], dict_key="name")

    def selected_items():
        s = CheckboxSelection(items=items, selection_name="Select Category",
                              finish_button_text_name="Change Category",
                              select_multiple=False)
        s.ShowDialog()
        return s.selected_items

    sel = selected_items()

    if len(sel) != 0:
        selected_category = sel.pop()
        # print(sel.selected_items[0])
        if int(app.VersionNumber) > 2022:
            category_id = selected_category.BuiltInCategory
            """ use the class attribute from the search"""
            category = BuiltInCategory().__getattribute__(str(category_id))

            # print(category)
            return category
        else:
            # print(sel.selected_items[0].)
            # category_id = selected_category.BuiltInCategory
            # """ use the class attribute from the search"""
            # category = BuiltInCategory().__getattribute__(str(category_id))
            # #
            # # print(category)
            # return category
            Alert(title="Resolution in progress", header="Not available in Revit {}".format(app.VersionNumber),
                  content="Resolution in progress")
            return None
    return None


def run():
    category = select_family_category()

    if category:
        swap_family_category(category)


run()
