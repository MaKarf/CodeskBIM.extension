def mk_extension_path():
    import os

    project_path = os.path.dirname(__file__)
    # print("project path: {}".format(project_path))
    spl = project_path.split("\\")
    # print(spl)
    search = 'CodeskBIM.extension'

    end = spl.index(search)
    # print(end)

    new_list = spl[:end + 1]
    new_list[0] += "\\"
    # print(new_list)

    extension_path = os.path.join(*new_list)
    # print(extension_path)

    return extension_path


# mk_extension_path()
