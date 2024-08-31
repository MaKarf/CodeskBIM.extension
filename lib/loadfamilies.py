import os

import Autodesk.Revit.DB

import clr

from Autodesk.Revit.DB import IFamilyLoadOptions, FamilySource, Transaction

from lib.UI.xamlFiles.CheckboxSelection import CheckboxSelection
from lib.files_path import version_specific_files_path

annotation_families_folder = version_specific_files_path.annotation_families

doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application
family_loaded = clr.Reference[Autodesk.Revit.DB.Family]()

"""
Family Loader

- loads families into project with a path and file name.
- implements IFamilyLoadOptions to silence OverwriteParamaterValue dialogue box.

Requires rpw library: github.com/gtalarico/revitpythonwrapper

Author: Grant Foster | github.com/grantdfoster
"""


class FamilyLoadOptions(IFamilyLoadOptions):
    """A Class implementation for loading families"""

    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        """Defines behavior when a family is found in the model."""
        overwriteParameterValues = True
        return True

    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        """Defines behavior when a shared family is found in the model."""
        source = FamilySource.Project
        # source = FamilySource.Family
        overwriteParameterValues = True
        return True


def get_families_path(specific_category=()):
    """Loads a family into the Revit project with path and file name."""

    # print(annotation_families_folder)
    if specific_category is None:
        specific_category = []
    if os.path.exists(annotation_families_folder) is False:
        return 'Path does not exist.'
    # cate = "Grid"
    path_list = []
    # def prep_path_list():
    for filepath in os.listdir(annotation_families_folder):
        # print(filepath,)
        if filepath[-4:] == ".rfa" and filepath[-9:-7] != ".0":
            if len(specific_category) == 0:
                path_list.append(os.path.join(annotation_families_folder, filepath))
                # print(os.path.join(annotation_families_folder, filepath))
            else:
                """if search categories matches then load those specific families"""

                def serach_and_load(category):
                    """extract only the category names from the family name"""
                    checker = filepath.replace("_", " ").split(" ")
                    # print(checker)
                    if category in checker:
                        # print(filepath)
                        path_list.append(os.path.join(annotation_families_folder, filepath))

                map(serach_and_load, specific_category)
    return path_list


def load_family(full_path, transact=True):
    t = Transaction(doc)

    if transact:
        t.Start('Load Family')

    loaded = doc.LoadFamily(full_path, FamilyLoadOptions(), family_loaded)
    if loaded:
        family = family_loaded.Value
        symbols = []

        for family_symbol_id in family.GetFamilySymbolIds():
            family_symbol = doc.GetElement(family_symbol_id)
            symbols.append(family_symbol)

        for s in symbols:
            # print(s)
            try:
                s.Activate()
            except:
                pass

        if transact:
            t.Commit()
        return symbols

    else:
        if transact:
            t.Commit()
        # print('Family already exists in project.')
        return



