class EngineType:
    def __init__(self):
        pass

    codesk_engine = 1
    pyrevit_engine = 2


def get_engine_type():
    """if the add-in is called from CodeskBIMRevit addin, __basePath__ will return a value
            else NameError exception will be thrown because pyrevit does not know __basePath__"""
    try:
        var = __basePath__
        return EngineType.codesk_engine
    except NameError:
        return EngineType.pyrevit_engine
