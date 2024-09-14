def to_vertical_string(list_of_strings):
    return "".join(["{}\n".format(item) for item in list_of_strings])


def to_horizontal_string(list_of_strings):
    return "".join(
        [("{}, ".format(item) if list_of_strings.index(item) != len(list_of_strings) - 1 else "{}".format(item))
         for item in list_of_strings])
