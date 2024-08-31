app = __revit__.Application


def get_path():
    from os.path import dirname
    family_path = dirname(__file__).replace(r"codeskResource",
                                            r"\families\MK_Annotation Families\{}".format(app.VersionNumber))

    return dirname(__file__)
