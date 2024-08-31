from lib.pyrevitExtensionManager import PyRevitExtensionManager, OperationType

mk = PyRevitExtensionManager()
mk.update_pyrevit_extensions_json(OperationType.add_to_json)
# mk.update_pyrevit_extensions_json(OperationType.remove_from_json)
