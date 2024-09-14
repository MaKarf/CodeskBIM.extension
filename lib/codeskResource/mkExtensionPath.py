from os.path import join, dirname


def mk_extension_path():
    project_path = dirname(__file__).replace("/", "\\")
    # print("project path: {}".format(project_path))
    spl = project_path.split("\\")
    # print(spl)
    search = [i for i in spl if i.endswith(".extension")]  # 'CodeskBIM.extension'
    # print search
    if len(search) > 0:
        end = spl.index(search.pop())
        # print(end)

        new_list = spl[:end + 1]
        new_list[0] += "\\"
        # print(new_list)

        _extension_path = join(*new_list)
        # print(_extension_path)

        return _extension_path


if __name__ == "__main__":
    mk_extension_path()
