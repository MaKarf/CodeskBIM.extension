def run():
    import subprocess
    # import sys
    # import win32process
    # import win32con
    #
    # import ctypes
    # from pywinauto import application

    __title__ = "Project\nFolder"

    """get instance of revit active document"""
    doc = __revit__.ActiveUIDocument.Document

    """get revit file path"""
    revit_file_path = doc.PathName

    """extract only revit file name with file extension"""
    only_rvt_name = revit_file_path.split("\\")[-1]

    """remove the file name from path to get the mother folder instead"""
    project_folder = revit_file_path.replace(only_rvt_name, "")

    """open the explorer using subprocess"""
    subprocess.Popen('explorer /open, {}'.format(project_folder))

    # from pywinauto import application
    #
    # app = application.Application()
    # print(app.window())
    #
    # user32 = ctypes.WinDLL('user32')
    #
    # SW_MAXIMISE = 3
    #
    # hWnd = user32.GetForegroundWindow()
    #
    # user32.ShowWindow(hWnd, SW_MAXIMISE)


run()
