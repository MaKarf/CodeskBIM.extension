def generate_data_from_list(list_of_element):
    return [{"name": i["name"], "element": i} for i in list_of_element]


def generate_data_from_dict(dictionary_data):
    return [{"name": i[0], "element": i[1]} for i in dictionary_data.items()]
