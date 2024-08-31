import re


def real_sorting(list_to_be_sorted, dict_key=None, index=None):
    """check if members in the list to be sorted are dictionaries"""
    is_dict = False
    if isinstance(list_to_be_sorted[0], dict):
        is_dict = True

    """#####################################################################################################"""

    def natural_keys(dictionary_items):
        if is_dict:
            if index:
                """ sort by index if members are dicts"""
                text = dictionary_items.items()[index]
            else:
                """ sort by key if members are dicts"""
                text = dictionary_items.get(dict_key)
        else:
            """ sort by texts if members raw texts"""
            text = dictionary_items

        return [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]

    list_to_be_sorted.sort(key=natural_keys)

    return list_to_be_sorted


if __name__ == "__main__":
    """                             EXAMPLES WITH DIFFERENT LINT TYPES  """
    """#################################################################################################"""

    lst = ['output_01.jpg', 'output_010.jpg', 'output_011.jpg', 'output_012.jpg', 'output_013.jpg', 'output_014.jpg',
           'output_015.jpg', 'output_016.jpg', 'output_017.jpg', 'output_018.jpg', 'output_019.jpg', 'output_02.jpg',
           'output_020.jpg', 'output_03.jpg', 'output_04.jpg', 'output_05.jpg', 'output_06.jpg', 'output_07.jpg',
           'output_08.jpg', 'output_09.jpg', 't1-2.jpg', 'uc.PNG']

    lst2 = [{"mk": 'output_01.jpg'}, {"mk": 'output_010.jpg'}, {"mk": 'output_011.jpg'}, {"mk": 'output_012.jpg'},
            {"mk": 'output_013.jpg'}, {"mk": 'output_014.jpg'},
            {"mk": 'output_015.jpg'}, {"mk": 'output_016.jpg'}, {"mk": 'output_017.jpg'}, {"mk": 'output_018.jpg'},
            {"mk": 'output_019.jpg'}, {"mk": 'output_02.jpg'},
            {"mk": 'output_020.jpg'}, {"mk": 'output_03.jpg'}, {"mk": 'output_04.jpg'}, {"mk": 'output_05.jpg'},
            {"mk": 'output_06.jpg'}, {"mk": 'output_07.jpg'},
            {"mk": 'output_08.jpg'}, {"mk": 'output_09.jpg'}]

    lst3 = [{'sheet_number': '1', 'sheet_name': 'SETTING OUT & SITE'},
            {'sheet_number': '4', 'sheet_name': 'GROUND FLOOR PLAN'},
            {'sheet_number': '5', 'sheet_name': 'GF - FURNITURE LAYOUT + FINISHES'},
            {'sheet_number': '6', 'sheet_name': 'ROOF PLAN'},
            {'sheet_number': '7', 'sheet_name': 'SECTIONS'},
            {'sheet_number': '10', 'sheet_name': 'ELEVATIONS'},
            {'sheet_number': '11', 'sheet_name': 'GF - ELECTRICAL LAYOUT'},
            {'sheet_number': '12', 'sheet_name': 'GF - PLUMBING LAYOUT'},
            {'sheet_number': '32', 'sheet_name': 'DETAILS'},
            {'sheet_number': '2', 'sheet_name': 'BLOCK PLAN'},
            {'sheet_number': '8', 'sheet_name': 'ELEVATION'},
            {'sheet_number': '9', 'sheet_name': 'ELEVATION'},
            {'sheet_number': '12.COVER', 'sheet_name': 'BLOCK TWO (ONE-BEDROOM)'},
            {'sheet_number': '14', 'sheet_name': 'GROUND FLOOR PLAN'},
            {'sheet_number': '15', 'sheet_name': 'GF - FURNITURE LAYOUT + FINISHES'},
            {'sheet_number': '16', 'sheet_name': 'ROOF PLAN'},
            {'sheet_number': '17', 'sheet_name': 'SECTIONS'},
            {'sheet_number': '18', 'sheet_name': 'ELEVATION'},
            {'sheet_number': '19', 'sheet_name': 'ELEVATION'},
            {'sheet_number': '20', 'sheet_name': 'GF - ELECTRICAL LAYOUT'},
            {'sheet_number': '21', 'sheet_name': 'GF - PLUMBING LAYOUT'},
            {'sheet_number': '21.COVER', 'sheet_name': 'BLOCK THREE (TWO-BEDROOM)'},
            {'sheet_number': '23', 'sheet_name': 'GROUND FLOOR PLAN'},
            {'sheet_number': '24', 'sheet_name': 'GF - FURNITURE LAYOUT + FINISHES'},
            {'sheet_number': '25', 'sheet_name': 'ROOF PLAN'},
            {'sheet_number': '26', 'sheet_name': 'SECTIONS'},
            {'sheet_number': '27', 'sheet_name': 'ELEVATION'},
            {'sheet_number': '28', 'sheet_name': 'ELEVATION'},
            {'sheet_number': '29', 'sheet_name': 'GF - PLUMBING LAYOUT'},
            {'sheet_number': '30', 'sheet_name': 'GF - ELECTRICAL LAYOUT'},
            {'sheet_number': '31', 'sheet_name': 'DOORS & WINDOWS SCHEDULE'},
            {'sheet_number': '3', 'sheet_name': 'FOUNDATION PLAN'},
            {'sheet_number': '13', 'sheet_name': 'FOUNDATION PLAN'},
            {'sheet_number': '22', 'sheet_name': 'FOUNDATION PLAN'}]

    r = real_sorting(list_to_be_sorted=lst)
    print(r)

    s = real_sorting(list_to_be_sorted=lst2, dict_key="mk")
    print(s)

    u = real_sorting(list_to_be_sorted=lst3, dict_key='sheet_number')
    print(u)
