import os
import time


def mak():
    source_folder = r"D:\8.myGitHub\Git-Revit\Python4Revit\CodeskBIMpyRevit\CodeskBIM.extension\MaKarf.tab"
    for a_subdir, b_dirs, c_files in os.walk(source_folder):

        if "Dev.panel" not in a_subdir.split("\\"):
            print(a_subdir)
    print(time.time())
