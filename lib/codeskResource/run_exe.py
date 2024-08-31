
def launch_exe(file_name):
    import os
    """ the path to the CodeskBIM.extension folder"""
    from codeskResource.mkExtensionPath import mk_extension_path

    extension_path = mk_extension_path()

    ex = r"lib\exe_files\{}".format(file_name)
    exe_path = os.path.join(extension_path, ex)
    # print(exe_path)
    # print(exe_path)
    os.startfile(exe_path)


