
# if __name__ != "__main__":
app = __revit__.Application


def revit_version_is(version_number):
    if int(app.VersionNumber) == int(version_number):
        return True
    else:
        return False


def inspect_methods_from_revit_version(version_number):
    if version_number == 2021:
        from Revit.Revit2021 import Autodesk as Autodesk
    elif version_number == 2022:
        from Revit.Revit2022 import Autodesk as Autodesk
    elif version_number == 2023:
        from Revit.Revit2023 import Autodesk as Autodesk
    elif version_number == 2024:
        from Revit.Revit2024 import Autodesk as Autodesk
