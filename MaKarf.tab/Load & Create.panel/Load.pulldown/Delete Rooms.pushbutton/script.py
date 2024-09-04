from Autodesk.Revit.DB import BuiltInCategory as Bic, FilteredElementCollector as Fec, Transaction

import clr

from UI.Popup import Alert
from UI.xamlFiles.CheckboxSelection import CheckboxSelection

from UI.xamlFiles.CheckBoxAndDropdown import CheckBoxAndDropdown
from UI.xamlFiles.Groupings import group_data

clr.AddReference("System")
from System.Windows import Visibility

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
t = Transaction(doc, "Revit Transaction")

rooms = Fec(doc).OfCategory(Bic.OST_Rooms).WhereElementIsNotElementType().ToElements()

if len(rooms) != 0:

    data = group_data(rooms)
    ui = CheckBoxAndDropdown(dropdown_list=data, finish_button_text_name="Delete")

    """hide the error text label if not in used"""
    ui.top_error_message.Visibility = Visibility.Collapsed
    ui.bottom_error_message.Visibility = Visibility.Collapsed
    ui.ShowDialog()

    selected_rooms = ui.selected_items
    if len(selected_rooms) != 0:

        with Transaction(doc, "Delete Rooms") as tx:
            tx.Start()

            for i in selected_rooms:
                doc.Delete(i.Id)
            tx.Commit()


else:
    Alert(title="Notification", header="No Rooms found in the Project", content="")
