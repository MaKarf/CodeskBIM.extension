import os

import clr

from UI.Popup import Alert
from UI.xamlFiles.CheckboxSelection import CheckboxSelection
from loadfamilies import get_families_path, load_family

clr.AddReference("System")
from System.Windows import Visibility


def Select_families():
    families_path_list = get_families_path()

    item = [{"name": os.path.basename(i), "element": i} for i in families_path_list]

    ui = CheckboxSelection(item)

    """hide the error text label if not in used"""
    ui.top_error_message.Visibility = Visibility.Collapsed
    ui.bottom_error_message.Visibility = Visibility.Collapsed
    ui.ShowDialog()

    list_of_selected_families_paths = ui.selected_items
    if len(list_of_selected_families_paths) != 0:
        if map(load_family, list_of_selected_families_paths):
            return list_of_selected_families_paths


"""report the successfully loaded families"""
successful_load_list = Select_families()
body_message = ""
if successful_load_list is not None:
    for p in successful_load_list:
        body_message += "{}\n".format(os.path.basename(p))

    Alert(title="Results", header="Successfully loaded", content=body_message)
