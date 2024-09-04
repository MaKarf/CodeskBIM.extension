def sorted_key(lists):
    return [x.LookupParameter("Phase").AsValueString() for x in lists]


def group_data(_list):
    check = []
    category_data = []
    sorted_rooms = sorted(_list, key=lambda x: x.LookupParameter("Phase").AsValueString())

    for rom in sorted_rooms:
        phase = rom.LookupParameter("Phase").AsValueString()
        elements_data = {"element": rom, "name": rom.LookupParameter("Name").AsString()}

        if phase not in check:
            category_data.append({"category_name": phase, "element": [elements_data]})
            check.append(phase)
        else:
            cat = list(filter(lambda x: x["category_name"] == phase, category_data)).pop()
            cat["element"].append(elements_data)

    return category_data


"""usage

rooms = Fec(doc).OfCategory(Bic.OST_Rooms).WhereElementIsNotElementType().ToElements()
data = group_data(rooms)
for el in data:
    print "______________________________________________________________________________________"
    print el["category_name"]

    for x in el["element"]:
        print x["name"]
    print "______________________________________________________________________________________\n"
"""
