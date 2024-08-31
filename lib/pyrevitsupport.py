"""#pylint: disable=import-error,invalid-name,broad-except,superfluous-parens"""

import os
from os.path import join

import clr


def get_pyrevit_master_path():
    p = {i for i in os.environ.get("PATH").split(";") if "pyRevit-Master" in i}
    if p:
        path = p.pop()
        # print path
        return path
    else:
        # print None
        return None


def get_dlls_from_path(path):
    ls = [join(path, i) for i in os.listdir(path) if i.endswith(".dll")]

    # print("Printing DLLS from \t {} \t \n______________________{}_______________________".format(path, len(ls)))
    # for p in ls:
    #     print p
    # print("_____________________________________________\n")
    return ls


def get_pyrevit_ipy_dlls():
    dlls = list()
    folder = r"C:\Users\Debbie\AppData\Roaming\pyRevit-Master\bin\engines\IPY273"
    for i in os.listdir(folder):
        full_path = join(folder, i)
        # print full_path
        dlls.append(full_path)
    return dlls


def filter_dlls(container_list, ref_list):
    # filter()
    new_list = list()

    [new_list.append(i) for i in container_list
     if os.path.basename(i) not in [os.path.basename(j) for j in ref_list]
     ]

    # """print new list"""
    # print("Printing New List\n______________________{}_______________________".format(len(new_list)))
    # for item in new_list:
    #     print item
    # print("_____________________________________________\n")

    return new_list


def add_dll_references(dll_list):
    """ add a reference to your C# .dll"""
    if isinstance(dll_list, list):
        for dll in dll_list:
            # print "[ADDING]: {}".format(dll)
            try:
                clr.AddReferenceToFileAndPath(dll)
                # print "[ADDED]: {}".format(dll)
            except:
                # print "[FAILED]: {}".format(dll)
                pass

    else:
        try:
            clr.AddReferenceToFileAndPath(dll_list)
            # print "[ADDED]: {}".format(dll_list)
        except:
            # print "[FAILED]: {}".format(dll_list)
            pass


def process():
    codesk_dlls_folder = r"{}\Autodesk\Revit\Addins\{}\CodeskBIMRevit".format(os.environ.get("APPDATA"), 2021)
    # print codesk_dlls_folder
    codesk_dlls = get_dlls_from_path(codesk_dlls_folder)

    pyrevit_master_path = get_pyrevit_master_path()
    pyrevit_dlls = get_dlls_from_path(pyrevit_master_path)

    # print pyrevit_master_path
    pyrevit_ipy_folder = join(pyrevit_master_path, "engines", "IPY273")
    pyrevit_ipy_dlls = get_dlls_from_path(pyrevit_ipy_folder)

    combined_pyrevit_dlls = pyrevit_dlls
    combined_pyrevit_dlls.extend(pyrevit_ipy_dlls)

    pyrevit_dlls_to_add = filter_dlls(combined_pyrevit_dlls, codesk_dlls)

    """add dlls to reference"""
    add_dll_references(pyrevit_dlls_to_add)


if __name__ == "__main__":
    process()

# import clr
# import sys
# import os
#
# folder = r"C:\Users\Debbie\AppData\Roaming\pyRevit-Master\bin\engines\IPY273"
# for i in os.listdir(folder):
#     full_path = os.path.join(folder, i)
#     print full_path
#     sys.path.append(full_path)
#     clr.AddReferenceToFileAndPath(full_path)
#
# Sqlite3 = None
# from Community.CsharpSqlite import Sqlite3 as Sqlite3  # this import sqlite3 properly
#
# import Sqlite3
#
# print(Sqlite3.sqlite3_version)
#
# # import pyrevit
